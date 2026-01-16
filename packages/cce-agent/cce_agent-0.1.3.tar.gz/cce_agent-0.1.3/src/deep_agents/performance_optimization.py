"""
Performance Optimization for CCE Deep Agent

This module provides performance optimization for virtual filesystem operations,
context storage, and retrieval with advanced caching and optimization strategies.
"""

import asyncio
import hashlib
import json
import logging
import time
import weakref
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.deep_agents.state import CCEDeepAgentState

logger = logging.getLogger(__name__)


class CacheStrategy(Enum):
    """Cache strategy types."""

    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live
    SIZE = "size"  # Size-based eviction


class OptimizationLevel(Enum):
    """Optimization levels."""

    NONE = "none"
    BASIC = "basic"
    AGGRESSIVE = "aggressive"
    MAXIMUM = "maximum"


@dataclass
class CacheEntry:
    """Cache entry with metadata."""

    key: str
    value: Any
    created_at: float
    last_accessed: float
    access_count: int = 0
    size_bytes: int = 0
    ttl: float | None = None
    tags: set[str] = field(default_factory=set)


@dataclass
class PerformanceMetrics:
    """Performance metrics for optimization."""

    cache_hit_rate: float = 0.0
    average_access_time: float = 0.0
    total_operations: int = 0
    cache_operations: int = 0
    storage_operations: int = 0
    optimization_savings: float = 0.0
    memory_usage: int = 0
    disk_usage: int = 0


class VirtualFilesystemOptimizer:
    """
    Optimizer for virtual filesystem operations.

    This class provides advanced optimization strategies for virtual filesystem
    operations including intelligent caching, compression, and performance monitoring.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.cache_strategy = CacheStrategy(self.config.get("cache_strategy", "lru"))
        self.max_cache_size = self.config.get("max_cache_size", 1000)
        self.max_memory_mb = self.config.get("max_memory_mb", 100)
        self.compression_enabled = self.config.get("compression_enabled", True)
        self.optimization_level = OptimizationLevel(self.config.get("optimization_level", "basic"))

        # Cache storage
        self.cache: dict[str, CacheEntry] = {}
        self.access_order = deque()  # For LRU
        self.access_counts = defaultdict(int)  # For LFU
        self.size_tracker = 0
        self.memory_usage = 0

        # Performance tracking
        self.metrics = PerformanceMetrics()
        self.operation_times = deque(maxlen=1000)

        # Context optimization
        self.context_cache: dict[str, Any] = {}
        self.context_compression_cache: dict[str, bytes] = {}

        # Weak references for memory management
        self.weak_refs: set[weakref.ref] = set()

    def optimize_context_storage(self, state: "CCEDeepAgentState") -> dict[str, Any]:
        """
        Optimize context storage for performance.

        Args:
            state: CCE Deep Agent state to optimize

        Returns:
            Optimization results
        """
        try:
            start_time = time.time()
            optimizations = {
                "compression_applied": False,
                "duplicates_removed": 0,
                "cache_entries_created": 0,
                "memory_saved": 0,
                "optimization_time": 0.0,
            }

            # Optimize files in virtual filesystem
            if hasattr(state, "files") and state.files:
                original_size = sum(len(str(content)) for content in state.files.values())

                # Remove duplicate content
                content_to_paths = defaultdict(list)
                for path, content in state.files.items():
                    content_hash = hashlib.md5(str(content).encode()).hexdigest()
                    content_to_paths[content_hash].append(path)

                duplicates_removed = 0
                for content_hash, paths in content_to_paths.items():
                    if len(paths) > 1:
                        # Keep first path, replace others with references
                        primary_path = paths[0]
                        for path in paths[1:]:
                            state.files[path] = f"@reference:{primary_path}"
                            duplicates_removed += 1

                optimizations["duplicates_removed"] = duplicates_removed

                # Apply compression if enabled
                if self.compression_enabled and self.optimization_level in [
                    OptimizationLevel.AGGRESSIVE,
                    OptimizationLevel.MAXIMUM,
                ]:
                    compressed_files = {}
                    for path, content in state.files.items():
                        if not content.startswith("@reference:"):
                            compressed_content = self._compress_content(content)
                            if len(compressed_content) < len(str(content)):
                                compressed_files[path] = compressed_content
                                optimizations["compression_applied"] = True
                            else:
                                compressed_files[path] = content
                        else:
                            compressed_files[path] = content

                    state.files = compressed_files

                # Cache frequently accessed files
                for path, content in state.files.items():
                    if not content.startswith("@reference:"):
                        cache_key = f"file:{path}"
                        self._add_to_cache(cache_key, content, tags={"file", "context"})
                        optimizations["cache_entries_created"] += 1

                # Calculate memory savings
                new_size = sum(len(str(content)) for content in state.files.values())
                optimizations["memory_saved"] = original_size - new_size

            # Optimize context memory
            if hasattr(state, "context_memory") and state.context_memory:
                self._optimize_context_memory(state.context_memory)

            optimizations["optimization_time"] = time.time() - start_time
            self.metrics.optimization_savings += optimizations["memory_saved"]

            logger.info(f"Context storage optimized: {optimizations['memory_saved']} bytes saved")
            return optimizations

        except Exception as e:
            logger.error(f"Failed to optimize context storage: {e}")
            return {"error": str(e)}

    def optimize_context_retrieval(self, query: str) -> dict[str, Any]:
        """
        Optimize context retrieval with caching.

        Args:
            query: Query string for context retrieval

        Returns:
            Optimization results
        """
        try:
            start_time = time.time()
            optimizations = {
                "cache_hit": False,
                "query_optimized": False,
                "results_cached": False,
                "retrieval_time": 0.0,
            }

            # Check cache first
            cache_key = f"query:{hashlib.md5(query.encode()).hexdigest()}"
            cached_result = self._get_from_cache(cache_key)

            if cached_result:
                optimizations["cache_hit"] = True
                optimizations["retrieval_time"] = time.time() - start_time
                self.metrics.cache_hit_rate = self._calculate_cache_hit_rate()
                return optimizations

            # Optimize query if needed
            optimized_query = self._optimize_query(query)
            if optimized_query != query:
                optimizations["query_optimized"] = True

            # Simulate context retrieval
            result = self._retrieve_context(optimized_query)

            # Cache results
            self._add_to_cache(cache_key, result, tags={"query", "context"})
            optimizations["results_cached"] = True

            optimizations["retrieval_time"] = time.time() - start_time
            self._update_performance_metrics(optimizations["retrieval_time"])

            return optimizations

        except Exception as e:
            logger.error(f"Failed to optimize context retrieval: {e}")
            return {"error": str(e)}

    def _optimize_context_memory(self, context_memory: dict[str, Any]) -> None:
        """Optimize context memory structure."""
        try:
            # Compress large context entries
            for key, value in context_memory.items():
                if isinstance(value, str) and len(value) > 1000:
                    compressed = self._compress_content(value)
                    if len(compressed) < len(value):
                        context_memory[key] = compressed

            # Remove expired entries
            current_time = time.time()
            expired_keys = []
            for key, value in context_memory.items():
                if isinstance(value, dict) and "expires_at" in value:
                    if current_time > value["expires_at"]:
                        expired_keys.append(key)

            for key in expired_keys:
                del context_memory[key]

        except Exception as e:
            logger.error(f"Failed to optimize context memory: {e}")

    def _optimize_query(self, query: str) -> str:
        """Optimize query for better performance."""
        try:
            # Basic query optimization
            optimized = query.strip().lower()

            # Remove redundant terms
            redundant_terms = ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"]
            words = optimized.split()
            optimized_words = [word for word in words if word not in redundant_terms]

            return " ".join(optimized_words)

        except Exception as e:
            logger.error(f"Failed to optimize query: {e}")
            return query

    def _retrieve_context(self, query: str) -> dict[str, Any]:
        """Simulate context retrieval."""
        # This would integrate with the actual context retrieval system
        return {
            "query": query,
            "results": f"Context for query: {query}",
            "timestamp": time.time(),
            "source": "optimized_retrieval",
        }

    def _compress_content(self, content: str) -> str:
        """Compress content using simple compression."""
        try:
            # Simple compression - in production, use proper compression
            if len(content) < 100:
                return content

            # Remove extra whitespace
            compressed = " ".join(content.split())

            # Simple dictionary compression for repeated patterns
            words = compressed.split()
            word_counts = defaultdict(int)
            for word in words:
                word_counts[word] += 1

            # Replace frequent words with shorter codes
            frequent_words = {
                word: f"#{i}"
                for i, word in enumerate(sorted(word_counts.keys(), key=lambda w: word_counts[w], reverse=True)[:10])
            }

            compressed_words = []
            for word in words:
                if word in frequent_words:
                    compressed_words.append(frequent_words[word])
                else:
                    compressed_words.append(word)

            return " ".join(compressed_words)

        except Exception as e:
            logger.error(f"Failed to compress content: {e}")
            return content

    def _add_to_cache(self, key: str, value: Any, tags: set[str] | None = None) -> None:
        """Add entry to cache with optimization."""
        try:
            # Calculate size
            size_bytes = len(str(value).encode("utf-8"))

            # Check if we need to evict entries
            while (
                len(self.cache) >= self.max_cache_size
                or self.memory_usage + size_bytes > self.max_memory_mb * 1024 * 1024
            ):
                self._evict_cache_entry()

            # Create cache entry
            entry = CacheEntry(
                key=key,
                value=value,
                created_at=time.time(),
                last_accessed=time.time(),
                size_bytes=size_bytes,
                tags=tags or set(),
            )

            # Add to cache
            self.cache[key] = entry
            self.access_order.append(key)
            self.access_counts[key] += 1
            self.size_tracker += size_bytes
            self.memory_usage += size_bytes

            self.metrics.cache_operations += 1

        except Exception as e:
            logger.error(f"Failed to add to cache: {e}")

    def _get_from_cache(self, key: str) -> Any | None:
        """Get entry from cache with optimization."""
        try:
            if key not in self.cache:
                return None

            entry = self.cache[key]

            # Check TTL
            if entry.ttl and time.time() - entry.created_at > entry.ttl:
                del self.cache[key]
                return None

            # Update access information
            entry.last_accessed = time.time()
            entry.access_count += 1

            # Update access order for LRU
            if key in self.access_order:
                self.access_order.remove(key)
            self.access_order.append(key)

            self.metrics.cache_operations += 1
            return entry.value

        except Exception as e:
            logger.error(f"Failed to get from cache: {e}")
            return None

    def _evict_cache_entry(self) -> None:
        """Evict cache entry based on strategy."""
        try:
            if not self.cache:
                return

            if self.cache_strategy == CacheStrategy.LRU:
                # Remove least recently used
                if self.access_order:
                    key_to_remove = self.access_order.popleft()
                    if key_to_remove in self.cache:
                        self._remove_from_cache(key_to_remove)

            elif self.cache_strategy == CacheStrategy.LFU:
                # Remove least frequently used
                if self.access_counts:
                    key_to_remove = min(self.access_counts.keys(), key=lambda k: self.access_counts[k])
                    self._remove_from_cache(key_to_remove)

            elif self.cache_strategy == CacheStrategy.SIZE:
                # Remove largest entry
                key_to_remove = max(self.cache.keys(), key=lambda k: self.cache[k].size_bytes)
                self._remove_from_cache(key_to_remove)

        except Exception as e:
            logger.error(f"Failed to evict cache entry: {e}")

    def _remove_from_cache(self, key: str) -> None:
        """Remove entry from cache."""
        try:
            if key in self.cache:
                entry = self.cache[key]
                self.memory_usage -= entry.size_bytes
                self.size_tracker -= entry.size_bytes

                del self.cache[key]

                if key in self.access_order:
                    self.access_order.remove(key)

                if key in self.access_counts:
                    del self.access_counts[key]

        except Exception as e:
            logger.error(f"Failed to remove from cache: {e}")

    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        try:
            if self.metrics.total_operations == 0:
                return 0.0

            return self.metrics.cache_operations / self.metrics.total_operations

        except Exception as e:
            logger.error(f"Failed to calculate cache hit rate: {e}")
            return 0.0

    def _update_performance_metrics(self, operation_time: float) -> None:
        """Update performance metrics."""
        try:
            self.metrics.total_operations += 1
            self.operation_times.append(operation_time)

            # Update average access time
            if len(self.operation_times) > 0:
                self.metrics.average_access_time = sum(self.operation_times) / len(self.operation_times)

            # Update memory usage
            self.metrics.memory_usage = self.memory_usage

        except Exception as e:
            logger.error(f"Failed to update performance metrics: {e}")

    def get_performance_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics."""
        self.metrics.cache_hit_rate = self._calculate_cache_hit_rate()
        return self.metrics

    def optimize_cache(self) -> dict[str, Any]:
        """Optimize cache performance."""
        try:
            optimizations = {"entries_evicted": 0, "memory_freed": 0, "cache_hit_rate_improved": False}

            # Evict expired entries
            current_time = time.time()
            expired_keys = []

            for key, entry in self.cache.items():
                if entry.ttl and current_time - entry.created_at > entry.ttl:
                    expired_keys.append(key)

            for key in expired_keys:
                self._remove_from_cache(key)
                optimizations["entries_evicted"] += 1

            # Evict low-value entries
            if self.optimization_level in [OptimizationLevel.AGGRESSIVE, OptimizationLevel.MAXIMUM]:
                low_value_keys = []
                for key, entry in self.cache.items():
                    if entry.access_count < 2 and time.time() - entry.last_accessed > 3600:  # 1 hour
                        low_value_keys.append(key)

                for key in low_value_keys:
                    self._remove_from_cache(key)
                    optimizations["entries_evicted"] += 1

            # Calculate memory freed
            optimizations["memory_freed"] = self.metrics.memory_usage - self.memory_usage

            # Check if cache hit rate improved
            old_hit_rate = self.metrics.cache_hit_rate
            new_hit_rate = self._calculate_cache_hit_rate()
            optimizations["cache_hit_rate_improved"] = new_hit_rate > old_hit_rate

            return optimizations

        except Exception as e:
            logger.error(f"Failed to optimize cache: {e}")
            return {"error": str(e)}

    def clear_cache(self) -> None:
        """Clear all cache entries."""
        try:
            self.cache.clear()
            self.access_order.clear()
            self.access_counts.clear()
            self.size_tracker = 0
            self.memory_usage = 0

            logger.info("Cache cleared")

        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        try:
            return {
                "total_entries": len(self.cache),
                "memory_usage_mb": self.memory_usage / (1024 * 1024),
                "cache_hit_rate": self._calculate_cache_hit_rate(),
                "average_entry_size": self.size_tracker / len(self.cache) if self.cache else 0,
                "strategy": self.cache_strategy.value,
                "max_size": self.max_cache_size,
                "max_memory_mb": self.max_memory_mb,
            }

        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {"error": str(e)}


# Global optimizer instance
_optimizer = None


def get_optimizer(config: dict[str, Any] | None = None) -> VirtualFilesystemOptimizer:
    """Get the global optimizer instance."""
    global _optimizer
    if _optimizer is None:
        _optimizer = VirtualFilesystemOptimizer(config)
    return _optimizer
