"""
Run tracking system for CCE Agent (legacy).

Deprecated in favor of manifest-based storage in src/run_manifest.py.
"""

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


class RunTracker:
    """
    Manages comprehensive run tracking for CCE Agent executions.

    Deprecated: use RunManifest (src/run_manifest.py).

    Features:
    - Thread ID generation following ticket-{number}-run-{uuid} format
    - Atomic JSON file writes with crash recovery
    - Token usage aggregation across planning and execution phases
    - Complete audit trail of tool calls and agent decisions
    - Local storage in agent's primary environment (artifact root)
    """

    def __init__(self, runs_directory: str | None = None):
        """
        Initialize the run tracker.

        Args:
            runs_directory: Optional directory to store run files.
                          If None, uses artifact root (recommended).
                          If provided, uses that path (for backward compatibility).
        """
        if runs_directory is None:
            self.runs_dir = get_runs_directory()
        else:
            self.runs_dir = Path(runs_directory)
            self.runs_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.current_run: RunLog | None = None

        self.logger.info(f"RunTracker initialized - storing runs in: {self.runs_dir.absolute()}")

    def start_run(self, ticket: Ticket) -> RunLog:
        """
        Start tracking a new agent run for the given ticket.

        Args:
            ticket: The ticket being processed

        Returns:
            RunLog instance for this run
        """
        run_log = RunLog(
            thread_id="",  # Will be generated
            run_id="",  # Will be generated
            ticket=ticket,
            start_time=datetime.now(),
            status="running",
        )

        # Generate thread_id and run_id
        run_log.thread_id = run_log.generate_thread_id()
        run_log.run_id = run_log.thread_id  # Use thread_id as run_id for simplicity

        self.current_run = run_log
        self._save_run(run_log)

        self.logger.info(f"Started run tracking: {run_log.thread_id}")
        return run_log

    def record_planning_start(self) -> None:
        """Record the start of the planning phase."""
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
        self._save_run(self.current_run)
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
        """
        Record the completion of the planning phase.

        Args:
            status: 'completed' or 'failed'
            iterations: Number of planning iterations
            messages_count: Total messages in planning
            technical_analysis: Technical planner's analysis
            architectural_analysis: Architectural planner's analysis
            final_plan: The final collaborative plan
            token_usage: List of token usage records
            tool_calls: List of tool calls made during planning
        """
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

        # Update aggregated metrics
        self.current_run.total_messages += messages_count
        self.current_run.total_tool_calls += len(tool_calls)

        for usage in token_usage:
            self.current_run.add_token_usage(usage)

        self._save_run(self.current_run)
        self.logger.info(f"Planning phase completed: {status} ({iterations} iterations, {len(tool_calls)} tool calls)")

    def record_execution_cycle_start(self, cycle_number: int, orientation: str) -> None:
        """
        Record the start of an execution cycle.

        Args:
            cycle_number: The cycle number (1-based)
            orientation: The orientation/focus for this cycle
        """
        if not self.current_run:
            raise ValueError("No active run to record execution cycle for")

        cycle_result = CycleResult(
            cycle_number=cycle_number, status="running", orientation=orientation, start_time=datetime.now()
        )

        self.current_run.execution_cycles.append(cycle_result)
        self._save_run(self.current_run)
        self.logger.info(f"Execution cycle {cycle_number} started")

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
        """
        Record the completion of an execution cycle.

        Args:
            cycle_number: The cycle number (1-based)
            status: 'success', 'failure', or 'max_iterations_hit'
            messages_count: Number of messages in this cycle
            tool_calls: Tool calls made during this cycle
            token_usage: Token usage during this cycle
            final_summary: Summary of what was accomplished
            commit_sha: Optional git commit SHA for this cycle
            commit_message: Optional git commit message for this cycle
            step_count: Optional step/tool-call count override
            soft_limit: Optional soft limit for this cycle
            soft_limit_reached: Optional soft limit reached flag
            steps_in_main_phase: Optional steps in main phase
            steps_in_wrap_up_phase: Optional steps in wrap-up phase
        """
        if not self.current_run:
            raise ValueError("No active run to record execution cycle completion for")

        # Find the cycle to update
        cycle = None
        for c in self.current_run.execution_cycles:
            if c.cycle_number == cycle_number:
                cycle = c
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
        if soft_limit is not None:
            cycle.soft_limit = soft_limit
        if soft_limit_reached is not None:
            cycle.soft_limit_reached = soft_limit_reached
        if steps_in_main_phase is not None:
            cycle.steps_in_main_phase = steps_in_main_phase
        if steps_in_wrap_up_phase is not None:
            cycle.steps_in_wrap_up_phase = steps_in_wrap_up_phase
        cycle.prompt_tokens = sum(usage.prompt_tokens for usage in token_usage)
        cycle.completion_tokens = sum(usage.completion_tokens for usage in token_usage)
        if not cycle.cycle_summary:
            cycle.cycle_summary = final_summary

        # Update aggregated metrics
        self.current_run.total_messages += messages_count
        self.current_run.total_tool_calls += len(tool_calls)

        for usage in token_usage:
            self.current_run.add_token_usage(usage)

        self._save_run(self.current_run)
        self.logger.info(f"Execution cycle {cycle_number} completed: {status} ({len(tool_calls)} tool calls)")

    def complete_run(self, status: str, final_summary: str, error_message: str = "") -> RunLog:
        """
        Complete the current run and finalize the run log.

        Args:
            status: 'completed' or 'failed'
            final_summary: Summary of the entire run
            error_message: Error message if the run failed

        Returns:
            The completed RunLog
        """
        if not self.current_run:
            raise ValueError("No active run to complete")

        self.current_run.status = status
        self.current_run.final_summary = final_summary
        self.current_run.error_message = error_message
        self.current_run.end_time = datetime.now()

        self._save_run(self.current_run)

        completed_run = self.current_run
        self.current_run = None

        total_tokens = completed_run.get_total_tokens()
        self.logger.info(
            f"Run completed: {status} (Total tokens: {total_tokens}, Tool calls: {completed_run.total_tool_calls})"
        )

        return completed_run

    def _save_run(self, run_log: RunLog) -> None:
        """
        Atomically save the run log to a JSON file.

        Uses atomic write pattern with temporary file and move to ensure
        crash safety and prevent corrupted files.

        Args:
            run_log: The run log to save
        """
        timestamp = run_log.start_time.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}-ticket-{run_log.ticket.number}-run-{run_log.run_id}.json"
        filepath = self.runs_dir / filename

        # Convert dataclass to dict for JSON serialization
        run_data = self._serialize_run_log(run_log)

        # Atomic write using temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tmp", dir=self.runs_dir, delete=False) as tmp_file:
            json.dump(run_data, tmp_file, indent=2, default=str)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
            tmp_path = tmp_file.name

        # Atomic move
        shutil.move(tmp_path, filepath)

        self.logger.debug(f"Saved run log: {filepath}")

    def _serialize_run_log(self, run_log: RunLog) -> dict[str, Any]:
        """
        Convert RunLog dataclass to JSON-serializable dictionary.

        Args:
            run_log: The run log to serialize

        Returns:
            Dictionary representation suitable for JSON
        """

        def serialize_dataclass(obj):
            """Recursively serialize dataclasses to dicts."""
            if hasattr(obj, "__dataclass_fields__"):
                return {field: serialize_dataclass(getattr(obj, field)) for field in obj.__dataclass_fields__}
            elif isinstance(obj, list):
                return [serialize_dataclass(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: serialize_dataclass(value) for key, value in obj.items()}
            elif isinstance(obj, datetime):
                return obj.isoformat()
            else:
                return obj

        return serialize_dataclass(run_log)

    def load_run(self, thread_id: str) -> RunLog | None:
        """
        Load a run log by thread_id.

        Args:
            thread_id: The thread_id to search for

        Returns:
            RunLog if found, None otherwise
        """
        for filepath in self.runs_dir.glob("*.json"):
            try:
                with open(filepath) as f:
                    data = json.load(f)
                    if data.get("thread_id") == thread_id:
                        return self._deserialize_run_log(data)
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.warning(f"Could not load run file {filepath}: {e}")

        return None

    def list_runs(self, ticket_number: int | None = None) -> list[dict[str, Any]]:
        """
        List all runs, optionally filtered by ticket number.

        Args:
            ticket_number: Optional ticket number to filter by

        Returns:
            List of run summary dictionaries
        """
        runs = []
        for filepath in sorted(self.runs_dir.glob("*.json")):
            try:
                with open(filepath) as f:
                    data = json.load(f)

                    # Handle both old format (ticket_number) and new format (ticket.number)
                    ticket_data = data.get("ticket", {})
                    run_ticket_number = ticket_data.get("number", data.get("ticket_number"))

                    if ticket_number and run_ticket_number != ticket_number:
                        continue

                    runs.append(
                        {
                            "thread_id": data.get("thread_id"),
                            "ticket_number": run_ticket_number,
                            "ticket_title": ticket_data.get("title", data.get("ticket_title", "")),
                            "status": data.get("status"),
                            "start_time": data.get("start_time"),
                            "end_time": data.get("end_time"),
                            "total_tokens": sum(data.get("total_token_usage", {}).values()),
                            "total_tool_calls": data.get("total_tool_calls", 0),
                            "filepath": str(filepath),
                        }
                    )
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.warning(f"Could not load run file {filepath}: {e}")

        return runs

    def _deserialize_run_log(self, data: dict[str, Any]) -> RunLog:
        """
        Convert JSON dictionary back to RunLog dataclass.

        Args:
            data: Dictionary loaded from JSON

        Returns:
            RunLog instance
        """
        # This is a simplified version - full implementation would need
        # recursive deserialization of all nested dataclasses
        # For now, we'll keep it simple and just return the basic structure

        # Create a basic Ticket object from the data
        from src.models import Ticket

        ticket_data = data.get("ticket", {})
        ticket = Ticket(
            number=ticket_data.get("number", data.get("ticket_number", 0)),
            title=ticket_data.get("title", data.get("ticket_title", "")),
            description=ticket_data.get("description", ""),
            url=ticket_data.get("url", f"https://github.com/unknown/repo/issues/{ticket_data.get('number', 0)}"),
            labels=ticket_data.get("labels", []),
            assignee=ticket_data.get("assignee"),
        )

        run_log = RunLog(
            thread_id=data.get("thread_id", ""),
            run_id=data.get("run_id", ""),
            ticket=ticket,
            start_time=datetime.now(),  # Will be overridden below
            status=data.get("status", "unknown"),
            total_tool_calls=data.get("total_tool_calls", 0),
            total_messages=data.get("total_messages", 0),
            final_summary=data.get("final_summary", ""),
            error_message=data.get("error_message", ""),
        )

        # Parse timestamps
        if data.get("start_time"):
            run_log.start_time = datetime.fromisoformat(data["start_time"])
        if data.get("end_time"):
            run_log.end_time = datetime.fromisoformat(data["end_time"])

        return run_log
