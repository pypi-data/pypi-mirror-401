import json
import os
import sys

import pytest
from langchain_core.messages import AIMessage, HumanMessage

sys.path.insert(0, os.path.abspath("."))

from src.models import ToolCall
from src.observability.dual_write import DualWriteTraceContext, LocalTraceWriter


def _read_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def test_local_trace_writer_outputs(tmp_path):
    writer = LocalTraceWriter(base_path=str(tmp_path), ticket_number=85)
    writer.initialize({"ticket_url": "https://example.com/issue/85"})

    writer.write_message_entry({"role": "human", "content": "hello", "phase": "planning"})
    writer.write_tool_call_entry({"tool_name": "rg", "arguments": {"query": "dual write"}, "phase": "planning"})
    writer.update_metrics({"total_tokens": 123, "phases": [{"name": "planning", "tokens": 123}]})
    writer.finalize({"status": "completed", "duration_seconds": 1.2})

    run_dir = tmp_path / writer.run_id
    assert (run_dir / "metadata.json").exists()
    assert (run_dir / "messages.jsonl").exists()
    assert (run_dir / "tool_calls.jsonl").exists()
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "summary.json").exists()

    messages = _read_jsonl(run_dir / "messages.jsonl")
    assert len(messages) == 1
    assert messages[0]["content"] == "hello"

    tool_calls = _read_jsonl(run_dir / "tool_calls.jsonl")
    assert len(tool_calls) == 1
    assert tool_calls[0]["tool_name"] == "rg"

    summary = json.loads((run_dir / "summary.json").read_text())
    assert summary["status"] == "completed"
    assert summary["tool_calls"]["total"] == 1
    assert summary["messages"]["total"] == 1


@pytest.mark.asyncio
async def test_dual_write_context_writes_local_trace(tmp_path, monkeypatch):
    monkeypatch.setenv("CCE_ENABLE_DUAL_WRITE", "true")

    async with DualWriteTraceContext(
        ticket_number=85,
        ticket_url="https://example.com/issue/85",
        local_storage_path=str(tmp_path),
        enable_langsmith=False,
        enable_local=True,
    ) as ctx:
        ctx.write_messages(
            [HumanMessage(content="plan"), AIMessage(content="done")],
            phase="planning",
        )
        ctx.write_tool_calls(
            [ToolCall(tool_name="rg", arguments={"query": "trace"})],
            phase="planning",
        )
        ctx.write_metrics({"total_tokens": 5})

    run_dirs = [path for path in tmp_path.iterdir() if path.is_dir()]
    assert len(run_dirs) == 1
    run_dir = run_dirs[0]

    messages = _read_jsonl(run_dir / "messages.jsonl")
    assert len(messages) == 2
    tool_calls = _read_jsonl(run_dir / "tool_calls.jsonl")
    assert len(tool_calls) == 1
    metrics = json.loads((run_dir / "metrics.json").read_text())
    assert metrics["total_tokens"] == 5
