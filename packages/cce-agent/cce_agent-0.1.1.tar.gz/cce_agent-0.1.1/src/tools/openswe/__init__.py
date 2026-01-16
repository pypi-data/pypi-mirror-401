"""
Open SWE Tools Integration

This package provides a complete implementation of Open SWE tools converted from TypeScript to Python.
All tools are LangChain-compatible and designed for use with the CCE Agent system.

Tool Categories:
- Core Tools: Basic shell, HTTP, and web search functionality
- File Tools: File operations, text editing, and viewing
- Development Tools: Patch application, grep search, dependency management
- Workflow Tools: Task management, planning, and human interaction
- GitHub Tools: PR management and review workflows
- Utilities: Infrastructure support classes
"""

# Core Tools
# CodeTools Facade
from .code_tools import CodeTools, ToolResult
from .core_tools import execute_bash, http_request, web_search

# Development Tools
from .dev_tools import advanced_shell, command_safety_evaluator, grep_search, install_dependencies

# File Tools
from .file_tools import apply_patch, text_editor, view, write_default_tsconfig

# GitHub Tools
from .github_tools import open_pr, reply_to_review_comment, review_started

# TreeSitter Tools
from .treesitter_tools import (
    CodeAnalysis,
    CodeNode,
    TreeSitterAnalyzer,
    analyze_code_structure,
    calculate_code_complexity,
    extract_code_symbols,
)

# Utilities
from .utilities import (
    DiffProcessor,
    DocumentSearchPrompts,
    ErrorHandler,
    FileOperations,
    ShellExecutor,
    URLParser,
    diff_processor,
    error_handler,
    file_ops,
    get_diff_processor,
    get_error_handler,
    get_file_ops,
    get_shell_executor,
    get_url_parser,
    shell_executor,
    url_parser,
)

# Command Safety
from .command_safety import validate_command_safety

# Web Tools
from .web_tools import get_url_content, search_documents_for

# Workflow Tools
from .workflow_tools import (
    conversation_history_summary,
    diagnose_error,
    mark_task_completed,
    mark_task_not_completed,
    request_human_help,
    scratchpad,
    session_plan,
    update_plan,
    write_technical_notes,
)

# Export all tools for easy importing
__all__ = [
    # Core Tools
    "execute_bash",
    "http_request",
    "web_search",
    # File Tools
    "text_editor",
    "view",
    "apply_patch",
    "write_default_tsconfig",
    # Development Tools
    "grep_search",
    "install_dependencies",
    "advanced_shell",
    "command_safety_evaluator",
    # Web Tools
    "get_url_content",
    "search_documents_for",
    # Workflow Tools
    "scratchpad",
    "request_human_help",
    "session_plan",
    "update_plan",
    "mark_task_completed",
    "mark_task_not_completed",
    "diagnose_error",
    "write_technical_notes",
    "conversation_history_summary",
    # GitHub Tools
    "reply_to_review_comment",
    "open_pr",
    "review_started",
    # Utilities
    "FileOperations",
    "ShellExecutor",
    "URLParser",
    "DiffProcessor",
    "DocumentSearchPrompts",
    "ErrorHandler",
    "file_ops",
    "shell_executor",
    "url_parser",
    "diff_processor",
    "error_handler",
    "get_file_ops",
    "get_shell_executor",
    "get_url_parser",
    "get_diff_processor",
    "get_error_handler",
    # Command Safety
    "validate_command_safety",
    # TreeSitter Tools
    "analyze_code_structure",
    "extract_code_symbols",
    "calculate_code_complexity",
    "TreeSitterAnalyzer",
    "CodeAnalysis",
    "CodeNode",
    # CodeTools Facade
    "CodeTools",
    "ToolResult",
]
