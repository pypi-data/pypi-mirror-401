import logging
import os
import sys
import types
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

if "deepagents.state" not in sys.modules:
    deepagents_module = types.ModuleType("deepagents")
    deepagents_state_module = types.ModuleType("deepagents.state")
    deepagents_tools_module = types.ModuleType("deepagents.tools")

    deepagents_state_module.DeepAgentState = object
    deepagents_module.SubAgent = object

    def _create_deep_agent(*args, **kwargs):
        return None

    def _write_todos(*args, **kwargs):
        return None

    deepagents_module.create_deep_agent = _create_deep_agent
    deepagents_tools_module.write_todos = _write_todos
    deepagents_module.state = deepagents_state_module
    deepagents_module.tools = deepagents_tools_module

    sys.modules["deepagents"] = deepagents_module
    sys.modules["deepagents.state"] = deepagents_state_module
    sys.modules["deepagents.tools"] = deepagents_tools_module

if "src.deep_agents" not in sys.modules:
    deep_agents_pkg = types.ModuleType("src.deep_agents")
    deep_agents_pkg.__path__ = []
    hybrid_tools_module = types.ModuleType("src.deep_agents.hybrid_filesystem_tools")

    def _initialize_virtual_filesystem_from_workspace(*args, **kwargs):
        return {}

    hybrid_tools_module.initialize_virtual_filesystem_from_workspace = _initialize_virtual_filesystem_from_workspace
    sys.modules["src.deep_agents"] = deep_agents_pkg
    sys.modules["src.deep_agents.hybrid_filesystem_tools"] = hybrid_tools_module

from src.agent import CCEAgent
from src.models import CycleResult, PlanResult, ReconciliationResult, Ticket


class _TracerStub:
    def trace_decision_event(self, *args, **kwargs):
        return None


def make_agent(max_cycles: int = 3) -> CCEAgent:
    agent = CCEAgent.__new__(CCEAgent)
    agent.logger = logging.getLogger("test.determine_next_action")
    agent.tracer = _TracerStub()
    agent.max_execution_cycles = max_cycles
    return agent


def make_ticket() -> Ticket:
    return Ticket(
        number=98,
        title="Determine next action",
        description="Test ticket",
        url="https://github.com/jkbrooks/cce-agent/issues/98",
    )


def make_cycle(status: str = "success", summary: str = "") -> CycleResult:
    return CycleResult(
        cycle_number=1,
        status=status,
        orientation="",
        start_time=datetime.now(),
        final_summary=summary,
        final_thought=summary,
    )


def test_determine_next_action_running_when_work_remaining():
    agent = make_agent()
    plan = {"plan_items": [{"status": "in_progress"}]}
    reconciliation = {"test_results": "Tests pending"}
    cycles = [make_cycle(status="success")]

    decision = agent.determine_next_action(make_ticket(), plan, reconciliation, cycles)
    assert decision == "running"


def test_determine_next_action_submitting_when_complete_and_tests_pass():
    agent = make_agent()
    plan = {"plan_items": [{"status": "completed"}, {"status": "completed"}]}
    reconciliation = {"test_results": "All tests passed"}
    cycles = [make_cycle(status="success")]

    decision = agent.determine_next_action(make_ticket(), plan, reconciliation, cycles)
    assert decision == "submitting"


def test_determine_next_action_failed_on_critical_errors():
    agent = make_agent()
    plan = {"plan_items": [{"status": "completed"}]}
    reconciliation = {"test_results": "All tests passed", "critical_errors": ["build_failed"]}
    cycles = [make_cycle(status="success")]

    decision = agent.determine_next_action(make_ticket(), plan, reconciliation, cycles)
    assert decision == "failed"


def test_determine_next_action_failed_on_cycle_limit():
    agent = make_agent(max_cycles=2)
    plan = {"plan_items": [{"status": "in_progress"}]}
    reconciliation = {"test_results": "Tests pending"}
    cycles = [make_cycle(status="success"), make_cycle(status="success")]

    decision = agent.determine_next_action(make_ticket(), plan, reconciliation, cycles)
    assert decision == "failed"


def test_determine_next_action_agent_signal_requires_verification():
    agent = make_agent()
    plan = {"plan_items": [{"status": "in_progress"}]}
    reconciliation = {"test_results": "All tests passed"}
    cycles = [make_cycle(status="success", summary="Ready to submit")]

    decision = agent.determine_next_action(make_ticket(), plan, reconciliation, cycles)
    assert decision == "running"


def test_determine_next_action_submits_on_checkbox_plan_and_tests_passing():
    agent = make_agent()
    plan = PlanResult(plan="- [x] Task 1\n- [x] Task 2")
    reconciliation = ReconciliationResult(tests_passing=True)
    cycles = [make_cycle(status="success")]

    decision = agent.determine_next_action(make_ticket(), plan, reconciliation, cycles)
    assert decision == "submitting"


def test_determine_next_action_honors_agent_completion_signal():
    agent = make_agent()
    plan = PlanResult(plan="- [x] Task 1")
    reconciliation = ReconciliationResult(tests_passing=None)
    cycle_history = [{"status": "success", "ready_to_end": True}]

    decision = agent.determine_next_action(
        ticket=make_ticket(),
        plan=plan,
        reconciliation=reconciliation,
        cycle_history=cycle_history,
    )
    assert decision == "submitting"
