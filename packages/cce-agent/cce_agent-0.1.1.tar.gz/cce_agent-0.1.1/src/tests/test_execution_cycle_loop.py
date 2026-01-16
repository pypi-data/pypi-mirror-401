import logging
from datetime import datetime

import pytest

from src.agent import CCEAgent
from src.models import CycleResult


@pytest.mark.asyncio
async def test_execution_graph_runs_multiple_cycles():
    agent = CCEAgent.__new__(CCEAgent)
    agent.logger = logging.getLogger("test_execution_cycle_loop")
    agent.checkpointer = None
    agent.max_execution_cycles = 3
    agent._cycle_spans = {}
    agent._execution_loop_span = None

    calls = {"orient": 0, "execute": 0, "reconcile": 0, "decide": 0}

    async def fake_orient(state, config=None):
        calls["orient"] += 1
        cycle_number = state["cycle_count"] + 1
        return {"orientation": f"Cycle {cycle_number}", "cycle_count": cycle_number}

    async def fake_execute(state, config=None):
        calls["execute"] += 1
        cycle_result = CycleResult(
            cycle_number=state["cycle_count"],
            status="success",
            orientation=state.get("orientation", ""),
            start_time=datetime.now(),
        )
        return {"messages": [], "cycle_results": state["cycle_results"] + [cycle_result]}

    async def fake_reconcile(state):
        calls["reconcile"] += 1
        return {}

    def fake_determine(state):
        calls["decide"] += 1
        status = "running" if state["cycle_count"] < 2 else "completed"
        return {"agent_status": status}

    agent._orient_for_next_cycle = fake_orient
    agent._execute_react_cycle = fake_execute
    agent._reconcile_cycle_results = fake_reconcile
    agent._determine_next_action = fake_determine
    agent.execution_graph = agent._create_execution_graph()

    execution_state = {
        "messages": [],
        "plan": "Test plan",
        "orientation": "",
        "cycle_count": 0,
        "max_cycles": 3,
        "agent_status": "running",
        "cycle_results": [],
        "test_attempts": [],
        "structured_phases": [],
    }

    result = await agent.execution_graph.ainvoke(
        execution_state,
        config={"configurable": {"thread_id": "test-cycle-loop"}, "recursion_limit": 25},
    )

    assert len(result["cycle_results"]) == 2
    assert calls["orient"] == 2
    assert calls["execute"] == 2
    assert calls["reconcile"] == 2
    assert calls["decide"] == 2
    assert result["agent_status"] == "completed"
