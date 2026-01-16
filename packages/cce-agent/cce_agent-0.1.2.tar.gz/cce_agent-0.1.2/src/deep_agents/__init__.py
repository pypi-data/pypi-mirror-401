"""
Deep Agents integration for CCE Agent.

This module provides the deep agents integration layer for the CCE (Constitutional Context Engineering) Agent,
enabling LLM-based code editing capabilities and enhanced sub-agent coordination.
"""

from .state import CCEDeepAgentState
from .subagents import context_engineering_agent

try:
    from .cce_deep_agent import createCCEDeepAgent
except Exception:
    createCCEDeepAgent = None

__all__ = ["CCEDeepAgentState", "context_engineering_agent", "createCCEDeepAgent"]
