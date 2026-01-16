import os
import sys
from datetime import datetime, timedelta

import pytest

sys.path.insert(0, os.path.abspath("."))

from src.models import CycleResult, ToolCall
from src.observability.cycle_metrics import CycleMetrics, CycleMetricsCollector
from src.observability.tracers import LANGSMITH_AVAILABLE, attach_cycle_metrics_metadata


def test_cycle_metrics_collector_records_cycle():
    start_time = datetime(2025, 1, 1, 0, 0, 0)
    end_time = start_time + timedelta(seconds=90)
    cycle_result = CycleResult(
        cycle_number=1,
        status="success",
        orientation="focus",
        start_time=start_time,
        end_time=end_time,
        messages_count=3,
        tool_calls=[
            ToolCall(tool_name="rg", arguments={"query": "cycle"}),
            ToolCall(tool_name="pytest", arguments={"args": ["-k", "cycle"]}),
        ],
        final_summary="Cycle completed",
        step_count=2,
        tests_run=4,
        tests_passed=4,
        tests_failed=0,
        soft_limit=20,
        soft_limit_reached=False,
        steps_in_main_phase=2,
        steps_in_wrap_up_phase=0,
    )
    cycle_result.duration_seconds = (end_time - start_time).total_seconds()

    collector = CycleMetricsCollector()
    collector.start_cycle(1, orientation="focus", start_time=start_time)
    metrics = collector.record_cycle(cycle_result)

    assert metrics.duration_seconds == 90.0
    assert metrics.tool_call_count == 2
    assert metrics.tests_run == 4

    payload = collector.to_dict()
    assert payload["cycle_metrics"][0]["cycle_number"] == 1
    assert payload["cycle_metrics_summary"]["cycles"] == 1


@pytest.mark.asyncio
async def test_attach_cycle_metrics_metadata_updates_context():
    if not LANGSMITH_AVAILABLE:
        pytest.skip("LangSmith not available in this environment.")

    from langsmith import run_helpers

    metrics = CycleMetrics(
        cycle_number=2,
        status="success",
        orientation="focus",
        start_time=datetime(2025, 1, 1),
        end_time=datetime(2025, 1, 1, 0, 1),
        duration_seconds=60.0,
        message_count=3,
        tool_call_count=1,
        step_count=1,
        soft_limit=20,
        soft_limit_reached=False,
        steps_in_main_phase=1,
        steps_in_wrap_up_phase=0,
        tests_run=1,
        tests_passed=1,
        tests_failed=0,
        linting_passed=True,
    )

    with run_helpers.tracing_context(project_name="cce-agent"):
        attach_cycle_metrics_metadata(metrics)
        metadata = run_helpers.get_tracing_context().get("metadata") or {}

    assert metadata["cycle_metrics"][0]["cycle_number"] == 2
