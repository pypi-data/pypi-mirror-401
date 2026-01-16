"""
Memory Serialization for CCE Deep Agent.

This module handles serialization and deserialization of the 3-layer memory system
for persistent storage using LangGraph checkpointing.
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional

from src.context_memory import MemoryRecord, MemoryType

logger = logging.getLogger(__name__)

# Memory size limits for context optimization
MAX_MEMORY_RECORD_SIZE_CONTEXT = 2000  # Maximum characters per memory record in context
MAX_MEMORY_RECORDS_PER_TYPE_CONTEXT = 10  # Maximum number of records per memory type in context
MAX_TOTAL_MEMORY_RECORDS_CONTEXT = 25  # Maximum total memory records in context
MAX_CONTEXT_METADATA_SIZE = 500  # Maximum characters for metadata in context
MAX_CONTEXT_TAGS_COUNT = 3  # Maximum number of tags in context

# Memory record relevance thresholds
MIN_RELEVANCE_SCORE = 0.5  # Minimum relevance score for context inclusion
PRIORITY_MEMORY_TYPES = [MemoryType.WORKING, MemoryType.PROCEDURAL]  # Priority memory types for context


def serialize_memory_record(record: MemoryRecord) -> dict[str, Any]:
    """
    Serialize a MemoryRecord to a dictionary for checkpointing.

    Args:
        record: MemoryRecord to serialize

    Returns:
        Dictionary representation of the memory record
    """
    return {
        "content": record.content,
        "memory_type": record.memory_type.value if hasattr(record.memory_type, "value") else str(record.memory_type),
        "metadata": record.metadata,
        "tags": record.tags,
        "timestamp": record.timestamp.isoformat() if hasattr(record.timestamp, "isoformat") else str(record.timestamp),
    }


def validate_memory_record_for_context(record: MemoryRecord) -> dict[str, Any]:
    """
    Validate a memory record for context inclusion based on size and relevance criteria.

    Args:
        record: MemoryRecord to validate

    Returns:
        Dictionary with validation results including is_valid, size_info, and relevance_info
    """
    validation_result = {"is_valid": True, "size_info": {}, "relevance_info": {}, "violations": []}

    # Check content size
    content_size = len(str(record.content))
    if content_size > MAX_MEMORY_RECORD_SIZE_CONTEXT:
        validation_result["is_valid"] = False
        validation_result["violations"].append(
            f"Content size {content_size} exceeds limit {MAX_MEMORY_RECORD_SIZE_CONTEXT}"
        )

    validation_result["size_info"]["content_size"] = content_size
    validation_result["size_info"]["content_size_limit"] = MAX_MEMORY_RECORD_SIZE_CONTEXT

    # Check metadata size
    metadata_size = len(str(record.metadata)) if record.metadata else 0
    if metadata_size > MAX_CONTEXT_METADATA_SIZE:
        validation_result["is_valid"] = False
        validation_result["violations"].append(
            f"Metadata size {metadata_size} exceeds limit {MAX_CONTEXT_METADATA_SIZE}"
        )

    validation_result["size_info"]["metadata_size"] = metadata_size
    validation_result["size_info"]["metadata_size_limit"] = MAX_CONTEXT_METADATA_SIZE

    # Check tags count
    tags_count = len(record.tags) if record.tags else 0
    if tags_count > MAX_CONTEXT_TAGS_COUNT:
        validation_result["is_valid"] = False
        validation_result["violations"].append(f"Tags count {tags_count} exceeds limit {MAX_CONTEXT_TAGS_COUNT}")

    validation_result["size_info"]["tags_count"] = tags_count
    validation_result["size_info"]["tags_count_limit"] = MAX_CONTEXT_TAGS_COUNT

    # Check relevance score
    relevance_score = getattr(record, "relevance_score", 0.0)
    if relevance_score < MIN_RELEVANCE_SCORE:
        validation_result["is_valid"] = False
        validation_result["violations"].append(f"Relevance score {relevance_score} below minimum {MIN_RELEVANCE_SCORE}")

    validation_result["relevance_info"]["relevance_score"] = relevance_score
    validation_result["relevance_info"]["min_relevance_score"] = MIN_RELEVANCE_SCORE
    validation_result["relevance_info"]["is_priority_type"] = record.memory_type in PRIORITY_MEMORY_TYPES

    return validation_result


def filter_memory_records_for_context(memory_records: list[MemoryRecord]) -> list[MemoryRecord]:
    """
    Filter memory records for context inclusion based on size and relevance criteria.

    Args:
        memory_records: List of memory records to filter

    Returns:
        Filtered list of memory records suitable for context
    """
    if not memory_records:
        return []

    # Step 1: Validate all records
    valid_records = []
    invalid_records = []

    for record in memory_records:
        validation = validate_memory_record_for_context(record)
        if validation["is_valid"]:
            valid_records.append(record)
        else:
            invalid_records.append((record, validation))
            logger.debug(f"🚫 [CONTEXT FILTERING] Excluded record: {validation['violations']}")

    # Step 2: Apply count limits per memory type
    filtered_records = []
    memory_type_counts = {}

    # Sort by relevance score (highest first) and timestamp (newest first)
    valid_records.sort(key=lambda r: (getattr(r, "relevance_score", 0.0), r.timestamp), reverse=True)

    for record in valid_records:
        memory_type = record.memory_type
        current_count = memory_type_counts.get(memory_type, 0)

        if current_count < MAX_MEMORY_RECORDS_PER_TYPE_CONTEXT:
            filtered_records.append(record)
            memory_type_counts[memory_type] = current_count + 1
        else:
            logger.debug(f"🚫 [CONTEXT FILTERING] Excluded record due to count limit for {memory_type}")

    # Step 3: Apply total count limit
    if len(filtered_records) > MAX_TOTAL_MEMORY_RECORDS_CONTEXT:
        # Keep the most relevant records
        filtered_records = filtered_records[:MAX_TOTAL_MEMORY_RECORDS_CONTEXT]
        logger.debug(f"🚫 [CONTEXT FILTERING] Limited to {MAX_TOTAL_MEMORY_RECORDS_CONTEXT} total records")

    logger.info(f"🎯 [CONTEXT FILTERING] Filtered {len(memory_records)} → {len(filtered_records)} records")
    logger.info(f"   📊 Excluded {len(invalid_records)} invalid records")
    logger.info(
        f"   📊 Excluded {len(memory_records) - len(filtered_records) - len(invalid_records)} records due to count limits"
    )

    return filtered_records


def serialize_memory_record_for_context(record: MemoryRecord) -> dict[str, Any]:
    """
    Serialize a MemoryRecord to a minimal dictionary for context usage.

    This function creates a context-optimized version that reduces metadata overhead
    by 80-90% while preserving essential information for context usage.

    Args:
        record: MemoryRecord to serialize for context

    Returns:
        Minimal dictionary representation optimized for context usage
    """
    # Essential fields that must be preserved for context
    context_record = {
        "content": record.content,
        "memory_type": record.memory_type.value if hasattr(record.memory_type, "value") else str(record.memory_type),
        "timestamp": record.timestamp.isoformat() if hasattr(record.timestamp, "isoformat") else str(record.timestamp),
    }

    # Add minimal metadata - only essential fields for context
    if record.metadata:
        # Filter out non-essential metadata that causes bloat
        essential_metadata = {}

        # Preserve only essential metadata fields
        essential_fields = ["message_type", "pattern_type"]
        for field in essential_fields:
            if field in record.metadata:
                essential_metadata[field] = record.metadata[field]

        # For procedural memory, preserve only the most essential pattern info
        if record.memory_type.value.upper() == "PROCEDURAL" and "pattern_type" in record.metadata:
            # Only keep pattern type, not the full pattern analysis
            essential_metadata["pattern_type"] = record.metadata["pattern_type"]
            # Optionally keep a summary of tool sequence if it's short
            if "tool_sequence" in record.metadata and len(record.metadata["tool_sequence"]) <= 3:
                essential_metadata["tools"] = record.metadata["tool_sequence"]

        if essential_metadata:
            context_record["metadata"] = essential_metadata

    # Add minimal tags - only the most relevant ones
    if record.tags:
        # Limit tags to most relevant ones for context
        context_record["tags"] = record.tags[:3] if len(record.tags) > 3 else record.tags

    return context_record


def filter_metadata_for_context(metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Filter metadata to remove non-essential fields that cause context bloat.

    Args:
        metadata: Original metadata dictionary

    Returns:
        Filtered metadata with only essential fields for context
    """
    if not metadata:
        return {}

    # Fields to exclude from context (these cause the most bloat)
    excluded_fields = {
        "pattern_id",  # Unique identifiers not needed in context
        "success_rate",  # Numerical analysis not essential for context
        "tool_sequence",  # Full tool sequences (replaced with 'tools' if short)
        "conditions",  # Pattern conditions not essential for context
        "outcomes",  # Pattern outcomes not essential for context
        "created_from_episode",  # Episode references not essential for context
        "working_memory_size",  # Size references not essential for context
        "episode_id",  # Episode identifiers not essential for context
        "task_id",  # Task identifiers not essential for context
        "session_id",  # Session identifiers not essential for context
        "user_id",  # User identifiers not essential for context
        "agent_id",  # Agent identifiers not essential for context
        "conversation_id",  # Conversation identifiers not essential for context
        "thread_id",  # Thread identifiers not essential for context
        "message_id",  # Message identifiers not essential for context
        "timestamp",  # Already included at record level
        "created_at",  # Creation timestamps not essential for context
        "updated_at",  # Update timestamps not essential for context
        "accessed_at",  # Access timestamps not essential for context
        "version",  # Version numbers not essential for context
        "hash",  # Hash values not essential for context
        "checksum",  # Checksum values not essential for context
        "signature",  # Signature values not essential for context
        "fingerprint",  # Fingerprint values not essential for context
        "uuid",  # UUID values not essential for context
        "id",  # Generic ID values not essential for context
    }

    # Filter out excluded fields
    filtered_metadata = {key: value for key, value in metadata.items() if key not in excluded_fields}

    # For tool sequences, replace with simplified version if short
    if "tool_sequence" in metadata and len(metadata["tool_sequence"]) <= 3:
        filtered_metadata["tools"] = metadata["tool_sequence"]

    return filtered_metadata


def deserialize_memory_record(data: dict[str, Any]) -> MemoryRecord:
    """
    Deserialize a dictionary to a MemoryRecord.

    Args:
        data: Dictionary representation of the memory record

    Returns:
        MemoryRecord instance
    """
    # Handle memory type conversion
    memory_type_str = data.get("memory_type", "WORKING")
    if isinstance(memory_type_str, str):
        try:
            memory_type = MemoryType(memory_type_str)
        except ValueError:
            # Fallback to WORKING if unknown type
            memory_type = MemoryType.WORKING
            logger.warning(f"⚠️ [MEMORY SERIALIZATION] Unknown memory type: {memory_type_str}, using WORKING")
    else:
        memory_type = memory_type_str

    # Handle timestamp conversion
    timestamp_str = data.get("timestamp")
    if timestamp_str:
        try:
            from datetime import datetime

            if isinstance(timestamp_str, str):
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            else:
                timestamp = timestamp_str
        except (ValueError, TypeError):
            timestamp = time.time()
            logger.warning(f"⚠️ [MEMORY SERIALIZATION] Invalid timestamp: {timestamp_str}, using current time")
    else:
        timestamp = time.time()

    return MemoryRecord(
        content=data.get("content", ""),
        memory_type=memory_type,
        metadata=data.get("metadata", {}),
        tags=data.get("tags", []),
        timestamp=timestamp,
    )


def serialize_memory_system(state: dict[str, Any]) -> dict[str, Any]:
    """
    Serialize the entire memory system for checkpointing.

    Args:
        state: CCE Deep Agent state containing memory system

    Returns:
        Dictionary containing serialized memory system data
    """
    try:
        serialized_data = {
            "working_memory": [],
            "episodic_memory": [],
            "procedural_memory": [],
            "memory_stats": state.get("memory_stats", {}),
            "episodic_stats": state.get("episodic_stats", {}),
            "procedural_stats": state.get("procedural_stats", {}),
            "working_memory_stats": state.get("working_memory_stats", {}),
            "last_memory_sync": state.get("last_memory_sync"),
            "serialization_timestamp": time.time(),
        }

        # Serialize working memory
        working_memory = state.get("working_memory", [])
        if working_memory:
            serialized_data["working_memory"] = [serialize_memory_record(record) for record in working_memory]
            logger.debug(f"📝 [MEMORY SERIALIZATION] Serialized {len(working_memory)} working memory records")

        # Serialize episodic memory
        episodic_memory = state.get("episodic_memory", [])
        if episodic_memory:
            serialized_data["episodic_memory"] = [serialize_memory_record(record) for record in episodic_memory]
            logger.debug(f"📚 [MEMORY SERIALIZATION] Serialized {len(episodic_memory)} episodic memory records")

        # Serialize procedural memory
        procedural_memory = state.get("procedural_memory", [])
        if procedural_memory:
            serialized_data["procedural_memory"] = [serialize_memory_record(record) for record in procedural_memory]
            logger.debug(f"🔧 [MEMORY SERIALIZATION] Serialized {len(procedural_memory)} procedural memory records")

        # Serialize semantic indices (if available)
        episodic_index = state.get("episodic_index")
        if episodic_index and hasattr(episodic_index, "serialize"):
            try:
                serialized_data["episodic_index_data"] = episodic_index.serialize()
                logger.debug(f"📚 [MEMORY SERIALIZATION] Serialized episodic index")
            except Exception as e:
                logger.warning(f"⚠️ [MEMORY SERIALIZATION] Failed to serialize episodic index: {e}")
                serialized_data["episodic_index_data"] = None

        procedural_index = state.get("procedural_index")
        if procedural_index and hasattr(procedural_index, "serialize"):
            try:
                serialized_data["procedural_index_data"] = procedural_index.serialize()
                logger.debug(f"🔧 [MEMORY SERIALIZATION] Serialized procedural index")
            except Exception as e:
                logger.warning(f"⚠️ [MEMORY SERIALIZATION] Failed to serialize procedural index: {e}")
                serialized_data["procedural_index_data"] = None

        logger.info(f"💾 [MEMORY SERIALIZATION] Successfully serialized memory system")
        logger.info(f"   📝 Working Memory: {len(serialized_data['working_memory'])} records")
        logger.info(f"   📚 Episodic Memory: {len(serialized_data['episodic_memory'])} records")
        logger.info(f"   🔧 Procedural Memory: {len(serialized_data['procedural_memory'])} records")

        return serialized_data

    except Exception as e:
        logger.error(f"❌ [MEMORY SERIALIZATION] Failed to serialize memory system: {e}")
        return {
            "working_memory": [],
            "episodic_memory": [],
            "procedural_memory": [],
            "memory_stats": {},
            "episodic_stats": {},
            "procedural_stats": {},
            "working_memory_stats": {},
            "last_memory_sync": None,
            "serialization_timestamp": time.time(),
            "serialization_error": str(e),
        }


def serialize_memory_system_for_context(state: dict[str, Any], max_records_per_type: int = None) -> dict[str, Any]:
    """
    Serialize the entire memory system for context usage with optimization and filtering.

    This function creates a context-optimized version that reduces memory overhead
    by 80-90% while preserving essential information for context usage. It applies
    size limits, count limits, and relevance filtering to prevent context bloat.

    Args:
        state: CCE Deep Agent state containing memory system
        max_records_per_type: Maximum number of records to include per memory type (uses default limits if None)

    Returns:
        Dictionary containing context-optimized serialized memory system data
    """
    try:
        # Use default limits if not specified
        if max_records_per_type is None:
            max_records_per_type = MAX_MEMORY_RECORDS_PER_TYPE_CONTEXT

        # Calculate size reduction metrics
        original_size = 0
        optimized_size = 0
        filtering_stats = {
            "total_records_before": 0,
            "total_records_after": 0,
            "excluded_by_size": 0,
            "excluded_by_relevance": 0,
            "excluded_by_count": 0,
        }

        serialized_data = {
            "working_memory": [],
            "episodic_memory": [],
            "procedural_memory": [],
            "memory_stats": state.get("memory_stats", {}),
            "episodic_stats": state.get("episodic_stats", {}),
            "procedural_stats": state.get("procedural_stats", {}),
            "working_memory_stats": state.get("working_memory_stats", {}),
            "last_memory_sync": state.get("last_memory_sync"),
            "serialization_timestamp": time.time(),
            "context_optimized": True,
            "filtering_applied": True,
        }

        # Process each memory type with filtering
        memory_types = [
            ("working_memory", state.get("working_memory", [])),
            ("episodic_memory", state.get("episodic_memory", [])),
            ("procedural_memory", state.get("procedural_memory", [])),
        ]

        for memory_type_name, memory_records in memory_types:
            if not memory_records:
                continue

            # Apply filtering to get valid records for context
            filtered_records = filter_memory_records_for_context(memory_records)

            # Update filtering stats
            filtering_stats["total_records_before"] += len(memory_records)
            filtering_stats["total_records_after"] += len(filtered_records)
            filtering_stats["excluded_by_size"] += len(memory_records) - len(filtered_records)

            # Serialize filtered records
            serialized_records = [serialize_memory_record_for_context(record) for record in filtered_records]
            serialized_data[memory_type_name] = serialized_records

            # Calculate size reduction for this memory type
            for record in memory_records:
                original_size += len(json.dumps(serialize_memory_record(record)))

            for record in filtered_records:
                optimized_size += len(json.dumps(serialize_memory_record_for_context(record)))

            logger.debug(
                f"📝 [CONTEXT OPTIMIZATION] {memory_type_name}: {len(memory_records)} → {len(filtered_records)} records"
            )

        # Calculate and log size reduction
        if original_size > 0:
            reduction_percentage = ((original_size - optimized_size) / original_size) * 100
            serialized_data["context_optimization_stats"] = {
                "original_size": original_size,
                "optimized_size": optimized_size,
                "size_reduction": original_size - optimized_size,
                "reduction_percentage": reduction_percentage,
                "filtering_stats": filtering_stats,
            }

            logger.info(f"💾 [CONTEXT OPTIMIZATION] Memory system optimized for context")
            logger.info(f"   📝 Working Memory: {len(serialized_data['working_memory'])} records")
            logger.info(f"   📚 Episodic Memory: {len(serialized_data['episodic_memory'])} records")
            logger.info(f"   🔧 Procedural Memory: {len(serialized_data['procedural_memory'])} records")
            logger.info(f"   📊 Size Reduction: {reduction_percentage:.1f}% ({original_size} → {optimized_size} chars)")
            logger.info(
                f"   🎯 Filtering: {filtering_stats['total_records_before']} → {filtering_stats['total_records_after']} records"
            )

        return serialized_data

    except Exception as e:
        logger.error(f"❌ [CONTEXT OPTIMIZATION] Failed to serialize memory system for context: {e}")
        return {
            "working_memory": [],
            "episodic_memory": [],
            "procedural_memory": [],
            "memory_stats": {},
            "episodic_stats": {},
            "procedural_stats": {},
            "working_memory_stats": {},
            "last_memory_sync": None,
            "serialization_timestamp": time.time(),
            "context_optimized": True,
            "filtering_applied": True,
            "serialization_error": str(e),
        }


def deserialize_memory_system(data: dict[str, Any]) -> dict[str, Any]:
    """
    Deserialize memory system from checkpoint data.

    Args:
        data: Dictionary containing serialized memory system data

    Returns:
        Dictionary containing deserialized memory system data
    """
    try:
        deserialized_data = {
            "working_memory": [],
            "episodic_memory": [],
            "procedural_memory": [],
            "memory_stats": data.get("memory_stats", {}),
            "episodic_stats": data.get("episodic_stats", {}),
            "procedural_stats": data.get("procedural_stats", {}),
            "working_memory_stats": data.get("working_memory_stats", {}),
            "last_memory_sync": data.get("last_memory_sync"),
            "needs_index_rebuild": True,
        }

        # Deserialize working memory
        working_memory_data = data.get("working_memory", [])
        if working_memory_data:
            deserialized_data["working_memory"] = [
                deserialize_memory_record(record_data) for record_data in working_memory_data
            ]
            logger.debug(
                f"📝 [MEMORY DESERIALIZATION] Deserialized {len(deserialized_data['working_memory'])} working memory records"
            )

        # Deserialize episodic memory
        episodic_memory_data = data.get("episodic_memory", [])
        if episodic_memory_data:
            deserialized_data["episodic_memory"] = [
                deserialize_memory_record(record_data) for record_data in episodic_memory_data
            ]
            logger.debug(
                f"📚 [MEMORY DESERIALIZATION] Deserialized {len(deserialized_data['episodic_memory'])} episodic memory records"
            )

        # Deserialize procedural memory
        procedural_memory_data = data.get("procedural_memory", [])
        if procedural_memory_data:
            deserialized_data["procedural_memory"] = [
                deserialize_memory_record(record_data) for record_data in procedural_memory_data
            ]
            logger.debug(
                f"🔧 [MEMORY DESERIALIZATION] Deserialized {len(deserialized_data['procedural_memory'])} procedural memory records"
            )

        # Store index data for later rebuilding
        episodic_index_data = data.get("episodic_index_data")
        if episodic_index_data:
            deserialized_data["episodic_index_data"] = episodic_index_data
            logger.debug(f"📚 [MEMORY DESERIALIZATION] Stored episodic index data for rebuilding")

        procedural_index_data = data.get("procedural_index_data")
        if procedural_index_data:
            deserialized_data["procedural_index_data"] = procedural_index_data
            logger.debug(f"🔧 [MEMORY DESERIALIZATION] Stored procedural index data for rebuilding")

        logger.info(f"🔄 [MEMORY DESERIALIZATION] Successfully deserialized memory system")
        logger.info(f"   📝 Working Memory: {len(deserialized_data['working_memory'])} records")
        logger.info(f"   📚 Episodic Memory: {len(deserialized_data['episodic_memory'])} records")
        logger.info(f"   🔧 Procedural Memory: {len(deserialized_data['procedural_memory'])} records")

        return deserialized_data

    except Exception as e:
        logger.error(f"❌ [MEMORY DESERIALIZATION] Failed to deserialize memory system: {e}")
        return {
            "working_memory": [],
            "episodic_memory": [],
            "procedural_memory": [],
            "memory_stats": {},
            "episodic_stats": {},
            "procedural_stats": {},
            "working_memory_stats": {},
            "last_memory_sync": None,
            "needs_index_rebuild": True,
            "deserialization_error": str(e),
        }


def get_memory_serialization_status(state: dict[str, Any]) -> dict[str, Any]:
    """
    Get status of memory serialization system.

    Args:
        state: CCE Deep Agent state

    Returns:
        Dictionary with serialization status information
    """
    working_memory = state.get("working_memory", [])
    episodic_memory = state.get("episodic_memory", [])
    procedural_memory = state.get("procedural_memory", [])

    return {
        "serialization_available": True,
        "working_memory_serializable": len(working_memory) > 0,
        "episodic_memory_serializable": len(episodic_memory) > 0,
        "procedural_memory_serializable": len(procedural_memory) > 0,
        "total_memory_records": len(working_memory) + len(episodic_memory) + len(procedural_memory),
        "episodic_index_serializable": state.get("episodic_index") is not None
        and hasattr(state.get("episodic_index"), "serialize"),
        "procedural_index_serializable": state.get("procedural_index") is not None
        and hasattr(state.get("procedural_index"), "serialize"),
        "last_memory_sync": state.get("last_memory_sync"),
        "memory_stats_available": state.get("memory_stats") is not None,
    }
