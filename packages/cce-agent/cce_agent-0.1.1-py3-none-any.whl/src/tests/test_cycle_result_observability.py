import json
import os
import sys
from datetime import datetime

import pytest

sys.path.insert(0, os.path.abspath("."))

from src.models import CycleResult, TokenUsage, ToolCall
from src.observability.tracers import LANGSMITH_AVAILABLE, attach_cycle_result_metadata


def test_cycle_result_to_dict_is_json_serializable():
    cycle = CycleResult(
        cycle_number=1,
        status="success",
        orientation="test",
        start_time=datetime(2025, 1, 1),
        end_time=datetime(2025, 1, 1, 0, 1),
        messages_count=2,
        tool_calls=[ToolCall(tool_name="rg", arguments={"query": "cycle"})],
        token_usage=[
            TokenUsage(
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                model_name="gpt-4o",
                operation="test",
            )
        ],
        final_summary="Cycle completed",
        cycle_summary="Cycle completed",
        step_count=1,
        prompt_tokens=10,
        completion_tokens=5,
    )

    payload = cycle.to_dict()
    json.dumps(payload)


def test_cycle_result_to_summary_uses_final_summary_fallback():
    cycle = CycleResult(
        cycle_number=2,
        status="success",
        orientation="test",
        start_time=datetime(2025, 1, 1),
        final_summary="Final summary",
        cycle_summary="",
    )

    summary = cycle.to_summary()
    assert summary["cycle_summary"] == "Final summary"


@pytest.mark.asyncio
async def test_attach_cycle_result_metadata_updates_context():
    if not LANGSMITH_AVAILABLE:
        pytest.skip("LangSmith not available in this environment.")

    from langsmith import run_helpers

    cycle = CycleResult(
        cycle_number=3,
        status="success",
        orientation="test",
        start_time=datetime(2025, 1, 1),
        final_summary="Summary",
    )

    with run_helpers.tracing_context(project_name="cce-agent"):
        attach_cycle_result_metadata(cycle)
        metadata = run_helpers.get_tracing_context().get("metadata") or {}

    assert metadata["cycle_results"][0]["cycle_number"] == 3
