"""Tool registration helpers for the legacy agent."""

from __future__ import annotations

from langchain.tools import BaseTool

from src.environments.base import BaseEnvironment
from src.graphs.aider_graph import AiderGraph
from src.tools.aider.wrapper import AiderctlWrapper
from src.tools.code_analyzer import CodeAnalyzer
from src.tools.edit_engine import EditEngine
from src.tools.git_ops import GitOps
from src.tools.langchain_tool_adapters import create_langchain_tool_adapters
from src.tools.shell_runner import ShellRunner
from src.tools.validation.runner import ValidationRunner


def initialize_tooling(
    workspace_env: BaseEnvironment,
) -> tuple[ShellRunner, EditEngine, GitOps, CodeAnalyzer, list[BaseTool], list[BaseTool]]:
    """Create tool services and adapter lists for the agent."""
    workspace_root = getattr(workspace_env, "workspace_root", None)
    from src.config_loader import get_config

    include_aider_tools = get_config(workspace_root=workspace_root).defaults.use_aider
    shell_runner = ShellRunner(workspace_root)
    git_ops = GitOps(shell_runner)
    code_analyzer = CodeAnalyzer(shell_runner)
    aider_wrapper = AiderctlWrapper(cwd=workspace_root, strict_mode=False)
    validation_runner = ValidationRunner(aider_wrapper)
    aider_graph = AiderGraph(
        aider_wrapper=aider_wrapper,
        git_ops=git_ops,
        validation_runner=validation_runner,
        enable_semantic_ranking=False,
    )
    edit_engine = EditEngine(
        workspace_env,
        shell_runner=shell_runner,
        code_analyzer=code_analyzer,
        git_ops=git_ops,
        aider_wrapper=aider_wrapper,
    )

    all_tools = create_langchain_tool_adapters(
        shell_runner=shell_runner,
        edit_engine=edit_engine,
        git_ops=git_ops,
        code_analyzer=code_analyzer,
        aider_wrapper=aider_wrapper,
        aider_graph=aider_graph,
        include_aider_tools=include_aider_tools,
    )
    planning_tools = [tool for tool in all_tools if tool.name != "write_to_file"]

    return shell_runner, edit_engine, git_ops, code_analyzer, all_tools, planning_tools
