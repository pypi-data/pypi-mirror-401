"""
Main CCE Deep Agent Implementation.

This module creates the main deep agent orchestrator for the CCE system,
integrating all sub-agents and providing LLM-based code editing capabilities.
"""

import copy
import logging
import os
from typing import Any, Dict, Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None

# Note: langchain.globals was removed in langchain 1.x.
# Configure verbosity via environment variables or logging instead.
if load_dotenv:
    load_dotenv()
else:
    logging.getLogger(__name__).debug("python-dotenv not installed; skipping .env load")

from deepagents.graph import BASE_AGENT_PROMPT
from deepagents.middleware.patch_tool_calls import PatchToolCallsMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

# ADD: Import existing integration infrastructure
from .middleware.filesystem import create_filesystem_middleware
from .middleware.graph_integration import GraphIntegrationMiddleware
from .middleware.memory import CCEMemoryMiddleware
from .middleware.prompt_caching import PromptCachingMiddleware
from .middleware.summarization import create_cce_summarization_middleware
from .prompt_manager import enhance_instructions_with_system_prompt
from .state import CCEDeepAgentState

# Note: deepagents 0.3.x uses middleware instead of built-in tools
# write_todos is no longer a built-in, so we handle todos in our own tools
# from deepagents.tools import write_todos  # No longer available in 0.3.x
from .subagents import general_purpose_agent, planning_agent
from .tools.planning import PLANNING_TOOLS

# Note: Pre-model hooks not supported by deepagents library
# Context management handled by summarization middleware


def _build_message_updates(before_messages: list[Any], after_messages: list[Any]) -> list[Any]:
    """Build a message update list compatible with add_messages semantics."""
    if before_messages is None:
        before_messages = []
    if after_messages is None:
        after_messages = []

    before_ids = [getattr(message, "id", None) for message in before_messages]
    after_ids = [getattr(message, "id", None) for message in after_messages]
    before_ids_filtered = [message_id for message_id in before_ids if message_id is not None]
    after_ids_filtered = [message_id for message_id in after_ids if message_id is not None]

    removed_ids = any(message_id is not None and message_id not in after_ids for message_id in before_ids)
    reordered = before_ids_filtered and after_ids_filtered[: len(before_ids_filtered)] != before_ids_filtered
    if removed_ids or reordered or len(after_messages) < len(before_messages):
        if not after_messages:
            return [RemoveMessage(id=REMOVE_ALL_MESSAGES)]
        return [RemoveMessage(id=REMOVE_ALL_MESSAGES), *after_messages]

    before_by_id = {}
    for message in before_messages:
        message_id = getattr(message, "id", None)
        if message_id is not None:
            before_by_id[message_id] = message

    updates: list[Any] = []
    for message in after_messages:
        message_id = getattr(message, "id", None)
        if message_id is None:
            updates.append(message)
            continue
        previous = before_by_id.get(message_id)
        if previous is None or message != previous:
            updates.append(message)

    return updates


def _build_state_updates(before_state: dict[str, Any], after_state: dict[str, Any]) -> dict[str, Any] | None:
    """Build state updates by diffing before/after states."""
    updates: dict[str, Any] = {}
    before_messages = before_state.get("messages", [])
    after_messages = after_state.get("messages", [])
    message_updates = _build_message_updates(before_messages, after_messages)
    if message_updates:
        updates["messages"] = message_updates

    for key, value in after_state.items():
        if key == "messages":
            continue
        if key not in before_state or before_state[key] != value:
            updates[key] = value

    return updates or None


def _extract_cycle_complete_signal(messages: list[Any]) -> dict[str, str] | None:
    """Detect signal_cycle_complete tool calls in messages."""
    for message in messages:
        tool_calls = getattr(message, "tool_calls", None) or []
        for tool_call in tool_calls:
            if isinstance(tool_call, dict):
                name = tool_call.get("name")
                args = tool_call.get("args") or {}
            else:
                name = getattr(tool_call, "name", None) or getattr(tool_call, "tool_name", None)
                args = getattr(tool_call, "args", None) or getattr(tool_call, "arguments", None) or {}
            if name != "signal_cycle_complete":
                continue
            return {
                "summary": args.get("summary", ""),
                "work_remaining": args.get("work_remaining", ""),
                "next_focus_suggestion": args.get("next_focus_suggestion", ""),
                "method": "tool_call",
            }
    return None


def _resolve_subagent_tools(
    subagent: dict[str, Any],
    tool_by_name: dict[str, Any],
    logger,
) -> dict[str, Any]:
    """Resolve subagent tool names to tool objects for DeepAgents."""
    tools = subagent.get("tools")
    if not isinstance(tools, list):
        return subagent

    if all(hasattr(tool, "name") for tool in tools):
        return subagent

    resolved_tools: list[Any] = []
    missing: list[str] = []
    for tool in tools:
        if isinstance(tool, str):
            resolved = tool_by_name.get(tool)
            if resolved is None:
                missing.append(tool)
                continue
            resolved_tools.append(resolved)
            continue
        if hasattr(tool, "name"):
            resolved_tools.append(tool)
            continue
        missing.append(str(tool))

    if missing:
        logger.warning(f"⚠️ [DEEP AGENTS CREATION] Missing subagent tools: {missing}")

    updated = dict(subagent)
    if resolved_tools:
        updated["tools"] = resolved_tools
    else:
        updated.pop("tools", None)
    return updated


def get_cce_deep_agent_tools() -> list[Any]:
    """Build the tool list for the deep agent without instantiating the agent."""
    from .cycle_tools import CYCLE_TOOLS
    from .tools.adr import ADR_TOOLS
    from .tools.bash import BASH_TOOLS
    from .tools.filesystem import FILESYSTEM_COMPAT_TOOLS
    from .tools.langgraph_interrupt import LANGGRAPH_INTERRUPT_TOOLS
    from .tools.validation import VALIDATION_TOOLS

    return (
        PLANNING_TOOLS
        + ADR_TOOLS
        + LANGGRAPH_INTERRUPT_TOOLS
        + VALIDATION_TOOLS
        + CYCLE_TOOLS
        + BASH_TOOLS
        + FILESYSTEM_COMPAT_TOOLS
    )


def get_cce_instructions() -> str:
    """
    Get the main CCE agent instructions with enhanced system prompt.

    Returns:
        String containing the constitutional context engineering instructions
    """
    # Enhance with system prompt architecture
    return enhance_instructions_with_system_prompt("", "main")


def createCCEDeepAgent(
    llm=None,
    context_mode="trim",
    enable_memory_persistence=True,
    enable_context_auditing=True,
    enable_prompt_cache: bool = True,
    cache_config: dict[str, Any] | None = None,
    enable_post_model_hook_manager: bool = True,
    workspace_root: str | None = None,
):
    """
    Create the main CCE Deep Agent with all stakeholder sub-agents and enhanced capabilities.

    Args:
        llm: Optional LLM instance to use for the deep agent
        context_mode: Context management mode - "trim" for simple trimming, "summarize" for intelligent summarization
        enable_memory_persistence: Whether to enable persistent memory storage with checkpointing
        enable_context_auditing: Whether to enable comprehensive context auditing for debugging
        enable_prompt_cache: Whether to enable prompt caching for token reduction
        cache_config: Optional cache configuration dictionary
        workspace_root: Optional workspace root for filesystem tooling

    Returns:
        Configured deep agent instance with all stakeholder sub-agents and enhanced features
    """
    instructions = get_cce_instructions()
    resolved_root = os.path.abspath(workspace_root) if workspace_root else os.getcwd()
    from src.workspace_context import set_workspace_root

    set_workspace_root(resolved_root)

    # Load tool definitions for logging and subagent resolution
    from .cycle_tools import CYCLE_TOOLS
    from .tools.adr import ADR_TOOLS
    from .tools.bash import BASH_TOOLS
    from .tools.filesystem import FILESYSTEM_COMPAT_TOOLS
    from .tools.langgraph_interrupt import LANGGRAPH_INTERRUPT_TOOLS
    from .tools.validation import VALIDATION_TOOLS

    # Combine all tools (planning tools + ADR tools + interrupt tools + validation tools + bash tools)
    # Note: filesystem tools are provided by middleware
    all_tools = get_cce_deep_agent_tools()

    import logging

    logger = logging.getLogger(__name__)

    tool_by_name = {tool.name: tool for tool in all_tools if hasattr(tool, "name")}
    enhanced_subagents = [
        _resolve_subagent_tools(planning_agent, tool_by_name, logger),
        _resolve_subagent_tools(general_purpose_agent, tool_by_name, logger),
    ]

    # Log the configuration
    logger.info(f"🔧 [DEEP AGENTS CREATION] Tools configured: {len(all_tools)} total")
    logger.info("   📁 Filesystem tools: provided via middleware")
    logger.info(
        f"   📋 Planning tools: {len(PLANNING_TOOLS)} tools (create_plan, update_plan, get_plan_status, list_plans, set_active_plan, get_active_plan)"
    )
    logger.info(f"   📝 ADR tools: {len(ADR_TOOLS)} tools (create_adr, list_adrs, get_adr, adr_summary)")
    logger.info(
        f"   🛑 LangGraph interrupt tools: {len(LANGGRAPH_INTERRUPT_TOOLS)} tools (trigger_quality_interrupt, trigger_architectural_decision_interrupt)"
    )
    logger.info(
        f"   ✅ Validation tools: {len(VALIDATION_TOOLS)} tools (validate_code, run_linting, run_tests, check_syntax)"
    )
    logger.info(f"   🏁 Cycle tools: {len(CYCLE_TOOLS)} tools (signal_cycle_complete)")
    logger.info(
        f"   🖥️ Bash tools: {len(BASH_TOOLS)} tools (execute_bash_command, advanced_shell_command, check_system_status)"
    )
    logger.info(f"   📁 Filesystem compat tools: {len(FILESYSTEM_COMPAT_TOOLS)} tools (sync_to_disk)")
    logger.info(f"   📝 Built-in todos: write_todos (state management)")
    logger.info(f"🤖 [DEEP AGENTS CREATION] Sub-agents configured: {len(enhanced_subagents)} total")
    for i, agent in enumerate(enhanced_subagents):
        agent_name = agent.get("name", f"agent_{i}") if isinstance(agent, dict) else str(agent)
        logger.info(f"   🤖 Sub-agent {i + 1}: {agent_name}")

    # Create a properly authenticated LLM if none provided
    if llm is None:
        from langchain_anthropic import ChatAnthropic
        from langchain_openai import ChatOpenAI

        # Create LLM with proper authentication and increased token limit
        llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=0,
            max_tokens=64000,  # Increased from default to prevent tool call truncation
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
        # llm = ChatOpenAI(
        #     model="gpt-4o-mini",
        #     temperature=0,
        #     api_key=os.getenv("OPENAI_API_KEY")
        # )

    prompt_cache_middleware = None
    prompt_cache = None
    if enable_prompt_cache and os.getenv("FEATURE_PROMPT_CACHE", "0") == "1":
        from src.prompt_cache import PromptCache

        from .utils.constants import get_config

        if cache_config is None:
            cache_config = get_config("prompt_cache")

        prompt_cache = PromptCache(**cache_config) if cache_config else PromptCache()
        prompt_cache_middleware = PromptCachingMiddleware(cache=prompt_cache)

        logger.info("💾 [DEEP AGENTS CREATION] Prompt caching enabled")
        logger.info(f"   Cache configuration: {cache_config or 'default'}")
    else:
        logger.info("💾 [DEEP AGENTS CREATION] Prompt caching disabled")

    # Note: LLM auditing disabled due to deepagents library compatibility issues
    # Post-hook auditing will capture the main sources of context explosion
    if enable_context_auditing:
        logger.info(f"🔍 [DEEP AGENTS CREATION] LLM auditing disabled (post-hook auditing enabled)")

    # Note: Tool auditing disabled due to deepagents library compatibility issues
    # Tools can be audited manually if needed, but LLM and post-hook auditing
    # will capture the main sources of context explosion
    if enable_context_auditing:
        logger.info(f"🔍 [DEEP AGENTS CREATION] Tool auditing disabled (LLM and post-hook auditing enabled)")

    # Create the deep agent with all tools and sub-agents
    logger.info(
        f"🚀 [DEEP AGENTS CREATION] Creating deep agent with {len(all_tools)} tools and {len(enhanced_subagents)} sub-agents"
    )
    logger.info(f"📝 [DEEP AGENTS CREATION] Instructions length: {len(instructions)} characters")
    logger.info(f"🧠 [DEEP AGENTS CREATION] LLM model: {llm.model_name if hasattr(llm, 'model_name') else 'unknown'}")
    # Optional post-model approval hook (tool validation, approvals)
    from .middleware.post_model_approval import getCCEPostModelHook

    # Create PostModelHookManager hook if enabled
    post_model_hook_manager = None
    if enable_post_model_hook_manager:
        post_model_hook_manager = getCCEPostModelHook()

    # Wrap hooks with auditing if enabled
    if enable_context_auditing:
        from .audited_post_hook import create_audited_post_hook_manager

        hook_manager = create_audited_post_hook_manager(resolved_root)

        post_model_hook = None
        if post_model_hook_manager:
            audited_post_model_hook = hook_manager.create_audited_hook(
                "post_model_hook_manager", post_model_hook_manager
            )
            post_model_hook = hook_manager.create_combined_audited_hook(
                "combined_post_hook",
                audited_post_model_hook,
            )
            logger.info(
                "🔍 [DEEP AGENTS CREATION] Post-model hooks wrapped with context auditing (PostModelHookManager)"
            )
    else:
        post_model_hook = post_model_hook_manager

    logger.info("🔧 [DEEP AGENTS CREATION] Context management: Summarization middleware enabled")
    if enable_post_model_hook_manager:
        logger.info(f"   ✅ PostModelHookManager enabled (tool validation, failure tracking, approval system)")
    else:
        logger.info(f"   ⚠️ PostModelHookManager disabled")
    logger.info("   🧠 Summarization via middleware")
    logger.info("   🔄 Working memory synchronization enabled (middleware)")
    if enable_context_auditing:
        logger.info(f"   🔍 Context auditing enabled for all hooks")

    class PostModelHookMiddleware(AgentMiddleware):
        """Run CCE post-model hooks via langchain middleware."""

        state_schema = CCEDeepAgentState

        def __init__(self, hook: callable):
            super().__init__()
            self._hook = hook
            self.tools = []

        def after_model(self, state: dict[str, Any], runtime) -> dict[str, Any] | None:
            if self._hook is None:
                return None
            try:
                state_snapshot = copy.deepcopy(state)
                updated_state = self._hook(state_snapshot)
                if not isinstance(updated_state, dict):
                    return None
                return _build_state_updates(state, updated_state)
            except Exception as exc:
                logger.error(f"❌ [DEEP AGENTS CREATION] Post-model middleware failed: {exc}")
                return None

    # ADD: Initialize 3-layer memory system
    from .memory_system_init import initialize_memory_system

    # Create a temporary state to initialize memory system
    temp_state = {}
    temp_state = initialize_memory_system(temp_state)

    # Note: Virtual filesystem will be initialized by middleware on first invocation
    logger.info("🔍 [DEEP AGENTS CREATION] Virtual filesystem initialized via middleware")

    # Log memory system initialization results
    if temp_state.get("memory_stats"):
        logger.info(f"🧠 [MEMORY SYSTEM] Initializing 3-layer memory system")
        logger.info(f"   📝 Working Memory: Intelligent message management")
        logger.info(f"   📚 Episodic Memory: {temp_state['memory_stats'].get('episodic_records', 0)} records")
        logger.info(f"   🔧 Procedural Memory: {temp_state['memory_stats'].get('procedural_patterns', 0)} patterns")
        logger.info(f"   🔍 Semantic Retrieval: {temp_state['memory_stats'].get('semantic_enabled', False)}")
        logger.info(
            f"   🧠 Context Memory Manager: {'Available' if temp_state.get('context_memory_manager') else 'Not Available'}"
        )
    else:
        logger.warning(f"⚠️ [MEMORY SYSTEM] Memory system initialization failed")

    # ADD: Memory persistence with checkpointing
    checkpointer = None
    if enable_memory_persistence:
        try:
            from langgraph.checkpoint.memory import MemorySaver

            checkpointer = MemorySaver()
            logger.info(f"🗄️ [MEMORY PERSISTENCE] Enabled with memory checkpointing")
            logger.info(f"   💾 Memory-based checkpointing (session-only)")
            logger.info(f"   🔄 Cross-session memory continuity enabled")
        except ImportError as e:
            logger.warning(f"⚠️ [MEMORY PERSISTENCE] Failed to import MemorySaver: {e}")
            logger.warning(f"   💾 Memory persistence disabled")
        except Exception as e:
            logger.warning(f"⚠️ [MEMORY PERSISTENCE] Failed to initialize checkpointing: {e}")
            logger.warning(f"   💾 Memory persistence disabled")
    else:
        logger.info(f"🗄️ [MEMORY PERSISTENCE] Disabled by configuration")

    post_model_middleware = PostModelHookMiddleware(post_model_hook) if post_model_hook else None
    memory_middleware = CCEMemoryMiddleware()
    filesystem_middleware = create_filesystem_middleware(
        workspace_root=resolved_root,
        enable_virtual_fs=False,
    )
    summarization_middleware = create_cce_summarization_middleware(llm)
    subagent_filesystem_middleware = create_filesystem_middleware(
        workspace_root=resolved_root,
        enable_virtual_fs=False,
    )
    subagent_middleware = [
        TodoListMiddleware(),
        subagent_filesystem_middleware,
        create_cce_summarization_middleware(llm),
    ]
    if prompt_cache is not None:
        subagent_middleware.append(PromptCachingMiddleware(cache=prompt_cache))
    subagent_middleware.append(PatchToolCallsMiddleware())

    middleware: list[AgentMiddleware] = [
        TodoListMiddleware(),
        filesystem_middleware,
        SubAgentMiddleware(
            default_model=llm,
            default_tools=all_tools,
            default_middleware=subagent_middleware,
            default_interrupt_on=None,
            subagents=enhanced_subagents,
            general_purpose_agent=True,
        ),
        summarization_middleware,
    ]
    if prompt_cache_middleware is not None:
        middleware.append(prompt_cache_middleware)
    middleware.append(PatchToolCallsMiddleware())
    if memory_middleware is not None:
        middleware.append(memory_middleware)
    if post_model_middleware is not None:
        middleware.append(post_model_middleware)
    middleware.append(GraphIntegrationMiddleware())

    system_prompt = f"{instructions}\n\n{BASE_AGENT_PROMPT}" if instructions else BASE_AGENT_PROMPT
    cce_deep_agent = create_agent(
        llm,
        tools=all_tools,
        system_prompt=system_prompt,
        middleware=middleware,
        state_schema=CCEDeepAgentState,
        checkpointer=checkpointer,
    ).with_config({"recursion_limit": 1000})

    logger.info(f"✅ [DEEP AGENTS CREATION] Deep agent created successfully")

    # Generate audit summary if auditing is enabled
    if enable_context_auditing:
        try:
            from .context_auditor import get_global_auditor

            auditor = get_global_auditor(resolved_root)
            summary_path = auditor.generate_summary_report()
            logger.info(f"📊 [DEEP AGENTS CREATION] Context audit summary generated: {summary_path}")
        except Exception as e:
            logger.warning(f"⚠️ [DEEP AGENTS CREATION] Failed to generate audit summary: {e}")

    # Wrap the agent for compatibility with existing call sites
    def create_initialized_agent():
        """Create a deep agent instance."""
        return cce_deep_agent

    # Add a convenience method to invoke with filesystem middleware support
    async def invoke_with_filesystem(state_or_messages, config=None, **kwargs):
        """Invoke the agent while ensuring filesystem middleware can initialize state."""
        try:
            # Handle both state dict and messages list inputs
            if isinstance(state_or_messages, dict):
                # If it's a state dict, extract messages and merge with existing state
                messages = state_or_messages.get("messages", [])
                existing_state = state_or_messages
            else:
                # If it's a messages list, use it directly
                messages = state_or_messages
                existing_state = {}

            cleaned_state = dict(existing_state)
            if "files" in cleaned_state and not isinstance(cleaned_state.get("files"), dict):
                logger.warning(
                    "⚠️ [DEEP AGENTS INVOKE] existing_state['files'] is invalid (type: %s), ignoring",
                    type(cleaned_state.get("files")),
                )
                cleaned_state.pop("files", None)
            if "changed_files" in cleaned_state and not isinstance(cleaned_state.get("changed_files"), list):
                logger.warning(
                    "⚠️ [DEEP AGENTS INVOKE] existing_state['changed_files'] is invalid (type: %s), ignoring",
                    type(cleaned_state.get("changed_files")),
                )
                cleaned_state.pop("changed_files", None)

            initial_state = {
                "messages": messages,
                "remaining_steps": kwargs.get("remaining_steps", 1000),
                "context_memory": kwargs.get("context_memory", {}),
                "execution_phases": kwargs.get("execution_phases", [{"cycle_count": 0}]),
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in ["remaining_steps", "context_memory", "execution_phases"]
                },
                **{k: v for k, v in cleaned_state.items() if k != "messages"},
            }

            # Pass config to ainvoke for checkpointer support
            return await cce_deep_agent.ainvoke(initial_state, config=config)

        except Exception as e:
            logger.error(f"❌ [DEEP AGENTS INVOKE] Failed to invoke deep agent: {e}")
            # Fall back to normal invocation with proper state structure
            if isinstance(state_or_messages, dict):
                messages = state_or_messages.get("messages", [])
                existing_state = state_or_messages
            else:
                messages = state_or_messages
                existing_state = {}

            fallback_state = {
                "messages": messages,
                "remaining_steps": kwargs.get("remaining_steps", 1000),
                "context_memory": kwargs.get("context_memory", {}),
                "execution_phases": kwargs.get("execution_phases", [{"cycle_count": 0}]),
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k not in ["remaining_steps", "context_memory", "execution_phases"]
                },
                **{k: v for k, v in existing_state.items() if k not in ["files", "messages"]},
            }
            # Fallback to normal invocation with proper state structure
            return await cce_deep_agent.ainvoke(fallback_state, config=config)

    async def run_with_cycles(state_or_messages, config=None, max_cycles: int | None = None, **kwargs):
        """Invoke the deep agent repeatedly until signal_cycle_complete or max cycles."""
        cycle_limit = max_cycles
        if cycle_limit is None:
            try:
                from src.config import get_max_execution_cycles

                cycle_limit = get_max_execution_cycles()
            except Exception:
                cycle_limit = 3

        if cycle_limit <= 0:
            return await invoke_with_filesystem(state_or_messages, config=config, **kwargs)

        logger = logging.getLogger(__name__)
        current_state = state_or_messages
        last_result = None
        cycle_index = 0

        while cycle_index < cycle_limit:
            logger.info("🔁 [DEEP AGENTS] Starting cycle %s/%s", cycle_index + 1, cycle_limit)
            last_result = await invoke_with_filesystem(current_state, config=config, **kwargs)

            if not isinstance(last_result, dict):
                return last_result

            messages = last_result.get("messages") or []
            signal = _extract_cycle_complete_signal(messages)
            if signal:
                last_result["cycle_complete_signal"] = signal
                last_result["ready_to_end"] = True
                return last_result

            cycle_index += 1
            phases = list(last_result.get("execution_phases") or [])
            next_phase = {"cycle_count": cycle_index, "phase": "ticket_processing"}
            if not phases or phases[-1].get("cycle_count") != next_phase["cycle_count"]:
                phases.append(next_phase)
            last_result["execution_phases"] = phases
            last_result["cycle_count"] = cycle_index
            current_state = last_result

        if isinstance(last_result, dict):
            last_result["ready_to_end"] = False
        return last_result

    # Add the convenience method to the agent
    cce_deep_agent.invoke_with_filesystem = invoke_with_filesystem
    cce_deep_agent.run_with_cycles = run_with_cycles

    return cce_deep_agent
