"""CCE package-first entrypoints and helpers."""

from __future__ import annotations

__all__ = ["__version__"]

try:  # pragma: no cover - best effort for runtime packaging
    from importlib.metadata import version

    __version__ = version("cce-agent")
except Exception:
    __version__ = "0.0.0"
