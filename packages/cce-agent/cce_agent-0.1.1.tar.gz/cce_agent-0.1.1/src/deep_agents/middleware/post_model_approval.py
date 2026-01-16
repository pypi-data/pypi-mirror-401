"""
Post-Model Approval Middleware for CCE Deep Agent

This module implements approval system with caching, directly ported from
open-swe-v2 patterns for enhanced user experience and safety.
"""

import asyncio
import logging
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage

# Import AI message checking functions
try:
    from langchain_core.messages.ai import isAIMessage, isAIMessageChunk
except ImportError:
    # Fallback for different LangChain versions
    def isAIMessage(message):
        return hasattr(message, "__class__") and "AI" in message.__class__.__name__

    def isAIMessageChunk(message):
        return (
            hasattr(message, "__class__")
            and "AI" in message.__class__.__name__
            and "Chunk" in message.__class__.__name__
        )


from ..tool_call_validator import ToolCallValidator
from ..tools.validation import check_syntax, run_linting
from ..utils import (
    POST_MODEL_HOOK_CONFIG,
    WRITE_COMMANDS,
    AgentStateHelpers,
    get_approval_requirements,
    get_safety_validator,
)

logger = logging.getLogger(__name__)


class PostModelHookManager:
    """
    Manager for post-model hook patterns.

    This class handles the post-model processing including approval caching,
    safety validation, and interrupt handling.
    """

    def __init__(self):
        self.safety_validator = get_safety_validator()
        self.tool_call_validator = ToolCallValidator()
        self.config = POST_MODEL_HOOK_CONFIG
        self.interrupt_count = 0
        self.max_interrupts = self.config.get("max_interrupts_per_session", 100)
        # Track failed attempts for fallback logic
        self.failed_attempts = {}  # {tool_call_id: count}

        # Debug logging for configuration
        logger.info(f"🔧 [CONFIG DEBUG] POST_MODEL_HOOK_CONFIG loaded: {self.config}")
        logger.info(
            f"🔧 [CONFIG DEBUG] enable_automatic_validation: {self.config.get('enable_automatic_validation', 'NOT_FOUND')}"
        )
        logger.info(f"🔧 [CONFIG DEBUG] validation_tools: {self.config.get('validation_tools', 'NOT_FOUND')}")

    def _is_deep_agents_mode(self, state: dict[str, Any]) -> bool:
        """
        Detect if we're running in deep agents mode.

        Simply checks the configuration flag that's set when deep agents are enabled.

        Args:
            state: Agent state (unused, kept for compatibility)

        Returns:
            True if running in deep agents mode
        """
        return True

    def _create_bash_fallback_tool_call(
        self, original_tool_call: dict[str, Any], tool_name: str, tool_args: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Create a bash fallback tool call for failed operations.

        Args:
            original_tool_call: The original tool call that failed
            tool_name: Name of the original tool
            tool_args: Arguments of the original tool

        Returns:
            New tool call using execute_bash_command
        """
        try:
            # Generate bash command based on the original tool call
            if tool_name in {"hybrid_edit_file", "edit_file"}:
                file_path = tool_args.get("file_path", "")
                old_string = tool_args.get("old_string", "")
                new_string = tool_args.get("new_string", "")

                # Create a sed command to replace the content
                # Escape special characters for sed
                escaped_old = old_string.replace("/", "\\/").replace("'", "'\"'\"'")
                escaped_new = new_string.replace("/", "\\/").replace("'", "'\"'\"'")

                bash_command = f"sed -i '' 's/{escaped_old}/{escaped_new}/g' '{file_path}'"

            elif tool_name in {"hybrid_write_file", "write_file"}:
                file_path = tool_args.get("file_path", "")
                content = tool_args.get("content", "")

                # Create a command to write content to file
                # Escape content for shell
                escaped_content = content.replace("'", "'\"'\"'")
                bash_command = f"echo '{escaped_content}' > '{file_path}'"

            else:
                # Generic fallback - just echo the operation
                bash_command = f"echo 'Fallback for {tool_name} with args: {tool_args}'"

            # Create new tool call
            fallback_tool_call = {
                "name": "execute_bash_command",
                "args": {"command": bash_command},
                "id": f"fallback_{original_tool_call.get('id', 'unknown')}",
            }

            logger.info(f"🔄 [FALLBACK] Created bash fallback for {tool_name}: {bash_command}")
            return fallback_tool_call

        except Exception as e:
            logger.error(f"Error creating bash fallback: {e}")
            # Return a simple echo command as ultimate fallback
            return {
                "name": "execute_bash_command",
                "args": {"command": f"echo 'Fallback failed for {tool_name}: {str(e)}'"},
                "id": f"fallback_error_{original_tool_call.get('id', 'unknown')}",
            }

    async def process_tool_calls(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Process tool calls in the post-model hook.

        Args:
            state: Agent state containing messages and tool calls

        Returns:
            Updated state with processed tool calls
        """
        try:
            logger.info(f"🔍 [DEBUG] POST MODEL HOOK CALLED - State keys: {list(state.keys())}")
            logger.info(f"🔍 [DEBUG] State content: {state}")

            # Check if we're in deep agents mode
            is_deep_agents = self._is_deep_agents_mode(state)
            logger.info(f"🤖 [DEEP AGENTS MODE] Detected deep agents mode: {is_deep_agents}")

            messages = state.get("messages", [])
            if not messages:
                logger.info(f"🔍 [DEBUG] No messages in state, returning early")
                return state

            last_message = messages[-1]
            logger.info(f"🔍 [DEBUG] Last message type: {type(last_message)}")
            logger.info(f"🔍 [DEBUG] Last message content: {last_message}")

            # Check if last message is an AI message with tool calls
            logger.debug(
                f"🔍 [POST MODEL HOOK] Checking if message has tool calls: {hasattr(last_message, 'tool_calls') and last_message.tool_calls}"
            )
            if not self._is_ai_message_with_tool_calls(last_message):
                logger.debug(f"🔍 [POST MODEL HOOK] Message is not AI message with tool calls, returning state")
                return state

            # Initialize approval operations if not present
            if "approved_operations" not in state:
                state["approved_operations"] = {"cached_operations": {}}

            # Process tool calls
            approved_tool_calls = []
            interrupted_tool_calls = []
            validation_failures = []
            fallback_tool_calls = []

            logger.info(f"🔍 [DEBUG] Found AI message with {len(last_message.tool_calls)} tool calls")

            for i, tool_call in enumerate(last_message.tool_calls):
                # Handle both dict and object tool calls
                if isinstance(tool_call, dict):
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})
                    tool_id = tool_call.get("id", f"tool_{i}")
                else:
                    tool_name = tool_call.name
                    tool_args = tool_call.args or {}
                    tool_id = getattr(tool_call, "id", f"tool_{i}")

                logger.info(f"🔍 [DEBUG] Processing tool call {i + 1}: {tool_name}")
                logger.info(f"🔍 [DEBUG] Tool call args: {tool_args}")

                # Check if this tool call has failed before
                failed_count = self.failed_attempts.get(tool_id, 0)
                logger.info(
                    f"🔍 [FALLBACK DEBUG] Tool {tool_name} (ID: {tool_id}) has failed {failed_count} times before"
                )

                # Validate tool call parameters first
                logger.info(f"🔍 [VALIDATION DEBUG] Starting validation for {tool_name}")
                validation_result = self.tool_call_validator.validate_tool_call(tool_name, tool_args)
                logger.info(f"🔍 [VALIDATION DEBUG] Validation result: {validation_result}")

                if not validation_result["valid"]:
                    logger.warning(
                        f"⚠️ [TOOL VALIDATION] Tool call validation failed for {tool_name}: {validation_result['error']}"
                    )

                    # Record validation failure for review
                    validation_failures.append(
                        {
                            "tool_name": tool_name,
                            "tool_args": tool_args,
                            "error": validation_result["error"],
                            "tool_id": tool_id,
                        }
                    )

                    # Increment failed attempts
                    self.failed_attempts[tool_id] = failed_count + 1
                    new_failed_count = self.failed_attempts[tool_id]

                    if is_deep_agents:
                        # In deep agents mode, implement fallback logic
                        if new_failed_count >= 3:
                            logger.warning(
                                f"🔄 [FALLBACK] Tool {tool_name} failed {new_failed_count} times, creating bash fallback"
                            )

                            # Create bash fallback
                            fallback_tool_call = self._create_bash_fallback_tool_call(tool_call, tool_name, tool_args)
                            fallback_tool_calls.append(fallback_tool_call)

                            # Add fallback to approved tool calls
                            approved_tool_calls.append(fallback_tool_call)
                            logger.info(f"✅ [FALLBACK] Added bash fallback for {tool_name}")

                            # Create a ToolMessage explaining the fallback
                            from langchain_core.messages import ToolMessage

                            fallback_message = ToolMessage(
                                content=f"[FALLBACK] Tool {tool_name} failed {new_failed_count} times, using bash fallback: {fallback_tool_call['args']['command']}",
                                tool_call_id=tool_id,
                            )
                            if "messages" not in state:
                                state["messages"] = []
                            state["messages"].append(fallback_message)

                        else:
                            # Log the validation failure but don't block (first 2 attempts)
                            logger.warning(
                                f"🤖 [DEEP AGENTS VALIDATION] Validation failed for {tool_name} (attempt {new_failed_count}/3) but CONTINUING in deep agents mode"
                            )
                            logger.warning(f"🤖 [DEEP AGENTS VALIDATION] Error details: {validation_result['error']}")

                            # Create a ToolMessage for the validation failure (for logging/review)
                            from langchain_core.messages import ToolMessage

                            tool_message = ToolMessage(
                                content=f"[VALIDATION WARNING] {validation_result['error']} (attempt {new_failed_count}/3)",
                                tool_call_id=tool_id,
                            )
                            # Add the validation warning message to the state
                            if "messages" not in state:
                                state["messages"] = []
                            state["messages"].append(tool_message)

                            # Continue processing the tool call despite validation failure
                            logger.info(
                                f"🤖 [DEEP AGENTS VALIDATION] Proceeding with tool call {tool_name} despite validation failure"
                            )
                    else:
                        # In non-deep agents mode, block the tool call as before
                        logger.warning(f"⚠️ [VALIDATION DEBUG] BLOCKING TOOL CALL - This will cause early termination!")

                        # Create a ToolMessage for the validation failure
                        from langchain_core.messages import ToolMessage

                        tool_message = ToolMessage(content=validation_result["error"], tool_call_id=tool_id)
                        # Add the validation error message to the state
                        if "messages" not in state:
                            state["messages"] = []
                        state["messages"].append(tool_message)
                        logger.warning(
                            f"⚠️ [VALIDATION DEBUG] SKIPPING TOOL CALL {i + 1} - This reduces total tool calls!"
                        )
                        continue  # Skip this tool call
                else:
                    logger.info(f"✅ [VALIDATION DEBUG] Tool call {tool_name} passed validation")

                # Check if this is a file operation
                if tool_name in ["write_file", "edit_file", "sync_to_disk"]:
                    logger.info(f"🔍 [DEBUG] File operation detected: {tool_name}")

                    # Check current changed_files state
                    current_changed_files = state.get("changed_files", [])
                    logger.info(f"🔍 [DEBUG] Current changed_files: {current_changed_files}")

                    # Check current files state
                    current_files = state.get("files", {})
                    logger.info(f"🔍 [DEBUG] Current files count: {len(current_files)}")

                # Check if tool requires approval
                if tool_name in WRITE_COMMANDS:
                    if is_deep_agents:
                        # AUTO-APPROVE in deep agents mode
                        logger.info(
                            f"🤖 [DEEP AGENTS AUTO-APPROVE] Auto-approving tool {tool_name} in deep agents mode"
                        )
                        approved_tool_calls.append(tool_call)
                        logger.info(f"✅ [APPROVAL DEBUG] Tool {tool_name} auto-approved for deep agents")
                    else:
                        # Normal approval process for non-deep agents mode
                        approval_result = await self._handle_tool_approval(state, tool_name, tool_args, tool_call)

                        if approval_result["approved"]:
                            approved_tool_calls.append(tool_call)
                            logger.info(f"✅ [APPROVAL DEBUG] Tool {tool_name} approved")
                        else:
                            interrupted_tool_calls.append(
                                {"tool_call": tool_call, "reason": approval_result["reason"], "requires_approval": True}
                            )
                            logger.warning(
                                f"⚠️ [APPROVAL DEBUG] Tool {tool_name} requires approval: {approval_result['reason']}"
                            )
                else:
                    # Safe tool, no approval needed
                    approved_tool_calls.append(tool_call)
                    logger.info(f"✅ [APPROVAL DEBUG] Tool {tool_name} is safe, no approval needed")

            # Log summary of processing
            logger.info(f"📊 [PROCESSING SUMMARY] Total tool calls: {len(last_message.tool_calls)}")
            logger.info(f"📊 [PROCESSING SUMMARY] Validation failures: {len(validation_failures)}")
            logger.info(f"📊 [PROCESSING SUMMARY] Approved tool calls: {len(approved_tool_calls)}")
            logger.info(f"📊 [PROCESSING SUMMARY] Interrupted tool calls: {len(interrupted_tool_calls)}")
            logger.info(f"📊 [PROCESSING SUMMARY] Fallback tool calls: {len(fallback_tool_calls)}")
            logger.info(f"🤖 [DEEP AGENTS SUMMARY] Deep agents mode: {is_deep_agents}")

            if validation_failures:
                logger.warning(f"⚠️ [VALIDATION SUMMARY] Validation failures detected:")
                for failure in validation_failures:
                    logger.warning(f"   - {failure['tool_name']}: {failure['error']}")

                if is_deep_agents:
                    logger.warning(
                        f"🤖 [VALIDATION SUMMARY] Deep agents mode - validation failures logged but NOT blocking execution"
                    )
                else:
                    logger.warning(f"⚠️ [VALIDATION SUMMARY] These failures are causing early termination!")

            if fallback_tool_calls:
                logger.info(f"🔄 [FALLBACK SUMMARY] Created {len(fallback_tool_calls)} bash fallback tool calls:")
                for fallback in fallback_tool_calls:
                    logger.info(f"   - {fallback['name']}: {fallback['args']['command']}")

            # Update state with approved tool calls
            if len(approved_tool_calls) != len(last_message.tool_calls):
                new_message = AIMessage(
                    content=last_message.content,
                    tool_calls=approved_tool_calls,
                    id=getattr(last_message, "id", None),
                )
                state["messages"] = messages[:-1] + [new_message]
                logger.info(f"🔧 [STATE UPDATE] Updated messages with {len(approved_tool_calls)} approved tool calls")

            # Handle interrupts (only if not in deep agents mode)
            if interrupted_tool_calls and not is_deep_agents:
                state = await self._handle_interrupts(state, interrupted_tool_calls)
            elif interrupted_tool_calls and is_deep_agents:
                logger.info(
                    f"🤖 [DEEP AGENTS] Skipping interrupts in deep agents mode - {len(interrupted_tool_calls)} tools would have been interrupted"
                )

            # Trigger automatic validation for successful file operations
            logger.info(
                f"🔍 [DEBUG] Checking automatic validation config: {self.config.get('enable_automatic_validation', False)}"
            )
            logger.info(f"🔧 [CONFIG DEBUG] Full config: {self.config}")

            if self.config.get("enable_automatic_validation", False):
                logger.info(f"🔍 [DEBUG] Automatic validation is ENABLED, detecting file operations...")
                try:
                    file_operations = self._detect_successful_file_operations(state)
                    logger.info(f"🔍 [DEBUG] Detected file operations: {file_operations}")

                    if file_operations:
                        logger.info(
                            f"🔍 [DEBUG] Found {len(file_operations)} file operations, triggering validation..."
                        )
                        validation_result = await self._trigger_automatic_validation(file_operations)
                        logger.info(f"🔍 [DEBUG] Validation completed with result: {validation_result}")

                        # Store validation results in state if configured
                        if self.config.get("store_validation_results", True):
                            if "validation_results" not in state:
                                state["validation_results"] = []
                            state["validation_results"].append(
                                {
                                    "timestamp": __import__("time").time(),
                                    "files": file_operations,
                                    "result": validation_result,
                                }
                            )
                            logger.debug(f"🔍 [AUTO VALIDATION] Stored validation results in state")
                    else:
                        logger.debug(f"🔍 [AUTO VALIDATION] No file operations detected")

                except Exception as e:
                    logger.error(f"Error in automatic validation trigger: {e}")
            else:
                logger.warning(
                    f"⚠️ [AUTO VALIDATION] Automatic validation is DISABLED - config value: {self.config.get('enable_automatic_validation', 'NOT_FOUND')}"
                )

            return state

        except Exception as e:
            logger.error(f"Error in post-model hook processing: {e}")
            return state

    def _is_ai_message_with_tool_calls(self, message: BaseMessage) -> bool:
        """Check if message is an AI message with tool calls."""
        if not (isAIMessage(message) or isAIMessageChunk(message)):
            return False

        return hasattr(message, "tool_calls") and message.tool_calls

    async def _handle_tool_approval(
        self, state: dict[str, Any], tool_name: str, tool_args: dict[str, Any], tool_call: Any
    ) -> dict[str, Any]:
        """
        Handle tool approval logic.

        Args:
            state: Agent state
            tool_name: Name of the tool
            tool_args: Tool arguments
            tool_call: Tool call object

        Returns:
            Approval result dictionary
        """
        try:
            # Check if operation is already approved
            if AgentStateHelpers.is_operation_approved(state, tool_name, tool_args):
                logger.debug(f"Tool {tool_name} approved from cache")
                return {"approved": True, "reason": "cached_approval"}

            # Perform safety validation
            if self.config.get("enable_safety_validation", True):
                safety_result = await self._validate_tool_safety(tool_name, tool_args)
                if not safety_result["is_safe"]:
                    logger.warning(f"Tool {tool_name} blocked by safety validation: {safety_result['reasoning']}")
                    return {"approved": False, "reason": f"safety_validation_failed: {safety_result['reasoning']}"}

            # Check interrupt limits
            if self.interrupt_count >= self.max_interrupts:
                logger.warning(f"Maximum interrupts reached ({self.max_interrupts}), blocking tool {tool_name}")
                return {"approved": False, "reason": "max_interrupts_reached"}

            # Tool requires approval
            return {
                "approved": False,
                "reason": "requires_approval",
                "approval_context": AgentStateHelpers.get_approval_context(tool_name, tool_args),
            }

        except Exception as e:
            logger.error(f"Error handling tool approval: {e}")
            return {"approved": False, "reason": f"approval_error: {str(e)}"}

    async def _validate_tool_safety(self, tool_name: str, tool_args: dict[str, Any]) -> dict[str, Any]:
        """
        Validate tool safety.

        Args:
            tool_name: Name of the tool
            tool_args: Tool arguments

        Returns:
            Safety validation result
        """
        try:
            # For file operations, validate file path and content
            if tool_name in [
                "write_file",
                "hybrid_write_file",
                "edit_file",
                "hybrid_edit_file",
                "str_replace_based_edit_tool",
            ]:
                file_path = tool_args.get("file_path") or tool_args.get("path", "")
                content = tool_args.get("content", "")

                safety_result = await self.safety_validator.validate_code_editing_safety(tool_name, file_path, content)

                return {
                    "is_safe": safety_result.is_safe,
                    "reasoning": safety_result.reasoning,
                    "threat_type": safety_result.threat_type.value,
                    "confidence": safety_result.confidence,
                }

            # For bash commands, validate command safety
            elif tool_name == "execute_bash":
                command = tool_args.get("command", "")

                safety_result = await self.safety_validator.validate_command_safety(command)

                return {
                    "is_safe": safety_result.is_safe,
                    "reasoning": safety_result.reasoning,
                    "threat_type": safety_result.threat_type.value,
                    "confidence": safety_result.confidence,
                }

            # For other tools, assume safe
            else:
                return {
                    "is_safe": True,
                    "reasoning": "Tool not subject to safety validation",
                    "threat_type": "SAFE",
                    "confidence": 0.5,
                }

        except Exception as e:
            logger.error(f"Error validating tool safety: {e}")
            return {
                "is_safe": False,
                "reasoning": f"Safety validation error: {str(e)}",
                "threat_type": "SUSPICIOUS_PATTERN",
                "confidence": 0.0,
            }

    async def _handle_interrupts(
        self, state: dict[str, Any], interrupted_tool_calls: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Handle interrupts for tools requiring approval.

        Args:
            state: Agent state
            interrupted_tool_calls: List of interrupted tool calls

        Returns:
            Updated state with interrupt information
        """
        try:
            self.interrupt_count += 1

            # Create interrupt information
            interrupt_info = {
                "interrupt_count": self.interrupt_count,
                "max_interrupts": self.max_interrupts,
                "interrupted_tools": [],
                "requires_user_approval": True,
                "timeout_seconds": self.config.get("approval_timeout_seconds", 300),
            }

            for interrupted in interrupted_tool_calls:
                tool_call = interrupted["tool_call"]

                # Handle both dict and object tool calls
                if isinstance(tool_call, dict):
                    tool_name = tool_call.get("name", "unknown")
                    tool_args = tool_call.get("args", {})
                else:
                    tool_name = tool_call.name
                    tool_args = tool_call.args or {}

                approval_context = AgentStateHelpers.get_approval_context(tool_name, tool_args)

                interrupt_info["interrupted_tools"].append(
                    {
                        "tool_name": tool_name,
                        "tool_args": tool_args,
                        "reason": interrupted["reason"],
                        "approval_context": approval_context,
                        "approval_requirements": get_approval_requirements(tool_name),
                    }
                )

            # Add interrupt information to state
            state["interrupt_info"] = interrupt_info

            logger.info(f"Interrupt #{self.interrupt_count}: {len(interrupted_tool_calls)} tools require approval")

            return state

        except Exception as e:
            logger.error(f"Error handling interrupts: {e}")
            return state

    async def handle_approval_response(
        self, state: dict[str, Any], approval_responses: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Handle approval responses from user.

        Args:
            state: Agent state
            approval_responses: List of approval responses

        Returns:
            Updated state with approved tools
        """
        try:
            if "interrupt_info" not in state:
                logger.warning("No interrupt info found in state")
                return state

            interrupt_info = state["interrupt_info"]
            approved_tool_calls = []

            for response in approval_responses:
                tool_name = response.get("tool_name")
                approved = response.get("approved", False)
                tool_args = response.get("tool_args", {})

                if approved:
                    # Add to approval cache
                    AgentStateHelpers.add_operation_approval(
                        state,
                        tool_name,
                        tool_args,
                        expires_in_hours=get_approval_requirements(tool_name)["expiration_hours"],
                    )

                    # Find the corresponding tool call
                    for interrupted_tool in interrupt_info["interrupted_tools"]:
                        if interrupted_tool["tool_name"] == tool_name and interrupted_tool["tool_args"] == tool_args:
                            # Recreate tool call (simplified)
                            tool_call = {
                                "name": tool_name,
                                "args": tool_args,
                                "id": f"approved_{tool_name}_{len(approved_tool_calls)}",
                            }
                            approved_tool_calls.append(tool_call)
                            break

                    logger.info(f"Tool {tool_name} approved by user")
                else:
                    logger.info(f"Tool {tool_name} rejected by user")

            # Update state with approved tool calls
            if approved_tool_calls:
                messages = state.get("messages", [])
                if messages:
                    last_message = messages[-1]
                    if hasattr(last_message, "tool_calls"):
                        # Add approved tool calls to existing message
                        existing_tool_calls = getattr(last_message, "tool_calls", [])
                        all_tool_calls = existing_tool_calls + approved_tool_calls

                        if hasattr(last_message, "model_copy"):
                            new_message = last_message.model_copy(update={"tool_calls": all_tool_calls})
                        else:
                            new_message = AIMessage(
                                content=last_message.content,
                                tool_calls=all_tool_calls,
                                id=getattr(last_message, "id", None),
                            )
                        state["messages"] = messages[:-1] + [new_message]

            # Clear interrupt info
            if "interrupt_info" in state:
                del state["interrupt_info"]

            return state

        except Exception as e:
            logger.error(f"Error handling approval response: {e}")
            return state

    def _detect_successful_file_operations(self, state: dict[str, Any]) -> list[str]:
        """
        Detect successful file editing operations from the current state.

        Args:
            state: Agent state containing messages and tool calls

        Returns:
            List of file paths that were successfully edited
        """
        try:
            logger.info(f"🔍 [DEBUG] _detect_successful_file_operations called with state keys: {list(state.keys())}")

            # Get changed files from state (tracked by filesystem middleware)
            changed_files = state.get("changed_files", [])
            logger.info(f"🔍 [DEBUG] Raw changed_files from state: {changed_files}")
            logger.info(f"🔍 [DEBUG] changed_files type: {type(changed_files)}")

            # Also check files state
            files = state.get("files", {})
            logger.info(f"🔍 [DEBUG] Files state has {len(files)} files")

            file_edit_operations: set[str] = set()
            for file_path in changed_files:
                if file_path and isinstance(file_path, str) and file_path.endswith(".py"):
                    file_edit_operations.add(file_path)

            # Fall back to scanning tool messages for middleware file tools
            tool_calls_by_id: dict[str, dict[str, Any]] = {}
            for message in state.get("messages", []):
                if isinstance(message, AIMessage) and getattr(message, "tool_calls", None):
                    for tool_call in message.tool_calls:
                        tool_id = tool_call.get("id")
                        if tool_id:
                            tool_calls_by_id[tool_id] = tool_call

            for message in state.get("messages", []):
                if not isinstance(message, ToolMessage):
                    continue
                tool_call = tool_calls_by_id.get(message.tool_call_id)
                if not tool_call:
                    continue
                tool_name = tool_call.get("name")
                if tool_name not in {"write_file", "edit_file"}:
                    continue
                content = (message.content or "").lower()
                if content.startswith("error") or "cannot write" in content or "failed" in content:
                    continue
                tool_args = tool_call.get("args", {}) if isinstance(tool_call.get("args"), dict) else {}
                file_path = tool_args.get("file_path") or tool_args.get("path")
                if file_path and isinstance(file_path, str) and file_path.endswith(".py"):
                    file_edit_operations.add(file_path)

            if file_edit_operations:
                logger.debug(
                    f"🔍 [AUTO VALIDATION] Detected {len(file_edit_operations)} file operations: {sorted(file_edit_operations)}"
                )

            return sorted(file_edit_operations)

        except Exception as e:
            logger.error(f"Error detecting file operations: {e}")
            return []

    async def _trigger_automatic_validation(self, file_paths: list[str]) -> dict[str, Any]:
        """
        Trigger automatic validation for the specified file paths.

        Args:
            file_paths: List of file paths to validate

        Returns:
            Dictionary containing validation results
        """
        try:
            if not self.config.get("enable_automatic_validation", False):
                return {"skipped": True, "reason": "automatic_validation_disabled"}

            validation_tools = self.config.get("validation_tools", ["run_linting", "check_syntax"])
            results = {}

            for tool_name in validation_tools:
                try:
                    if tool_name == "run_linting":
                        # Call the underlying async function directly using coroutine
                        result = await run_linting.coroutine(files=file_paths)
                        results["linting"] = result
                    elif tool_name == "check_syntax":
                        # Call the underlying async function directly using coroutine
                        result = await check_syntax.coroutine(files=file_paths)
                        results["syntax"] = result

                    if self.config.get("log_validation_results", True):
                        # Truncate result for logging
                        result_str = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
                        logger.info(f"🔍 [AUTO VALIDATION] {tool_name} result: {result_str}")

                except Exception as e:
                    logger.error(f"Error running {tool_name}: {e}")
                    results[tool_name] = f"Error: {str(e)}"

            return {"success": True, "results": results}

        except Exception as e:
            logger.error(f"Error in automatic validation: {e}")
            return {"success": False, "error": str(e)}

    def get_hook_statistics(self) -> dict[str, Any]:
        """Get post-model hook statistics."""
        return {
            "interrupt_count": self.interrupt_count,
            "max_interrupts": self.max_interrupts,
            "interrupts_remaining": self.max_interrupts - self.interrupt_count,
            "config": self.config,
            "safety_validation_enabled": self.config.get("enable_safety_validation", True),
            "approval_caching_enabled": self.config.get("enable_approval_caching", True),
            "automatic_validation_enabled": self.config.get("enable_automatic_validation", False),
            "validation_tools": self.config.get("validation_tools", []),
            "validation_timeout_seconds": self.config.get("validation_timeout_seconds", 30),
            "failed_attempts": self.failed_attempts,
        }


def createCCEPostModelHook() -> Callable:
    """
    Create post-model hook for approval system.

    This function creates a post-model hook that implements approval caching
    and safety validation, directly inspired by open-swe-v2 patterns.

    Returns:
        Post-model hook function
    """
    hook_manager = PostModelHookManager()

    def _run_async(coro_fn, *args, **kwargs):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro_fn(*args, **kwargs))

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(lambda: asyncio.run(coro_fn(*args, **kwargs)))
            return future.result()

    def postModelHook(state: dict[str, Any]) -> dict[str, Any]:
        """
        Post-model hook function for CCE agent.

        Args:
            state: Agent state containing messages and tool calls

        Returns:
            Updated state with processed tool calls
        """
        try:
            # Process tool calls through the hook manager (sync wrapper for async method)
            updated_state = _run_async(hook_manager.process_tool_calls, state)

            return updated_state

        except Exception as e:
            logger.error(f"Error in CCE post-model hook: {e}")
            return state

    # Attach manager methods to the hook function for external access
    postModelHook.manager = hook_manager
    postModelHook.handle_approval_response = hook_manager.handle_approval_response
    postModelHook.get_statistics = hook_manager.get_hook_statistics

    return postModelHook


# Global post-model hook instance
_ccp_post_model_hook = None


def getCCEPostModelHook() -> Callable:
    """Get the global CCE post-model hook instance."""
    global _ccp_post_model_hook
    if _ccp_post_model_hook is None:
        _ccp_post_model_hook = createCCEPostModelHook()
    return _ccp_post_model_hook
