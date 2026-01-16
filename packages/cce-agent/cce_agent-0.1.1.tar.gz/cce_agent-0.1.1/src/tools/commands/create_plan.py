"""
Create Plan Command Implementation

This module provides programmatic access to the create_plan command
functionality as a LangChain tool, implementing the actual logic from
.cursor/commands/create_plan.md
"""

import logging
import os
import re
from datetime import datetime
from typing import Any

from langchain_core.tools import tool

from src.config.artifact_root import get_plans_directory, get_research_directory

logger = logging.getLogger(__name__)


def _resolve_workspace_root(workspace_root: str | None) -> str:
    if workspace_root:
        return os.path.abspath(workspace_root)
    from src.workspace_context import get_workspace_root

    stored_root = get_workspace_root()
    if stored_root:
        return os.path.abspath(stored_root)
    return "."


def _truncate_context(text: str, max_length: int = 5000) -> str:
    """
    Truncate context text to prevent bloat while preserving important information.

    Args:
        text: The text to truncate
        max_length: Maximum length in characters

    Returns:
        Truncated text with summary if needed
    """
    if not text:
        return text

    # First, filter out recursive grep patterns that cause bloat
    filtered_text = _filter_recursive_patterns(text)

    if len(filtered_text) <= max_length:
        return filtered_text

    # Try to find a good truncation point (end of sentence or paragraph)
    truncate_at = max_length - 200  # Leave room for summary

    # Look for sentence endings
    for i in range(truncate_at, max(0, truncate_at - 500), -1):
        if filtered_text[i] in ".!?":
            truncate_at = i + 1
            break

    # Look for paragraph breaks
    for i in range(truncate_at, max(0, truncate_at - 200), -1):
        if filtered_text[i : i + 2] == "\n\n":
            truncate_at = i
            break

    truncated = filtered_text[:truncate_at].strip()

    # Add summary if we truncated significantly
    if len(filtered_text) > max_length * 1.5:
        truncated += (
            f"\n\n[CONTEXT TRUNCATED: Original length {len(filtered_text)} chars, showing first {len(truncated)} chars]"
        )

    return truncated


def _filter_recursive_patterns(text: str) -> str:
    """
    Filter out recursive grep patterns that cause context bloat.

    Args:
        text: The text to filter

    Returns:
        Filtered text with recursive patterns removed
    """
    if not text:
        return text

    lines = text.split("\n")
    filtered_lines = []

    for line in lines:
        # Skip lines with any "Found title::" patterns (these are recursive grep artifacts)
        if "Found title::" in line:
            continue

        # Skip lines that are just recursive file path chains
        if re.search(r"\.md:\d+:.*\.md:\d+:.*\.md:\d+:", line):
            continue

        # Skip lines that contain recursive file path patterns
        if re.search(r"\.md:\d+:.*\.md:\d+:", line):
            continue

        filtered_lines.append(line)

    return "\n".join(filtered_lines)


def _format_discovered_files(discovered_files: list[str]) -> str:
    """Format discovered files for inclusion in plan content."""
    if not discovered_files:
        return "No target files identified."

    formatted_files = []
    for i, file_path in enumerate(discovered_files, 1):
        formatted_files.append(f"{i}. `{file_path}`")

    return "\n".join(formatted_files)


@tool
async def create_plan(
    plan_topic: str,
    context: str | None = None,
    discovered_files: list[str] | None = None,
    workspace_root: str | None = None,
) -> dict[str, Any]:
    """Interactive, iterative creation of detailed technical specifications and
    implementation plans based on research findings and requirements.
    This implements the actual create_plan command logic from .cursor/commands/create_plan.md

    Args:
        plan_topic: The specific feature, component, or system to plan
        context: Optional context, constraints, or specific requirements
        discovered_files: Optional list of target files discovered by file discovery
        workspace_root: Optional workspace root for codebase analysis
    """
    logger.debug(
        f"STARTING create_plan: topic='{plan_topic}', context_length={len(context or '')}, discovered_files={len(discovered_files or [])}"
    )

    try:
        # Import here to avoid circular imports
        from ..code_analyzer import CodeAnalyzer
        from ..shell_runner import ShellRunner

        resolved_root = _resolve_workspace_root(workspace_root)

        # Initialize required services
        shell_runner = ShellRunner(resolved_root)
        code_analyzer = CodeAnalyzer(shell_runner)

        # Phase 1: Context Gathering
        github_context = await _analyze_github_issue(plan_topic, shell_runner, context)
        logger.debug("Phase 1: Extracting key findings from rich context")
        # Extract key findings from the rich context instead of using it all
        research_findings = await _extract_key_research_findings(context or "No context provided")
        logger.debug(f"Extracted research findings length: {len(research_findings)}")

        # Phase 2: Research Integration
        logger.debug("Phase 2: Analyzing codebase for planning")
        codebase_analysis = await _analyze_codebase_for_planning(plan_topic, code_analyzer)
        logger.debug(f"Codebase analysis length: {len(codebase_analysis)}")

        # Phase 2.5: Extract Research Findings
        logger.debug("Phase 2.5: Extracting research findings")
        parsed_research = await _extract_research_findings(plan_topic, research_findings)
        logger.debug(
            f"Parsed research keys: {list(parsed_research.keys()) if isinstance(parsed_research, dict) else 'Not dict'}"
        )

        # Phase 3: Plan Design
        logger.debug("Phase 3: Designing plan structure")
        plan_structure = await _design_plan_structure(
            plan_topic,
            context,
            github_context,
            research_findings,
            parsed_research,
            codebase_analysis,
            discovered_files,
        )
        logger.debug(
            f"Plan structure keys: {list(plan_structure.keys()) if isinstance(plan_structure, dict) else 'Not dict'}"
        )
        # Phase 4: Documentation
        plan_document = await _create_plan_document(
            plan_topic, context, github_context, research_findings, codebase_analysis, plan_structure, discovered_files
        )

        # Phase 5: Structure and Return Enhanced Result
        # Handle case where plan_structure is None (topic analysis failed)
        if plan_structure is None:
            logger.warning("⚠️ Plan structure is None, using fallback structure")
            plan_structure = {
                "phases": [],
                "dependencies": [],
                "risks": [],
                "estimated_duration": "Unknown",
                "success_criteria": [],
            }

        result = {
            "markdown_plan": plan_document,
            "structured_phases": _convert_to_pydantic_phases(plan_structure.get("phases", [])),
            "plan_metadata": {
                "topic": plan_topic,
                "context": context,
                "timestamp": datetime.now().isoformat(),
                "dependencies": plan_structure.get("dependencies", []),
                "risks": plan_structure.get("risks", []),
                "estimated_duration": plan_structure.get("estimated_duration", "Unknown"),
                "success_criteria": plan_structure.get("success_criteria", []),
            },
        }

        return result

    except Exception as e:
        logger.error(f"Create plan command failed: {e}")
        error_result = {
            "markdown_plan": f"Plan creation failed for topic '{plan_topic}': {str(e)}",
            "structured_phases": [],
            "plan_metadata": {
                "topic": plan_topic,
                "context": context,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
            },
        }
        return error_result


async def _analyze_github_issue(plan_topic: str, shell_runner, context: str | None = None) -> str:
    """Analyze GitHub issue if referenced in plan topic or provided in context."""
    try:
        # First check if GitHub issue content is provided in context
        if context and ("Ticket Title:" in context or "## Description" in context):
            return f"GitHub Issue Context from provided content:\n{context}"

        # Fallback: Extract issue number or URL from plan topic
        issue_match = re.search(r"#(\d+)", plan_topic)
        url_match = re.search(r"github\.com/([^/]+)/([^/]+)/issues/(\d+)", plan_topic)

        if issue_match:
            issue_number = issue_match.group(1)
            # Try to get repo info from git
            result = shell_runner.execute("git remote get-url origin")
            if result.exit_code == 0:
                repo_url = result.stdout.strip()
                repo_match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
                if repo_match:
                    owner, repo = repo_match.groups()
                    cmd = f"gh issue view {issue_number} --repo {owner}/{repo}"
                    result = shell_runner.execute(cmd)
                    if result.exit_code == 0:
                        return f"GitHub Issue #{issue_number}:\n{result.stdout}"

        elif url_match:
            owner, repo, issue_number = url_match.groups()
            cmd = f"gh issue view {issue_number} --repo {owner}/{repo}"
            result = shell_runner.execute(cmd)
            if result.exit_code == 0:
                return f"GitHub Issue #{issue_number}:\n{result.stdout}"

        return "No GitHub issue referenced"
    except Exception as e:
        logger.warning(f"GitHub issue analysis failed: {e}")
        return "GitHub issue analysis failed"


async def _find_associated_research(plan_topic: str) -> str:
    """Find associated research documents and return only file names."""
    try:
        research_dir = get_research_directory()
        if not research_dir.exists():
            return "No research directory found"

        # Look for research documents with similar topics
        research_files = []
        for file_path in research_dir.glob("*.md"):
            if any(term.lower() in file_path.name.lower() for term in plan_topic.split()):
                research_files.append(file_path)

        if not research_files:
            return "No related research documents found"

        # Sort by modification time (most recent first) and limit to 3 files
        sorted_files = sorted(research_files, key=lambda f: f.stat().st_mtime, reverse=True)
        limited_files = sorted_files[:3]  # Only take the 3 most recent

        # Return only file names, not content
        file_names = [f.name for f in limited_files]
        return f"Related research files found: {', '.join(file_names)}"

    except Exception as e:
        logger.warning(f"Research search failed: {e}")
        return "Research search failed"


async def _analyze_codebase_for_planning(plan_topic: str, code_analyzer) -> str:
    """Enhanced codebase analysis using semantic understanding."""
    try:
        # Import the SemanticCodeAnalyzer
        from ..semantic_file_analyzer import SemanticCodeAnalyzer

        # Create semantic analyzer (reuse shell from existing analyzer)
        semantic_analyzer = SemanticCodeAnalyzer(code_analyzer.shell)

        # Get semantically relevant files
        relevant_files = await semantic_analyzer.discover_architecturally_relevant_files(
            plan_topic=plan_topic, context="implementation planning"
        )

        if not relevant_files:
            # Fallback to naive analysis if semantic analysis fails
            logger.warning("Semantic analysis returned no results, falling back to naive approach")
            return await _naive_codebase_analysis(plan_topic, code_analyzer)

        # Group by architectural role for organized output
        by_role = {}
        for file in relevant_files:
            role = file.architectural_role
            if role not in by_role:
                by_role[role] = []
            by_role[role].append(file)

        # Generate rich analysis report
        analysis_sections = []
        for role, files in by_role.items():
            if not files:
                continue

            role_title = role.title().replace("_", " ")
            files_desc = []

            for file in files[:3]:  # Top 3 per role
                score_str = f"({file.relevance_score:.2f})" if file.relevance_score > 0 else ""
                complexity = f"[{file.modification_complexity}]" if file.modification_complexity != "medium" else ""
                files_desc.append(f"• {file.path} {score_str} {complexity}- {file.semantic_summary}")

            analysis_sections.append(f"**{role_title}**:\n" + "\n".join(files_desc))

        if analysis_sections:
            return "Codebase Analysis Results:\n\n" + "\n\n".join(analysis_sections)
        else:
            return "No architecturally relevant files found for this plan topic."

    except Exception as e:
        logger.warning(f"Semantic codebase analysis failed: {e}")
        # Fallback to naive analysis
        return await _naive_codebase_analysis(plan_topic, code_analyzer)


async def _naive_codebase_analysis(plan_topic: str, code_analyzer) -> str:
    """Fallback naive codebase analysis (original implementation)."""
    try:
        # Get directory structure
        structure = code_analyzer.list_files(".")

        # Look for relevant files based on plan topic
        relevant_files = []
        search_terms = plan_topic.lower().split()

        for line in structure.split("\n"):
            line_lower = line.lower()
            if any(term in line_lower for term in search_terms if len(term) > 3):
                relevant_files.append(line.strip())

        return f"Relevant files found (naive analysis): {', '.join(relevant_files[:10])}"
    except Exception as e:
        logger.warning(f"Naive codebase analysis failed: {e}")
        return "Codebase analysis failed"


async def _extract_key_research_findings(full_context: str) -> str:
    """Extract key research findings from the full context to avoid duplication."""
    logger.debug("Extracting key findings from full context")
    # Look for key sections in the research
    key_sections = []
    lines = full_context.split("\n")

    # Extract file analysis findings
    in_file_analysis = False
    file_count = 0
    for line in lines:
        if "File Analysis" in line or "Intelligent File Analysis" in line:
            in_file_analysis = True
            continue
        elif in_file_analysis and line.strip().startswith("**File:") and file_count < 5:
            # Extract top 5 most relevant files
            key_sections.append(line.strip())
            file_count += 1
        elif in_file_analysis and line.strip().startswith("-") and key_sections:
            # Add the reasoning for the last file
            key_sections.append(line.strip())
        elif "Target Files Discovered:" in line:
            # Extract discovered files list
            if "[" in line:
                files_str = line.split("[")[1].split("]")[0]
                key_sections.append(f"Target Files: {files_str}")
            break

    if key_sections:
        result = "## Key Research Findings\n" + "\n".join(key_sections[:10])  # Top 10 findings
        logger.debug(f"Extracted {len(key_sections)} key findings")
        return result
    else:
        # Fallback: extract first 500 chars
        logger.debug("No structured findings found, using fallback extraction")
        return full_context[:500] + "..." if len(full_context) > 500 else full_context


async def _extract_research_findings(plan_topic: str, research_findings: str) -> dict[str, Any]:
    """Extract detailed research findings including file analysis from research documents."""
    try:
        # Parse research documents to extract file analysis
        file_analyses = []

        # Look for intelligent file analysis patterns in the research
        lines = research_findings.split("\n")
        current_analysis = None

        for line in lines:
            # Look for file analysis sections
            if "File Analysis" in line or "Intelligent File Analysis" in line:
                if current_analysis:
                    file_analyses.append(current_analysis)
                current_analysis = {}

            # Extract location
            if "- **Location**: " in line and current_analysis is not None:
                location_match = re.search(r"`([^`]+)`", line)
                if location_match:
                    current_analysis["file_path"] = location_match.group(1)

            # Extract relevance score
            if "relevance:" in line.lower() or "score:" in line.lower():
                score_match = re.search(r"(\d+\.\d+)", line)
                if score_match:
                    current_analysis["relevance_score"] = float(score_match.group(1))

            # Extract reasoning
            if "- **Significance**: " in line or "Relevance reasoning:" in line:
                reasoning_match = re.search(r":\s*(.+)$", line)
                if reasoning_match:
                    current_analysis["reasoning"] = reasoning_match.group(1).strip()

        # Add the last analysis if exists
        if current_analysis and current_analysis.get("file_path"):
            file_analyses.append(current_analysis)

        # Sort by relevance score
        file_analyses.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        return {
            "file_analyses": file_analyses,
            "total_files_analyzed": len(file_analyses),
            "high_relevance_files": [f for f in file_analyses if f.get("relevance_score", 0) >= 0.8],
            "parsed_successfully": True,
        }

    except Exception as e:
        logger.warning(f"Failed to extract research findings: {e}")
        return {
            "file_analyses": [],
            "total_files_analyzed": 0,
            "high_relevance_files": [],
            "parsed_successfully": False,
            "error": str(e),
        }


async def _design_plan_structure(
    plan_topic: str,
    context: str | None,
    github_context: str,
    research_findings: str,
    parsed_research: dict[str, Any],
    codebase_analysis: str,
    discovered_files: list[str] | None = None,
) -> dict[str, Any]:
    logger.debug(
        f"STARTING _design_plan_structure: topic='{plan_topic}', research_len={len(research_findings)}, parsed_research_keys={list(parsed_research.keys()) if isinstance(parsed_research, dict) else 'Not dict'}"
    )

    """Design the plan structure using intelligent LangGraph-based analysis."""

    try:
        logger.debug("Initializing TopicAnalysisGraph...")
        # Use new intelligent plan generation system
        from ..plan_generation.topic_analyzer import TopicAnalysisGraph

        # Initialize the intelligent topic analyzer
        logger.info(f"🔍 Initializing intelligent topic analyzer for: '{plan_topic}'")
        topic_analyzer = TopicAnalysisGraph()
        logger.info(f"✅ Topic analyzer initialized successfully")

        # Generate intelligent plan structure
        logger.info(f"🚀 Starting intelligent plan generation for: '{plan_topic}'")

        # Combine all context sources for rich input with truncation
        # Truncate research findings to prevent context bloat
        truncated_research = _truncate_context(research_findings, max_length=5000)
        truncated_github = _truncate_context(github_context, max_length=3000)
        truncated_codebase = _truncate_context(codebase_analysis, max_length=3000)

        # Add discovered files and research findings to context
        discovered_files_context = ""
        research_context = ""

        # Use detailed research findings if available
        if parsed_research and parsed_research.get("parsed_successfully"):
            research_context = "\n\n## Detailed Research Findings:\n"
            for analysis in parsed_research.get("file_analyses", [])[:10]:  # Top 10 most relevant
                research_context += (
                    f"- **{analysis['file_path']}** (relevance: {analysis.get('relevance_score', 0):.2f})\n"
                )
                if "reasoning" in analysis:
                    research_context += f"  - {analysis['reasoning'][:200]}...\n"
            research_context += f"\nTotal files analyzed: {parsed_research.get('total_files_analyzed', 0)}"

        # Fallback to basic discovered files if no detailed research
        if not research_context and discovered_files:
            discovered_files_context = f"""

        Target Files Discovered: {", ".join(discovered_files)}
        """

        combined_context = f"""
        Original Context: {context or ""}

        GitHub Issue Details: {truncated_github}

        Research Findings: {truncated_research}{research_context}{discovered_files_context}
        """
        logger.debug("About to call topic_analyzer.analyze_and_structure_plan")
        logger.debug(f"Plan topic: {plan_topic}")
        logger.debug(f"Combined context length: {len(combined_context)} chars")
        logger.debug(f"Codebase analysis length: {len(codebase_analysis)} chars")

        try:
            logger.debug("Building enhanced context...")
            # Include detailed research findings for better plan generation
            enhanced_context = combined_context
            if parsed_research and parsed_research.get("parsed_successfully"):
                enhanced_context += f"\n\n## Research-Based File Analysis:\n"
                enhanced_context += (
                    f"Total files with detailed analysis: {parsed_research.get('total_files_analyzed', 0)}\n"
                )
                enhanced_context += (
                    f"High-relevance files (≥0.8): {len(parsed_research.get('high_relevance_files', []))}\n\n"
                )
                enhanced_context += (
                    "Use this detailed analysis to create specific, file-referenced phases instead of generic phases."
                )

            logger.debug("Calling topic_analyzer.analyze_and_structure_plan...")
            phase_structure = await topic_analyzer.analyze_and_structure_plan(
                plan_topic=plan_topic,
                context=enhanced_context,
                semantic_analysis=codebase_analysis,
                discovered_files=discovered_files,
            )
            logger.debug("topic_analyzer.analyze_and_structure_plan completed successfully")
            logger.debug(f"Phase structure type: {type(phase_structure)}")
            logger.debug(
                f"Phase structure keys: {list(phase_structure.keys()) if isinstance(phase_structure, dict) else 'Not a dict'}"
            )
        except Exception as e:
            logger.debug(
                f"topic_analyzer.analyze_and_structure_plan failed with exception: {type(e).__name__}: {str(e)}"
            )
            import traceback

            logger.debug(f"Exception traceback: {traceback.format_exc()}")
            raise

        logger.info(f"✅ Generated intelligent plan structure for topic: '{plan_topic}'")
        logger.info(
            f"📊 Plan structure keys: {list(phase_structure.keys()) if isinstance(phase_structure, dict) else 'Not a dict'}"
        )
        if isinstance(phase_structure, dict) and "phases" in phase_structure:
            logger.info(f"📋 Number of phases: {len(phase_structure['phases'])}")
            if phase_structure["phases"]:
                logger.info(f"🎯 First phase: {phase_structure['phases'][0].get('name', 'Unknown')}")

        # Ensure we always return a valid structure
        if phase_structure is None:
            logger.debug("Phase structure is None, using fallback")
            phase_structure = {
                "phases": [],
                "dependencies": [],
                "risks": [],
                "estimated_duration": "Unknown",
                "success_criteria": [],
            }

        logger.debug(
            f"_design_plan_structure returning successfully with {len(phase_structure.get('phases', []))} phases"
        )
        return phase_structure

    except Exception as e:
        logger.debug(f"Intelligent plan generation failed: {type(e).__name__}: {str(e)}")
        import traceback

        logger.debug(f"Traceback: {traceback.format_exc()}")
        logger.debug("Falling back to template-based structure")
        # Fallback using template-based generator (no topic-specific hardcoding)
        result = await _create_fallback_plan_structure(plan_topic, context, codebase_analysis)
        logger.debug(f"Fallback completed, returning {len(result.get('phases', []))} phases")
        return result


async def _create_plan_document(
    plan_topic: str,
    context: str | None,
    github_context: str,
    research_findings: str,
    codebase_analysis: str,
    plan_structure: dict[str, Any],
    discovered_files: list[str] | None = None,
) -> str:
    """Create the implementation plan document."""
    try:
        # Create plans directory if it doesn't exist
        plans_dir = get_plans_directory()
        plans_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename with timestamp
        topic_slug = re.sub(r"[^a-zA-Z0-9_-]", "_", plan_topic.lower())[:50]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")  # Include time for uniqueness
        filename = f"{timestamp}_plan_{topic_slug}.md"
        filepath = plans_dir / filename

        # Get current branch
        from ..shell_runner import ShellRunner
        from src.workspace_context import get_workspace_root

        workspace_root = get_workspace_root() or "."
        shell_runner = ShellRunner(workspace_root)
        branch_result = shell_runner.execute("git branch --show-current")
        current_branch = branch_result.stdout.strip() if branch_result.exit_code == 0 else "unknown"

        # Create document content
        content = f"""# Implementation Plan: {plan_topic}

**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Repository**: cce-agent
**Branch**: {current_branch}

## Overview
Implementation plan for {plan_topic} based on research findings and requirements.

## GitHub Issue Context (if applicable)
{_truncate_context(github_context, max_length=2000) if github_context != "No GitHub issue referenced" else "No GitHub issue referenced"}

## Associated Research
{_truncate_context(research_findings, max_length=1000)}

## Current State Analysis
{_truncate_context(codebase_analysis, max_length=2000)}

## Target Files Identified
{_format_discovered_files(discovered_files) if discovered_files else "No specific target files identified yet."}

## Desired End State
- Complete implementation of {plan_topic}
- Full integration with existing systems
- Comprehensive testing and documentation
- Performance requirements met

## Implementation Phases

"""

        # Add phases (limit to prevent excessive content)
        phases = plan_structure.get("phases", [])[:5]  # Limit to 5 phases max
        for i, phase in enumerate(phases, 1):
            phase_name = phase.get("phase_name", phase.get("name", f"Phase {i}"))
            # Check if phase name already starts with "Phase" to avoid duplication
            if phase_name.startswith("Phase"):
                content += f"""### {phase_name}
**Description**: {phase["description"]}

**Tasks**:
"""
            else:
                content += f"""### Phase {i}: {phase_name}
**Description**: {phase["description"]}

**Tasks**:
"""
            tasks = phase.get("tasks", [])[:10]  # Limit to 10 tasks per phase
            for task in tasks:
                content += f"- [ ] {task}\n"
            content += "\n"
            # Optionally include deliverables and acceptance criteria if provided
            deliverables = phase.get("deliverables", [])[:5]  # Limit to 5 deliverables per phase
            if deliverables:
                content += "**Deliverables**:\n"
                for d in deliverables:
                    content += f"- {d}\n"
                content += "\n"
            acceptance = phase.get("acceptance_criteria", [])[:5]  # Limit to 5 criteria per phase
            if acceptance:
                content += "**Acceptance Criteria**:\n"
                for a in acceptance:
                    content += f"- {a}\n"
                content += "\n"

        # Add success criteria (safe access)
        content += """## Success Criteria

### Automated Verification:
"""
        success_criteria = plan_structure.get("success_criteria", [])[:10]  # Limit to 10 criteria
        for criterion in success_criteria:
            content += f"- [ ] {criterion}\n"

        content += f"""
### Manual Verification:
- [ ] Feature works as expected when tested
- [ ] Performance is acceptable under normal load
- [ ] Edge case handling verified manually
- [ ] No regressions in existing functionality
- [ ] All manual verification steps completed

## Dependencies
"""
        # Optionally include dependencies/risks if provided by the intelligent planner
        dependencies = plan_structure.get("dependencies", [])[:5]  # Limit to 5 dependencies
        if dependencies:
            for dep in dependencies:
                content += f"- {dep}\n"
        else:
            content += "- Research findings from codebase analysis\n- Existing system architecture\n- Development environment setup\n"

        risks = plan_structure.get("risks", [])[:5]  # Limit to 5 risks
        if risks:
            content += "\n## Risks\n"
            for risk in risks:
                content += f"- {risk}\n"

        content += """

## Notes
This plan was generated programmatically using the CCE create_plan command.
For detailed planning and iterative refinement, use the full /create_plan command.
"""

        # Write document
        with open(filepath, "w") as f:
            f.write(content)

        return f"Implementation plan created at: {filepath}\n\n{content}"

    except Exception as e:
        logger.error(f"Failed to create plan document: {e}")
        return f"Plan creation completed for '{plan_topic}' but failed to create document: {str(e)}"


async def _create_fallback_plan_structure(
    plan_topic: str, context: str | None, codebase_analysis: str
) -> dict[str, Any]:
    """Create fallback plan structure when intelligent generation fails."""
    try:
        # Use template-based fallback
        from ..plan_generation.plan_templates import PlanTemplateLibrary

        library = PlanTemplateLibrary()

        # Determine domain type from topic
        topic_lower = plan_topic.lower()
        if any(word in topic_lower for word in ["bug", "fix", "error", "issue"]):
            domain_type = "bug_fixing"
        elif any(word in topic_lower for word in ["refactor", "clean", "improve", "optimize"]):
            domain_type = "refactoring"
        elif any(word in topic_lower for word in ["infrastructure", "deploy", "ci", "cd", "pipeline"]):
            domain_type = "infrastructure"
        elif any(word in topic_lower for word in ["performance", "speed", "memory", "optimize"]):
            domain_type = "performance_optimization"
        else:
            domain_type = "feature_development"

        # Get template and customize it
        template = library.get_customized_template(domain_type, "moderate", "medium")

        # Customize with plan topic
        for phase in template["phases"]:
            phase["description"] = phase["description"].replace("feature", plan_topic)
            phase["description"] = phase["description"].replace("system", plan_topic)

        logger.info(f"✅ Created fallback plan structure for topic: '{plan_topic}' using {domain_type} template")
        return template

    except Exception as e:
        logger.warning(f"Fallback plan generation failed: {e}, using basic structure")

        # Ultimate fallback - basic structure
        return {
            "phases": [
                {
                    "name": "Analysis and Design",
                    "description": f"Analyze requirements for {plan_topic}",
                    "tasks": ["Requirement analysis", "Technical design", "Risk assessment"],
                    "deliverables": ["Requirements document", "Technical specification"],
                    "acceptance_criteria": ["Requirements validated", "Design approved"],
                },
                {
                    "name": "Implementation",
                    "description": f"Implement {plan_topic}",
                    "tasks": ["Core implementation", "Integration", "Unit testing"],
                    "deliverables": ["Working implementation", "Test coverage"],
                    "acceptance_criteria": ["Functionality complete", "Tests passing"],
                },
                {
                    "name": "Validation and Deployment",
                    "description": f"Validate and deploy {plan_topic}",
                    "tasks": ["Integration testing", "User acceptance", "Deployment"],
                    "deliverables": ["Validated system", "Deployment documentation"],
                    "acceptance_criteria": ["System validated", "Successfully deployed"],
                },
            ],
            "dependencies": ["Codebase analysis", "Stakeholder review"],
            "risks": ["Technical complexity", "Integration challenges"],
            "estimated_duration": "To be determined based on scope",
            "success_criteria": [
                "All functionality implemented as specified",
                "Tests pass with adequate coverage",
                "Documentation updated and accurate",
                "System validated and deployed successfully",
            ],
        }


def _convert_to_pydantic_phases(phases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Convert phase dictionaries to Pydantic-compatible format for structured output.

    Args:
        phases: List of phase dictionaries from the plan structure

    Returns:
        List of structured phase dictionaries compatible with PlanPhase model
    """
    try:
        structured_phases = []
        for i, phase in enumerate(phases, 1):
            # Extract phase number from name if present, otherwise use index
            phase_number = i
            phase_name = phase.get("name", f"Phase {i}")

            # Remove "Phase X:" prefix if present to avoid duplication
            if phase_name.startswith("Phase ") and ":" in phase_name:
                phase_name = phase_name.split(":", 1)[1].strip()

            # Create structured phase
            structured_phase = {
                "phase_number": phase_number,
                "phase_name": phase_name,
                "description": phase.get("description", ""),
                "tasks": phase.get("tasks", []),
                "deliverables": phase.get("deliverables", []),
                "acceptance_criteria": phase.get("acceptance_criteria", []),
            }

            structured_phases.append(structured_phase)

        logger.info(f"✅ Converted {len(structured_phases)} phases to structured format")
        return structured_phases

    except Exception as e:
        logger.warning(f"Failed to convert phases to structured format: {e}")
        # Fallback: return phases as-is with basic structure
        fallback_phases = []
        for i, phase in enumerate(phases, 1):
            fallback_phase = {
                "phase_number": i,
                "phase_name": phase.get("name", f"Phase {i}"),
                "description": phase.get("description", ""),
                "tasks": phase.get("tasks", []),
                "deliverables": phase.get("deliverables", []),
                "acceptance_criteria": phase.get("acceptance_criteria", []),
            }
            fallback_phases.append(fallback_phase)

        return fallback_phases
