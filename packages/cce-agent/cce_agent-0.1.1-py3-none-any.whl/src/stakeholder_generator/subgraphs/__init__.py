"""
Stakeholder Subgraphs - LangGraph Multi-Agent Implementation

This module implements true LangGraph subgraphs for each stakeholder domain,
replacing the previous single-graph-with-nodes approach with proper
multi-agent subgraph architecture as specified in ticket #160.

Each stakeholder is now a compiled LangGraph subgraph with its own StateGraph,
enabling proper parallel processing and state management.
"""

from .aider_integration_subgraph import create_aider_integration_subgraph
from .base_subgraph import StakeholderSubgraphState, create_stakeholder_handoff_command, create_stakeholder_subgraph
from .context_engineering_subgraph import create_context_engineering_subgraph
from .developer_experience_subgraph import create_developer_experience_subgraph
from .langgraph_architecture_subgraph import create_langgraph_architecture_subgraph
from .production_stability_subgraph import create_production_stability_subgraph

__all__ = [
    "create_stakeholder_subgraph",
    "StakeholderSubgraphState",
    "create_stakeholder_handoff_command",
    "create_aider_integration_subgraph",
    "create_langgraph_architecture_subgraph",
    "create_context_engineering_subgraph",
    "create_production_stability_subgraph",
    "create_developer_experience_subgraph",
]
