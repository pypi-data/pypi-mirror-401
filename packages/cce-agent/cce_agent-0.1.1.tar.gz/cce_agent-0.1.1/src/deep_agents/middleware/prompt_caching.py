"""
Prompt caching middleware for CCE deep agents.

Implements in-memory caching of model responses keyed on model settings and
message content to reduce redundant calls.
"""

from __future__ import annotations

import logging
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware, ModelRequest, ModelResponse
from langchain_core.messages import AIMessage, BaseMessage

from src.prompt_cache import PromptCache

logger = logging.getLogger(__name__)


def _serialize_for_cache(value: Any) -> Any:
    """Convert values into JSON-serializable structures for cache keys."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _serialize_for_cache(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_serialize_for_cache(v) for v in value]
    if hasattr(value, "name"):
        return value.name
    if hasattr(value, "model_name"):
        return value.model_name
    return str(value)


def _get_model_name(model: Any) -> str:
    for attr in ("model_name", "model", "name"):
        value = getattr(model, attr, None)
        if value:
            return str(value)
    return model.__class__.__name__


class PromptCachingMiddleware(AgentMiddleware):
    """Cache model responses for repeated prompts."""

    def __init__(self, cache: PromptCache | None = None) -> None:
        super().__init__()
        self.cache = cache or PromptCache()
        self.tools = []

    def _build_messages(self, request: ModelRequest) -> list[BaseMessage]:
        messages: list[BaseMessage] = []
        if request.system_message is not None:
            messages.append(request.system_message)
        messages.extend(request.messages or [])
        return messages

    def _build_cache_kwargs(self, request: ModelRequest) -> dict[str, Any]:
        tool_names = []
        for tool in request.tools or []:
            if hasattr(tool, "name"):
                tool_names.append(tool.name)
            elif isinstance(tool, dict):
                tool_names.append(tool.get("name", str(tool)))
            else:
                tool_names.append(str(tool))

        cache_kwargs = {
            "tool_choice": _serialize_for_cache(request.tool_choice),
            "tools": tool_names,
            "response_format": _serialize_for_cache(request.response_format),
            "model_settings": _serialize_for_cache(request.model_settings),
        }
        return cache_kwargs

    def _get_cached_response(self, request: ModelRequest) -> Any | None:
        if not self.cache.enabled:
            return None

        try:
            messages = self._build_messages(request)
            model_name = _get_model_name(request.model)
            cache_kwargs = self._build_cache_kwargs(request)
            return self.cache.get(messages, model_name, **cache_kwargs)
        except Exception as exc:
            logger.warning("Prompt cache lookup failed: %s", exc)
            return None

    def _store_response(self, request: ModelRequest, response: Any) -> None:
        if not self.cache.enabled:
            return

        try:
            messages = self._build_messages(request)
            model_name = _get_model_name(request.model)
            cache_kwargs = self._build_cache_kwargs(request)
            self.cache.put(messages, model_name, response, **cache_kwargs)
        except Exception as exc:
            logger.warning("Prompt cache store failed: %s", exc)

    def wrap_model_call(self, request: ModelRequest, handler) -> ModelResponse | AIMessage:
        cached = self._get_cached_response(request)
        if cached is not None:
            return cached

        response = handler(request)
        self._store_response(request, response)
        return response

    async def awrap_model_call(self, request: ModelRequest, handler) -> ModelResponse | AIMessage:
        cached = self._get_cached_response(request)
        if cached is not None:
            return cached

        response = await handler(request)
        self._store_response(request, response)
        return response
