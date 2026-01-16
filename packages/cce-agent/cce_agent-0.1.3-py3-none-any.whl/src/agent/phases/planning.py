"""Planning phase helpers."""

from __future__ import annotations

from src.agent.state import PlanningState
from src.agent.utils import merge_analyses as _merge_analyses


def merge_analyses(state: PlanningState) -> str:
    """Merge technical and architectural analyses into a final plan."""
    return _merge_analyses(state)
