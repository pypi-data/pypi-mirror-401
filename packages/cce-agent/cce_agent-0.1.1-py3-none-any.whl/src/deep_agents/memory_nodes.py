"""
Memory Nodes for CCE Deep Agent.

This module provides LangGraph nodes for managing episodic and procedural memory
with semantic indexing and context injection capabilities.
"""

import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.context_memory import MemoryRecord, MemoryType

from .memory_reducers import get_working_memory_summary

logger = logging.getLogger(__name__)

# Memory limits
MAX_EPISODIC_RECORDS = 1000  # Maximum number of episodic memory records
MAX_PROCEDURAL_RECORDS = 500  # Maximum number of procedural memory records
EPISODE_CREATION_THRESHOLD = 20  # Minimum working memory records to create episode
PROCEDURAL_LEARNING_THRESHOLD = 5  # Minimum successful task completions for pattern learning


def generate_episode_id() -> str:
    """Generate a unique episode ID."""
    return f"episode_{uuid.uuid4().hex[:8]}_{int(time.time())}"


def extract_task_context(messages: list[Any]) -> str:
    """
    Extract task context from recent messages.

    Args:
        messages: List of recent messages

    Returns:
        String representation of task context
    """
    if not messages:
        return ""

    # Extract content from last few messages
    context_parts = []
    for msg in messages[-3:]:  # Last 3 messages
        if hasattr(msg, "content") and msg.content:
            content = msg.content
            # Handle both string and list content
            if isinstance(content, list):
                content = " ".join(str(item) for item in content)
            elif not isinstance(content, str):
                content = str(content)

            content = content[:100]  # First 100 characters
            context_parts.append(content)

    return " | ".join(context_parts)


def extract_outcomes(working_memory: list[MemoryRecord]) -> list[str]:
    """
    Extract outcomes from working memory.

    Args:
        working_memory: List of working memory records

    Returns:
        List of outcome descriptions
    """
    outcomes = []

    for record in working_memory:
        # Look for success indicators in AI messages
        if record.metadata.get("message_type") == "AIMessage":
            # Handle both string and list content
            content = record.content
            if isinstance(content, list):
                content = " ".join(str(item) for item in content)
            elif not isinstance(content, str):
                content = str(content)

            if any(keyword in content.lower() for keyword in ["success", "completed", "finished", "done", "solved"]):
                outcomes.append(f"Task completion: {content[:100]}...")

    return outcomes


def extract_decisions(working_memory: list[MemoryRecord]) -> list[str]:
    """
    Extract key decisions from working memory.

    Args:
        working_memory: List of working memory records

    Returns:
        List of decision descriptions
    """
    decisions = []

    for record in working_memory:
        # Look for decision indicators
        if record.metadata.get("message_type") == "AIMessage":
            # Handle both string and list content
            content = record.content
            if isinstance(content, list):
                content = " ".join(str(item) for item in content)
            elif not isinstance(content, str):
                content = str(content)

            if any(keyword in content.lower() for keyword in ["decide", "choose", "select", "will use", "going to"]):
                decisions.append(f"Decision: {content[:100]}...")

    return decisions


def summarize_working_memory(working_memory: list[MemoryRecord]) -> str:
    """
    Summarize working memory into an episode summary.

    Args:
        working_memory: List of working memory records

    Returns:
        String summary of the episode
    """
    if not working_memory:
        return "Empty episode"

    # Get summary statistics
    summary_stats = get_working_memory_summary(working_memory)

    # Extract key information
    message_types = summary_stats.get("message_types", {})
    total_messages = summary_stats.get("record_count", 0)

    # Create summary
    summary_parts = [
        f"Episode Summary ({total_messages} messages):",
        f"- Message types: {dict(message_types)}",
    ]

    # Add key outcomes and decisions
    outcomes = extract_outcomes(working_memory)
    decisions = extract_decisions(working_memory)

    if outcomes:
        summary_parts.append(f"- Key outcomes: {len(outcomes)} identified")

    if decisions:
        summary_parts.append(f"- Key decisions: {len(decisions)} made")

    # Add recent activity
    recent_records = working_memory[-3:] if len(working_memory) >= 3 else working_memory
    recent_activity = []
    for record in recent_records:
        msg_type = record.metadata.get("message_type", "Unknown")
        content_preview = record.content[:50] + "..." if len(record.content) > 50 else record.content
        recent_activity.append(f"{msg_type}: {content_preview}")

    if recent_activity:
        summary_parts.append(f"- Recent activity: {'; '.join(recent_activity)}")

    return "\n".join(summary_parts)


def detect_task_completion(working_memory: list[MemoryRecord]) -> bool:
    """
    Detect if a task has been completed based on working memory.

    Args:
        working_memory: List of working memory records

    Returns:
        True if task appears completed
    """
    if not working_memory:
        return False

    # Look for completion indicators in recent messages
    recent_records = working_memory[-5:]  # Last 5 records

    completion_keywords = [
        "completed",
        "finished",
        "done",
        "success",
        "solved",
        "resolved",
        "task complete",
        "implementation complete",
        "all done",
    ]

    for record in recent_records:
        # Handle both string and list content
        content = record.content
        if isinstance(content, list):
            content = " ".join(str(item) for item in content)
        elif not isinstance(content, str):
            content = str(content)

        content_lower = content.lower()
        if any(keyword in content_lower for keyword in completion_keywords):
            return True

    return False


def should_create_episode(state: dict[str, Any]) -> bool:
    """
    Determine if current working memory should become an episode.

    Args:
        state: CCE Deep Agent state

    Returns:
        True if episode should be created
    """
    working_memory = state.get("working_memory", [])
    if not working_memory:
        return False

    # Create episode if working memory has substantial content
    if len(working_memory) > EPISODE_CREATION_THRESHOLD:
        return True

    # Create episode if task appears completed
    if detect_task_completion(working_memory):
        return True

    # Create episode if significant time has passed since last episode
    last_episode_time = state.get("memory_stats", {}).get("last_episode_created", 0)
    current_time = time.time()
    if current_time - last_episode_time > 3600:  # 1 hour
        return True

    return False


def episodic_storage_node(state: dict[str, Any]) -> dict[str, Any]:
    """
    Store completed episodes in episodic memory with semantic indexing.

    Args:
        state: CCE Deep Agent state

    Returns:
        Updated state with episodic memory
    """
    try:
        if not should_create_episode(state):
            return state

        working_memory = state.get("working_memory", [])
        if not working_memory:
            return state

        # Summarize working memory into episode
        episode_summary = summarize_working_memory(working_memory)

        # Create episodic memory record
        episode_record = MemoryRecord(
            content=episode_summary,
            memory_type=MemoryType.EPISODIC,
            metadata={
                "episode_id": generate_episode_id(),
                "task_context": extract_task_context(state.get("messages", [])),
                "outcomes": extract_outcomes(working_memory),
                "decisions": extract_decisions(working_memory),
                "working_memory_size": len(working_memory),
                "created_at": time.time(),
            },
            tags=["episode", "conversation_summary"],
        )

        # Store in episodic memory
        episodic_memory = state.get("episodic_memory", [])
        episodic_memory.append(episode_record)
        state["episodic_memory"] = episodic_memory

        # Update episodic index if available
        episodic_index = state.get("episodic_index")
        if episodic_index:
            try:
                episodic_index.add_text(episode_summary, metadata=episode_record.metadata)
                logger.info(f"📚 [EPISODIC MEMORY] Added episode to semantic index")
            except Exception as e:
                logger.warning(f"⚠️ [EPISODIC MEMORY] Failed to update semantic index: {e}")

        # Update statistics
        memory_stats = state.get("memory_stats", {})
        memory_stats["episodic_records"] = memory_stats.get("episodic_records", 0) + 1
        memory_stats["last_episode_created"] = time.time()
        state["memory_stats"] = memory_stats

        # Update episodic stats
        episodic_stats = state.get("episodic_stats", {})
        episodic_stats["total_episodes"] = len(episodic_memory)
        episodic_stats["last_episode_id"] = episode_record.metadata["episode_id"]
        episodic_stats["last_episode_size"] = len(working_memory)
        state["episodic_stats"] = episodic_stats

        logger.info(f"📚 [EPISODIC MEMORY] Created episode: {episode_record.metadata['episode_id']}")
        logger.info(f"   📊 Summary: {len(episode_summary)} characters, {len(working_memory)} working memory records")

    except Exception as e:
        logger.error(f"❌ [EPISODIC MEMORY] Failed to create episode: {e}")

    return state


def extract_task_context_for_search(messages: list[Any]) -> str:
    """
    Extract task context for semantic search.

    Args:
        messages: List of recent messages

    Returns:
        String representation suitable for semantic search
    """
    if not messages:
        return ""

    # Focus on human messages and recent AI responses
    context_parts = []
    for msg in messages[-5:]:  # Last 5 messages
        if hasattr(msg, "content") and msg.content:
            # Handle both string and list content
            content = msg.content
            if isinstance(content, list):
                content = " ".join(str(item) for item in content)
            elif not isinstance(content, str):
                content = str(content)

            # Clean and normalize content
            content = content.strip()
            if content:
                context_parts.append(content)

    return " ".join(context_parts)


def context_injection_node(state: dict[str, Any]) -> dict[str, Any]:
    """
    Inject relevant context from episodic memory based on current task.

    Args:
        state: CCE Deep Agent state

    Returns:
        Updated state with injected context
    """
    try:
        episodic_index = state.get("episodic_index")
        messages = state.get("messages", [])

        if not episodic_index or not messages:
            return state

        # Extract current task context
        current_task = extract_task_context_for_search(messages[-5:])  # Last 5 messages

        if not current_task.strip():
            return state

        # Semantic retrieval from episodic memory
        try:
            relevant_episodes = episodic_index.search(current_task, top_k=3)
        except Exception as e:
            logger.warning(f"⚠️ [CONTEXT INJECTION] Semantic search failed: {e}")
            return state

        if relevant_episodes:
            # Create context injection message
            context_content = "## Relevant Past Experience:\n\n"
            for i, episode in enumerate(relevant_episodes, 1):
                episode_preview = episode[:200] + "..." if len(episode) > 200 else episode
                context_content += f"{i}. {episode_preview}\n\n"

            # Inject as context memory (not added to messages directly)
            context_memory = state.get("context_memory", {})
            context_memory["injected_context"] = context_content
            context_memory["injected_context_timestamp"] = time.time()
            state["context_memory"] = context_memory

            # Update statistics
            memory_stats = state.get("memory_stats", {})
            memory_stats["context_injections"] = memory_stats.get("context_injections", 0) + 1
            memory_stats["last_context_injection"] = time.time()
            state["memory_stats"] = memory_stats

            logger.info(f"💉 [CONTEXT INJECTION] Injected {len(relevant_episodes)} relevant episodes")
            logger.info(f"   🔍 Search query: {current_task[:100]}...")

    except Exception as e:
        logger.error(f"❌ [CONTEXT INJECTION] Failed to inject context: {e}")

    return state


def get_episodic_memory_status(state: dict[str, Any]) -> dict[str, Any]:
    """
    Get status of episodic memory system.

    Args:
        state: CCE Deep Agent state

    Returns:
        Dictionary with episodic memory status information
    """
    episodic_memory = state.get("episodic_memory", [])
    episodic_stats = state.get("episodic_stats", {})
    memory_stats = state.get("memory_stats", {})

    return {
        "episodic_memory_available": len(episodic_memory) > 0,
        "episodic_memory_size": len(episodic_memory),
        "episodic_index_available": state.get("episodic_index") is not None,
        "total_episodes": episodic_stats.get("total_episodes", 0),
        "last_episode_created": memory_stats.get("last_episode_created"),
        "context_injections": memory_stats.get("context_injections", 0),
        "last_context_injection": memory_stats.get("last_context_injection"),
    }


def generate_pattern_id() -> str:
    """Generate a unique pattern ID."""
    return f"pattern_{uuid.uuid4().hex[:8]}_{int(time.time())}"


def task_completed_successfully(state: dict[str, Any]) -> bool:
    """
    Detect if the current task appears to be completed successfully.

    Args:
        state: Current agent state

    Returns:
        True if task appears completed successfully
    """
    working_memory = state.get("working_memory", [])
    if not working_memory:
        return False

    # Look for success indicators in recent working memory
    success_indicators = [
        "completed successfully",
        "task finished",
        "implementation complete",
        "all tests passed",
        "validation successful",
        "phase completed",
        "done",
        "finished",
    ]

    # Check last few memory records for success indicators
    recent_records = working_memory[-5:] if len(working_memory) >= 5 else working_memory

    for record in recent_records:
        # Handle both string and list content
        content = record.content
        if isinstance(content, list):
            content = " ".join(str(item) for item in content)
        elif not isinstance(content, str):
            content = str(content)

        content_lower = content.lower()
        if any(indicator in content_lower for indicator in success_indicators):
            return True

    # Check if we have substantial working memory (indicates significant task completion)
    if len(working_memory) >= PROCEDURAL_LEARNING_THRESHOLD:
        return True

    return False


def analyze_tool_sequences(working_memory: list[MemoryRecord]) -> list[dict[str, Any]]:
    """
    Analyze tool usage sequences from working memory.

    Args:
        working_memory: List of working memory records

    Returns:
        List of tool sequence patterns
    """
    sequences = []
    current_sequence = []
    current_tools = []

    for record in working_memory:
        # Handle both string and list content
        content = record.content
        if isinstance(content, list):
            content = " ".join(str(item) for item in content)
        elif not isinstance(content, str):
            content = str(content)

        content = content.lower()

        # Detect tool usage patterns - check for specific tool names directly
        if "read_file" in content:
            current_tools.append("read_file")
        elif "write_file" in content:
            current_tools.append("write_file")
        elif "edit_file" in content:
            current_tools.append("edit_file")
        elif "ls" in content:
            current_tools.append("ls")
        elif "codebase_search" in content:
            current_tools.append("codebase_search")
        elif "grep" in content:
            current_tools.append("grep")
        elif "tool" in content or "function" in content or "method" in content:
            # Generic tool detection for other tools
            pass

        # Detect task completion or sequence end
        if any(indicator in content for indicator in ["completed", "finished", "done", "success"]):
            if current_tools:
                sequences.append(
                    {
                        "tools": list(set(current_tools)),  # Remove duplicates
                        "task_type": "file_operations"
                        if any(t in current_tools for t in ["read_file", "write_file", "edit_file"])
                        else "analysis",
                        "success_indicators": True,
                        "success_rate": 1.0,  # Simplified - assume successful if we reached completion
                        "conditions": ["task_completion_detected"],
                    }
                )
                current_tools = []

    return sequences


def analyze_decision_patterns(working_memory: list[MemoryRecord]) -> list[dict[str, Any]]:
    """
    Analyze decision patterns from working memory.

    Args:
        working_memory: List of working memory records

    Returns:
        List of decision patterns
    """
    patterns = []

    # Look for decision-making patterns
    decision_keywords = ["decided", "chose", "selected", "determined", "concluded", "recommended"]

    for record in working_memory:
        # Handle both string and list content
        content = record.content
        if isinstance(content, list):
            content = " ".join(str(item) for item in content)
        elif not isinstance(content, str):
            content = str(content)

        content = content.lower()

        for keyword in decision_keywords:
            if keyword in content:
                # Extract decision context (simplified)
                patterns.append(
                    {
                        "description": f"Decision pattern involving {keyword}",
                        "conditions": [f"contains_{keyword}"],
                        "outcomes": ["decision_made"],
                        "success_rate": 1.0,  # Simplified
                    }
                )
                break

    return patterns


def extract_task_patterns(working_memory: list[MemoryRecord]) -> list[dict[str, Any]]:
    """
    Extract successful patterns from working memory.

    Args:
        working_memory: List of working memory records

    Returns:
        List of extracted patterns
    """
    patterns = []

    # Analyze tool usage sequences
    tool_sequences = analyze_tool_sequences(working_memory)
    for sequence in tool_sequences:
        if sequence["success_indicators"]:
            patterns.append(
                {
                    "type": "tool_sequence",
                    "description": f"Successful {sequence['task_type']} using {', '.join(sequence['tools'])}",
                    "tool_sequence": sequence["tools"],
                    "success_rate": sequence["success_rate"],
                    "conditions": sequence["conditions"],
                }
            )

    # Analyze decision patterns
    decision_patterns = analyze_decision_patterns(working_memory)
    for pattern in decision_patterns:
        patterns.append(
            {
                "type": "decision_tree",
                "description": pattern["description"],
                "conditions": pattern["conditions"],
                "outcomes": pattern["outcomes"],
                "success_rate": pattern["success_rate"],
            }
        )

    return patterns


def procedural_learning_node(state: dict[str, Any]) -> dict[str, Any]:
    """
    Extract successful patterns from completed tasks and store in procedural memory.

    Args:
        state: Current agent state

    Returns:
        Updated state with procedural memory patterns
    """
    try:
        if not task_completed_successfully(state):
            return state

        working_memory = state.get("working_memory", [])
        if not working_memory:
            return state

        # Extract successful patterns
        patterns = extract_task_patterns(working_memory)

        if not patterns:
            logger.info("📚 [PROCEDURAL LEARNING] No patterns extracted from working memory")
            return state

        # Get or initialize procedural memory
        procedural_memory = state.get("procedural_memory", [])
        if not procedural_memory:
            procedural_memory = []

        # Create procedural memory records for each pattern
        for pattern in patterns:
            procedural_record = MemoryRecord(
                content=pattern["description"],
                memory_type=MemoryType.PROCEDURAL,
                metadata={
                    "pattern_id": generate_pattern_id(),
                    "pattern_type": pattern["type"],
                    "success_rate": pattern["success_rate"],
                    "tool_sequence": pattern.get("tool_sequence", []),
                    "conditions": pattern.get("conditions", []),
                    "outcomes": pattern.get("outcomes", []),
                    "created_from_episode": state.get("memory_stats", {}).get("last_episode_created"),
                    "working_memory_size": len(working_memory),
                },
            )

            procedural_memory.append(procedural_record)

            # Store in context memory manager if available
            context_memory_manager = state.get("context_memory_manager")
            if context_memory_manager:
                try:
                    context_memory_manager.store_procedural(procedural_record)
                except Exception as e:
                    logger.warning(f"⚠️ [PROCEDURAL LEARNING] Failed to store in context memory manager: {e}")

        # Update state with new procedural memory
        state["procedural_memory"] = procedural_memory

        # Update memory statistics
        memory_stats = state.get("memory_stats", {})
        memory_stats["procedural_patterns"] = memory_stats.get("procedural_patterns", 0) + len(patterns)
        memory_stats["last_pattern_created"] = time.time()
        state["memory_stats"] = memory_stats

        # Update procedural statistics
        procedural_stats = state.get("procedural_stats", {})
        procedural_stats["total_patterns"] = len(procedural_memory)
        procedural_stats["last_pattern_created"] = time.time()
        procedural_stats["pattern_types"] = {}

        # Count pattern types
        for record in procedural_memory:
            pattern_type = record.metadata.get("pattern_type", "unknown")
            procedural_stats["pattern_types"][pattern_type] = procedural_stats["pattern_types"].get(pattern_type, 0) + 1

        state["procedural_stats"] = procedural_stats

        logger.info(f"🔧 [PROCEDURAL LEARNING] Extracted {len(patterns)} patterns from successful task completion")
        logger.info(f"   📊 Total procedural patterns: {len(procedural_memory)}")
        logger.info(f"   🎯 Pattern types: {procedural_stats['pattern_types']}")

    except Exception as e:
        logger.error(f"❌ [PROCEDURAL LEARNING] Failed to extract patterns: {e}")

    return state


def get_procedural_memory_status(state: dict[str, Any]) -> dict[str, Any]:
    """
    Get current status of the procedural memory system.

    Args:
        state: Current agent state

    Returns:
        Dictionary with procedural memory status information
    """
    procedural_memory = state.get("procedural_memory", [])
    procedural_stats = state.get("procedural_stats", {})
    memory_stats = state.get("memory_stats", {})

    return {
        "procedural_memory_available": len(procedural_memory) > 0,
        "procedural_memory_size": len(procedural_memory),
        "procedural_index_available": state.get("procedural_index") is not None,
        "total_patterns": procedural_stats.get("total_patterns", 0),
        "last_pattern_created": memory_stats.get("last_pattern_created"),
        "pattern_types": procedural_stats.get("pattern_types", {}),
        "learning_threshold_met": len(procedural_memory) >= PROCEDURAL_LEARNING_THRESHOLD,
    }
