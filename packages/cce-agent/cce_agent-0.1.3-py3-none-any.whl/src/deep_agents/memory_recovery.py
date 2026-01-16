"""
Memory Recovery for CCE Deep Agent.

This module handles memory recovery and reconstruction from persistent storage
when the agent restarts, including semantic index rebuilding.
"""

import logging
import time
from typing import Any, Dict, List, Optional

from src.context_memory import MemoryRecord, MemoryType

from .memory_serialization import deserialize_memory_system

logger = logging.getLogger(__name__)


def rebuild_episodic_index(episodic_memory: list[MemoryRecord], index_data: dict[str, Any] | None = None) -> Any | None:
    """
    Rebuild the episodic memory semantic index from memory records.

    Args:
        episodic_memory: List of episodic memory records
        index_data: Optional serialized index data for reconstruction

    Returns:
        Rebuilt InMemoryVectorIndex or None if unavailable
    """
    try:
        from src.semantic.embeddings import InMemoryVectorIndex, create_embedding_provider

        if not episodic_memory:
            logger.info("📚 [MEMORY RECOVERY] No episodic memory records to index")
            return None

        # Create new embedding provider and index
        embedding_provider = create_embedding_provider()
        episodic_index = InMemoryVectorIndex(embedding_provider)

        # Add all episodic memory records to the index
        for record in episodic_memory:
            try:
                episodic_index.add_text(
                    record.content,
                    metadata={
                        "memory_type": record.memory_type.value
                        if hasattr(record.memory_type, "value")
                        else str(record.memory_type),
                        "metadata": record.metadata,
                        "tags": record.tags,
                        "timestamp": record.timestamp.isoformat()
                        if hasattr(record.timestamp, "isoformat")
                        else str(record.timestamp),
                    },
                )
            except Exception as e:
                logger.warning(f"⚠️ [MEMORY RECOVERY] Failed to add episodic record to index: {e}")
                continue

        logger.info(f"📚 [MEMORY RECOVERY] Rebuilt episodic index with {len(episodic_memory)} records")
        return episodic_index

    except ImportError as e:
        logger.warning(f"⚠️ [MEMORY RECOVERY] Semantic embeddings not available: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ [MEMORY RECOVERY] Failed to rebuild episodic index: {e}")
        return None


def rebuild_procedural_index(
    procedural_memory: list[MemoryRecord], index_data: dict[str, Any] | None = None
) -> Any | None:
    """
    Rebuild the procedural memory semantic index from memory records.

    Args:
        procedural_memory: List of procedural memory records
        index_data: Optional serialized index data for reconstruction

    Returns:
        Rebuilt InMemoryVectorIndex or None if unavailable
    """
    try:
        from src.semantic.embeddings import InMemoryVectorIndex, create_embedding_provider

        if not procedural_memory:
            logger.info("🔧 [MEMORY RECOVERY] No procedural memory records to index")
            return None

        # Create new embedding provider and index
        embedding_provider = create_embedding_provider()
        procedural_index = InMemoryVectorIndex(embedding_provider)

        # Add all procedural memory records to the index
        for record in procedural_memory:
            try:
                procedural_index.add_text(
                    record.content,
                    metadata={
                        "memory_type": record.memory_type.value
                        if hasattr(record.memory_type, "value")
                        else str(record.memory_type),
                        "metadata": record.metadata,
                        "tags": record.tags,
                        "timestamp": record.timestamp.isoformat()
                        if hasattr(record.timestamp, "isoformat")
                        else str(record.timestamp),
                    },
                )
            except Exception as e:
                logger.warning(f"⚠️ [MEMORY RECOVERY] Failed to add procedural record to index: {e}")
                continue

        logger.info(f"🔧 [MEMORY RECOVERY] Rebuilt procedural index with {len(procedural_memory)} records")
        return procedural_index

    except ImportError as e:
        logger.warning(f"⚠️ [MEMORY RECOVERY] Semantic embeddings not available: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ [MEMORY RECOVERY] Failed to rebuild procedural index: {e}")
        return None


def recover_memory_system(state: dict[str, Any], checkpoint_data: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Recover memory system from persistent storage and rebuild semantic indices.

    Args:
        state: Current CCE Deep Agent state
        checkpoint_data: Optional checkpoint data from persistent storage

    Returns:
        Updated state with recovered memory system
    """
    try:
        logger.info("🔄 [MEMORY RECOVERY] Starting memory system recovery...")

        # If checkpoint data is provided, deserialize it
        if checkpoint_data:
            logger.info("🔄 [MEMORY RECOVERY] Deserializing checkpoint data...")
            recovered_data = deserialize_memory_system(checkpoint_data)

            # Update state with recovered memory data
            state.update(recovered_data)
            logger.info(f"🔄 [MEMORY RECOVERY] Recovered memory data from checkpoint")

        # Rebuild semantic indices
        episodic_memory = state.get("episodic_memory", [])
        procedural_memory = state.get("procedural_memory", [])

        # Rebuild episodic index
        if episodic_memory:
            episodic_index_data = state.get("episodic_index_data")
            state["episodic_index"] = rebuild_episodic_index(episodic_memory, episodic_index_data)

            # Update episodic stats
            episodic_stats = state.get("episodic_stats", {})
            episodic_stats["episodic_index_available"] = state["episodic_index"] is not None
            episodic_stats["total_episodes"] = len(episodic_memory)
            state["episodic_stats"] = episodic_stats

        # Rebuild procedural index
        if procedural_memory:
            procedural_index_data = state.get("procedural_index_data")
            state["procedural_index"] = rebuild_procedural_index(procedural_memory, procedural_index_data)

            # Update procedural stats
            procedural_stats = state.get("procedural_stats", {})
            procedural_stats["procedural_index_available"] = state["procedural_index"] is not None
            procedural_stats["total_patterns"] = len(procedural_memory)
            state["procedural_stats"] = procedural_stats

        # Update context memory manager with recovered data
        context_memory_manager = state.get("context_memory_manager")
        if context_memory_manager:
            try:
                # Update memory manager with recovered episodic memory
                if hasattr(context_memory_manager, "episodic_memory"):
                    context_memory_manager.episodic_memory = episodic_memory

                # Update memory manager with recovered procedural memory
                if hasattr(context_memory_manager, "procedural_memory"):
                    context_memory_manager.procedural_memory = procedural_memory

                logger.info("🔄 [MEMORY RECOVERY] Updated context memory manager with recovered data")
            except Exception as e:
                logger.warning(f"⚠️ [MEMORY RECOVERY] Failed to update context memory manager: {e}")

        # Update memory statistics
        memory_stats = state.get("memory_stats", {})
        memory_stats.update(
            {
                "episodic_records": len(episodic_memory),
                "procedural_patterns": len(procedural_memory),
                "working_memory_size": len(state.get("working_memory", [])),
                "recovery_timestamp": time.time(),
                "episodic_index_available": state.get("episodic_index") is not None,
                "procedural_index_available": state.get("procedural_index") is not None,
            }
        )
        state["memory_stats"] = memory_stats

        # Clear the needs_index_rebuild flag
        if "needs_index_rebuild" in state:
            del state["needs_index_rebuild"]

        logger.info(f"🔄 [MEMORY RECOVERY] Memory system recovery completed successfully")
        logger.info(f"   📝 Working Memory: {len(state.get('working_memory', []))} records")
        logger.info(f"   📚 Episodic Memory: {len(episodic_memory)} records")
        logger.info(f"   🔧 Procedural Memory: {len(procedural_memory)} patterns")
        logger.info(f"   📚 Episodic Index: {'Available' if state.get('episodic_index') else 'Not Available'}")
        logger.info(f"   🔧 Procedural Index: {'Available' if state.get('procedural_index') else 'Not Available'}")

        return state

    except Exception as e:
        logger.error(f"❌ [MEMORY RECOVERY] Failed to recover memory system: {e}")

        # Return state with error information
        memory_stats = state.get("memory_stats", {})
        memory_stats["recovery_error"] = str(e)
        memory_stats["recovery_timestamp"] = time.time()
        state["memory_stats"] = memory_stats

        return state


def get_memory_recovery_status(state: dict[str, Any]) -> dict[str, Any]:
    """
    Get status of memory recovery system.

    Args:
        state: CCE Deep Agent state

    Returns:
        Dictionary with recovery status information
    """
    working_memory = state.get("working_memory", [])
    episodic_memory = state.get("episodic_memory", [])
    procedural_memory = state.get("procedural_memory", [])
    memory_stats = state.get("memory_stats", {})

    return {
        "recovery_available": True,
        "working_memory_recovered": len(working_memory) > 0,
        "episodic_memory_recovered": len(episodic_memory) > 0,
        "procedural_memory_recovered": len(procedural_memory) > 0,
        "episodic_index_rebuilt": state.get("episodic_index") is not None,
        "procedural_index_rebuilt": state.get("procedural_index") is not None,
        "total_recovered_records": len(working_memory) + len(episodic_memory) + len(procedural_memory),
        "recovery_timestamp": memory_stats.get("recovery_timestamp"),
        "recovery_error": memory_stats.get("recovery_error"),
        "context_memory_manager_updated": state.get("context_memory_manager") is not None,
        "needs_index_rebuild": state.get("needs_index_rebuild", False),
    }


def validate_memory_recovery(state: dict[str, Any]) -> bool:
    """
    Validate that memory recovery was successful.

    Args:
        state: CCE Deep Agent state after recovery

    Returns:
        True if recovery was successful, False otherwise
    """
    try:
        # Check basic memory data
        working_memory = state.get("working_memory", [])
        episodic_memory = state.get("episodic_memory", [])
        procedural_memory = state.get("procedural_memory", [])

        # Check memory statistics
        memory_stats = state.get("memory_stats", {})
        if not memory_stats:
            logger.warning("⚠️ [MEMORY RECOVERY VALIDATION] No memory statistics found")
            return False

        # Check for recovery errors
        if memory_stats.get("recovery_error"):
            logger.error(f"❌ [MEMORY RECOVERY VALIDATION] Recovery error found: {memory_stats['recovery_error']}")
            return False

        # Validate record counts match statistics
        if memory_stats.get("episodic_records", 0) != len(episodic_memory):
            logger.warning(
                f"⚠️ [MEMORY RECOVERY VALIDATION] Episodic record count mismatch: stats={memory_stats.get('episodic_records', 0)}, actual={len(episodic_memory)}"
            )

        if memory_stats.get("procedural_patterns", 0) != len(procedural_memory):
            logger.warning(
                f"⚠️ [MEMORY RECOVERY VALIDATION] Procedural pattern count mismatch: stats={memory_stats.get('procedural_patterns', 0)}, actual={len(procedural_memory)}"
            )

        # Check semantic indices if memory exists
        if episodic_memory and not state.get("episodic_index"):
            logger.warning("⚠️ [MEMORY RECOVERY VALIDATION] Episodic memory exists but index not rebuilt")

        if procedural_memory and not state.get("procedural_index"):
            logger.warning("⚠️ [MEMORY RECOVERY VALIDATION] Procedural memory exists but index not rebuilt")

        logger.info("✅ [MEMORY RECOVERY VALIDATION] Memory recovery validation passed")
        return True

    except Exception as e:
        logger.error(f"❌ [MEMORY RECOVERY VALIDATION] Validation failed: {e}")
        return False
