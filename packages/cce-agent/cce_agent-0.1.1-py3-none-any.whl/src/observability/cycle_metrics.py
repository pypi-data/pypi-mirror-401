"""Cycle-level metrics collection for execution runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean
from typing import Any

from src.models import CycleResult


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return float(mean(values))


@dataclass
class CycleMetrics:
    """Collected metrics for a single execution cycle."""

    cycle_number: int
    status: str
    orientation: str
    start_time: datetime | None
    end_time: datetime | None
    duration_seconds: float | None
    message_count: int
    tool_call_count: int
    step_count: int | None
    soft_limit: int | None
    soft_limit_reached: bool | None
    steps_in_main_phase: int | None
    steps_in_wrap_up_phase: int | None
    tests_run: int
    tests_passed: int
    tests_failed: int
    linting_passed: bool | None
    wrap_up_issues: list[str] = field(default_factory=list)
    commit_sha: str | None = None
    commit_message: str | None = None
    prompt_tokens: int = 0
    completion_tokens: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle_number": self.cycle_number,
            "status": self.status,
            "orientation": self.orientation,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "message_count": self.message_count,
            "tool_call_count": self.tool_call_count,
            "step_count": self.step_count,
            "soft_limit": self.soft_limit,
            "soft_limit_reached": self.soft_limit_reached,
            "steps_in_main_phase": self.steps_in_main_phase,
            "steps_in_wrap_up_phase": self.steps_in_wrap_up_phase,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "tests_failed": self.tests_failed,
            "linting_passed": self.linting_passed,
            "wrap_up_issues": self.wrap_up_issues,
            "commit_sha": self.commit_sha,
            "commit_message": self.commit_message,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.prompt_tokens + self.completion_tokens,
        }


class CycleMetricsCollector:
    """Accumulate per-cycle metrics for the current execution run."""

    def __init__(self) -> None:
        self._cycles: list[CycleMetrics] = []
        self._cycle_starts: dict[int, datetime] = {}
        self._cycle_orientations: dict[int, str] = {}

    def reset(self) -> None:
        """Clear collected metrics for a new run."""
        self._cycles.clear()
        self._cycle_starts.clear()
        self._cycle_orientations.clear()

    def start_cycle(self, cycle_number: int, orientation: str | None = None, start_time: datetime | None = None) -> None:
        """Record the start timestamp for a cycle."""
        self._cycle_starts[cycle_number] = start_time or datetime.now()
        if orientation:
            self._cycle_orientations[cycle_number] = orientation

    def record_cycle(self, cycle_result: CycleResult) -> CycleMetrics:
        """Record metrics from a completed cycle."""
        cycle_number = cycle_result.cycle_number
        start_time = self._cycle_starts.pop(cycle_number, None) or cycle_result.start_time
        end_time = cycle_result.end_time or datetime.now()
        orientation = cycle_result.orientation or self._cycle_orientations.pop(cycle_number, "")
        duration_seconds = cycle_result.duration_seconds
        if duration_seconds is None and start_time:
            duration_seconds = (end_time - start_time).total_seconds()

        tool_call_count = len(cycle_result.tool_calls) if cycle_result.tool_calls else 0
        step_count = cycle_result.step_count
        if tool_call_count == 0 and step_count is not None:
            tool_call_count = step_count

        metrics = CycleMetrics(
            cycle_number=cycle_number,
            status=cycle_result.status,
            orientation=orientation,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration_seconds,
            message_count=cycle_result.messages_count,
            tool_call_count=tool_call_count,
            step_count=step_count,
            soft_limit=cycle_result.soft_limit,
            soft_limit_reached=cycle_result.soft_limit_reached,
            steps_in_main_phase=cycle_result.steps_in_main_phase,
            steps_in_wrap_up_phase=cycle_result.steps_in_wrap_up_phase,
            tests_run=cycle_result.tests_run,
            tests_passed=cycle_result.tests_passed,
            tests_failed=cycle_result.tests_failed,
            linting_passed=cycle_result.linting_passed,
            wrap_up_issues=cycle_result.wrap_up_issues or [],
            commit_sha=cycle_result.commit_sha,
            commit_message=cycle_result.commit_message,
            prompt_tokens=cycle_result.prompt_tokens,
            completion_tokens=cycle_result.completion_tokens,
        )
        self._cycles.append(metrics)
        return metrics

    def to_dict(self) -> dict[str, Any]:
        return {
            "cycle_metrics": [metric.to_dict() for metric in self._cycles],
            "cycle_metrics_summary": self._build_summary(),
        }

    def _build_summary(self) -> dict[str, Any]:
        if not self._cycles:
            return {}

        durations = [m.duration_seconds for m in self._cycles if m.duration_seconds is not None]
        steps = [float(m.step_count) for m in self._cycles if m.step_count is not None]
        tests_run = sum(m.tests_run for m in self._cycles)
        tests_failed = sum(m.tests_failed for m in self._cycles)

        return {
            "cycles": len(self._cycles),
            "avg_duration_seconds": _mean(durations),
            "avg_step_count": _mean(steps),
            "tests_run": tests_run,
            "tests_failed": tests_failed,
        }
