"""
Tool output processor for intelligent condensation of large outputs.

This module provides utilities to process and condense large tool outputs before
they are added to the agent's context, preventing context overflow while preserving
important information.
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ..code_analyzer import analyze_file_structure, create_file_summary, extract_key_functions

logger = logging.getLogger(__name__)


class OutputCondensationConfig:
    """Configuration for output condensation behavior."""

    def __init__(
        self,
        max_output_chars: int = 10000,
        max_lines: int = 500,
        max_functions: int = 10,
        max_classes: int = 5,
        preserve_imports: bool = True,
        preserve_docstrings: bool = True,
        enable_code_analysis: bool = True,
        enable_logging: bool = True,
    ):
        self.max_output_chars = max_output_chars
        self.max_lines = max_lines
        self.max_functions = max_functions
        self.max_classes = max_classes
        self.preserve_imports = preserve_imports
        self.preserve_docstrings = preserve_docstrings
        self.enable_code_analysis = enable_code_analysis
        self.enable_logging = enable_logging


class CondensedOutput:
    """Represents a condensed tool output with metadata."""

    def __init__(self, content: str, original_size: int, condensation_method: str, metadata: dict[str, Any] = None):
        self.content = content
        self.original_size = original_size
        self.condensation_method = condensation_method
        self.metadata = metadata or {}
        self.condensation_ratio = (original_size - len(content)) / original_size if original_size > 0 else 0


def should_condense_output(content: str, config: OutputCondensationConfig) -> bool:
    """
    Determine if output should be condensed based on size and content.

    Args:
        content: The output content to evaluate
        config: Condensation configuration

    Returns:
        True if output should be condensed
    """
    if len(content) <= config.max_output_chars:
        return False

    # Check if it looks like a code file
    lines = content.split("\n")
    if len(lines) > config.max_lines:
        return True

    # Check for code-like patterns
    code_indicators = [
        r"^\s*def\s+\w+",  # Python functions
        r"^\s*class\s+\w+",  # Python classes
        r"^\s*function\s+\w+",  # JavaScript functions
        r"^\s*import\s+",  # Imports
        r"^\s*from\s+\w+\s+import",  # Python imports
        r"^\s*#\s*",  # Comments
        r"^\s*//\s*",  # JavaScript comments
        r"^\s*/\*",  # Block comments
    ]

    code_line_count = 0
    for line in lines[:100]:  # Check first 100 lines
        for pattern in code_indicators:
            if re.search(pattern, line):
                code_line_count += 1
                break

    # If more than 20% of lines look like code, consider for condensation
    return code_line_count > len(lines[:100]) * 0.2


def condense_code_file(content: str, file_path: str, config: OutputCondensationConfig) -> CondensedOutput:
    """
    Condense a code file by extracting key structural information.

    Args:
        content: File content
        file_path: Path to the file
        config: Condensation configuration

    Returns:
        CondensedOutput with structural summary
    """
    original_size = len(content)

    if config.enable_logging:
        logger.info(f"🔍 [CONDENSER] Analyzing code file: {file_path} ({original_size:,} chars)")

    try:
        # Analyze file structure
        structure = analyze_file_structure(content, file_path)

        # Create summary
        summary = create_file_summary(structure, max_items=config.max_functions)

        # Extract key functions with full content
        key_functions = extract_key_functions(structure, max_functions=config.max_functions)

        condensed_lines = [summary, ""]

        # Add key functions with full content
        if key_functions:
            condensed_lines.append("🔧 Key Functions:")
            for func in key_functions:
                if config.enable_logging:
                    logger.debug(f"   Including function: {func['name']}")

                # Extract function content from original file
                lines = content.split("\n")
                start_line = func["line_start"] - 1
                end_line = func.get("line_end", start_line + 50)  # Default 50 lines if no end

                func_lines = lines[start_line:end_line]
                func_content = "\n".join(func_lines)

                # Truncate if too long
                if len(func_content) > 2000:
                    func_content = func_content[:2000] + "\n... (truncated)"

                condensed_lines.append(f"\n# {func['name']} (line {func['line_start']})")
                condensed_lines.append(func_content)

        # Add imports if preserved
        if config.preserve_imports and structure.imports:
            condensed_lines.append("\n📦 All Imports:")
            for imp in structure.imports[:20]:  # Limit imports
                condensed_lines.append(f"   {imp}")
            if len(structure.imports) > 20:
                condensed_lines.append(f"   ... and {len(structure.imports) - 20} more imports")

        condensed_content = "\n".join(condensed_lines)

        # Ensure we don't exceed max size
        if len(condensed_content) > config.max_output_chars:
            condensed_content = condensed_content[: config.max_output_chars] + "\n... (truncated due to size limit)"

        metadata = {
            "file_type": structure.file_type,
            "total_functions": len(structure.functions),
            "total_classes": len(structure.classes),
            "total_imports": len(structure.imports),
            "key_functions_included": len(key_functions),
            "analysis_errors": structure.analysis_errors,
        }

        if config.enable_logging:
            logger.info(
                f"✅ [CONDENSER] Code condensation: {original_size:,} → {len(condensed_content):,} chars ({metadata['key_functions_included']} key functions)"
            )

        return CondensedOutput(
            content=condensed_content,
            original_size=original_size,
            condensation_method="code_structure_analysis",
            metadata=metadata,
        )

    except Exception as e:
        logger.error(f"❌ [CONDENSER] Error condensing code file {file_path}: {e}")
        # Fallback to simple truncation
        return condense_by_truncation(content, config)


def condense_by_truncation(content: str, config: OutputCondensationConfig) -> CondensedOutput:
    """
    Condense content by simple truncation with header/footer preservation.

    Args:
        content: Content to condense
        config: Condensation configuration

    Returns:
        CondensedOutput with truncated content
    """
    original_size = len(content)
    lines = content.split("\n")

    if len(lines) <= config.max_lines and len(content) <= config.max_output_chars:
        return CondensedOutput(content, original_size, "no_condensation_needed")

    # Keep first and last portions
    keep_lines = config.max_lines // 2
    first_part = lines[:keep_lines]
    last_part = lines[-keep_lines:] if len(lines) > keep_lines * 2 else []

    condensed_lines = first_part.copy()

    if last_part and len(lines) > keep_lines * 2:
        condensed_lines.append(f"\n... ({len(lines) - keep_lines * 2} lines omitted) ...\n")
        condensed_lines.extend(last_part)

    condensed_content = "\n".join(condensed_lines)

    # Ensure we don't exceed max size
    if len(condensed_content) > config.max_output_chars:
        condensed_content = condensed_content[: config.max_output_chars] + "\n... (truncated due to size limit)"

    if config.enable_logging:
        logger.info(f"✂️ [CONDENSER] Truncation: {original_size:,} → {len(condensed_content):,} chars")

    return CondensedOutput(
        content=condensed_content,
        original_size=original_size,
        condensation_method="truncation",
        metadata={"lines_kept": len(condensed_lines), "total_lines": len(lines)},
    )


def condense_json_output(content: str, config: OutputCondensationConfig) -> CondensedOutput:
    """
    Condense JSON output by extracting key fields and structure.

    Args:
        content: JSON content
        config: Condensation configuration

    Returns:
        CondensedOutput with condensed JSON
    """
    original_size = len(content)

    try:
        import json

        data = json.loads(content)

        if isinstance(data, dict):
            # Extract key fields
            key_fields = list(data.keys())[:10]  # First 10 keys
            condensed_data = {k: data[k] for k in key_fields}

            if len(data) > 10:
                condensed_data["..."] = f"({len(data) - 10} more fields)"

            condensed_content = json.dumps(condensed_data, indent=2)

        elif isinstance(data, list):
            # Show first few items and summary
            if len(data) <= 5:
                condensed_content = json.dumps(data, indent=2)
            else:
                condensed_data = data[:3]
                condensed_data.append(f"... ({len(data) - 3} more items)")
                condensed_content = json.dumps(condensed_data, indent=2)
        else:
            # Simple value, just truncate if needed
            condensed_content = str(data)
            if len(condensed_content) > config.max_output_chars:
                condensed_content = condensed_content[: config.max_output_chars] + "... (truncated)"

        if config.enable_logging:
            logger.info(f"📋 [CONDENSER] JSON condensation: {original_size:,} → {len(condensed_content):,} chars")

        return CondensedOutput(
            content=condensed_content,
            original_size=original_size,
            condensation_method="json_structure",
            metadata={"original_type": type(data).__name__},
        )

    except json.JSONDecodeError:
        # Not valid JSON, fall back to truncation
        return condense_by_truncation(content, config)


def process_tool_output(
    content: str, tool_name: str, file_path: str | None = None, config: OutputCondensationConfig | None = None
) -> str | CondensedOutput:
    """
    Process and potentially condense a tool output.

    Args:
        content: The tool output content
        tool_name: Name of the tool that produced the output
        file_path: Path to file if this is a file operation
        config: Condensation configuration

    Returns:
        Original content if no condensation needed, or CondensedOutput
    """
    if config is None:
        config = OutputCondensationConfig()

    # Don't condense if content is small enough
    if not should_condense_output(content, config):
        return content

    if config.enable_logging:
        logger.info(f"🔧 [CONDENSER] Processing {tool_name} output: {len(content):,} chars")

    # Determine condensation strategy based on tool and content
    if tool_name in ["read_file", "real_read_file"] and file_path:
        # File reading - use code analysis if it's a code file
        file_ext = Path(file_path).suffix.lower()
        if file_ext in [".py", ".js", ".ts", ".jsx", ".tsx", ".md"] and config.enable_code_analysis:
            return condense_code_file(content, file_path, config)
        else:
            return condense_by_truncation(content, config)

    elif tool_name in ["ls", "real_ls"]:
        # Directory listing - usually not too large, but truncate if needed
        return condense_by_truncation(content, config)

    elif tool_name in ["web_search", "fetch_url"]:
        # Web content - truncate with header preservation
        return condense_by_truncation(content, config)

    else:
        # Try JSON condensation first, then fall back to truncation
        if content.strip().startswith("{") or content.strip().startswith("["):
            try:
                return condense_json_output(content, config)
            except:
                pass

        return condense_by_truncation(content, config)


def create_condensation_summary(condensed_outputs: list[CondensedOutput]) -> str:
    """
    Create a summary of condensation operations performed.

    Args:
        condensed_outputs: List of CondensedOutput objects

    Returns:
        Formatted summary string
    """
    if not condensed_outputs:
        return "No condensation performed."

    total_original = sum(co.original_size for co in condensed_outputs)
    total_condensed = sum(len(co.content) for co in condensed_outputs)
    total_saved = total_original - total_condensed
    avg_reduction = (total_saved / total_original * 100) if total_original > 0 else 0

    lines = [
        f"📊 Condensation Summary:",
        f"   Files processed: {len(condensed_outputs)}",
        f"   Original size: {total_original:,} characters",
        f"   Condensed size: {total_condensed:,} characters",
        f"   Space saved: {total_saved:,} characters ({avg_reduction:.1f}% reduction)",
        "",
    ]

    for co in condensed_outputs:
        method = co.condensation_method.replace("_", " ").title()
        lines.append(f"   • {method}: {co.original_size:,} → {len(co.content):,} chars")

    return "\n".join(lines)
