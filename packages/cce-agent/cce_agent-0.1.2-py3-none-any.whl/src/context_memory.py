"""
Context Memory Manager for CCE Agent

Provides structured memory layers as per ticket #142:
- Working Memory: Current conversation context with intelligent trimming
- Episodic Memory: Summaries of past interactions and key outcomes
- Procedural Memory: Successful patterns, workflows, and best practices

This replaces direct message trimming with a more sophisticated approach
that preserves important context while staying within token limits.

Enhanced with semantic similarity retrieval using embeddings.
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING, Any

from langchain_core.messages import BaseMessage
from langchain_core.messages.utils import trim_messages

if TYPE_CHECKING:
    from src.deep_agents.state import CCEDeepAgentState

logger = logging.getLogger(__name__)

# Import semantic embeddings with graceful fallback
try:
    from src.semantic.embeddings import InMemoryVectorIndex, create_embedding_provider

    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False


class MemoryType(Enum):
    """Types of memory in the CCE system."""

    WORKING = "working"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"


@dataclass
class MemoryRecord:
    """A single memory record with metadata."""

    content: str
    memory_type: MemoryType
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    relevance_score: float = 1.0


@dataclass
class WorkingMemory:
    """Current conversation context with metadata."""

    messages: list[BaseMessage] = field(default_factory=list)
    max_tokens: int = 800000
    last_trimmed: datetime | None = None
    trim_count: int = 0


class ContextWindowManager:
    """
    Context window manager optimized for deep agents patterns.

    This class provides advanced context window management with optimization
    strategies for deep agents workflows and virtual filesystem integration.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.max_context_tokens = self.config.get("max_context_tokens", 800000)
        self.optimization_level = self.config.get("optimization_level", "basic")
        self.compression_enabled = self.config.get("compression_enabled", True)
        self.context_cache = {}
        self.optimization_stats = {"compressions_applied": 0, "contexts_optimized": 0, "tokens_saved": 0}

    def optimize_for_deep_agents(self, state: "CCEDeepAgentState") -> dict[str, Any]:
        """
        Optimize context window for deep agents patterns.

        Args:
            state: CCE Deep Agent state to optimize

        Returns:
            Optimization results
        """
        try:
            optimizations = {
                "context_compressed": False,
                "tokens_saved": 0,
                "optimization_applied": False,
                "performance_improved": False,
            }

            # Optimize messages context
            if hasattr(state, "messages") and state.messages:
                original_token_count = self._estimate_tokens(state.messages)

                # Apply context compression
                if self.compression_enabled:
                    compressed_messages = self._compress_messages(state.messages)
                    if len(compressed_messages) < len(state.messages):
                        state.messages = compressed_messages
                        optimizations["context_compressed"] = True
                        optimizations["tokens_saved"] = original_token_count - self._estimate_tokens(state.messages)

                # Apply deep agents specific optimizations
                if self.optimization_level in ["aggressive", "maximum"]:
                    optimized_messages = self._apply_deep_agents_optimizations(state.messages)
                    if optimized_messages != state.messages:
                        state.messages = optimized_messages
                        optimizations["optimization_applied"] = True

            # Optimize virtual filesystem context
            if hasattr(state, "files") and state.files:
                self._optimize_virtual_filesystem_context(state.files)

            # Update statistics
            self.optimization_stats["contexts_optimized"] += 1
            self.optimization_stats["tokens_saved"] += optimizations["tokens_saved"]

            if optimizations["context_compressed"] or optimizations["optimization_applied"]:
                optimizations["performance_improved"] = True

            return optimizations

        except Exception as e:
            logger.error(f"Failed to optimize context for deep agents: {e}")
            return {"error": str(e)}

    def _estimate_tokens(self, messages: list[BaseMessage]) -> int:
        """Estimate token count for messages."""
        try:
            total_tokens = 0
            for message in messages:
                content = str(message.content) if hasattr(message, "content") else str(message)
                total_tokens += len(content.split()) * 1.3  # Rough estimation
            return int(total_tokens)
        except Exception:
            return 0

    def _compress_messages(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Compress messages for better context utilization."""
        try:
            compressed = []
            for message in messages:
                if hasattr(message, "content"):
                    content = str(message.content)
                    if len(content) > 1000:  # Only compress long messages
                        compressed_content = self._compress_content(content)
                        if len(compressed_content) < len(content):
                            # Create new message with compressed content
                            new_message = type(message)(content=compressed_content)
                            compressed.append(new_message)
                            self.optimization_stats["compressions_applied"] += 1
                        else:
                            compressed.append(message)
                    else:
                        compressed.append(message)
                else:
                    compressed.append(message)
            return compressed
        except Exception as e:
            logger.error(f"Failed to compress messages: {e}")
            return messages

    def _compress_content(self, content: str) -> str:
        """Compress content using simple compression."""
        try:
            # Remove extra whitespace
            compressed = " ".join(content.split())

            # Remove redundant phrases
            redundant_phrases = [
                "I understand that",
                "Let me help you with",
                "I can help you",
                "I'll help you",
                "I will help you",
            ]

            for phrase in redundant_phrases:
                compressed = compressed.replace(phrase, "")

            return compressed.strip()
        except Exception:
            return content

    def _apply_deep_agents_optimizations(self, messages: list[BaseMessage]) -> list[BaseMessage]:
        """Apply deep agents specific optimizations."""
        try:
            optimized = []
            for message in messages:
                if hasattr(message, "content"):
                    content = str(message.content)

                    # Optimize for deep agents patterns
                    if "tool_calls" in content.lower():
                        # Compress tool call information
                        optimized_content = self._optimize_tool_calls(content)
                        if optimized_content != content:
                            new_message = type(message)(content=optimized_content)
                            optimized.append(new_message)
                        else:
                            optimized.append(message)
                    else:
                        optimized.append(message)
                else:
                    optimized.append(message)
            return optimized
        except Exception as e:
            logger.error(f"Failed to apply deep agents optimizations: {e}")
            return messages

    def _optimize_tool_calls(self, content: str) -> str:
        """Optimize tool call content for better context utilization."""
        try:
            # This would implement specific optimizations for tool calls
            # For now, return the original content
            return content
        except Exception:
            return content

    def _optimize_virtual_filesystem_context(self, files: dict[str, str]) -> None:
        """Optimize virtual filesystem context."""
        try:
            # Remove empty files
            empty_files = [path for path, content in files.items() if not content.strip()]
            for path in empty_files:
                del files[path]

            # Compress large files
            for path, content in files.items():
                if len(content) > 5000:  # Large file threshold
                    compressed_content = self._compress_content(content)
                    if len(compressed_content) < len(content):
                        files[path] = compressed_content
        except Exception as e:
            logger.error(f"Failed to optimize virtual filesystem context: {e}")

    def get_optimization_stats(self) -> dict[str, Any]:
        """Get optimization statistics."""
        return self.optimization_stats.copy()


class ContextMemoryManager:
    """
    Manages the three-layer memory system for CCE Agent.

    - Working Memory: Current conversation messages with intelligent trimming
    - Episodic Memory: Summaries of past conversations and key outcomes
    - Procedural Memory: Successful patterns and reusable workflows

    Enhanced with semantic similarity retrieval using embeddings and deep agents optimization.
    """

    def __init__(
        self,
        max_episodic_records: int = 1000,
        max_procedural_records: int = 500,
        enable_semantic_retrieval: bool = True,
        embedding_provider: str = "auto",
    ):
        self.logger = logging.getLogger(__name__)

        # Initialize memory layers
        self.working = WorkingMemory()
        self.episodic_memory: list[MemoryRecord] = []
        self.procedural_memory: list[MemoryRecord] = []

        # Configuration
        self.max_episodic_records = max_episodic_records
        self.max_procedural_records = max_procedural_records
        self.enable_semantic_retrieval = enable_semantic_retrieval and SEMANTIC_AVAILABLE

        # Initialize semantic retrieval if available
        self.episodic_index = None
        self.procedural_index = None

        if self.enable_semantic_retrieval:
            try:
                provider = create_embedding_provider(embedding_provider)
                self.episodic_index = InMemoryVectorIndex(provider)
                self.procedural_index = InMemoryVectorIndex(provider)
                self.logger.info(f"🔍 Semantic retrieval enabled with {provider.get_model_name()}")
            except Exception as e:
                self.logger.warning(f"Failed to initialize semantic retrieval: {e}")
                self.enable_semantic_retrieval = False

        # Audit trail
        self.audit_log: list[dict[str, Any]] = []

        self.logger.info(
            f"🧠 ContextMemoryManager initialized - "
            f"Episodic: {max_episodic_records} records, "
            f"Procedural: {max_procedural_records} records, "
            f"Semantic: {self.enable_semantic_retrieval}"
        )

    def append_working(self, messages: list[BaseMessage]) -> None:
        """
        Append messages to working memory.

        Args:
            messages: Messages to add to working memory
        """
        if not messages:
            return

        self.working.messages.extend(messages)

        # Log the addition
        self._log_audit(
            "append_working", {"message_count": len(messages), "total_working_messages": len(self.working.messages)}
        )

        self.logger.debug(f"📝 Added {len(messages)} messages to working memory (total: {len(self.working.messages)})")

    def get_working_messages(self, max_tokens: int | None = None) -> list[BaseMessage]:
        """
        Get working memory messages, trimmed if necessary.

        Args:
            max_tokens: Optional token limit override

        Returns:
            Trimmed messages that fit within context window
        """
        if not self.working.messages:
            return []

        target_max_tokens = max_tokens or self.working.max_tokens

        try:
            # Use LangChain's trim_messages for consistent behavior
            # Note: For standalone testing, we'll use a simple fallback
            # In production, the agent will provide the proper token_counter
            from langchain_openai import ChatOpenAI

            try:
                # Try to use a token counter if available
                token_counter = ChatOpenAI(model="gpt-3.5-turbo")
                trimmed = trim_messages(
                    self.working.messages,
                    strategy="last",
                    token_counter=token_counter,
                    max_tokens=target_max_tokens,
                    include_system=True,
                    start_on="human",
                    end_on=("human", "tool"),
                    allow_partial=False,
                )
            except Exception:
                # Fallback: simple truncation if no token counter available
                message_count = len(self.working.messages)
                # Keep last 80% of messages as a simple approximation
                keep_count = max(1, int(message_count * 0.8))
                trimmed = self.working.messages[-keep_count:]

            # Track trimming statistics
            original_count = len(self.working.messages)
            trimmed_count = len(trimmed)

            if trimmed_count < original_count:
                self.working.last_trimmed = datetime.now(UTC)
                self.working.trim_count += 1

                self._log_audit(
                    "trim_working_memory",
                    {
                        "original_count": original_count,
                        "trimmed_count": trimmed_count,
                        "tokens_limit": target_max_tokens,
                        "trim_count": self.working.trim_count,
                    },
                )

                self.logger.info(
                    f"🔧 Trimmed working memory: {original_count} → {trimmed_count} messages "
                    f"(within {target_max_tokens} tokens)"
                )

            return trimmed

        except Exception as e:
            self.logger.warning(f"Failed to trim working memory: {e}. Using original messages.")
            return self.working.messages

    def promote_to_episodic(
        self, summary: str, metadata: dict[str, Any] | None = None, tags: list[str] | None = None
    ) -> None:
        """
        Promote a summary to episodic memory.

        Args:
            summary: Summary of the interaction or key outcome
            metadata: Optional metadata about the context
            tags: Optional tags for categorization
        """
        record = MemoryRecord(
            content=summary, memory_type=MemoryType.EPISODIC, metadata=metadata or {}, tags=tags or []
        )

        self.episodic_memory.append(record)

        # Add to semantic index if available
        if self.enable_semantic_retrieval and self.episodic_index:
            try:
                index_metadata = {
                    "memory_type": "episodic",
                    "timestamp": record.timestamp.isoformat(),
                    "tags": tags or [],
                    **(metadata or {}),
                }
                self.episodic_index.add_text(summary, index_metadata)
                self.logger.debug(f"🔍 Added episodic memory to semantic index")
            except Exception as e:
                self.logger.warning(f"Failed to add episodic memory to semantic index: {e}")

        # Maintain size limits
        if len(self.episodic_memory) > self.max_episodic_records:
            # Remove oldest records beyond limit
            removed_count = len(self.episodic_memory) - self.max_episodic_records
            self.episodic_memory = self.episodic_memory[removed_count:]
            self.logger.info(f"🗑️ Removed {removed_count} old episodic records to maintain limit")

        self._log_audit(
            "promote_to_episodic",
            {
                "summary_length": len(summary),
                "total_episodic_records": len(self.episodic_memory),
                "metadata_keys": list(metadata.keys()) if metadata else [],
                "tags": tags or [],
            },
        )

        self.logger.debug(f"📚 Promoted to episodic memory: {summary[:100]}...")

    def record_procedural(
        self, pattern: str, context: str, success_metrics: dict[str, Any] | None = None, tags: list[str] | None = None
    ) -> None:
        """
        Record a successful procedural pattern.

        Args:
            pattern: Description of the successful approach/pattern
            context: Context in which this pattern was successful
            success_metrics: Optional metrics demonstrating success
            tags: Optional tags for categorization
        """
        metadata = {"context": context, "success_metrics": success_metrics or {}}

        record = MemoryRecord(content=pattern, memory_type=MemoryType.PROCEDURAL, metadata=metadata, tags=tags or [])

        self.procedural_memory.append(record)

        # Add to semantic index if available
        if self.enable_semantic_retrieval and self.procedural_index:
            try:
                index_metadata = {
                    "memory_type": "procedural",
                    "timestamp": record.timestamp.isoformat(),
                    "context": context,
                    "success_metrics": success_metrics or {},
                    "tags": tags or [],
                }
                self.procedural_index.add_text(pattern, index_metadata)
                self.logger.debug(f"🔍 Added procedural pattern to semantic index")
            except Exception as e:
                self.logger.warning(f"Failed to add procedural pattern to semantic index: {e}")

        # Maintain size limits
        if len(self.procedural_memory) > self.max_procedural_records:
            # Remove oldest records beyond limit
            removed_count = len(self.procedural_memory) - self.max_procedural_records
            self.procedural_memory = self.procedural_memory[removed_count:]
            self.logger.info(f"🗑️ Removed {removed_count} old procedural records to maintain limit")

        self._log_audit(
            "record_procedural",
            {
                "pattern_length": len(pattern),
                "context_length": len(context),
                "total_procedural_records": len(self.procedural_memory),
                "success_metrics": success_metrics or {},
                "tags": tags or [],
            },
        )

        self.logger.debug(f"⚙️ Recorded procedural pattern: {pattern[:100]}...")

    def retrieve(
        self, query: str, memory_types: list[MemoryType] | None = None, limit: int = 10, use_semantic: bool = True
    ) -> list[MemoryRecord]:
        """
        Retrieve relevant memories based on query.

        Uses semantic similarity when available, falls back to keyword matching.

        Args:
            query: Query string to match against
            memory_types: Types of memory to search (default: all types)
            limit: Maximum number of records to return
            use_semantic: Whether to use semantic similarity (if available)

        Returns:
            List of relevant memory records, sorted by relevance
        """
        if not query:
            return []

        search_types = memory_types or list(MemoryType)

        # Try semantic retrieval first if available
        if self.enable_semantic_retrieval and use_semantic:
            return self._retrieve_semantic(query, search_types, limit)

        # Fallback to keyword-based retrieval
        return self._retrieve_keyword(query, search_types, limit)

    def _retrieve_semantic(self, query: str, memory_types: list[MemoryType], limit: int) -> list[MemoryRecord]:
        """Retrieve memories using semantic similarity."""
        all_results = []

        # Search episodic memory
        if MemoryType.EPISODIC in memory_types and self.episodic_index:
            try:
                episodic_results = self.episodic_index.search(query, top_k=limit)
                for result in episodic_results:
                    # Find corresponding memory record
                    for record in self.episodic_memory:
                        if record.content == result.text:
                            record.relevance_score = result.similarity
                            all_results.append(record)
                            break
            except Exception as e:
                self.logger.warning(f"Semantic search failed for episodic memory: {e}")

        # Search procedural memory
        if MemoryType.PROCEDURAL in memory_types and self.procedural_index:
            try:
                procedural_results = self.procedural_index.search(query, top_k=limit)
                for result in procedural_results:
                    # Find corresponding memory record
                    for record in self.procedural_memory:
                        if record.content == result.text:
                            record.relevance_score = result.similarity
                            all_results.append(record)
                            break
            except Exception as e:
                self.logger.warning(f"Semantic search failed for procedural memory: {e}")

        # Sort by relevance and limit results
        all_results.sort(key=lambda r: r.relevance_score, reverse=True)
        return all_results[:limit]

    def _retrieve_keyword(self, query: str, memory_types: list[MemoryType], limit: int) -> list[MemoryRecord]:
        """Retrieve memories using keyword matching (fallback)."""
        all_records = []

        # Collect records from specified memory types
        for memory_type in memory_types:
            if memory_type == MemoryType.EPISODIC:
                all_records.extend(self.episodic_memory)
            elif memory_type == MemoryType.PROCEDURAL:
                all_records.extend(self.procedural_memory)

        # Simple keyword matching
        query_lower = query.lower()
        matching_records = []

        for record in all_records:
            relevance = 0.0
            content_lower = record.content.lower()

            # Basic keyword matching
            query_words = query_lower.split()
            content_words = content_lower.split()

            # Count word matches
            matches = sum(1 for word in query_words if word in content_words)
            if matches > 0:
                relevance = matches / len(query_words)

                # Boost relevance for tag matches
                for tag in record.tags:
                    if tag.lower() in query_lower:
                        relevance += 0.2

                record.relevance_score = relevance
                matching_records.append(record)

        # Sort by relevance and apply limit
        matching_records.sort(key=lambda r: r.relevance_score, reverse=True)
        results = matching_records[:limit]

        if results:
            self.logger.debug(f"🔍 Retrieved {len(results)} memories using keyword matching for query: {query[:50]}...")

        return results

    def clear_working_memory(self) -> int:
        """
        Clear working memory and return count of cleared messages.

        Returns:
            Number of messages that were cleared
        """
        cleared_count = len(self.working.messages)
        self.working = WorkingMemory(max_tokens=self.working.max_tokens)

        self._log_audit("clear_working_memory", {"cleared_count": cleared_count})

        self.logger.info(f"🧹 Cleared {cleared_count} messages from working memory")
        return cleared_count

    def get_memory_stats(self) -> dict[str, Any]:
        """
        Get statistics about current memory usage.

        Returns:
            Dictionary with memory statistics
        """
        stats = {
            "working_messages": len(self.working.messages),
            "working_max_tokens": self.working.max_tokens,
            "working_trim_count": self.working.trim_count,
            "working_last_trimmed": self.working.last_trimmed.isoformat() if self.working.last_trimmed else None,
            "episodic_records": len(self.episodic_memory),
            "episodic_max": self.max_episodic_records,
            "procedural_records": len(self.procedural_memory),
            "procedural_max": self.max_procedural_records,
            "audit_log_entries": len(self.audit_log),
            "semantic_retrieval_enabled": self.enable_semantic_retrieval,
        }

        # Add semantic index stats if available
        if self.enable_semantic_retrieval:
            stats["episodic_index_size"] = self.episodic_index.size() if self.episodic_index else 0
            stats["procedural_index_size"] = self.procedural_index.size() if self.procedural_index else 0

        return stats

    def _log_audit(self, action: str, details: dict[str, Any]) -> None:
        """
        Log an action to the audit trail.

        Args:
            action: Name of the action performed
            details: Details about the action
        """
        audit_entry = {"timestamp": datetime.now(UTC).isoformat(), "action": action, "details": details}

        self.audit_log.append(audit_entry)

        # Keep audit log from growing too large
        max_audit_entries = 10000
        if len(self.audit_log) > max_audit_entries:
            removed_count = len(self.audit_log) - max_audit_entries
            self.audit_log = self.audit_log[removed_count:]

    def export_memories(self, filepath: str) -> None:
        """
        Export memories to a JSON file for backup/analysis.

        Args:
            filepath: Path to save the export file
        """
        export_data = {
            "timestamp": datetime.now(UTC).isoformat(),
            "working_memory": {
                "message_count": len(self.working.messages),
                "max_tokens": self.working.max_tokens,
                "trim_count": self.working.trim_count,
            },
            "episodic_memory": [
                {
                    "content": record.content,
                    "timestamp": record.timestamp.isoformat(),
                    "metadata": record.metadata,
                    "tags": record.tags,
                }
                for record in self.episodic_memory
            ],
            "procedural_memory": [
                {
                    "content": record.content,
                    "timestamp": record.timestamp.isoformat(),
                    "metadata": record.metadata,
                    "tags": record.tags,
                }
                for record in self.procedural_memory
            ],
            "stats": self.get_memory_stats(),
        }

        with open(filepath, "w") as f:
            json.dump(export_data, f, indent=2)

        self.logger.info(f"💾 Exported memories to {filepath}")

        self._log_audit(
            "export_memories",
            {
                "filepath": filepath,
                "episodic_count": len(self.episodic_memory),
                "procedural_count": len(self.procedural_memory),
            },
        )

    def store_to_virtual_filesystem(self, state: dict[str, Any], record: MemoryRecord) -> None:
        """
        Store memory record in virtual filesystem for cross-agent access.

        Args:
            state: Deep agent state containing virtual filesystem
            record: Memory record to store
        """
        try:
            # Ensure virtual filesystem exists in state
            if "context_files" not in state:
                state["context_files"] = {}

            # Create structured path for memory record
            memory_path = f"memory/{record.memory_type.value}/{record.timestamp.strftime('%Y%m%d_%H%M%S')}_{record.id if hasattr(record, 'id') else 'record'}.json"

            # Convert record to JSON-serializable format
            record_data = {
                "content": record.content,
                "memory_type": record.memory_type.value,
                "timestamp": record.timestamp.isoformat(),
                "metadata": record.metadata,
                "tags": record.tags,
                "relevance_score": record.relevance_score,
            }

            # Store in virtual filesystem
            state["context_files"][memory_path] = json.dumps(record_data, indent=2)

            self.logger.debug(f"📁 Stored memory record to virtual filesystem: {memory_path}")

            self._log_audit(
                "store_to_virtual_filesystem",
                {
                    "memory_path": memory_path,
                    "memory_type": record.memory_type.value,
                    "content_length": len(record.content),
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to store memory record to virtual filesystem: {e}")

    def retrieve_from_virtual_filesystem(
        self, state: dict[str, Any], query: str, memory_types: list[MemoryType] | None = None
    ) -> list[MemoryRecord]:
        """
        Retrieve context from virtual filesystem for cross-agent access.

        Args:
            state: Deep agent state containing virtual filesystem
            query: Query string to match against
            memory_types: Types of memory to search (default: all types)

        Returns:
            List of relevant memory records from virtual filesystem
        """
        try:
            if "context_files" not in state or not state["context_files"]:
                return []

            search_types = memory_types or list(MemoryType)
            results = []

            # Search through virtual filesystem memory records
            for file_path, content in state["context_files"].items():
                if not file_path.startswith("memory/"):
                    continue

                try:
                    # Parse memory record from virtual filesystem
                    record_data = json.loads(content)
                    memory_type = MemoryType(record_data["memory_type"])

                    # Filter by memory type if specified
                    if memory_type not in search_types:
                        continue

                    # Create MemoryRecord object
                    record = MemoryRecord(
                        content=record_data["content"],
                        memory_type=memory_type,
                        timestamp=datetime.fromisoformat(record_data["timestamp"]),
                        metadata=record_data.get("metadata", {}),
                        tags=record_data.get("tags", []),
                        relevance_score=record_data.get("relevance_score", 1.0),
                    )

                    # Simple keyword matching for now (could be enhanced with semantic search)
                    if query.lower() in record.content.lower():
                        results.append(record)

                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    self.logger.warning(f"Failed to parse memory record from {file_path}: {e}")
                    continue

            # Sort by relevance score and timestamp
            results.sort(key=lambda r: (r.relevance_score, r.timestamp), reverse=True)

            self.logger.debug(f"🔍 Retrieved {len(results)} memory records from virtual filesystem for query: {query}")

            self._log_audit(
                "retrieve_from_virtual_filesystem",
                {"query": query, "memory_types": [mt.value for mt in search_types], "results_count": len(results)},
            )

            return results

        except Exception as e:
            self.logger.error(f"Failed to retrieve from virtual filesystem: {e}")
            return []

    def sync_with_virtual_filesystem(self, state: dict[str, Any]) -> None:
        """
        Sync all memory records to virtual filesystem for cross-agent access.

        Args:
            state: Deep agent state containing virtual filesystem
        """
        try:
            # Ensure virtual filesystem exists
            if "context_files" not in state:
                state["context_files"] = {}

            # Sync episodic memory
            for record in self.episodic_memory:
                self.store_to_virtual_filesystem(state, record)

            # Sync procedural memory
            for record in self.procedural_memory:
                self.store_to_virtual_filesystem(state, record)

            self.logger.info(
                f"🔄 Synced {len(self.episodic_memory)} episodic and {len(self.procedural_memory)} procedural records to virtual filesystem"
            )

            self._log_audit(
                "sync_with_virtual_filesystem",
                {"episodic_count": len(self.episodic_memory), "procedural_count": len(self.procedural_memory)},
            )

        except Exception as e:
            self.logger.error(f"Failed to sync with virtual filesystem: {e}")
