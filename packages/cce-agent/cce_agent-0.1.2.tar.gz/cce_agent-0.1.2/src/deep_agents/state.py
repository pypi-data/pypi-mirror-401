"""
CCE Deep Agent State Management.

This module defines the CCE deep agent state with CCE-specific capabilities,
including approval caching and context memory integration.

Note: As of deepagents 0.3.x, there is no DeepAgentState base class.
We define our own TypedDict-based state compatible with LangGraph.
"""

from typing import Annotated, Any, Dict, List, NotRequired, Optional, Set, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel


# Base state compatible with deepagents 0.3.x and LangGraph 1.x
class DeepAgentState(TypedDict, total=False):
    """Base deep agent state compatible with LangGraph 1.x."""

    messages: Annotated[list[AnyMessage], add_messages]
    files: dict[str, str]  # Virtual filesystem
    todos: list[dict[str, Any]]  # Todo list for task tracking


# Import memory system components
try:
    from src.context_memory import MemoryRecord
    from src.semantic.embeddings import InMemoryVectorIndex

    from .memory_reducers import episodic_memory_reducer, procedural_memory_reducer, working_memory_reducer
except ImportError:
    # Fallback for when memory system is not available
    MemoryRecord = Any
    working_memory_reducer = None
    episodic_memory_reducer = None
    procedural_memory_reducer = None
    InMemoryVectorIndex = Any


class ApprovedOperations(BaseModel):
    """Approval operations cache for reducing user friction."""

    cached_approvals: set[str]


class CCEDeepAgentState(DeepAgentState):
    """
    Extended deep agent state with CCE capabilities.

    This state extends the base DeepAgentState with:
    - Approval operations caching
    - Context memory integration
    - Virtual filesystem support
    - Cross-agent coordination
    - Optimized file system state management
    - 3-layer memory system integration
    """

    # Preserve existing CCE state
    context_memory: NotRequired[dict[str, Any] | None]
    stakeholder_analysis: NotRequired[dict[str, Any] | None]
    execution_phases: NotRequired[list[dict[str, Any]] | None]

    # Deep agents enhancements (inspired by open-swe-v2)
    approved_operations: NotRequired[ApprovedOperations | None]
    context_files: NotRequired[dict[str, str] | None]  # Virtual filesystem
    agent_coordination: NotRequired[dict[str, Any] | None]  # Cross-agent state

    # Optimized file system state management (from Deep Agents patterns)
    # files: inherited from DeepAgentState
    changed_files: NotRequired[list[str] | None]  # List of files that have been modified

    # Context management and trimming tracking
    context_size: NotRequired[int | None]  # Current context size in tokens
    last_trimmed_count: NotRequired[int | None]  # Number of messages trimmed in last operation
    trimming_stats: NotRequired[dict[str, Any] | None]  # Detailed trimming statistics

    # Summarization tracking (Phase 2)
    last_summarized_count: NotRequired[int | None]  # Number of messages summarized in last operation
    summarization_stats: NotRequired[dict[str, Any] | None]  # Detailed summarization statistics
    context: NotRequired[dict[str, Any] | None]  # For summarization state tracking

    # DeepAgents-specific context management
    context_management_enabled: NotRequired[bool]  # Whether context management is active

    # Execution control
    remaining_steps: NotRequired[int | None]  # Number of remaining execution steps
    max_context_tokens: NotRequired[int]  # Maximum tokens allowed in context
    last_context_check: NotRequired[int | None]  # Timestamp of last context check
    context_management_mode: NotRequired[str]  # "trim", "summarize", or "adaptive"

    # ADD: 3-layer memory system integration
    context_memory_manager: NotRequired[Any | None]  # ContextMemoryManager instance
    memory_integration: NotRequired[dict[str, Any] | None]  # Memory system configuration

    # ADD: Memory system statistics
    memory_stats: NotRequired[dict[str, Any] | None]  # Memory system statistics
    last_memory_sync: NotRequired[int | None]  # Timestamp of last memory sync

    # ADD: Working memory with intelligent management
    working_memory: NotRequired[list[MemoryRecord] | None]  # Working memory records
    working_memory_stats: NotRequired[dict[str, Any] | None]  # Working memory statistics

    # ADD: Episodic memory with semantic indexing
    episodic_memory: NotRequired[list[MemoryRecord] | None]  # Episodic memory records
    episodic_index: NotRequired[InMemoryVectorIndex | None]  # Semantic index for episodic memory
    episodic_stats: NotRequired[dict[str, Any] | None]  # Episodic memory statistics

    # ADD: Procedural memory with pattern extraction
    procedural_memory: NotRequired[list[MemoryRecord] | None]  # Procedural memory records
    procedural_index: NotRequired[InMemoryVectorIndex | None]  # Semantic index for procedural memory
    procedural_patterns: NotRequired[dict[str, Any] | None]  # Procedural pattern metadata
    procedural_stats: NotRequired[dict[str, Any] | None]  # Procedural memory statistics

    # ADD: Memory persistence and recovery
    memory_persistence_enabled: NotRequired[bool | None]  # Whether memory persistence is enabled
    memory_checkpoint_data: NotRequired[dict[str, Any] | None]  # Checkpoint data for recovery
    memory_recovery_timestamp: NotRequired[float | None]  # Timestamp of last memory recovery
    memory_serialization_status: NotRequired[dict[str, Any] | None]  # Serialization status information
    memory_recovery_status: NotRequired[dict[str, Any] | None]  # Recovery status information

    def add_file(self, path: str, content: str) -> None:
        """
        Add file to virtual filesystem.

        Args:
            path: File path in virtual filesystem
            content: File content
        """
        if self.files is None:
            self.files = {}
        self.files[path] = content

    def get_file(self, path: str) -> str | None:
        """
        Get file from virtual filesystem.

        Args:
            path: File path in virtual filesystem

        Returns:
            File content or None if not found
        """
        if self.files is None:
            return None
        return self.files.get(path)

    def remove_file(self, path: str) -> bool:
        """
        Remove file from virtual filesystem.

        Args:
            path: File path in virtual filesystem

        Returns:
            True if file was removed, False if not found
        """
        if self.files is None:
            return False
        return self.files.pop(path, None) is not None

    def list_files(self, prefix: str = "") -> list[str]:
        """
        List files in virtual filesystem.

        Args:
            prefix: Optional prefix to filter files

        Returns:
            List of file paths
        """
        if self.files is None:
            return []

        if prefix:
            return [path for path in self.files.keys() if path.startswith(prefix)]
        return list(self.files.keys())

    def get_file_info(self, path: str) -> dict[str, Any] | None:
        """
        Get file information from virtual filesystem.

        Args:
            path: File path in virtual filesystem

        Returns:
            File information dict or None if not found
        """
        if self.files is None or path not in self.files:
            return None

        content = self.files[path]
        return {"path": path, "size": len(content), "lines": len(content.splitlines()), "exists": True}

    def sync_with_context_files(self) -> None:
        """
        Sync virtual filesystem with context_files for backward compatibility.
        """
        if self.files is not None and self.context_files is None:
            self.context_files = self.files.copy()
        elif self.context_files is not None and self.files is None:
            self.files = self.context_files.copy()
        elif self.files is not None and self.context_files is not None:
            # Merge both, with files taking precedence
            self.context_files.update(self.files)
            self.files = self.context_files.copy()
