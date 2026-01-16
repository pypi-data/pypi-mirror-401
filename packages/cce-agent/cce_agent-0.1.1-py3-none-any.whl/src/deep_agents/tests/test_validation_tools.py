import os
import sys
import types

from src.deep_agents.tools import validation
from src.workspace_context import set_workspace_root


def test_resolve_workspace_root_uses_workspace_context(tmp_path):
    set_workspace_root(str(tmp_path))
    try:
        assert validation._resolve_workspace_root() == str(tmp_path.resolve())
    finally:
        set_workspace_root(None)


def test_get_code_tools_instance_builds_components(monkeypatch, tmp_path):
    class FakeShellRunner:
        def __init__(self, workspace_root):
            self.workspace_root = workspace_root

    class FakeGitOps:
        def __init__(self, shell_runner):
            self.shell_runner = shell_runner

    class FakeLinting:
        def __init__(self, workspace_root):
            self.workspace_root = workspace_root

    class FakeTesting:
        def __init__(self, workspace_root):
            self.workspace_root = workspace_root

    class FakeLLM:
        def __init__(self, model, temperature, api_key):
            self.model = model
            self.temperature = temperature
            self.api_key = api_key

    class FakeCodeTools:
        def __init__(self, workspace_root, shell_runner, git_ops, linting, testing, editor_llm):
            self.workspace_root = workspace_root
            self.shell_runner = shell_runner
            self.git_ops = git_ops
            self.linting = linting
            self.testing = testing
            self.editor_llm = editor_llm

    monkeypatch.setattr(validation, "ShellRunner", FakeShellRunner)
    monkeypatch.setattr(validation, "GitOps", FakeGitOps)
    monkeypatch.setattr(validation, "LintingManager", FakeLinting)
    monkeypatch.setattr(validation, "FrameworkTestManager", FakeTesting)
    monkeypatch.setattr(validation, "CodeTools", FakeCodeTools)
    monkeypatch.setitem(sys.modules, "langchain_anthropic", types.SimpleNamespace(ChatAnthropic=FakeLLM))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    instance = validation.get_code_tools_instance(str(tmp_path))

    assert isinstance(instance, FakeCodeTools)
    assert isinstance(instance.shell_runner, FakeShellRunner)
    assert isinstance(instance.git_ops, FakeGitOps)
    assert instance.git_ops.shell_runner is instance.shell_runner
    assert instance.workspace_root == str(tmp_path.resolve())

def test_get_code_tools_instance_openai_fallback(monkeypatch, tmp_path):
    class FakeShellRunner:
        def __init__(self, workspace_root):
            self.workspace_root = workspace_root

    class FakeGitOps:
        def __init__(self, shell_runner):
            self.shell_runner = shell_runner

    class FakeLinting:
        def __init__(self, workspace_root):
            self.workspace_root = workspace_root

    class FakeTesting:
        def __init__(self, workspace_root):
            self.workspace_root = workspace_root

    class FakeOpenAI:
        def __init__(self, model, temperature):
            self.model = model
            self.temperature = temperature

    class FakeCodeTools:
        def __init__(self, workspace_root, shell_runner, git_ops, linting, testing, editor_llm):
            self.workspace_root = workspace_root
            self.shell_runner = shell_runner
            self.git_ops = git_ops
            self.linting = linting
            self.testing = testing
            self.editor_llm = editor_llm

    monkeypatch.setattr(validation, "ShellRunner", FakeShellRunner)
    monkeypatch.setattr(validation, "GitOps", FakeGitOps)
    monkeypatch.setattr(validation, "LintingManager", FakeLinting)
    monkeypatch.setattr(validation, "FrameworkTestManager", FakeTesting)
    monkeypatch.setattr(validation, "CodeTools", FakeCodeTools)
    monkeypatch.setitem(sys.modules, "langchain_openai", types.SimpleNamespace(ChatOpenAI=FakeOpenAI))
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai")

    instance = validation.get_code_tools_instance(str(tmp_path))

    assert isinstance(instance.editor_llm, FakeOpenAI)
