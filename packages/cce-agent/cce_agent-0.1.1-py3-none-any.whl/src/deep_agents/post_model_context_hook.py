"""
Post-model context management hook for deepagents integration.

Since deepagents doesn't support pre_model_hook, we adapt our context management
to work with the post-model approval middleware after each model call.
"""

import logging
from typing import Any, Dict, List

from langchain_core.messages.utils import count_tokens_approximately, trim_messages

logger = logging.getLogger(__name__)


def _intelligently_trim_files(
    files_dict: dict[str, str], max_tokens: int, enable_logging: bool = True
) -> dict[str, str]:
    """
    Intelligently trim files by prioritizing important files and using summaries.

    Args:
        files_dict: Dictionary of file paths to content
        max_tokens: Maximum tokens allowed for files
        enable_logging: Whether to enable logging

    Returns:
        Trimmed files dictionary
    """
    if not isinstance(files_dict, dict):
        return files_dict

    # Separate files by importance
    important_files = {}
    test_files = {}
    other_files = {}

    for file_path, content in files_dict.items():
        # Skip the full content cache
        if file_path == "__full_content_cache__":
            continue

        if "test" in file_path.lower():
            test_files[file_path] = content
        elif any(
            core in file_path.lower() for core in ["cce_deep_agent", "state", "context_manager", "memory", "agent.py"]
        ):
            important_files[file_path] = content
        else:
            other_files[file_path] = content

    # Start with important files
    trimmed_files = {}
    current_tokens = 0

    # Add important files first
    for file_path, content in important_files.items():
        file_tokens = count_tokens_approximately([{"content": content}])
        if current_tokens + file_tokens <= max_tokens:
            trimmed_files[file_path] = content
            current_tokens += file_tokens
        else:
            if enable_logging:
                logger.debug(f"🚫 [FILE TRIMMING] Excluded important file due to token limit: {file_path}")

    # Add other files if we have room
    for file_path, content in other_files.items():
        file_tokens = count_tokens_approximately([{"content": content}])
        if current_tokens + file_tokens <= max_tokens:
            trimmed_files[file_path] = content
            current_tokens += file_tokens
        else:
            if enable_logging:
                logger.debug(f"🚫 [FILE TRIMMING] Excluded other file due to token limit: {file_path}")

    # Add test files if we have room
    for file_path, content in test_files.items():
        file_tokens = count_tokens_approximately([{"content": content}])
        if current_tokens + file_tokens <= max_tokens:
            trimmed_files[file_path] = content
            current_tokens += file_tokens
        else:
            if enable_logging:
                logger.debug(f"🚫 [FILE TRIMMING] Excluded test file due to token limit: {file_path}")

    # Preserve the full content cache if it exists
    if "__full_content_cache__" in files_dict:
        trimmed_files["__full_content_cache__"] = files_dict["__full_content_cache__"]

    if enable_logging:
        logger.info(f"🎯 [FILE TRIMMING] Intelligent trimming results:")
        logger.info(
            f"   Important files: {len(important_files)} → {len([f for f in trimmed_files if f in important_files])}"
        )
        logger.info(f"   Other files: {len(other_files)} → {len([f for f in trimmed_files if f in other_files])}")
        logger.info(f"   Test files: {len(test_files)} → {len([f for f in trimmed_files if f in test_files])}")
        logger.info(f"   Total tokens used: {current_tokens}/{max_tokens}")

    return trimmed_files


def create_context_management_post_hook(
    max_tokens: int = 80000,  # More aggressive limit - 40% of 200k to ensure we stay under
    strategy: str = "last",
    enable_logging: bool = True,
) -> callable:
    """
    Create a post-model hook that manages context after each model call.

    This works by:
    1. Monitoring context size after each model call
    2. If context gets too large, trimming it for the next iteration
    3. Storing trimmed context in state for future reference

    Args:
        max_tokens: Maximum tokens to allow in context
        strategy: Trimming strategy ("last" keeps recent messages)
        enable_logging: Whether to enable detailed logging

    Returns:
        Post-model hook function
    """

    def post_model_hook(state: dict[str, Any]) -> dict[str, Any]:
        """
        Post-model hook that manages context size.

        Args:
            state: Current agent state (can be dict or Pydantic model)

        Returns:
            Updated state with context management
        """
        try:
            # Handle both dict and Pydantic model states
            if hasattr(state, "messages"):
                messages = state.messages
            else:
                messages = state.get("messages", [])

            if not messages:
                return state

            current_tokens = count_tokens_approximately(messages)

            if enable_logging:
                logger.info(f"🔍 [POST-HOOK] Context check: {len(messages)} messages, {current_tokens} tokens")

            # If context is within limits, no action needed
            if current_tokens <= max_tokens:
                if enable_logging:
                    logger.debug(f"✅ [POST-HOOK] Context within limit ({current_tokens} <= {max_tokens})")
                return state

            # Context is too large - trim it
            if enable_logging:
                logger.info(f"🔧 [POST-HOOK] Context too large ({current_tokens} > {max_tokens}), trimming...")

            # Trim messages using LangChain utility
            trimmed_messages = trim_messages(
                messages,
                strategy=strategy,
                token_counter=count_tokens_approximately,
                max_tokens=max_tokens,
                start_on="human",
                end_on=("human", "tool"),
            )

            trimmed_tokens = count_tokens_approximately(trimmed_messages)
            reduction_percentage = (
                ((current_tokens - trimmed_tokens) / current_tokens) * 100 if current_tokens > 0 else 0
            )

            if enable_logging:
                logger.info(f"✅ [POST-HOOK] Context trimmed:")
                logger.info(f"   Messages: {len(messages)} → {len(trimmed_messages)}")
                logger.info(f"   Tokens: {current_tokens} → {trimmed_tokens}")
                logger.info(f"   Reduction: {reduction_percentage:.1f}%")

            # Update state with trimmed messages
            if hasattr(state, "messages"):
                # Pydantic model - update directly
                state.messages = trimmed_messages
                updated_state = state
            else:
                # Dictionary - create copy and update
                updated_state = state.copy()
                updated_state["messages"] = trimmed_messages

            # CRITICAL: Also trim the files field if it exists and is too large
            files_field = "files" if "files" in updated_state else None
            if files_field and updated_state[files_field]:
                files_content = str(updated_state[files_field])
                files_tokens = count_tokens_approximately([{"content": files_content}])

                if enable_logging:
                    logger.info(f"🔍 [POST-HOOK] Files field check: {files_tokens} tokens")

                # If files field is too large, trim it intelligently
                max_files_tokens = max_tokens // 3  # Use only 1/3 of token budget for files (more aggressive)
                if files_tokens > max_files_tokens:
                    if enable_logging:
                        logger.info(
                            f"🔧 [POST-HOOK] Files field too large ({files_tokens} > {max_files_tokens}), applying intelligent trimming..."
                        )

                    # Apply intelligent file trimming
                    trimmed_files = _intelligently_trim_files(
                        updated_state[files_field], max_files_tokens, enable_logging
                    )

                    updated_state[files_field] = trimmed_files

                    final_files_tokens = count_tokens_approximately([{"content": str(trimmed_files)}])
                    files_reduction = (
                        ((files_tokens - final_files_tokens) / files_tokens) * 100 if files_tokens > 0 else 0
                    )

                    if enable_logging:
                        logger.info(f"✅ [POST-HOOK] Files field intelligently trimmed:")
                        logger.info(f"   Files: {len(updated_state[files_field])} → {len(trimmed_files)}")
                        logger.info(f"   Tokens: {files_tokens} → {final_files_tokens}")
                        logger.info(f"   Reduction: {files_reduction:.1f}%")

            # Ensure we don't break tool use/result message pairs
            # Only trim if we have a reasonable number of messages left
            if len(trimmed_messages) < 2:
                if enable_logging:
                    logger.warning("⚠️ [POST-HOOK] Too few messages after trimming, reverting to original")
                return state

            # Store trimming statistics in state if supported
            if hasattr(state, "trimming_stats"):
                state.trimming_stats = {
                    "original_messages": len(messages),
                    "trimmed_messages": len(trimmed_messages),
                    "original_tokens": current_tokens,
                    "trimmed_tokens": trimmed_tokens,
                    "reduction_percentage": reduction_percentage,
                    "method": "post_model_trimming",
                    "files_trimmed": files_field is not None and updated_state.get(files_field) is not None,
                }

            return updated_state

        except Exception as e:
            logger.error(f"❌ [POST-HOOK] Error in context management: {e}")
            return state

    return post_model_hook


def create_adaptive_post_hook(
    max_tokens: int = 80000,  # More aggressive limit - 40% of 200k to ensure we stay under
    enable_logging: bool = True,
) -> callable:
    """
    Create an adaptive post-model hook that can handle both trimming and summarization.

    Args:
        max_tokens: Maximum tokens to allow in context
        enable_logging: Whether to enable detailed logging

    Returns:
        Adaptive post-model hook function
    """

    def adaptive_post_hook(state: dict[str, Any]) -> dict[str, Any]:
        """
        Adaptive post-model hook that chooses the best context management strategy.
        """
        try:
            # Handle both dict and Pydantic model states
            if hasattr(state, "messages"):
                messages = state.messages
            else:
                messages = state.get("messages", [])

            if not messages:
                return state

            current_tokens = count_tokens_approximately(messages)

            if enable_logging:
                logger.info(
                    f"🧠 [ADAPTIVE POST-HOOK] Context analysis: {len(messages)} messages, {current_tokens} tokens"
                )

            # If context is within limits, no action needed
            if current_tokens <= max_tokens:
                if enable_logging:
                    logger.debug(f"✅ [ADAPTIVE POST-HOOK] Context within limit")
                return state

            # Try summarization first if available
            try:
                import os

                # Create a simple model for summarization (we'll use a basic one)
                from langchain_anthropic import ChatAnthropic

                from .context_summarization import create_summarization_hook

                model = ChatAnthropic(
                    model="claude-3-haiku-20240307", temperature=0, api_key=os.getenv("ANTHROPIC_API_KEY")
                )

                summarization_hook = create_summarization_hook(
                    model=model, max_tokens=max_tokens, max_summary_tokens=128
                )

                # Apply summarization
                result = summarization_hook(state)

                if "llm_input_messages" in result:
                    summarized_messages = result["llm_input_messages"]
                    summarized_tokens = count_tokens_approximately(summarized_messages)

                    if enable_logging:
                        logger.info(f"🧠 [ADAPTIVE POST-HOOK] Summarization successful:")
                        logger.info(f"   Messages: {len(messages)} → {len(summarized_messages)}")
                        logger.info(f"   Tokens: {current_tokens} → {summarized_tokens}")

                    # Update state with summarized messages
                    if hasattr(state, "messages"):
                        # Pydantic model - update directly
                        state.messages = summarized_messages
                        return state
                    else:
                        # Dictionary - create copy and update
                        updated_state = state.copy()
                        updated_state["messages"] = summarized_messages
                        return updated_state

            except Exception as e:
                if enable_logging:
                    logger.warning(f"⚠️ [ADAPTIVE POST-HOOK] Summarization failed: {e}, falling back to trimming")

            # Fallback to simple trimming
            trimming_hook = create_context_management_post_hook(max_tokens=max_tokens, enable_logging=enable_logging)
            return trimming_hook(state)

        except Exception as e:
            logger.error(f"❌ [ADAPTIVE POST-HOOK] Error in adaptive context management: {e}")
            return state

    return adaptive_post_hook
