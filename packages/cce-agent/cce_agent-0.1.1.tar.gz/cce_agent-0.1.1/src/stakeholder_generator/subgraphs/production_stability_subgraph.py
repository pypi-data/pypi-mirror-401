"""
Production Stability Stakeholder Subgraph

Specialized LangGraph subgraph for production stability expertise.
Handles reliability, monitoring, and production readiness concerns.
"""

import logging
from typing import Any

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

from ..stakeholder_agents import StakeholderType
from .base_subgraph import create_stakeholder_subgraph


def create_production_stability_subgraph(llm: ChatOpenAI | None = None, checkpointer: Any | None = None) -> StateGraph:
    """
    Create the Production Stability stakeholder subgraph.

    This subgraph specializes in:
    - System reliability and fault tolerance
    - Monitoring and observability patterns
    - Performance and scalability concerns
    - Production deployment strategies
    - Error handling and recovery patterns
    - Quality gates and validation

    Args:
        llm: Optional LLM instance (defaults to gpt-4o)
        checkpointer: Optional checkpointer for persistence

    Returns:
        Compiled LangGraph subgraph for production stability expertise
    """
    logger = logging.getLogger("production_stability_subgraph")
    logger.info("Creating Production Stability stakeholder subgraph")

    # Use the base subgraph factory with PRODUCTION_STABILITY type
    subgraph = create_stakeholder_subgraph(
        stakeholder_type=StakeholderType.PRODUCTION_STABILITY, llm=llm, checkpointer=checkpointer
    )

    logger.info("Production Stability subgraph created successfully")
    return subgraph
