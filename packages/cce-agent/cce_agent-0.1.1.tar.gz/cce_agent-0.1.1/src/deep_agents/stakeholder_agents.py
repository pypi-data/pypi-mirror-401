"""
CCE Deep Agent Stakeholder Sub-Agents.

This module converts all 5 stakeholder subgraphs to deep agents sub-agents
with LLM-based code editing capabilities, preserving their domain expertise
while enabling enhanced coordination patterns.
"""

from deepagents import SubAgent

# from .prompt_manager import (
#     aider_integration_prompt,
#     context_engineering_prompt,
#     langgraph_architecture_prompt,
#     production_stability_prompt,
#     developer_experience_prompt
# )

aider_integration_agent: SubAgent = {
    "name": "aider-specialist",
    "description": "Expert in code analysis, repository mapping, and LLM-based code editing",
    "prompt": "",
    "tools": [
        # Validation tools for code quality
        "validate_code",
        "run_linting",
        "run_tests",
        "check_syntax",
        # Bash tools for system operations
        "execute_bash_command",
        "advanced_shell_command",
    ],
}


# Context Engineering Sub-Agent (already exists, but enhanced)

context_engineering_agent: SubAgent = {
    "name": "context-engineer",
    "description": "Expert in context management, memory systems, semantic optimization, and LLM-based code editing",
    "prompt": "",
    "tools": [
        # Bash tools for analysis and system operations
        "execute_bash_command",
        "check_system_status",
    ],
}


# LangGraph Architecture Sub-Agent

langgraph_architecture_agent: SubAgent = {
    "name": "langgraph-architect",
    "description": "Expert in LangGraph orchestration, state management, and multi-agent coordination",
    "prompt": "",
    "tools": [
        # Planning tools for complex architecture tasks
        "create_plan",
        "update_plan",
        "get_plan_status",
        # Validation tools for architecture validation
        "validate_code",
        "check_syntax",
    ],
}


# Production Stability Sub-Agent

production_stability_agent: SubAgent = {
    "name": "stability-specialist",
    "description": "Expert in operational reliability, performance optimization, and error handling",
    "prompt": "",
    "tools": [
        # Validation and testing tools for reliability
        "validate_code",
        "run_linting",
        "run_tests",
        "check_syntax",
        # Bash tools for system monitoring and analysis
        "execute_bash_command",
        "advanced_shell_command",
        "check_system_status",
    ],
}


# Developer Experience Sub-Agent

developer_experience_agent: SubAgent = {
    "name": "developer-experience-specialist",
    "description": "Expert in API design, debugging, documentation, and maintainability",
    "prompt": "",
    "tools": [
        # Validation tools for code quality
        "validate_code",
        "run_linting",
        "run_tests",
        "check_syntax",
        # Bash tools for development operations
        "execute_bash_command",
        "check_system_status",
    ],
}


# Export all stakeholder agents
ALL_STAKEHOLDER_AGENTS = [
    context_engineering_agent,
    langgraph_architecture_agent,
    production_stability_agent,
    developer_experience_agent,
]

# Agent lookup by name
STAKEHOLDER_AGENTS_BY_NAME = {agent["name"]: agent for agent in ALL_STAKEHOLDER_AGENTS}
