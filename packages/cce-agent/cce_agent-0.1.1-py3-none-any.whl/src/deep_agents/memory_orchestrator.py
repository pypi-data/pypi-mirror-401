"""
Memory Orchestrator for CCE Deep Agent.

This module provides LangGraph subgraph orchestration for the complete 3-layer memory system,
including working memory sync, episodic storage, procedural learning, and context injection.
"""

import logging
from typing import Any, Dict, List, Optional

from langgraph.graph import StateGraph

from .memory_hooks import create_working_memory_sync_hook, create_working_memory_trim_hook
from .memory_nodes import (
    context_injection_node,
    episodic_storage_node,
    procedural_learning_node,
    should_create_episode,
    task_completed_successfully,
)
from .state import CCEDeepAgentState

logger = logging.getLogger(__name__)


def working_memory_sync_node(state: dict[str, Any]) -> dict[str, Any]:
    """
    LangGraph node for working memory synchronization.

    Args:
        state: Current agent state

    Returns:
        Updated state with synchronized working memory
    """
    try:
        sync_hook = create_working_memory_sync_hook()
        return sync_hook(state)
    except Exception as e:
        logger.error(f"❌ [WORKING MEMORY SYNC NODE] Failed to sync working memory: {e}")
        return state


def working_memory_trim_node(state: dict[str, Any]) -> dict[str, Any]:
    """
    LangGraph node for working memory trimming.

    Args:
        state: Current agent state

    Returns:
        Updated state with trimmed working memory
    """
    try:
        trim_hook = create_working_memory_trim_hook()
        return trim_hook(state)
    except Exception as e:
        logger.error(f"❌ [WORKING MEMORY TRIM NODE] Failed to trim working memory: {e}")
        return state


def route_memory_action(state: dict[str, Any]) -> str:
    """
    Route to appropriate memory action based on current state.

    Args:
        state: Current agent state

    Returns:
        Next node name to execute
    """
    try:
        # Check if we should create an episode
        if should_create_episode(state):
            logger.info("🔄 [MEMORY ROUTING] Routing to episodic storage")
            return "episodic_storage"

        # Check if task is completed successfully for procedural learning
        if task_completed_successfully(state):
            logger.info("🔄 [MEMORY ROUTING] Routing to procedural learning")
            return "procedural_learning"

        # Default to context injection
        logger.info("🔄 [MEMORY ROUTING] Routing to context injection")
        return "context_injection"

    except Exception as e:
        logger.error(f"❌ [MEMORY ROUTING] Failed to route memory action: {e}")
        return "context_injection"  # Safe fallback


def create_memory_management_subgraph():
    """
    Create LangGraph subgraph for comprehensive memory management.

    Returns:
        Compiled LangGraph subgraph for memory management
    """
    try:
        # Create the memory management graph
        memory_graph = StateGraph(CCEDeepAgentState)

        # Add memory management nodes
        memory_graph.add_node("working_memory_sync", working_memory_sync_node)
        memory_graph.add_node("working_memory_trim", working_memory_trim_node)
        memory_graph.add_node("episodic_storage", episodic_storage_node)
        memory_graph.add_node("procedural_learning", procedural_learning_node)
        memory_graph.add_node("context_injection", context_injection_node)

        # Define the memory management flow
        memory_graph.add_edge("working_memory_sync", "working_memory_trim")
        memory_graph.add_conditional_edges("working_memory_trim", route_memory_action)

        # Define conditional routing from working memory trim
        memory_graph.add_edge("episodic_storage", "procedural_learning")
        memory_graph.add_edge("procedural_learning", "context_injection")
        memory_graph.add_edge("context_injection", "context_injection")  # End node

        # Set entry and finish points
        memory_graph.set_entry_point("working_memory_sync")
        memory_graph.set_finish_point("context_injection")

        # Compile the graph
        compiled_graph = memory_graph.compile()

        logger.info("🧠 [MEMORY ORCHESTRATOR] Memory management subgraph created successfully")
        logger.info("   📝 Working Memory: Sync → Trim → Route")
        logger.info("   📚 Episodic Memory: Storage with semantic indexing")
        logger.info("   🔧 Procedural Memory: Pattern learning and extraction")
        logger.info("   🔍 Context Injection: Semantic retrieval and injection")

        return compiled_graph

    except Exception as e:
        logger.error(f"❌ [MEMORY ORCHESTRATOR] Failed to create memory management subgraph: {e}")
        raise


def create_simplified_memory_hook():
    """
    Create a simplified memory management hook that combines all memory operations.

    This is a fallback when the full subgraph is not needed or available.

    Returns:
        Combined memory management hook function
    """

    def memory_hook(state: dict[str, Any]) -> dict[str, Any]:
        """
        Simplified memory management hook that combines all memory operations.

        Args:
            state: Current agent state

        Returns:
            Updated state with all memory operations applied
        """
        try:
            # Step 1: Sync working memory
            sync_hook = create_working_memory_sync_hook()
            state = sync_hook(state)

            # Step 2: Trim working memory if needed
            trim_hook = create_working_memory_trim_hook()
            state = trim_hook(state)

            # Step 3: Check for episodic storage
            if should_create_episode(state):
                state = episodic_storage_node(state)

            # Step 4: Check for procedural learning
            if task_completed_successfully(state):
                state = procedural_learning_node(state)

            # Step 5: Always inject context
            state = context_injection_node(state)

            logger.info("🧠 [SIMPLIFIED MEMORY HOOK] All memory operations completed")

        except Exception as e:
            logger.error(f"❌ [SIMPLIFIED MEMORY HOOK] Failed to execute memory operations: {e}")

        return state

    return memory_hook


def get_memory_orchestrator_status(state: dict[str, Any]) -> dict[str, Any]:
    """
    Get comprehensive status of the memory orchestrator system.

    Args:
        state: Current agent state

    Returns:
        Dictionary with memory orchestrator status information
    """
    try:
        from .memory_hooks import get_memory_hook_status
        from .memory_nodes import get_episodic_memory_status, get_procedural_memory_status

        # Get status from each memory component
        working_memory_status = get_memory_hook_status(state)
        episodic_memory_status = get_episodic_memory_status(state)
        procedural_memory_status = get_procedural_memory_status(state)

        # Combine all status information
        orchestrator_status = {
            "memory_orchestrator_available": True,
            "working_memory": working_memory_status,
            "episodic_memory": episodic_memory_status,
            "procedural_memory": procedural_memory_status,
            "total_memory_records": (
                working_memory_status.get("working_memory_size", 0)
                + episodic_memory_status.get("episodic_memory_size", 0)
                + procedural_memory_status.get("procedural_memory_size", 0)
            ),
            "memory_system_health": "healthy"
            if all(
                [
                    working_memory_status.get("working_memory_available", False),
                    episodic_memory_status.get("episodic_memory_available", False) or True,  # Optional
                    procedural_memory_status.get("procedural_memory_available", False) or True,  # Optional
                ]
            )
            else "degraded",
        }

        return orchestrator_status

    except Exception as e:
        logger.error(f"❌ [MEMORY ORCHESTRATOR STATUS] Failed to get status: {e}")
        return {"memory_orchestrator_available": False, "error": str(e), "memory_system_health": "error"}
