"""Execution phase helpers."""

from __future__ import annotations

import asyncio
import concurrent.futures
import time
from datetime import datetime
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import create_react_agent as _default_create_react_agent

from src.agent.state import ExecutionState
from src.models import CycleResult


def _resolve_timeout(value: Any, default: int) -> int:
    if value is None:
        return default
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return default


def _invoke_llm_with_timeout(agent, messages: list[Any], timeout_s: int, label: str) -> Any:
    start = time.monotonic()
    last_message = messages[-1] if messages else None
    last_message_type = type(last_message).__name__ if last_message else "none"
    last_message_len = len(getattr(last_message, "content", "") or "") if last_message else 0
    agent.logger.info(
        "LLM invoke start (%s): messages=%s last_message_type=%s last_message_len=%s timeout=%ss",
        label,
        len(messages),
        last_message_type,
        last_message_len,
        timeout_s,
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(agent.llm.invoke, messages)
        try:
            response = future.result(timeout=timeout_s)
        except concurrent.futures.TimeoutError as exc:
            agent.logger.error("LLM invoke timeout (%s) after %ss", label, timeout_s)
            future.cancel()
            raise TimeoutError(f"LLM invoke timed out after {timeout_s}s ({label})") from exc
        except Exception:
            agent.logger.exception("LLM invoke failed (%s) after %.2fs", label, time.monotonic() - start)
            raise

    duration = time.monotonic() - start
    response_len = len(getattr(response, "content", "") or "")
    agent.logger.info("LLM invoke finished (%s): duration=%.2fs response_len=%s", label, duration, response_len)
    return response


def orient_for_next_cycle(agent, state: ExecutionState) -> dict[str, Any]:
    """Simple prompt-based orientation for the next execution cycle."""
    agent.logger.info("\N{DIRECT HIT} Orienting for cycle %s", state["cycle_count"] + 1)

    soft_limit = state.get("soft_limit") or getattr(agent, "soft_limit", None) or 20
    timeout_s = _resolve_timeout(getattr(agent, "llm_invoke_timeout", None), 300)
    plan_text = state.get("plan") or ""
    agent.logger.info(
        "\N{DIRECT HIT} Orientation context: plan_len=%s messages=%s cycle_results=%s",
        len(plan_text),
        len(state.get("messages", [])),
        len(state.get("cycle_results", [])),
    )

    # Create orientation prompt
    orientation_prompt = f"""You are about to begin execution cycle {state["cycle_count"] + 1} of {state["max_cycles"]}.

    Your overall plan is:
    {state["plan"]}

    Soft limit for this cycle: {soft_limit} tool calls. After reaching it, shift into wrap-up and summarize progress.

    Based on your conversation history and the plan above, what specific aspect should you focus on for this execution cycle? 
    Provide a clear, focused orientation that will guide your actions in this cycle.

    Previous cycle results: {len(state["cycle_results"])} cycles completed
    """

    # Create orientation messages with conversation context
    orientation_messages = state["messages"] + [HumanMessage(content=orientation_prompt)]
    agent.logger.info(
        "\N{DIRECT HIT} Orientation prompt size: %s chars (pre-trim messages=%s)",
        len(orientation_prompt),
        len(orientation_messages),
    )

    # Apply context management to prevent token limit exceeded errors
    trimmed_messages = agent._trim_messages_for_context(orientation_messages, max_tokens=900000)
    agent.logger.info(
        "\N{DIRECT HIT} Orientation messages trimmed: %s -> %s",
        len(orientation_messages),
        len(trimmed_messages),
    )

    # LLM call for orientation with context
    response = _invoke_llm_with_timeout(agent, trimmed_messages, timeout_s, label="orientation")
    orientation = response.content

    agent.logger.info("\N{DIRECT HIT} Cycle orientation: %s...", orientation[:100])

    return {
        "orientation": orientation,
        "cycle_count": state["cycle_count"] + 1,
    }


def _count_tool_calls(messages: list[Any]) -> int:
    tool_message_count = sum(1 for msg in messages if isinstance(msg, ToolMessage))
    if tool_message_count:
        return tool_message_count
    return sum(
        len(msg.tool_calls)
        for msg in messages
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None)
    )


def _derive_soft_limit_metrics(step_count: int, soft_limit: int, wrap_up_started_at: int | None) -> dict[str, Any]:
    if soft_limit <= 0:
        return {
            "soft_limit": soft_limit,
            "soft_limit_reached": False,
            "wrap_up_started_at_step": None,
            "steps_in_main_phase": max(step_count, 0),
            "steps_in_wrap_up_phase": 0,
        }

    soft_limit_reached = step_count >= soft_limit
    steps_in_main_phase = step_count if not soft_limit_reached else soft_limit
    steps_in_wrap_up_phase = 0 if not soft_limit_reached else max(step_count - steps_in_main_phase, 0)
    if soft_limit_reached and wrap_up_started_at is None:
        wrap_up_started_at = soft_limit
    if not soft_limit_reached:
        wrap_up_started_at = None
    return {
        "soft_limit": soft_limit,
        "soft_limit_reached": soft_limit_reached,
        "wrap_up_started_at_step": wrap_up_started_at,
        "steps_in_main_phase": steps_in_main_phase,
        "steps_in_wrap_up_phase": steps_in_wrap_up_phase,
    }


async def execute_react_cycle(agent, state: ExecutionState) -> dict[str, Any]:
    """Execute a ReAct cycle with tool access and conversation persistence."""
    soft_limit = state.get("soft_limit") or getattr(agent, "soft_limit", None) or 20
    recursion_limit = getattr(agent, "recursion_limit", None) or 25
    react_timeout = _resolve_timeout(getattr(agent, "react_timeout", None), 600)
    cycle_start_time = datetime.now()
    if hasattr(agent, "cycle_metrics"):
        try:
            agent.cycle_metrics.start_cycle(
                cycle_number=state["cycle_count"],
                orientation=state.get("orientation", ""),
                start_time=cycle_start_time,
            )
        except Exception:
            agent.logger.debug("Failed to start cycle metrics tracking", exc_info=True)
    agent.logger.info(
        "\N{HIGH VOLTAGE SIGN} Executing ReAct cycle %s (max %s iterations)",
        state["cycle_count"],
        recursion_limit,
    )
    agent.logger.info("\N{HIGH VOLTAGE SIGN} Soft limit: %s tool calls", soft_limit)
    agent.logger.info("\N{HIGH VOLTAGE SIGN} ReAct timeout: %s seconds", react_timeout)
    agent.logger.info(
        "\N{HIGH VOLTAGE SIGN} Current focus: %s...",
        state["orientation"][:100],
    )

    # Create execution prompt combining orientation with agent identity
    execution_prompt = f"""You are a sophisticated software engineering agent working on a ticket.

    Current Focus: {state["orientation"]}

    Overall Plan: {state["plan"]}

    You have access to all tools for file operations, shell commands, git operations, and code analysis.
    Work systematically toward completing the current focus area. You have up to {recursion_limit} iterations for this cycle.
    Soft limit: {soft_limit} tool calls. After reaching it, shift into wrap-up and summarize progress.

    When you've made meaningful progress on the current focus, provide a summary of what you accomplished.
    """

    # Add execution prompt to conversation
    cycle_messages = state["messages"] + [HumanMessage(content=execution_prompt)]
    agent.logger.info(
        "\N{HIGH VOLTAGE SIGN} ReAct prompt size: %s chars (messages=%s)",
        len(execution_prompt),
        len(cycle_messages),
    )

    reminder_message = None
    wrap_up_message = None
    if state.get("soft_limit_reached"):
        agent.logger.info("\N{WARNING SIGN} Soft limit already reached before cycle start")
        from src.prompts.wrap_up_prompt import build_wrap_up_message
        from src.wrap_up_protocol import WrapUpPhaseState, check_wrap_up_progress, track_wrap_up_activity

        step_count = state.get("step_count", 0)
        wrap_up_started_at = state.get("wrap_up_started_at_step", step_count)
        wrap_up_steps = max(0, step_count - wrap_up_started_at)
        wrap_up_state = WrapUpPhaseState(started_at_step=wrap_up_started_at)
        previous_cycle = state.get("cycle_results", [])[-1] if state.get("cycle_results") else None
        tool_calls = getattr(previous_cycle, "tool_calls", None) if previous_cycle else None
        if not tool_calls and previous_cycle is not None and hasattr(agent, "_extract_tool_calls_from_messages"):
            tool_calls = agent._extract_tool_calls_from_messages(getattr(previous_cycle, "history", []))
        if tool_calls:
            wrap_up_state = track_wrap_up_activity(tool_calls, wrap_up_state)
        wrap_up_message = build_wrap_up_message(
            step_count=step_count,
            soft_limit=soft_limit,
            previous_cycles=state.get("cycle_results"),
        )
        cycle_messages.append(wrap_up_message)
        reminder = check_wrap_up_progress(wrap_up_state, wrap_up_steps)
        if reminder:
            reminder_message = SystemMessage(content=reminder)
            cycle_messages.append(reminder_message)

    # Create ReAct agent with all tools (no restrictions like planning had)
    try:
        from src import agent as agent_module

        react_agent_factory = getattr(agent_module, "create_react_agent", _default_create_react_agent)
    except Exception:
        react_agent_factory = _default_create_react_agent

    react_agent = react_agent_factory(agent.llm, agent.tools)

    async def _invoke_react(messages: list[Any], recursion_limit: int) -> dict[str, Any]:
        if hasattr(agent, "_get_contextual_messages"):
            trimmed = agent._get_contextual_messages(messages, max_tokens=800000)
        else:
            trimmed = agent._trim_messages_for_context(messages, max_tokens=800000)

        agent.logger.info(
            "\N{HIGH VOLTAGE SIGN} Starting ReAct execution with %s conversation messages (trimmed from %s)",
            len(trimmed),
            len(messages),
        )
        agent.logger.info(
            "\N{HIGH VOLTAGE SIGN} ReAct invoke start: recursion_limit=%s timeout=%ss",
            recursion_limit,
            react_timeout,
        )
        invoke_start = time.monotonic()

        try:
            result = await asyncio.wait_for(
                react_agent.ainvoke(
                    {"messages": trimmed},
                    config={
                        "recursion_limit": recursion_limit,
                        "timeout": react_timeout,
                    },
                ),
                timeout=react_timeout,
            )
        except asyncio.TimeoutError as exc:
            agent.logger.error(
                "\N{HIGH VOLTAGE SIGN} ReAct invoke timeout after %ss (recursion_limit=%s)",
                react_timeout,
                recursion_limit,
            )
            raise TimeoutError(f"ReAct invoke timed out after {react_timeout}s") from exc
        except Exception:
            agent.logger.exception("\N{HIGH VOLTAGE SIGN} ReAct invoke failed after %.2fs", time.monotonic() - invoke_start)
            raise
        else:
            agent.logger.info(
                "\N{HIGH VOLTAGE SIGN} ReAct invoke finished in %.2fs (messages=%s)",
                time.monotonic() - invoke_start,
                len(result.get("messages", [])),
            )
            return result

    try:
        # Execute ReAct cycle with trimmed conversation history
        result = await _invoke_react(cycle_messages, recursion_limit=recursion_limit)

        # Count tool calls and actions taken
        new_messages = result.get("messages", [])
        if wrap_up_message and wrap_up_message not in new_messages:
            new_messages = [wrap_up_message] + new_messages
            result["messages"] = new_messages
        if reminder_message and reminder_message not in new_messages:
            new_messages = [reminder_message] + new_messages
            result["messages"] = new_messages
        step_count = _count_tool_calls(new_messages)
        soft_limit_metrics = _derive_soft_limit_metrics(
            step_count=step_count,
            soft_limit=soft_limit,
            wrap_up_started_at=state.get("wrap_up_started_at_step"),
        )
        wrap_up_started_at = soft_limit_metrics["wrap_up_started_at_step"]
        if soft_limit_metrics["soft_limit_reached"] and not state.get("soft_limit_reached"):
            from src.prompts.wrap_up_prompt import build_wrap_up_message
            from src.wrap_up_protocol import WrapUpPhaseState, check_wrap_up_progress, track_wrap_up_activity

            wrap_up_started_at = wrap_up_started_at or soft_limit
            wrap_up_steps = max(0, step_count - wrap_up_started_at)
            wrap_up_state = WrapUpPhaseState(started_at_step=wrap_up_started_at)
            if hasattr(agent, "_extract_tool_calls_from_messages"):
                tool_calls = agent._extract_tool_calls_from_messages(new_messages)
                if tool_calls:
                    wrap_up_state = track_wrap_up_activity(tool_calls, wrap_up_state)
            mid_cycle_wrap_up = build_wrap_up_message(
                step_count=step_count,
                soft_limit=soft_limit,
                previous_cycles=state.get("cycle_results"),
            )
            wrap_up_messages = new_messages + [mid_cycle_wrap_up]
            reminder = check_wrap_up_progress(wrap_up_state, wrap_up_steps)
            mid_cycle_reminder = SystemMessage(content=reminder) if reminder else None
            if mid_cycle_reminder:
                wrap_up_messages.append(mid_cycle_reminder)

            agent.logger.info(
                "\N{WARNING SIGN} Soft limit reached mid-cycle; invoking wrap-up phase now."
            )
            wrap_up_result = await _invoke_react(wrap_up_messages, recursion_limit=recursion_limit)
            wrap_up_messages = wrap_up_result.get("messages", [])
            if mid_cycle_wrap_up not in wrap_up_messages:
                wrap_up_messages = [mid_cycle_wrap_up] + wrap_up_messages
            if mid_cycle_reminder and mid_cycle_reminder not in wrap_up_messages:
                wrap_up_messages = [mid_cycle_reminder] + wrap_up_messages
            new_messages = wrap_up_messages
            step_count = _count_tool_calls(new_messages)
            soft_limit_metrics = _derive_soft_limit_metrics(
                step_count=step_count,
                soft_limit=soft_limit,
                wrap_up_started_at=wrap_up_started_at,
            )
        tool_calls = step_count
        agent.logger.info(
            "\N{HIGH VOLTAGE SIGN} Cycle %s made %s tool calls across %s messages",
            state["cycle_count"],
            tool_calls,
            len(new_messages),
        )
        if soft_limit_metrics["soft_limit_reached"]:
            agent.logger.info(
                "\N{WARNING SIGN} Soft limit reached at step %s; wrap-up phase started.",
                soft_limit_metrics["wrap_up_started_at_step"],
            )

        # Extract final response
        if new_messages:
            final_message = new_messages[-1]
            cycle_summary = final_message.content if hasattr(final_message, "content") else "Cycle completed"
            agent.logger.info(
                "\N{HIGH VOLTAGE SIGN} Cycle %s final summary: %s...",
                state["cycle_count"],
                cycle_summary[:150],
            )
        else:
            cycle_summary = "No response from ReAct cycle"
            agent.logger.warning(
                "\N{HIGH VOLTAGE SIGN} Cycle %s produced no messages",
                state["cycle_count"],
            )

        # Create cycle result
        cycle_result = CycleResult(
            cycle_number=state["cycle_count"],
            status="success",
            orientation=state.get("orientation", ""),
            start_time=cycle_start_time,
            end_time=datetime.now(),
            final_summary=cycle_summary,
            messages_count=len(new_messages),
            # Legacy fields for backward compatibility
            history=new_messages,
            final_thought=cycle_summary,
            soft_limit=soft_limit_metrics["soft_limit"],
            soft_limit_reached=soft_limit_metrics["soft_limit_reached"],
            step_count=step_count,
            steps_in_main_phase=soft_limit_metrics["steps_in_main_phase"],
            steps_in_wrap_up_phase=soft_limit_metrics["steps_in_wrap_up_phase"],
        )
        if cycle_result.end_time:
            cycle_result.duration_seconds = (cycle_result.end_time - cycle_result.start_time).total_seconds()

        detected_tool_calls = None
        if hasattr(agent, "_extract_tool_calls_from_messages"):
            detected_tool_calls = agent._extract_tool_calls_from_messages(new_messages)
            cycle_result.tool_calls = detected_tool_calls

        from src.wrap_up_protocol import WrapUpPhaseState, can_end_cycle, track_wrap_up_activity

        wrap_up_state = WrapUpPhaseState(started_at_step=wrap_up_started_at or step_count)
        if detected_tool_calls:
            wrap_up_state = track_wrap_up_activity(detected_tool_calls, wrap_up_state)
        can_end, issues = can_end_cycle(wrap_up_state)
        if issues:
            cycle_result.wrap_up_issues = issues
        cycle_result.wrap_up_tests_run = wrap_up_state.tests_run
        cycle_result.wrap_up_tests_passed = wrap_up_state.tests_passed
        cycle_result.wrap_up_linting_run = wrap_up_state.linting_run
        cycle_result.wrap_up_linting_passed = wrap_up_state.linting_passed
        cycle_result.wrap_up_cycle_report_prepared = wrap_up_state.cycle_report_prepared

        if hasattr(agent, "_detect_cycle_complete_signal"):
            signal = agent._detect_cycle_complete_signal(new_messages)
            if signal:
                cycle_result.cycle_summary = signal.summary
                cycle_result.work_remaining = signal.work_remaining
                cycle_result.next_focus_suggestion = signal.next_focus_suggestion
                cycle_result.cycle_complete_signal_method = signal.method
                cycle_result.ready_to_end = can_end
                if not can_end and issues:
                    agent.logger.info(
                        "\N{WARNING SIGN} Cycle completion signal received but wrap-up is incomplete: %s",
                        ", ".join(issues),
                    )

        agent.logger.info("\N{HIGH VOLTAGE SIGN} Cycle %s completed successfully", state["cycle_count"])

        # Update conversation with new messages
        return {
            "messages": new_messages,
            "cycle_results": state["cycle_results"] + [cycle_result],
            "step_count": step_count,
            "soft_limit": soft_limit_metrics["soft_limit"],
            "soft_limit_reached": soft_limit_metrics["soft_limit_reached"],
            "wrap_up_started_at_step": soft_limit_metrics["wrap_up_started_at_step"],
        }

    except Exception as exc:
        agent.logger.error(
            "\N{HIGH VOLTAGE SIGN} Cycle %s failed with error: %s",
            state["cycle_count"],
            exc,
        )

        # Create failure result - make error available to LLM
        error_message = AIMessage(
            content=(f"Cycle failed with error: {str(exc)}. I should analyze this error and decide how to proceed.")
        )
        soft_limit_metrics = _derive_soft_limit_metrics(
            step_count=state.get("step_count", 0),
            soft_limit=soft_limit,
            wrap_up_started_at=state.get("wrap_up_started_at_step"),
        )
        cycle_result = CycleResult(
            cycle_number=state["cycle_count"],
            status="failure",
            orientation=state.get("orientation", ""),
            start_time=cycle_start_time,
            end_time=datetime.now(),
            final_summary=f"Cycle failed due to error: {str(exc)}",
            messages_count=1,
            # Legacy fields for backward compatibility
            history=[error_message],
            final_thought=f"Cycle failed due to error: {str(exc)}",
            soft_limit=soft_limit_metrics["soft_limit"],
            soft_limit_reached=soft_limit_metrics["soft_limit_reached"],
            step_count=state.get("step_count", 0),
            steps_in_main_phase=soft_limit_metrics["steps_in_main_phase"],
            steps_in_wrap_up_phase=soft_limit_metrics["steps_in_wrap_up_phase"],
        )
        if cycle_result.end_time:
            cycle_result.duration_seconds = (cycle_result.end_time - cycle_result.start_time).total_seconds()

        return {
            "messages": [error_message],
            "cycle_results": state["cycle_results"] + [cycle_result],
            "soft_limit": soft_limit_metrics["soft_limit"],
            "soft_limit_reached": soft_limit_metrics["soft_limit_reached"],
            "wrap_up_started_at_step": soft_limit_metrics["wrap_up_started_at_step"],
            "step_count": state.get("step_count", 0),
        }


async def reconcile_cycle_results(agent, state: ExecutionState) -> dict[str, Any]:
    """Process and log the results of the completed cycle."""
    agent.logger.info(
        "\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS} Reconciling results from cycle %s",
        state["cycle_count"],
    )

    latest_result = state["cycle_results"][-1] if state["cycle_results"] else None

    if latest_result:
        agent.logger.info(
            "\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS} Cycle %s status: %s",
            state["cycle_count"],
            latest_result.status,
        )
        agent.logger.info(
            "\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS} Cycle summary: %s...",
            latest_result.final_thought[:200],
        )

    if hasattr(agent, "_simple_reconcile_cycle_results"):
        try:
            return await agent._simple_reconcile_cycle_results(state)
        except Exception as exc:
            agent.logger.warning("Reconciliation sequence failed: %s", exc)
            return {}

    return {}


def determine_next_action(agent, state: ExecutionState) -> dict[str, Any]:
    """Determine whether to continue, complete, or fail based on current state."""
    agent.logger.info(
        "\N{THINKING FACE} Determining next action after %s cycles",
        state["cycle_count"],
    )
    timeout_s = _resolve_timeout(getattr(agent, "llm_invoke_timeout", None), 300)

    latest_result = state["cycle_results"][-1] if state["cycle_results"] else None

    # Check for explicit cycle completion signal
    if latest_result and getattr(latest_result, "ready_to_end", False):
        agent.logger.info("\N{CHEQUERED FLAG} Cycle marked ready to end")
        return {"agent_status": "completed"}

    max_cycles = state.get("max_cycles") or getattr(agent, "max_execution_cycles", None) or 50

    # Check cycle limits first
    if state["cycle_count"] >= max_cycles:
        agent.logger.info(
            "\N{CHEQUERED FLAG} Reached max cycles (%s), completing",
            max_cycles,
        )
        return {"agent_status": "completed"}

    # Count consecutive failures to detect systemic issues
    consecutive_failures = 0
    for result in reversed(state["cycle_results"]):
        if result.status == "failure":
            consecutive_failures += 1
        else:
            break

    # Fail fast after multiple consecutive failures (likely systemic issue)
    MAX_CONSECUTIVE_FAILURES = 3
    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
        agent.logger.error(
            "\N{CROSS MARK} Stopping after %s consecutive cycle failures - likely systemic issue",
            consecutive_failures,
        )
        return {"agent_status": "failed"}

    # Single failure: log and allow retry (transient errors are recoverable)
    if latest_result and latest_result.status == "failure":
        agent.logger.info(
            "\N{WARNING SIGN} Cycle %s failed, will retry (consecutive failures: %s/%s)",
            state["cycle_count"],
            consecutive_failures,
            MAX_CONSECUTIVE_FAILURES,
        )

    # Simple completion check - ask LLM if the work is done
    completion_prompt = f"""Based on the work completed so far, should we:
    1. Continue with another execution cycle
    2. Mark the ticket as completed
    3. Mark the ticket as failed

    Plan: {state["plan"]}
    Cycles completed: {state["cycle_count"]}
    Latest cycle status: {latest_result.status if latest_result else "none"}

    Respond with just: CONTINUE, COMPLETED, or FAILED"""

    messages = state["messages"] + [HumanMessage(content=completion_prompt)]
    response = _invoke_llm_with_timeout(agent, messages, timeout_s, label="completion-check")
    decision = response.content.strip().upper()

    if "COMPLETED" in decision:
        agent.logger.info("\N{PARTY POPPER} Agent determined work is completed")
        return {"agent_status": "completed"}
    if "FAILED" in decision:
        agent.logger.info("\N{CROSS MARK} Agent determined work has failed")
        return {"agent_status": "failed"}

    agent.logger.info(
        "\N{ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS} Agent determined to continue with next cycle"
    )
    return {"agent_status": "running"}
