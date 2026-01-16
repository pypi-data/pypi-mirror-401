import logging
import os
import re
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage

# No longer need dotenv here
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.types import Command

from src.agent.core import process_ticket as process_ticket_core
from src.agent.graphs.execution import create_execution_graph
from src.agent.graphs.planning import create_planning_graph
from src.agent.phases.execution import (
    determine_next_action,
    execute_react_cycle,
    orient_for_next_cycle,
    reconcile_cycle_results,
)
from src.agent.phases.planning import merge_analyses as merge_planning_analyses
from src.agent.state import ExecutionState, PlanningState
from src.agent.tools.registry import initialize_tooling
from src.agent.utils import (
    extract_tool_calls_from_messages,
    trim_messages_for_context,
)
from src.environments.base import BaseEnvironment
from src.environments.local import LocalEnvironment
from src.config import get_max_execution_cycles, get_recursion_limit, get_soft_limit
from src.models import (
    CycleCompleteSignal,
    CycleReconciliationResult,
    CycleResult,
    OrientationResult,
    PlanResult,
    PlanningResult,
    ReconciliationResult,
    RunResult,
    Ticket,
    TokenUsage,
    ToolCall,
)
from src.observability.cycle_metrics import CycleMetricsCollector
from src.run_manifest import RunManifest
from src.token_tracker import TokenTrackingLLM
from src.tools.command_orchestrator import CommandOrchestrator

# Type alias for a structured plan
Plan = str  # For the MVP, a plan is just a string.


def _read_timeout_env(keys: list[str], default: int) -> int:
    for key in keys:
        value = os.getenv(key)
        if value is None:
            continue
        try:
            return max(1, int(value))
        except (TypeError, ValueError):
            logging.getLogger(__name__).warning("Invalid timeout value for %s=%s; using default %s", key, value, default)
            break
    return default


class CCEAgent:
    """
    The core implementation of the Constitutional Context Engineering Agent.

    This class orchestrates the entire process of handling a ticket,
    from planning to execution and final submission.
    """

    def __init__(
        self,
        primary_environment: BaseEnvironment | None = None,
        workspace_environment: BaseEnvironment | None = None,
        workspace_root: str | None = None,
        git_base_branch: str | None = None,
        enable_git_workflow: bool | None = None,
    ):
        """
        Initializes the agent with environment connectors.

        Args:
            primary_environment: Environment for agent state, logs, and metadata.
                                If None, defaults to LocalEnvironment.
            workspace_environment: Environment where actual work is performed.
                                  If None, defaults to same as primary_environment.
        """
        # Env vars are now loaded in main.py
        # load_dotenv()

        if workspace_root and workspace_environment is None:
            workspace_environment = LocalEnvironment(workspace_root)
        if workspace_root and primary_environment is None:
            primary_environment = LocalEnvironment(workspace_root)

        self.primary_env = primary_environment if primary_environment else LocalEnvironment()
        self.workspace_env = workspace_environment if workspace_environment else self.primary_env
        self.workspace_root = workspace_root or getattr(self.workspace_env, "workspace_root", None)
        if self.workspace_root:
            from src.workspace_context import set_workspace_root

            set_workspace_root(self.workspace_root)
        self.git_base_branch = git_base_branch
        self.enable_git_workflow = enable_git_workflow
        self.max_execution_cycles = get_max_execution_cycles()
        self.soft_limit = get_soft_limit()
        self.recursion_limit = get_recursion_limit()
        self.use_command_orchestrated_planning = True

        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.react_timeout = _read_timeout_env(["CCE_REACT_TIMEOUT", "REACT_TIMEOUT"], 900)
        self.llm_invoke_timeout = _read_timeout_env(["CCE_LLM_INVOKE_TIMEOUT", "LLM_INVOKE_TIMEOUT"], 300)
        self.logger.info(
            "Timeouts configured: react_timeout=%s llm_invoke_timeout=%s",
            self.react_timeout,
            self.llm_invoke_timeout,
        )

        # Initialize Run Tracker for comprehensive logging
        self.run_tracker = RunManifest()
        self.command_orchestrator = CommandOrchestrator()
        self.cycle_metrics = CycleMetricsCollector()
        self.trace_ctx = None

        # Initialize Token Tracking LLM - GPT-4.1 with 1M token context window
        self.llm = TokenTrackingLLM(model="gpt-4.1", temperature=0)

        # Initialize Tool Services (Dependency Injection)
        (
            self.shell_runner,
            self.edit_engine,
            self.git_ops,
            self.code_analyzer,
            self.all_tools,
            self.planning_tools,
        ) = initialize_tooling(self.workspace_env)

        # Execution tools have no restrictions - all tools available
        self.tools = self.all_tools

        # Initialize LangGraph components
        self.memory = MemorySaver()
        # Separate graphs: planning and execution
        self.planning_graph = self._create_planning_graph()
        self.execution_graph = self._create_execution_graph()

        self.logger.info(
            f"CCEAgent initialized - Primary: {self.primary_env.__class__.__name__}, "
            f"Workspace: {self.workspace_env.__class__.__name__}"
        )
        self.logger.info(
            f"LangGraph initialized with {len(self.all_tools)} total tools, {len(self.planning_tools)} for planning"
        )

    def _trim_messages_for_context(self, messages: list[BaseMessage], max_tokens: int = 800000) -> list[BaseMessage]:
        """
        Trim messages to fit within context window using LangChain's trim_messages utility.

        This implements Phase 1 of context length management - intelligent message trimming
        that preserves conversation structure and system messages while staying within
        token limits.

        Args:
            messages: List of messages to trim
            max_tokens: Maximum tokens to keep (default 800k to leave buffer for GPT-4.1's ~1M limit)

        Returns:
            Trimmed list of messages that fit within context window
        """
        if not messages:
            return messages

        try:
            trimmed = trim_messages_for_context(
                messages,
                token_counter=self.llm.llm,
                max_tokens=max_tokens,
            )

            if len(trimmed) < len(messages):
                self.logger.info(
                    f"🔧 Context management: Trimmed {len(messages)} messages to {len(trimmed)} "
                    f"to fit within {max_tokens} token limit"
                )

            return trimmed

        except Exception as e:
            self.logger.warning(f"Failed to trim messages: {e}. Using original messages.")
            return messages

    def _create_planning_graph(self) -> StateGraph:
        """Create the multi-agent collaborative planning graph."""
        if getattr(self, "use_command_orchestrated_planning", False):
            return self._create_command_orchestrated_planning_graph()
        return create_planning_graph(self)

    def _create_command_orchestrated_planning_graph(self) -> StateGraph:
        """Create a command-orchestrated planning graph."""
        from langgraph.graph import END, START, StateGraph

        from src.agent.state import PlanningState

        async def command_planning(state: PlanningState) -> dict[str, Any]:
            messages = state.get("messages", [])
            last_message = messages[-1] if messages else None
            ticket_description = getattr(last_message, "content", "") if last_message else ""
            ticket_description = (ticket_description or "").strip()

            if not ticket_description:
                plan_text = "Command-orchestrated planning failed: empty request."
                ai_message = AIMessage(content=f"COMMAND-ORCHESTRATED PLAN\n\n{plan_text}")
                return {
                    "messages": [ai_message],
                    "shared_plan": plan_text,
                    "consensus_reached": False,
                    "structured_phases": [],
                    "iteration_count": state.get("iteration_count", 0) + 1,
                }

            orchestrator = getattr(self, "command_orchestrator", None) or CommandOrchestrator()
            self.command_orchestrator = orchestrator

            try:
                orchestration_result = await orchestrator.orchestrate_planning_sequence(
                    ticket_description, workspace_root=self.workspace_root
                )
            except Exception as exc:
                orchestration_result = None
                plan_text = f"Command-orchestrated planning failed: {exc}"
                ai_message = AIMessage(content=f"COMMAND-ORCHESTRATED PLAN\n\n{plan_text}")
                return {
                    "messages": [ai_message],
                    "shared_plan": plan_text,
                    "consensus_reached": False,
                    "structured_phases": [],
                    "iteration_count": state.get("iteration_count", 0) + 1,
                }

            plan_payload = orchestration_result.final_result if orchestration_result else None
            structured_phases = []

            if isinstance(plan_payload, dict):
                plan_text = plan_payload.get("markdown_plan") or plan_payload.get("plan") or ""
                structured_phases = plan_payload.get("structured_phases") or []
            else:
                plan_text = str(plan_payload or "")

            if len(plan_text) < 200:
                plan_text = self._build_fallback_plan(ticket_description, plan_text)

            ai_message = AIMessage(content=f"COMMAND-ORCHESTRATED PLAN\n\n{plan_text}")
            consensus = True if ticket_description else False

            return {
                "messages": [ai_message],
                "shared_plan": plan_text,
                "consensus_reached": consensus,
                "structured_phases": structured_phases,
                "iteration_count": state.get("iteration_count", 0) + 1,
            }

        workflow = StateGraph(PlanningState)
        workflow.add_node("command_planning", command_planning)
        workflow.add_edge(START, "command_planning")
        workflow.add_edge("command_planning", END)

        return workflow.compile(checkpointer=self.memory)

    def _merge_analyses(self, state: PlanningState) -> str:
        """Merge technical and architectural analyses into a final plan."""
        return merge_planning_analyses(state)

    # Remove the old _planning_node, as it's replaced by the new graph structure.

    def _create_execution_graph(self) -> StateGraph:
        """Create the execution graph that handles iterative work cycles."""
        return create_execution_graph(self)

    def _orient_for_next_cycle(self, state: ExecutionState) -> dict[str, Any]:
        """Simple prompt-based orientation for the next execution cycle."""
        return orient_for_next_cycle(self, state)

    async def _execute_react_cycle(self, state: ExecutionState) -> dict[str, Any]:
        """Execute a ReAct cycle with tool access and conversation persistence."""
        return await execute_react_cycle(self, state)

    async def _reconcile_cycle_results(self, state: ExecutionState) -> dict[str, Any]:
        """Process and log the results of the completed cycle."""
        return await reconcile_cycle_results(self, state)

    def _determine_next_action(self, state: ExecutionState) -> dict[str, Any]:
        """Determine whether to continue, complete, or fail based on current state."""
        return determine_next_action(self, state)

    async def process_ticket(self, ticket: Ticket) -> RunResult:
        """
        The main entry point for the agent to process a single ticket.
        Uses a true multi-agent collaborative planning system with handoffs
        and comprehensive run tracking.
        """
        return await process_ticket_core(self, ticket)

    def _extract_tool_calls_from_messages(self, messages) -> list[ToolCall]:
        """
        Extract tool calls from LangChain messages for audit trail.

        Args:
            messages: List of LangChain messages

        Returns:
            List of ToolCall records
        """
        return extract_tool_calls_from_messages(messages)

    def _build_fallback_plan(self, ticket_description: str, existing_plan: str | None = None) -> str:
        summary = existing_plan.strip() if existing_plan else ""
        if not summary:
            summary = "No generated plan content was available; using a structured fallback plan."

        return (
            "## Ticket Summary\n"
            f"{ticket_description}\n\n"
            "## Plan Overview\n"
            f"{summary}\n\n"
            "## Phase 1: Discovery\n"
            "- Identify the relevant modules and entry points referenced in the request.\n"
            "- Review configuration, tooling, and workflow dependencies.\n"
            "- Document current behaviors and edge cases.\n\n"
            "## Phase 2: Implementation\n"
            "- Apply focused changes in small, testable steps.\n"
            "- Keep changes aligned with existing code patterns.\n"
            "- Add guardrails for error handling and rollback paths.\n\n"
            "## Phase 3: Validation\n"
            "- Run targeted unit and integration tests.\n"
            "- Validate behavior against the ticket expectations.\n"
            "- Capture any follow-up work items.\n\n"
            "## Risks and Mitigations\n"
            "- Risk: Scope creep. Mitigation: Keep changes tightly scoped to the request.\n"
            "- Risk: Regression. Mitigation: Add or update tests and validate outputs.\n\n"
            "## Success Criteria\n"
            "- Core functionality implemented and verified.\n"
            "- Tests pass for affected areas.\n"
            "- Documentation or notes updated if behavior changes.\n"
        )

    def _extract_plan_items(self, plan_text: str) -> tuple[list[str], list[str]]:
        completed: list[str] = []
        in_progress: list[str] = []

        for line in plan_text.splitlines():
            match = re.match(r"\s*-\s*\[(?P<status>[xX ])\]\s+(?P<item>.+)", line)
            if not match:
                continue
            item = match.group("item").strip()
            status = match.group("status")
            if status.lower() == "x":
                completed.append(item)
            else:
                in_progress.append(item)

        return completed, in_progress

    def _extract_next_focus(self, summary: str) -> str | None:
        if not summary:
            return None
        for line in summary.splitlines():
            lowered = line.lower().strip()
            if lowered.startswith("next focus:"):
                return line.split(":", 1)[1].strip()
            if lowered.startswith("next:"):
                return line.split(":", 1)[1].strip()
        return None

    def _parse_test_counts(self, test_results: Any) -> tuple[int, int]:
        if isinstance(test_results, dict):
            passed = int(test_results.get("tests_passed") or 0)
            failed = int(test_results.get("tests_failed") or 0)
            return passed, failed

        if isinstance(test_results, str):
            cleaned = test_results.replace("*", "")
            passed_match = re.search(r"Passed Tests:\s*(\d+)", cleaned)
            failed_match = re.search(r"Failed Tests:\s*(\d+)", cleaned)
            passed = int(passed_match.group(1)) if passed_match else 0
            failed = int(failed_match.group(1)) if failed_match else 0

            if "all tests passed" in cleaned.lower():
                passed = max(passed, 1)
            return passed, failed

        return 0, 0

    def _plan_is_complete(self, plan: Any) -> bool:
        if isinstance(plan, PlanResult):
            completed, pending = self._extract_plan_items(plan.plan)
            return bool(completed) and not pending

        if isinstance(plan, dict):
            plan_items = plan.get("plan_items")
            if isinstance(plan_items, list) and plan_items:
                statuses = [item.get("status") for item in plan_items if isinstance(item, dict)]
                if statuses:
                    return all(status == "completed" for status in statuses)

            plan_text = plan.get("plan")
            if isinstance(plan_text, str):
                completed, pending = self._extract_plan_items(plan_text)
                return bool(completed) and not pending

        if isinstance(plan, str):
            completed, pending = self._extract_plan_items(plan)
            return bool(completed) and not pending

        return False

    def _tests_passing(self, reconciliation: Any) -> bool | None:
        if isinstance(reconciliation, ReconciliationResult):
            return reconciliation.tests_passing

        if isinstance(reconciliation, dict):
            if "tests_passed" in reconciliation or "tests_failed" in reconciliation:
                passed, failed = self._parse_test_counts(reconciliation)
                if failed > 0:
                    return False
                if passed > 0:
                    return True
            test_results = reconciliation.get("test_results")
            passed, failed = self._parse_test_counts(test_results)
            if failed > 0:
                return False
            if passed > 0:
                return True

        return None

    def determine_next_action(self, ticket: Ticket, plan: Any, reconciliation: Any, cycle_history: list[Any]) -> str:
        max_cycles = getattr(self, "max_execution_cycles", None)
        if max_cycles is not None and len(cycle_history) >= max_cycles:
            return "failed"

        critical_errors: list[str] = []
        if isinstance(reconciliation, ReconciliationResult):
            critical_errors = reconciliation.critical_errors
        elif isinstance(reconciliation, dict):
            critical_errors = reconciliation.get("critical_errors") or []

        if critical_errors:
            return "failed"

        for cycle in cycle_history:
            ready = cycle.get("ready_to_end") if isinstance(cycle, dict) else getattr(cycle, "ready_to_end", False)
            if ready:
                return "submitting"

        plan_complete = self._plan_is_complete(plan)
        tests_passing = self._tests_passing(reconciliation)

        if plan_complete and tests_passing is True:
            return "submitting"

        return "running"

    def orient_for_next_cycle(self, plan: str | PlanResult, cycle_history: list[CycleResult], run_log) -> OrientationResult:
        plan_text = plan.plan if isinstance(plan, PlanResult) else str(plan)
        completed, pending = self._extract_plan_items(plan_text)
        previous_suggestion = None
        focus = None

        if cycle_history:
            previous_suggestion = self._extract_next_focus(cycle_history[-1].final_summary or "")
            if previous_suggestion and previous_suggestion in pending:
                focus = previous_suggestion

        if not focus and pending:
            focus = pending[0]

        if not focus and completed and not pending:
            focus = "Review completed work and finalize any remaining items"

        if not focus:
            focus = "Review completed work and finalize any remaining items"

        cycle_number = len(cycle_history) + 1
        return OrientationResult(
            focus=focus,
            focus_description=focus,
            relevant_files=[],
            relevant_plan_items=[focus] if focus else [],
            suggested_approach="",
            acceptance_criteria=[],
            previous_cycle_summary=cycle_history[-1].final_summary if cycle_history else None,
            previous_suggestion=previous_suggestion,
            cycle_number=cycle_number,
        )

    def _detect_cycle_complete_signal(self, messages) -> CycleCompleteSignal | None:
        for message in messages:
            tool_calls = getattr(message, "tool_calls", None)
            if not tool_calls:
                continue
            for tool_call in tool_calls:
                if tool_call.get("name") != "signal_cycle_complete":
                    continue
                args = tool_call.get("args") or {}
                return CycleCompleteSignal(
                    summary=args.get("summary", ""),
                    work_remaining=args.get("work_remaining", ""),
                    next_focus_suggestion=args.get("next_focus_suggestion", ""),
                    method="tool_call",
                    raw_content=str(tool_call),
                )
        return None

    def _format_commit_message(
        self,
        cycle_number: int,
        cycle_result: CycleResult,
        test_results: Any,
        evaluation_result: Any,
    ) -> str:
        summary_line = (cycle_result.final_summary or "").splitlines()[0].strip()
        passed, failed = self._parse_test_counts(test_results)
        next_focus = self._extract_next_focus(cycle_result.final_summary or "")

        lines = [
            f"chore: reconcile cycle {cycle_number}",
            "",
            f"Summary: {summary_line}" if summary_line else "Summary: (no summary)",
            f"Tests: {passed} passed, {failed} failed",
        ]
        if next_focus:
            lines.append(f"Next focus: {next_focus}")
        return "\n".join(lines)

    def _commit_cycle_work(
        self,
        cycle_number: int,
        cycle_result: CycleResult,
        test_results: Any,
        evaluation_result: Any,
    ) -> str | None:
        if getattr(self, "enable_git_workflow", True) is False:
            return None

        if not getattr(self, "git_ops", None):
            return None

        if cycle_result.status != "success":
            return None

        passed, failed = self._parse_test_counts(test_results)
        if failed > 0:
            return None

        if not self.git_ops.has_changes():
            return None

        if not self.git_ops.add_all():
            return None

        commit_message = self._format_commit_message(
            cycle_number=cycle_number,
            cycle_result=cycle_result,
            test_results=test_results,
            evaluation_result=evaluation_result,
        )
        commit_result = self.git_ops.commit(commit_message)
        if not commit_result.success:
            return None

        cycle_result.commit_message = commit_message
        cycle_result.commit_sha = commit_result.commit_sha
        return commit_result.commit_sha

    def _build_reconciliation_result(
        self,
        cycle_number: int,
        cycle_result: CycleResult,
        plan_text: str,
        test_results: Any,
        evaluation_result: Any,
        commit_sha: str | None = None,
    ) -> CycleReconciliationResult:
        completed, in_progress = self._extract_plan_items(plan_text)
        passed, failed = self._parse_test_counts(test_results)
        next_focus = self._extract_next_focus(cycle_result.final_summary or "")

        return CycleReconciliationResult(
            cycle_number=cycle_number,
            status=cycle_result.status,
            items_completed=completed,
            items_in_progress=in_progress,
            tests_passed=passed,
            tests_failed=failed,
            commit_sha=commit_sha,
            next_focus_suggestion=next_focus,
            summary=cycle_result.final_summary or "",
        )

    async def _execute_testing_phase(
        self, execution_state: dict[str, Any], final_return_state: dict[str, Any], ticket_title: str, ticket_description: str
    ) -> dict[str, Any]:
        try:
            from src.agent_testing_improvements import (
                SmartTestDiscovery,
                build_test_attempt,
                get_max_test_retries,
                should_retry_test_failure,
            )
            from src.tools.validation.testing import FrameworkTestManager

            workspace_root = self.workspace_root or "."
            testing = FrameworkTestManager(workspace_root)
            changed_files: list[str] = []
            scoped_tests: list[str] = []
            target_files: list[str] | None = None

            if getattr(self, "git_ops", None):
                try:
                    changed_files = self.git_ops.get_modified_files()
                    if not changed_files:
                        changed_files = self.git_ops.get_changed_files("HEAD~1")
                except Exception as exc:
                    self.logger.warning("Testing scope detection failed: %s", exc)

            changed_file_paths = changed_files
            if changed_files:
                changed_file_paths = [
                    path if os.path.isabs(path) else os.path.join(workspace_root, path) for path in changed_files
                ]
                try:
                    scoped_tests = SmartTestDiscovery(workspace_root).discover_relevant_tests(changed_file_paths)
                    if scoped_tests:
                        target_files = scoped_tests
                except Exception as exc:
                    self.logger.warning("Smart test discovery failed: %s", exc)

            def summarize_results(results: dict[str, Any]) -> dict[str, Any]:
                if not results:
                    return {"summary": "no tests detected", "tests_passed": 0, "tests_failed": 0, "tests_run": 0}

                total_tests = 0
                total_passed = 0
                total_failed = 0
                total_skipped = 0

                detailed_results: dict[str, list[dict[str, Any]]] = {}
                tests_run_details: list[dict[str, Any]] = []
                for language, language_results in results.items():
                    detailed_results[language] = [result.to_dict() for result in language_results]
                    for result in language_results:
                        total_tests += result.tests_run
                        total_passed += result.tests_passed
                        total_failed += result.tests_failed
                        total_skipped += result.tests_skipped
                        command = " ".join(result.command) if getattr(result, "command", None) else ""
                        selected_tests = getattr(result, "selected_tests", [])
                        tests_run_details.append(
                            {
                                "framework": result.framework,
                                "command": command,
                                "selected_tests": selected_tests,
                                "tests_run": result.tests_run,
                                "tests_passed": result.tests_passed,
                                "tests_failed": result.tests_failed,
                                "tests_skipped": result.tests_skipped,
                            }
                        )

                if total_tests == 0:
                    summary = "no tests detected"
                elif total_failed == 0:
                    summary = "tests ok"
                else:
                    summary = "tests failed"

                suggested_test_plan = None
                if total_tests == 0:
                    suggested_test_plan = testing.suggest_test_plan(target_files=target_files)

                return {
                    "summary": summary,
                    "tests_run": total_tests,
                    "tests_passed": total_passed,
                    "tests_failed": total_failed,
                    "tests_skipped": total_skipped,
                    "frameworks": list(results.keys()),
                    "details": detailed_results,
                    "tests_run_details": tests_run_details,
                    "suggested_test_plan": suggested_test_plan,
                }

            max_attempts = max(1, min(get_max_test_retries(), 3))
            attempt_number = 0
            attempt_records: list[dict[str, Any]] = []
            tests_summary: dict[str, Any] = {}
            final_scope = "full test suite"

            while True:
                attempt_number += 1
                attempt_scope = "scoped tests" if target_files else "full test suite"
                final_scope = attempt_scope
                fast_mode = bool(target_files) and attempt_number == 1
                results = testing.run_tests(target_files=target_files, fast_mode=fast_mode)
                tests_summary = summarize_results(results)
                has_failures = tests_summary.get("tests_failed", 0) > 0

                attempt = build_test_attempt(
                    test_path=attempt_scope,
                    attempt_number=attempt_number,
                    passed=not has_failures,
                    failure_reason=None if not has_failures else tests_summary.get("summary"),
                )
                attempt_data = {
                    "test_path": attempt.test_path,
                    "attempt_number": attempt.attempt_number,
                    "passed": attempt.passed,
                    "failure_reason": attempt.failure_reason,
                    "fix_applied": attempt.fix_applied,
                    "timestamp": attempt.timestamp.isoformat(),
                }
                if isinstance(execution_state, dict):
                    execution_state.setdefault("test_attempts", []).append(attempt_data)
                attempt_records.append(attempt_data)

                if not should_retry_test_failure(attempt_number, max_attempts, has_failures):
                    break

                # Retry strategy: expand to full suite after a scoped failure.
                if target_files is not None:
                    target_files = None

            tests_summary["attempts"] = attempt_records
            tests_summary["retries"] = max(0, attempt_number - 1)
            tests_summary["changed_files"] = changed_files
            tests_summary["scoped_tests"] = scoped_tests
            tests_summary["scope"] = final_scope

            return tests_summary
        except Exception as exc:
            self.logger.warning("Testing phase failed: %s", exc)
            return {"summary": f"tests failed: {exc}", "tests_passed": 0, "tests_failed": 1, "tests_run": 0}

    def _record_cycle_metrics(self, cycle_result: CycleResult) -> None:
        if not cycle_result:
            return

        if not hasattr(self, "cycle_metrics"):
            return

        try:
            metrics = self.cycle_metrics.record_cycle(cycle_result)
            cycle_result.cycle_metrics = metrics.to_dict()

            trace_ctx = getattr(self, "trace_ctx", None)
            if trace_ctx:
                trace_ctx.write_metrics(self.cycle_metrics.to_dict())

            from src.observability.tracers import attach_cycle_metrics_metadata

            attach_cycle_metrics_metadata(metrics)
        except Exception as exc:
            self.logger.debug("Cycle metrics collection failed: %s", exc, exc_info=True)

    async def _simple_reconcile_cycle_results(self, state: dict[str, Any]) -> dict[str, Any]:
        cycle_count = state.get("cycle_count", 0)
        plan_text = state.get("plan", "")
        cycle_result = state.get("cycle_results", [])[-1] if state.get("cycle_results") else None
        evaluation_result = state.get("evaluation_result")

        test_results = state.get("test_results")
        if test_results is None:
            test_results = await self._execute_testing_phase(state, state, "", "")

        tests_passed = 0
        tests_failed = 0
        tests_run = 0
        if isinstance(test_results, dict):
            tests_summary = test_results.get("summary")
            tests_passed = int(test_results.get("tests_passed", 0))
            tests_failed = int(test_results.get("tests_failed", 0))
            tests_run = int(test_results.get("tests_run") or (tests_passed + tests_failed))
            test_results_text = f"**Passed Tests**: {tests_passed}\n**Failed Tests**: {tests_failed}"
        else:
            tests_summary = None
            test_results_text = str(test_results)
            tests_passed, tests_failed = self._parse_test_counts(test_results_text)
            tests_run = tests_passed + tests_failed

        reconciliation = None
        commit_sha = None
        if cycle_result:
            cycle_result.tests_run = tests_run
            cycle_result.tests_passed = tests_passed
            cycle_result.tests_failed = tests_failed
            commit_sha = self._commit_cycle_work(
                cycle_number=cycle_count,
                cycle_result=cycle_result,
                test_results=test_results_text,
                evaluation_result=evaluation_result,
            )
            reconciliation = self._build_reconciliation_result(
                cycle_number=cycle_count,
                cycle_result=cycle_result,
                plan_text=plan_text,
                test_results=test_results_text,
                evaluation_result=evaluation_result,
                commit_sha=commit_sha,
            )
            self._record_cycle_metrics(cycle_result)

        summary_parts = []
        if cycle_result and cycle_result.final_summary:
            summary_parts.append(cycle_result.final_summary)
        if tests_summary:
            summary_parts.append(f"Testing: {tests_summary}")

        reconciliation_text = "\n".join(summary_parts).strip() if summary_parts else ""

        return {
            "reconciliation_result": reconciliation_text,
            "test_results": test_results,
            "evaluation_result": evaluation_result,
            "reconciliation_data": reconciliation,
        }
