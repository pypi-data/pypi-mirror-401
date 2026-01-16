import importlib

MODULES_TO_IMPORT = [
    "src.agent",
    "src.agent.core",
    "src.agent.state",
    "src.deep_agents",
    "src.context_resolver",
    "src.prompt_cache",
    "src.observability.tracers",
    "src.deep_agents.prompt_manager",
    "src.deep_agents.mcp_integration",
    "src.deep_agents.planning_tool",
    "src.deep_agents.command_safety",
    "src.tools.openswe.treesitter_tools",
    "src.tools.commands.discover_target_files",
    "src.tools.openswe.web_tools",
    "src.tools.openswe.workflow_tools",
    "src.config.execution_limits",
]


def test_imports_are_clean() -> None:
    for module_name in MODULES_TO_IMPORT:
        importlib.import_module(module_name)
