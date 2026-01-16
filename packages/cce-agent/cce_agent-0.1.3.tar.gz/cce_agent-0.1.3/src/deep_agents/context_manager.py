"""
CCE Context Manager for Deep Agents Integration.

This module bridges the existing ContextMemoryManager with the deep agents virtual filesystem,
enabling cross-agent context sharing and persistent context storage.
"""

from typing import Any, Dict, Optional

from .state import CCEDeepAgentState


class CCEContextManager:
    """
    Bridge between existing ContextMemoryManager and deep agents virtual filesystem.

    This class enables:
    - Cross-agent context sharing via virtual filesystem
    - Integration with existing memory systems
    - Persistent context storage
    """

    def __init__(self, deep_agent_state, memory_manager=None):
        """
        Initialize the context manager.

        Args:
            deep_agent_state: The deep agent state containing virtual filesystem (can be dict or CCEDeepAgentState)
            memory_manager: Optional existing memory manager for integration
        """
        self.state = deep_agent_state
        self.memory_manager = memory_manager

        # Initialize virtual filesystem if not present
        # Handle both dict and object state formats
        if isinstance(self.state, dict):
            if "context_files" not in self.state or self.state["context_files"] is None:
                self.state["context_files"] = {}
        else:
            if not hasattr(self.state, "context_files") or self.state.context_files is None:
                self.state.context_files = {}

    def store_cross_agent_context(self, agent_type: str, content: str) -> None:
        """
        Store context in both memory system and virtual filesystem.

        Args:
            agent_type: Type of agent (e.g., 'context-engineer', 'aider-specialist')
            content: Content to store
        """
        # Store in virtual filesystem for cross-agent access
        if isinstance(self.state, dict):
            if self.state.get("context_files") is None:
                self.state["context_files"] = {}
            self.state["context_files"][f"context/{agent_type}_analysis.md"] = content
        else:
            if self.state.context_files is None:
                self.state.context_files = {}
            self.state.context_files[f"context/{agent_type}_analysis.md"] = content

        # Also store in existing memory system if available
        if self.memory_manager:
            try:
                # Use existing memory manager's episodic storage
                self.memory_manager.store_episodic(content)
            except Exception as e:
                # Log error but don't fail - virtual filesystem is primary
                print(f"Warning: Could not store in memory manager: {e}")

    def retrieve_cross_agent_context(self, agent_type: str) -> str | None:
        """
        Retrieve context from virtual filesystem.

        Args:
            agent_type: Type of agent to retrieve context for

        Returns:
            Context content if found, None otherwise
        """
        if isinstance(self.state, dict):
            if self.state.get("context_files") is None:
                return None
            key = f"context/{agent_type}_analysis.md"
            return self.state["context_files"].get(key)
        else:
            if not hasattr(self.state, "context_files") or self.state.context_files is None:
                return None
            key = f"context/{agent_type}_analysis.md"
            return self.state.context_files.get(key)

    def list_available_contexts(self) -> dict[str, str]:
        """
        List all available contexts in the virtual filesystem.

        Returns:
            Dictionary mapping context keys to content previews
        """
        if isinstance(self.state, dict):
            if self.state.get("context_files") is None:
                return {}
            context_files = self.state["context_files"]
        else:
            if not hasattr(self.state, "context_files") or self.state.context_files is None:
                return {}
            context_files = self.state.context_files

        contexts = {}
        for key, content in context_files.items():
            if key.startswith("context/"):
                # Create preview (first 100 characters)
                preview = content[:100] + "..." if len(content) > 100 else content
                contexts[key] = preview

        return contexts
