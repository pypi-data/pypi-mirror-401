"""
Compatibility filesystem tools for deep agents.

Deepagents provides built-in filesystem tools via FilesystemMiddleware. This
module provides a no-op sync tool for legacy prompts and workflows.
"""

from __future__ import annotations

from langchain_core.tools import tool


@tool(
    description="No-op filesystem sync. FilesystemMiddleware writes directly to disk.",
    infer_schema=False,
    parse_docstring=False,
)
def sync_to_disk(*_args, **_kwargs) -> str:
    """Return a confirmation that files are already persisted."""
    return "FilesystemMiddleware writes directly to disk; no sync required."


FILESYSTEM_COMPAT_TOOLS = [sync_to_disk]
