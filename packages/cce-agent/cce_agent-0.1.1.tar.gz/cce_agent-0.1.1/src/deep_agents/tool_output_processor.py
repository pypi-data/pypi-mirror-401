"""Compatibility shim for tool output processing utilities."""

from .utils.tool_output_processor import (
    CondensedOutput,
    OutputCondensationConfig,
    condense_by_truncation,
    condense_code_file,
    condense_json_output,
    create_condensation_summary,
    process_tool_output,
    should_condense_output,
)

__all__ = [
    "CondensedOutput",
    "OutputCondensationConfig",
    "condense_by_truncation",
    "condense_code_file",
    "condense_json_output",
    "create_condensation_summary",
    "process_tool_output",
    "should_condense_output",
]
