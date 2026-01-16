"""
Validation Pipeline Package

AIDER-inspired validation system for the CCE agent.
Provides linting and testing integration with rollback capabilities.
"""

from .linting import LinterConfig, LintingManager, LintResult
from .testing import FrameworkTestManager, TestFrameworkConfig, TestResult

__all__ = ["LintingManager", "LintResult", "LinterConfig", "FrameworkTestManager", "TestResult", "TestFrameworkConfig"]
