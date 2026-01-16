"""
Repository Indexer for Advanced Code Analysis

Provides comprehensive symbol indexing and context-aware code analysis using TreeSitter.
Enables intelligent code navigation, symbol queries, and context-aware diff generation.
"""

import json
import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from src.tools.openswe.treesitter_tools import TreeSitterAnalyzer

logger = logging.getLogger(__name__)


@dataclass
class SymbolMatch:
    """Represents a symbol match in the repository"""

    file_path: str
    symbol_name: str
    symbol_type: str  # function, class, variable, import
    line_number: int
    column_number: int
    context: str  # Surrounding code context
    signature: str  # Function signature or class definition
    docstring: str | None = None
    complexity_score: int = 0
    dependencies: list[str] = None  # Other symbols this depends on
    dependents: list[str] = None  # Symbols that depend on this


@dataclass
class FileContext:
    """Context information for a file"""

    file_path: str
    language: str
    line_count: int
    symbol_count: int
    complexity_score: int
    last_modified: datetime
    imports: list[str]
    exports: list[str]  # Functions/classes defined in this file
    dependencies: list[str]  # Files this file imports from
    dependents: list[str]  # Files that import from this file


@dataclass
class RepositoryIndex:
    """Complete repository index"""

    root_path: str
    indexed_at: datetime
    total_files: int
    total_symbols: int
    languages: dict[str, int]  # language -> file count
    file_contexts: dict[str, FileContext]
    symbol_index: dict[str, list[SymbolMatch]]  # symbol_name -> matches
    dependency_graph: dict[str, set[str]]  # file -> dependencies
    complexity_metrics: dict[str, Any]


class RepoIndexer:
    """Advanced repository indexer with TreeSitter integration"""

    def __init__(self, root_path: str, cache_dir: str | None = None):
        """
        Initialize the repository indexer.

        Args:
            root_path: Root path of the repository to index
            cache_dir: Optional cache directory for index persistence
        """
        self.root_path = Path(root_path).resolve()
        self.cache_dir = Path(cache_dir) if cache_dir else self.root_path / ".repo_index"
        self.cache_dir.mkdir(exist_ok=True)

        self.analyzer = TreeSitterAnalyzer()
        self.logger = logging.getLogger(__name__)

        # Supported file extensions
        self.supported_extensions = {
            ".py",
            ".js",
            ".mjs",
            ".cjs",
            ".ts",
            ".tsx",
            ".jsx",
            ".java",
            ".cpp",
            ".cc",
            ".cxx",
            ".c",
            ".go",
            ".rs",
            ".rb",
            ".php",
            ".cs",
            ".swift",
            ".kt",
            ".scala",
        }

        # Index cache
        self._index_cache: RepositoryIndex | None = None
        self._index_db_path = self.cache_dir / "index.db"

    async def build_index(self, force_rebuild: bool = False) -> RepositoryIndex:
        """
        Build comprehensive repository index.

        Args:
            force_rebuild: Force rebuild even if cache exists

        Returns:
            RepositoryIndex with complete symbol and dependency information
        """
        # Check if we can use cached index
        if not force_rebuild and await self._is_cache_valid():
            self.logger.info("Using cached repository index")
            return await self._load_cached_index()

        self.logger.info(f"Building repository index for {self.root_path}")

        # Find all source files
        source_files = await self._find_source_files()
        self.logger.info(f"Found {len(source_files)} source files")

        # Analyze each file
        file_contexts = {}
        all_symbols = []
        dependency_graph = {}

        for file_path in source_files:
            try:
                context, symbols = await self._analyze_file(file_path)
                # Store relative path in index for consistency
                rel_path = str(file_path.relative_to(self.root_path))
                file_contexts[rel_path] = context
                all_symbols.extend(symbols)
                dependency_graph[rel_path] = set(context.dependencies)
            except Exception as e:
                self.logger.warning(f"Failed to analyze {file_path}: {e}")

        # Build symbol index
        symbol_index = self._build_symbol_index(all_symbols)

        # Calculate complexity metrics
        complexity_metrics = self._calculate_complexity_metrics(file_contexts)

        # Count languages
        languages = {}
        for context in file_contexts.values():
            lang = context.language
            languages[lang] = languages.get(lang, 0) + 1

        # Create repository index
        index = RepositoryIndex(
            root_path=str(self.root_path),
            indexed_at=datetime.now(),
            total_files=len(file_contexts),
            total_symbols=len(all_symbols),
            languages=languages,
            file_contexts=file_contexts,
            symbol_index=symbol_index,
            dependency_graph=dependency_graph,
            complexity_metrics=complexity_metrics,
        )

        # Cache the index
        await self._cache_index(index)

        self._index_cache = index
        self.logger.info(f"Repository index built: {index.total_files} files, {index.total_symbols} symbols")

        return index

    def query_symbols(
        self, query: str, kind: str = "symbol", file_filter: str | None = None, max_results: int = 50
    ) -> list[SymbolMatch]:
        """
        Query symbols in the repository.

        Args:
            query: Search query (symbol name or pattern)
            kind: Type of symbols to search for (function, class, variable, all)
            file_filter: Optional file path filter
            max_results: Maximum number of results to return

        Returns:
            List of matching symbols
        """
        # Use the cached index if available, otherwise return empty list
        if self._index_cache is None:
            return []
        index = self._index_cache

        matches = []
        query_lower = query.lower()

        for symbol_name, symbol_matches in index.symbol_index.items():
            if query_lower in symbol_name.lower():
                for match in symbol_matches:
                    # Apply filters
                    if kind != "all" and match.symbol_type != kind:
                        continue

                    if file_filter and file_filter not in match.file_path:
                        continue

                    matches.append(match)

                    if len(matches) >= max_results:
                        break

                if len(matches) >= max_results:
                    break

        # Sort by relevance (exact matches first, then by complexity)
        matches.sort(
            key=lambda m: (
                m.symbol_name.lower() != query_lower,  # Exact matches first
                -m.complexity_score,  # Higher complexity first
            )
        )

        return matches[:max_results]

    async def get_file_context(self, file_path: str, symbol: str | None = None) -> str:
        """
        Get comprehensive context for a file or specific symbol.

        Args:
            file_path: Path to the file
            symbol: Optional specific symbol to get context for

        Returns:
            Formatted context string
        """
        index = self._get_or_build_index()

        # Convert to relative path if needed
        try:
            if os.path.isabs(file_path):
                file_path = str(Path(file_path).relative_to(self.root_path))
        except ValueError:
            pass  # Already relative or not under root

        if file_path not in index.file_contexts:
            return f"File not found in index: {file_path}"

        context = index.file_contexts[file_path]

        if symbol:
            # Get context for specific symbol
            symbol_matches = index.symbol_index.get(symbol, [])
            file_symbols = [m for m in symbol_matches if m.file_path == file_path]

            if not file_symbols:
                return f"Symbol '{symbol}' not found in {file_path}"

            match = file_symbols[0]  # Take first match
            return self._format_symbol_context(match, context)
        else:
            # Get full file context
            return self._format_file_context(context)

    async def get_dependency_context(self, file_path: str, depth: int = 2) -> dict[str, Any]:
        """
        Get dependency context for a file.

        Args:
            file_path: Path to the file
            depth: How many levels of dependencies to include

        Returns:
            Dictionary with dependency information
        """
        index = self._get_or_build_index()

        # Convert to relative path if needed
        try:
            if os.path.isabs(file_path):
                file_path = str(Path(file_path).relative_to(self.root_path))
        except ValueError:
            pass  # Already relative or not under root

        if file_path not in index.file_contexts:
            return {"error": f"File not found in index: {file_path}"}

        visited = set()
        dependencies = set()
        dependents = set()

        def collect_deps(current_file: str, current_depth: int):
            if current_depth <= 0 or current_file in visited:
                return

            visited.add(current_file)

            if current_file in index.dependency_graph:
                for dep in index.dependency_graph[current_file]:
                    dependencies.add(dep)
                    collect_deps(dep, current_depth - 1)

            # Find dependents
            for other_file, deps in index.dependency_graph.items():
                if current_file in deps:
                    dependents.add(other_file)

        collect_deps(file_path, depth)

        return {
            "file": file_path,
            "dependencies": list(dependencies),
            "dependents": list(dependents),
            "depth": depth,
            "context": index.file_contexts[file_path],
        }

    async def _find_source_files(self) -> list[Path]:
        """Find all source files in the repository, limited to src/ directory"""
        source_files = []

        # Limit scanning to src/ directory only
        src_path = self.root_path / "src"
        if not src_path.exists():
            self.logger.warning(f"src/ directory not found at {src_path}, scanning entire repository")
            scan_path = self.root_path
        else:
            self.logger.info(f"Limiting repository indexing to src/ directory: {src_path}")
            scan_path = src_path

        for root, dirs, files in os.walk(scan_path):
            # Skip hidden directories and common build/cache directories
            dirs[:] = [
                d
                for d in dirs
                if not d.startswith(".")
                and d not in {"node_modules", "__pycache__", "build", "dist", "target", "bin", "obj"}
            ]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.supported_extensions:
                    source_files.append(file_path)

        return source_files

    async def _analyze_file(self, file_path: Path) -> tuple[FileContext, list[SymbolMatch]]:
        """Analyze a single file and extract context and symbols"""
        try:
            # Get file stats
            stat = file_path.stat()
            last_modified = datetime.fromtimestamp(stat.st_mtime)

            # Analyze with TreeSitter
            analysis = await self.analyzer.analyze_file(str(file_path))

            # Extract symbols
            symbols = []

            # Get relative path for symbols
            rel_path = str(file_path.relative_to(self.root_path))

            # Process functions
            for func in analysis.functions:
                symbol = SymbolMatch(
                    file_path=rel_path,
                    symbol_name=self._extract_symbol_name(func.get("text", "")),
                    symbol_type="function",
                    line_number=func.get("line", 0),
                    column_number=0,
                    context=self._get_context_around_line(file_path, func.get("line", 0)),
                    signature=func.get("text", ""),
                    complexity_score=1,
                )
                symbols.append(symbol)

            # Process classes
            for cls in analysis.classes:
                symbol = SymbolMatch(
                    file_path=rel_path,
                    symbol_name=self._extract_symbol_name(cls.get("text", "")),
                    symbol_type="class",
                    line_number=cls.get("line", 0),
                    column_number=0,
                    context=self._get_context_around_line(file_path, cls.get("line", 0)),
                    signature=cls.get("text", ""),
                    complexity_score=2,
                )
                symbols.append(symbol)

            # Process imports
            imports = []
            for imp in analysis.imports:
                import_text = imp.get("text", "")
                imports.append(import_text)

            # Create file context
            context = FileContext(
                file_path=rel_path,
                language=analysis.language,
                line_count=analysis.line_count,
                symbol_count=len(symbols),
                complexity_score=analysis.complexity_score,
                last_modified=last_modified,
                imports=imports,
                exports=[s.symbol_name for s in symbols],
                dependencies=self._extract_dependencies(imports),
                dependents=[],  # Will be filled later
            )

            return context, symbols

        except Exception as e:
            self.logger.error(f"Failed to analyze {file_path}: {e}")
            # Return empty context
            return FileContext(
                file_path=str(file_path),
                language="unknown",
                line_count=0,
                symbol_count=0,
                complexity_score=0,
                last_modified=datetime.now(),
                imports=[],
                exports=[],
                dependencies=[],
                dependents=[],
            ), []

    def _extract_symbol_name(self, text: str) -> str:
        """Extract symbol name from definition text"""
        # Simple extraction - in production, use proper AST parsing
        import re

        # Function definition patterns
        func_patterns = [r"def\s+(\w+)", r"function\s+(\w+)", r"(\w+)\s*\([^)]*\)\s*{", r"(\w+)\s*\([^)]*\)\s*=>"]

        # Class definition patterns
        class_patterns = [r"class\s+(\w+)", r"interface\s+(\w+)", r"type\s+(\w+)"]

        for pattern in func_patterns + class_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return text.split()[0] if text.split() else "unknown"

    def _get_context_around_line(self, file_path: Path, line_number: int, context_lines: int = 3) -> str:
        """Get context around a specific line"""
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()

            start = max(0, line_number - context_lines - 1)
            end = min(len(lines), line_number + context_lines)

            context_lines_list = []
            for i in range(start, end):
                prefix = ">>> " if i == line_number - 1 else "    "
                context_lines_list.append(f"{prefix}{i + 1:4d}: {lines[i].rstrip()}")

            return "\n".join(context_lines_list)

        except Exception:
            return f"Context unavailable for line {line_number}"

    def _extract_dependencies(self, imports: list[str]) -> list[str]:
        """Extract file dependencies from import statements"""
        dependencies = []

        for import_stmt in imports:
            # Simple extraction - in production, use proper parsing
            import re

            # Python imports
            if "from" in import_stmt and "import" in import_stmt:
                match = re.search(r"from\s+([^\s]+)", import_stmt)
                if match:
                    dependencies.append(match.group(1))
            elif import_stmt.startswith("import"):
                match = re.search(r"import\s+([^\s,]+)", import_stmt)
                if match:
                    dependencies.append(match.group(1))

            # JavaScript/TypeScript imports
            elif "import" in import_stmt and "from" in import_stmt:
                match = re.search(r'from\s+[\'"]([^\'"]+)[\'"]', import_stmt)
                if match:
                    dependencies.append(match.group(1))
            elif import_stmt.startswith("import"):
                match = re.search(r'import\s+[\'"]([^\'"]+)[\'"]', import_stmt)
                if match:
                    dependencies.append(match.group(1))

        return dependencies

    def _build_symbol_index(self, symbols: list[SymbolMatch]) -> dict[str, list[SymbolMatch]]:
        """Build symbol index from list of symbols"""
        index = {}

        for symbol in symbols:
            if symbol.symbol_name not in index:
                index[symbol.symbol_name] = []
            index[symbol.symbol_name].append(symbol)

        return index

    def _calculate_complexity_metrics(self, file_contexts: dict[str, FileContext]) -> dict[str, Any]:
        """Calculate repository-wide complexity metrics"""
        total_files = len(file_contexts)
        total_symbols = sum(ctx.symbol_count for ctx in file_contexts.values())
        total_complexity = sum(ctx.complexity_score for ctx in file_contexts.values())

        # Find most complex files
        complex_files = sorted(file_contexts.items(), key=lambda x: x[1].complexity_score, reverse=True)[:10]

        # Language distribution
        language_dist = {}
        for ctx in file_contexts.values():
            language_dist[ctx.language] = language_dist.get(ctx.language, 0) + 1

        return {
            "total_files": total_files,
            "total_symbols": total_symbols,
            "average_complexity": total_complexity / total_files if total_files > 0 else 0,
            "most_complex_files": [{"file": file, "complexity": ctx.complexity_score} for file, ctx in complex_files],
            "language_distribution": language_dist,
        }

    def _format_symbol_context(self, symbol: SymbolMatch, file_context: FileContext) -> str:
        """Format context for a specific symbol"""
        return f"""
Symbol: {symbol.symbol_name} ({symbol.symbol_type})
File: {symbol.file_path}
Location: Line {symbol.line_number}
Signature: {symbol.signature}

Context:
{symbol.context}

File Info:
- Language: {file_context.language}
- Lines: {file_context.line_count}
- Complexity: {file_context.complexity_score}
- Dependencies: {", ".join(file_context.dependencies[:5])}
"""

    def _format_file_context(self, context: FileContext) -> str:
        """Format context for a file"""
        return f"""
File: {context.file_path}
Language: {context.language}
Lines: {context.line_count}
Symbols: {context.symbol_count}
Complexity: {context.complexity_score}
Last Modified: {context.last_modified}

Exports:
{chr(10).join(f"- {export}" for export in context.exports[:10])}

Dependencies:
{chr(10).join(f"- {dep}" for dep in context.dependencies[:10])}
"""

    def _get_or_build_index(self) -> RepositoryIndex:
        """Get existing index or build new one"""
        if self._index_cache is None:
            # This is a synchronous method, but we need to handle the async build_index
            import asyncio

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If we're in an async context, we can't use run_until_complete
                    # So we'll need to handle this differently
                    raise RuntimeError("Cannot build index synchronously in async context")
                else:
                    self._index_cache = loop.run_until_complete(self.build_index())
            except RuntimeError:
                # Fallback: create a simple index
                self._index_cache = RepositoryIndex(
                    root_path=str(self.root_path),
                    indexed_at=datetime.now(),
                    total_files=0,
                    total_symbols=0,
                    languages={},
                    file_contexts={},
                    symbol_index={},
                    dependency_graph={},
                    complexity_metrics={},
                )
        return self._index_cache

    async def _is_cache_valid(self) -> bool:
        """Check if cached index is still valid"""
        if not self._index_db_path.exists():
            return False

        # Check if any source files have been modified since last index
        try:
            with open(self.cache_dir / "index_metadata.json") as f:
                metadata = json.load(f)

            last_indexed = datetime.fromisoformat(metadata["indexed_at"])

            # Check if any source files are newer than the index
            source_files = await self._find_source_files()
            for file_path in source_files:
                if file_path.stat().st_mtime > last_indexed.timestamp():
                    return False

            return True

        except Exception:
            return False

    async def _load_cached_index(self) -> RepositoryIndex:
        """Load index from cache"""
        try:
            with open(self.cache_dir / "index_metadata.json") as f:
                metadata = json.load(f)

            # Load file contexts
            with open(self.cache_dir / "file_contexts.json") as f:
                file_contexts_data = json.load(f)

            file_contexts = {}
            for path, data in file_contexts_data.items():
                data["last_modified"] = datetime.fromisoformat(data["last_modified"])
                file_contexts[path] = FileContext(**data)

            # Load symbol index
            with open(self.cache_dir / "symbol_index.json") as f:
                symbol_index_data = json.load(f)

            symbol_index = {}
            for symbol_name, matches_data in symbol_index_data.items():
                symbol_index[symbol_name] = [SymbolMatch(**match) for match in matches_data]

            # Load dependency graph
            with open(self.cache_dir / "dependency_graph.json") as f:
                dependency_graph_data = json.load(f)

            dependency_graph = {path: set(deps) for path, deps in dependency_graph_data.items()}

            return RepositoryIndex(
                root_path=metadata["root_path"],
                indexed_at=datetime.fromisoformat(metadata["indexed_at"]),
                total_files=metadata["total_files"],
                total_symbols=metadata["total_symbols"],
                languages=metadata["languages"],
                file_contexts=file_contexts,
                symbol_index=symbol_index,
                dependency_graph=dependency_graph,
                complexity_metrics=metadata["complexity_metrics"],
            )

        except Exception as e:
            self.logger.warning(f"Failed to load cached index: {e}")
            raise

    async def _cache_index(self, index: RepositoryIndex):
        """Cache the index to disk"""
        try:
            # Save metadata
            metadata = {
                "root_path": index.root_path,
                "indexed_at": index.indexed_at.isoformat(),
                "total_files": index.total_files,
                "total_symbols": index.total_symbols,
                "languages": index.languages,
                "complexity_metrics": index.complexity_metrics,
            }

            with open(self.cache_dir / "index_metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)

            # Save file contexts
            file_contexts_data = {}
            for path, context in index.file_contexts.items():
                data = asdict(context)
                data["last_modified"] = data["last_modified"].isoformat()
                file_contexts_data[path] = data

            with open(self.cache_dir / "file_contexts.json", "w") as f:
                json.dump(file_contexts_data, f, indent=2)

            # Save symbol index
            symbol_index_data = {}
            for symbol_name, matches in index.symbol_index.items():
                symbol_index_data[symbol_name] = [asdict(match) for match in matches]

            with open(self.cache_dir / "symbol_index.json", "w") as f:
                json.dump(symbol_index_data, f, indent=2)

            # Save dependency graph
            dependency_graph_data = {path: list(deps) for path, deps in index.dependency_graph.items()}

            with open(self.cache_dir / "dependency_graph.json", "w") as f:
                json.dump(dependency_graph_data, f, indent=2)

            self.logger.info(f"Index cached to {self.cache_dir}")

        except Exception as e:
            self.logger.error(f"Failed to cache index: {e}")


# Global instance for easy access
_repo_indexer: RepoIndexer | None = None


def get_repo_indexer(root_path: str = None) -> RepoIndexer:
    """Get or create global repository indexer instance"""
    global _repo_indexer

    if _repo_indexer is None or (root_path and _repo_indexer.root_path != Path(root_path)):
        if root_path is None:
            root_path = os.getcwd()
        _repo_indexer = RepoIndexer(root_path)

    return _repo_indexer


__all__ = ["RepoIndexer", "RepositoryIndex", "SymbolMatch", "FileContext", "get_repo_indexer"]
