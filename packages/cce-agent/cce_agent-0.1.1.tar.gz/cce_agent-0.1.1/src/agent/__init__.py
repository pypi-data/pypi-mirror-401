"""
CCE Agent package scaffolding.

This package is additive and preserves legacy imports by loading src/agent.py
as a separate module and re-exporting CCEAgent.
"""

from __future__ import annotations

import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from langgraph.prebuilt import create_react_agent

from .core import CCEAgentCore
from .state import ExecutionState, PlanningState

_LEGACY_MODULE_NAME = "src.agent_legacy"

if _LEGACY_MODULE_NAME in sys.modules:
    _legacy_module = sys.modules[_LEGACY_MODULE_NAME]
else:
    _legacy_path = Path(__file__).resolve().parent.parent / "agent.py"
    _spec = spec_from_file_location(_LEGACY_MODULE_NAME, _legacy_path)
    if _spec is None or _spec.loader is None:
        raise ImportError("Unable to load legacy agent module from src/agent.py")
    _legacy_module = module_from_spec(_spec)
    sys.modules[_LEGACY_MODULE_NAME] = _legacy_module
    _spec.loader.exec_module(_legacy_module)

CCEAgent = _legacy_module.CCEAgent

__all__ = [
    "CCEAgent",
    "CCEAgentCore",
    "PlanningState",
    "ExecutionState",
    "create_react_agent",
]
