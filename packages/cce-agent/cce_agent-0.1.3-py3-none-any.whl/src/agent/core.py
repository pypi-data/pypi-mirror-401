"""
CCE Agent Core helpers.

This module hosts shared orchestration logic extracted from the legacy agent.
It provides a stable interface for modular imports while retaining backwards
compatibility with the existing CCEAgent implementation.
"""

import logging
from contextlib import asynccontextmanager

from langchain_core.messages import HumanMessage

from src.agent.state import ExecutionState, PlanningState
from src.environments.base import BaseEnvironment
from src.environments.local import LocalEnvironment
from src.models import RunResult, Ticket

logger = logging.getLogger(__name__)


class CCEAgentCore:
    """Core agent entrypoint for modularized imports."""

    def __init__(
        self,
        primary_environment: BaseEnvironment | None = None,
        workspace_environment: BaseEnvironment | None = None,
    ) -> None:
        self.primary_env = primary_environment or LocalEnvironment()
        self.workspace_env = workspace_environment or self.primary_env
        logger.info(
            "CCEAgentCore initialized - Primary: %s, Workspace: %s",
            self.primary_env.__class__.__name__,
            self.workspace_env.__class__.__name__,
        )

    async def process_ticket(self, ticket: Ticket) -> RunResult:
        """Process a ticket end-to-end using the current CCEAgent implementation."""
        from src.agent import CCEAgent

        agent = CCEAgent(
            primary_environment=self.primary_env,
            workspace_environment=self.workspace_env,
        )
        return await agent.process_ticket(ticket)


async def process_ticket(agent, ticket: Ticket) -> RunResult:
    """
    Orchestrate a single ticket run using the legacy agent instance.
    """
    agent.logger.info("Processing ticket #%s: %s", ticket.number, ticket.title)

    run_log = None

    from src.observability.dual_write import dual_write_trace_context, is_dual_write_enabled

    @asynccontextmanager
    async def _maybe_trace_context():
        if not is_dual_write_enabled():
            yield None
            return
        async with dual_write_trace_context(ticket.number, ticket.url) as ctx:
            yield ctx

    async with _maybe_trace_context() as trace_ctx:
        agent.trace_ctx = trace_ctx
        if hasattr(agent, "cycle_metrics"):
            agent.cycle_metrics.reset()
        # Start run tracking
        run_log = agent.run_tracker.start_run(ticket)
        if trace_ctx:
            trace_ctx.add_metadata("run_id", run_log.run_id)
            trace_ctx.add_metadata("thread_id", run_log.thread_id)

        planning_phase_started = False
        execution_phase_started = False

        try:
            # Clear token tracking for this run
            agent.llm.clear_usage_records()

            if trace_ctx:
                trace_ctx.start_phase("planning")
                planning_phase_started = True

            initial_message = HumanMessage(content=f"Ticket Title: {ticket.title}\n\nTicket Body: {ticket.body}")

            # Initialize state for multi-agent planning
            initial_state: PlanningState = {
                "messages": [initial_message],
                "shared_plan": "",
                "technical_analysis": "",
                "architectural_analysis": "",
                "consensus_reached": False,
                "iteration_count": 0,
                "max_iterations": 12,
            }

            # Use run thread_id for planning
            config = {
                "configurable": {"thread_id": run_log.thread_id + "-planning"},
                "recursion_limit": 50,
            }

            agent.logger.info("\N{HANDSHAKE} Starting multi-agent collaborative planning...")
            agent.run_tracker.record_planning_start()

            result = await agent.planning_graph.ainvoke(initial_state, config=config)

            # Extract results from the multi-agent state
            messages = result.get("messages", [])
            shared_plan = result.get("shared_plan", "")
            technical_analysis = result.get("technical_analysis", "")
            architectural_analysis = result.get("architectural_analysis", "")
            consensus_reached = result.get("consensus_reached", False)
            iteration_count = result.get("iteration_count", 0)

            # Collect planning token usage and tool calls
            planning_token_usage = agent.llm.get_usage_records()
            planning_tool_calls = agent._extract_tool_calls_from_messages(messages)

            if trace_ctx:
                trace_ctx.write_messages(messages, phase="planning")
                trace_ctx.write_tool_calls(planning_tool_calls, phase="planning")

            # Record planning completion
            agent.run_tracker.record_planning_completion(
                status="completed" if consensus_reached else "partial",
                iterations=iteration_count,
                messages_count=len(messages),
                technical_analysis=technical_analysis,
                architectural_analysis=architectural_analysis,
                final_plan=shared_plan,
                token_usage=planning_token_usage,
                tool_calls=planning_tool_calls,
            )

            agent.logger.info("\N{WHITE HEAVY CHECK MARK} Multi-agent collaborative planning completed")
            agent.logger.info("\N{BAR CHART} Multi-Agent Planning Summary:")
            agent.logger.info("  - Total messages exchanged: %s", len(messages))
            agent.logger.info("  - Consensus reached: %s", consensus_reached)
            agent.logger.info("  - Iterations completed: %s", iteration_count)
            agent.logger.info("  - Technical analysis length: %s characters", len(technical_analysis))
            agent.logger.info("  - Architectural analysis length: %s characters", len(architectural_analysis))
            agent.logger.info("  - Final plan length: %s characters", len(shared_plan))
            agent.logger.info(
                "  - Planning tokens used: %s",
                sum(t.total_tokens for t in planning_token_usage),
            )

            # Log a preview of the final plan
            if shared_plan:
                lines = shared_plan.split("\n")[:5]
                preview = " | ".join(line.strip() for line in lines if line.strip())
                agent.logger.info("  - Plan preview: %s...", preview[:150])

            if trace_ctx and planning_phase_started:
                trace_ctx.end_phase("planning")
                planning_phase_started = False
                trace_ctx.start_phase("execution")
                execution_phase_started = True

            # Phase 2: Execution Graph
            agent.logger.info("\N{ROCKET} Starting execution phase...")

            # Initialize execution state
            execution_state: ExecutionState = {
                "messages": [],
                "plan": shared_plan,
                "orientation": "",
                "cycle_count": 0,
                "max_cycles": getattr(agent, "max_execution_cycles", 3),
                "agent_status": "running",
                "cycle_results": [],
                "soft_limit": getattr(agent, "soft_limit", None),
                "test_attempts": [],
            }

            # Execute the work cycles with run tracking
            max_cycles = execution_state.get("max_cycles") or getattr(agent, "max_execution_cycles", 50) or 50
            # The execution graph has a fixed 4-node loop per cycle:
            # orient_cycle -> execute_react -> reconcile_results -> check_status.
            # Use a separate, derived recursion limit so outer graph execution doesn't fail
            # when ReAct recursion limits are tuned lower/higher.
            execution_graph_recursion_limit = max(100, (max_cycles * 4) + 25)
            execution_config = {
                "configurable": {"thread_id": run_log.thread_id + "-execution"},
                "recursion_limit": execution_graph_recursion_limit,
            }

            execution_result = await agent.execution_graph.ainvoke(execution_state, config=execution_config)

            # Extract execution results
            final_status = execution_result.get("agent_status", "unknown")
            cycle_results = execution_result.get("cycle_results", [])
            execution_messages = execution_result.get("messages", [])

            # Get token usage for execution phase
            total_tokens = agent.llm.get_total_tokens()
            planning_tokens = sum(t.total_tokens for t in planning_token_usage)
            execution_token_usage = agent.llm.get_usage_records()[len(planning_token_usage) :]

            # Record execution cycles in run tracker
            for i, cycle_result in enumerate(cycle_results):
                cycle_number = i + 1

                # Extract tool calls from cycle (if available)
                cycle_tool_calls = []
                if hasattr(cycle_result, "history") and cycle_result.history:
                    cycle_tool_calls = agent._extract_tool_calls_from_messages(cycle_result.history)

                # Calculate tokens for this cycle (rough approximation)
                cycle_tokens = execution_token_usage[i : i + 1] if i < len(execution_token_usage) else []

                # Record cycle start and completion
                agent.run_tracker.record_execution_cycle_start(
                    cycle_number=cycle_number,
                    orientation=getattr(cycle_result, "orientation", f"Cycle {cycle_number} orientation"),
                )

                agent.run_tracker.record_execution_cycle_completion(
                    cycle_number=cycle_number,
                    status=getattr(cycle_result, "status", "success"),
                    messages_count=len(getattr(cycle_result, "history", [])),
                    tool_calls=cycle_tool_calls,
                    token_usage=cycle_tokens,
                    final_summary=getattr(cycle_result, "final_summary", cycle_result.final_thought),
                    commit_sha=getattr(cycle_result, "commit_sha", None),
                    commit_message=getattr(cycle_result, "commit_message", None),
                    step_count=getattr(cycle_result, "step_count", None),
                    soft_limit=getattr(cycle_result, "soft_limit", None),
                    soft_limit_reached=getattr(cycle_result, "soft_limit_reached", None),
                    steps_in_main_phase=getattr(cycle_result, "steps_in_main_phase", None),
                    steps_in_wrap_up_phase=getattr(cycle_result, "steps_in_wrap_up_phase", None),
                )

                if trace_ctx and hasattr(cycle_result, "history"):
                    trace_ctx.write_messages(cycle_result.history, phase="execution", cycle_number=cycle_number)
                    trace_ctx.write_tool_calls(cycle_tool_calls, phase="execution", cycle_number=cycle_number)

            agent.logger.info("\N{CHEQUERED FLAG} Execution completed with status: %s", final_status)
            agent.logger.info("\N{BAR CHART} Execution Summary:")
            agent.logger.info("  - Cycles completed: %s", len(cycle_results))
            agent.logger.info("  - Final status: %s", final_status)
            agent.logger.info("  - Total execution messages: %s", len(execution_messages))
            agent.logger.info("  - Total tokens used: %s", total_tokens)

            # Create comprehensive summary combining planning and execution
            execution_summary = "\n".join(
                [f"Cycle {i + 1}: {result.final_thought[:100]}..." for i, result in enumerate(cycle_results)]
            )

            full_summary = f"""# CCE Agent Run Complete

## Planning Phase
{shared_plan}

## Execution Phase  
Status: {final_status}
Cycles: {len(cycle_results)}

### Execution Summary:
{execution_summary}

### Token Usage:
Total tokens: {total_tokens}
Planning tokens: {planning_tokens}
Execution tokens: {total_tokens - planning_tokens}
"""

            if trace_ctx and execution_phase_started:
                trace_ctx.end_phase("execution")
                execution_phase_started = False

            # Complete run tracking
            completed_run = agent.run_tracker.complete_run(
                status=final_status,
                final_summary=full_summary,
                error_message="",
            )

            total_duration_seconds = 0.0
            if completed_run.end_time:
                total_duration_seconds = (completed_run.end_time - completed_run.start_time).total_seconds()

            if trace_ctx:
                trace_ctx.write_metrics(
                    {
                        "total_tokens": total_tokens,
                        "planning_tokens": planning_tokens,
                        "execution_tokens": total_tokens - planning_tokens,
                        "cycles_completed": len(cycle_results),
                    }
                )

            return RunResult(
                ticket=ticket,
                thread_id=completed_run.thread_id,
                status=final_status,
                planning_result=completed_run.planning_result,
                execution_cycles=completed_run.execution_cycles,
                final_summary=full_summary,
                error_message="",
                start_time=completed_run.start_time,
                end_time=completed_run.end_time,
                total_duration_seconds=total_duration_seconds,
            )

        except Exception as exc:
            agent.logger.error("Error processing ticket: %s", str(exc))

            if trace_ctx:
                trace_ctx.write_event({"type": "error", "error": str(exc)})

            # Complete run tracking with error
            agent.run_tracker.complete_run(
                status="failed",
                final_summary=f"Run failed due to error: {str(exc)}",
                error_message=str(exc),
            )

            total_duration_seconds = 0.0
            end_time = run_log.end_time if run_log else None
            if run_log and end_time:
                total_duration_seconds = (end_time - run_log.start_time).total_seconds()

            return RunResult(
                ticket=ticket,
                thread_id=run_log.thread_id if run_log else "",
                status="error",
                planning_result=run_log.planning_result if run_log else None,
                execution_cycles=run_log.execution_cycles if run_log else [],
                final_summary=f"Error processing ticket: {str(exc)}",
                error_message=str(exc),
                start_time=run_log.start_time if run_log else None,
                end_time=end_time,
                total_duration_seconds=total_duration_seconds,
            )

        finally:
            agent.trace_ctx = None
            if trace_ctx:
                if planning_phase_started:
                    trace_ctx.end_phase("planning")
                if execution_phase_started:
                    trace_ctx.end_phase("execution")
