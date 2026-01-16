"""
Virtual filesystem summary utilities.

These helpers build summary or full-content snapshots for intelligent file discovery
and context-aware analysis. They are not used by deepagents file tools.
"""

from __future__ import annotations

import glob
import logging
import os
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

_DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".next",
    "dist",
    "build",
    "artifacts",
    "out",
    ".turbo",
    ".cache",
    ".artifacts",
    "coverage",
    ".venv",
    "venv",
}


def _should_skip_path(file_path: str, workspace_root: str) -> bool:
    try:
        rel_path = Path(file_path).resolve().relative_to(Path(workspace_root).resolve())
    except Exception:
        rel_path = Path(file_path)
    for part in rel_path.parts:
        if part in _DEFAULT_EXCLUDED_DIRS:
            return True
    return False


def create_file_summary(content: str, file_path: str, max_summary_lines: int = 50) -> str:
    """Create an intelligent summary of a file for context loading."""
    if not content:
        return ""

    lines = content.split("\n")
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".py":
        return _create_python_summary(lines, max_summary_lines)
    if file_ext in [".yaml", ".yml", ".json"]:
        return _create_config_summary(lines, max_summary_lines)
    if file_ext == ".md":
        return _create_markdown_summary(lines, max_summary_lines)
    return _create_generic_summary(lines, max_summary_lines)


def _create_python_summary(lines: list[str], max_lines: int) -> str:
    """Create summary for Python files focusing on imports, classes, and functions."""
    important_lines: list[str] = []

    for i, line in enumerate(lines[:20]):
        if line.strip():
            important_lines.append(f"{i + 1:4d}|{line}")

    for i, line in enumerate(lines):
        stripped = line.strip()
        if (
            stripped.startswith("class ")
            or stripped.startswith("def ")
            or stripped.startswith("async def ")
            or stripped.startswith("@")
        ):
            important_lines.append(f"{i + 1:4d}|{line}")

    if len(important_lines) > max_lines:
        summary_lines = important_lines[:10]
        summary_lines.append("... (truncated for context)")
        summary_lines.extend(important_lines[-max_lines + 11 :])
        return "\n".join(summary_lines)

    return "\n".join(important_lines)


def _create_config_summary(lines: list[str], max_lines: int) -> str:
    """Create summary for config files."""
    if len(lines) <= max_lines:
        return "\n".join(f"{i + 1:4d}|{line}" for i, line in enumerate(lines))

    summary_lines = []
    summary_lines.extend(f"{i + 1:4d}|{line}" for i, line in enumerate(lines[: max_lines // 2]))
    summary_lines.append("... (truncated for context)")
    summary_lines.extend(
        f"{i + 1:4d}|{line}" for i, line in enumerate(lines[-max_lines // 2 :], len(lines) - max_lines // 2)
    )
    return "\n".join(summary_lines)


def _create_markdown_summary(lines: list[str], max_lines: int) -> str:
    """Create summary for Markdown files focusing on headers and key content."""
    summary_lines = []

    for i, line in enumerate(lines):
        if line.startswith("#") or (line.strip() and len(summary_lines) < max_lines):
            summary_lines.append(f"{i + 1:4d}|{line}")

    if len(summary_lines) > max_lines:
        summary_lines = summary_lines[:max_lines]
        summary_lines.append("... (truncated for context)")

    return "\n".join(summary_lines)


def _create_generic_summary(lines: list[str], max_lines: int) -> str:
    """Create generic summary for other file types."""
    if len(lines) <= max_lines:
        return "\n".join(f"{i + 1:4d}|{line}" for i, line in enumerate(lines))

    summary_lines = []
    summary_lines.extend(f"{i + 1:4d}|{line}" for i, line in enumerate(lines[: max_lines - 1]))
    summary_lines.append("... (truncated for context)")
    return "\n".join(summary_lines)


def _load_file_to_virtual_fs(
    file_path: str,
    workspace_root: str,
    files: dict[str, str],
    full_content_cache: dict[str, str],
    load_mode: str,
) -> None:
    """Helper function to load a single file into the virtual filesystem."""
    try:
        if _should_skip_path(file_path, workspace_root):
            return
        rel_path = os.path.relpath(file_path, workspace_root)
        content = Path(file_path).read_text(encoding="utf-8")
        full_content_cache[rel_path] = content

        if load_mode == "summary":
            summary_content = create_file_summary(content, rel_path)
            files[rel_path] = summary_content
            logger.debug("📁 [VFS] Loaded summary: %s", rel_path)
        else:
            files[rel_path] = content
            logger.debug("📁 [VFS] Loaded full: %s", rel_path)
    except Exception as exc:
        logger.warning("⚠️ [VFS] Could not load %s: %s", file_path, exc)


def initialize_virtual_filesystem_from_workspace(
    workspace_root: str,
    include_patterns: list[str] | None = None,
    load_mode: str = "summary",
) -> dict[str, str]:
    """
    Initialize virtual filesystem with actual files from workspace.

    Args:
        workspace_root: Root directory to scan
        include_patterns: List of glob patterns to include (default: common source files)
        load_mode: "summary" for intelligent summaries, "full" for complete content

    Returns:
        Dictionary mapping file paths to their contents (summaries or full content)
    """
    if include_patterns is None:
        include_patterns = [
            "*.py",
            "*.yaml",
            "*.yml",
            "*.json",
            "*.md",
            "*.txt",
            "*.sh",
            "*.js",
            "*.ts",
            "*.css",
            "*.html",
            "config/*",
            "src/**/*.py",
            "docs/**/*.md",
        ]

    files: dict[str, str] = {}
    full_content_cache: dict[str, str] = {}
    workspace_path = Path(workspace_root)

    logger.info("🔍 [VFS] Scanning workspace: %s (mode: %s)", workspace_root, load_mode)

    for pattern in include_patterns:
        pattern_path = workspace_path / pattern
        if any(ch in pattern for ch in ["*", "?", "["]):
            for file_path in glob.glob(str(pattern_path), recursive=True):
                if os.path.isfile(file_path):
                    _load_file_to_virtual_fs(file_path, workspace_root, files, full_content_cache, load_mode)
        else:
            if pattern_path.is_file():
                _load_file_to_virtual_fs(str(pattern_path), workspace_root, files, full_content_cache, load_mode)
            else:
                logger.warning("⚠️ [VFS] Essential file not found: %s", pattern)

    if load_mode == "summary":
        files["__full_content_cache__"] = full_content_cache
        loaded_count = len(files) - 1
        logger.info("✅ [VFS] Loaded %s file summaries + full content cache", loaded_count)
    else:
        loaded_count = len(files)
        logger.info("✅ [VFS] Loaded %s files with full content", loaded_count)

    if loaded_count == 0:
        logger.warning("⚠️ [VFS] No files loaded (workspace_root=%s, patterns=%s)", workspace_root, include_patterns)

    return files
