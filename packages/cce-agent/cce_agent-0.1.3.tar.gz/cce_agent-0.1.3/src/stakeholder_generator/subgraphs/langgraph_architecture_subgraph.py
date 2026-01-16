"""
LangGraph Architecture Stakeholder Subgraph

Specialized LangGraph subgraph for LangGraph ecosystem expertise.
Handles LangGraph/LangChain patterns, state management, and
orchestration requirements.
"""

import logging
from typing import Any

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

from ..stakeholder_agents import StakeholderType
from .base_subgraph import create_stakeholder_subgraph


def create_langgraph_architecture_subgraph(
    llm: ChatOpenAI | None = None, checkpointer: Any | None = None
) -> StateGraph:
    """
    Create the LangGraph Architecture stakeholder subgraph.

    This subgraph specializes in:
    - LangGraph StateGraph patterns and best practices
    - LangChain tool integration
    - Multi-agent orchestration patterns
    - State management and checkpointing
    - Message passing and handoffs
    - Observability with LangSmith

    Args:
        llm: Optional LLM instance (defaults to gpt-4o)
        checkpointer: Optional checkpointer for persistence

    Returns:
        Compiled LangGraph subgraph for LangGraph architecture expertise
    """
    logger = logging.getLogger("langgraph_architecture_subgraph")
    logger.info("Creating LangGraph Architecture stakeholder subgraph")

    # Use the base subgraph factory with LANGGRAPH_ARCHITECTURE type
    subgraph = create_stakeholder_subgraph(
        stakeholder_type=StakeholderType.LANGGRAPH_ARCHITECTURE, llm=llm, checkpointer=checkpointer
    )

    logger.info("LangGraph Architecture subgraph created successfully")
    return subgraph
