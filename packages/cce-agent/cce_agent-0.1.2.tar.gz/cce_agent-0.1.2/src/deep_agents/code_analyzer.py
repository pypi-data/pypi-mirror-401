"""
Code structure analyzer for intelligent file condensation.

This module provides utilities to extract key structural information from code files,
enabling intelligent condensation of large files while preserving important context.
"""

import ast
import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class CodeStructure:
    """Represents the structural analysis of a code file."""

    def __init__(self, file_path: str, file_type: str):
        self.file_path = file_path
        self.file_type = file_type
        self.functions: list[dict[str, Any]] = []
        self.classes: list[dict[str, Any]] = []
        self.imports: list[str] = []
        self.constants: list[dict[str, Any]] = []
        self.total_lines: int = 0
        self.total_chars: int = 0
        self.analysis_errors: list[str] = []


def analyze_python_file(content: str, file_path: str) -> CodeStructure:
    """
    Analyze a Python file and extract structural information.

    Args:
        content: File content as string
        file_path: Path to the file

    Returns:
        CodeStructure object with extracted information
    """
    structure = CodeStructure(file_path, "python")
    structure.total_lines = len(content.split("\n"))
    structure.total_chars = len(content)

    try:
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "line_start": node.lineno,
                    "line_end": getattr(node, "end_lineno", node.lineno),
                    "args": [arg.arg for arg in node.args.args],
                    "decorators": [ast.unparse(dec) for dec in node.decorator_list],
                    "docstring": ast.get_docstring(node),
                    "is_async": isinstance(node, ast.AsyncFunctionDef),
                    "is_method": any(
                        isinstance(parent, ast.ClassDef)
                        for parent in ast.walk(tree)
                        if hasattr(parent, "body") and isinstance(parent.body, list) and node in parent.body
                    ),
                }
                structure.functions.append(func_info)

            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "line_start": node.lineno,
                    "line_end": getattr(node, "end_lineno", node.lineno),
                    "bases": [ast.unparse(base) for base in node.bases],
                    "decorators": [ast.unparse(dec) for dec in node.decorator_list],
                    "docstring": ast.get_docstring(node),
                    "methods": [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))],
                }
                structure.classes.append(class_info)

            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        structure.imports.append(f"import {alias.name}")
                else:
                    module = node.module or ""
                    for alias in node.names:
                        structure.imports.append(f"from {module} import {alias.name}")

            elif isinstance(node, ast.Assign):
                # Look for module-level constants
                if all(isinstance(target, ast.Name) for target in node.targets):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            constant_info = {
                                "name": target.id,
                                "line": node.lineno,
                                "value": ast.unparse(node.value) if hasattr(ast, "unparse") else str(node.value),
                            }
                            structure.constants.append(constant_info)

    except SyntaxError as e:
        structure.analysis_errors.append(f"Syntax error: {e}")
        logger.warning(f"Could not parse Python file {file_path}: {e}")
    except Exception as e:
        structure.analysis_errors.append(f"Analysis error: {e}")
        logger.warning(f"Error analyzing Python file {file_path}: {e}")

    return structure


def analyze_javascript_file(content: str, file_path: str) -> CodeStructure:
    """
    Analyze a JavaScript/TypeScript file and extract structural information.

    Args:
        content: File content as string
        file_path: Path to the file

    Returns:
        CodeStructure object with extracted information
    """
    structure = CodeStructure(file_path, "javascript")
    structure.total_lines = len(content.split("\n"))
    structure.total_chars = len(content)

    try:
        # Extract function declarations
        function_pattern = r"(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s+)?\(|(\w+)\s*:\s*(?:async\s+)?\("
        for match in re.finditer(function_pattern, content):
            func_name = match.group(1) or match.group(2) or match.group(3)
            if func_name:
                line_num = content[: match.start()].count("\n") + 1
                structure.functions.append({"name": func_name, "line_start": line_num, "type": "function"})

        # Extract class declarations
        class_pattern = r"(?:export\s+)?class\s+(\w+)"
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            line_num = content[: match.start()].count("\n") + 1
            structure.classes.append({"name": class_name, "line_start": line_num, "type": "class"})

        # Extract imports
        import_pattern = r'(?:import\s+.*?from\s+[\'"]([^\'"]+)[\'"]|import\s+[\'"]([^\'"]+)[\'"])'
        for match in re.finditer(import_pattern, content):
            import_path = match.group(1) or match.group(2)
            if import_path:
                structure.imports.append(f"import from {import_path}")

        # Extract constants (const declarations)
        const_pattern = r"const\s+([A-Z_][A-Z0-9_]*)\s*="
        for match in re.finditer(const_pattern, content):
            const_name = match.group(1)
            line_num = content[: match.start()].count("\n") + 1
            structure.constants.append({"name": const_name, "line": line_num, "type": "const"})

    except Exception as e:
        structure.analysis_errors.append(f"Analysis error: {e}")
        logger.warning(f"Error analyzing JavaScript file {file_path}: {e}")

    return structure


def analyze_markdown_file(content: str, file_path: str) -> CodeStructure:
    """
    Analyze a Markdown file and extract structural information.

    Args:
        content: File content as string
        file_path: Path to the file

    Returns:
        CodeStructure object with extracted information
    """
    structure = CodeStructure(file_path, "markdown")
    structure.total_lines = len(content.split("\n"))
    structure.total_chars = len(content)

    try:
        # Extract headers
        header_pattern = r"^(#{1,6})\s+(.+)$"
        for match in re.finditer(header_pattern, content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()
            line_num = content[: match.start()].count("\n") + 1

            structure.functions.append(
                {  # Reusing functions for headers
                    "name": title,
                    "line_start": line_num,
                    "type": f"h{level}",
                    "level": level,
                }
            )

        # Extract code blocks
        code_block_pattern = r"```(\w+)?\n(.*?)\n```"
        for match in re.finditer(code_block_pattern, content, re.DOTALL):
            language = match.group(1) or "text"
            code_content = match.group(2)
            line_num = content[: match.start()].count("\n") + 1

            structure.classes.append(
                {  # Reusing classes for code blocks
                    "name": f"Code block ({language})",
                    "line_start": line_num,
                    "type": "code_block",
                    "language": language,
                    "size": len(code_content),
                }
            )

    except Exception as e:
        structure.analysis_errors.append(f"Analysis error: {e}")
        logger.warning(f"Error analyzing Markdown file {file_path}: {e}")

    return structure


def analyze_file_structure(content: str, file_path: str) -> CodeStructure:
    """
    Analyze a file and extract structural information based on file type.

    Args:
        content: File content as string
        file_path: Path to the file

    Returns:
        CodeStructure object with extracted information
    """
    file_ext = Path(file_path).suffix.lower()

    if file_ext == ".py":
        return analyze_python_file(content, file_path)
    elif file_ext in [".js", ".ts", ".jsx", ".tsx"]:
        return analyze_javascript_file(content, file_path)
    elif file_ext == ".md":
        return analyze_markdown_file(content, file_path)
    else:
        # Generic analysis for other file types
        structure = CodeStructure(file_path, "generic")
        structure.total_lines = len(content.split("\n"))
        structure.total_chars = len(content)
        return structure


def create_file_summary(structure: CodeStructure, max_items: int = 20) -> str:
    """
    Create a condensed summary of a file's structure.

    Args:
        structure: CodeStructure object
        max_items: Maximum number of items to include in summary

    Returns:
        Formatted string summary
    """
    lines = []
    lines.append(f"📄 {structure.file_path} ({structure.file_type})")
    lines.append(f"   📊 {structure.total_lines} lines, {structure.total_chars:,} characters")

    if structure.analysis_errors:
        lines.append(f"   ⚠️ Analysis errors: {len(structure.analysis_errors)}")

    # Show imports (limited)
    if structure.imports:
        import_count = len(structure.imports)
        shown_imports = structure.imports[: min(5, max_items)]
        lines.append(f"   📦 Imports ({import_count}): {', '.join(shown_imports)}")
        if import_count > 5:
            lines.append(f"      ... and {import_count - 5} more")

    # Show classes
    if structure.classes:
        class_count = len(structure.classes)
        shown_classes = structure.classes[: min(5, max_items)]
        for cls in shown_classes:
            if structure.file_type == "markdown" and cls.get("type") == "code_block":
                lines.append(f"   📝 {cls['name']} (line {cls['line_start']}, {cls['size']} chars)")
            else:
                lines.append(f"   🏗️ class {cls['name']} (line {cls['line_start']})")
        if class_count > 5:
            lines.append(f"      ... and {class_count - 5} more classes")

    # Show functions
    if structure.functions:
        func_count = len(structure.functions)
        shown_functions = structure.functions[: min(10, max_items)]
        for func in shown_functions:
            if structure.file_type == "markdown" and func.get("type", "").startswith("h"):
                lines.append(f"   📑 {func['name']} (line {func['line_start']})")
            else:
                args_str = f"({', '.join(func.get('args', []))})" if func.get("args") else "()"
                async_str = "async " if func.get("is_async") else ""
                lines.append(f"   🔧 {async_str}{func['name']}{args_str} (line {func['line_start']})")
        if func_count > 10:
            lines.append(f"      ... and {func_count - 10} more functions")

    # Show constants
    if structure.constants:
        const_count = len(structure.constants)
        shown_constants = structure.constants[: min(3, max_items)]
        for const in shown_constants:
            lines.append(f"   📌 {const['name']} (line {const['line']})")
        if const_count > 3:
            lines.append(f"      ... and {const_count - 3} more constants")

    return "\n".join(lines)


def extract_key_functions(structure: CodeStructure, max_functions: int = 5) -> list[dict[str, Any]]:
    """
    Extract the most important functions from a code structure.

    Args:
        structure: CodeStructure object
        max_functions: Maximum number of functions to return

    Returns:
        List of function dictionaries with full details
    """
    if not structure.functions:
        return []

    # Filter out markdown headers
    code_functions = [f for f in structure.functions if not f.get("type", "").startswith("h")]

    # Sort by importance (public functions first, then by line number)
    def function_importance(func):
        score = 0
        # Public functions (no leading underscore) are more important
        if not func["name"].startswith("_"):
            score += 100
        # Functions with docstrings are more important
        if func.get("docstring"):
            score += 50
        # Earlier functions might be more important
        score += 1000 - func["line_start"]
        return score

    sorted_functions = sorted(code_functions, key=function_importance, reverse=True)
    return sorted_functions[:max_functions]
