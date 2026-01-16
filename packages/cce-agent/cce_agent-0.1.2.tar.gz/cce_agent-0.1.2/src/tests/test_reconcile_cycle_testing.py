import logging
import os
import sys
from datetime import datetime

import pytest

sys.path.insert(0, os.path.abspath("."))

from src.agent import CCEAgent
from src.models import CycleResult


class DummyTracer:
    enabled = False
    traces = []


def make_agent() -> CCEAgent:
    agent = CCEAgent.__new__(CCEAgent)
    agent.logger = logging.getLogger("test_reconcile_cycle_testing")
    agent.tracer = DummyTracer()
    return agent


@pytest.mark.asyncio
async def test_simple_reconcile_runs_testing(monkeypatch):
    agent = make_agent()

    async def fake_execute_testing_phase(execution_state, final_return_state, ticket_title, ticket_description):
        return {"summary": "tests ok", "tests_passed": 1, "tests_failed": 0}

    monkeypatch.setattr(agent, "_execute_testing_phase", fake_execute_testing_phase)

    state = {
        "cycle_count": 1,
        "plan": "Plan",
        "cycle_results": [
            CycleResult(
                cycle_number=1,
                status="success",
                orientation="focus",
                start_time=datetime.now(),
                final_summary="Did work",
            )
        ],
        "test_attempts": [],
    }

    result = await agent._simple_reconcile_cycle_results(state)

    assert result["test_results"]["tests_passed"] == 1
    assert "Testing: tests ok" in result["reconciliation_result"]
