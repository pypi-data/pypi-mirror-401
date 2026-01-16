"""
Prompt Manager for CCE Deep Agent

This module centralizes all prompts for the CCE Deep Agent system,
providing a single source of truth for all prompt definitions.
"""

import logging

from src.prompts.manager import PromptManager

_PROMPT_MANAGER: PromptManager | None = None
_LOGGER = logging.getLogger(__name__)

_SYSTEM_PROMPT_FILES = [
    "identity/cce_identity.md",
    "tools/tool_descriptions.md",
    "frameworks/when_to_search.md",
    "frameworks/when_to_test.md",
    "frameworks/when_to_commit.md",
    "guardrails/approval_required.md",
    "guardrails/banned_commands.md",
]


def _load_system_prompt_sections() -> list[str]:
    sections: list[str] = []
    for relative_path in _SYSTEM_PROMPT_FILES:
        try:
            sections.append(get_prompt_manager().load_template(relative_path))
        except FileNotFoundError:
            _LOGGER.warning(f"System prompt section not found: {relative_path}")
    return sections


def get_prompt_manager() -> PromptManager:
    """Get the global prompt manager instance (lazy initialized)."""
    global _PROMPT_MANAGER
    if _PROMPT_MANAGER is None:
        _PROMPT_MANAGER = PromptManager()
    return _PROMPT_MANAGER


def get_system_prompt(agent_type: str = "main") -> str:
    """
    Get the appropriate system prompt for the specified agent type.

    Args:
        agent_type: Type of agent ("main", "context_engineering", "planning", "general_purpose")

    Returns:
        System prompt string for the specified agent type
    """
    if agent_type != "main":
        agent_type = "main"

    sections = _load_system_prompt_sections()
    if not sections:
        _LOGGER.warning("No system prompt sections found; returning empty prompt")
        return ""

    return "\n\n".join(sections)


def enhance_instructions_with_system_prompt(instructions: str, agent_type: str = "main") -> str:
    """
    Enhance existing instructions with the appropriate system prompt.

    Args:
        instructions: Existing instructions
        agent_type: Type of agent for system prompt selection

    Returns:
        Enhanced instructions with system prompt
    """
    system_prompt = get_system_prompt(agent_type)
    return system_prompt
    # return f"{system_prompt}\n\n## Additional Instructions\n{instructions}"
