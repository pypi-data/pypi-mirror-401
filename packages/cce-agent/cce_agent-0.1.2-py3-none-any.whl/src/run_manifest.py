"""
Manifest-based run storage for CCE Agent.

This replaces the legacy flat JSON RunTracker files with per-run directories
containing a single manifest.json payload.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from src.config.artifact_root import get_runs_directory
from src.models import CycleResult, PlanningResult, RunLog, Ticket, TokenUsage, ToolCall


class RunManifest:
    """
    Persist run data as manifest.json under a per-run directory.

    Directory layout:
        <runs_dir>/<run_id>/manifest.json
    """

    def __init__(self, runs_directory: str | None = None) -> None:
        if runs_directory is None:
            self.runs_dir = get_runs_directory()
        else:
            self.runs_dir = Path(runs_directory)
            self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.current_run: RunLog | None = None
        self.current_run_dir: Path | None = None

        self.logger.info("RunManifest initialized - storing runs in: %s", self.runs_dir.absolute())

    def start_run(self, ticket: Ticket) -> RunLog:
        run_log = RunLog(
            thread_id="",
            run_id="",
            ticket=ticket,
            start_time=datetime.now(),
            status="running",
        )
        run_log.thread_id = run_log.generate_thread_id()
        run_log.run_id = run_log.thread_id

        run_dir = self.runs_dir / run_log.run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        self.current_run = run_log
        self.current_run_dir = run_dir
        self._write_manifest(run_log)

        self.logger.info("Started run tracking: %s", run_log.thread_id)
        return run_log

    def record_planning_start(self) -> None:
        if not self.current_run:
            raise ValueError("No active run to record planning for")

        self.current_run.planning_result = PlanningResult(
            status="running",
            iterations=0,
            consensus_reached=False,
            shared_plan="",
            technical_analysis="",
            architectural_analysis="",
        )
        self._write_manifest(self.current_run)
        self.logger.info("Planning phase started")

    def record_planning_completion(
        self,
        status: str,
        iterations: int,
        messages_count: int,
        technical_analysis: str,
        architectural_analysis: str,
        final_plan: str,
        token_usage: list[TokenUsage],
        tool_calls: list[ToolCall],
    ) -> None:
        if not self.current_run or not self.current_run.planning_result:
            raise ValueError("No active planning phase to complete")

        planning = self.current_run.planning_result
        planning.status = status
        planning.iterations = iterations
        planning.messages_count = messages_count
        planning.technical_analysis = technical_analysis
        planning.architectural_analysis = architectural_analysis
        planning.final_plan = final_plan
        planning.token_usage = token_usage
        planning.tool_calls = tool_calls
        planning.end_time = datetime.now()

        self.current_run.total_messages += messages_count
        self.current_run.total_tool_calls += len(tool_calls)

        for usage in token_usage:
            self.current_run.add_token_usage(usage)

        self._write_manifest(self.current_run)
        self.logger.info(
            "Planning phase completed: %s (%s iterations, %s tool calls)",
            status,
            iterations,
            len(tool_calls),
        )

    def record_execution_cycle_start(self, cycle_number: int, orientation: str) -> None:
        if not self.current_run:
            raise ValueError("No active run to record execution cycle for")

        cycle_result = CycleResult(
            cycle_number=cycle_number,
            status="running",
            orientation=orientation,
            start_time=datetime.now(),
        )

        self.current_run.execution_cycles.append(cycle_result)
        self._write_manifest(self.current_run)
        self.logger.info("Execution cycle %s started", cycle_number)

    def record_execution_cycle_completion(
        self,
        cycle_number: int,
        status: str,
        messages_count: int,
        tool_calls: list[ToolCall],
        token_usage: list[TokenUsage],
        final_summary: str,
        commit_sha: str | None = None,
        commit_message: str | None = None,
        step_count: int | None = None,
        soft_limit: int | None = None,
        soft_limit_reached: bool | None = None,
        steps_in_main_phase: int | None = None,
        steps_in_wrap_up_phase: int | None = None,
    ) -> None:
        if not self.current_run:
            raise ValueError("No active run to record execution cycle completion for")

        cycle = None
        for existing in self.current_run.execution_cycles:
            if existing.cycle_number == cycle_number:
                cycle = existing
                break

        if not cycle:
            raise ValueError(f"No active cycle {cycle_number} found")

        cycle.status = status
        cycle.messages_count = messages_count
        cycle.tool_calls = tool_calls
        cycle.token_usage = token_usage
        cycle.final_summary = final_summary
        if commit_sha:
            cycle.commit_sha = commit_sha
        if commit_message:
            cycle.commit_message = commit_message
        cycle.end_time = datetime.now()
        cycle.duration_seconds = (cycle.end_time - cycle.start_time).total_seconds()
        cycle.step_count = step_count if step_count is not None else len(tool_calls)
        cycle.prompt_tokens = sum(usage.prompt_tokens for usage in token_usage)
        cycle.completion_tokens = sum(usage.completion_tokens for usage in token_usage)
        if soft_limit is not None:
            cycle.soft_limit = soft_limit
        if soft_limit_reached is not None:
            cycle.soft_limit_reached = soft_limit_reached
        if steps_in_main_phase is not None:
            cycle.steps_in_main_phase = steps_in_main_phase
        if steps_in_wrap_up_phase is not None:
            cycle.steps_in_wrap_up_phase = steps_in_wrap_up_phase
        if not cycle.cycle_summary:
            cycle.cycle_summary = final_summary

        self.current_run.total_messages += messages_count
        self.current_run.total_tool_calls += len(tool_calls)

        for usage in token_usage:
            self.current_run.add_token_usage(usage)

        self._write_manifest(self.current_run)
        self.logger.info("Execution cycle %s completed: %s", cycle_number, status)

    def complete_run(self, status: str, final_summary: str, error_message: str = "") -> RunLog:
        if not self.current_run:
            raise ValueError("No active run to complete")

        self.current_run.status = status
        self.current_run.final_summary = final_summary
        self.current_run.error_message = error_message
        self.current_run.end_time = datetime.now()

        self._write_manifest(self.current_run)

        completed_run = self.current_run
        self.current_run = None
        self.current_run_dir = None

        total_tokens = completed_run.get_total_tokens()
        self.logger.info(
            "Run completed: %s (Total tokens: %s, Tool calls: %s)",
            status,
            total_tokens,
            completed_run.total_tool_calls,
        )

        return completed_run

    def list_runs(self, ticket_number: int | None = None) -> list[dict[str, Any]]:
        runs: list[dict[str, Any]] = []
        for run_dir in sorted(self.runs_dir.iterdir()):
            if not run_dir.is_dir():
                continue
            manifest_path = run_dir / "manifest.json"
            if not manifest_path.exists():
                continue
            try:
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                self.logger.warning("Could not load manifest %s: %s", manifest_path, exc)
                continue

            ticket_data = data.get("ticket", {})
            run_ticket_number = ticket_data.get("number", data.get("ticket_number"))
            if ticket_number and run_ticket_number != ticket_number:
                continue

            runs.append(
                {
                    "run_id": data.get("run_id"),
                    "thread_id": data.get("thread_id"),
                    "ticket_number": run_ticket_number,
                    "ticket_title": ticket_data.get("title", data.get("ticket_title", "")),
                    "status": data.get("status"),
                    "start_time": data.get("start_time"),
                    "end_time": data.get("end_time"),
                    "total_tokens": data.get("total_tokens", 0),
                    "total_tool_calls": data.get("total_tool_calls", 0),
                    "manifest_path": str(manifest_path),
                }
            )
        return runs

    def load_run(self, run_id: str) -> RunLog | None:
        manifest_path = self.runs_dir / run_id / "manifest.json"
        if not manifest_path.exists():
            return None
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            self.logger.warning("Could not load manifest %s: %s", manifest_path, exc)
            return None
        return self._deserialize_run_log(data)

    def _write_manifest(self, run_log: RunLog) -> None:
        if self.current_run_dir is None:
            self.current_run_dir = self.runs_dir / run_log.run_id
            self.current_run_dir.mkdir(parents=True, exist_ok=True)

        manifest_path = self.current_run_dir / "manifest.json"
        run_data = self._serialize_run_log(run_log)
        run_data["manifest_version"] = 1

        with tempfile.NamedTemporaryFile(mode="w", suffix=".tmp", dir=self.current_run_dir, delete=False) as tmp_file:
            json.dump(run_data, tmp_file, indent=2, default=str)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
            tmp_path = tmp_file.name

        shutil.move(tmp_path, manifest_path)

    def _serialize_run_log(self, run_log: RunLog) -> dict[str, Any]:
        def serialize_dataclass(obj):
            if hasattr(obj, "__dataclass_fields__"):
                return {field: serialize_dataclass(getattr(obj, field)) for field in obj.__dataclass_fields__}
            if isinstance(obj, list):
                return [serialize_dataclass(item) for item in obj]
            if isinstance(obj, dict):
                return {key: serialize_dataclass(value) for key, value in obj.items()}
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj

        return serialize_dataclass(run_log)

    def _deserialize_run_log(self, data: dict[str, Any]) -> RunLog:
        from src.models import Ticket

        ticket_data = data.get("ticket", {})
        assignees = ticket_data.get("assignees")
        if assignees is None:
            assignee = ticket_data.get("assignee")
            assignees = [assignee] if assignee else []

        ticket = Ticket(
            number=ticket_data.get("number", data.get("ticket_number", 0)),
            title=ticket_data.get("title", data.get("ticket_title", "")),
            description=ticket_data.get("description", ""),
            url=ticket_data.get("url", f"https://github.com/unknown/repo/issues/{ticket_data.get('number', 0)}"),
            labels=ticket_data.get("labels", []),
            assignees=assignees,
        )

        run_log = RunLog(
            thread_id=data.get("thread_id", ""),
            run_id=data.get("run_id", ""),
            ticket=ticket,
            start_time=datetime.now(),
            status=data.get("status", "unknown"),
            total_tool_calls=data.get("total_tool_calls", 0),
            total_messages=data.get("total_messages", 0),
            final_summary=data.get("final_summary", ""),
            error_message=data.get("error_message", ""),
        )

        if data.get("start_time"):
            run_log.start_time = datetime.fromisoformat(data["start_time"])
        if data.get("end_time"):
            run_log.end_time = datetime.fromisoformat(data["end_time"])

        return run_log
