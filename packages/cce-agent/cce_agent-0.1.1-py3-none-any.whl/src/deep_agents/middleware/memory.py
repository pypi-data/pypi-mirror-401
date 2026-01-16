"""
Memory middleware for CCE deep agents.

Runs the existing memory management hook as middleware so memory synchronization
does not depend on legacy post-model hooks.
"""

from __future__ import annotations

import copy
import logging
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES

from ..memory_hooks import create_memory_management_hook
from ..state import CCEDeepAgentState

logger = logging.getLogger(__name__)


def _build_message_updates(before_messages: list[Any], after_messages: list[Any]) -> list[Any]:
    """Build a message update list compatible with add_messages semantics."""
    if before_messages is None:
        before_messages = []
    if after_messages is None:
        after_messages = []

    before_ids = [getattr(message, "id", None) for message in before_messages]
    after_ids = [getattr(message, "id", None) for message in after_messages]
    before_ids_filtered = [message_id for message_id in before_ids if message_id is not None]
    after_ids_filtered = [message_id for message_id in after_ids if message_id is not None]

    removed_ids = any(message_id is not None and message_id not in after_ids for message_id in before_ids)
    reordered = before_ids_filtered and after_ids_filtered[: len(before_ids_filtered)] != before_ids_filtered
    if removed_ids or reordered or len(after_messages) < len(before_messages):
        if not after_messages:
            return [RemoveMessage(id=REMOVE_ALL_MESSAGES)]
        return [RemoveMessage(id=REMOVE_ALL_MESSAGES), *after_messages]

    before_by_id = {}
    for message in before_messages:
        message_id = getattr(message, "id", None)
        if message_id is not None:
            before_by_id[message_id] = message

    updates: list[Any] = []
    for message in after_messages:
        message_id = getattr(message, "id", None)
        if message_id is None:
            updates.append(message)
            continue
        previous = before_by_id.get(message_id)
        if previous is None or message != previous:
            updates.append(message)

    return updates


def _build_state_updates(before_state: dict[str, Any], after_state: dict[str, Any]) -> dict[str, Any] | None:
    """Build state updates by diffing before/after states."""
    updates: dict[str, Any] = {}
    before_messages = before_state.get("messages", [])
    after_messages = after_state.get("messages", [])
    message_updates = _build_message_updates(before_messages, after_messages)
    if message_updates:
        updates["messages"] = message_updates

    for key, value in after_state.items():
        if key == "messages":
            continue
        if key not in before_state or before_state[key] != value:
            updates[key] = value

    return updates or None


class CCEMemoryMiddleware(AgentMiddleware):
    """Run CCE memory management via langchain middleware."""

    state_schema = CCEDeepAgentState

    def __init__(self, hook: callable | None = None) -> None:
        super().__init__()
        self._hook = hook or create_memory_management_hook()
        self.tools = []

    def after_model(self, state: dict[str, Any], runtime) -> dict[str, Any] | None:  # type: ignore[override]
        if self._hook is None:
            return None
        try:
            state_snapshot = copy.deepcopy(state)
            updated_state = self._hook(state_snapshot)
            if not isinstance(updated_state, dict):
                return None
            return _build_state_updates(state, updated_state)
        except Exception as exc:
            logger.error("❌ [MEMORY MIDDLEWARE] Memory hook failed: %s", exc)
            return None

    async def aafter_model(self, state: dict[str, Any], runtime) -> dict[str, Any] | None:  # type: ignore[override]
        return self.after_model(state, runtime)
