import os
import sys

import pytest
from langsmith import run_helpers, run_trees, traceable

# Add project to path
sys.path.insert(0, os.path.abspath("."))

from src.observability.tracers import LANGSMITH_AVAILABLE, UnifiedTraceContext


@pytest.mark.asyncio
async def test_unified_trace_context_respects_tracing_disabled(monkeypatch):
    if not LANGSMITH_AVAILABLE:
        pytest.skip("LangSmith not available in this environment.")

    monkeypatch.setattr("langsmith.utils.tracing_is_enabled", lambda ctx=None: False)

    post_called = {"called": False}

    def fake_post(self, exclude_child_runs=True):
        post_called["called"] = True

    monkeypatch.setattr(run_trees.RunTree, "post", fake_post, raising=True)

    ctx = UnifiedTraceContext(ticket_number=1, ticket_url="https://github.com/example/repo/issues/1")

    async with ctx:
        assert ctx._root_run is None
        assert ctx._context is None

    assert post_called["called"] is False


@pytest.mark.asyncio
async def test_unified_trace_context_creates_root_and_propagates_metadata(monkeypatch):
    if not LANGSMITH_AVAILABLE:
        pytest.skip("LangSmith not available in this environment.")

    monkeypatch.setattr("langsmith.utils.tracing_is_enabled", lambda ctx=None: True)

    posted_runs = []

    def fake_post(self, exclude_child_runs=True):
        posted_runs.append(self)

    monkeypatch.setattr(run_trees.RunTree, "post", fake_post, raising=True)
    monkeypatch.setattr(run_trees.RunTree, "patch", lambda self, exclude_inputs=False: None, raising=True)

    ctx = UnifiedTraceContext(
        ticket_number=123, ticket_url="https://github.com/example/repo/issues/123", project_name="cce-agent"
    )

    @traceable(name="child-operation")
    def child_operation():
        return run_helpers.get_current_run_tree()

    async with ctx:
        ctx.add_metadata("pr_url", "https://github.com/example/repo/pull/1")
        run_tree = child_operation()

        assert run_tree is not None
        assert run_tree.parent_run_id == ctx._root_run.id

        tracing_metadata = run_helpers.get_tracing_context().get("metadata") or {}
        assert tracing_metadata["pr_url"] == "https://github.com/example/repo/pull/1"
        assert ctx._root_run.extra["metadata"]["pr_url"] == "https://github.com/example/repo/pull/1"

    assert ctx._root_run in posted_runs
