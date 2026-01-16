"""
Execution limits configuration.

Centralizes execution limits like max cycle count so they can be overridden
via environment variables.
"""

import os
from functools import lru_cache
from typing import Any


def _normalize_positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(1, parsed)


def _get_config_value(name: str) -> Any:
    try:
        from src.config_loader import get_config

        execution = getattr(get_config(), "execution", None)
        return getattr(execution, name, None) if execution is not None else None
    except Exception:
        return None


def _parse_max_cycles() -> int:
    config_value = _get_config_value("max_cycles")
    if config_value is not None:
        return _normalize_positive_int(config_value, 50)
    return _normalize_positive_int(os.getenv("CCE_MAX_CYCLES", "50"), 50)


@lru_cache(maxsize=1)
def get_max_execution_cycles() -> int:
    """Get max execution cycles from env (cached)."""
    return _parse_max_cycles()


def _parse_soft_limit() -> int:
    config_value = _get_config_value("soft_limit")
    if config_value is not None:
        return _normalize_positive_int(config_value, 20)
    return _normalize_positive_int(os.getenv("CCE_SOFT_LIMIT", "20"), 20)


@lru_cache(maxsize=1)
def get_soft_limit() -> int:
    """Get soft limit from env (cached)."""
    return _parse_soft_limit()


def _parse_recursion_limit() -> int:
    config_value = _get_config_value("recursion_limit")
    if config_value is not None:
        return _normalize_positive_int(config_value, 200)
    return _normalize_positive_int(os.getenv("CCE_RECURSION_LIMIT", "200"), 200)


@lru_cache(maxsize=1)
def get_recursion_limit() -> int:
    """Get recursion limit from config (cached)."""
    return _parse_recursion_limit()
