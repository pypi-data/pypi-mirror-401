"""
Target File Discovery Command Implementation

This module implements Gemini's "funnel methodology" for intelligent file discovery
in coding agents. It systematically narrows from broad codebase understanding to
specific files that need modification.

The funnel methodology:
1. Initial Context & Keyword Extraction
2. Broad Codebase Exploration & Search
3. Initial Analysis and Triage
4. Deep Dive and Code Comprehension
5. Dependency and Usage Analysis (Following the Trail)
6. Synthesis and Planning
"""

import asyncio
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain_core.tools import tool

from ..intelligent_file_discovery import IntelligentFileDiscovery
from ..openswe.code_tools import CodeTools
from ..shell_runner import ShellRunner

logger = logging.getLogger(__name__)


# Phase 3 Enhancement: Performance optimizations
class CachedRepositoryIndexer:
    """Cache repository index to avoid rebuilding."""

    def __init__(self):
        self._cached_index = None
        self._cache_timestamp = None
        self._cache_validity_seconds = 300  # 5 minutes

    async def get_or_build_index(self, indexer_func):
        """Get cached index or rebuild if needed."""
        if self._is_cache_valid():
            logger.info("📦 Using cached repository index")
            return self._cached_index
        else:
            logger.info("🔨 Rebuilding repository index")
            self._cached_index = await indexer_func()
            self._cache_timestamp = datetime.now()
            return self._cached_index

    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self._cached_index or not self._cache_timestamp:
            return False

        age = (datetime.now() - self._cache_timestamp).total_seconds()
        return age < self._cache_validity_seconds


# Global cache instance (lazy initialization to avoid import side effects)
_repo_index_cache: CachedRepositoryIndexer | None = None


def get_repo_index_cache() -> CachedRepositoryIndexer:
    """Get the repo index cache instance (lazy initialized)."""
    global _repo_index_cache
    if _repo_index_cache is None:
        _repo_index_cache = CachedRepositoryIndexer()
    return _repo_index_cache


def _resolve_workspace_root(workspace_root: str | None) -> str:
    if workspace_root:
        return os.path.abspath(workspace_root)
    from src.workspace_context import get_workspace_root

    stored_root = get_workspace_root()
    if stored_root:
        return os.path.abspath(stored_root)
    return "."


# Phase 1: AST and Repository Indexing imports
try:
    from ..openswe.treesitter_tools import CodeAnalysis, TreeSitterAnalyzer
    from ..repo_indexer import RepoIndexer, SymbolMatch, get_repo_indexer

    AST_AND_INDEXING_AVAILABLE = True
except ImportError as e:
    logger.warning(f"AST and repository indexing tools not available: {e}")
    AST_AND_INDEXING_AVAILABLE = False
    # Set fallback values to avoid NameError
    get_repo_indexer = None
    TreeSitterAnalyzer = None
    CodeAnalysis = None

# Phase 3: Advanced Deep Agents Tools imports
try:
    from ...context_injection.semantic_tagging import SemanticTagger
    from ...deep_agents.tools.bash import advanced_shell_command, execute_bash_command

    DEEP_AGENTS_TOOLS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Deep agents tools not available: {e}")
    DEEP_AGENTS_TOOLS_AVAILABLE = False
    # Set fallback values to avoid NameError
    execute_bash_command = None
    advanced_shell_command = None
    SemanticTagger = None


@tool
async def discover_target_files(
    plan_topic: str,
    research_findings: str | None = None,
    stakeholder_analysis: str | None = None,
    max_files: int = 10,
    workspace_root: str | None = None,
) -> dict[str, Any]:
    """
    Discover target files using intelligent file discovery.

    This replaces the funnel methodology with intelligent semantic analysis
    using the virtual filesystem and LLM-based relevance scoring.

    Args:
        plan_topic: The ticket description or task to implement
        research_findings: Optional research context from research_codebase
        stakeholder_analysis: Optional stakeholder analysis context
        max_files: Maximum number of files to discover (default: 10)
        workspace_root: Optional workspace root for file discovery

    Returns:
        Dictionary containing:
        {
            "discovered_files": List[str],
            "reasoning": str,
            "confidence": float,
            "search_strategy": str,
            "investigation_steps": List[Dict[str, Any]]
        }
    """
    try:
        logger.info(f"🔍 Starting intelligent file discovery for: {plan_topic[:100]}...")

        resolved_root = _resolve_workspace_root(workspace_root)

        # Use intelligent file discovery service
        discovery = IntelligentFileDiscovery(workspace_root=resolved_root)
        result = await discovery.discover_relevant_files(plan_topic=plan_topic, max_files=max_files)

        discovered_files = result.get("discovered_files", [])
        reasoning = result.get("reasoning", "")
        confidence = result.get("confidence", 0.0)

        # Convert to the expected format
        file_paths = [file_info["file_path"] for file_info in discovered_files]

        # Create investigation steps for compatibility
        investigation_steps = [
            {
                "step": 1,
                "name": "Intelligent File Discovery",
                "files_found": len(discovered_files),
                "description": f"Used intelligent semantic analysis to discover {len(discovered_files)} relevant files",
            },
            {
                "step": 2,
                "name": "LLM-based Relevance Scoring",
                "confidence": confidence,
                "description": f"Applied LLM-based relevance scoring with {confidence:.2f} confidence",
            },
        ]

        logger.info(f"✅ Intelligent file discovery completed: {len(file_paths)} files, confidence: {confidence:.2f}")

        return {
            "discovered_files": file_paths,
            "reasoning": reasoning,
            "confidence": confidence,
            "search_strategy": "intelligent_semantic_analysis",
            "investigation_steps": investigation_steps,
        }

    except Exception as e:
        logger.error(f"❌ File discovery failed: {e}")
        return {
            "discovered_files": [],
            "reasoning": f"File discovery failed due to error: {str(e)}",
            "confidence": 0.0,
            "search_strategy": "error_fallback",
            "investigation_steps": [],
            "keywords_used": [],
        }


async def _extract_keywords_and_concepts(
    plan_topic: str,
    research_findings: str | None = None,
    stakeholder_analysis: str | None = None,
    workspace_root: str | None = None,
) -> list[str]:
    """Extract key technical concepts and keywords from the task description with semantic tag resolution."""
    keywords = set()

    # Phase 3 Enhancement: Use semantic tagging to resolve context references
    resolved_topic = plan_topic
    if DEEP_AGENTS_TOOLS_AVAILABLE and SemanticTagger:
        try:
            logger.info("🔍 Using semantic tagging for context resolution")
            resolved_root = _resolve_workspace_root(workspace_root)

            def _resolve_tag_path(path: str) -> str:
                candidate = Path(path)
                if not candidate.is_absolute():
                    candidate = Path(resolved_root) / path
                return candidate.read_text()

            tagger = SemanticTagger(
                file_resolver=_resolve_tag_path, workspace_root=resolved_root, project_root=resolved_root
            )

            # Resolve any @file() or @symbol() references
            resolved_topic = tagger.resolve_tags(plan_topic)
            logger.info(f"✅ Semantic tag resolution completed: {len(resolved_topic)} chars")
        except Exception as e:
            logger.warning(f"Semantic tag resolution failed: {e}")
            resolved_topic = plan_topic

    # Extract from resolved plan topic
    topic_keywords = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", resolved_topic.lower())
    keywords.update([k for k in topic_keywords if len(k) > 2])

    # Extract technical terms (CamelCase, snake_case, etc.)
    technical_patterns = [
        r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b",  # CamelCase
        r"\b[a-z]+(?:_[a-z]+)+\b",  # snake_case
        r"\b[A-Z]+(?:_[A-Z]+)*\b",  # UPPER_CASE
    ]

    for pattern in technical_patterns:
        matches = re.findall(pattern, plan_topic)
        keywords.update([m.lower() for m in matches])

    # Add domain-specific keywords based on context
    if research_findings:
        research_keywords = re.findall(
            r"\b(?:class|function|method|module|component|service|api|database|config|model|view|controller)\w*\b",
            research_findings.lower(),
        )
        keywords.update(research_keywords)

    if stakeholder_analysis:
        analysis_keywords = re.findall(
            r"\b(?:architecture|design|pattern|framework|library|tool|system|integration)\w*\b",
            stakeholder_analysis.lower(),
        )
        keywords.update(analysis_keywords)

    # Filter and prioritize keywords
    filtered_keywords = [
        k
        for k in keywords
        if len(k) > 2
        and k not in {"the", "and", "for", "with", "this", "that", "from", "have", "will", "can", "are", "was", "were"}
    ]

    return sorted(list(set(filtered_keywords)))[:20]  # Limit to top 20 keywords


async def _deep_dive_analysis_parallel(
    candidate_files: list[dict[str, Any]], plan_topic: str, code_tools: "CodeTools"
) -> dict[str, dict[str, Any]]:
    """Perform deep analysis of candidate files using parallel processing for better performance."""
    logger.info(f"🚀 Starting parallel analysis of {len(candidate_files)} files")

    # Create tasks for parallel execution
    tasks = []
    for candidate in candidate_files:
        task = asyncio.create_task(_analyze_single_file(candidate, plan_topic, code_tools))
        tasks.append(task)

    # Execute all tasks in parallel
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    analyzed_files = {}
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.warning(f"Parallel analysis failed for file {i}: {result}")
            analyzed_files[candidate_files[i]["file_path"]] = {
                "relevance_score": 0.0,
                "key_symbols": [],
                "content_preview": "",
                "file_size": 0,
                "analysis_status": "error",
                "error": str(result),
                "ast_analysis": None,
                "analysis_method": "error",
            }
        else:
            analyzed_files.update(result)

    logger.info(f"✅ Parallel analysis completed: {len(analyzed_files)} files analyzed")
    return analyzed_files


async def _analyze_single_file(
    candidate: dict[str, Any], plan_topic: str, code_tools: "CodeTools"
) -> dict[str, dict[str, Any]]:
    """Analyze a single file - used for parallel processing."""
    file_path = candidate["file_path"]
    analyzed_files = {}

    try:
        # Read file content
        read_result = await code_tools.read_file(file_path)

        if read_result.status != "success":
            analyzed_files[file_path] = {
                "relevance_score": 0.0,
                "key_symbols": [],
                "content_preview": "",
                "file_size": 0,
                "analysis_status": "read_failed",
                "ast_analysis": None,
                "analysis_method": "error",
            }
            return analyzed_files

        content = read_result.result
        relevance_score = 0.0
        key_symbols = []
        ast_analysis = None

        # Phase 1 Enhancement: Use AST analysis if available
        if AST_AND_INDEXING_AVAILABLE and TreeSitterAnalyzer and content:
            try:
                logger.info(f"🔬 Performing AST analysis for {file_path}")
                analyzer = TreeSitterAnalyzer()
                ast_analysis = await analyzer.analyze_file(file_path)

                # Calculate relevance based on AST analysis
                relevance_score = await _calculate_ast_relevance(ast_analysis, plan_topic)

                # Extract symbols from AST analysis
                if ast_analysis:
                    import re

                    # Extract class names from text
                    for cls in ast_analysis.classes:
                        class_match = re.search(r"class\s+(\w+)", cls.get("text", ""))
                        if class_match:
                            key_symbols.append(class_match.group(1))

                    # Extract function names from text
                    for func in ast_analysis.functions:
                        func_match = re.search(r"def\s+(\w+)", func.get("text", ""))
                        if func_match:
                            key_symbols.append(func_match.group(1))

                    # Extract variable names from text (if variables exist)
                    if hasattr(ast_analysis, "variables"):
                        for var in ast_analysis.variables:
                            var_match = re.search(r"(\w+)\s*=", var.get("text", ""))
                            if var_match:
                                key_symbols.append(var_match.group(1))

                    key_symbols = [s for s in key_symbols if s]  # Remove empty strings

            except Exception as e:
                logger.warning(f"AST analysis failed for {file_path}: {e}")
                # Fall back to text-based analysis
                ast_analysis = None

        # Fallback: Text-based analysis (if AST not available or failed)
        if not ast_analysis and content:
            logger.info(f"🔍 Using fallback text analysis for {file_path}")

            # Look for class definitions
            class_matches = re.findall(r"class\s+(\w+)", content)
            key_symbols.extend(class_matches)

            # Look for function definitions
            func_matches = re.findall(r"def\s+(\w+)", content)
            key_symbols.extend(func_matches)

            # Look for imports that might be relevant
            import_matches = re.findall(r"from\s+(\S+)\s+import|import\s+(\S+)", content)
            for match in import_matches:
                key_symbols.extend([m for m in match if m])

            # Calculate relevance based on plan topic
            topic_words = set(plan_topic.lower().split())
            content_words = set(content.lower().split())

            # Intersection score
            common_words = topic_words.intersection(content_words)
            relevance_score += len(common_words) * 0.1

            # Boost for architectural keywords
            arch_keywords = ["agent", "graph", "state", "execute", "plan", "config", "mode", "run"]
            for keyword in arch_keywords:
                if keyword in content.lower():
                    relevance_score += 0.2

            # Boost for file size (reasonable files are more likely to be important)
            lines = len(content.split("\n"))
            if 50 < lines < 1000:  # Sweet spot for implementation files
                relevance_score += 0.3
            elif lines > 1000:
                relevance_score += 0.1  # Large files might be important but harder to modify

        analyzed_files[file_path] = {
            "relevance_score": min(relevance_score, 1.0),  # Cap at 1.0
            "key_symbols": key_symbols,
            "content_preview": content[:500] if content else "",
            "file_size": len(content) if content else 0,
            "analysis_status": "success",
            "ast_analysis": ast_analysis,  # NEW: Include AST analysis results
            "analysis_method": "ast" if ast_analysis else "text",  # NEW: Track analysis method
        }

    except Exception as e:
        logger.warning(f"Deep analysis failed for {file_path}: {e}")
        analyzed_files[file_path] = {
            "relevance_score": 0.0,
            "key_symbols": [],
            "content_preview": "",
            "file_size": 0,
            "analysis_status": "error",
            "error": str(e),
            "ast_analysis": None,
            "analysis_method": "error",
        }

    return analyzed_files


def _find_kubernetes_manifests(max_results: int = 20) -> list[str]:
    """Detect Kubernetes manifests by checking for apiVersion/kind fields."""
    manifests = []
    skip_dirs = {".git", "node_modules", "dist", "build", "__pycache__", ".terraform"}
    max_size = 2 * 1024 * 1024

    for ext in ("*.yml", "*.yaml"):
        for path in Path(".").rglob(ext):
            if any(part in skip_dirs for part in path.parts):
                continue
            try:
                if path.stat().st_size > max_size:
                    continue
            except OSError:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if re.search(r"(?m)^\\s*apiVersion\\s*:", content) and re.search(r"(?m)^\\s*kind\\s*:", content):
                manifests.append(str(path))
                if len(manifests) >= max_results:
                    return manifests

    return manifests


async def _broad_codebase_search(
    keywords: list[str], code_tools: "CodeTools", shell_runner: "ShellRunner"
) -> list[dict[str, Any]]:
    """Perform broad codebase search using multiple strategies with AST and repository indexing."""
    search_results = []

    # Strategy 1: Repository Indexer Search (NEW - Phase 1 Enhancement)
    if AST_AND_INDEXING_AVAILABLE and get_repo_indexer:
        try:
            logger.info("🔍 Using repository indexer for symbol-based search")
            indexer = get_repo_indexer(".")
            repo_index = await get_repo_index_cache().get_or_build_index(indexer.build_index)

            # Use indexed search instead of basic grep
            symbol_matches = []
            for keyword in keywords[:10]:  # Limit to avoid too many searches
                try:
                    # Use the correct method name: query_symbols
                    matches = indexer.query_symbols(keyword, kind="symbol")
                    symbol_matches.extend(matches)

                    # Convert symbol matches to search results format
                    for match in matches[:5]:  # Limit matches per keyword
                        search_results.append(
                            {
                                "file_path": match.file_path,
                                "keyword": keyword,
                                "context": match.context,
                                "line_number": match.line_number,
                                "search_type": "symbol_index",
                                "symbol_name": match.symbol_name,
                                "symbol_type": match.symbol_type,
                                "signature": match.signature,
                            }
                        )
                except Exception as e:
                    logger.warning(f"Repository indexer search failed for keyword '{keyword}': {e}")

        except Exception as e:
            logger.warning(f"Repository indexer initialization failed: {e}")

    # Strategy 2: Fallback Grep search (if repository indexer not available)
    if not AST_AND_INDEXING_AVAILABLE or not search_results:
        logger.info("🔍 Using fallback grep search")
        for keyword in keywords[:10]:  # Limit to avoid too many searches
            try:
                # Use shell_runner for grep search since CodeTools doesn't have grep_search
                result = shell_runner.execute(
                    f"grep -r --include='*.py' --include='*.js' --include='*.ts' --include='*.go' --include='*.rs' --include='*.json' --include='*.yaml' --include='*.yml' --include='*.toml' --include='*.sql' --include='*.sol' --include='*.tf' --include='*.tfvars' --include='*.xml' --include='*.html' --include='*.htm' --include='*.css' --include='*.scss' --include='*.sass' --include='*.md' --include='*.sh' --include='*.bash' --include='*.ps1' --include='*.psm1' --include='Dockerfile' --include='Dockerfile.*' --include='*.dockerfile' --include='dockerfile' --include='dockerfile.*' --include='Makefile' --include='makefile' --include='GNUmakefile' --exclude-dir='__pycache__' --exclude-dir='.git' --exclude-dir='node_modules' --exclude-dir='dist' --exclude-dir='build' '{keyword}' . | head -20"
                )

                if result.exit_code == 0 and result.stdout:
                    # Parse grep output
                    lines = result.stdout.strip().split("\n")
                    for line in lines[:5]:  # Limit matches per keyword
                        if ":" in line:
                            parts = line.split(":", 2)
                            if len(parts) >= 2:
                                file_path = parts[0]
                                content = parts[1] if len(parts) > 1 else ""
                                search_results.append(
                                    {
                                        "file_path": file_path,
                                        "keyword": keyword,
                                        "context": content,
                                        "line_number": 0,  # Grep doesn't always show line numbers
                                        "search_type": "keyword_grep",
                                    }
                                )
            except Exception as e:
                logger.warning(f"Grep search failed for keyword '{keyword}': {e}")

    # Strategy 3: File listing with intelligent filtering
    try:
        # Focus on src/ directory and common config locations
        important_dirs = ["src", "config", "configs", "lib", "app", "components", ".github", "contracts", "test"]

        for dir_name in important_dirs:
            if os.path.exists(dir_name):
                result = shell_runner.execute(
                    f"find {dir_name} -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.go' -o -name '*.rs' -o -name '*.json' -o -name '*.yaml' -o -name '*.yml' -o -name '*.toml' -o -name '*.sql' -o -name '*.sol' -o -name '*.tf' -o -name '*.tfvars' -o -name '*.xml' -o -name '*.html' -o -name '*.htm' -o -name '*.css' -o -name '*.scss' -o -name '*.sass' -o -name '*.sh' -o -name '*.bash' -o -name '*.ps1' -o -name '*.psm1' -o -name 'Dockerfile' -o -name 'Dockerfile.*' -o -name '*.dockerfile' -o -name 'dockerfile' -o -name 'dockerfile.*' -o -name 'Makefile' -o -name 'makefile' -o -name 'GNUmakefile' | head -50"
                )
                if result.exit_code == 0 and result.stdout:
                    files = result.stdout.strip().split("\n")
                    for file_path in files:
                        if file_path.strip():
                            search_results.append(
                                {
                                    "file_path": file_path.strip(),
                                    "keyword": "file_structure",
                                    "context": f"File in {dir_name}/ directory",
                                    "line_number": 0,
                                    "search_type": "directory_scan",
                                }
                            )
    except Exception as e:
        logger.warning(f"Directory scanning failed: {e}")

    # Strategy 4: Kubernetes manifest detection
    k8s_keywords = {
        "kubernetes",
        "k8s",
        "manifest",
        "deployment",
        "service",
        "statefulset",
        "daemonset",
        "ingress",
    }
    if {k.lower() for k in keywords} & k8s_keywords:
        for manifest_path in _find_kubernetes_manifests():
            search_results.append(
                {
                    "file_path": manifest_path,
                    "keyword": "kubernetes_manifest",
                    "context": "Detected Kubernetes manifest (apiVersion/kind)",
                    "line_number": 0,
                    "search_type": "kubernetes_manifest",
                }
            )

    # Strategy 5: Solidity config detection
    solidity_keywords = {"solidity", "sol", "foundry", "forge", "hardhat"}
    if {k.lower() for k in keywords} & solidity_keywords:
        for config_name in [
            "foundry.toml",
            "hardhat.config.js",
            "hardhat.config.ts",
            "hardhat.config.cjs",
            "hardhat.config.mjs",
        ]:
            if os.path.exists(config_name):
                search_results.append(
                    {
                        "file_path": config_name,
                        "keyword": "solidity_config",
                        "context": "Detected Solidity framework config",
                        "line_number": 0,
                        "search_type": "solidity_config",
                    }
                )

    return search_results


async def _triage_search_results(
    search_results: list[dict[str, Any]], plan_topic: str, keywords: list[str], max_files: int
) -> list[dict[str, Any]]:
    """Triage and prioritize search results using heuristics."""
    scored_files = {}

    for result in search_results:
        file_path = result["file_path"]
        if not file_path or file_path in scored_files:
            continue

        score = 0.0

        # File naming heuristics
        filename = os.path.basename(file_path).lower()

        # Higher score for files with relevant keywords in name
        for keyword in keywords:
            if keyword in filename:
                score += 2.0

        # Path-based scoring
        path_parts = file_path.lower().split("/")

        # Prefer src/ files over others
        if "src" in path_parts:
            score += 1.0

        # Prefer main application files
        if any(part in path_parts for part in ["main", "app", "core", "agent", "service"]):
            score += 1.5

        # Prefer source files over non-code assets
        if file_path.endswith(
            (
                ".py",
                ".js",
                ".mjs",
                ".cjs",
                ".ts",
                ".tsx",
                ".jsx",
                ".sh",
                ".bash",
                ".ps1",
                ".psm1",
                ".json",
                ".yaml",
                ".yml",
                ".toml",
                ".xml",
                ".html",
                ".htm",
                ".css",
                ".scss",
                ".sass",
                ".go",
                ".rs",
                ".java",
                ".cs",
                ".cpp",
                ".c",
                ".h",
            )
        ):
            score += 1.0
        if filename in {"makefile", "gnumakefile"}:
            score += 1.0

        # Avoid test and documentation files for implementation
        if any(part in path_parts for part in ["test", "tests", "docs", "__pycache__", ".git"]):
            score -= 1.0

        # Frequency bonus - files that appear in multiple searches
        frequency = len([r for r in search_results if r["file_path"] == file_path])
        score += frequency * 0.5

        scored_files[file_path] = {
            "file_path": file_path,
            "score": score,
            "frequency": frequency,
            "context": result.get("context", ""),
        }

    # Sort by score and return top candidates
    sorted_files = sorted(scored_files.values(), key=lambda x: x["score"], reverse=True)
    return sorted_files[: max_files * 2]  # Get more candidates for deep analysis


async def _deep_dive_analysis(
    candidate_files: list[dict[str, Any]], plan_topic: str, code_tools: "CodeTools"
) -> dict[str, dict[str, Any]]:
    """Perform deep analysis of candidate files using AST analysis and semantic understanding."""
    analyzed_files = {}

    for candidate in candidate_files:
        file_path = candidate["file_path"]

        try:
            # Read file content
            read_result = await code_tools.read_file(file_path)

            if read_result.status != "success":
                continue

            content = read_result.result
            relevance_score = 0.0
            key_symbols = []
            ast_analysis = None

            # Phase 1 Enhancement: Use AST analysis if available
            if AST_AND_INDEXING_AVAILABLE and TreeSitterAnalyzer and content:
                try:
                    logger.info(f"🔬 Performing AST analysis for {file_path}")
                    analyzer = TreeSitterAnalyzer()
                    ast_analysis = await analyzer.analyze_file(file_path)

                    # Calculate relevance based on AST analysis
                    relevance_score = await _calculate_ast_relevance(ast_analysis, plan_topic)

                    # Extract symbols from AST analysis
                    if ast_analysis:
                        import re

                        # Extract class names from text
                        for cls in ast_analysis.classes:
                            class_match = re.search(r"class\s+(\w+)", cls.get("text", ""))
                            if class_match:
                                key_symbols.append(class_match.group(1))

                        # Extract function names from text
                        for func in ast_analysis.functions:
                            func_match = re.search(r"def\s+(\w+)", func.get("text", ""))
                            if func_match:
                                key_symbols.append(func_match.group(1))

                        # Extract variable names from text (if variables exist)
                        if hasattr(ast_analysis, "variables"):
                            for var in ast_analysis.variables:
                                var_match = re.search(r"(\w+)\s*=", var.get("text", ""))
                                if var_match:
                                    key_symbols.append(var_match.group(1))

                        key_symbols = [s for s in key_symbols if s]  # Remove empty strings

                except Exception as e:
                    logger.warning(f"AST analysis failed for {file_path}: {e}")
                    # Fall back to text-based analysis
                    ast_analysis = None

            # Fallback: Text-based analysis (if AST not available or failed)
            if not ast_analysis and content:
                logger.info(f"🔍 Using fallback text analysis for {file_path}")

                # Look for class definitions
                class_matches = re.findall(r"class\s+(\w+)", content)
                key_symbols.extend(class_matches)

                # Look for function definitions
                func_matches = re.findall(r"def\s+(\w+)", content)
                key_symbols.extend(func_matches)

                # Look for imports that might be relevant
                import_matches = re.findall(r"from\s+(\S+)\s+import|import\s+(\S+)", content)
                for match in import_matches:
                    key_symbols.extend([m for m in match if m])

                # Calculate relevance based on plan topic
                topic_words = set(plan_topic.lower().split())
                content_words = set(content.lower().split())

                # Intersection score
                common_words = topic_words.intersection(content_words)
                relevance_score += len(common_words) * 0.1

                # Boost for architectural keywords
                arch_keywords = ["agent", "graph", "state", "execute", "plan", "config", "mode", "run"]
                for keyword in arch_keywords:
                    if keyword in content.lower():
                        relevance_score += 0.2

                # Boost for file size (reasonable files are more likely to be important)
                lines = len(content.split("\n"))
                if 50 < lines < 1000:  # Sweet spot for implementation files
                    relevance_score += 0.3
                elif lines > 1000:
                    relevance_score += 0.1  # Large files might be important but harder to modify

            analyzed_files[file_path] = {
                "relevance_score": min(relevance_score, 1.0),  # Cap at 1.0
                "key_symbols": key_symbols,
                "content_preview": content[:500] if content else "",
                "file_size": len(content) if content else 0,
                "analysis_status": "success",
                "ast_analysis": ast_analysis,  # NEW: Include AST analysis results
                "analysis_method": "ast" if ast_analysis else "text",  # NEW: Track analysis method
            }

        except Exception as e:
            logger.warning(f"Deep analysis failed for {file_path}: {e}")
            analyzed_files[file_path] = {
                "relevance_score": 0.0,
                "key_symbols": [],
                "content_preview": "",
                "file_size": 0,
                "analysis_status": "error",
                "error": str(e),
                "ast_analysis": None,
                "analysis_method": "error",
            }

    return analyzed_files


async def _follow_dependency_trails(
    discovered_files: list[str],
    analyzed_files: dict[str, dict[str, Any]],
    code_tools: "CodeTools",
    shell_runner: "ShellRunner",
) -> set[str]:
    """Follow dependency trails using AST-based dependency graph and symbol relationships."""
    related_files = set()

    # Phase 1 Enhancement: Use repository indexer for dependency analysis
    if AST_AND_INDEXING_AVAILABLE and get_repo_indexer:
        try:
            logger.info("🔗 Using repository indexer for dependency analysis")
            indexer = get_repo_indexer(".")

            # Use cached repository index for dependency analysis
            repo_index = await get_repo_index_cache().get_or_build_index(indexer.build_index)

            for file_path in discovered_files:
                if file_path not in analyzed_files:
                    continue

                analysis = analyzed_files[file_path]
                key_symbols = analysis.get("key_symbols", [])

                # Find related files using symbol index
                for symbol in key_symbols[:5]:  # Limit to avoid too many searches
                    try:
                        # Get files that use this symbol from the index
                        if symbol in repo_index.symbol_index:
                            symbol_matches = repo_index.symbol_index[symbol]
                            for match in symbol_matches[:3]:  # Limit matches per symbol
                                usage_file = match.file_path
                                if usage_file and usage_file != file_path and usage_file not in discovered_files:
                                    related_files.add(usage_file)

                    except Exception as e:
                        logger.warning(f"AST dependency search failed for symbol '{symbol}': {e}")

        except Exception as e:
            logger.warning(f"Repository indexer dependency analysis failed: {e}")
            # Fall back to grep-based analysis

    # Phase 3 Enhancement: Use bash tools for system-level analysis
    if DEEP_AGENTS_TOOLS_AVAILABLE and execute_bash_command:
        try:
            logger.info("🔧 Using bash tools for system-level analysis")

            for file_path in discovered_files[:3]:  # Limit to avoid too many git operations
                try:
                    # Find files that import/use symbols from this file using git history
                    git_command = f"git log --follow --name-only --oneline {file_path} | head -20"
                    result = await execute_bash_command.ainvoke({"command": git_command})

                    if result and hasattr(result, "content"):
                        git_output = result.content
                        # Parse git log output to find related files
                        lines = git_output.split("\n")
                        for line in lines:
                            line = line.strip()
                            if (
                                line
                                and not line.startswith("commit")
                                and not line.startswith("Author")
                                and line.endswith(".py")
                            ):
                                if line != file_path and line not in discovered_files:
                                    related_files.add(line)

                    # Find files that import this file
                    import_command = f"grep -r 'from.*{Path(file_path).stem}\\|import.*{Path(file_path).stem}' --include='*.py' . | head -10"
                    import_result = await execute_bash_command.ainvoke({"command": import_command})

                    if import_result and hasattr(import_result, "content"):
                        import_output = import_result.content
                        lines = import_output.split("\n")
                        for line in lines:
                            if ":" in line:
                                import_file = line.split(":")[0]
                                if import_file != file_path and import_file not in discovered_files:
                                    related_files.add(import_file)

                except Exception as e:
                    logger.warning(f"Bash tools analysis failed for {file_path}: {e}")

        except Exception as e:
            logger.warning(f"Bash tools system-level analysis failed: {e}")

    # Fallback: Grep-based dependency analysis (if repository indexer not available)
    if not AST_AND_INDEXING_AVAILABLE or not related_files:
        logger.info("🔍 Using fallback grep-based dependency analysis")

    for file_path in discovered_files:
        if file_path not in analyzed_files:
            continue

        analysis = analyzed_files[file_path]
        key_symbols = analysis.get("key_symbols", [])

        # For each key symbol, find where it's used
        for symbol in key_symbols[:5]:  # Limit to avoid too many searches
            try:
                # Search for usages of this symbol using shell_runner
                grep_result = shell_runner.execute(
                    f"grep -r --include='*.py' --exclude-dir='__pycache__' --exclude-dir='.git' --exclude-dir='tests' '{symbol}' . | head -10"
                )

                if grep_result.exit_code == 0 and grep_result.stdout:
                    lines = grep_result.stdout.strip().split("\n")
                    for line in lines[:3]:  # Limit matches per symbol
                        if ":" in line:
                            parts = line.split(":", 2)
                            if len(parts) >= 2:
                                usage_file = parts[0]
                                context = parts[1].lower() if len(parts) > 1 else ""
                    if usage_file and usage_file != file_path and usage_file not in discovered_files:
                        # Only add if it looks like an important usage
                        if any(keyword in context for keyword in ["import", "class", "def", "from"]):
                            related_files.add(usage_file)

            except Exception as e:
                logger.warning(f"Dependency search failed for symbol '{symbol}': {e}")

    return related_files


# Phase 1 Enhancement: New helper functions for AST and repository indexing


async def _calculate_ast_relevance(analysis: "CodeAnalysis", plan_topic: str) -> float:
    """Calculate relevance score based on AST analysis."""
    if not analysis:
        return 0.0

    relevance_score = 0.0
    topic_words = set(plan_topic.lower().split())

    # Extract names from text field using regex patterns
    import re

    # Score based on class names
    for cls in analysis.classes:
        class_text = cls.get("text", "").lower()
        # Extract class name from "class ClassName(" pattern
        class_match = re.search(r"class\s+(\w+)", class_text)
        if class_match:
            class_name = class_match.group(1)
            if any(word in class_name for word in topic_words):
                relevance_score += 0.3

        # Check class text content
        if any(word in class_text for word in topic_words):
            relevance_score += 0.2

    # Score based on function names
    for func in analysis.functions:
        func_text = func.get("text", "").lower()
        # Extract function name from "def function_name(" pattern
        func_match = re.search(r"def\s+(\w+)", func_text)
        if func_match:
            func_name = func_match.group(1)
            if any(word in func_name for word in topic_words):
                relevance_score += 0.2

        # Check function text content
        if any(word in func_text for word in topic_words):
            relevance_score += 0.1

    # Score based on imports
    for imp in analysis.imports:
        import_text = imp.get("text", "").lower()
        # Extract import name from "from module import" or "import module" patterns
        import_match = re.search(r"(?:from\s+(\w+)|import\s+(\w+))", import_text)
        if import_match:
            import_name = import_match.group(1) or import_match.group(2)
            if any(word in import_name for word in topic_words):
                relevance_score += 0.1

        # Check import text content
        if any(word in import_text for word in topic_words):
            relevance_score += 0.05

    # Boost for architectural patterns
    arch_patterns = ["agent", "graph", "state", "execute", "plan", "config", "mode", "run"]
    for pattern in arch_patterns:
        if pattern in plan_topic.lower():
            # Check if file contains related symbols in any text
            all_texts = (
                [cls.get("text", "") for cls in analysis.classes]
                + [func.get("text", "") for func in analysis.functions]
                + [imp.get("text", "") for imp in analysis.imports]
            )
            if any(pattern in text.lower() for text in all_texts):
                relevance_score += 0.2

    return min(relevance_score, 1.0)  # Cap at 1.0


async def _find_symbol_relationships(symbols: list[str], indexer: "RepoIndexer") -> list[str]:
    """Find related symbols using repository index."""
    related_symbols = []

    try:
        # Get the repository index
        repo_index = await get_repo_index_cache().get_or_build_index(indexer.build_index)

        for symbol in symbols:
            try:
                # Find symbols that are related to this one using query_symbols
                related = indexer.query_symbols(symbol, kind="symbol")
                related_symbols.extend([match.symbol_name for match in related])
            except Exception as e:
                logger.warning(f"Failed to find relationships for symbol '{symbol}': {e}")
    except Exception as e:
        logger.warning(f"Failed to build repository index for symbol relationships: {e}")

    # Remove duplicates and return
    return list(set(related_symbols))


async def _synthesize_final_selection(
    candidate_files: list[str], plan_topic: str, analyzed_files: dict[str, dict[str, Any]], max_files: int
) -> list[str]:
    """Synthesize final file selection based on all analysis."""

    # Score files based on multiple factors
    file_scores = {}

    for file_path in candidate_files:
        score = 0.0

        # Base relevance score from deep analysis
        if file_path in analyzed_files:
            analysis = analyzed_files[file_path]
            score += analysis.get("relevance_score", 0.0) * 10

            # Bonus for files with many symbols (likely to be important)
            symbol_count = len(analysis.get("key_symbols", []))
            score += min(symbol_count * 0.5, 3.0)

        # Path-based final scoring
        if "agent" in file_path.lower():
            score += 2.0
        if "main" in file_path.lower() or "core" in file_path.lower():
            score += 1.5
        if file_path.startswith("src/"):
            score += 1.0

        file_scores[file_path] = score

    # Sort by score and return top files
    sorted_files = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)
    return [file_path for file_path, score in sorted_files[:max_files]]


def _calculate_discovery_confidence(
    investigation_steps: list[dict[str, Any]], final_files: list[str], keywords: list[str]
) -> float:
    """Calculate confidence score for the discovery process."""
    confidence = 0.0

    # Base confidence from having files
    if final_files:
        confidence += 0.3

    # Confidence from investigation completeness
    if len(investigation_steps) >= 6:  # All steps completed
        confidence += 0.2

    # Confidence from keyword coverage
    if len(keywords) >= 5:
        confidence += 0.2

    # Confidence from file count (sweet spot is 3-8 files)
    file_count = len(final_files)
    if 3 <= file_count <= 8:
        confidence += 0.3
    elif 1 <= file_count <= 2:
        confidence += 0.1
    elif file_count > 8:
        confidence += 0.1  # Too many files might indicate poor targeting

    return min(confidence, 1.0)


def _generate_discovery_reasoning(
    investigation_steps: list[dict[str, Any]], final_files: list[str], keywords: list[str], confidence: float
) -> str:
    """Generate detailed reasoning for the file discovery process."""

    reasoning = f"""# File Discovery Analysis

## Investigation Summary
Completed {len(investigation_steps)} investigation steps using the funnel methodology:

"""

    for step in investigation_steps:
        reasoning += f"**Step {step['step']}: {step['name']}**\n"
        reasoning += f"- {step['description']}\n\n"

    reasoning += f"""## Keywords Analyzed
Extracted {len(keywords)} key concepts: {", ".join(keywords[:10])}{"..." if len(keywords) > 10 else ""}

## Final Selection ({len(final_files)} files)
"""

    for i, file_path in enumerate(final_files, 1):
        reasoning += f"{i}. `{file_path}`\n"

    reasoning += f"""
## Confidence Assessment
Discovery confidence: {confidence:.1%}

This confidence is based on:
- Investigation completeness ({len(investigation_steps)}/6 steps)
- Keyword coverage ({len(keywords)} concepts identified)
- File selection quality ({len(final_files)} files targeted)
- Path analysis and relevance scoring

## Next Steps
These files should be analyzed in the planning phase to understand:
1. Current implementation patterns
2. Integration points and dependencies  
3. Specific modification requirements
4. Testing and validation needs
"""

    return reasoning
