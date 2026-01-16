import pytest
from pathlib import Path

import importlib


class DummyDiscovery:
    seen_roots: list[str] = []

    def __init__(self, workspace_root: str = ".", *args, **kwargs):
        self.seen_roots.append(workspace_root)

    async def _get_virtual_filesystem(self) -> dict[str, str]:
        return {}

    def _filter_file_summaries(self, virtual_files: dict[str, str]) -> dict[str, str]:
        return {}

    async def discover_relevant_files(self, *args, **kwargs) -> dict[str, object]:
        return {"discovered_files": [], "reasoning": "", "confidence": 0.0}


@pytest.mark.asyncio
async def test_research_codebase_uses_workspace_root(monkeypatch, tmp_path):
    DummyDiscovery.seen_roots = []
    research_module = importlib.import_module("src.tools.commands.research_codebase")
    monkeypatch.setattr(research_module, "IntelligentFileDiscovery", DummyDiscovery)

    await research_module.research_codebase.ainvoke(
        {
            "research_question": "test workspace root",
            "context": "",
            "workspace_root": str(tmp_path),
        }
    )

    assert DummyDiscovery.seen_roots
    expected = Path(tmp_path).resolve()
    assert all(Path(root).resolve() == expected for root in DummyDiscovery.seen_roots)


@pytest.mark.asyncio
async def test_discover_target_files_uses_workspace_root(monkeypatch, tmp_path):
    DummyDiscovery.seen_roots = []
    discover_module = importlib.import_module("src.tools.commands.discover_target_files")
    monkeypatch.setattr(discover_module, "IntelligentFileDiscovery", DummyDiscovery)

    await discover_module.discover_target_files.ainvoke(
        {
            "plan_topic": "test workspace root",
            "workspace_root": str(tmp_path),
        }
    )

    assert DummyDiscovery.seen_roots
    expected = Path(tmp_path).resolve()
    assert all(Path(root).resolve() == expected for root in DummyDiscovery.seen_roots)
