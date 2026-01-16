import logging
import os
import sys

sys.path.insert(0, os.path.abspath("."))

import pytest
from langchain_core.messages import AIMessage, SystemMessage

from src.agent import CCEAgent
from src.models import ToolCall
from src.wrap_up_protocol import WrapUpPhaseState, can_end_cycle, track_wrap_up_activity


def test_wrap_up_tracks_activities():
    state = WrapUpPhaseState(started_at_step=0)
    tool_calls = [
        ToolCall(tool_name="run_tests", arguments={}, result="PASS"),
        ToolCall(tool_name="run_linting", arguments={}, result="success"),
    ]

    updated = track_wrap_up_activity(tool_calls, state)

    assert updated.tests_run is True
    assert updated.tests_passed is True
    assert updated.linting_run is True
    assert updated.linting_passed is True


def test_cycle_end_requires_tests():
    state = WrapUpPhaseState(started_at_step=0)

    can_end, issues = can_end_cycle(state)

    assert can_end is False
    assert "Tests not run during wrap-up" in issues


@pytest.mark.asyncio
async def test_wrap_up_reminder_injected(monkeypatch):
    class DummyReactAgent:
        def __init__(self, messages):
            self._messages = messages

        async def ainvoke(self, payload, config):
            return {"messages": list(self._messages)}

    dummy_message = AIMessage(
        content="Done",
        tool_calls=[{"name": "grep_native", "args": {}, "id": f"call-{index}"} for index in range(6)],
    )

    def fake_create_react_agent(llm, tools):
        return DummyReactAgent([dummy_message])

    import src.agent as agent_module

    monkeypatch.setattr(agent_module, "create_react_agent", fake_create_react_agent)

    class DummyLLM:
        def get_usage_records(self):
            return []

    agent = CCEAgent.__new__(CCEAgent)
    agent.logger = logging.getLogger("wrap_up_test")
    agent.llm = DummyLLM()
    agent.tools = []
    agent.soft_limit = 20
    agent._get_contextual_messages = lambda messages, max_tokens: messages
    agent._extract_tool_calls_from_messages = CCEAgent._extract_tool_calls_from_messages.__get__(agent, CCEAgent)
    agent._promote_cycle_to_episodic_memory = lambda *args, **kwargs: None
    agent._record_successful_pattern = lambda *args, **kwargs: None

    state = {
        "messages": [],
        "plan": "plan",
        "orientation": "focus",
        "cycle_count": 1,
        "cycle_results": [],
        "soft_limit_reached": True,
        "soft_limit": 20,
        "wrap_up_started_at_step": 0,
        "step_count": 6,
    }

    result = await agent._execute_react_cycle(state)

    assert any(
        isinstance(message, SystemMessage) and "WRAP-UP REMINDER" in message.content for message in result["messages"]
    )
