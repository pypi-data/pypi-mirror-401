"""Wrap-up phase tracking and reminder helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

TEST_TOOL_NAMES = {"run_tests", "test_native"}
LINT_TOOL_NAMES = {"run_linting", "lint_native"}

WRAP_UP_REMINDER_TEMPLATE = """WRAP-UP REMINDER: You've been in wrap-up for {wrap_up_steps} steps.

Missing items:
{missing_items}

Please complete these before signaling cycle complete.
"""


@dataclass
class WrapUpPhaseState:
    """State tracked during wrap-up phase."""

    started_at_step: int
    tests_run: bool = False
    tests_passed: bool | None = None
    linting_run: bool = False
    linting_passed: bool | None = None
    cycle_report_prepared: bool = False

    def is_complete(self) -> bool:
        """Check if wrap-up requirements are met."""
        return self.tests_run and self.linting_run


def _infer_tool_success(tool_call: Any) -> bool | None:
    success = getattr(tool_call, "success", None)
    if isinstance(success, bool):
        return success

    error = getattr(tool_call, "error", None)
    result = getattr(tool_call, "result", None)
    if error:
        return False
    if result:
        result = str(result).lower()
        if "fail" in result or "error" in result:
            return False
        if "pass" in result or "success" in result:
            return True
    return None


def _get_activity_name(tool_call: Any) -> str | None:
    name = getattr(tool_call, "tool_name", None) or getattr(tool_call, "command_name", None)
    if not name and isinstance(tool_call, dict):
        name = tool_call.get("tool_name") or tool_call.get("command_name") or tool_call.get("name")
    return name


def track_wrap_up_activity(tool_calls: Iterable[Any], wrap_up_state: WrapUpPhaseState) -> WrapUpPhaseState:
    """Update wrap-up state based on tool calls."""
    for tool_call in tool_calls:
        name = _get_activity_name(tool_call)
        if not name:
            continue
        if name in TEST_TOOL_NAMES:
            wrap_up_state.tests_run = True
            inferred = _infer_tool_success(tool_call)
            if inferred is not None:
                wrap_up_state.tests_passed = inferred
        elif name in LINT_TOOL_NAMES:
            wrap_up_state.linting_run = True
            inferred = _infer_tool_success(tool_call)
            if inferred is not None:
                wrap_up_state.linting_passed = inferred

    return wrap_up_state


def check_wrap_up_progress(wrap_up_state: WrapUpPhaseState, wrap_up_steps: int) -> str | None:
    """Generate reminder if wrap-up is taking too long."""
    if wrap_up_steps < 5:
        return None

    missing = []
    if not wrap_up_state.tests_run:
        missing.append("- Run tests on modified files")
    if not wrap_up_state.linting_run:
        missing.append("- Run linting on modified files")

    if not missing:
        return None

    return WRAP_UP_REMINDER_TEMPLATE.format(
        wrap_up_steps=wrap_up_steps,
        missing_items="\n".join(missing),
    )


def can_end_cycle(wrap_up_state: WrapUpPhaseState) -> tuple[bool, list[str]]:
    """Check if cycle can end based on wrap-up requirements."""
    issues: list[str] = []

    if not wrap_up_state.tests_run:
        issues.append("Tests not run during wrap-up")
    if wrap_up_state.tests_run and wrap_up_state.tests_passed is False:
        issues.append("Tests failed - consider fixing before cycle end")
    if not wrap_up_state.linting_run:
        issues.append("Linting not run during wrap-up")

    can_end = wrap_up_state.tests_run and wrap_up_state.linting_run
    return can_end, issues
