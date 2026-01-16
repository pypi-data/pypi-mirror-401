"""Wrap-up prompt template and helpers for soft limit handling."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterable

from langchain_core.messages import SystemMessage

WRAP_UP_PROMPT_TEMPLATE = """SOFT LIMIT REACHED ({step_count} steps, limit {soft_limit}).

What to do now:
1. Finish current work to a natural stopping point.
2. Run tests on modified files.
3. Run linting on modified files.
4. Fix any issues found by tests or linting.
5. Polish and clean up temporary code.
6. Prepare a cycle report (summary, work remaining, next focus).

Previous cycle stats:
{previous_cycle_stats}

Examples of wrap-up activities:
- Run pytest on modified files (1-3 commands).
- Fix 1-2 minor issues found by tests.
- Run linting and address style issues (1-2 commands).
- Add docstrings or comments for new functions.
- Remove debug print statements.
- Update inline comments.

When ready:
Provide a brief summary, note any work remaining, suggest the next focus,
then call:

signal_cycle_complete(
    summary="What you accomplished this cycle",
    work_remaining="What's left to do (if anything)",
    next_focus_suggestion="What to focus on next cycle"
)
"""


def get_wrap_up_prompt_template() -> str:
    """Return the wrap-up prompt template, optionally loading from disk."""
    override_path = os.getenv("CCE_WRAP_UP_PROMPT_PATH")
    if override_path:
        path = Path(override_path)
        if path.exists():
            return path.read_text(encoding="utf-8")
    return WRAP_UP_PROMPT_TEMPLATE


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
) -> str:
    """Format the wrap-up prompt with current context."""
    template = get_wrap_up_prompt_template()
    previous_cycle_stats = _format_cycle_stats(previous_cycles)
    return template.format(
        step_count=step_count,
        soft_limit=soft_limit,
        previous_cycle_stats=previous_cycle_stats,
    )


def build_wrap_up_message(
    step_count: int,
    soft_limit: int,
    previous_cycles: Iterable[Any] | None = None,
) -> SystemMessage:
    """Build a system message containing the wrap-up prompt."""
    prompt = format_wrap_up_prompt(step_count, soft_limit, previous_cycles)
    return SystemMessage(content=prompt)
