"""
Developer Experience Stakeholder Subgraph

Specialized LangGraph subgraph for developer experience expertise.
Handles usability, debuggability, and developer workflow concerns.
"""

import logging
from typing import Any

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

from ..stakeholder_agents import StakeholderType
from .base_subgraph import create_stakeholder_subgraph


def create_developer_experience_subgraph(llm: ChatOpenAI | None = None, checkpointer: Any | None = None) -> StateGraph:
    """
    Create the Developer Experience stakeholder subgraph.

    This subgraph specializes in:
    - Developer workflow optimization
    - API design and usability
    - Documentation and developer onboarding
    - Debugging and troubleshooting support
    - IDE integration and tooling
    - Developer productivity patterns

    Args:
        llm: Optional LLM instance (defaults to gpt-4o)
        checkpointer: Optional checkpointer for persistence

    Returns:
        Compiled LangGraph subgraph for developer experience expertise
    """
    logger = logging.getLogger("developer_experience_subgraph")
    logger.info("Creating Developer Experience stakeholder subgraph")

    # Use the base subgraph factory with DEVELOPER_EXPERIENCE type
    subgraph = create_stakeholder_subgraph(
        stakeholder_type=StakeholderType.DEVELOPER_EXPERIENCE, llm=llm, checkpointer=checkpointer
    )

    logger.info("Developer Experience subgraph created successfully")
    return subgraph
