"""
Observability and Tracing for CCE Agent

Provides LangSmith integration and custom tracing decorators for monitoring
agent performance, debugging graph execution, and collecting metrics.

Environment Variables:
- LANGSMITH_TRACING: Enable/disable tracing (default: false)
- LANGSMITH_PROJECT: Project name for traces (default: "cce-agent")
- LANGSMITH_API_KEY: LangSmith API key
"""

import json
import logging
import os
from datetime import UTC, datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

# Conditional LangSmith imports (graceful degradation if not available)
try:
    from langsmith import Client, traceable

    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False

    # Create no-op decorators for when LangSmith is not available
    def traceable(*args, **kwargs):
        def decorator(func):
            return func

        return decorator if args and callable(args[0]) else decorator


class CCETracer:
    """
    Custom tracer for CCE Agent operations.

    Provides structured logging and optional LangSmith integration
    for monitoring agent behavior and performance.
    """

    def __init__(self, enabled: bool | None = None, project_name: str | None = None):
        """
        Initialize the CCE tracer.

        Args:
            enabled: Whether tracing is enabled (None = check env var)
            project_name: LangSmith project name (None = check env var)
        """
        # Check environment variables
        if enabled is None:
            enabled = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"

        if project_name is None:
            try:
                from src.config_loader import get_config

                project_name = get_config().langsmith.project
            except Exception:
                project_name = os.getenv("LANGSMITH_PROJECT", "cce-agent")

        self.enabled = enabled
        self.project_name = project_name
        self.logger = logging.getLogger(__name__)

        # Initialize LangSmith client if available and enabled
        self.langsmith_client = None
        if self.enabled and LANGSMITH_AVAILABLE:
            try:
                self.langsmith_client = Client()
                self.logger.info(f"📊 LangSmith tracing enabled (project: {project_name})")
            except Exception as e:
                self.logger.warning(f"Failed to initialize LangSmith client: {e}")
                self.enabled = False
        elif self.enabled and not LANGSMITH_AVAILABLE:
            self.logger.warning("LangSmith tracing requested but langsmith package not available")
            self.enabled = False
        else:
            self.logger.info("📊 Tracing disabled")

        # Local trace storage for analysis
        self.traces: list[dict[str, Any]] = []

    def trace_graph_execution(self, graph_name: str, ticket_id: str | None = None):
        """
        Decorator for tracing LangGraph execution.

        Args:
            graph_name: Name of the graph being executed
            ticket_id: Optional ticket ID for correlation

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            if not self.enabled:
                return func

            @wraps(func)
            def wrapper(*args, **kwargs):
                # Prepare trace metadata
                metadata = {
                    "graph_name": graph_name,
                    "ticket_id": ticket_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                }

                if LANGSMITH_AVAILABLE and self.langsmith_client:
                    # Use LangSmith tracing
                    @traceable(
                        name=f"graph_{graph_name}",
                        project_name=self.project_name,
                        tags=[graph_name, "langgraph"] + ([f"ticket-{ticket_id}"] if ticket_id else []),
                    )
                    def traced_execution(*args, **kwargs):
                        return func(*args, **kwargs)

                    return traced_execution(*args, **kwargs)
                else:
                    # Fall back to local tracing
                    start_time = datetime.now(UTC)

                    try:
                        result = func(*args, **kwargs)

                        # Record successful execution
                        trace_record = {
                            **metadata,
                            "function": func.__name__,
                            "status": "success",
                            "duration_ms": (datetime.now(UTC) - start_time).total_seconds() * 1000,
                            "args_count": len(args),
                            "kwargs_keys": list(kwargs.keys()),
                        }

                        self.traces.append(trace_record)
                        self.logger.debug(f"📊 Traced {graph_name} execution: {trace_record['duration_ms']:.1f}ms")

                        return result

                    except Exception as e:
                        # Record failed execution
                        trace_record = {
                            **metadata,
                            "function": func.__name__,
                            "status": "error",
                            "error": str(e),
                            "error_type": e.__class__.__name__,
                            "duration_ms": (datetime.now(UTC) - start_time).total_seconds() * 1000,
                        }

                        self.traces.append(trace_record)
                        self.logger.warning(f"📊 Traced {graph_name} error: {e}")

                        raise

            return wrapper

        return decorator

    def trace_tool_usage(self, tool_name: str):
        """
        Decorator for tracing tool usage.

        Args:
            tool_name: Name of the tool being used

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            if not self.enabled:
                return func

            @wraps(func)
            def wrapper(*args, **kwargs):
                metadata = {"tool_name": tool_name, "timestamp": datetime.now(UTC).isoformat()}

                if LANGSMITH_AVAILABLE and self.langsmith_client:

                    @traceable(name=f"tool_{tool_name}", project_name=self.project_name, tags=[tool_name, "tool"])
                    def traced_tool_execution(*args, **kwargs):
                        return func(*args, **kwargs)

                    return traced_tool_execution(*args, **kwargs)
                else:
                    # Local tracing
                    start_time = datetime.now(UTC)

                    try:
                        result = func(*args, **kwargs)

                        trace_record = {
                            **metadata,
                            "function": func.__name__,
                            "status": "success",
                            "duration_ms": (datetime.now(UTC) - start_time).total_seconds() * 1000,
                        }

                        self.traces.append(trace_record)
                        return result

                    except Exception as e:
                        trace_record = {
                            **metadata,
                            "function": func.__name__,
                            "status": "error",
                            "error": str(e),
                            "error_type": e.__class__.__name__,
                            "duration_ms": (datetime.now(UTC) - start_time).total_seconds() * 1000,
                        }

                        self.traces.append(trace_record)
                        raise

            return wrapper

        return decorator

    def trace_memory_operation(self, operation: str):
        """
        Decorator for tracing memory operations.

        Args:
            operation: Name of the memory operation

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            if not self.enabled:
                return func

            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = datetime.now(UTC)

                try:
                    result = func(*args, **kwargs)

                    if self.enabled:
                        trace_record = {
                            "operation": operation,
                            "timestamp": start_time.isoformat(),
                            "function": func.__name__,
                            "status": "success",
                            "duration_ms": (datetime.now(UTC) - start_time).total_seconds() * 1000,
                        }

                        # Add memory-specific metrics if available
                        if hasattr(args[0], "get_memory_stats"):
                            trace_record["memory_stats"] = args[0].get_memory_stats()

                        self.traces.append(trace_record)

                    return result

                except Exception as e:
                    if self.enabled:
                        trace_record = {
                            "operation": operation,
                            "timestamp": start_time.isoformat(),
                            "function": func.__name__,
                            "status": "error",
                            "error": str(e),
                            "error_type": e.__class__.__name__,
                            "duration_ms": (datetime.now(UTC) - start_time).total_seconds() * 1000,
                        }
                        self.traces.append(trace_record)

                    raise

            return wrapper

        return decorator

    def trace_decision_event(self, name: str, metadata: dict[str, Any], event: str = "decision_made") -> None:
        """
        Record a decision event for debugging and analysis.

        Args:
            name: Name of the decision span/event.
            metadata: Metadata to associate with the decision.
            event: Event label (e.g., decision_made, max_cycles_warning).
        """
        if not self.enabled:
            return

        trace_record = {
            "type": "decision",
            "name": name,
            "event": event,
            "timestamp": datetime.now(UTC).isoformat(),
            **metadata,
        }

        self.traces.append(trace_record)
        self.logger.debug(f"📊 Traced decision event {name}: {event}")

    def log_metric(self, name: str, value: Any, tags: dict[str, str] | None = None):
        """
        Log a custom metric.

        Args:
            name: Metric name
            value: Metric value
            tags: Optional tags for the metric
        """
        if not self.enabled:
            return

        metric_record = {
            "type": "metric",
            "name": name,
            "value": value,
            "tags": tags or {},
            "timestamp": datetime.now(UTC).isoformat(),
        }

        self.traces.append(metric_record)
        self.logger.debug(f"📊 Metric: {name} = {value}")

    def log_event(self, name: str, metadata: dict[str, Any] | None = None):
        """
        Log a custom event with structured metadata.

        Args:
            name: Event name
            metadata: Optional metadata payload
        """
        if not self.enabled:
            return

        event_record = {
            "type": "event",
            "name": name,
            "metadata": metadata or {},
            "timestamp": datetime.now(UTC).isoformat(),
        }

        self.traces.append(event_record)
        self.logger.info(f"📊 Event: {name}")

    def log_span(self, name: str, metadata: dict[str, Any] | None = None):
        """
        Log a lightweight span with structured metadata.

        Args:
            name: Span name
            metadata: Optional metadata payload
        """
        if not self.enabled:
            return

        span_record = {
            "type": "span",
            "name": name,
            "metadata": metadata or {},
            "timestamp": datetime.now(UTC).isoformat(),
        }

        self.traces.append(span_record)
        self.logger.info(f"📊 Span: {name}")

    def start_run(
        self, run_name: str, ticket_id: str | None = None, inputs: dict[str, Any] | None = None
    ) -> str | None:
        """
        Start a new run for tracking.

        Args:
            run_name: Name of the run
            ticket_id: Optional ticket ID
            inputs: Optional input data

        Returns:
            Run ID if tracing is enabled
        """
        if not self.enabled:
            return None

        run_id = f"{run_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        run_record = {
            "type": "run_start",
            "run_id": run_id,
            "run_name": run_name,
            "ticket_id": ticket_id,
            "inputs": inputs,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        self.traces.append(run_record)
        self.logger.info(f"📊 Started run: {run_name} (ID: {run_id})")

        return run_id

    def end_run(self, run_id: str, outputs: dict[str, Any] | None = None, error: str | None = None):
        """
        End a run.

        Args:
            run_id: Run ID from start_run
            outputs: Optional output data
            error: Optional error message if run failed
        """
        if not self.enabled or not run_id:
            return

        run_record = {
            "type": "run_end",
            "run_id": run_id,
            "outputs": outputs,
            "error": error,
            "status": "error" if error else "success",
            "timestamp": datetime.now(UTC).isoformat(),
        }

        self.traces.append(run_record)
        status = "FAILED" if error else "COMPLETED"
        self.logger.info(f"📊 {status} run: {run_id}")

    def get_traces(self, trace_type: str | None = None, since: datetime | None = None) -> list[dict[str, Any]]:
        """
        Get recorded traces.

        Args:
            trace_type: Optional filter by trace type
            since: Optional filter by timestamp

        Returns:
            List of matching trace records
        """
        traces = self.traces

        if trace_type:
            traces = [t for t in traces if t.get("type") == trace_type]

        if since:
            since_iso = since.isoformat()
            traces = [t for t in traces if t.get("timestamp", "") >= since_iso]

        return traces

    def get_metrics_summary(self) -> dict[str, Any]:
        """
        Get summary of collected metrics and traces.

        Returns:
            Dictionary with trace statistics
        """
        total_traces = len(self.traces)

        # Count by type
        type_counts = {}
        for trace in self.traces:
            trace_type = trace.get("type", "unknown")
            type_counts[trace_type] = type_counts.get(trace_type, 0) + 1

        # Count successes vs errors
        success_count = len([t for t in self.traces if t.get("status") == "success"])
        error_count = len([t for t in self.traces if t.get("status") == "error"])

        # Calculate average duration for timed operations
        durations = [t.get("duration_ms", 0) for t in self.traces if "duration_ms" in t]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "enabled": self.enabled,
            "langsmith_available": LANGSMITH_AVAILABLE,
            "project_name": self.project_name,
            "total_traces": total_traces,
            "type_counts": type_counts,
            "success_count": success_count,
            "error_count": error_count,
            "error_rate": error_count / total_traces if total_traces > 0 else 0,
            "avg_duration_ms": avg_duration,
        }

    def export_traces(self, filepath: str):
        """
        Export traces to a JSON file.

        Args:
            filepath: Path to save traces
        """
        export_data = {
            "metadata": {
                "export_timestamp": datetime.now(UTC).isoformat(),
                "tracer_config": {"enabled": self.enabled, "project_name": self.project_name},
            },
            "summary": self.get_metrics_summary(),
            "traces": self.traces,
        }

        with open(filepath, "w") as f:
            json.dump(export_data, f, indent=2)

        self.logger.info(f"📁 Exported {len(self.traces)} traces to {filepath}")

    def clear_traces(self) -> int:
        """
        Clear all stored traces.

        Returns:
            Number of traces cleared
        """
        cleared_count = len(self.traces)
        self.traces.clear()

        if cleared_count > 0:
            self.logger.info(f"🧹 Cleared {cleared_count} traces")

        return cleared_count


# Global tracer instance (lazy initialization to avoid import side effects)
_global_tracer: CCETracer | None = None


def get_global_tracer() -> CCETracer:
    """Get the global tracer instance (lazy initialized)."""
    global _global_tracer
    if _global_tracer is None:
        _global_tracer = CCETracer()
    return _global_tracer


def attach_cycle_result_metadata(cycle_result: Any) -> None:
    """Attach CycleResult summary data to the current LangSmith span metadata."""
    if cycle_result is None:
        return

    if hasattr(cycle_result, "to_summary"):
        summary = cycle_result.to_summary()
    elif isinstance(cycle_result, dict):
        summary = cycle_result
    else:
        summary = {"cycle_summary": str(cycle_result)}

    if not summary:
        return

    if not LANGSMITH_AVAILABLE:
        return

    try:
        from langsmith import run_helpers

        current_context = run_helpers.get_tracing_context() or {}
        current_metadata = dict(current_context.get("metadata") or {})
        cycle_results = list(current_metadata.get("cycle_results", []))
        cycle_results.append(summary)
        current_metadata["cycle_results"] = cycle_results
        run_helpers._set_tracing_context({"metadata": current_metadata})
    except Exception:
        logging.getLogger(__name__).debug("Failed to attach cycle result metadata", exc_info=True)


def attach_cycle_metrics_metadata(cycle_metrics: Any) -> None:
    """Attach CycleMetrics summary data to the current LangSmith span metadata."""
    if cycle_metrics is None:
        return

    if hasattr(cycle_metrics, "to_dict"):
        summary = cycle_metrics.to_dict()
    elif isinstance(cycle_metrics, dict):
        summary = cycle_metrics
    else:
        summary = {"cycle_metrics": str(cycle_metrics)}

    if not summary:
        return

    if not LANGSMITH_AVAILABLE:
        return

    try:
        from langsmith import run_helpers

        current_context = run_helpers.get_tracing_context() or {}
        current_metadata = dict(current_context.get("metadata") or {})
        cycle_metrics_list = list(current_metadata.get("cycle_metrics", []))
        cycle_metrics_list.append(summary)
        current_metadata["cycle_metrics"] = cycle_metrics_list
        run_helpers._set_tracing_context({"metadata": current_metadata})
    except Exception:
        logging.getLogger(__name__).debug("Failed to attach cycle metrics metadata", exc_info=True)


# =============================================================================
# Unified Tracing Context Manager (Ticket #84)
# =============================================================================


class UnifiedTraceContext:
    """
    Context manager for creating a single root trace per CCE run.

    This ensures all operations (planning, execution, tool calls) appear as
    nested children under a single root trace in LangSmith.

    Usage:
        async with unified_trace_context(ticket.number, ticket.url) as ctx:
            result = await agent.process_ticket(ticket)
            ctx.add_metadata("pr_url", result.pr_url)
    """

    def __init__(
        self,
        ticket_number: int,
        ticket_url: str,
        project_name: str = "cce-agent",
        extra_tags: list[str] | None = None,
        extra_metadata: dict[str, Any] | None = None,
    ):
        self.ticket_number = ticket_number
        self.ticket_url = ticket_url
        self.project_name = project_name
        self.tags = ["ticket-processing", f"ticket-{ticket_number}"] + (extra_tags or [])
        self.metadata = {"ticket_url": ticket_url, "ticket_number": ticket_number, **(extra_metadata or {})}
        self._context = None
        self._root_run = None
        self._client = None
        self._enabled = False
        self.logger = logging.getLogger(__name__)

    def _is_tracing_enabled(self) -> bool:
        if not LANGSMITH_AVAILABLE:
            return False
        try:
            from langsmith import utils as ls_utils

            return bool(ls_utils.tracing_is_enabled())
        except Exception:
            return False

    def _get_root_name(self) -> str:
        return f"{self.project_name}/ticket-{self.ticket_number}"

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
        """Enter the unified trace context."""
        if not self._is_tracing_enabled():
            return self

        try:
            from langsmith import Client, run_helpers, run_trees

            # Add git info to metadata
            self.metadata.update(self._get_git_info())

            # Create and post the root run
            self._client = Client()
            self._root_run = run_trees.RunTree(
                name=self._get_root_name(),
                run_type="chain",
                inputs={"ticket_number": self.ticket_number, "ticket_url": self.ticket_url},
                project_name=self.project_name,
                tags=self.tags,
                extra={"metadata": self.metadata},
                client=self._client,
            )
            try:
                self._root_run.post()
            except Exception as e:
                self.logger.warning(f"Failed to post unified root run: {e}")

            # Create the tracing context with root parent
            self._context = run_helpers.tracing_context(
                project_name=self.project_name,
                tags=self.tags,
                metadata=self.metadata,
                parent=self._root_run,
                client=self._client,
                enabled=True,
            )
            self._context.__enter__()
            self._enabled = True

            self.logger.info(
                f"📊 Unified trace started for ticket #{self.ticket_number} (project: {self.project_name})"
            )
        except Exception as e:
            self.logger.warning(f"Failed to start unified trace: {e}")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the unified trace context."""
        if self._context is not None:
            try:
                self._context.__exit__(exc_type, exc_val, exc_tb)
            except Exception as e:
                self.logger.warning(f"Error closing unified trace context: {e}")

        if self._root_run is not None:
            try:
                error_message = str(exc_val) if exc_val is not None else None
                self._root_run.add_metadata(self.metadata)
                self._root_run.end(error=error_message)
                self._root_run.patch()

                if exc_type is not None:
                    self.logger.warning(
                        f"📊 Unified trace ended with error for ticket #{self.ticket_number}: {exc_val}"
                    )
                else:
                    self.logger.info(f"📊 Unified trace completed for ticket #{self.ticket_number}")
            except Exception as e:
                self.logger.warning(f"Error finalizing unified trace: {e}")

        return False  # Don't suppress exceptions

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the current trace and tracing context."""
        self.metadata[key] = value

        if self._root_run is not None:
            self._root_run.add_metadata({key: value})

        if self._context is not None:
            try:
                from langsmith import run_helpers

                current_context = run_helpers.get_tracing_context()
                current_metadata = dict(current_context.get("metadata") or {})
                current_metadata[key] = value
                run_helpers._set_tracing_context({"metadata": current_metadata})
            except Exception as e:
                self.logger.debug(f"Failed to update tracing context metadata: {e}")


def unified_trace_context(
    ticket_number: int,
    ticket_url: str,
    project_name: str = "cce-agent",
    extra_tags: list[str] | None = None,
    extra_metadata: dict[str, Any] | None = None,
) -> UnifiedTraceContext:
    """
    Create a unified tracing context for a CCE run.

    This ensures a single root trace is created in LangSmith with all
    operations as nested children.

    Args:
        ticket_number: GitHub issue number
        ticket_url: Full URL to the GitHub issue
        project_name: LangSmith project name
        extra_tags: Additional tags for the trace
        extra_metadata: Additional metadata for the trace

    Returns:
        UnifiedTraceContext async context manager

    Example:
        async with unified_trace_context(123, "https://github.com/...") as ctx:
            result = await agent.process_ticket(ticket)
            ctx.add_metadata("pr_url", result.pr_url)
    """
    return UnifiedTraceContext(
        ticket_number=ticket_number,
        ticket_url=ticket_url,
        project_name=project_name,
        extra_tags=extra_tags,
        extra_metadata=extra_metadata,
    )


def configure_tracing(enabled: bool, project_name: str = "cce-agent"):
    """
    Configure global tracing settings.

    Args:
        enabled: Whether to enable tracing
        project_name: LangSmith project name
    """
    global _global_tracer
    _global_tracer = CCETracer(enabled=enabled, project_name=project_name)


# Convenience decorators using global tracer
def trace_graph(graph_name: str, ticket_id: str | None = None):
    """Trace graph execution using global tracer."""
    return get_global_tracer().trace_graph_execution(graph_name, ticket_id)


def trace_tool(tool_name: str):
    """Trace tool usage using global tracer."""
    return get_global_tracer().trace_tool_usage(tool_name)


def trace_memory(operation: str):
    """Trace memory operation using global tracer."""
    return get_global_tracer().trace_memory_operation(operation)
