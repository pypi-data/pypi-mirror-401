import logging
from datetime import datetime

from src.agent import CCEAgent
from src.models import CycleResult, RunLog, Ticket


class DummyTracer:
    enabled = False
    traces = []


def make_agent() -> CCEAgent:
    agent = CCEAgent.__new__(CCEAgent)
    agent.logger = logging.getLogger("test_orient_for_next_cycle")
    agent.tracer = DummyTracer()
    return agent


def make_run_log() -> RunLog:
    ticket = Ticket(
        number=96,
        title="Orient test",
        description="Test orient_for_next_cycle",
        url="https://github.com/jkbrooks/cce-agent/issues/96",
    )
    return RunLog(
        thread_id="test-thread",
        run_id="test-run",
        ticket=ticket,
        start_time=datetime.now(),
    )


def test_orient_first_cycle_uses_first_plan_item():
    agent = make_agent()
    plan = "- [ ] First task\n- [ ] Second task"
    run_log = make_run_log()

    result = agent.orient_for_next_cycle(plan=plan, cycle_history=[], run_log=run_log)

    assert result.focus == "First task"
    assert result.cycle_number == 1
    assert "First task" in result.relevant_plan_items


def test_orient_uses_previous_suggestion_when_matching_plan_item():
    agent = make_agent()
    plan = "- [ ] Setup scaffolding\n- [ ] Add retry guidance\n- [ ] Write tests"
    run_log = make_run_log()

    previous_cycle = CycleResult(
        cycle_number=1,
        status="success",
        orientation="previous",
        start_time=datetime.now(),
        final_summary="Next: Add retry guidance",
    )

    result = agent.orient_for_next_cycle(plan=plan, cycle_history=[previous_cycle], run_log=run_log)

    assert result.focus == "Add retry guidance"
    assert result.previous_suggestion == "Add retry guidance"


def test_orient_when_plan_complete_falls_back_to_wrap_up():
    agent = make_agent()
    plan = "- [x] Done item\n- [x] Another done item"
    run_log = make_run_log()

    result = agent.orient_for_next_cycle(plan=plan, cycle_history=[], run_log=run_log)

    assert result.focus == "Review completed work and finalize any remaining items"
