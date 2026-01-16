import logging
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath("."))

from langchain_core.messages import AIMessage

from src.agent import CCEAgent
from src.deep_agents.cycle_tools import CYCLE_TOOLS, signal_cycle_complete
from src.models import CycleResult


def test_signal_tool_exists():
    assert signal_cycle_complete in CYCLE_TOOLS
    assert signal_cycle_complete.name == "signal_cycle_complete"


def test_signal_detection_from_tool_call():
    agent = CCEAgent.__new__(CCEAgent)

    message = AIMessage(
        content="done",
        tool_calls=[
            {
                "id": "signal-1",
                "name": "signal_cycle_complete",
                "args": {
                    "summary": "Wrapped up",
                    "work_remaining": "None",
                    "next_focus_suggestion": "Start next task",
                },
            }
        ],
    )

    signal = agent._detect_cycle_complete_signal([message])

    assert signal is not None
    assert signal.summary == "Wrapped up"
    assert signal.work_remaining == "None"
    assert signal.next_focus_suggestion == "Start next task"
    assert signal.method == "tool_call"


def test_signal_ends_cycle():
    agent = CCEAgent.__new__(CCEAgent)
    agent.logger = logging.getLogger("cycle_signal_test")
    agent.llm = type("Dummy", (), {"invoke": lambda *_args, **_kwargs: None})()

    cycle_result = CycleResult(
        cycle_number=1,
        status="success",
        orientation="",
        start_time=datetime.now(),
        ready_to_end=True,
    )

    state = {
        "messages": [],
        "plan": "",
        "cycle_count": 0,
        "cycle_results": [cycle_result],
        "agent_status": "running",
    }

    result = agent._determine_next_action(state)

    assert result["agent_status"] == "completed"
