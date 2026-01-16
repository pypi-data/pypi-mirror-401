"""
Prompt Cache for CCE Agent

Provides hash-based caching of LLM calls to reduce token usage and improve
response times for repeated queries. Integrates with TokenTrackingLLM.

Cache keys are generated from:
- Model name and parameters
- Message content (excluding timestamps and dynamic IDs)
- Tool configuration

Cache can be disabled via FEATURE_PROMPT_CACHE environment variable.
"""

import hashlib
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol, runtime_checkable

from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable


@runtime_checkable
class LLMProtocol(Protocol):
    """Protocol for LLM objects that can be cached."""

    def invoke(self, messages: list[BaseMessage], **kwargs) -> Any:
        """Invoke the LLM with messages."""
        ...

    def bind_tools(self, tools: list[Any], **kwargs: Any) -> "LLMProtocol":
        """Bind tools to the LLM."""
        ...


@dataclass
class CacheEntry:
    """A single cache entry with metadata."""

    response: Any
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    hit_count: int = 0
    model: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class PromptCache:
    """
    Hash-based cache for LLM responses.

    Caches responses based on normalized prompt content and model configuration.
    Provides statistics and configurable TTL for cache entries.
    """

    def __init__(self, enabled: bool | None = None, max_entries: int = 10000, ttl_hours: int = 24):
        """
        Initialize the prompt cache.

        Args:
            enabled: Whether caching is enabled (None = check env var)
            max_entries: Maximum number of cache entries to maintain
            ttl_hours: Time to live for cache entries in hours
        """
        # Check configuration defaults if not explicitly set
        if enabled is None:
            try:
                from src.config_loader import get_config

                enabled = bool(get_config().defaults.prompt_cache)
            except Exception:
                enabled = os.getenv("FEATURE_PROMPT_CACHE", "0") == "1"

        self.enabled = enabled
        self.max_entries = max_entries
        self.ttl = timedelta(hours=ttl_hours)

        # Cache storage
        self.cache: dict[str, CacheEntry] = {}

        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0

        self.logger = logging.getLogger(__name__)

        if self.enabled:
            self.logger.info(f"💾 PromptCache initialized (max_entries={max_entries}, ttl={ttl_hours}h)")
        else:
            self.logger.info("💾 PromptCache initialized but DISABLED")

    def _normalize_messages(self, messages: list[BaseMessage]) -> list[dict[str, Any]]:
        """
        Normalize messages for consistent cache key generation.

        Removes dynamic elements like timestamps and UUIDs that would
        prevent cache hits for functionally identical requests.

        Args:
            messages: Original messages

        Returns:
            Normalized message representation
        """
        normalized = []

        for msg in messages:
            # Extract core content
            content = msg.content if hasattr(msg, "content") else str(msg)

            # Create normalized representation
            msg_dict = {"type": msg.__class__.__name__, "content": content}

            # Include tool calls if present (but normalize IDs)
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                normalized_calls = []
                for tool_call in msg.tool_calls:
                    normalized_call = {
                        "name": tool_call.get("name", ""),
                        "args": tool_call.get("args", {}),
                        # Omit call ID as it's always unique
                    }
                    normalized_calls.append(normalized_call)
                msg_dict["tool_calls"] = normalized_calls

            normalized.append(msg_dict)

        return normalized

    def _generate_cache_key(self, messages: list[BaseMessage], model: str, **kwargs) -> str:
        """
        Generate a cache key for the given input.

        Args:
            messages: Input messages
            model: Model name
            **kwargs: Additional model parameters

        Returns:
            Cache key string
        """
        # Normalize messages
        normalized_messages = self._normalize_messages(messages)

        # Create cache key components
        key_data = {
            "model": model,
            "messages": normalized_messages,
            "kwargs": {k: v for k, v in kwargs.items() if k not in ["callbacks"]},  # Exclude callbacks from key
        }

        # Generate hash
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()

    def get(self, messages: list[BaseMessage], model: str, **kwargs) -> Any | None:
        """
        Get cached response if available and valid.

        Args:
            messages: Input messages
            model: Model name
            **kwargs: Additional parameters

        Returns:
            Cached response or None if not found/expired
        """
        if not self.enabled:
            return None

        cache_key = self._generate_cache_key(messages, model, **kwargs)

        if cache_key not in self.cache:
            self.misses += 1
            return None

        entry = self.cache[cache_key]

        # Check if entry is expired
        if datetime.now(UTC) - entry.timestamp > self.ttl:
            del self.cache[cache_key]
            self.evictions += 1
            self.misses += 1
            return None

        # Update hit statistics
        entry.hit_count += 1
        self.hits += 1

        self.logger.debug(f"🎯 Cache HIT for model {model} (hits={entry.hit_count})")
        return entry.response

    def put(
        self,
        messages: list[BaseMessage],
        model: str,
        response: Any,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        **kwargs,
    ) -> None:
        """
        Store response in cache.

        Args:
            messages: Input messages
            model: Model name
            response: LLM response to cache
            prompt_tokens: Number of prompt tokens used
            completion_tokens: Number of completion tokens generated
            **kwargs: Additional parameters
        """
        if not self.enabled:
            return

        cache_key = self._generate_cache_key(messages, model, **kwargs)

        # Create cache entry
        entry = CacheEntry(
            response=response,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )

        self.cache[cache_key] = entry

        # Enforce size limits
        if len(self.cache) > self.max_entries:
            # Remove oldest entries (simple FIFO eviction)
            oldest_keys = sorted(self.cache.keys(), key=lambda k: self.cache[k].timestamp)[:100]
            for old_key in oldest_keys:
                del self.cache[old_key]
                self.evictions += 1

        self.logger.debug(f"💾 Cached response for model {model} ({prompt_tokens + completion_tokens} tokens)")

    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate cache entries matching a pattern.

        Args:
            pattern: Pattern to match against message content

        Returns:
            Number of entries invalidated
        """
        if not self.enabled:
            return 0

        pattern_lower = pattern.lower()
        keys_to_remove = []

        for key, entry in self.cache.items():
            # Check if any message content contains the pattern
            try:
                # Reconstruct normalized messages to check content
                key_data = json.loads(key)  # Won't work with hash, need different approach
                # For now, just return 0 as this is a complex operation
                # In production, we'd need to store searchable metadata
                pass
            except:
                pass

        for key in keys_to_remove:
            del self.cache[key]
            self.evictions += 1

        if keys_to_remove:
            self.logger.info(f"🗑️ Invalidated {len(keys_to_remove)} cache entries matching '{pattern}'")

        return len(keys_to_remove)

    def clear(self) -> int:
        """
        Clear all cache entries.

        Returns:
            Number of entries cleared
        """
        cleared_count = len(self.cache)
        self.cache.clear()
        self.evictions += cleared_count

        if cleared_count > 0:
            self.logger.info(f"🧹 Cleared {cleared_count} cache entries")

        return cleared_count

    def get_stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0

        # Calculate token savings
        total_cached_tokens = sum(
            entry.total_tokens * (entry.hit_count - 1) for entry in self.cache.values() if entry.hit_count > 1
        )

        return {
            "enabled": self.enabled,
            "total_entries": len(self.cache),
            "max_entries": self.max_entries,
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "hit_rate": hit_rate,
            "total_requests": total_requests,
            "tokens_saved": total_cached_tokens,
            "ttl_hours": self.ttl.total_seconds() / 3600,
        }

    def cleanup_expired(self) -> int:
        """
        Remove expired cache entries.

        Returns:
            Number of entries removed
        """
        if not self.enabled:
            return 0

        now = datetime.now(UTC)
        expired_keys = [key for key, entry in self.cache.items() if now - entry.timestamp > self.ttl]

        for key in expired_keys:
            del self.cache[key]
            self.evictions += 1

        if expired_keys:
            self.logger.debug(f"🕐 Removed {len(expired_keys)} expired cache entries")

        return len(expired_keys)


class CachedLLMWrapper(Runnable):
    """
    Wrapper that adds caching to any LLM with an invoke method.

    Designed to work seamlessly with TokenTrackingLLM and other LangChain LLMs.
    """

    def __init__(self, llm: LLMProtocol, cache: PromptCache | None = None):
        """
        Initialize the cached LLM wrapper.

        Args:
            llm: The underlying LLM to wrap
            cache: Optional cache instance (creates new one if None)
        """
        self.llm = llm
        self.cache = cache or PromptCache()
        self.logger = logging.getLogger(__name__)

    @property
    def profile(self) -> Any:
        """Expose model profile if the underlying LLM provides one."""
        return getattr(self.llm, "profile", None)

    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attributes to the underlying LLM."""
        return getattr(self.llm, name)

    def invoke(self, input, config=None, **kwargs) -> Any:
        """
        Invoke the LLM with caching.

        Args:
            input: Messages to send to the LLM (List[BaseMessage])
            config: Optional configuration
            **kwargs: Additional arguments for the LLM

        Returns:
            LLM response (from cache or fresh)
        """
        # Handle both direct message lists and LangChain input formats
        if isinstance(input, list):
            messages = input
        else:
            # For LangChain compatibility, input might be a single message or other format
            messages = input if isinstance(input, list) else [input]
        model_name = getattr(self.llm, "model", "unknown")

        # Check cache first
        cached_response = self.cache.get(messages, model_name, **kwargs)
        if cached_response is not None:
            return cached_response

        # Call underlying LLM
        response = self.llm.invoke(messages, config=config, **kwargs)

        # Extract token usage if available
        prompt_tokens = 0
        completion_tokens = 0

        if hasattr(self.llm, "callback_handler"):
            # For TokenTrackingLLM, get the latest usage
            usage_records = self.llm.callback_handler.get_usage_records()
            if usage_records:
                latest_usage = usage_records[-1]
                prompt_tokens = latest_usage.prompt_tokens
                completion_tokens = latest_usage.completion_tokens

        # Store in cache
        self.cache.put(messages, model_name, response, prompt_tokens, completion_tokens, **kwargs)

        return response

    def bind_tools(self, tools: list[Any], **kwargs: Any) -> "CachedLLMWrapper":
        """
        Bind tools and return a new wrapped instance.

        Args:
            tools: Tools to bind

        Returns:
            New CachedLLMWrapper with tools bound
        """
        bound_llm = self.llm.bind_tools(tools, **kwargs)
        return CachedLLMWrapper(bound_llm, self.cache)

    def clear_usage_records(self) -> None:
        """Clear all recorded token usage (delegates to underlying LLM)."""
        if hasattr(self.llm, "clear_usage_records"):
            self.llm.clear_usage_records()

    def get_usage_records(self):
        """Get all recorded token usage (delegates to underlying LLM)."""
        if hasattr(self.llm, "get_usage_records"):
            return self.llm.get_usage_records()
        return []

    def get_total_tokens(self) -> int:
        """Get total tokens used (delegates to underlying LLM)."""
        if hasattr(self.llm, "get_total_tokens"):
            return self.llm.get_total_tokens()
        return 0

    def with_structured_output(self, schema: Any, **kwargs) -> Any:
        """
        Create a structured output version of the LLM.

        Args:
            schema: The schema to use for structured output
            **kwargs: Additional arguments

        Returns:
            LLM configured for structured output
        """
        return self.llm.with_structured_output(schema, **kwargs)


# Global cache instance for convenience (lazy initialization to avoid import side effects)
_global_cache: PromptCache | None = None


def get_global_cache() -> PromptCache:
    """Get the global cache instance (lazy initialized)."""
    global _global_cache
    if _global_cache is None:
        _global_cache = PromptCache()
    return _global_cache


def wrap_llm_with_cache(llm: LLMProtocol, cache: PromptCache | None = None) -> CachedLLMWrapper:
    """
    Convenience function to wrap an LLM with caching.

    Args:
        llm: LLM to wrap
        cache: Optional cache instance (uses global cache if None)

    Returns:
        Cached LLM wrapper
    """
    return CachedLLMWrapper(llm, cache or get_global_cache())
