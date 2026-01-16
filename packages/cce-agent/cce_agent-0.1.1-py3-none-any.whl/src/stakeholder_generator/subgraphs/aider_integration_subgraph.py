"""
AIDER Integration Stakeholder Subgraph

Specialized LangGraph subgraph for AIDER domain expertise.
Handles all AIDER tooling requirements, integration patterns, and
code modification capabilities.
"""

import logging
from typing import Any

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

from ..stakeholder_agents import StakeholderType
from .base_subgraph import create_stakeholder_subgraph


def create_aider_integration_subgraph(llm: ChatOpenAI | None = None, checkpointer: Any | None = None) -> StateGraph:
    """
    Create the AIDER Integration stakeholder subgraph.

    This subgraph specializes in:
    - AIDER tool integration patterns
    - RepoMap and TreeSitter capabilities
    - Multi-strategy editing (UnifiedDiff, EditBlock, WholeFile)
    - Code modification and validation workflows
    - GitOps integration

    Args:
        llm: Optional LLM instance (defaults to gpt-4o)
        checkpointer: Optional checkpointer for persistence

    Returns:
        Compiled LangGraph subgraph for AIDER integration expertise
    """
    logger = logging.getLogger("aider_integration_subgraph")
    logger.info("Creating AIDER Integration stakeholder subgraph")

    # Use the base subgraph factory with AIDER_INTEGRATION type
    subgraph = create_stakeholder_subgraph(
        stakeholder_type=StakeholderType.AIDER_INTEGRATION, llm=llm, checkpointer=checkpointer
    )

    logger.info("AIDER Integration subgraph created successfully")
    return subgraph
