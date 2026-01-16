"""
Filesystem backend configuration for deepagents middleware.

Deepagents 0.3.x already includes FilesystemMiddleware; we supply a backend
configured for the CCE workspace.
"""

from __future__ import annotations

import logging
from pathlib import Path

from deepagents.backends import FilesystemBackend
from deepagents.middleware.filesystem import FilesystemMiddleware

logger = logging.getLogger(__name__)


def get_filesystem_backend(
    workspace_root: str | Path = ".",
    enable_virtual_fs: bool = True,
    max_file_size_mb: int = 10,
) -> FilesystemBackend:
    """Create a FilesystemBackend rooted at the workspace.

    Args:
        workspace_root: Root directory for file operations.
        enable_virtual_fs: Whether to require virtual absolute paths ("/...") within root.
        max_file_size_mb: Maximum file size the backend will read during grep/glob.

    Returns:
        Configured FilesystemBackend.
    """
    root = Path(workspace_root).resolve()
    logger.info(
        "Configured FilesystemBackend (root=%s, virtual_mode=%s)",
        root,
        enable_virtual_fs,
    )
    return FilesystemBackend(
        root_dir=str(root),
        virtual_mode=enable_virtual_fs,
        max_file_size_mb=max_file_size_mb,
    )


def create_filesystem_middleware(
    workspace_root: str | Path = ".",
    enable_virtual_fs: bool = True,
    max_file_size_mb: int = 10,
    tool_token_limit_before_evict: int | None = 20000,
) -> FilesystemMiddleware:
    """Create filesystem middleware configured for the workspace root."""
    backend = get_filesystem_backend(
        workspace_root=workspace_root,
        enable_virtual_fs=enable_virtual_fs,
        max_file_size_mb=max_file_size_mb,
    )
    return FilesystemMiddleware(
        backend=backend,
        tool_token_limit_before_evict=tool_token_limit_before_evict,
    )
