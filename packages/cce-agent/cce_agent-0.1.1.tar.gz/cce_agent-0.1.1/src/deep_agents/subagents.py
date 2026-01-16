"""
CCE Deep Agent Sub-Agents.

This module defines specialized sub-agents for the CCE system,
converting existing stakeholder expertise into deep agents sub-agents.
"""

from deepagents import SubAgent  # SubAgent is re-exported from deepagents

# from .prompt_manager import context_engineering_prompt

# Note: In deepagents 0.3.x, SubAgent is a class from deepagents.middleware.subagents
# and uses the "system_prompt" field for per-subagent prompts.

context_engineering_agent: SubAgent = {
    "name": "context-engineer",
    "description": "Expert in context management, memory systems, semantic optimization, and LLM-based code editing",
    "system_prompt": "",
    "tools": ["sync_to_disk"],
}


# General-Purpose Sub-Agent (Enhanced from Deep Agents patterns)
# from .prompt_manager import general_purpose_prompt

general_purpose_agent: SubAgent = {
    "name": "general-purpose",
    "description": "General-purpose sub-agent with same capabilities as main agent, providing fallback functionality",
    "system_prompt": "",
    "tools": [
        "sync_to_disk",
        # Planning tools
        "create_plan",
        "update_plan",
        "get_plan_status",
        "list_plans",
        "set_active_plan",
        "get_active_plan",
        # ADR tools
        "create_adr_tool",
        "list_adrs_tool",
        "get_adr_tool",
        "adr_summary_tool",
        # LangGraph interrupt tools
        "trigger_quality_interrupt_tool",
        "trigger_architectural_decision_interrupt_tool",
        "generate_quality_assessment",
        # Validation tools
        "validate_code",
        "run_linting",
        "run_tests",
        "check_syntax",
        # Cycle tools
        "signal_cycle_complete",
        # Bash tools
        "execute_bash_command",
        "advanced_shell_command",
        "check_system_status",
    ],
}


# Planning Sub-Agent (Enhanced from Deep Agents patterns)
# from .prompt_manager import planning_prompt

planning_agent: SubAgent = {
    "name": "planning-specialist",
    "description": "Expert in task planning, progress tracking, and context preservation",
    "system_prompt": "",
    "tools": [
        # Core planning tools
        "create_plan",
        "update_plan",
        "get_plan_status",
        "list_plans",
        "set_active_plan",
        "get_active_plan",
    ],
}
