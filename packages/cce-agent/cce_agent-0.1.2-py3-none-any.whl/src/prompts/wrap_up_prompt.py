"""Wrap-up prompt template and helpers for soft limit handling."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterable

from langchain_core.messages import SystemMessage

from src.prompts.manager import PromptManager


def get_wrap_up_prompt_template() -> str:
    """Return the wrap-up prompt template, optionally loading from disk."""
    override_path = os.getenv("CCE_WRAP_UP_PROMPT_PATH")
    if override_path:
        path = Path(override_path)
        if path.exists():
            return path.read_text(encoding="utf-8")
    return PromptManager().get_cycling_prompt("wrap_up")


def _get_cycle_value(cycle: Any, key: str, default: Any = None) -> Any:
    if isinstance(cycle, dict):
        return cycle.get(key, default)
    return getattr(cycle, key, default)


def _format_cycle_stats(previous_cycles: Iterable[Any] | None) -> str:
    if not previous_cycles:
        return "- No previous cycles in this run"

    lines: list[str] = []
    for cycle in list(previous_cycles)[-3:]:
        cycle_number = _get_cycle_value(cycle, "cycle_number", "?")
        step_count = _get_cycle_value(cycle, "step_count", "?")
        main_steps = _get_cycle_value(cycle, "steps_in_main_phase")
        wrap_steps = _get_cycle_value(cycle, "steps_in_wrap_up_phase")

        details = ""
        if main_steps is not None or wrap_steps is not None:
            main_display = main_steps if main_steps is not None else "?"
            wrap_display = wrap_steps if wrap_steps is not None else "?"
            details = f" (main: {main_display}, wrap-up: {wrap_display})"

        lines.append(f"- Cycle {cycle_number}: {step_count} steps{details}")

    return "\n".join(lines)


def format_wrap_up_prompt(
    step_count: int,
    soft_limit: int,
    previous_cycles: Iterable[Any] | None = None,
    *,
    cycle_number: int | None = None,
    max_cycles: int | None = None,
    work_completed: str | None = None,
    artifacts: str | None = None,
    tests_run: str | None = None,
    issues_found: str | None = None,
    work_remaining: str | None = None,
    next_focus_suggestion: str | None = None,
    status: str | None = None,
) -> str:
    """Format the wrap-up prompt with current context."""
    template = get_wrap_up_prompt_template()
    previous_cycle_stats = _format_cycle_stats(previous_cycles)
    derived_cycle_number = cycle_number
    if derived_cycle_number is None:
        derived_cycle_number = len(list(previous_cycles)) + 1 if previous_cycles else 1
    variables = {
        "cycle_number": derived_cycle_number,
        "max_cycles": max_cycles or "unknown",
        "work_completed": work_completed or "Summarize the work completed in this cycle.",
        "artifacts": artifacts or "List files changed or artifacts created.",
        "tests_run": tests_run or "Note tests run and results (or state Not run).",
        "issues_found": issues_found or "List any issues or risks discovered (or None).",
        "work_remaining": work_remaining or "List remaining work in priority order.",
        "next_focus_suggestion": next_focus_suggestion or "Recommend the next focus for the upcoming cycle.",
        "status": status or f"Soft limit reached after {step_count} steps (limit {soft_limit}).",
    }
    if previous_cycle_stats:
        variables["work_completed"] = f"{variables['work_completed']}\n\nPrevious cycle stats:\n{previous_cycle_stats}"
    return PromptManager().substitute_variables(template, variables)


def build_wrap_up_message(
    step_count: int,
    soft_limit: int,
    previous_cycles: Iterable[Any] | None = None,
    *,
    cycle_number: int | None = None,
    max_cycles: int | None = None,
    work_completed: str | None = None,
    artifacts: str | None = None,
    tests_run: str | None = None,
    issues_found: str | None = None,
    work_remaining: str | None = None,
    next_focus_suggestion: str | None = None,
    status: str | None = None,
) -> SystemMessage:
    """Build a system message containing the wrap-up prompt."""
    prompt = format_wrap_up_prompt(
        step_count,
        soft_limit,
        previous_cycles,
        cycle_number=cycle_number,
        max_cycles=max_cycles,
        work_completed=work_completed,
        artifacts=artifacts,
        tests_run=tests_run,
        issues_found=issues_found,
        work_remaining=work_remaining,
        next_focus_suggestion=next_focus_suggestion,
        status=status,
    )
    return SystemMessage(content=prompt)
