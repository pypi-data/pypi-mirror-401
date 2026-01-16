from pathlib import Path
import importlib


def test_deep_agent_filesystem_root_propagation(monkeypatch, tmp_path):
    module = importlib.import_module("src.deep_agents.cce_deep_agent")
    captured_roots = []

    class DummyAgent:
        def with_config(self, config):
            return self

        async def ainvoke(self, *args, **kwargs):
            return {}

    class DummyMiddleware:
        def __init__(self, *args, **kwargs):
            self.tools = []

    def fake_create_filesystem_middleware(*, workspace_root, **kwargs):
        captured_roots.append(Path(workspace_root).resolve())
        return DummyMiddleware()

    monkeypatch.setattr(module, "create_filesystem_middleware", fake_create_filesystem_middleware)
    monkeypatch.setattr(module, "create_cce_summarization_middleware", lambda llm: DummyMiddleware())
    monkeypatch.setattr(module, "create_agent", lambda *args, **kwargs: DummyAgent())
    monkeypatch.setattr(module, "TodoListMiddleware", DummyMiddleware)
    monkeypatch.setattr(module, "SubAgentMiddleware", DummyMiddleware)
    monkeypatch.setattr(module, "PatchToolCallsMiddleware", DummyMiddleware)
    monkeypatch.setattr(module, "GraphIntegrationMiddleware", DummyMiddleware)
    monkeypatch.setattr(module, "CCEMemoryMiddleware", DummyMiddleware)
    monkeypatch.setattr(module, "get_cce_deep_agent_tools", lambda: [])
    monkeypatch.setattr(module, "_resolve_subagent_tools", lambda subagent, tool_by_name, logger: subagent)

    module.createCCEDeepAgent(
        llm=object(),
        enable_context_auditing=False,
        enable_post_model_hook_manager=False,
        enable_prompt_cache=False,
        enable_memory_persistence=False,
        workspace_root=str(tmp_path),
    )

    expected_root = Path(tmp_path).resolve()
    assert captured_roots == [expected_root, expected_root]
