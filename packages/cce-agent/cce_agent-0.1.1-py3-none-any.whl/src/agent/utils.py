"""Utility helpers for the legacy CCE agent module."""

from __future__ import annotations

from typing import Any, Iterable

from langchain_core.messages import BaseMessage
from langchain_core.messages.utils import trim_messages

from src.agent.state import PlanningState
from src.models import ToolCall


def trim_messages_for_context(
    messages: list[BaseMessage],
    token_counter: Any,
    max_tokens: int = 800000,
) -> list[BaseMessage]:
    """Trim messages to fit within context window using LangChain's trim_messages utility."""
    if not messages:
        return messages

    return trim_messages(
        messages,
        strategy="last",
        token_counter=token_counter,
        max_tokens=max_tokens,
        include_system=True,
        start_on="human",
        end_on=("human", "tool"),
        allow_partial=False,
    )


def merge_analyses(state: PlanningState) -> str:
    """Merge technical and architectural analyses into a final plan."""
    technical = state.get("technical_analysis", "")
    architectural = state.get("architectural_analysis", "")

    return f"""# Collaborative Planning Result

        ## Technical Implementation Analysis
        {technical}

        ## Architectural Strategy Analysis  
        {architectural}

        ## Integrated Plan
        This plan combines both technical implementation details and architectural strategy considerations for a comprehensive approach to the ticket requirements.
        """


def extract_tool_calls_from_messages(messages: Iterable[Any]) -> list[ToolCall]:
    """Extract tool calls from LangChain messages for audit trail."""
    tool_calls: list[ToolCall] = []

    for message in messages:
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_calls.append(
                    ToolCall(
                        tool_name=tool_call.get("name", "unknown"),
                        arguments=tool_call.get("args", {}),
                        result="",
                    )
                )

    return tool_calls
