from src.deep_agents.cce_deep_agent import get_cce_deep_agent_tools

REQUIRED_TESTING_TOOLS = {
    "run_tests",
    "run_linting",
    "check_syntax",
    "validate_code",
}


def test_testing_tools_available():
    """Verify testing tools are present in the deep agent tool list."""
    tool_names = {tool.name for tool in get_cce_deep_agent_tools() if hasattr(tool, "name")}
    missing = REQUIRED_TESTING_TOOLS - tool_names
    assert not missing, f"Missing testing tools: {sorted(missing)}"


def test_testing_tools_callable():
    """Verify testing tools expose an invoke method for execution."""
    tools = {tool.name: tool for tool in get_cce_deep_agent_tools() if hasattr(tool, "name")}
    for tool_name in REQUIRED_TESTING_TOOLS:
        tool = tools.get(tool_name)
        assert tool is not None, f"Tool {tool_name} not found"
        assert callable(getattr(tool, "invoke", None)) or callable(getattr(tool, "ainvoke", None)), (
            f"Tool {tool_name} is not callable"
        )
