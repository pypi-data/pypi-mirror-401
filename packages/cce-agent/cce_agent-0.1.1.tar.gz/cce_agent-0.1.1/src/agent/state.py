"""
CCE Agent state definitions.

These TypedDicts are extracted from the legacy src/agent.py module as part of
ticket #125 and are wired into src/agent.py for planning/execution state.
"""

from typing import Annotated, Any

from langchain_core.messages import AnyMessage, BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import NotRequired, TypedDict

from src.models import CycleResult


class PlanningState(TypedDict):
    """State for dual-agent collaborative planning using native LangGraph patterns."""

    messages: Annotated[list[AnyMessage], add_messages]
    shared_plan: str
    technical_analysis: str
    architectural_analysis: str
    consensus_reached: bool
    iteration_count: int
    max_iterations: int


class ExecutionState(TypedDict):
    """State for the execution graph that handles iterative work cycles."""

    messages: Annotated[list[BaseMessage], add_messages]
    plan: str
    orientation: str
    cycle_count: int
    max_cycles: int
    agent_status: str
    cycle_results: list[CycleResult]
    soft_limit: NotRequired[int]
    soft_limit_reached: NotRequired[bool]
    step_count: NotRequired[int]
    wrap_up_started_at_step: NotRequired[int | None]
    test_results: NotRequired[Any]
    evaluation_result: NotRequired[Any]
    test_attempts: NotRequired[list[Any]]
    structured_phases: NotRequired[list[dict[str, Any]]]


__all__ = ["PlanningState", "ExecutionState"]
