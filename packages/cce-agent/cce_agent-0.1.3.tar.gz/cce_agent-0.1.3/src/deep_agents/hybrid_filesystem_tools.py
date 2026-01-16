"""
Hybrid filesystem tools for deep agents integration.

This approach combines the safety of virtual filesystem with real file operations:
1. Initialize virtual filesystem with actual files from the workspace
2. Allow deep agents to work in the safe virtual environment
3. Sync changes back to real filesystem when needed

This gives us:
- Safety: Deep agents can't accidentally damage files outside workspace
- Functionality: Real files are loaded and changes are persisted
- Isolation: Each agent run starts with a clean state
- Rollback: Can revert changes if needed
"""

import glob
import logging
import os
from pathlib import Path
from typing import Annotated, Any, Dict, List, Optional

from langchain_core.tools import tool

# Removed ToolMessage and Command imports - not needed for custom tools
from langgraph.prebuilt import InjectedState
from pydantic import BaseModel, Field

from .tool_output_processor import CondensedOutput, OutputCondensationConfig, process_tool_output

logger = logging.getLogger(__name__)


def _normalize_virtual_path(file_path: str, workspace_root: str) -> str:
    """Normalize file paths to be workspace-relative for hybrid filesystem tools."""
    if not file_path:
        return file_path

    workspace_root = os.path.abspath(workspace_root)
    path = Path(file_path)

    if path.is_absolute():
        try:
            resolved = path.resolve()
            try:
                return str(resolved.relative_to(workspace_root))
            except ValueError:
                normalized = os.path.normpath(file_path.lstrip("/"))
        except Exception:
            normalized = os.path.normpath(file_path.lstrip("/"))
    else:
        normalized = os.path.normpath(file_path)

    if normalized.startswith(".."):
        logger.warning(f"⚠️ [HYBRID FS] Path outside workspace: {file_path}")
        return os.path.basename(normalized)

    return normalized


class HybridWriteFileInput(BaseModel):
    """Input schema for hybrid_write_file tool."""

    file_path: str = Field(..., description="Path to the file to write")
    content: str = Field(..., description="Content to write to the file (required - cannot be empty)")


class HybridEditFileInput(BaseModel):
    """Input schema for hybrid_edit_file tool."""

    file_path: str = Field(..., description="Path to the file to edit")
    old_string: str = Field(..., description="String to find and replace")
    new_string: str = Field(..., description="String to replace with")
    replace_all: bool = Field(default=False, description="Whether to replace all occurrences")


class HybridLsInput(BaseModel):
    """Input schema for hybrid_ls tool."""

    directory: str = Field(default=".", description="Directory to list")
    enable_condensation: bool = Field(default=True, description="Whether to condense large directory listings")
    max_files_shown: int = Field(default=50, description="Maximum number of files to show before condensing")


class HybridReadFileInput(BaseModel):
    """Input schema for hybrid_read_file tool."""

    file_path: str = Field(..., description="Path to file in virtual filesystem")
    offset: int = Field(default=0, description="Line offset to start reading from")
    limit: int = Field(default=200, description="Maximum number of lines to read")
    enable_condensation: bool = Field(
        default=True, description="Whether to use intelligent condensation for large files"
    )
    max_condensed_size: int = Field(default=5000, description="Maximum size for condensed output")
    load_full_content: bool = Field(default=False, description="Whether to load full content from cache")


class SyncToDiskInput(BaseModel):
    """Input schema for sync_to_disk tool."""

    workspace_root: str = Field(default=".", description="Root directory to write to")


def create_file_summary(content: str, file_path: str, max_summary_lines: int = 50) -> str:
    """
    Create an intelligent summary of a file for context loading.

    Args:
        content: Full file content
        file_path: Path to the file (for type detection)
        max_summary_lines: Maximum lines to include in summary

    Returns:
        Intelligent file summary
    """
    if not content:
        return ""

    lines = content.split("\n")
    file_ext = os.path.splitext(file_path)[1].lower()

    # Different strategies based on file type
    if file_ext == ".py":
        return _create_python_summary(lines, max_summary_lines)
    elif file_ext in [".yaml", ".yml", ".json"]:
        return _create_config_summary(lines, max_summary_lines)
    elif file_ext == ".md":
        return _create_markdown_summary(lines, max_summary_lines)
    else:
        return _create_generic_summary(lines, max_summary_lines)


def _create_python_summary(lines: list[str], max_lines: int) -> str:
    """Create summary for Python files focusing on imports, classes, and functions."""
    summary_lines = []
    important_lines = []

    # Always include first few lines (usually imports and docstrings)
    for i, line in enumerate(lines[:20]):
        if line.strip():
            important_lines.append(f"{i + 1:4d}|{line}")

    # Find class and function definitions
    for i, line in enumerate(lines):
        stripped = line.strip()
        if (
            stripped.startswith("class ")
            or stripped.startswith("def ")
            or stripped.startswith("async def ")
            or stripped.startswith("@")
        ):
            important_lines.append(f"{i + 1:4d}|{line}")

    # Limit to max_lines
    if len(important_lines) > max_lines:
        # Keep first 10 lines and most important definitions
        summary_lines = important_lines[:10]
        summary_lines.append("... (truncated for context)")
        summary_lines.extend(important_lines[-max_lines + 11 :])
    else:
        summary_lines = important_lines

    return "\n".join(summary_lines)


def _create_config_summary(lines: list[str], max_lines: int) -> str:
    """Create summary for config files."""
    if len(lines) <= max_lines:
        return "\n".join(f"{i + 1:4d}|{line}" for i, line in enumerate(lines))

    # Keep first and last portions
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

    # Include headers and first content
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

    # Keep first portion
    summary_lines = []
    summary_lines.extend(f"{i + 1:4d}|{line}" for i, line in enumerate(lines[: max_lines - 1]))
    summary_lines.append("... (truncated for context)")

    return "\n".join(summary_lines)


def _load_file_to_virtual_fs(
    file_path: str, workspace_root: str, files: dict[str, str], full_content_cache: dict[str, str], load_mode: str
):
    """Helper function to load a single file into the virtual filesystem."""
    try:
        # Make path relative to workspace root
        rel_path = os.path.relpath(file_path, workspace_root)

        with open(file_path, encoding="utf-8") as f:
            full_content = f.read()

        # Cache full content for lazy loading
        full_content_cache[rel_path] = full_content

        if load_mode == "summary":
            # Create intelligent summary
            summary_content = create_file_summary(full_content, rel_path)
            files[rel_path] = summary_content
            logger.debug(
                f"📁 [HYBRID FS] Loaded summary: {rel_path} ({len(summary_content)} chars from {len(full_content)} chars)"
            )
        else:
            # Load full content
            files[rel_path] = full_content
            logger.debug(f"📁 [HYBRID FS] Loaded full: {rel_path} ({len(full_content)} chars)")

    except Exception as e:
        logger.warning(f"⚠️ [HYBRID FS] Could not load {file_path}: {e}")


def initialize_virtual_filesystem_from_workspace(
    workspace_root: str, include_patterns: list = None, load_mode: str = "summary"
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

    files = {}
    full_content_cache = {}  # Cache full content for lazy loading
    workspace_path = Path(workspace_root)

    logger.info(f"🔍 [HYBRID FS] Scanning workspace: {workspace_root} (mode: {load_mode})")

    for pattern in include_patterns:
        # Check if this is a specific file path or a glob pattern
        if "*" in pattern or "?" in pattern or "[" in pattern:
            # This is a glob pattern
            pattern_path = workspace_path / pattern
            for file_path in glob.glob(str(pattern_path), recursive=True):
                if os.path.isfile(file_path):
                    _load_file_to_virtual_fs(file_path, workspace_root, files, full_content_cache, load_mode)
        else:
            # This is a specific file path
            file_path = workspace_path / pattern
            if os.path.isfile(file_path):
                _load_file_to_virtual_fs(file_path, workspace_root, files, full_content_cache, load_mode)
            else:
                logger.warning(f"⚠️ [HYBRID FS] Essential file not found: {pattern}")

    # Store full content cache in a special key for lazy loading
    if load_mode == "summary":
        files["__full_content_cache__"] = full_content_cache
        logger.info(f"✅ [HYBRID FS] Loaded {len(files) - 1} file summaries + full content cache")
    else:
        logger.info(f"✅ [HYBRID FS] Loaded {len(files)} files with full content")

    return files


def sync_virtual_to_real_filesystem(virtual_files: dict[str, str], workspace_root: str, changed_files: set = None):
    """
    Sync changes from virtual filesystem back to real filesystem.

    Args:
        virtual_files: Virtual filesystem state
        workspace_root: Root directory to write to
        changed_files: Set of files that have changed (if None, sync all)
    """
    workspace_path = Path(workspace_root)
    files_to_sync = changed_files or set(virtual_files.keys())

    logger.info(f"💾 [HYBRID FS] Syncing {len(files_to_sync)} files to disk")

    for rel_path in files_to_sync:
        if rel_path in virtual_files:
            try:
                normalized_path = _normalize_virtual_path(rel_path, workspace_root)
                if not normalized_path:
                    logger.warning(f"⚠️ [HYBRID FS] Skipping empty path from {rel_path}")
                    continue

                full_path = workspace_path / normalized_path

                # Create directory if it doesn't exist
                full_path.parent.mkdir(parents=True, exist_ok=True)

                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(virtual_files[rel_path])

                logger.info(f"💾 [HYBRID FS] Synced: {normalized_path}")

            except Exception as e:
                logger.error(f"❌ [HYBRID FS] Failed to sync {rel_path}: {e}")


@tool(
    args_schema=HybridLsInput,
    description="List files and directories in the virtual filesystem with intelligent condensation for large directories",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def hybrid_ls(
    directory: str = ".",
    state: Annotated[Any, InjectedState] = None,
    enable_condensation: bool = True,
    max_files_shown: int = 50,
) -> str:
    """
    List files in the virtual filesystem with intelligent condensation for large directories.

    Args:
        directory: Directory to list
        enable_condensation: Whether to condense large directory listings
        max_files_shown: Maximum number of files to show before condensing
    """
    # Get current state - handle case where state might be None
    if state is None:
        state = {}
    files = state.get("files") if isinstance(state, dict) else {}
    if not isinstance(files, dict):
        files = {}
    if isinstance(state, dict) and state.get("files") is not files:
        state["files"] = files
    # Debug logging
    logger.debug(f"🔍 [HYBRID LS DEBUG] Directory: {directory}")
    logger.debug(f"🔍 [HYBRID LS DEBUG] State type: {type(state)}")
    logger.debug(f"🔍 [HYBRID LS DEBUG] Files count: {len(files)}")
    logger.debug(f"🔍 [HYBRID LS DEBUG] First 5 files: {list(files.keys())[:5] if files else 'No files'}")

    if directory == ".":
        # List all files
        file_list = [path for path in files.keys() if path != "__full_content_cache__"]
    else:
        # Filter files by directory
        file_list = [f for f in files.keys() if f != "__full_content_cache__" and f.startswith(directory)]

    if not file_list:
        return f"No files found in directory '{directory}'"

    # Group by directory
    dirs = {}
    for file_path in sorted(file_list):
        dir_name = os.path.dirname(file_path) or "."
        if dir_name not in dirs:
            dirs[dir_name] = []
        dirs[dir_name].append(os.path.basename(file_path))

    result = []
    total_files = len(file_list)

    # Check if we need condensation
    if enable_condensation and total_files > max_files_shown:
        logger.info(f"🔍 [HYBRID FS] Large directory listing: {total_files} files, using condensation")

        # Show summary first
        result.append(f"📁 Directory listing for '{directory}' ({total_files} files total)")
        result.append("=" * 50)

        # Show directory structure with file counts
        for dir_name, files_in_dir in dirs.items():
            if dir_name == "." and directory == ".":
                result.append(f"📁 Root directory: {len(files_in_dir)} files")
            else:
                result.append(f"📁 {dir_name}/: {len(files_in_dir)} files")

        result.append("")
        result.append("🔧 Large directory - showing first few files from each directory:")
        result.append("")

        # Show first few files from each directory
        for dir_name, files_in_dir in dirs.items():
            if dir_name == "." and directory == ".":
                result.append("📁 Root directory:")
            else:
                result.append(f"📁 {dir_name}/:")

            # Show first 5 files from each directory
            for file_name in files_in_dir[:5]:
                file_path = file_name if dir_name == "." else f"{dir_name}/{file_name}"
                content_size = len(files.get(file_path, ""))
                result.append(f"  📄 {file_name} ({content_size} chars)")

            if len(files_in_dir) > 5:
                result.append(f"  ... and {len(files_in_dir) - 5} more files")
            result.append("")

        result.append(f"💡 Use 'hybrid_read_file' to read specific files")
        result.append(f"📊 Total: {total_files} files across {len(dirs)} directories")

    else:
        # Standard listing for smaller directories
        for dir_name, files_in_dir in dirs.items():
            if dir_name == "." and directory == ".":
                result.append("📁 Root directory:")
            else:
                result.append(f"📁 {dir_name}/:")

            for file_name in files_in_dir:
                file_path = file_name if dir_name == "." else f"{dir_name}/{file_name}"
                content_size = len(files.get(file_path, ""))
                result.append(f"  📄 {file_name} ({content_size} chars)")

    return "\n".join(result)


@tool(
    args_schema=HybridReadFileInput,
    description="Read file content from virtual filesystem with intelligent condensation and fallback to real filesystem",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def hybrid_read_file(
    file_path: str,
    state: Annotated[Any, InjectedState] = None,
    offset: int = 0,
    limit: int = 200,
    enable_condensation: bool = True,
    max_condensed_size: int = 5000,
    load_full_content: bool = False,
) -> str:
    """
    Read file from virtual filesystem with intelligent condensation and lazy loading.

    🚨 CRITICAL: Always use limit=200 or higher for meaningful context!

    This tool supports two modes:
    1. **Summary Mode** (default): Reads intelligent summaries loaded at startup
    2. **Full Content Mode**: Lazy loads full file content when needed for editing

    RECOMMENDED USAGE:
    - For context/reading: use default (summary mode)
    - For editing: use load_full_content=True to get complete file
    - For small files (<200 lines): use limit=200 (read entire file)
    - For medium files (200-1000 lines): use limit=200-500
    - For large files (>1000 lines): use limit=200-500 (tool will auto-condense if >5000 chars)

    EXAMPLES:
    - hybrid_read_file("src/main.py", limit=200)  # Read summary (fast)
    - hybrid_read_file("src/main.py", load_full_content=True)  # Read full content (for editing)
    - hybrid_read_file("config.json", limit=200)  # Read 200 lines

    Args:
        file_path: Path to file in virtual filesystem
        offset: Line offset to start reading from (default: 0)
        limit: Maximum number of lines to read (default: 200, RECOMMENDED: use 200+ for good context)
        enable_condensation: Whether to use intelligent condensation for large files
        max_condensed_size: Maximum size for condensed output
        load_full_content: Whether to load full content from cache (for editing)
    """
    # Get current state - handle case where state might be None
    if state is None:
        state = {}
    files = state.get("files") if isinstance(state, dict) else {}
    if not isinstance(files, dict):
        files = {}
    workspace_root = os.getcwd()
    normalized_path = _normalize_virtual_path(file_path, workspace_root)

    # If virtual filesystem is empty or file not found, try to read from real filesystem
    if normalized_path not in files:
        try:
            # Check if file exists in real filesystem
            full_path = os.path.join(workspace_root, normalized_path)
            if os.path.exists(full_path):
                logger.info(
                    f"🔄 [HYBRID FS] File not in virtual filesystem, reading from real filesystem: {normalized_path}"
                )
                with open(full_path, encoding="utf-8") as f:
                    content = f.read()

                # Add to virtual filesystem for future use
                files[normalized_path] = content
                if "__full_content_cache__" not in files:
                    files["__full_content_cache__"] = {}
                files["__full_content_cache__"][normalized_path] = content

                # Update state
                state["files"] = files
                logger.info(
                    f"✅ [HYBRID FS] Added file to virtual filesystem: {normalized_path} ({len(content)} chars)"
                )
            else:
                return f"Error: File '{normalized_path}' not found in virtual filesystem or real filesystem"
        except Exception as e:
            return f"Error: Failed to read file '{normalized_path}' from real filesystem: {str(e)}"

    # Get content from virtual filesystem (now guaranteed to exist)
    content = files[normalized_path]

    # Check if we need to load full content from cache
    if load_full_content:
        # First try to get from state cache
        full_content_cache = files.get("__full_content_cache__", {})

        # If not in state, try to get from agent instance (stored separately)
        if not full_content_cache and hasattr(state, "_full_content_cache"):
            full_content_cache = state._full_content_cache
            logger.info(f"🔄 [HYBRID FS] Using agent-level full content cache for {file_path}")

        if normalized_path in full_content_cache:
            content = full_content_cache[normalized_path]
            logger.info(f"🔄 [HYBRID FS] Loaded full content for editing: {normalized_path} ({len(content)} chars)")
        else:
            # Fallback to current content if no cache
            logger.warning(f"⚠️ [HYBRID FS] No full content cache for {normalized_path}, using current content")

    if not content:
        return f"File '{normalized_path}' is empty"

    # Check if we should use intelligent condensation
    if enable_condensation and len(content) > max_condensed_size:
        logger.info(
            f"🔍 [HYBRID FS] Large file detected: {normalized_path} ({len(content):,} chars), using intelligent condensation"
        )

        # Create condensation config
        config = OutputCondensationConfig(
            max_output_chars=max_condensed_size,
            max_lines=limit * 2,  # Allow more lines for condensed output
            enable_logging=True,
        )

        # Process with intelligent condensation
        result = process_tool_output(content, "hybrid_read_file", normalized_path, config)

        if isinstance(result, CondensedOutput):
            # Add metadata header
            header = f"📄 {file_path} (condensed from {result.original_size:,} chars)\n"
            header += f"🔧 Condensation method: {result.condensation_method}\n"
            header += f"📊 Reduction: {result.condensation_ratio:.1%}\n"
            if result.metadata:
                if result.metadata.get("key_functions_included"):
                    header += f"🔧 Key functions included: {result.metadata['key_functions_included']}\n"
                if result.metadata.get("total_functions"):
                    header += f"📊 Total functions in file: {result.metadata['total_functions']}\n"
            header += "=" * 50 + "\n\n"

            return header + result.content
        else:
            return result

    # Standard file reading for smaller files
    lines = content.split("\n")

    # Handle offset and limit
    start_idx = max(0, offset)
    end_idx = min(len(lines), start_idx + limit)

    if start_idx >= len(lines):
        return f"Error: Line offset {offset} exceeds file length ({len(lines)} lines)"

    # Format output with line numbers
    result_lines = []
    for i in range(start_idx, end_idx):
        line_content = lines[i]

        # Truncate lines longer than 2000 characters
        if len(line_content) > 2000:
            line_content = line_content[:2000]

        line_number = i + 1
        result_lines.append(f"{line_number:6d}\t{line_content}")

    return "\n".join(result_lines)


@tool(
    args_schema=HybridWriteFileInput,
    description="Write content to a file in virtual filesystem and track changes. CRITICAL: Always provide both file_path AND content parameters. Content cannot be empty or whitespace-only. Use this to create new files or completely overwrite existing files.",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def hybrid_write_file(
    file_path: str,
    content: str,
    state: Annotated[Any, InjectedState] = None,
) -> str:
    """
    Write content to a file in virtual filesystem and track changes.

    Args:
        file_path: Path to the file to write (required)
        content: Content to write to the file (required - cannot be empty)
        state: Internal state (injected automatically)

    Returns:
        Command object with state updates or error message

    Note: This tool creates a new file or overwrites an existing file with the provided content.
    Use hybrid_edit_file if you need to modify specific parts of an existing file.
    """
    # Check if content is provided and not just whitespace
    if content is None or (isinstance(content, str) and not content.strip()):
        error_msg = f"""⚠️ Content parameter is empty or missing.

To write to {file_path}, provide content like:
hybrid_write_file(file_path="{file_path}", content="your content here")

Examples:
hybrid_write_file(file_path="{file_path}", content="print('hello world')")
hybrid_write_file(file_path="{file_path}", content="def my_function():\\n    return 42")

If you want to modify an existing file instead of creating/overwriting, use hybrid_edit_file:
hybrid_edit_file(file_path="{file_path}", old_string="old code", new_string="new code")

CRITICAL: The content parameter cannot be None, empty string, or just whitespace."""

        # Return error message instead of raising exception
        return error_msg

    # Get current state - handle case where state might be None
    logger.info(f"🔍 [DEBUG] hybrid_write_file called with file_path: {file_path}")
    logger.info(f"🔍 [DEBUG] Content length: {len(content)} chars")

    if state is None:
        state = {}
    files = state.get("files") if isinstance(state, dict) else {}
    if not isinstance(files, dict):
        files = {}
    changed_files = state.get("changed_files") if isinstance(state, dict) else []
    if not isinstance(changed_files, list):
        changed_files = []
    if isinstance(state, dict) and state.get("files") is not files:
        state["files"] = files
    workspace_root = os.getcwd()
    normalized_path = _normalize_virtual_path(file_path, workspace_root)

    logger.info(f"🔍 [DEBUG] Current state - files: {len(files)}, changed_files: {changed_files}")

    # Update virtual filesystem with full content (creates new file if it doesn't exist)
    files[normalized_path] = content

    # Also update the full content cache if it exists
    if "__full_content_cache__" in files:
        files["__full_content_cache__"][normalized_path] = content

    # Track changed files
    if normalized_path not in changed_files:
        changed_files.append(normalized_path)
        logger.info(f"🔍 [DEBUG] Added {normalized_path} to changed_files list")

    logger.info(f"🔍 [DEBUG] Updated virtual file: {normalized_path} ({len(content)} chars)")
    logger.info(f"🔍 [DEBUG] Changed files now: {changed_files}")

    # Update state
    state["files"] = files
    state["changed_files"] = changed_files

    logger.info(f"🔍 [DEBUG] Updated state with files and changed_files")

    # Auto-sync to disk for real-time changes
    try:
        # Filter out the full content cache from sync
        files_to_sync = {k: v for k, v in files.items() if k != "__full_content_cache__"}
        if files_to_sync:
            sync_virtual_to_real_filesystem(files_to_sync, workspace_root, [normalized_path])
            logger.info(f"💾 [HYBRID FS] Auto-synced {normalized_path} to disk")
    except Exception as e:
        logger.warning(f"⚠️ [HYBRID FS] Auto-sync failed for {file_path}: {e}")

    # Return success message instead of Command (following custom tools pattern)
    return f"Successfully wrote {len(content)} characters to {normalized_path}"


@tool(
    args_schema=HybridEditFileInput,
    description="Edit a file in virtual filesystem by replacing specific content. CRITICAL: Always provide file_path, old_string, and new_string parameters. Use this to modify specific parts of existing files. For creating new files or complete overwrites, use hybrid_write_file instead.",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def hybrid_edit_file(
    file_path: str,
    old_string: str,
    new_string: str,
    state: Annotated[Any, InjectedState] = None,
    replace_all: bool = False,
) -> str:
    """
    Edit a file in virtual filesystem by replacing specific content.

    Args:
        file_path: Path to the file to edit (required)
        old_string: String to find and replace (required)
        new_string: String to replace with (required)
        state: Internal state (injected automatically)
        replace_all: Whether to replace all occurrences (default: False)

    Returns:
        Command object with state updates or error message

    Note: This tool modifies existing files by replacing specific content.
    Use hybrid_write_file if you need to create a new file or overwrite the entire file.
    """
    # Validate required parameters
    if not file_path or not file_path.strip():
        return f"""⚠️ File path parameter is empty or missing.

To edit a file, provide the file path like:
hybrid_edit_file(file_path="src/existing_file.py", old_string="old code", new_string="new code")

Example:
hybrid_edit_file(file_path="src/main.py", old_string="print('hello')", new_string="print('world')")

CRITICAL: The file_path parameter cannot be empty."""

    if not old_string or not old_string.strip():
        return f"""⚠️ Old string parameter is empty or missing.

To edit {file_path}, provide the old string to find and replace:
hybrid_edit_file(file_path="{file_path}", old_string="text to find", new_string="replacement text")

Example:
hybrid_edit_file(file_path="{file_path}", old_string="old_function()", new_string="new_function()")

CRITICAL: The old_string parameter cannot be empty."""

    if new_string is None:  # Allow empty new_string (for deletions)
        return f"""⚠️ New string parameter is missing.

To edit {file_path}, provide the new string to replace with:
hybrid_edit_file(file_path="{file_path}", old_string="{old_string}", new_string="replacement text")

Example:
hybrid_edit_file(file_path="{file_path}", old_string="{old_string}", new_string="new code")

Note: new_string can be empty to delete the old_string."""

    logger.info(f"🔍 [DEBUG] hybrid_edit_file called with file_path: {file_path}")
    logger.info(f"🔍 [DEBUG] old_string length: {len(old_string)}, new_string length: {len(new_string)}")
    logger.info(f"🔍 [DEBUG] replace_all: {replace_all}")

    # Get current state - handle case where state might be None
    if state is None:
        state = {}
    files = state.get("files") if isinstance(state, dict) else {}
    if not isinstance(files, dict):
        files = {}
    changed_files = state.get("changed_files") if isinstance(state, dict) else []
    if not isinstance(changed_files, list):
        changed_files = []
    if isinstance(state, dict) and state.get("files") is not files:
        state["files"] = files

    logger.info(f"🔍 [DEBUG] Current state - files: {len(files)}, changed_files: {changed_files}")

    # Normalize file path to match how it was stored in the cache during initialization
    # This ensures we can find the file regardless of whether it was passed as absolute or relative path
    workspace_root = os.getcwd()
    normalized_path = _normalize_virtual_path(file_path, workspace_root)

    logger.debug(f"🔍 [HYBRID FS] hybrid_edit_file: {file_path} -> {normalized_path}")
    logger.debug(f"🔍 [HYBRID FS DEBUG] Files keys: {list(files.keys())}")
    logger.debug(f"🔍 [HYBRID FS DEBUG] Looking for: '{normalized_path}'")
    logger.debug(f"🔍 [HYBRID FS DEBUG] File in files: {normalized_path in files}")

    # If file not in VFS, try to load from disk directly
    if normalized_path not in files:
        logger.warning(f"⚠️ [HYBRID FS] File not found in VFS, attempting to load from disk: {normalized_path}")

        # Try to load full content from disk
        try:
            full_path = os.path.join(workspace_root, normalized_path)
            if os.path.exists(full_path):
                with open(full_path, encoding="utf-8") as f:
                    content = f.read()
                logger.info(
                    f"✅ [HYBRID FS] Successfully loaded full content from disk: {normalized_path} ({len(content)} chars)"
                )
                logger.info(f"🔍 [HYBRID FS DEBUG] Disk content preview (first 200 chars): {content[:200]}")

                # Skip the VFS lookup and go directly to editing
                # We'll handle the content replacement below
            else:
                return f"Error: File '{normalized_path}' not found on disk and not in virtual filesystem."
        except Exception as e:
            logger.error(f"❌ [HYBRID FS] Failed to load full content from disk: {e}")
            return (
                "Error: Could not load full content from disk for editing. "
                "Use hybrid_write_file for full file replacement instead of hybrid_edit_file."
            )
    else:
        # File is in VFS, proceed with normal flow
        content = None  # Will be loaded below

    # Load full content for editing (only if not already loaded from disk)
    if content is None:
        full_content_cache = files.get("__full_content_cache__", {})

        # If not in state, try to get from agent instance (stored separately)
        if not full_content_cache and hasattr(state, "_full_content_cache"):
            full_content_cache = state._full_content_cache
            logger.info(f"🔄 [HYBRID FS] Using agent-level full content cache for editing: {normalized_path}")
            logger.info(
                f"🔍 [HYBRID FS DEBUG] Agent-level cache keys: {list(full_content_cache.keys()) if full_content_cache else 'EMPTY'}"
            )

        if normalized_path in full_content_cache:
            content = full_content_cache[normalized_path]
            logger.info(f"🔄 [HYBRID FS] Using full content for editing: {normalized_path} ({len(content)} chars)")
            logger.info(f"🔍 [HYBRID FS DEBUG] Full content preview (first 200 chars): {content[:200]}")
        else:
            # Always load full content from disk for editing to avoid truncation issues
            logger.info(
                f"🔄 [HYBRID FS] No full content cache, loading full content from disk for editing: {normalized_path}"
            )

            try:
                full_path = os.path.join(workspace_root, normalized_path)
                if os.path.exists(full_path):
                    with open(full_path, encoding="utf-8") as f:
                        content = f.read()
                    logger.info(
                        f"✅ [HYBRID FS] Successfully loaded full content from disk: {normalized_path} ({len(content)} chars)"
                    )
                    logger.info(f"🔍 [HYBRID FS DEBUG] Disk content preview (first 200 chars): {content[:200]}")
                else:
                    # Fallback to VFS content if file doesn't exist on disk
                    content = files[normalized_path]
                    logger.warning(
                        f"⚠️ [HYBRID FS] File not found on disk, using VFS content: {normalized_path} ({len(content)} chars)"
                    )
                    logger.info(f"🔍 [HYBRID FS DEBUG] VFS content preview (first 200 chars): {content[:200]}")

                    # Check if the content seems truncated (common issue)
                    if len(content) < 1000 and "..." in content:
                        logger.error(
                            f"❌ [HYBRID FS] VFS content appears truncated and file not found on disk: {normalized_path}"
                        )
                        return (
                            f"Error: File '{normalized_path}' not found on disk and VFS content appears truncated. "
                            "Use hybrid_write_file for full file replacement instead of hybrid_edit_file."
                        )
            except Exception as e:
                logger.error(f"❌ [HYBRID FS] Failed to load full content from disk: {e}")
                return (
                    "Error: Could not load full content from disk for editing. "
                    "Use hybrid_write_file for full file replacement instead of hybrid_edit_file."
                )

    # Check if old_string exists in content BEFORE making any replacements
    if old_string not in content:
        logger.error(f"❌ [HYBRID FS] String not found in file: {normalized_path}")
        logger.error(f"❌ [HYBRID FS] Old string length: {len(old_string)} chars")
        logger.error(f"❌ [HYBRID FS] Content length: {len(content)} chars")

        # Provide helpful error message with suggestions
        return f"""⚠️ String not found in file '{normalized_path}'

The old_string '{old_string}' was not found in the file.

Troubleshooting:
1. Check if the string exists exactly as written (case-sensitive)
2. Use hybrid_read_file to see the current file content:
   hybrid_read_file(file_path="{normalized_path}", limit=200)
3. Make sure you're using the exact text including spaces and formatting
4. If you want to create a new file instead, use hybrid_write_file:
   hybrid_write_file(file_path="{normalized_path}", content="your content here")

File length: {len(content)} characters
Search string length: {len(old_string)} characters"""

    logger.info(f"✏️ [HYBRID FS] Found old_string in file: {normalized_path}")
    logger.info(f"✏️ [HYBRID FS] Old string length: {len(old_string)} chars")
    logger.info(f"✏️ [HYBRID FS] New string length: {len(new_string)} chars")

    if replace_all:
        new_content = content.replace(old_string, new_string)
        replacements = content.count(old_string)
        logger.info(f"✏️ [HYBRID FS] Replace all mode: {replacements} replacements")
    else:
        new_content = content.replace(old_string, new_string, 1)
        replacements = 1
        logger.info(f"✏️ [HYBRID FS] Single replacement mode: 1 replacement")

    # Update virtual filesystem with full content
    files[normalized_path] = new_content

    # Also update the full content cache if it exists
    if "__full_content_cache__" in files:
        files["__full_content_cache__"][normalized_path] = new_content

    # Also update the agent-level cache if it exists
    if hasattr(state, "_full_content_cache"):
        state._full_content_cache[normalized_path] = new_content

    # Track changed files
    if normalized_path not in changed_files:
        changed_files.append(normalized_path)
        logger.info(f"🔍 [DEBUG] Added {normalized_path} to changed_files list")

    logger.info(f"🔍 [DEBUG] Edited virtual file: {normalized_path} ({replacements} replacements)")
    logger.info(f"🔍 [DEBUG] Changed files now: {changed_files}")

    # Update state
    state["files"] = files
    state["changed_files"] = changed_files

    logger.info(f"🔍 [DEBUG] Updated state with files and changed_files")

    # Auto-sync to disk for real-time changes
    try:
        # Filter out the full content cache from sync
        files_to_sync = {k: v for k, v in files.items() if k != "__full_content_cache__"}
        if files_to_sync:
            sync_virtual_to_real_filesystem(files_to_sync, workspace_root, [normalized_path])
            logger.info(f"💾 [HYBRID FS] Auto-synced {normalized_path} to disk")
    except Exception as e:
        logger.warning(f"⚠️ [HYBRID FS] Auto-sync failed for {normalized_path}: {e}")

    # Return success message instead of Command (following custom tools pattern)
    return f"Successfully replaced {replacements} occurrence(s) in {normalized_path}"


@tool(
    args_schema=SyncToDiskInput,
    description="Sync all files from virtual filesystem to real disk",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
def sync_to_disk(
    workspace_root: str = ".",
    state: Annotated[Any, InjectedState] = None,
) -> str:
    """Sync all files from virtual filesystem to real disk."""
    if state is None:
        state = {}
    files = state.get("files") if isinstance(state, dict) else {}
    if not isinstance(files, dict):
        files = {}

    # Filter out the full content cache from sync
    files_to_sync = {k: v for k, v in files.items() if k != "__full_content_cache__"}

    logger.info(f"💾 [HYBRID FS] Sync requested - total files in virtual filesystem: {len(files_to_sync)}")

    if not files_to_sync:
        return "No files in virtual filesystem to sync"

    # Sync files to disk (excluding the cache)
    all_file_paths = set(files_to_sync.keys())
    sync_virtual_to_real_filesystem(files_to_sync, workspace_root, all_file_paths)

    logger.info(f"💾 [HYBRID FS] Successfully synced {len(all_file_paths)} files to disk")

    # Return success message instead of Command (following custom tools pattern)
    return f"Successfully synced {len(all_file_paths)} files to disk"


# Export the hybrid filesystem tools
HYBRID_FILESYSTEM_TOOLS = [hybrid_ls, hybrid_read_file, hybrid_write_file, hybrid_edit_file, sync_to_disk]
