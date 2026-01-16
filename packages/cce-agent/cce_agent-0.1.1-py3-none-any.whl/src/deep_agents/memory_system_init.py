"""
Memory System Initialization for CCE Deep Agent.

This module provides initialization helpers for the 3-layer memory system
integration with the deep agents workflow.
"""

import logging
import os
import time
from typing import Any

from .context_manager import CCEContextManager

# Import semantic embeddings for episodic memory indexing
try:
    from src.semantic.embeddings import InMemoryVectorIndex, create_embedding_provider

    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False
    InMemoryVectorIndex = None

try:
    from src.context_memory import ContextMemoryManager
except ImportError:
    ContextMemoryManager = None

try:
    from src.context_resolver import ContextInjector
except ImportError:
    ContextInjector = None

logger = logging.getLogger(__name__)


def _build_unified_context_system(state: dict[str, Any]) -> dict[str, Any]:
    """Create a lightweight unified context system without legacy integrations."""
    context_memory_manager = None
    if ContextMemoryManager:
        try:
            context_memory_manager = ContextMemoryManager(
                max_episodic_records=1000,
                max_procedural_records=500,
                enable_semantic_retrieval=True,
                embedding_provider="auto",
            )
            logger.info("ContextMemoryManager loaded successfully")
        except Exception as exc:
            logger.warning("Failed to initialize ContextMemoryManager: %s", exc)

    context_injector = None
    if ContextInjector:
        try:
            context_injector = ContextInjector(workspace_root=os.getcwd())
            logger.info("ContextInjector loaded successfully")
        except Exception as exc:
            logger.warning("Failed to initialize ContextInjector: %s", exc)

    deep_agents_context_manager = None
    try:
        deep_agents_context_manager = CCEContextManager(state)
    except Exception as exc:
        logger.warning("Failed to initialize CCEContextManager: %s", exc)

    context_retrieval = {
        "semantic_retrieval": {
            "enabled": True,
            "embedding_provider": "auto",
            "similarity_threshold": 0.7,
            "max_results": 10,
        },
        "keyword_retrieval": {"enabled": True, "fuzzy_matching": True, "max_results": 5},
        "temporal_retrieval": {"enabled": True, "time_decay": True, "max_results": 5},
        "hybrid_retrieval": {
            "enabled": True,
            "combination_strategy": "weighted",
            "weights": {"semantic": 0.5, "keyword": 0.3, "temporal": 0.2},
        },
    }

    memory_system = {
        "context_memory_manager": context_memory_manager,
        "context_injector": context_injector,
        "deep_agents_context_manager": deep_agents_context_manager,
        "context_registry": {},
        "memory_layers": {
            "working_memory": {
                "description": "Current conversation messages with intelligent trimming",
                "max_size": 50,
                "trimming_strategy": "intelligent",
                "compression": True,
            },
            "episodic_memory": {
                "description": "Summaries of past conversations and key outcomes",
                "max_records": 1000,
                "semantic_indexing": True,
                "retrieval_strategy": "semantic_similarity",
            },
            "procedural_memory": {
                "description": "Successful patterns and reusable workflows",
                "max_records": 500,
                "semantic_indexing": True,
                "retrieval_strategy": "pattern_matching",
            },
            "virtual_filesystem": {
                "description": "Deep agents virtual filesystem for cross-agent context sharing",
                "max_files": 1000,
                "compression": True,
                "persistence": True,
            },
        },
        "context_retrieval": context_retrieval,
        "context_storage": {
            "storage_backends": {
                "memory": {"enabled": True, "max_size": 100 * 1024 * 1024},
                "filesystem": {"enabled": True, "path": ".context_cache", "compression": True},
                "vector_database": {"enabled": True, "provider": "in_memory", "index_type": "hnsw"},
            },
            "compression": {"enabled": True, "algorithm": "gzip", "threshold": 1024},
            "persistence": {"enabled": True, "auto_save": True, "save_interval": 300},
        },
        "semantic_retrieval": context_retrieval.get("semantic_retrieval", {}),
        "episodic_memory": getattr(context_memory_manager, "episodic_memory", []),
        "procedural_memory": getattr(context_memory_manager, "procedural_memory", []),
    }

    return memory_system


def initialize_memory_system(state) -> dict:
    """
    Initialize 3-layer memory system in deep agent state.

    Args:
        state: CCE Deep Agent state to initialize

    Returns:
        Updated state with initialized memory system
    """
    try:
        logger.info("🧠 [MEMORY SYSTEM INIT] Initializing 3-layer memory system...")

        memory_system = _build_unified_context_system(state)

        # Initialize memory system fields in state
        state["context_memory_manager"] = memory_system.get("context_memory_manager")
        state["memory_integration"] = memory_system

        # Initialize episodic memory
        state["episodic_memory"] = []
        state["episodic_stats"] = {"total_episodes": 0, "last_episode_created": None, "episodic_index_available": False}

        # Initialize procedural memory
        state["procedural_memory"] = []
        state["procedural_stats"] = {
            "total_patterns": 0,
            "last_pattern_created": None,
            "procedural_index_available": False,
            "pattern_types": {},
        }

        # Initialize episodic memory semantic index
        if SEMANTIC_AVAILABLE:
            try:
                embedding_provider = create_embedding_provider()
                state["episodic_index"] = InMemoryVectorIndex(embedding_provider)
                state["episodic_stats"]["episodic_index_available"] = True
                logger.info(f"📚 [EPISODIC MEMORY] Semantic index initialized")
            except Exception as e:
                logger.warning(f"⚠️ [EPISODIC MEMORY] Failed to initialize semantic index: {e}")
                state["episodic_index"] = None
        else:
            logger.warning(f"⚠️ [EPISODIC MEMORY] Semantic embeddings not available")
            state["episodic_index"] = None

        # Initialize procedural memory semantic index
        if SEMANTIC_AVAILABLE:
            try:
                embedding_provider = create_embedding_provider()
                state["procedural_index"] = InMemoryVectorIndex(embedding_provider)
                state["procedural_stats"]["procedural_index_available"] = True
                logger.info(f"🔧 [PROCEDURAL MEMORY] Semantic index initialized")
            except Exception as e:
                logger.warning(f"⚠️ [PROCEDURAL MEMORY] Failed to initialize semantic index: {e}")
                state["procedural_index"] = None
        else:
            logger.warning(f"⚠️ [PROCEDURAL MEMORY] Semantic embeddings not available")
            state["procedural_index"] = None

        # Initialize memory statistics
        state["memory_stats"] = {
            "working_memory_size": 0,
            "episodic_records": 0,  # Will be updated as episodes are created
            "procedural_patterns": len(memory_system.get("procedural_memory", [])),
            "semantic_enabled": memory_system.get("semantic_retrieval", {}).get("enabled", False),
            "initialization_time": time.time(),
            "context_memory_manager_available": state["context_memory_manager"] is not None,
            "episodic_index_available": state["episodic_index"] is not None,
            "procedural_index_available": state["procedural_index"] is not None,
            "context_injections": 0,
        }

        state["last_memory_sync"] = time.time()

        # Log initialization results
        logger.info(f"🧠 [MEMORY SYSTEM INIT] Memory system initialized successfully")
        logger.info(f"   📝 Working Memory: Intelligent message management")
        logger.info(f"   📚 Episodic Memory: {state['memory_stats']['episodic_records']} records")
        logger.info(f"   🔧 Procedural Memory: {state['memory_stats']['procedural_patterns']} patterns")
        logger.info(f"   🔍 Semantic Retrieval: {state['memory_stats']['semantic_enabled']}")
        logger.info(
            f"   🧠 Context Memory Manager: {'Available' if state['context_memory_manager'] else 'Not Available'}"
        )
        logger.info(f"   📚 Episodic Index: {'Available' if state['episodic_index'] else 'Not Available'}")
        logger.info(f"   🔧 Procedural Index: {'Available' if state['procedural_index'] else 'Not Available'}")

        return state

    except Exception as e:
        logger.error(f"❌ [MEMORY SYSTEM INIT] Failed to initialize memory system: {e}")
        # Initialize with minimal state to prevent failures
        state["memory_stats"] = {
            "working_memory_size": 0,
            "episodic_records": 0,
            "procedural_patterns": 0,
            "semantic_enabled": False,
            "initialization_time": time.time(),
            "context_memory_manager_available": False,
            "initialization_error": str(e),
            "episodic_index_available": False,
            "procedural_index_available": False,
            "context_injections": 0,
        }
        state["last_memory_sync"] = time.time()
        return state


def validate_memory_system(state) -> dict[str, Any]:
    """
    Validate that memory system is properly initialized.

    Args:
        state: CCE Deep Agent state to validate

    Returns:
        Validation results dictionary
    """
    validation_results = {"success": True, "errors": [], "warnings": [], "memory_stats": state.get("memory_stats", {})}

    try:
        # Check if memory system is initialized
        if not state.get("memory_stats"):
            validation_results["errors"].append("Memory stats not initialized")
            validation_results["success"] = False

        # Check if context memory manager is available
        if not state.get("context_memory_manager"):
            validation_results["warnings"].append("Context memory manager not available")

        # Check if memory integration is configured
        if not state.get("memory_integration"):
            validation_results["warnings"].append("Memory integration not configured")

        # Check if last sync timestamp is set
        if not state.get("last_memory_sync"):
            validation_results["warnings"].append("Last memory sync timestamp not set")

        logger.info(
            f"🔍 [MEMORY SYSTEM VALIDATION] Validation {'PASSED' if validation_results['success'] else 'FAILED'}"
        )
        if validation_results["errors"]:
            logger.error(f"   ❌ Errors: {validation_results['errors']}")
        if validation_results["warnings"]:
            logger.warning(f"   ⚠️ Warnings: {validation_results['warnings']}")

    except Exception as e:
        validation_results["success"] = False
        validation_results["errors"].append(f"Validation failed: {e}")
        logger.error(f"❌ [MEMORY SYSTEM VALIDATION] Validation failed: {e}")

    return validation_results


def get_memory_system_status(state) -> dict[str, Any]:
    """
    Get current status of the memory system.

    Args:
        state: CCE Deep Agent state

    Returns:
        Memory system status dictionary
    """
    status = {
        "initialized": state.get("memory_stats") is not None,
        "context_memory_manager_available": state.get("context_memory_manager") is not None,
        "memory_integration_configured": state.get("memory_integration") is not None,
        "last_sync": state.get("last_memory_sync"),
        "stats": state.get("memory_stats", {}),
    }

    return status
