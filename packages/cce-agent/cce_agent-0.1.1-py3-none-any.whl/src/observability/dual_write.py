"""
Dual-Write Trace Architecture

This module implements a dual-write architecture for trace storage:
1. LangSmith - For UI visualization and querying
2. Local files - For offline analysis and AI processing

This addresses the issue discovered during the December 2024 run analysis where
LangSmith API returned 502 errors for large traces (~4.7M tokens).

See ticket #85 for full context.

Usage:
    from src.observability.dual_write import DualWriteTraceContext

    async with DualWriteTraceContext(
        ticket_number=123,
        ticket_url="https://github.com/...",
        local_storage_path="runs/traces/",
    ) as ctx:
        result = await agent.process_ticket(ticket)

Environment Variables:
    LANGSMITH_API_KEY: LangSmith API key
    LANGSMITH_PROJECT: Project name (default: cce-agent)
    CCE_LOCAL_TRACE_PATH: Local storage path for traces (default: runs/traces/)
    CCE_ENABLE_DUAL_WRITE: Enable dual-write (default: true if LANGSMITH_API_KEY set)
"""

import json
import logging
import os
from datetime import UTC, datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Check if LangSmith is available
try:
    from langsmith import Client
    from langsmith.run_helpers import tracing_context

    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    Client = None
    tracing_context = None


class LocalTraceWriter:
    """
    Writes trace data to local JSON files for offline analysis.

    File structure:
        {local_path}/
        ├── ticket-123-2024-12-23T12-00-00/
        │   ├── metadata.json       # Run metadata
        │   ├── messages.jsonl      # Message entries (append-only)
        │   ├── tool_calls.jsonl    # Tool call entries (append-only)
        │   ├── metrics.json        # Aggregated metrics
        │   └── summary.json        # Final summary (written on close)
    """

    def __init__(
        self,
        base_path: str = "runs/traces/",
        ticket_number: int | None = None,
    ):
        self.base_path = Path(base_path)
        self.ticket_number = ticket_number
        self.run_id = self._generate_run_id()
        self.run_path = self.base_path / self.run_id
        self.metadata: dict[str, Any] = {}
        self.message_count = 0
        self.tool_call_count = 0
        self.event_count = 0
        self.metrics: dict[str, Any] = {}
        self._initialized = False
        self._messages_path = self.run_path / "messages.jsonl"
        self._tool_calls_path = self.run_path / "tool_calls.jsonl"
        self._metrics_path = self.run_path / "metrics.json"
        self._events_path = self.run_path / "trace.jsonl"

    def _generate_run_id(self) -> str:
        """Generate a unique run ID."""
        timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%S")
        if self.ticket_number:
            return f"ticket-{self.ticket_number}-{timestamp}"
        return f"run-{timestamp}"

    def initialize(self, metadata: dict[str, Any]) -> None:
        """Initialize the local trace storage."""
        self.metadata = {
            "run_id": self.run_id,
            "ticket_number": self.ticket_number,
            "started_at": datetime.now(UTC).isoformat(),
            **metadata,
        }

        # Create directory
        self.run_path.mkdir(parents=True, exist_ok=True)
        self._messages_path.touch(exist_ok=True)
        self._tool_calls_path.touch(exist_ok=True)

        # Write initial metadata
        metadata_path = self.run_path / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2, default=str)

        self._initialized = True
        logger.info(f"📁 Local trace initialized: {self.run_path}")

    def _append_jsonl(self, path: Path, entry: dict[str, Any]) -> None:
        """Append a JSON entry to a JSONL file with a timestamp."""
        if not self._initialized:
            return

        entry_with_timestamp = {
            "timestamp": datetime.now(UTC).isoformat(),
            **entry,
        }

        with open(path, "a") as f:
            f.write(json.dumps(entry_with_timestamp, ensure_ascii=True, default=str) + "\n")

    def write_message_entry(self, entry: dict[str, Any]) -> None:
        """Write a message entry to the local trace."""
        if not self._initialized:
            return

        self._append_jsonl(self._messages_path, entry)
        self.message_count += 1

    def write_tool_call_entry(self, entry: dict[str, Any]) -> None:
        """Write a tool call entry to the local trace."""
        if not self._initialized:
            return

        self._append_jsonl(self._tool_calls_path, entry)
        self.tool_call_count += 1

    def update_metrics(self, metrics: dict[str, Any]) -> None:
        """Update aggregated metrics for the trace."""
        if not self._initialized:
            return

        self.metrics.update(metrics)
        with open(self._metrics_path, "w") as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=True, default=str)

    def write_event(self, event: dict[str, Any]) -> None:
        """Write a trace event to the local file."""
        if not self._initialized:
            return
        self._append_jsonl(self._events_path, event)
        self.event_count += 1

    def finalize(self, summary: dict[str, Any]) -> str:
        """Finalize the trace and write summary."""
        if not self._initialized:
            return ""

        # Update metadata with end time
        self.metadata["ended_at"] = datetime.now(UTC).isoformat()
        self.metadata["message_count"] = self.message_count
        self.metadata["tool_call_count"] = self.tool_call_count
        self.metadata["event_count"] = self.event_count
        self.metadata.update(summary)

        # Write updated metadata
        metadata_path = self.run_path / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2, default=str)

        # Write summary
        summary_path = self.run_path / "summary.json"
        with open(summary_path, "w") as f:
            json.dump(
                {
                    "run_id": self.run_id,
                    "status": summary.get("status", "unknown"),
                    "duration_seconds": summary.get("duration_seconds"),
                    "duration_ms": summary.get("duration_ms"),
                    "error": summary.get("error"),
                    "messages": {"total": self.message_count},
                    "tool_calls": {"total": self.tool_call_count},
                    "events": {"total": self.event_count},
                    "metrics": self.metrics,
                    "summary": summary,
                },
                f,
                indent=2,
                ensure_ascii=True,
                default=str,
            )

        logger.info(f"📁 Local trace finalized: {self.run_path}")
        return str(self.run_path)


class DualWriteTraceContext:
    """
    Context manager for dual-write tracing to both LangSmith and local storage.

    This ensures trace data is available even when LangSmith API has issues
    with large traces.

    Usage:
        async with DualWriteTraceContext(
            ticket_number=123,
            ticket_url="https://github.com/...",
        ) as ctx:
            result = await agent.process_ticket(ticket)
            ctx.write_event({"type": "completed", "result": result})
    """

    def __init__(
        self,
        ticket_number: int,
        ticket_url: str,
        project_name: str | None = None,
        local_storage_path: str | None = None,
        enable_langsmith: bool = True,
        enable_local: bool = True,
        extra_tags: list[str] | None = None,
        extra_metadata: dict[str, Any] | None = None,
    ):
        self.ticket_number = ticket_number
        self.ticket_url = ticket_url
        self.project_name = project_name or os.getenv("LANGSMITH_PROJECT", "cce-agent")
        self.local_storage_path = local_storage_path or os.getenv("CCE_LOCAL_TRACE_PATH", "runs/traces/")
        self.enable_langsmith = enable_langsmith and LANGSMITH_AVAILABLE
        self.enable_local = enable_local
        self.tags = ["ticket-processing", f"ticket-{ticket_number}"] + (extra_tags or [])
        self.metadata = {
            "ticket_url": ticket_url,
            "ticket_number": ticket_number,
            **(extra_metadata or {}),
        }

        self._langsmith_context = None
        self._local_writer: LocalTraceWriter | None = None
        self._start_time: datetime | None = None
        self._phase_starts: dict[str, datetime] = {}
        self._phase_timings: list[dict[str, Any]] = []

    def _get_git_info(self) -> dict[str, str]:
        """Get current git branch and commit."""
        import subprocess

        git_info = {}
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                git_info["git_branch"] = result.stdout.strip()
        except Exception:
            pass

        try:
            result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                git_info["git_commit"] = result.stdout.strip()[:8]
        except Exception:
            pass

        return git_info

    async def __aenter__(self):
        """Enter the dual-write trace context."""
        self._start_time = datetime.now(UTC)

        # Add git info to metadata
        self.metadata.update(self._get_git_info())

        # Start LangSmith tracing
        if self.enable_langsmith:
            try:
                self._langsmith_context = tracing_context(
                    project_name=self.project_name,
                    tags=self.tags,
                    metadata=self.metadata,
                )
                self._langsmith_context.__enter__()
                logger.info(f"📊 LangSmith tracing started for ticket #{self.ticket_number}")
            except Exception as e:
                logger.warning(f"Failed to start LangSmith tracing: {e}")

        # Start local tracing
        if self.enable_local:
            try:
                self._local_writer = LocalTraceWriter(
                    base_path=self.local_storage_path,
                    ticket_number=self.ticket_number,
                )
                self._local_writer.initialize(self.metadata)
            except Exception as e:
                logger.warning(f"Failed to start local tracing: {e}")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the dual-write trace context."""
        duration_seconds = None
        duration_ms = None
        if self._start_time:
            duration_seconds = (datetime.now(UTC) - self._start_time).total_seconds()
            duration_ms = duration_seconds * 1000

        summary = {
            "status": "error" if exc_type else "completed",
            "duration_seconds": duration_seconds,
            "duration_ms": duration_ms,
            "error": str(exc_val) if exc_val else None,
        }

        # Close LangSmith context
        if self._langsmith_context is not None:
            try:
                self._langsmith_context.__exit__(exc_type, exc_val, exc_tb)
                if exc_type:
                    logger.warning(f"📊 LangSmith trace ended with error for ticket #{self.ticket_number}")
                else:
                    logger.info(f"📊 LangSmith trace completed for ticket #{self.ticket_number}")
            except Exception as e:
                logger.warning(f"Error closing LangSmith context: {e}")

        # Finalize local trace
        if self._local_writer is not None:
            try:
                local_path = self._local_writer.finalize(summary)
                logger.info(f"📁 Local trace saved: {local_path}")
            except Exception as e:
                logger.warning(f"Error finalizing local trace: {e}")

        return False  # Don't suppress exceptions

    def start_phase(self, name: str) -> None:
        """Mark the start of a named phase."""
        self._phase_starts[name] = datetime.now(UTC)
        if self._local_writer:
            self._local_writer.write_event({"type": "phase_start", "name": name})

    def end_phase(self, name: str) -> None:
        """Mark the end of a named phase."""
        started_at = self._phase_starts.pop(name, None)
        ended_at = datetime.now(UTC)
        duration_s = (ended_at - started_at).total_seconds() if started_at else None
        phase_record = {
            "name": name,
            "started_at": started_at.isoformat() if started_at else None,
            "ended_at": ended_at.isoformat(),
            "duration_s": duration_s,
        }
        self._phase_timings.append(phase_record)
        if self._local_writer:
            self._local_writer.write_event({"type": "phase_end", **phase_record})

    def get_phase_timings(self) -> list[dict[str, Any]]:
        """Return recorded phase timing data."""
        return list(self._phase_timings)

    def _format_message_entry(
        self,
        message: Any,
        phase: str | None = None,
        cycle_number: int | None = None,
    ) -> dict[str, Any]:
        role = getattr(message, "type", None) or getattr(message, "role", None)
        if not role:
            role = message.__class__.__name__.replace("Message", "").lower()

        content = getattr(message, "content", message)
        if not isinstance(content, str):
            content = str(content)

        entry = {"role": role, "content": content}
        if phase:
            entry["phase"] = phase
        if cycle_number is not None:
            entry["cycle_number"] = cycle_number
        return entry

    def _format_tool_call_entry(
        self,
        tool_call: Any,
        phase: str | None = None,
        cycle_number: int | None = None,
    ) -> dict[str, Any]:
        entry: dict[str, Any] = {}

        if isinstance(tool_call, dict):
            entry.update(tool_call)
        else:
            tool_name = getattr(tool_call, "tool_name", None)
            if tool_name:
                entry["tool_name"] = tool_name
                entry["arguments"] = getattr(tool_call, "arguments", {})
                result = getattr(tool_call, "result", None)
                if result is not None:
                    entry["result"] = result
                error = getattr(tool_call, "error", None)
                if error:
                    entry["error"] = error
                duration_seconds = getattr(tool_call, "duration_seconds", None)
                if duration_seconds is not None:
                    entry["duration_seconds"] = duration_seconds
                timestamp = getattr(tool_call, "timestamp", None)
                if timestamp is not None:
                    entry["timestamp"] = timestamp.isoformat() if hasattr(timestamp, "isoformat") else str(timestamp)
            else:
                entry["tool_name"] = str(tool_call)

        if phase:
            entry["phase"] = phase
        if cycle_number is not None:
            entry["cycle_number"] = cycle_number
        return entry

    def write_messages(
        self,
        messages: list[Any],
        phase: str | None = None,
        cycle_number: int | None = None,
    ) -> None:
        """Write message entries to the local trace."""
        if not self._local_writer:
            return

        for message in messages:
            entry = self._format_message_entry(message, phase=phase, cycle_number=cycle_number)
            self._local_writer.write_message_entry(entry)

    def write_tool_calls(
        self,
        tool_calls: list[Any],
        phase: str | None = None,
        cycle_number: int | None = None,
    ) -> None:
        """Write tool call entries to the local trace."""
        if not self._local_writer:
            return

        for tool_call in tool_calls:
            entry = self._format_tool_call_entry(tool_call, phase=phase, cycle_number=cycle_number)
            self._local_writer.write_tool_call_entry(entry)

    def write_metrics(self, metrics: dict[str, Any]) -> None:
        """Write or update metrics in the local trace."""
        if self._local_writer:
            self._local_writer.update_metrics(metrics)

    def write_event(self, event: dict[str, Any]) -> None:
        """Write an event to the local trace."""
        if self._local_writer:
            self._local_writer.write_event(event)

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to both traces."""
        self.metadata[key] = value
        if self._local_writer:
            self._local_writer.metadata[key] = value


def dual_write_trace_context(
    ticket_number: int,
    ticket_url: str,
    project_name: str | None = None,
    local_storage_path: str | None = None,
    enable_langsmith: bool = True,
    enable_local: bool = True,
    extra_tags: list[str] | None = None,
    extra_metadata: dict[str, Any] | None = None,
) -> DualWriteTraceContext:
    """
    Create a dual-write tracing context.

    This ensures trace data is written to both LangSmith (for UI) and
    local files (for offline analysis).

    Args:
        ticket_number: GitHub issue number
        ticket_url: Full URL to the GitHub issue
        project_name: LangSmith project name
        local_storage_path: Local path for trace files
        enable_langsmith: Whether to enable LangSmith tracing
        enable_local: Whether to enable local file tracing
        extra_tags: Additional tags for the trace
        extra_metadata: Additional metadata for the trace

    Returns:
        DualWriteTraceContext async context manager

    Example:
        async with dual_write_trace_context(123, "https://github.com/...") as ctx:
            result = await agent.process_ticket(ticket)
            ctx.add_metadata("pr_url", result.pr_url)
    """
    return DualWriteTraceContext(
        ticket_number=ticket_number,
        ticket_url=ticket_url,
        project_name=project_name,
        local_storage_path=local_storage_path,
        enable_langsmith=enable_langsmith,
        enable_local=enable_local,
        extra_tags=extra_tags,
        extra_metadata=extra_metadata,
    )


def is_dual_write_enabled() -> bool:
    """Check if dual-write tracing is enabled via environment configuration."""
    env_value = os.getenv("CCE_ENABLE_DUAL_WRITE")
    if env_value is None:
        return bool(os.getenv("LANGSMITH_API_KEY"))
    return env_value.strip().lower() in {"1", "true", "yes", "on"}
