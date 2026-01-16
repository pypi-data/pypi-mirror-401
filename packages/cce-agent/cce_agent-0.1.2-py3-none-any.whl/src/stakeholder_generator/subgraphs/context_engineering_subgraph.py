"""
Context Engineering Stakeholder Subgraph

Specialized LangGraph subgraph for context management expertise.
Handles memory systems, context engineering, and advanced context
management requirements.
"""

import logging
from typing import Any

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

from ..stakeholder_agents import StakeholderType
from .base_subgraph import create_stakeholder_subgraph


def create_context_engineering_subgraph(llm: ChatOpenAI | None = None, checkpointer: Any | None = None) -> StateGraph:
    """
    Create the Context Engineering stakeholder subgraph.

    This subgraph specializes in:
    - Multi-layered memory systems (working/episodic/procedural)
    - Context window management and optimization
    - Semantic tagging and targeted context injection
    - Context engineering patterns and best practices
    - Memory persistence and retrieval strategies

    Args:
        llm: Optional LLM instance (defaults to gpt-4o)
        checkpointer: Optional checkpointer for persistence

    Returns:
        Compiled LangGraph subgraph for context engineering expertise
    """
    logger = logging.getLogger("context_engineering_subgraph")
    logger.info("Creating Context Engineering stakeholder subgraph")

    # Use the base subgraph factory with CONTEXT_ENGINEERING type
    subgraph = create_stakeholder_subgraph(
        stakeholder_type=StakeholderType.CONTEXT_ENGINEERING, llm=llm, checkpointer=checkpointer
    )

    logger.info("Context Engineering subgraph created successfully")
    return subgraph
