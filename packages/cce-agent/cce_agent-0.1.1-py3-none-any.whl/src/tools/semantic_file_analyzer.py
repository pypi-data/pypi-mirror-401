"""
Semantic File Analysis Models and Classes

This module provides semantic analysis capabilities for codebase files,
extending the basic CodeAnalyzer with embedding-based file discovery,
architectural classification, and dependency analysis.
"""

import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.semantic.embeddings import InMemoryVectorIndex, create_embedding_provider

from .code_analyzer import CodeAnalyzer
from .plan_generation.topic_analyzer import TopicAnalysisGraph
from .shell_runner import ShellRunner

logger = logging.getLogger(__name__)


@dataclass
class ArchitecturalFile:
    """Rich file representation with semantic context and architectural insights."""

    path: str
    semantic_summary: str = ""  # What this file does (LLM-generated)
    architectural_role: str = ""  # "controller", "data_layer", "ui_component", etc.
    file_type: str = ""  # "model", "service", "config", "test", "component"
    relevance_score: float = 0.0  # 0.0-1.0 similarity to plan topic
    dependencies: list[str] = None  # Files this depends on
    dependents: list[str] = None  # Files that depend on this
    key_functions: list[str] = None  # Main functions/classes
    modification_complexity: str = "medium"  # "low", "medium", "high"
    content_preview: str = ""  # First 1000 chars for context

    def __post_init__(self):
        """Initialize mutable fields."""
        if self.dependencies is None:
            self.dependencies = []
        if self.dependents is None:
            self.dependents = []
        if self.key_functions is None:
            self.key_functions = []


class SemanticCodeAnalyzer(CodeAnalyzer):
    """Enhanced CodeAnalyzer with semantic understanding and architectural insights."""

    def __init__(self, shell: ShellRunner, embedding_provider=None, enable_caching: bool = True):
        super().__init__(shell)
        self.embedding_provider = embedding_provider or create_embedding_provider("auto")
        self.file_index = InMemoryVectorIndex(self.embedding_provider)
        self.architecture_cache = {} if enable_caching else None
        self.initialized = False
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            "SemanticCodeAnalyzer initialized (base_directory=%s, embedding_provider=%s, caching=%s)",
            getattr(self.shell, "base_directory", os.getcwd()),
            type(self.embedding_provider).__name__,
            enable_caching,
        )
        self._missing_file_log_count = 0
        self._missing_file_log_limit = 5

    async def discover_architecturally_relevant_files(
        self, plan_topic: str, context: str = "", use_llm: bool = False
    ) -> list[ArchitecturalFile]:
        """
        Discover files using multi-stage semantic analysis.

        Args:
            plan_topic: The plan topic to find relevant files for
            context: Additional context for the search

        Returns:
            List of ArchitecturalFile objects ranked by relevance
        """
        try:
            if use_llm:
                # Use LLM-based reasoning for file discovery
                llm_graph = TopicAnalysisGraph()
                llm_analysis = await llm_graph.analyze_and_structure_plan(plan_topic, context, "")
                self.logger.info(f"LLM Analysis Result: {llm_analysis}")
                # Convert LLM analysis to ArchitecturalFile objects if needed
                # This is a placeholder for actual conversion logic
            if not self.initialized:
                await self._initialize_codebase_index()

            if not self.initialized:  # Still not initialized, return empty
                self.logger.warning("Codebase indexing failed, returning empty results")
                return []

            # Stage 1: Semantic similarity search
            semantic_matches = await self._semantic_file_discovery(plan_topic, context)

            # Stage 2: Dependency-based expansion
            dependency_matches = await self._dependency_based_discovery(semantic_matches, plan_topic)

            # Stage 3: Architectural pattern matching
            architectural_matches = await self._architectural_pattern_discovery(plan_topic, context)

            # Combine and rank all results
            combined_results = self._merge_and_rank_results(semantic_matches, dependency_matches, architectural_matches)

            # Return top 15 most relevant files
            return combined_results[:15]

        except Exception as e:
            self.logger.error(f"Error in semantic file discovery: {e}")
            return []

    async def _initialize_codebase_index(self):
        """Build semantic index of all code files with content analysis."""
        try:
            self.logger.info("Initializing codebase semantic index...")

            # Discover all code files
            code_files = await self._discover_all_code_files()
            self.logger.info("Code file discovery returned %s files", len(code_files))

            if not code_files:
                base_directory = getattr(self.shell, "base_directory", os.getcwd())
                self.logger.warning("No code files found for indexing (base_directory=%s)", base_directory)
                return
            self.logger.info("Code file sample: %s", code_files[:5])

            # Analyze files in batches for efficiency
            batch_size = 10
            file_summaries = []
            summary_stats = {
                "total": 0,
                "summarized": 0,
                "skipped_unreadable": 0,
                "skipped_no_summary": 0,
            }

            for i in range(0, len(code_files), batch_size):
                batch = code_files[i : i + batch_size]
                batch_summaries, batch_stats = await self._analyze_file_batch(batch)
                file_summaries.extend(batch_summaries)
                for key in summary_stats:
                    summary_stats[key] += batch_stats.get(key, 0)

            if not file_summaries:
                base_directory = getattr(self.shell, "base_directory", os.getcwd())
                self.logger.warning(
                    "No file summaries generated (files_total=%s summarized=%s skipped_unreadable=%s skipped_no_summary=%s base_directory=%s)",
                    summary_stats["total"],
                    summary_stats["summarized"],
                    summary_stats["skipped_unreadable"],
                    summary_stats["skipped_no_summary"],
                    base_directory,
                )
                return

            # Build vector index for semantic search
            texts = [f"{item['path']}: {item['summary']}" for item in file_summaries if item.get("summary")]
            metadata = [
                {
                    "path": item["path"],
                    "dependencies": item.get("dependencies", []),
                    "preview": item.get("content_preview", ""),
                    "file_type": item.get("file_type", "general"),
                    "architectural_role": item.get("architectural_role", "general"),
                }
                for item in file_summaries
                if item.get("summary")
            ]

            if texts:
                try:
                    self.file_index.add_batch(texts, metadata)
                    self.initialized = True
                    self.logger.info(f"Initialized semantic index with {len(texts)} files")
                except Exception as exc:
                    self.initialized = False
                    self.logger.warning(
                        "Semantic index build failed: %s. Set CCE_EMBEDDING_PROVIDER=local to avoid remote embedding errors.",
                        exc,
                    )
                    return
            else:
                self.logger.warning("No texts available for indexing")

        except Exception as e:
            self.logger.error(f"Failed to initialize codebase index: {e}")
            self.initialized = False

    async def _discover_all_code_files(self) -> list[str]:
        """Discover all code files in the repository, using configuration."""
        try:
            # Import configuration
            from .file_discovery_config import get_discovery_config

            config = get_discovery_config()

            # Get allowed directories
            allowed_paths = config["allowed_directories"]
            excluded_dirs = config["excluded_directories"]
            excluded_patterns = config["excluded_file_patterns"]
            allowed_extensions = config["allowed_file_extensions"]
            allowed_names = config.get("allowed_file_names", [])
            max_files = config["max_files_limit"]

            # Check which allowed paths exist relative to the workspace root
            base_directory = getattr(self.shell, "base_directory", os.getcwd())
            self.logger.info(
                "Discovery config (base_directory=%s, allowed_paths=%s, excluded_dirs=%s, max_files=%s)",
                base_directory,
                allowed_paths,
                excluded_dirs,
                max_files,
            )
            existing_paths = []
            for path in allowed_paths:
                check_path = path if os.path.isabs(path) else os.path.join(base_directory, path)
                if os.path.exists(check_path):
                    existing_paths.append(path)

            if not existing_paths:
                self.logger.warning(
                    "No allowed paths found under base_directory=%s (allowed_paths=%s); scanning entire repository",
                    base_directory,
                    allowed_paths,
                )
                scan_path = "."
            else:
                # Create a find command that only scans allowed paths
                path_filter = " \\( " + " -o ".join(f"-path '{path}/*'" for path in existing_paths) + " \\)"
                self.logger.info(f"Limiting code file discovery to: {existing_paths}")
                scan_path = "."

            if scan_path == "." and existing_paths:
                # Use path filter for specific directories
                find_cmd = f"find . -type f {path_filter}"
            else:
                find_cmd = f"find {scan_path} -type f"
            # Add exclusion patterns
            for pattern in excluded_patterns:
                if "*" in pattern:
                    find_cmd += f" ! -name '{pattern}'"
                else:
                    find_cmd += f" ! -path '*/{pattern}/*'"

            # Add directory exclusions
            for dir_pattern in excluded_dirs:
                find_cmd += f" ! -path '*/{dir_pattern}/*'"

            # Add file extension and file name filters
            ext_filter = " -o ".join(f"-name '*{ext}'" for ext in allowed_extensions)
            name_filter = " -o ".join(f"-name '{name}'" for name in allowed_names)
            filters = [f for f in [ext_filter, name_filter] if f]
            combined_filter = " -o ".join(filters)
            find_cmd += f" \\( {combined_filter} \\) | head -{max_files}"  # Limit to configured max files

            self.logger.info("File discovery command: %s", find_cmd)
            result = self.shell.execute(find_cmd)

            if result.exit_code == 0 and result.stdout:
                files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
                self.logger.info(f"Discovered {len(files)} code files")
                self.logger.info("Discovered file sample: %s", files[:5])
                return files
            if result.exit_code == 0:
                self.logger.warning(
                    "File discovery returned no files (command=%s, base_directory=%s)",
                    find_cmd,
                    base_directory,
                )
                return []
            self.logger.warning(
                "File discovery failed (command=%s, exit_code=%s, stdout_len=%s, stderr=%s)",
                find_cmd,
                result.exit_code,
                len(result.stdout or ""),
                result.stderr,
            )
            return []

        except Exception as e:
            self.logger.error(f"Error discovering code files: {e}")
            return []

    async def _analyze_file_batch(self, file_paths: list[str]) -> tuple[list[dict[str, Any]], dict[str, int]]:
        """Analyze a batch of files for semantic content."""
        summaries = []
        total = len(file_paths)
        skipped_unreadable = 0
        skipped_no_summary = 0

        for file_path in file_paths:
            try:
                # Read file content safely
                content = await self._read_file_safely(file_path)
                if not content:
                    skipped_unreadable += 1
                    continue

                # Generate semantic summary
                summary = await self._extract_file_semantic_summary(content, file_path)
                if not summary:
                    skipped_no_summary += 1
                    continue

                # Extract dependencies
                dependencies = self._extract_dependencies(content, file_path)

                # Classify file
                file_type = self._classify_file_type(file_path, content)
                architectural_role = self._classify_architectural_role(file_path, content)

                summaries.append(
                    {
                        "path": file_path,
                        "summary": summary,
                        "dependencies": dependencies,
                        "content_preview": content[:1000],
                        "file_type": file_type,
                        "architectural_role": architectural_role,
                    }
                )

            except Exception as e:
                self.logger.warning(f"Failed to analyze {file_path}: {e}")
                continue

        if total:
            self.logger.info(
                "Batch analysis summary: total=%s summarized=%s skipped_unreadable=%s skipped_no_summary=%s",
                total,
                len(summaries),
                skipped_unreadable,
                skipped_no_summary,
            )
        return summaries, {
            "total": total,
            "summarized": len(summaries),
            "skipped_unreadable": skipped_unreadable,
            "skipped_no_summary": skipped_no_summary,
        }

    def _resolve_path(self, file_path: str) -> str:
        base_directory = getattr(self.shell, "base_directory", os.getcwd())
        if os.path.isabs(file_path):
            return file_path
        return os.path.join(base_directory, file_path)

    def _log_missing_file(self, file_path: str, resolved_path: str) -> None:
        if self._missing_file_log_count >= self._missing_file_log_limit:
            return
        base_directory = getattr(self.shell, "base_directory", os.getcwd())
        self.logger.warning(
            "Semantic file read skipped; file not found (path=%s resolved=%s base_directory=%s)",
            file_path,
            resolved_path,
            base_directory,
        )
        self._missing_file_log_count += 1
        if self._missing_file_log_count == self._missing_file_log_limit:
            self.logger.warning("Further missing file logs suppressed.")

    async def _read_file_safely(self, file_path: str, max_size: int = 100000) -> str:
        """Safely read file content with size limits."""
        try:
            # Check file size first
            resolved_path = self._resolve_path(file_path)
            if os.path.exists(resolved_path):
                file_size = os.path.getsize(resolved_path)
                if file_size > max_size:
                    self.logger.debug("Skipping large file %s (%s bytes)", resolved_path, file_size)
                    return ""
            else:
                self._log_missing_file(file_path, resolved_path)
                return ""

            with open(resolved_path, encoding="utf-8", errors="ignore") as f:
                return f.read(max_size)

        except Exception as e:
            self.logger.debug(f"Could not read {file_path}: {e}")
            return ""

    def _classify_file_type(self, file_path: str, content_preview: str) -> str:
        """Classify file purpose: component, service, model, config, test, etc."""
        path_lower = file_path.lower()
        content_lower = content_preview.lower()

        # Test files
        if "test" in path_lower or "spec" in path_lower or "__test__" in path_lower:
            return "test"

        # Configuration files
        if path_lower.endswith((".json", ".yaml", ".yml", ".ini", ".env", ".config")):
            return "config"

        # Model files
        if "model" in path_lower or "models" in path_lower:
            return "model"
        if "class " in content_lower and ("def __init__" in content_lower or "@dataclass" in content_lower):
            return "model"

        # Component files (UI)
        if "component" in path_lower or "components" in path_lower:
            return "component"
        if "import react" in content_lower or "from react" in content_lower:
            return "component"

        # Service files
        if "service" in path_lower or "services" in path_lower:
            return "service"
        if "api" in path_lower or "client" in path_lower:
            return "service"

        # Controller files
        if "controller" in path_lower or "controllers" in path_lower:
            return "controller"

        # Utility files
        if "util" in path_lower or "utils" in path_lower or "helper" in path_lower:
            return "utility"

        return "general"

    def _classify_architectural_role(self, file_path: str, content_preview: str) -> str:
        """Determine architectural role: data_layer, business_logic, ui_component, etc."""
        content_indicators = {
            "data_layer": ["database", "repository", "model", "schema", "orm", "sql", "query"],
            "business_logic": ["service", "manager", "handler", "processor", "logic"],
            "ui_component": ["component", "view", "template", "render", "jsx", "tsx"],
            "api_layer": ["controller", "router", "endpoint", "api", "route"],
            "configuration": ["config", "settings", "environment", "env"],
            "infrastructure": ["deployment", "docker", "kubernetes", "infrastructure", "deploy"],
            "testing": ["test", "spec", "mock", "fixture"],
            "utilities": ["util", "helper", "tools", "common"],
        }

        content_lower = content_preview.lower()
        path_lower = file_path.lower()

        for role, indicators in content_indicators.items():
            if any(indicator in content_lower or indicator in path_lower for indicator in indicators):
                return role

        return "general"

    def _extract_dependencies(self, content: str, file_path: str) -> list[str]:
        """Extract file dependencies from imports and references."""
        dependencies = []

        try:
            # Python imports
            python_imports = re.findall(r"^(?:from|import)\s+([.\w]+)", content, re.MULTILINE)
            for imp in python_imports:
                if not imp.startswith("."):  # Skip relative imports for now
                    continue
                # Convert relative import to file path approximation
                dep_path = imp.replace(".", "/") + ".py"
                if dep_path != file_path:
                    dependencies.append(dep_path)

            # JavaScript/TypeScript imports
            js_imports = re.findall(r'import.*from [\'"]([.\w/]+)[\'"]', content)
            for imp in js_imports:
                if imp.startswith("./") or imp.startswith("../"):
                    dependencies.append(imp)

            # Remove duplicates
            dependencies = list(set(dependencies))

        except Exception as e:
            self.logger.debug(f"Could not extract dependencies from {file_path}: {e}")

        return dependencies[:10]  # Limit to 10 dependencies

    async def _extract_file_semantic_summary(self, content: str, file_path: str) -> str:
        """Generate a semantic summary of the file's purpose."""
        try:
            # For now, use a simple heuristic-based summary
            # In a full implementation, this could use an LLM call

            if len(content) > 3000:
                content = content[:3000] + "..."

            # Extract key information
            summary_parts = []

            # File type context
            file_ext = Path(file_path).suffix
            if file_ext in [".py", ".js", ".ts"]:
                summary_parts.append(f"{file_ext[1:].upper()} file")

            # Look for class definitions
            class_matches = re.findall(r"class (\w+)", content)
            if class_matches:
                summary_parts.append(f"defines classes: {', '.join(class_matches[:3])}")

            # Look for function definitions
            func_matches = re.findall(r"def (\w+)|function (\w+)", content)
            if func_matches:
                functions = [f[0] or f[1] for f in func_matches if f[0] or f[1]]
                if functions:
                    summary_parts.append(f"implements functions: {', '.join(functions[:3])}")

            # Look for specific patterns
            if "async def" in content or "await " in content:
                summary_parts.append("uses async/await patterns")
            if "import " in content or "from " in content:
                summary_parts.append("imports external dependencies")
            if "@tool" in content or "@dataclass" in content:
                summary_parts.append("uses decorators")

            # Combine summary
            if summary_parts:
                return f"File {file_path}: {', '.join(summary_parts)}"
            else:
                return f"File {file_path}: general purpose file"

        except Exception as e:
            self.logger.debug(f"Could not generate summary for {file_path}: {e}")
            return f"File {file_path}: content analysis unavailable"

    async def _semantic_file_discovery(self, plan_topic: str, context: str) -> list[ArchitecturalFile]:
        """Stage 1: Direct semantic similarity matching."""
        try:
            query = f"Files related to: {plan_topic}. Context: {context}"

            # Search vector index for semantically similar files
            similarity_results = self.file_index.search(query, top_k=20)

            architectural_files = []
            for result in similarity_results:
                metadata = result.metadata

                # Extract summary from the indexed text
                text_parts = result.text.split(": ", 1)
                summary = text_parts[1] if len(text_parts) > 1 else result.text

                architectural_file = ArchitecturalFile(
                    path=metadata["path"],
                    semantic_summary=summary,
                    relevance_score=result.similarity,
                    file_type=metadata.get("file_type", "general"),
                    architectural_role=metadata.get("architectural_role", "general"),
                    dependencies=metadata.get("dependencies", []),
                    key_functions=self._extract_key_functions(metadata.get("preview", "")),
                    modification_complexity=self._estimate_modification_complexity(metadata.get("preview", "")),
                    content_preview=metadata.get("preview", ""),
                )
                architectural_files.append(architectural_file)

            return architectural_files

        except Exception as e:
            self.logger.error(f"Error in semantic file discovery: {e}")
            return []

    async def _dependency_based_discovery(
        self, initial_matches: list[ArchitecturalFile], plan_topic: str
    ) -> list[ArchitecturalFile]:
        """Stage 2: Expand based on dependency relationships."""
        try:
            dependency_candidates = set()

            # Add direct dependencies and reverse dependencies
            for file in initial_matches:
                dependency_candidates.update(file.dependencies)

            # Analyze dependency candidates for relevance
            relevant_dependencies = []
            for dep_path in dependency_candidates:
                if await self._is_dependency_relevant(dep_path, plan_topic):
                    arch_file = await self._analyze_single_file(dep_path)
                    if arch_file:
                        arch_file.relevance_score *= 0.7  # Reduce score as it's indirect
                        relevant_dependencies.append(arch_file)

            return relevant_dependencies

        except Exception as e:
            self.logger.error(f"Error in dependency-based discovery: {e}")
            return []

    async def _architectural_pattern_discovery(self, plan_topic: str, context: str) -> list[ArchitecturalFile]:
        """Stage 3: Pattern-based discovery (controllers, models, configs, etc.)."""
        try:
            pattern_files = []

            # Identify architectural patterns from plan topic
            patterns = self._identify_architectural_patterns(plan_topic, context)

            for pattern in patterns:
                pattern_matches = await self._find_files_matching_pattern(pattern)
                for match_path in pattern_matches:
                    arch_file = await self._analyze_single_file(match_path)
                    if arch_file:
                        arch_file.relevance_score = self._calculate_pattern_relevance_score(
                            pattern, plan_topic, arch_file
                        )
                        pattern_files.append(arch_file)

            return pattern_files

        except Exception as e:
            self.logger.error(f"Error in architectural pattern discovery: {e}")
            return []

    def _extract_key_functions(self, content_preview: str) -> list[str]:
        """Extract key function/class names from content."""
        try:
            functions = []

            # Python functions and classes
            py_matches = re.findall(r"(?:def|class) (\w+)", content_preview)
            functions.extend(py_matches)

            # JavaScript/TypeScript functions
            js_matches = re.findall(r"function (\w+)|const (\w+) =|(\w+)\s*\(.*\)\s*=>", content_preview)
            for match in js_matches:
                func_name = match[0] or match[1] or match[2]
                if func_name:
                    functions.append(func_name)

            return functions[:5]  # Top 5 functions

        except Exception as e:
            self.logger.debug(f"Could not extract key functions: {e}")
            return []

    def _estimate_modification_complexity(self, content_preview: str) -> str:
        """Estimate how complex it would be to modify this file."""
        try:
            # Simple heuristic based on content characteristics
            if len(content_preview) < 500:
                return "low"
            elif len(content_preview) > 2000:
                return "high"

            # Look for complexity indicators
            complexity_indicators = [
                "async def",
                "await ",
                "try:",
                "except:",
                "class ",
                "import ",
                "from ",
                "@",
                "lambda",
                "yield",
            ]

            indicator_count = sum(1 for indicator in complexity_indicators if indicator in content_preview)

            if indicator_count < 3:
                return "low"
            elif indicator_count > 8:
                return "high"
            else:
                return "medium"

        except Exception as e:
            self.logger.debug(f"Could not estimate complexity: {e}")
            return "medium"

    async def _is_dependency_relevant(self, dep_path: str, plan_topic: str) -> bool:
        """Check if a dependency is relevant to the plan topic."""
        try:
            # Simple relevance check based on path and plan topic keywords
            plan_keywords = plan_topic.lower().split()
            dep_lower = dep_path.lower()

            # Check for keyword matches
            return any(keyword in dep_lower for keyword in plan_keywords if len(keyword) > 3)

        except Exception as e:
            self.logger.debug(f"Could not check dependency relevance: {e}")
            return False

    async def _analyze_single_file(self, file_path: str) -> ArchitecturalFile | None:
        """Analyze a single file and return ArchitecturalFile object."""
        try:
            content = await self._read_file_safely(file_path)
            if not content:
                return None

            return ArchitecturalFile(
                path=file_path,
                semantic_summary=await self._extract_file_semantic_summary(content, file_path),
                file_type=self._classify_file_type(file_path, content),
                architectural_role=self._classify_architectural_role(file_path, content),
                dependencies=self._extract_dependencies(content, file_path),
                key_functions=self._extract_key_functions(content),
                modification_complexity=self._estimate_modification_complexity(content),
                content_preview=content[:1000],
            )

        except Exception as e:
            self.logger.debug(f"Could not analyze file {file_path}: {e}")
            return None

    def _identify_architectural_patterns(self, plan_topic: str, context: str) -> list[str]:
        """Identify architectural patterns relevant to the plan topic."""
        patterns = []

        topic_lower = plan_topic.lower()
        context_lower = context.lower()
        combined = f"{topic_lower} {context_lower}"

        # Map keywords to architectural patterns
        pattern_keywords = {
            "api": ["controller", "router", "endpoint"],
            "auth": ["authentication", "authorization", "user", "session"],
            "data": ["model", "repository", "database", "schema"],
            "ui": ["component", "view", "template", "frontend"],
            "config": ["configuration", "settings", "environment"],
            "test": ["test", "spec", "fixture", "mock"],
            "service": ["service", "manager", "handler", "processor"],
        }

        for keyword, pattern_list in pattern_keywords.items():
            if keyword in combined:
                patterns.extend(pattern_list)

        return list(set(patterns))  # Remove duplicates

    async def _find_files_matching_pattern(self, pattern: str) -> list[str]:
        """Find files matching architectural pattern."""
        try:
            # Use simple grep to find files containing pattern (limit to src directory)
            grep_cmd = f"find ./src -name '*.py' -o -name '*.js' -o -name '*.ts' | xargs grep -l '{pattern}' 2>/dev/null | head -10"
            result = self.shell.execute(grep_cmd)

            if result.exit_code == 0 and result.stdout:
                return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
            return []

        except Exception as e:
            self.logger.debug(f"Could not find files matching pattern {pattern}: {e}")
            return []

    def _calculate_pattern_relevance_score(self, pattern: str, plan_topic: str, arch_file: ArchitecturalFile) -> float:
        """Calculate relevance score for pattern-matched files."""
        try:
            base_score = 0.6  # Base score for pattern matches

            # Boost score if pattern appears in file path or summary
            if pattern.lower() in arch_file.path.lower():
                base_score += 0.2
            if pattern.lower() in arch_file.semantic_summary.lower():
                base_score += 0.1

            # Boost if plan topic keywords appear in file
            topic_keywords = plan_topic.lower().split()
            for keyword in topic_keywords:
                if len(keyword) > 3 and keyword in arch_file.path.lower():
                    base_score += 0.1
                    break

            return min(base_score, 1.0)

        except Exception as e:
            self.logger.debug(f"Could not calculate pattern relevance: {e}")
            return 0.5

    def _merge_and_rank_results(
        self,
        semantic_matches: list[ArchitecturalFile],
        dependency_matches: list[ArchitecturalFile],
        architectural_matches: list[ArchitecturalFile],
    ) -> list[ArchitecturalFile]:
        """Combine and rank all discovery results."""
        try:
            # Combine all results
            all_files = {}

            # Add semantic matches (highest priority)
            for file in semantic_matches:
                all_files[file.path] = file

            # Add dependency matches (medium priority)
            for file in dependency_matches:
                if file.path in all_files:
                    # Boost score if found through multiple methods
                    all_files[file.path].relevance_score = max(
                        all_files[file.path].relevance_score, file.relevance_score
                    )
                else:
                    all_files[file.path] = file

            # Add architectural matches (lower priority but still relevant)
            for file in architectural_matches:
                if file.path in all_files:
                    all_files[file.path].relevance_score = max(
                        all_files[file.path].relevance_score, file.relevance_score
                    )
                else:
                    all_files[file.path] = file

            # Sort by relevance score (descending)
            sorted_files = sorted(all_files.values(), key=lambda f: f.relevance_score, reverse=True)

            return sorted_files

        except Exception as e:
            self.logger.error(f"Error merging and ranking results: {e}")
            return []
