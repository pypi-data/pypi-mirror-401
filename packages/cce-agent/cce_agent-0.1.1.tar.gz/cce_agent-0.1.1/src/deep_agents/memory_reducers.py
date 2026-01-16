"""
Memory Reducers for CCE Deep Agent.

This module provides custom LangGraph reducers for managing the 3-layer memory system
with intelligent trimming and context management.
"""

import logging
import time
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage

from src.context_memory import MemoryRecord, MemoryType

logger = logging.getLogger(__name__)

# Memory limits for intelligent trimming
MAX_WORKING_MEMORY_TOKENS = 30000  # 30k tokens for working memory (more conservative)
MAX_WORKING_MEMORY_RECORDS = 100  # Maximum number of working memory records
MAX_EPISODIC_RECORDS = 1000  # Maximum number of episodic memory records
MAX_PROCEDURAL_RECORDS = 500  # Maximum number of procedural memory records


def estimate_tokens(memory_records: list[MemoryRecord]) -> int:
    """
    Estimate token count for memory records.

    Args:
        memory_records: List of memory records to estimate

    Returns:
        Estimated token count
    """
    if not memory_records:
        return 0

    total_chars = sum(len(record.content) for record in memory_records)
    # Rough estimation: 1 token ≈ 4 characters
    return total_chars // 4


def estimate_message_tokens(messages: list[BaseMessage]) -> int:
    """
    Estimate token count for LangGraph messages.

    Args:
        messages: List of messages to estimate

    Returns:
        Estimated token count
    """
    if not messages:
        return 0

    total_chars = sum(len(msg.content) for msg in messages if hasattr(msg, "content"))
    # Rough estimation: 1 token ≈ 4 characters
    return total_chars // 4


def trim_working_memory(memory_records: list[MemoryRecord]) -> list[MemoryRecord]:
    """
    Intelligently trim working memory to stay within limits.

    Args:
        memory_records: List of memory records to trim

    Returns:
        Trimmed list of memory records
    """
    if not memory_records:
        return []

    # Sort by relevance score (higher is better) and timestamp (newer is better)
    sorted_records = sorted(memory_records, key=lambda r: (r.relevance_score, r.timestamp), reverse=True)

    # Keep most relevant and recent records
    trimmed_records = []
    current_tokens = 0

    for record in sorted_records:
        record_tokens = len(record.content) // 4
        if current_tokens + record_tokens <= MAX_WORKING_MEMORY_TOKENS:
            trimmed_records.append(record)
            current_tokens += record_tokens
        else:
            break

    # Ensure we don't exceed record count limit
    if len(trimmed_records) > MAX_WORKING_MEMORY_RECORDS:
        trimmed_records = trimmed_records[:MAX_WORKING_MEMORY_RECORDS]

    logger.info(f"🧠 [WORKING MEMORY] Trimmed from {len(memory_records)} to {len(trimmed_records)} records")
    logger.info(f"   📊 Token estimate: {estimate_tokens(trimmed_records)}/{MAX_WORKING_MEMORY_TOKENS}")

    return trimmed_records


def working_memory_reducer(existing: list[MemoryRecord], new: list[MemoryRecord]) -> list[MemoryRecord]:
    """
    Custom reducer for working memory with intelligent trimming.

    Args:
        existing: Existing working memory records
        new: New memory records to add

    Returns:
        Combined and trimmed working memory records
    """
    if not new:
        return existing or []

    # Combine existing and new records
    combined = (existing or []) + new

    # Apply context window limits and intelligent trimming
    if estimate_tokens(combined) > MAX_WORKING_MEMORY_TOKENS or len(combined) > MAX_WORKING_MEMORY_RECORDS:
        return trim_working_memory(combined)

    return combined


def message_to_memory_record(message: BaseMessage) -> MemoryRecord:
    """
    Convert a LangGraph message to a memory record.

    Args:
        message: LangGraph message to convert

    Returns:
        Memory record representation of the message
    """
    # Determine message type and relevance
    if isinstance(message, SystemMessage):
        memory_type = MemoryType.WORKING
        relevance_score = 0.9  # System messages are highly relevant
        tags = ["system", "instruction"]
    elif isinstance(message, HumanMessage):
        memory_type = MemoryType.WORKING
        relevance_score = 0.8  # Human messages are very relevant
        tags = ["human", "input"]
    elif isinstance(message, AIMessage):
        memory_type = MemoryType.WORKING
        relevance_score = 0.7  # AI responses are relevant
        tags = ["ai", "response"]
        # Check for tool calls
        if hasattr(message, "tool_calls") and message.tool_calls:
            tags.append("tool_calls")
    elif isinstance(message, ToolMessage):
        memory_type = MemoryType.WORKING
        relevance_score = 0.6  # Tool results are moderately relevant
        tags = ["tool", "result"]
    else:
        memory_type = MemoryType.WORKING
        relevance_score = 0.5  # Unknown message types
        tags = ["unknown"]

    # Create memory record
    record = MemoryRecord(
        content=message.content if hasattr(message, "content") else str(message),
        memory_type=memory_type,
        metadata={
            "message_type": type(message).__name__,
            "message_id": getattr(message, "id", None),
            "timestamp": time.time(),
        },
        tags=tags,
        relevance_score=relevance_score,
    )

    return record


def sync_messages_to_working_memory(messages: list[BaseMessage]) -> list[MemoryRecord]:
    """
    Convert LangGraph messages to working memory records.

    Args:
        messages: List of LangGraph messages to convert

    Returns:
        List of memory records
    """
    if not messages:
        return []

    memory_records = []
    for message in messages:
        try:
            record = message_to_memory_record(message)
            memory_records.append(record)
        except Exception as e:
            logger.warning(f"⚠️ [WORKING MEMORY] Failed to convert message to memory record: {e}")
            continue

    logger.info(f"🔄 [WORKING MEMORY] Converted {len(messages)} messages to {len(memory_records)} memory records")

    return memory_records


def get_working_memory_summary(memory_records: list[MemoryRecord]) -> dict[str, Any]:
    """
    Get summary statistics for working memory.

    Args:
        memory_records: List of working memory records

    Returns:
        Dictionary with working memory statistics
    """
    if not memory_records:
        return {
            "record_count": 0,
            "token_estimate": 0,
            "message_types": {},
            "relevance_distribution": {},
            "last_updated": None,
        }

    # Count message types
    message_types = {}
    relevance_scores = []

    for record in memory_records:
        msg_type = record.metadata.get("message_type", "unknown")
        message_types[msg_type] = message_types.get(msg_type, 0) + 1
        relevance_scores.append(record.relevance_score)

    # Calculate relevance distribution
    relevance_distribution = {
        "high": len([s for s in relevance_scores if s >= 0.8]),
        "medium": len([s for s in relevance_scores if 0.5 <= s < 0.8]),
        "low": len([s for s in relevance_scores if s < 0.5]),
    }

    return {
        "record_count": len(memory_records),
        "token_estimate": estimate_tokens(memory_records),
        "message_types": message_types,
        "relevance_distribution": relevance_distribution,
        "last_updated": max(record.timestamp for record in memory_records).isoformat() if memory_records else None,
    }


def episodic_memory_reducer(existing: list[MemoryRecord], new: list[MemoryRecord]) -> list[MemoryRecord]:
    """
    Custom reducer for episodic memory with semantic indexing.

    Args:
        existing: Existing episodic memory records
        new: New episodic memory records to add

    Returns:
        Combined and trimmed episodic memory records
    """
    if not new:
        return existing or []

    # Combine existing and new records
    combined = (existing or []) + new

    # Apply episodic memory limits (keep most recent N records)
    if len(combined) > MAX_EPISODIC_RECORDS:
        # Keep most recent records, archive older ones
        combined = combined[-MAX_EPISODIC_RECORDS:]
        logger.info(f"📚 [EPISODIC MEMORY] Trimmed to {MAX_EPISODIC_RECORDS} records")

    return combined


def get_episodic_memory_summary(episodic_memory: list[MemoryRecord]) -> dict[str, Any]:
    """
    Get summary statistics for episodic memory.

    Args:
        episodic_memory: List of episodic memory records

    Returns:
        Dictionary with episodic memory statistics
    """
    if not episodic_memory:
        return {
            "episode_count": 0,
            "total_content_length": 0,
            "average_episode_length": 0,
            "episode_types": {},
            "last_episode": None,
        }

    # Count episode types and calculate statistics
    episode_types = {}
    total_content_length = 0

    for record in episodic_memory:
        # Count by tags
        for tag in record.tags:
            episode_types[tag] = episode_types.get(tag, 0) + 1

        total_content_length += len(record.content)

    # Calculate averages
    average_episode_length = total_content_length // len(episodic_memory) if episodic_memory else 0

    # Get most recent episode
    last_episode = max(episodic_memory, key=lambda r: r.timestamp) if episodic_memory else None

    return {
        "episode_count": len(episodic_memory),
        "total_content_length": total_content_length,
        "average_episode_length": average_episode_length,
        "episode_types": episode_types,
        "last_episode": last_episode.metadata.get("episode_id") if last_episode else None,
        "last_episode_timestamp": last_episode.timestamp.isoformat() if last_episode else None,
    }


def procedural_memory_reducer(existing: list[MemoryRecord], new: list[MemoryRecord]) -> list[MemoryRecord]:
    """
    Custom reducer for procedural memory with pattern management.

    Args:
        existing: Existing procedural memory records
        new: New procedural memory records to add

    Returns:
        Combined and trimmed procedural memory records
    """
    if not new:
        return existing or []

    # Combine existing and new records
    combined = (existing or []) + new

    # Apply procedural memory limits (keep most recent N records)
    if len(combined) > MAX_PROCEDURAL_RECORDS:
        # Keep most recent records, archive older ones
        combined = combined[-MAX_PROCEDURAL_RECORDS:]
        logger.info(f"🔧 [PROCEDURAL MEMORY] Trimmed to {MAX_PROCEDURAL_RECORDS} records")

    return combined


def get_procedural_memory_summary(procedural_memory: list[MemoryRecord]) -> dict[str, Any]:
    """
    Get summary statistics for procedural memory.

    Args:
        procedural_memory: List of procedural memory records

    Returns:
        Dictionary with procedural memory summary statistics
    """
    if not procedural_memory:
        return {
            "pattern_count": 0,
            "total_content_length": 0,
            "average_pattern_length": 0,
            "pattern_types": {},
            "last_pattern": None,
            "success_rates": [],
        }

    pattern_types = {}
    total_content_length = 0
    success_rates = []

    for record in procedural_memory:
        # Count pattern types
        pattern_type = record.metadata.get("pattern_type", "unknown")
        pattern_types[pattern_type] = pattern_types.get(pattern_type, 0) + 1

        # Calculate content length
        total_content_length += len(record.content)

        # Collect success rates
        success_rate = record.metadata.get("success_rate", 0.0)
        if success_rate > 0:
            success_rates.append(success_rate)

    average_pattern_length = total_content_length // len(procedural_memory) if procedural_memory else 0
    average_success_rate = sum(success_rates) / len(success_rates) if success_rates else 0.0

    last_pattern = max(procedural_memory, key=lambda r: r.timestamp) if procedural_memory else None

    return {
        "pattern_count": len(procedural_memory),
        "total_content_length": total_content_length,
        "average_pattern_length": average_pattern_length,
        "pattern_types": pattern_types,
        "last_pattern": last_pattern.metadata.get("pattern_id") if last_pattern else None,
        "last_pattern_timestamp": last_pattern.timestamp.isoformat() if last_pattern else None,
        "success_rates": success_rates,
        "average_success_rate": average_success_rate,
        "high_success_patterns": len([r for r in success_rates if r >= 0.8]),
    }


def apply_context_optimization_to_memory_records(memory_records: list[MemoryRecord]) -> list[dict[str, Any]]:
    """
    Apply context optimization to memory records for context usage.

    This function converts memory records to context-optimized format that reduces
    metadata overhead by 80-90% while preserving essential information.

    Args:
        memory_records: List of memory records to optimize

    Returns:
        List of context-optimized memory record dictionaries
    """
    if not memory_records:
        return []

    try:
        # Import context optimization functions
        from .memory_serialization import serialize_memory_record_for_context

        # Apply context optimization to each record
        optimized_records = []
        for record in memory_records:
            optimized_record = serialize_memory_record_for_context(record)
            optimized_records.append(optimized_record)

        logger.debug(f"🎯 [CONTEXT OPTIMIZATION] Applied context optimization to {len(memory_records)} memory records")
        return optimized_records

    except Exception as e:
        logger.error(f"❌ [CONTEXT OPTIMIZATION] Failed to apply context optimization to memory records: {e}")
        # Fallback to basic serialization
        return [
            {"content": record.content, "memory_type": record.memory_type.value, "timestamp": str(record.timestamp)}
            for record in memory_records
        ]


def get_context_optimization_stats(memory_records: list[MemoryRecord]) -> dict[str, Any]:
    """
    Get context optimization statistics for memory records.

    Args:
        memory_records: List of memory records to analyze

    Returns:
        Dictionary with context optimization statistics
    """
    if not memory_records:
        return {
            "original_size": 0,
            "optimized_size": 0,
            "size_reduction": 0,
            "reduction_percentage": 0.0,
            "record_count": 0,
        }

    try:
        # Import context optimization functions
        from .memory_serialization import serialize_memory_record_for_context

        # Calculate original size
        original_size = 0
        for record in memory_records:
            original_size += len(str(record.content)) + len(str(record.metadata)) + len(str(record.tags))

        # Calculate optimized size
        optimized_size = 0
        for record in memory_records:
            context_record = serialize_memory_record_for_context(record)
            optimized_size += (
                len(str(context_record.get("content", "")))
                + len(str(context_record.get("metadata", {})))
                + len(str(context_record.get("tags", [])))
            )

        # Calculate reduction
        size_reduction = original_size - optimized_size
        reduction_percentage = (size_reduction / original_size) * 100 if original_size > 0 else 0.0

        return {
            "original_size": original_size,
            "optimized_size": optimized_size,
            "size_reduction": size_reduction,
            "reduction_percentage": reduction_percentage,
            "record_count": len(memory_records),
        }

    except Exception as e:
        logger.error(f"❌ [CONTEXT OPTIMIZATION] Failed to calculate context optimization stats: {e}")
        return {
            "original_size": 0,
            "optimized_size": 0,
            "size_reduction": 0,
            "reduction_percentage": 0.0,
            "record_count": len(memory_records),
            "error": str(e),
        }
