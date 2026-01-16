"""
Graph integration middleware for CCE deep agents.

Provides graph execution as a middleware-registered tool.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.graphs.utils import get_graph_orchestration_manager

logger = logging.getLogger(__name__)


class GraphExecutionInput(BaseModel):
    """Input schema for execute_graph tool."""

    graph_name: str = Field(..., description="Registered graph name to execute")
    instruction: str = Field(..., description="Instruction for the graph")
    context: dict[str, Any] | None = Field(default=None, description="Optional context payload")


@tool(
    args_schema=GraphExecutionInput,
    description="Execute a registered graph with an instruction and optional context",
    infer_schema=False,
    parse_docstring=False,
)
async def execute_graph(
    graph_name: str,
    instruction: str,
    context: dict[str, Any] | None = None,
) -> str:
    """Execute a graph via the unified orchestration layer."""
    try:
        orchestration_manager = get_graph_orchestration_manager()
        result = await orchestration_manager.execute_graph(graph_name, instruction, context)
        return json.dumps(result, default=str)
    except Exception as exc:
        logger.error("Graph execution failed: %s", exc)
        return json.dumps(
            {"success": False, "error": str(exc), "graph_name": graph_name},
            default=str,
        )


GRAPH_INTEGRATION_TOOLS = [execute_graph]


class GraphIntegrationMiddleware(AgentMiddleware):
    """Expose graph integration tools through middleware."""

    def __init__(self) -> None:
        super().__init__()
        self.tools = GRAPH_INTEGRATION_TOOLS
