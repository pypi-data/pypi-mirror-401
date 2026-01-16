"""
Memory Hooks for CCE Deep Agent.

This module provides hooks for synchronizing LangGraph messages with the 3-layer memory system
and managing working memory operations.
"""

import logging
import time
from typing import Any, Dict, Optional

from src.context_memory import MemoryRecord

from .memory_nodes import (
    context_injection_node,
    episodic_storage_node,
    get_episodic_memory_status,
    get_procedural_memory_status,
    procedural_learning_node,
)
from .memory_reducers import (
    estimate_tokens,
    get_episodic_memory_summary,
    get_working_memory_summary,
    sync_messages_to_working_memory,
)
from .memory_serialization import serialize_memory_record_for_context, serialize_memory_system_for_context

logger = logging.getLogger(__name__)


def create_working_memory_sync_hook():
    """
    Create hook to sync messages with working memory.

    Returns:
        Hook function that syncs LangGraph messages to working memory
    """

    def sync_hook(state) -> dict:
        """
        Sync LangGraph messages to working memory.

        Args:
            state: CCE Deep Agent state (dict)

        Returns:
            Updated state with working memory synchronized
        """
        try:
            messages = state.get("messages", [])
            if not messages:
                logger.debug("🔄 [WORKING MEMORY] No messages to sync")
                return state

            # Check if we have the necessary components (optional for basic working memory)
            context_memory_manager = state.get("context_memory_manager")
            if not context_memory_manager:
                logger.debug("🔄 [WORKING MEMORY] No context memory manager available, using basic working memory")

            # Sync messages to working memory
            memory_records = sync_messages_to_working_memory(messages)

            # Update working memory in state
            state["working_memory"] = memory_records

            # Calculate context size metrics for optimization tracking
            original_size = 0
            optimized_size = 0
            if memory_records:
                # Calculate original size (full serialization)
                for record in memory_records:
                    original_size += len(str(record.content)) + len(str(record.metadata)) + len(str(record.tags))

                # Calculate optimized size (context-optimized serialization)
                for record in memory_records:
                    context_record = serialize_memory_record_for_context(record)
                    optimized_size += (
                        len(str(context_record.get("content", "")))
                        + len(str(context_record.get("metadata", {})))
                        + len(str(context_record.get("tags", [])))
                    )

            # Calculate size reduction
            size_reduction = 0
            reduction_percentage = 0
            if original_size > 0:
                size_reduction = original_size - optimized_size
                reduction_percentage = (size_reduction / original_size) * 100

            # Update working memory statistics with context optimization metrics
            state["working_memory_stats"] = {
                "record_count": len(memory_records),
                "token_estimate": estimate_tokens(memory_records),
                "last_sync": time.time(),
                "summary": get_working_memory_summary(memory_records),
                "context_optimization": {
                    "original_size": original_size,
                    "optimized_size": optimized_size,
                    "size_reduction": size_reduction,
                    "reduction_percentage": reduction_percentage,
                },
            }

            # Update overall memory stats
            if "memory_stats" in state:
                state["memory_stats"]["working_memory_size"] = len(memory_records)
                state["memory_stats"]["last_working_memory_sync"] = time.time()
                state["memory_stats"]["context_optimization_enabled"] = True

            logger.info(f"🔄 [WORKING MEMORY] Synced {len(messages)} messages to {len(memory_records)} memory records")
            logger.info(f"   📊 Token estimate: {estimate_tokens(memory_records)}")
            if size_reduction > 0:
                logger.info(
                    f"   🎯 Context optimization: {reduction_percentage:.1f}% reduction ({original_size} → {optimized_size} chars)"
                )

        except Exception as e:
            logger.error(f"❌ [WORKING MEMORY] Failed to sync messages to working memory: {e}")
            # Don't fail the entire operation, just log the error

        return state

    return sync_hook


def create_working_memory_trim_hook(max_tokens: int = 30000):  # More conservative
    """
    Create hook to trim working memory when it exceeds limits.

    Args:
        max_tokens: Maximum tokens allowed in working memory

    Returns:
        Hook function that trims working memory
    """

    def trim_hook(state) -> dict:
        """
        Trim working memory if it exceeds limits.

        Args:
            state: CCE Deep Agent state (dict)

        Returns:
            Updated state with trimmed working memory
        """
        try:
            working_memory = state.get("working_memory", [])
            if not working_memory:
                return state

            current_tokens = estimate_tokens(working_memory)
            if current_tokens <= max_tokens:
                return state

            # Import trim function here to avoid circular imports
            from .memory_reducers import trim_working_memory

            # Trim working memory
            trimmed_memory = trim_working_memory(working_memory)
            state["working_memory"] = trimmed_memory

            # Update statistics
            if "working_memory_stats" in state:
                state["working_memory_stats"]["record_count"] = len(trimmed_memory)
                state["working_memory_stats"]["token_estimate"] = estimate_tokens(trimmed_memory)
                state["working_memory_stats"]["last_trim"] = time.time()
                state["working_memory_stats"]["trimmed_from"] = len(working_memory)

            logger.info(f"✂️ [WORKING MEMORY] Trimmed from {len(working_memory)} to {len(trimmed_memory)} records")
            logger.info(f"   📊 Token reduction: {current_tokens} → {estimate_tokens(trimmed_memory)}")

        except Exception as e:
            logger.error(f"❌ [WORKING MEMORY] Failed to trim working memory: {e}")

        return state

    return trim_hook


def create_memory_management_hook():
    """
    Create comprehensive memory management hook that combines sync, trim, and episodic operations.

    Returns:
        Hook function that manages working and episodic memory comprehensively
    """

    def memory_hook(state) -> dict:
        """
        Comprehensive memory management hook.

        Args:
            state: CCE Deep Agent state (dict)

        Returns:
            Updated state with managed working and episodic memory
        """
        try:
            # First sync messages to working memory
            sync_hook = create_working_memory_sync_hook()
            state = sync_hook(state)

            # Then trim if necessary
            trim_hook = create_working_memory_trim_hook()
            state = trim_hook(state)

            # Check for episodic memory creation
            state = episodic_storage_node(state)

            # Check for procedural learning
            state = procedural_learning_node(state)

            # Inject relevant context from episodic memory
            state = context_injection_node(state)

            # Update last memory sync timestamp
            state["last_memory_sync"] = time.time()

        except Exception as e:
            logger.error(f"❌ [MEMORY MANAGEMENT] Failed to manage memory: {e}")

        return state

    return memory_hook


def create_memory_context_optimization_hook():
    """
    Create hook to apply context optimization to memory system.

    Returns:
        Hook function that optimizes memory records for context usage
    """

    def optimization_hook(state) -> dict:
        """
        Apply context optimization to memory system.

        Args:
            state: CCE Deep Agent state (dict)

        Returns:
            Updated state with context-optimized memory system
        """
        try:
            # Check if context optimization is enabled
            if not state.get("memory_stats", {}).get("context_optimization_enabled", False):
                logger.debug("🎯 [CONTEXT OPTIMIZATION] Context optimization not enabled")
                return state

            # Apply context optimization to memory system
            optimized_memory_system = serialize_memory_system_for_context(state, max_records_per_type=10)

            # Update state with optimized memory system
            if "context_optimization_stats" in optimized_memory_system:
                context_stats = optimized_memory_system["context_optimization_stats"]

                # Update memory stats with optimization metrics
                if "memory_stats" not in state:
                    state["memory_stats"] = {}

                state["memory_stats"]["context_optimization_stats"] = context_stats
                state["memory_stats"]["last_context_optimization"] = time.time()

                logger.info(f"🎯 [CONTEXT OPTIMIZATION] Applied context optimization")
                logger.info(
                    f"   📊 Size reduction: {context_stats['reduction_percentage']:.1f}% ({context_stats['original_size']} → {context_stats['optimized_size']} chars)"
                )

        except Exception as e:
            logger.error(f"❌ [CONTEXT OPTIMIZATION] Failed to apply context optimization: {e}")
            # Don't fail the entire operation, just log the error

        return state

    return optimization_hook


def get_memory_hook_status(state) -> dict[str, Any]:
    """
    Get status of memory hooks, working memory, and episodic memory.

    Args:
        state: CCE Deep Agent state (dict)

    Returns:
        Dictionary with memory hook status information
    """
    working_memory = state.get("working_memory", [])
    working_memory_stats = state.get("working_memory_stats", {})
    episodic_memory = state.get("episodic_memory", [])

    # Get episodic and procedural memory status
    episodic_status = get_episodic_memory_status(state)
    procedural_status = get_procedural_memory_status(state)

    # Get context optimization status
    memory_stats = state.get("memory_stats", {})
    context_optimization_stats = memory_stats.get("context_optimization_stats", {})
    working_memory_context_stats = working_memory_stats.get("context_optimization", {})

    return {
        "working_memory_available": len(working_memory) > 0,
        "working_memory_size": len(working_memory),
        "token_estimate": estimate_tokens(working_memory),
        "last_sync": working_memory_stats.get("last_sync"),
        "last_trim": working_memory_stats.get("last_trim"),
        "context_memory_manager_available": state.get("context_memory_manager") is not None,
        "memory_integration_configured": state.get("memory_integration") is not None,
        "episodic_memory_available": episodic_status["episodic_memory_available"],
        "episodic_memory_size": episodic_status["episodic_memory_size"],
        "episodic_index_available": episodic_status["episodic_index_available"],
        "context_injections": episodic_status["context_injections"],
        "procedural_memory_available": procedural_status["procedural_memory_available"],
        "procedural_memory_size": procedural_status["procedural_memory_size"],
        "procedural_index_available": procedural_status["procedural_index_available"],
        "total_patterns": procedural_status["total_patterns"],
        "pattern_types": procedural_status["pattern_types"],
        "context_optimization_enabled": memory_stats.get("context_optimization_enabled", False),
        "last_context_optimization": memory_stats.get("last_context_optimization"),
        "context_optimization_stats": context_optimization_stats,
        "working_memory_context_optimization": working_memory_context_stats,
    }
