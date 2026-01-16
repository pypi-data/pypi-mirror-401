"""
Intelligent File Discovery Service

This service replaces brittle keyword matching with semantic analysis of file summaries
using the existing virtual filesystem infrastructure. It provides a unified interface
for all planning phase tools to discover relevant files.
"""

import json
import logging
import os
import time
from typing import Any

from pydantic import BaseModel, Field

from ..deep_agents.utils.virtual_filesystem import initialize_virtual_filesystem_from_workspace
from ..token_tracker import TokenTrackingLLM

logger = logging.getLogger(__name__)


class RelevantFile(BaseModel):
    """Pydantic model for a relevant file discovered by LLM analysis."""

    file_path: str = Field(description="Path to the relevant file")
    relevance_score: float = Field(description="Relevance score from 0.0 to 1.0", ge=0.0, le=1.0)
    reasoning: str = Field(description="Explanation of why this file is relevant")


class FileRelevanceResponse(BaseModel):
    """Pydantic model for LLM response about file relevance."""

    relevant_files: list[RelevantFile] = Field(description="List of relevant files with scores and reasoning")


class IntelligentFileDiscovery:
    """
    Intelligent file discovery service that uses virtual filesystem summaries
    and LLM semantic analysis instead of brittle keyword matching.

    This service:
    1. Loads file summaries from the virtual filesystem
    2. Uses LLM to semantically match plan topics against file summaries
    3. Returns ranked list of relevant files with reasoning
    4. Caches virtual filesystem to avoid recomputation
    """

    def __init__(
        self,
        workspace_root: str = ".",
        cache_timeout: int = 300,
        llm_model: str | None = None,
        summary_max_chars: int | None = None,
    ):
        """
        Initialize the intelligent file discovery service.

        Args:
            workspace_root: Root directory to scan for files
            cache_timeout: Cache timeout in seconds (default: 5 minutes)
            llm_model: Optional model override for LLM analysis
            summary_max_chars: Optional override for max summary size before skipping
        """
        self.workspace_root = workspace_root
        self.cache_timeout = cache_timeout
        self.logger = logging.getLogger(__name__)
        self.summary_max_chars = self._resolve_summary_max_chars(summary_max_chars)

        # Cache for virtual filesystem to avoid recomputation
        self._virtual_files_cache: dict[str, str] | None = None
        self._cache_timestamp: float | None = None

        # Initialize LLM for semantic analysis
        model = llm_model or os.getenv("INTELLIGENT_FILE_DISCOVERY_MODEL") or "claude-sonnet-4-20250514"
        self.llm = TokenTrackingLLM(model=model, temperature=0)
        self.logger.info(
            "IntelligentFileDiscovery initialized (workspace_root=%s, cache_timeout=%s, model=%s, summary_max_chars=%s)",
            os.path.abspath(self.workspace_root),
            self.cache_timeout,
            model,
            self.summary_max_chars,
        )

    def _resolve_summary_max_chars(self, summary_max_chars: int | None) -> int:
        if summary_max_chars is not None:
            return summary_max_chars
        try:
            from ..config_loader import get_config

            config = get_config(workspace_root=self.workspace_root)
            return config.file_discovery.summary_max_chars
        except Exception as exc:
            self.logger.debug("Failed to resolve file discovery summary limit from config: %s", exc)
            return 30000

    async def discover_relevant_files(
        self,
        plan_topic: str,
        max_files: int = 10,
        research_findings: str | None = None,
        stakeholder_analysis: str | None = None,
    ) -> dict[str, Any]:
        """
        Discover files relevant to a plan topic using semantic analysis.

        Args:
            plan_topic: The topic or task to find relevant files for
            max_files: Maximum number of files to return
            research_findings: Optional research context to inform discovery
            stakeholder_analysis: Optional stakeholder analysis context

        Returns:
            Dictionary containing:
            - discovered_files: List of relevant files with scores and reasoning
            - reasoning: Overall reasoning for the discovery process
            - confidence: Confidence score for the discovery quality
        """
        try:
            self.logger.info(f"🔍 Starting intelligent file discovery for: {plan_topic[:100]}...")

            # Get virtual filesystem with intelligent summaries
            virtual_files = await self._get_virtual_filesystem()

            # Filter and format file summaries for LLM analysis
            include_tests = self._should_include_tests(plan_topic, research_findings, stakeholder_analysis)
            file_summaries = self._filter_file_summaries(virtual_files, include_tests=include_tests)
            self.logger.info("Test file inclusion: %s", include_tests)
            self.logger.info(
                "Filtered file summaries: %s/%s usable summaries",
                len(file_summaries),
                len(virtual_files),
            )

            if not file_summaries:
                self.logger.warning(
                    "No usable file summaries after filtering (workspace_root=%s, total_files=%s)",
                    os.path.abspath(self.workspace_root),
                    len(virtual_files),
                )
                return {
                    "discovered_files": [],
                    "reasoning": "No source files found in the workspace",
                    "confidence": 0.0,
                }

            # Use LLM to semantically analyze file relevance
            relevant_files, analysis_error = await self._analyze_file_relevance(
                plan_topic, file_summaries, max_files, research_findings, stakeholder_analysis
            )

            # If there was an analysis error, return error response
            if analysis_error:
                return {
                    "discovered_files": [],
                    "reasoning": f"File discovery failed due to LLM analysis error: {analysis_error}",
                    "confidence": 0.0,
                }

            # Calculate confidence based on results
            confidence = self._calculate_confidence(relevant_files, plan_topic)

            # Generate reasoning
            reasoning = self._generate_discovery_reasoning(relevant_files, plan_topic, len(file_summaries))

            self.logger.info(f"✅ File discovery completed: {len(relevant_files)} files, confidence: {confidence:.2f}")

            return {
                "discovered_files": [
                    {"file_path": f.file_path, "relevance_score": f.relevance_score, "reasoning": f.reasoning}
                    for f in relevant_files
                ],
                "reasoning": reasoning,
                "confidence": confidence,
            }

        except Exception as e:
            self.logger.error(f"❌ File discovery failed: {e}")
            return {
                "discovered_files": [],
                "reasoning": f"File discovery failed due to error: {str(e)}",
                "confidence": 0.0,
            }

    async def _get_virtual_filesystem(self) -> dict[str, str]:
        """Get virtual filesystem with caching."""
        current_time = time.time()

        # Check if cache is valid
        if (
            self._virtual_files_cache is not None
            and self._cache_timestamp is not None
            and current_time - self._cache_timestamp < self.cache_timeout
        ):
            cache_age = current_time - self._cache_timestamp
            self.logger.info("📦 Using cached virtual filesystem (age=%.1fs)", cache_age)
            return self._virtual_files_cache

        # Initialize virtual filesystem with intelligent summaries
        self.logger.info("🔨 Initializing virtual filesystem with intelligent summaries")
        include_patterns = [
            "**/*.py",
            "**/*.js",
            "**/*.jsx",
            "**/*.ts",
            "**/*.tsx",
            "**/*.json",
            "**/*.yaml",
            "**/*.yml",
            "**/*.md",
            "**/*.txt",
            "**/*.sh",
            "**/*.css",
            "**/*.html",
            "config/*",
        ]
        self.logger.info(
            "Virtual filesystem scan (workspace_root=%s, load_mode=summary, include_patterns=%s)",
            os.path.abspath(self.workspace_root),
            include_patterns,
        )
        virtual_files = initialize_virtual_filesystem_from_workspace(
            workspace_root=self.workspace_root,
            include_patterns=include_patterns,
            load_mode="summary",  # Use intelligent summaries
        )

        # Cache the result
        self._virtual_files_cache = virtual_files
        self._cache_timestamp = current_time

        has_cache = "__full_content_cache__" in virtual_files
        self.logger.info(
            "✅ Virtual filesystem initialized with %s entries (full_content_cache=%s)",
            len(virtual_files),
            has_cache,
        )
        return virtual_files

    def _filter_file_summaries(self, virtual_files: dict[str, str], include_tests: bool = False) -> dict[str, str]:
        """
        Filter and format file summaries for LLM analysis.

        Args:
            virtual_files: Raw virtual filesystem data

        Returns:
            Filtered dictionary of file paths to summaries
        """
        filtered = {}
        total = len(virtual_files)
        skipped_cache = 0
        skipped_test = 0
        skipped_empty = 0
        skipped_large = 0

        for file_path, content in virtual_files.items():
            # Skip special cache keys
            if file_path == "__full_content_cache__":
                skipped_cache += 1
                continue

            # Skip test files by default (they're rarely relevant for implementation planning)
            if not include_tests and self._is_test_file(file_path):
                skipped_test += 1
                continue

            # Skip empty content
            if not content or not content.strip():
                skipped_empty += 1
                continue

            # Skip very large summaries (likely full content accidentally)
            if len(content) > self.summary_max_chars:
                skipped_large += 1
                self.logger.warning(
                    "Skipping %s: summary too large (%s chars, limit=%s)", file_path, len(content), self.summary_max_chars
                )
                continue

            filtered[file_path] = content

        self.logger.info(
            "Summary filter stats: total=%s kept=%s skipped_cache=%s skipped_test=%s skipped_empty=%s skipped_large=%s",
            total,
            len(filtered),
            skipped_cache,
            skipped_test,
            skipped_empty,
            skipped_large,
        )
        if not filtered:
            self.logger.warning(
                "Summary filter produced zero usable files (total=%s, skipped_cache=%s, skipped_test=%s, skipped_empty=%s, skipped_large=%s)",
                total,
                skipped_cache,
                skipped_test,
                skipped_empty,
                skipped_large,
            )
        return filtered

    def _is_test_file(self, file_path: str) -> bool:
        """Check if a file is a test file."""
        path_lower = file_path.lower()
        return (
            path_lower.startswith("tests/")
            or path_lower.startswith("test/")
            or "/tests/" in path_lower
            or "/test/" in path_lower
            or path_lower.startswith("test_")
            or path_lower.endswith("_test.py")
            or path_lower.endswith(".test.py")
            or "spec.py" in path_lower
        )

    def _should_include_tests(
        self,
        plan_topic: str,
        research_findings: str | None = None,
        stakeholder_analysis: str | None = None,
    ) -> bool:
        """Heuristic to include test files when the task implies validation."""
        haystack = " ".join(filter(None, [plan_topic, research_findings, stakeholder_analysis])).lower()
        return any(
            keyword in haystack
            for keyword in (
                "test",
                "tests",
                "testing",
                "unit",
                "integration",
                "e2e",
                "verify",
                "validation",
                "rss",
            )
        )

    def _rank_file_summaries(
        self,
        plan_topic: str,
        file_summaries: dict[str, str],
        max_candidates: int = 200,
    ) -> list[tuple[str, str]]:
        """Rank file summaries by simple keyword relevance to reduce prompt size."""
        keywords = [word for word in plan_topic.lower().split() if len(word) > 3]
        scored = []
        for path, summary in file_summaries.items():
            path_lower = path.lower()
            summary_lower = summary.lower()
            score = 0
            for keyword in keywords:
                if keyword in path_lower:
                    score += 3
                if keyword in summary_lower:
                    score += 1
            scored.append((score, path, summary))

        scored.sort(key=lambda item: (-item[0], item[1]))
        if max_candidates and len(scored) > max_candidates:
            scored = scored[:max_candidates]
        return [(path, summary) for _, path, summary in scored]

    async def _analyze_file_relevance(
        self,
        plan_topic: str,
        file_summaries: dict[str, str],
        max_files: int,
        research_findings: str | None = None,
        stakeholder_analysis: str | None = None,
    ) -> tuple[list[RelevantFile], str | None]:
        """
        Use LLM to analyze file relevance to the plan topic.

        Args:
            plan_topic: The topic to find relevant files for
            file_summaries: Dictionary of file paths to summaries
            max_files: Maximum number of files to return
            research_findings: Optional research context
            stakeholder_analysis: Optional stakeholder context

        Returns:
            Tuple of (List of relevant files sorted by relevance score, Optional error message)
        """
        # Create structured LLM for consistent output
        structured_llm = self.llm.with_structured_output(FileRelevanceResponse)

        # Build context for LLM
        context_parts = [f"Plan Topic: {plan_topic}"]
        if research_findings:
            context_parts.append(f"Research Findings: {research_findings[:1000]}")
        if stakeholder_analysis:
            context_parts.append(f"Stakeholder Analysis: {stakeholder_analysis[:1000]}")

        context = "\n\n".join(context_parts)

        # Format file summaries for analysis with size limits
        ranked_files = self._rank_file_summaries(plan_topic, file_summaries, max_candidates=200)
        max_total_chars = 120_000
        entries = []
        total_chars = 0
        for file_path, summary in ranked_files:
            entry = f"FILE: {file_path}\n{summary[:300]}..."
            projected = total_chars + len(entry)
            if projected > max_total_chars:
                break
            entries.append(entry)
            total_chars = projected

        file_summaries_text = "\n\n".join(entries)
        summary_lengths = [len(summary) for summary in file_summaries.values()]
        if summary_lengths:
            self.logger.info(
                "LLM relevance input: files=%s max_files=%s total_summary_chars=%s avg_summary_chars=%.1f",
                len(entries),
                max_files,
                total_chars,
                (total_chars / len(entries)) if entries else 0.0,
            )

        # Create prompt for semantic analysis
        prompt = f"""You are an expert code analyst. Analyze the provided file summaries to identify which files are most relevant for implementing the given plan topic.

{context}

FILE SUMMARIES:
{file_summaries_text}

INSTRUCTIONS:
1. Analyze each file's purpose and content based on its summary
2. Score relevance from 0.0 (not relevant) to 1.0 (highly relevant) for the plan topic
3. Provide clear reasoning for each relevance score
4. Focus on files that would need modification or are architecturally important
5. Return up to {max_files} most relevant files
6. Sort results by relevance score (highest first)

RELEVANCE CRITERIA:
- 0.9-1.0: Directly implements the feature or needs major changes
- 0.7-0.8: Important architectural component that needs integration
- 0.5-0.6: Supporting component that may need minor changes
- 0.3-0.4: Related but unlikely to need changes
- 0.0-0.2: Not relevant to the plan topic

Return only files with relevance score >= 0.3."""

        try:
            response = await structured_llm.ainvoke([{"role": "user", "content": prompt}])

            # Handle both Pydantic objects and dictionaries (for testing)
            if hasattr(response, "relevant_files"):
                relevant_files_data = response.relevant_files
            elif isinstance(response, dict) and "relevant_files" in response:
                relevant_files_data = response["relevant_files"]
            elif isinstance(response, str):
                try:
                    parsed = json.loads(response)
                except json.JSONDecodeError:
                    parsed = None
                if isinstance(parsed, dict) and "relevant_files" in parsed:
                    relevant_files_data = parsed["relevant_files"]
                else:
                    self.logger.error(f"Unexpected response format: {type(response)}")
                    return []
            else:
                self.logger.error(f"Unexpected response format: {type(response)}")
                return []

            if isinstance(relevant_files_data, str):
                try:
                    relevant_files_data = json.loads(relevant_files_data)
                except json.JSONDecodeError:
                    self.logger.error("Failed to parse relevant_files payload from string response")
                    return []

            # Convert to RelevantFile objects if needed
            relevant_files = []
            for file_data in relevant_files_data:
                if isinstance(file_data, RelevantFile):
                    relevant_files.append(file_data)
                elif isinstance(file_data, dict):
                    relevant_files.append(
                        RelevantFile(
                            file_path=file_data["file_path"],
                            relevance_score=file_data["relevance_score"],
                            reasoning=file_data["reasoning"],
                        )
                    )

            # Sort by relevance score and limit results
            relevant_files = sorted(relevant_files, key=lambda f: f.relevance_score, reverse=True)[:max_files]

            # Filter out files that don't exist in our summaries (hallucination protection)
            normalized_map = self._build_normalized_path_map(file_summaries)
            valid_files: list[RelevantFile] = []
            hallucinated_count = 0
            for item in relevant_files:
                resolved = self._resolve_suggested_path(item.file_path, file_summaries, normalized_map)
                if resolved is None:
                    hallucinated_count += 1
                    continue
                if resolved != item.file_path:
                    item = RelevantFile(
                        file_path=resolved,
                        relevance_score=item.relevance_score,
                        reasoning=item.reasoning,
                    )
                valid_files.append(item)

            if hallucinated_count > 0:
                self.logger.warning(f"Filtered out {hallucinated_count} hallucinated files")

            # Fail fast if ALL suggested files were hallucinations
            if len(relevant_files) > 0 and len(valid_files) == 0:
                error_msg = f"All {len(relevant_files)} LLM-suggested files were hallucinated. No valid files found."
                self.logger.error(error_msg)
                return [], error_msg

            return valid_files, None

        except Exception as e:
            self.logger.error(f"LLM analysis failed: {e}")
            return [], str(e)

    def _normalize_path(self, path: str) -> str:
        normalized = path.strip().replace("\\", "/")
        if normalized.startswith("./"):
            normalized = normalized[2:]
        if normalized.startswith("/"):
            normalized = normalized.lstrip("/")
        return normalized

    def _build_normalized_path_map(self, file_summaries: dict[str, str]) -> dict[str, str]:
        normalized_map: dict[str, str] = {}
        for key in file_summaries.keys():
            normalized_key = self._normalize_path(key)
            if normalized_key not in normalized_map:
                normalized_map[normalized_key] = key
        return normalized_map

    def _resolve_suggested_path(
        self,
        suggested_path: str,
        file_summaries: dict[str, str],
        normalized_map: dict[str, str],
    ) -> str | None:
        if not suggested_path:
            return None
        if suggested_path in file_summaries:
            return suggested_path
        normalized = self._normalize_path(suggested_path)
        if normalized in file_summaries:
            return normalized
        mapped = normalized_map.get(normalized)
        if mapped:
            return mapped
        suffix_matches = [key for key in file_summaries if key.endswith(normalized)]
        if len(suffix_matches) == 1:
            return suffix_matches[0]
        return None

    def _calculate_confidence(self, relevant_files, plan_topic: str) -> float:
        """
        Calculate confidence score for the discovery results.

        Args:
            relevant_files: List of discovered relevant files (RelevantFile objects or dicts)
            plan_topic: The original plan topic

        Returns:
            Confidence score from 0.0 to 1.0
        """
        if not relevant_files:
            return 0.0

        # Base confidence from having results
        confidence = 0.3

        # Helper function to get relevance score from either object type
        def get_score(f):
            if hasattr(f, "relevance_score"):
                return f.relevance_score
            elif isinstance(f, dict):
                return f.get("relevance_score", 0.0)
            else:
                return 0.0

        # Boost confidence based on top relevance scores
        top_scores = [get_score(f) for f in relevant_files[:3]]
        avg_top_score = sum(top_scores) / len(top_scores) if top_scores else 0
        confidence += avg_top_score * 0.4

        # Boost confidence if we have multiple high-relevance files
        high_relevance_count = sum(1 for f in relevant_files if get_score(f) >= 0.7)
        if high_relevance_count >= 2:
            confidence += 0.2
        elif high_relevance_count >= 1:
            confidence += 0.1

        # Boost confidence based on topic specificity (longer topics tend to be more specific)
        topic_words = len(plan_topic.split())
        if topic_words >= 5:
            confidence += 0.1
        elif topic_words >= 3:
            confidence += 0.05

        return min(confidence, 1.0)

    def _generate_discovery_reasoning(
        self, relevant_files: list[RelevantFile], plan_topic: str, total_files_analyzed: int
    ) -> str:
        """
        Generate human-readable reasoning for the discovery results.

        Args:
            relevant_files: List of discovered relevant files
            plan_topic: The original plan topic
            total_files_analyzed: Total number of files that were analyzed

        Returns:
            Reasoning text explaining the discovery process and results
        """
        if not relevant_files:
            return f"""Analyzed {total_files_analyzed} files using intelligent summaries from the virtual filesystem, but found no files with sufficient relevance to '{plan_topic}'. This could indicate:
1. The topic requires new files to be created
2. The topic is very specific and existing files don't match
3. The codebase doesn't currently implement this functionality"""

        reasoning = f"""Intelligent File Discovery Analysis:

Analyzed {total_files_analyzed} files using semantic analysis of intelligent file summaries (not brittle keyword matching).

Found {len(relevant_files)} relevant files for '{plan_topic}':

"""

        for i, file in enumerate(relevant_files, 1):
            relevance_desc = (
                "Highly relevant"
                if file.relevance_score >= 0.8
                else "Moderately relevant"
                if file.relevance_score >= 0.6
                else "Potentially relevant"
            )

            reasoning += (
                f"{i}. {file.file_path} ({file.relevance_score:.2f}) - {relevance_desc}\n   {file.reasoning}\n\n"
            )

        reasoning += """This analysis used the existing virtual filesystem with intelligent file summaries instead of brittle keyword matching, providing more accurate semantic understanding of file purposes and relevance."""

        return reasoning


# Convenience functions for backward compatibility with existing planning tools


async def discover_files_for_topic(
    plan_topic: str, max_files: int = 10, research_findings: str | None = None, stakeholder_analysis: str | None = None
) -> list[str]:
    """
    Convenience function that returns just the file paths for backward compatibility.

    Args:
        plan_topic: The topic to find relevant files for
        max_files: Maximum number of files to return
        research_findings: Optional research context
        stakeholder_analysis: Optional stakeholder context

    Returns:
        List of file paths sorted by relevance
    """
    discovery = IntelligentFileDiscovery()
    result = await discovery.discover_relevant_files(plan_topic, max_files, research_findings, stakeholder_analysis)

    return [f["file_path"] for f in result["discovered_files"]]


async def get_file_discovery_reasoning(
    plan_topic: str, max_files: int = 10, research_findings: str | None = None, stakeholder_analysis: str | None = None
) -> str:
    """
    Convenience function that returns the discovery reasoning.

    Args:
        plan_topic: The topic to find relevant files for
        max_files: Maximum number of files to return
        research_findings: Optional research context
        stakeholder_analysis: Optional stakeholder context

    Returns:
        Reasoning text explaining the discovery process
    """
    discovery = IntelligentFileDiscovery()
    result = await discovery.discover_relevant_files(plan_topic, max_files, research_findings, stakeholder_analysis)

    return result["reasoning"]
