"""
TreeSitter Code Analysis Tools

Provides advanced code parsing and analysis using TreeSitter for multiple languages.
Enables semantic understanding of code structure, AST traversal, and intelligent code analysis.
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from langchain_core.tools import tool

from .models import CodeAnalysisResponse, CodeAnalysisResult, CodeSymbol, SymbolExtractionResponse
from src.workspace_context import get_workspace_root

logger = logging.getLogger(__name__)


def _resolve_work_dir(work_dir: str | None) -> str:
    if work_dir and work_dir != ".":
        return work_dir
    resolved = get_workspace_root()
    return resolved or (work_dir or ".")


@dataclass
class CodeNode:
    """Represents a code node in the AST"""

    type: str
    text: str
    start_point: tuple[int, int]
    end_point: tuple[int, int]
    children: list["CodeNode"] = None
    metadata: dict[str, Any] = None


@dataclass
class CodeAnalysis:
    """Results of code analysis"""

    language: str
    functions: list[dict[str, Any]]
    classes: list[dict[str, Any]]
    imports: list[dict[str, Any]]
    variables: list[dict[str, Any]]
    comments: list[dict[str, Any]]
    ast_summary: str
    complexity_score: int
    line_count: int


class TreeSitterAnalyzer:
    """TreeSitter-based code analyzer"""

    def __init__(self):
        self.supported_languages = {
            "python": "tree-sitter-python",
            "javascript": "tree-sitter-javascript",
            "typescript": "tree-sitter-typescript",
            "java": "tree-sitter-java",
            "cpp": "tree-sitter-cpp",
            "c": "tree-sitter-c",
            "go": "tree-sitter-go",
            "rust": "tree-sitter-rust",
            "ruby": "tree-sitter-ruby",
            "php": "tree-sitter-php",
        }
        self._check_treesitter_installation()

    def _check_treesitter_installation(self):
        """Check if TreeSitter Python bindings are available and compatible"""
        try:
            import tree_sitter
            import tree_sitter_javascript
            import tree_sitter_python
            import tree_sitter_typescript

            # Test compatibility by trying to create a parser
            parser = tree_sitter.Parser()
            language = tree_sitter.Language(tree_sitter_python.language())
            parser.language = language

            # Only log once that TreeSitter is available
            if not hasattr(self, "_treesitter_available_logged"):
                logger.info("TreeSitter Python bindings available and compatible")
                self._treesitter_available_logged = True
            return True

        except (ImportError, ValueError, TypeError) as e:
            # Only log warning once
            if not hasattr(self, "_treesitter_warning_logged"):
                logger.info(f"TreeSitter not available or incompatible ({e}), using regex-based analysis")
                self._treesitter_warning_logged = True
            return False

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".mjs": "javascript",
            ".cjs": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".java": "java",
            ".cpp": "cpp",
            ".cc": "cpp",
            ".cxx": "cpp",
            ".c": "c",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
        }
        return language_map.get(ext, "unknown")

    async def analyze_file(self, file_path: str, content: str = None) -> CodeAnalysis:
        """
        Analyze a file using TreeSitter or fallback to regex-based analysis

        Args:
            file_path: Path to the file to analyze
            content: Optional file content (if not provided, will read from file)

        Returns:
            CodeAnalysis object with parsed code structure
        """
        try:
            if content is None:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

            language = self._detect_language(file_path)

            # Try TreeSitter first
            if self._check_treesitter_installation():
                try:
                    return await self._analyze_with_treesitter(file_path, content, language)
                except Exception as e:
                    logger.warning(f"TreeSitter analysis failed: {e}, falling back to regex")

            # Fallback to regex-based analysis
            return await self._analyze_with_regex(content, language)

        except Exception as e:
            logger.error(f"Code analysis failed for {file_path}: {e}")
            return self._create_empty_analysis(language)

    async def _analyze_with_treesitter(self, file_path: str, content: str, language: str) -> CodeAnalysis:
        """Analyze code using TreeSitter Python bindings"""
        try:
            import tree_sitter

            # Get the appropriate language parser
            if language == "python":
                import tree_sitter_python

                language_obj = tree_sitter.Language(tree_sitter_python.language())
            elif language == "javascript":
                import tree_sitter_javascript

                language_obj = tree_sitter.Language(tree_sitter_javascript.language())
            elif language == "typescript":
                import tree_sitter_typescript

                language_obj = tree_sitter.Language(tree_sitter_typescript.language())
            else:
                logger.warning(f"Unsupported language for TreeSitter: {language}")
                return await self._analyze_with_regex(content, language)

            # Parse the content
            parser = tree_sitter.Parser()
            parser.language = language_obj
            tree = parser.parse(bytes(content, "utf8"))

            # Extract analysis from the AST
            return self._extract_analysis_from_ast(tree, content, language)

        except Exception as e:
            logger.warning(f"TreeSitter Python bindings analysis failed: {e}")
            return await self._analyze_with_regex(content, language)

    def _extract_analysis_from_ast(self, tree, content: str, language: str) -> CodeAnalysis:
        """Parse TreeSitter AST output into structured analysis"""
        lines = content.split("\n")

        # Parse AST output to extract functions, classes, etc.
        functions = []
        classes = []
        imports = []
        variables = []
        comments = []

        # Traverse the AST to extract information
        def traverse_node(node, depth=0):
            if node.type in ["function_definition", "method_definition"]:
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                function_text = "\n".join(lines[start_line - 1 : end_line])
                functions.append(
                    {
                        "type": "function",
                        "line": start_line,
                        "text": function_text,
                        "name": self._extract_node_name(node, content),
                    }
                )
            elif node.type in ["class_definition"]:
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                class_text = "\n".join(lines[start_line - 1 : end_line])
                classes.append(
                    {
                        "type": "class",
                        "line": start_line,
                        "text": class_text,
                        "name": self._extract_node_name(node, content),
                    }
                )
            elif node.type in ["import_statement", "import_from_statement"]:
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                import_text = "\n".join(lines[start_line - 1 : end_line])
                imports.append({"type": "import", "line": start_line, "text": import_text})
            elif node.type in ["assignment", "variable_declaration"]:
                start_line = node.start_point[0] + 1
                variables.append(
                    {"type": "variable", "line": start_line, "name": self._extract_node_name(node, content)}
                )
            elif node.type in ["comment"]:
                start_line = node.start_point[0] + 1
                comment_text = content[node.start_byte : node.end_byte]
                comments.append({"type": "comment", "line": start_line, "text": comment_text})

            # Recursively traverse children
            for child in node.children:
                traverse_node(child, depth + 1)

        # Start traversal from root
        traverse_node(tree.root_node)

        return CodeAnalysis(
            language=language,
            functions=functions,
            classes=classes,
            imports=imports,
            variables=variables,
            comments=comments,
            ast_summary=f"Analyzed {len(functions)} functions, {len(classes)} classes, {len(imports)} imports",
            complexity_score=len(functions) + len(classes) * 2,
            line_count=len(lines),
        )

    def _extract_node_name(self, node, content: str) -> str:
        """Extract the name of a node (function, class, etc.)"""
        try:
            # Look for identifier child nodes
            for child in node.children:
                if child.type == "identifier":
                    return content[child.start_byte : child.end_byte]
            return "unknown"
        except Exception:
            return "unknown"

    def _extract_line_number(self, ast_line: str) -> int:
        """Extract line number from AST output"""
        try:
            # Simple regex to extract line number
            import re

            match = re.search(r"(\d+):", ast_line)
            return int(match.group(1)) if match else 0
        except:
            return 0

    def _extract_text_from_line(self, ast_line: str, content_lines: list[str]) -> str:
        """Extract text content from AST line"""
        line_num = self._extract_line_number(ast_line)
        if 0 <= line_num < len(content_lines):
            return content_lines[line_num].strip()
        return ""

    async def _analyze_with_regex(self, content: str, language: str) -> CodeAnalysis:
        """Fallback regex-based code analysis"""
        lines = content.split("\n")
        functions = []
        classes = []
        imports = []
        variables = []
        comments = []

        for i, line in enumerate(lines):
            line = line.strip()

            # Function detection
            if language == "python":
                if line.startswith("def ") or line.startswith("async def "):
                    functions.append({"type": "function", "line": i + 1, "text": line})
                elif line.startswith("class "):
                    classes.append({"type": "class", "line": i + 1, "text": line})
                elif line.startswith("import ") or line.startswith("from "):
                    imports.append({"type": "import", "line": i + 1, "text": line})

            elif language in ["javascript", "typescript"]:
                if "function " in line or "=>" in line or line.startswith("const ") and "=" in line:
                    functions.append({"type": "function", "line": i + 1, "text": line})
                elif line.startswith("class ") or line.startswith("interface "):
                    classes.append({"type": "class", "line": i + 1, "text": line})
                elif line.startswith("import ") or line.startswith("export "):
                    imports.append({"type": "import", "line": i + 1, "text": line})

            # Comment detection
            if line.startswith("#") or line.startswith("//") or line.startswith("/*"):
                comments.append({"type": "comment", "line": i + 1, "text": line})

        return CodeAnalysis(
            language=language,
            functions=functions,
            classes=classes,
            imports=imports,
            variables=variables,
            comments=comments,
            ast_summary=f"Regex analysis: {len(functions)} functions, {len(classes)} classes, {len(imports)} imports",
            complexity_score=len(functions) + len(classes) * 2,
            line_count=len(lines),
        )

    def _create_empty_analysis(self, language: str) -> CodeAnalysis:
        """Create empty analysis result"""
        return CodeAnalysis(
            language=language,
            functions=[],
            classes=[],
            imports=[],
            variables=[],
            comments=[],
            ast_summary="Analysis failed",
            complexity_score=0,
            line_count=0,
        )


# Global analyzer instance
_treesitter_analyzer: TreeSitterAnalyzer | None = None


def get_treesitter_analyzer() -> TreeSitterAnalyzer:
    """Get the global TreeSitter analyzer instance (lazy initialized)."""
    global _treesitter_analyzer
    if _treesitter_analyzer is None:
        _treesitter_analyzer = TreeSitterAnalyzer()
    return _treesitter_analyzer


@tool
async def analyze_code_structure(
    file_path: str, content: str | None = None, work_dir: str = "."
) -> CodeAnalysisResponse:
    """
    Analyze code structure using TreeSitter or regex-based parsing.

    Args:
        file_path: Path to the file to analyze
        content: Optional file content (if not provided, will read from file)
        work_dir: Working directory (default: current directory)

    Returns:
        Structured code analysis results
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        full_path = os.path.join(work_dir, file_path)

        if not os.path.exists(full_path) and content is None:
            return CodeAnalysisResponse(
                success=False,
                result=f"File not found: {file_path}",
                status="error",
                error_code="FILE_NOT_FOUND",
                error_hint="Ensure the file path is correct and the file exists",
            )

        analysis = await get_treesitter_analyzer().analyze_file(full_path, content)

        # Convert analysis to structured format
        functions = [
            CodeSymbol(
                name=func.get("name", ""), line_number=func.get("line", 0), text=func.get("text", ""), type="function"
            )
            for func in analysis.functions
        ]

        classes = [
            CodeSymbol(name=cls.get("name", ""), line_number=cls.get("line", 0), text=cls.get("text", ""), type="class")
            for cls in analysis.classes
        ]

        imports = [
            CodeSymbol(
                name=imp.get("name", ""), line_number=imp.get("line", 0), text=imp.get("text", ""), type="import"
            )
            for imp in analysis.imports
        ]

        variables = [
            CodeSymbol(
                name=var.get("name", ""), line_number=var.get("line", 0), text=var.get("text", ""), type="variable"
            )
            for var in analysis.variables
        ]

        analysis_result = CodeAnalysisResult(
            language=analysis.language,
            functions=functions,
            classes=classes,
            imports=imports,
            variables=variables,
            comments=analysis.comments,
            ast_summary=analysis.ast_summary,
            complexity_score=analysis.complexity_score,
            line_count=analysis.line_count,
        )

        return CodeAnalysisResponse(
            success=True,
            result=f"Successfully analyzed {file_path}",
            status="success",
            analysis=analysis_result,
            metadata={
                "file_path": file_path,
                "analysis_method": "treesitter" if analysis.language != "unknown" else "regex",
            },
        )

    except Exception as e:
        return CodeAnalysisResponse(
            success=False,
            result=f"Code analysis failed: {str(e)}",
            status="error",
            error_code="ANALYSIS_ERROR",
            error_hint="Check file format and try again",
        )


@tool
async def extract_code_symbols(
    file_path: str, symbol_type: str = "all", work_dir: str = "."
) -> SymbolExtractionResponse:
    """
    Extract specific code symbols (functions, classes, imports) from a file.

    Args:
        file_path: Path to the file to analyze
        symbol_type: Type of symbols to extract ("functions", "classes", "imports", "all")
        work_dir: Working directory (default: current directory)

    Returns:
        Dictionary containing extracted symbols
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        full_path = os.path.join(work_dir, file_path)

        if not os.path.exists(full_path):
            return {"success": False, "result": f"File not found: {file_path}", "status": "error"}

        analysis = await get_treesitter_analyzer().analyze_file(full_path)

        result = {"file_path": file_path, "language": analysis.language, "symbols": {}}

        if symbol_type in ["functions", "all"]:
            result["symbols"]["functions"] = analysis.functions

        if symbol_type in ["classes", "all"]:
            result["symbols"]["classes"] = analysis.classes

        if symbol_type in ["imports", "all"]:
            result["symbols"]["imports"] = analysis.imports

        if symbol_type in ["variables", "all"]:
            result["symbols"]["variables"] = analysis.variables

        return {"success": True, "result": result, "status": "success"}

    except Exception as e:
        return {"success": False, "result": f"Symbol extraction failed: {str(e)}", "status": "error"}


@tool
async def calculate_code_complexity(file_path: str, work_dir: str = ".") -> dict[str, Any]:
    """
    Calculate code complexity metrics for a file.

    Args:
        file_path: Path to the file to analyze
        work_dir: Working directory (default: current directory)

    Returns:
        Dictionary containing complexity metrics
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        full_path = os.path.join(work_dir, file_path)

        if not os.path.exists(full_path):
            return {"success": False, "result": f"File not found: {file_path}", "status": "error"}

        analysis = await get_treesitter_analyzer().analyze_file(full_path)

        # Calculate additional complexity metrics
        cyclomatic_complexity = analysis.complexity_score
        maintainability_index = max(0, 100 - (cyclomatic_complexity * 2))

        return {
            "success": True,
            "result": {
                "file_path": file_path,
                "language": analysis.language,
                "line_count": analysis.line_count,
                "function_count": len(analysis.functions),
                "class_count": len(analysis.classes),
                "import_count": len(analysis.imports),
                "cyclomatic_complexity": cyclomatic_complexity,
                "maintainability_index": maintainability_index,
                "complexity_level": "low"
                if cyclomatic_complexity < 10
                else "medium"
                if cyclomatic_complexity < 20
                else "high",
            },
            "status": "success",
        }

    except Exception as e:
        return {"success": False, "result": f"Complexity calculation failed: {str(e)}", "status": "error"}


__all__ = [
    "analyze_code_structure",
    "extract_code_symbols",
    "calculate_code_complexity",
    "TreeSitterAnalyzer",
    "CodeAnalysis",
    "CodeNode",
]
