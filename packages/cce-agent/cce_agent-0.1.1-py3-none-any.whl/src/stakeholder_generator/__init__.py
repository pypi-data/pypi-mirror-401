"""
LangGraph-Native Multi-Stakeholder Architecture Description Generator

This module implements the production-ready LangGraph-native multi-stakeholder
system for generating comprehensive architecture descriptions per ticket #160.

Features:
- Supervisor pattern with LangGraph StateGraph
- Individual stakeholder subgraphs
- Parallel stakeholder processing
- Quality gates and synthesis
- Centralized prompt management
- Advanced observability integration
"""

from .human_feedback import HumanFeedback
from .quality import QualityGates
from .stakeholder_agents import StakeholderAgent
from .supervisor_graph import SupervisorGraph
from .synthesis import SynthesisEngine

__all__ = ["SupervisorGraph", "StakeholderAgent", "SynthesisEngine", "QualityGates", "HumanFeedback"]
