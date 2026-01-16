import logging
from datetime import datetime

import pytest

from src.agent import CCEAgent
from src.models import CycleResult


class DummyTracer:
    enabled = False
    traces = []


def make_agent() -> CCEAgent:
    agent = CCEAgent.__new__(CCEAgent)
    agent.logger = logging.getLogger("test_reconcile_cycle_results")
    agent.tracer = DummyTracer()
    return agent


def test_build_reconciliation_result_from_plan_and_test_report():
    agent = make_agent()
    plan = "- [x] Done item\n- [ ] Pending item"
    cycle_result = CycleResult(
        cycle_number=1,
        status="success",
        orientation="focus",
        start_time=datetime.now(),
        final_summary="Did work\nNext focus: Pending item",
    )
    test_report = "**Passed Tests**: 2\n**Failed Tests**: 1"

    result = agent._build_reconciliation_result(
        cycle_number=1,
        cycle_result=cycle_result,
        plan_text=plan,
        test_results=test_report,
        evaluation_result=None,
        commit_sha="abc123",
    )

    assert result.items_completed == ["Done item"]
    assert result.items_in_progress == ["Pending item"]
    assert result.tests_passed == 2
    assert result.tests_failed == 1
    assert result.next_focus_suggestion == "Pending item"
    assert result.commit_sha == "abc123"


@pytest.mark.asyncio
async def test_simple_reconcile_emits_serialized_payload():
    agent = make_agent()

    async def fake_run_reconciliation_tests(_state):
        return None

    agent._run_reconciliation_tests = fake_run_reconciliation_tests
    plan = "- [x] Done item\n- [ ] Pending item"
    cycle_result = CycleResult(
        cycle_number=1,
        status="success",
        orientation="focus",
        start_time=datetime.now(),
        final_summary="Did work\nNext focus: Pending item",
    )

    state = {
        "cycle_count": 1,
        "plan": plan,
        "cycle_results": [cycle_result],
        "test_results": "**Passed Tests**: 3\n**Failed Tests**: 0",
        "evaluation_result": None,
    }

    result = await agent._simple_reconcile_cycle_results(state)

    payload = result["reconciliation_result"]
    assert isinstance(payload, str)
    assert "Did work" in payload
