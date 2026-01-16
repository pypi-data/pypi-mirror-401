"""
CCE Commands Module

This module provides programmatic access to CCE (Constitutional Context Engineering) commands
that are typically executed as cursor commands. These commands orchestrate complex workflows
for research, planning, implementation, and evaluation.
"""

from .address_evaluation import address_evaluation
from .commit_and_push import commit_and_push
from .create_plan import create_plan
from .discover_target_files import discover_target_files  # NEW: File discovery command
from .evaluate_implementation import evaluate_implementation
from .implement_plan import implement_plan
from .research_codebase import research_codebase
from .run_tests import run_tests
from .update_plan import update_plan

__all__ = [
    "research_codebase",
    "create_plan",
    "update_plan",
    "implement_plan",
    "evaluate_implementation",
    "address_evaluation",
    "run_tests",
    "commit_and_push",
    "discover_target_files",  # NEW: File discovery command
]
