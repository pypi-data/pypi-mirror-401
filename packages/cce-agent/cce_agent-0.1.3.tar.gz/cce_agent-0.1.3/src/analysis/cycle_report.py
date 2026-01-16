"""Cycle analysis report generator."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

from src.analysis.empirical_questions import check_empirical_questions, summarize_runs
from src.config.artifact_root import get_command_outputs_directory, get_runs_directory


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return float(mean(values))


def _format_float(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}"


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|")


def _load_run_logs(runs_dir: Path) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for path in sorted(runs_dir.glob("*/manifest.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            runs.append(data)
    for path in sorted(runs_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            runs.append(data)
    return runs


def _get_cycles(run: dict[str, Any]) -> list[dict[str, Any]]:
    cycles = run.get("execution_cycles") or []
    return [cycle for cycle in cycles if isinstance(cycle, dict)]


def _build_run_table(run_logs: list[dict[str, Any]]) -> str:
    if not run_logs:
        return "No run logs found."

    header = "| Run ID | Ticket | Status | Cycles | Avg Steps | Avg Wrap-up | Commits |"
    divider = "| --- | --- | --- | --- | --- | --- | --- |"
    lines = [header, divider]

    for run in run_logs:
        run_id = run.get("run_id") or run.get("thread_id") or "unknown"
        ticket = run.get("ticket", {}) if isinstance(run.get("ticket"), dict) else {}
        ticket_number = ticket.get("number", run.get("ticket_number", "?"))
        ticket_title = ticket.get("title", run.get("ticket_title", ""))
        ticket_label = f"{ticket_number} {ticket_title}".strip()
        status = run.get("status", "unknown")

        cycles = _get_cycles(run)
        step_counts = [
            float(cycle.get("step_count"))
            for cycle in cycles
            if isinstance(cycle.get("step_count"), (int, float))
        ]
        wrap_counts = [
            float(cycle.get("steps_in_wrap_up_phase"))
            for cycle in cycles
            if isinstance(cycle.get("steps_in_wrap_up_phase"), (int, float))
        ]
        avg_steps = _format_float(_mean(step_counts))
        avg_wrap = _format_float(_mean(wrap_counts))
        commit_count = sum(1 for cycle in cycles if cycle.get("commit_sha"))

        lines.append(
            "| "
            + " | ".join(
                [
                    _escape_table(str(run_id)),
                    _escape_table(ticket_label),
                    _escape_table(str(status)),
                    str(len(cycles)),
                    avg_steps,
                    avg_wrap,
                    str(commit_count),
                ]
            )
            + " |"
        )

    return "\n".join(lines)


def _format_empirical_report(report: dict[str, Any]) -> str:
    if not report:
        return "No empirical data available."

    sections: list[str] = []
    for question, details in report.items():
        sections.append(f"### {question}")
        if isinstance(details, dict):
            for key, value in details.items():
                sections.append(f"- {key}: {value}")
        else:
            sections.append(f"- {details}")
        sections.append("")
    return "\n".join(sections).strip()


def generate_cycle_analysis_report(output_path: Path | None = None) -> Path:
    """
    Generate a cycle analysis report from run logs.

    Args:
        output_path: Optional output path for the report. Defaults to the command outputs directory.

    Returns:
        Path to the written report.
    """
    runs_dir = get_runs_directory()
    run_logs = _load_run_logs(runs_dir)
    summaries = summarize_runs(run_logs)
    empirical_report = check_empirical_questions(summaries)

    total_cycles = sum(len(_get_cycles(run)) for run in run_logs)
    total_commits = sum(
        1 for run in run_logs for cycle in _get_cycles(run) if cycle.get("commit_sha")
    )

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    report_body = f"""# Cycle Analysis Report

Generated: {generated_at}
Runs directory: {runs_dir}

## Overview
- Runs analyzed: {len(run_logs)}
- Total cycles: {total_cycles}
- Total commits: {total_commits}

## Run Summary
{_build_run_table(run_logs)}

## Empirical Questions
{_format_empirical_report(empirical_report)}
"""

    if output_path is None:
        outputs_dir = get_command_outputs_directory() / "reports"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_path = outputs_dir / f"cycle_analysis_report_{timestamp}.md"
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(report_body.strip() + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    report_path = generate_cycle_analysis_report()
    print(f"Wrote cycle analysis report to {report_path}")


if __name__ == "__main__":
    main()
