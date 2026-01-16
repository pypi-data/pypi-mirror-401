# src/context_injection/semantic_tagging.py
import re


class SemanticTagger:
    """
    Handles semantic tagging and resolution for context injection.
    """

    def __init__(self, file_resolver: callable, workspace_root: str, project_root: str = None):
        self.file_resolver = file_resolver
        self.workspace_root = workspace_root
        self.project_root = project_root or workspace_root

    def resolve_tags(self, text: str) -> str:
        """
        Resolves semantic tags in the given text.
        """
        # @file tag resolution
        text = re.sub(r"@file\((.*?)\)", self._resolve_file_tag, text)

        # @symbol tag resolution
        text = re.sub(r"@symbol\((.*?)#(.*?)\)", self._resolve_symbol_tag, text)

        # @snippet tag resolution
        text = re.sub(r"@snippet\((.*?):L(\d+)-L(\d+)\)", self._resolve_snippet_tag, text)

        return text

    def _resolve_file_tag(self, match: re.Match) -> str:
        """
        Resolves an @file tag.
        """
        file_path = match.group(1)
        try:
            return self.file_resolver(file_path)
        except FileNotFoundError:
            return f"[File not found: {file_path}]"

    def _resolve_symbol_tag(self, match: re.Match) -> str:
        """
        Resolves an @symbol tag using AST parsing and regex fallback.
        """
        file_path = match.group(1)
        symbol_name = match.group(2)
        try:
            # Parse the file directly with Python AST for simple symbol extraction
            try:
                import ast

                content = self.file_resolver(file_path)
                lines = content.split("\n")
                tree = ast.parse(content, filename=file_path)
                for node in ast.walk(tree):
                    if (
                        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                        and getattr(node, "name", None) == symbol_name
                    ):
                        start_line = getattr(node, "lineno", 1)
                        end_line = getattr(node, "end_lineno", None)
                        if end_line is None:
                            # Heuristic: extend until next top-level def/class or EOF
                            end_line = start_line
                            for idx in range(start_line, len(lines)):
                                if (
                                    lines[idx]
                                    and not lines[idx].startswith((" ", "\t"))
                                    and (lines[idx].startswith("def ") or lines[idx].startswith("class "))
                                ):
                                    end_line = idx
                                    break
                            else:
                                end_line = len(lines)
                        # Clamp to file length
                        start_line = max(1, start_line)
                        end_line = min(len(lines), end_line)
                        result = "\n".join(lines[start_line - 1 : end_line])
                        return result
            except Exception:
                pass

            # Fallback: Regex-based scan for top-level def/class blocks
            try:
                content = self.file_resolver(file_path)
                lines = content.split("\n")
                import re as _re

                pattern = _re.compile(rf"^(def|class)\s+{_re.escape(symbol_name)}\b")
                start_idx = None
                for idx, line in enumerate(lines):
                    if pattern.match(line):
                        start_idx = idx
                        break
                if start_idx is not None:
                    end_idx = len(lines)
                    for idx in range(start_idx + 1, len(lines)):
                        if (
                            lines[idx]
                            and not lines[idx].startswith((" ", "\t"))
                            and (lines[idx].startswith("def ") or lines[idx].startswith("class "))
                        ):
                            end_idx = idx
                            break
                    result = "\n".join(lines[start_idx:end_idx])
                    return result
            except Exception:
                pass

            return f"[Symbol '{symbol_name}' not found in {file_path}]"

        except FileNotFoundError:
            return f"[File not found: {file_path}]"
        except Exception as e:
            return f"[Error resolving symbol '{symbol_name}': {e}]"

    def _resolve_snippet_tag(self, match: re.Match) -> str:
        """
        Resolves a @snippet tag.
        """
        file_path = match.group(1)
        start_line = int(match.group(2))
        end_line = int(match.group(3))
        try:
            content = self.file_resolver(file_path)
            lines = content.split("\n")
            if start_line > 0 and end_line <= len(lines):
                return "\n".join(lines[start_line - 1 : end_line])
            else:
                return f"[Invalid line numbers for snippet in {file_path}]"
        except FileNotFoundError:
            return f"[File not found: {file_path}]"
