"""
Context Injection for CCE Agent

Provides targeted context injection using @file, @symbol, and @snippet syntax.
Integrates with TreeSitter for semantic parsing (future enhancement).

Current implementation provides basic placeholder resolution.
Future versions will include full semantic analysis and ranking.
"""

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ContextReference:
    """A reference to be resolved for context injection."""

    type: str  # 'file', 'symbol', 'snippet'
    target: str  # file path, symbol name, or snippet query
    line_range: tuple[int, int] | None = None
    resolved_content: str | None = None
    error: str | None = None


class ContextInjector:
    """
    Resolves @-style context references in agent prompts.

    Supports:
    - @file:path/to/file.py - Include entire file
    - @file:path/to/file.py:10-20 - Include specific lines
    - @symbol:ClassName.method_name - Include symbol definition (future)
    - @snippet:search_query - Include relevant code snippets (future)
    """

    def __init__(self, workspace_root: str | None = None):
        """
        Initialize the context injector.

        Args:
            workspace_root: Root directory for resolving relative paths
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self.logger = logging.getLogger(__name__)

        # Pattern for matching @-style references
        self.reference_pattern = re.compile(r"@(file|symbol|snippet):([^:\s]+)(?::(\d+)-(\d+))?")

    def extract_references(self, text: str) -> list[ContextReference]:
        """
        Extract all @-style references from text.

        Args:
            text: Text to search for references

        Returns:
            List of context references found
        """
        references = []

        for match in self.reference_pattern.finditer(text):
            ref_type = match.group(1)
            target = match.group(2)
            start_line = int(match.group(3)) if match.group(3) else None
            end_line = int(match.group(4)) if match.group(4) else None

            line_range = (start_line, end_line) if start_line and end_line else None

            reference = ContextReference(type=ref_type, target=target, line_range=line_range)

            references.append(reference)

        self.logger.debug(f"🎯 Extracted {len(references)} context references")
        return references

    def resolve_file_reference(self, reference: ContextReference) -> str:
        """
        Resolve a file reference to actual content.

        Args:
            reference: File reference to resolve

        Returns:
            File content or error message
        """
        try:
            # Resolve relative to workspace root
            file_path = self.workspace_root / reference.target

            if not file_path.exists():
                # Try as absolute path
                file_path = Path(reference.target)

            if not file_path.exists():
                reference.error = f"File not found: {reference.target}"
                return f"<!-- ERROR: {reference.error} -->"

            if not file_path.is_file():
                reference.error = f"Not a file: {reference.target}"
                return f"<!-- ERROR: {reference.error} -->"

            # Read file content
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()

            # Apply line range if specified
            if reference.line_range:
                start_line, end_line = reference.line_range
                # Convert to 0-based indexing
                start_idx = max(0, start_line - 1)
                end_idx = min(len(lines), end_line)
                selected_lines = lines[start_idx:end_idx]
                content = "".join(selected_lines)

                header = f"<!-- @file:{reference.target}:{start_line}-{end_line} -->\n"
            else:
                content = "".join(lines)
                header = f"<!-- @file:{reference.target} -->\n"

            # Add line numbers for easier reference
            if reference.line_range:
                start_line_num = reference.line_range[0]
                numbered_lines = []
                for i, line in enumerate(content.splitlines()):
                    line_num = start_line_num + i
                    numbered_lines.append(f"{line_num:4d}|{line}")
                content = "\n".join(numbered_lines)
            else:
                numbered_lines = []
                for i, line in enumerate(content.splitlines(), 1):
                    numbered_lines.append(f"{i:4d}|{line}")
                content = "\n".join(numbered_lines)

            reference.resolved_content = content
            return header + "```" + self._get_file_extension(file_path) + "\n" + content + "\n```"

        except Exception as e:
            reference.error = f"Error reading file: {str(e)}"
            self.logger.warning(f"Failed to resolve file reference {reference.target}: {e}")
            return f"<!-- ERROR: {reference.error} -->"

    def resolve_symbol_reference(self, reference: ContextReference) -> str:
        """
        Resolve a symbol reference (stub implementation).

        Args:
            reference: Symbol reference to resolve

        Returns:
            Symbol definition or placeholder
        """
        # This is a stub - full implementation would use TreeSitter
        # to find and extract symbol definitions
        reference.error = "Symbol resolution not yet implemented"
        return f"<!-- TODO: Implement symbol resolution for {reference.target} -->"

    def resolve_snippet_reference(self, reference: ContextReference) -> str:
        """
        Resolve a snippet reference (stub implementation).

        Args:
            reference: Snippet reference to resolve

        Returns:
            Relevant code snippets or placeholder
        """
        # This is a stub - full implementation would use semantic search
        # to find relevant code snippets
        reference.error = "Snippet resolution not yet implemented"
        return f"<!-- TODO: Implement snippet resolution for '{reference.target}' -->"

    def resolve_reference(self, reference: ContextReference) -> str:
        """
        Resolve a context reference to actual content.

        Args:
            reference: Reference to resolve

        Returns:
            Resolved content
        """
        if reference.type == "file":
            return self.resolve_file_reference(reference)
        elif reference.type == "symbol":
            return self.resolve_symbol_reference(reference)
        elif reference.type == "snippet":
            return self.resolve_snippet_reference(reference)
        else:
            reference.error = f"Unknown reference type: {reference.type}"
            return f"<!-- ERROR: {reference.error} -->"

    def inject_context(self, text: str) -> tuple[str, list[ContextReference]]:
        """
        Replace all @-style references in text with resolved content.

        Args:
            text: Text containing references to resolve

        Returns:
            Tuple of (processed text, list of references)
        """
        references = self.extract_references(text)

        if not references:
            return text, []

        processed_text = text

        for reference in references:
            resolved_content = self.resolve_reference(reference)

            # Build the original reference string
            if reference.line_range:
                original_ref = (
                    f"@{reference.type}:{reference.target}:{reference.line_range[0]}-{reference.line_range[1]}"
                )
            else:
                original_ref = f"@{reference.type}:{reference.target}"

            # Replace in text
            processed_text = processed_text.replace(original_ref, resolved_content)

        successful_resolutions = len([r for r in references if not r.error])
        failed_resolutions = len([r for r in references if r.error])

        self.logger.info(f"🎯 Resolved {successful_resolutions} context references ({failed_resolutions} failed)")

        return processed_text, references

    def _get_file_extension(self, file_path: Path) -> str:
        """
        Get file extension for syntax highlighting.

        Args:
            file_path: Path to the file

        Returns:
            Extension for markdown code blocks
        """
        suffix = file_path.suffix.lower()

        # Map common extensions to markdown syntax highlighting
        extension_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".go": "go",
            ".rs": "rust",
            ".php": "php",
            ".rb": "ruby",
            ".sh": "bash",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".json": "json",
            ".xml": "xml",
            ".html": "html",
            ".css": "css",
            ".sql": "sql",
            ".md": "markdown",
            ".txt": "text",
        }

        return extension_map.get(suffix, "text")

    def get_stats(self) -> dict[str, Any]:
        """
        Get context injection statistics.

        Returns:
            Dictionary with statistics
        """
        return {
            "workspace_root": str(self.workspace_root),
            "supported_types": ["file", "symbol (stub)", "snippet (stub)"],
        }


# Global context injector (lazy initialization to avoid import side effects)
_global_injector: ContextInjector | None = None


def get_global_injector() -> ContextInjector:
    """Get the global context injector (lazy initialized)."""
    global _global_injector
    if _global_injector is None:
        _global_injector = ContextInjector()
    return _global_injector


def inject_context_in_text(text: str) -> tuple[str, list[ContextReference]]:
    """
    Convenience function to inject context using global injector.

    Args:
        text: Text to process

    Returns:
        Tuple of (processed text, references)
    """
    return get_global_injector().inject_context(text)
