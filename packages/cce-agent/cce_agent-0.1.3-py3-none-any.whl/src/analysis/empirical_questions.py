"""Empirical question analysis helpers for run summaries."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any, Iterable


@dataclass
class RunSummary:
    """Aggregate metrics from a single run."""

    run_id: str
    avg_steps_per_cycle: float | None
    avg_wrap_up_steps: float | None
    cycles_per_run: int


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return float(mean(values))


def summarize_runs(run_logs: Iterable[dict[str, Any]]) -> list[RunSummary]:
    """Summarize run logs into lightweight run summaries."""
    summaries: list[RunSummary] = []

    for run in run_logs:
        cycles = run.get("execution_cycles", []) or []
        step_counts = [
            cycle.get("step_count")
            for cycle in cycles
            if isinstance(cycle, dict) and cycle.get("step_count") is not None
        ]
        wrap_up_steps = [
            cycle.get("steps_in_wrap_up_phase")
            for cycle in cycles
            if isinstance(cycle, dict) and cycle.get("steps_in_wrap_up_phase") is not None
        ]

        avg_steps = _mean([float(value) for value in step_counts]) if step_counts else None
        avg_wrap_up = _mean([float(value) for value in wrap_up_steps]) if wrap_up_steps else None

        summaries.append(
            RunSummary(
                run_id=str(run.get("run_id", "")),
                avg_steps_per_cycle=avg_steps,
                avg_wrap_up_steps=avg_wrap_up,
                cycles_per_run=len(cycles),
            )
        )

    return summaries


def check_empirical_questions(summaries: list[RunSummary]) -> dict[str, Any]:
    """Check data against empirical questions and return a summary report."""
    avg_steps = _mean([s.avg_steps_per_cycle for s in summaries if s.avg_steps_per_cycle is not None])
    avg_wrap_up = _mean([s.avg_wrap_up_steps for s in summaries if s.avg_wrap_up_steps is not None])

    report: dict[str, Any] = {
        "Q1_soft_limit": {
            "data_points": len(summaries),
            "avg_steps_per_cycle": avg_steps,
            "recommendation": "Collect more runs" if avg_steps is None else "Review step distribution",
        },
        "Q2_wrap_up_duration": {
            "data_points": len(summaries),
            "avg_wrap_up_steps": avg_wrap_up,
            "recommendation": "Collect more runs" if avg_wrap_up is None else "Review wrap-up duration",
        },
        "Q3_orientation_change": {
            "data_points": len(summaries),
            "status": "needs_data",
        },
        "Q4_cycle_reflection_value": {
            "data_points": len(summaries),
            "status": "needs_data",
        },
        "Q5_test_failure_rate": {
            "data_points": len(summaries),
            "status": "needs_data",
        },
        "Q6_test_retry_count": {
            "data_points": len(summaries),
            "status": "needs_data",
        },
        "Q7_commit_rhythm": {
            "data_points": len(summaries),
            "status": "needs_data",
        },
        "Q8_cycles_per_ticket": {
            "data_points": len(summaries),
            "avg_cycles_per_run": _mean([float(s.cycles_per_run) for s in summaries]),
        },
    }

    return report
