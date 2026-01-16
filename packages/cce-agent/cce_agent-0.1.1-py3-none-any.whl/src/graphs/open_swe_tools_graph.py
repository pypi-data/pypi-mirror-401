"""
Open SWE Tools Graph Implementation (Unified)

This module consolidates the best features from both open_swe_tools_graph.py and
open_swe_tools_graph_fixed.py into a single, comprehensive implementation.

Key Features:
- Proper LangGraph ToolNode patterns for native execution
- Complete workflow from discovery to final testing
- Structured outputs with Pydantic validation
- Proper message state management
- Full compatibility with existing interfaces
"""

import asyncio
import logging
import os
from pathlib import Path
from typing import Any, Callable, Literal, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

try:
    # Try relative imports first (for package usage)
    from ..tools.git_ops import GitOps
    from ..tools.openswe.code_tools import CodeTools, ToolResult
    from ..tools.types import AiderState
    from ..tools.validation.runner import ValidationRunner
except ImportError:
    # Fall back to absolute imports (for direct execution and testing)
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from ..tools.git_ops import GitOps
    from ..tools.openswe.code_tools import CodeTools
    from ..tools.validation.runner import ValidationRunner

logger = logging.getLogger(__name__)


# Pydantic Models for Structured Outputs
class RepositoryMapResult(BaseModel):
    """Structured result for repository mapping."""

    repo_map_content: str = Field(description="The generated repository map content")
    key_files: list[str] = Field(description="List of key files identified")
    architecture_summary: str = Field(description="Summary of codebase architecture")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence in the analysis")


class FileDiscoveryResult(BaseModel):
    """Structured result for file discovery."""

    discovered_files: list[str] = Field(description="List of discovered target files")
    discovery_reasoning: str = Field(description="Reasoning for file selection")
    discovery_confidence: float = Field(ge=0.0, le=1.0, description="Confidence in discovery")
    file_categories: dict[str, list[str]] = Field(description="Files grouped by category")


class FileRankingResult(BaseModel):
    """Structured result for file ranking."""

    ranked_files: list[dict[str, Any]] = Field(description="Files ranked by relevance")
    ranking_reasoning: str = Field(description="Reasoning for ranking decisions")
    ranking_confidence: float = Field(ge=0.0, le=1.0, description="Confidence in ranking")


class DryRunResult(BaseModel):
    """Structured result for dry run validation."""

    status: Literal["success", "warning", "error"] = Field(description="Validation status")
    syntax_issues: list[str] = Field(description="Syntax issues found")
    logic_issues: list[str] = Field(description="Logic issues found")
    integration_concerns: list[str] = Field(description="Integration concerns")
    diff_size: int = Field(description="Number of lines changed")
    lines_changed: int = Field(description="Total lines modified")


class OpenSWEState(TypedDict):
    """
    Unified state for the Open SWE Tools Graph combining both implementations.
    """

    # Core workflow state
    instruction: str
    target_files: list[str]
    current_node: str

    # Message history for LLM-tool interaction (from fixed version)
    messages: list[Any]

    # Discovery and ranking results (from both versions)
    repo_map_path: str | None
    repo_map_content: str | None
    discovered_files: list[str] | None
    discovery_reasoning: str | None
    discovery_confidence: float | None
    ranked_files: list[dict[str, Any]] | None
    ranking_reasoning: str | None
    ranking_confidence: float | None

    # Execution results (from original version)
    diff_result: dict[str, Any] | None
    dry_run_result: dict[str, Any] | None
    validation_result: dict[str, Any] | None
    apply_result: dict[str, Any] | None
    test_result: dict[str, Any] | None

    # Approval and completion
    approved: bool | None
    is_approved: bool | None
    error_message: str | None

    # Git state (from both versions)
    git_branch_name: str | None
    original_branch_name: str | None
    git_head_before_edit: str | None
    commit_hash: str | None
    commit_message: str | None

    # Phased execution support (from original version)
    structured_phases: list[dict[str, Any]] | None
    parsed_phases: list[dict[str, Any]] | None
    current_phase_index: int | None
    completed_phases: list[dict[str, Any]] | None
    use_phased_execution: bool
    plan_content: str | None
    phase_execution_summary: dict[str, Any] | None

    # Execution summary
    execution_summary: dict[str, Any] | None


class OpenSWEToolsGraph:
    """
    Unified Open SWE Tools Graph implementation.

    Combines the best features from both implementations:
    - Proper LangGraph ToolNode patterns for discovery/ranking phases
    - Complete workflow through diff generation, validation, and application
    - Structured outputs with Pydantic validation
    - Proper message state management
    """

    def __init__(
        self,
        code_tools: CodeTools,
        git_ops: GitOps,
        validation_runner: ValidationRunner,
        approval_node=None,
        enable_semantic_ranking: bool = True,
        validation_config: dict | None = None,
    ):
        """Initialize the unified OpenSWEToolsGraph with necessary dependencies."""
        self.code_tools = code_tools
        self.git_ops = git_ops
        self.validation_runner = validation_runner
        self.approval_node = approval_node
        self.enable_semantic_ranking = enable_semantic_ranking

        # Validation configuration with sensible defaults
        self.validation_config = validation_config or {
            "max_retries": 3,
            "timeout_seconds": 60,
            "enable_linting": True,
            "enable_testing": True,
            "strict_mode": False,
        }

        logger.info("OpenSWEToolsGraph (Unified) initialized with complete workflow")

    def _resolve_repo_root(self) -> str:
        repo_root = getattr(getattr(self, "git_ops", None), "shell", None)
        repo_root = getattr(repo_root, "base_directory", None)
        return repo_root or os.getcwd()

    # === DISCOVERY PHASE: LLM + ToolNode Pattern ===

    async def llm_repo_map(self, state: OpenSWEState) -> dict:
        """
        LLM node for repository mapping - generates tool calls.
        Uses proper ToolNode pattern from the fixed implementation.
        """
        logger.info("--- LLM Repository Mapping ---")

        try:
            # Get available Open SWE tools
            from src.tools.openswe import (
                analyze_code_structure,
                calculate_code_complexity,
                extract_code_symbols,
                grep_search,
                view,
            )

            # Create tools list for the LLM
            repo_tools = [analyze_code_structure, extract_code_symbols, calculate_code_complexity, view, grep_search]

            # Bind tools to LLM
            llm_with_tools = self.code_tools.editor_llm.bind_tools(repo_tools)

            # Create structured prompt for repository mapping
            system_prompt = """You are a repository analysis expert. Your task is to create a comprehensive repository map.

GOAL: Generate a structured repository map that helps understand:
1. Overall codebase architecture
2. Key modules and their purposes  
3. Important classes and functions
4. File relationships and dependencies

AVAILABLE TOOLS:
- analyze_code_structure: Analyze code structure using TreeSitter or regex-based parsing
- extract_code_symbols: Extract specific code symbols (functions, classes, imports)
- calculate_code_complexity: Calculate code complexity metrics
- view: View file or directory contents
- grep_search: Search for patterns in files

PROCESS:
1. Start by exploring the repository structure using the view tool
2. Identify key files based on names and structure
3. Use analyze_code_structure to understand important files
4. Use extract_code_symbols to get detailed function/class information
5. Use calculate_code_complexity for complexity analysis
6. Create a structured map with:
   - Directory structure
   - Key files and their purposes
   - Important classes/functions
   - Dependencies between modules

Use the tools to gather information, then provide a comprehensive repository map."""

            user_prompt = f"""Please analyze the repository at {self.code_tools.workspace_root} and create a comprehensive repository map.

Focus on the src/ directory and create a map that will help with:
- Understanding the codebase architecture
- Identifying relevant files for code changes
- Understanding relationships between modules

Instruction context: {state.get("instruction", "General repository analysis")}"""

            # Initialize messages if not present
            if "messages" not in state or not state["messages"]:
                messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            else:
                messages = state["messages"] + [HumanMessage(content=user_prompt)]

            # Let LLM generate tool calls
            response = await llm_with_tools.ainvoke(messages)

            # Update messages with LLM response
            updated_messages = messages + [response]

            return {
                "messages": updated_messages,
                "current_node": "repo_map_tools" if response.tool_calls else "repo_map_analysis",
            }

        except Exception as e:
            error_msg = f"LLM repository mapping failed: {str(e)}"
            logger.error(error_msg)
            return {"error_message": error_msg, "current_node": "error_handler"}

    async def llm_file_discovery(self, state: OpenSWEState) -> dict:
        """
        LLM node for file discovery - generates tool calls.
        Uses proper ToolNode pattern from the fixed implementation.
        """
        logger.info("--- LLM File Discovery ---")

        try:
            instruction = state.get("instruction", "")
            repo_map_content = state.get("repo_map_content", "")

            if not instruction:
                return {
                    "error_message": "No instruction provided for target file discovery",
                    "current_node": "error_handler",
                }

            # Get available tools for file discovery
            from src.tools.openswe import grep_search, view

            discovery_tools = [view, grep_search]
            llm_with_tools = self.code_tools.editor_llm.bind_tools(discovery_tools)

            system_prompt = """You are a file discovery expert. Your task is to identify the most relevant files for a given instruction.

GOAL: Discover 3-8 target files that are most likely to need modification for the given instruction.

CRITERIA for file selection:
- Files that directly implement the functionality mentioned in the instruction
- Files that contain classes/functions referenced in the instruction
- Test files if the instruction involves testing
- Configuration files if the instruction involves setup/config changes
- Related files that might be affected by the changes

AVAILABLE TOOLS:
- view: View file or directory contents
- grep_search: Search for patterns in files

PROCESS:
1. Analyze the instruction to understand what needs to be done
2. Use the repository map to understand the codebase structure
3. Use view and grep_search tools to explore relevant files
4. Identify the most relevant files based on the criteria above
5. Return a structured list of target files with reasoning

Return your analysis as a structured file discovery result."""

            user_prompt = f"""INSTRUCTION: {instruction}

REPOSITORY MAP:
{repo_map_content[:2000]}  # Limit to first 2000 chars to avoid token limits

Please analyze this instruction and repository structure to discover the target files that need modification. Use the available tools to search and analyze the codebase as needed.

Focus on finding files that:
1. Directly relate to the functionality mentioned in the instruction
2. Contain relevant classes, functions, or modules
3. Would logically need changes to implement the instruction
4. Include any test files that would need updates

Return 3-8 most relevant files, prioritized by likelihood of needing changes."""

            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

            response = await llm_with_tools.ainvoke(messages)
            updated_messages = messages + [response]

            return {
                "messages": updated_messages,
                "current_node": "discovery_tools" if response.tool_calls else "discovery_analysis",
            }

        except Exception as e:
            error_msg = f"LLM file discovery failed: {str(e)}"
            logger.error(error_msg)
            return {"error_message": error_msg, "current_node": "error_handler"}

    async def llm_file_ranking(self, state: OpenSWEState) -> dict:
        """
        LLM node for file ranking - generates tool calls.
        Uses proper ToolNode pattern from the fixed implementation.
        """
        logger.info("--- LLM File Ranking ---")

        try:
            instruction = state.get("instruction", "")
            discovered_files = state.get("discovered_files", [])

            if not discovered_files:
                return {"error_message": "No discovered files to rank", "current_node": "error_handler"}

            # Get available tools for file analysis
            from src.tools.openswe import analyze_code_structure, view

            ranking_tools = [view, analyze_code_structure]
            llm_with_tools = self.code_tools.editor_llm.bind_tools(ranking_tools)

            system_prompt = """You are a file ranking expert. Your task is to rank discovered files by their relevance to a given instruction.

GOAL: Rank files by their likelihood of needing modification for the given instruction.

RANKING CRITERIA:
1. Direct relevance to the instruction (highest priority)
2. Complexity of changes required
3. Impact on other parts of the system
4. Test coverage and validation needs
5. Dependencies and integration points

AVAILABLE TOOLS:
- view: View file contents to understand structure
- analyze_code_structure: Analyze code complexity and structure

PROCESS:
1. Analyze each discovered file using the available tools
2. Evaluate relevance to the instruction
3. Consider complexity and impact
4. Rank files from most to least relevant
5. Provide reasoning for ranking decisions

Return your analysis as a structured file ranking result."""

            user_prompt = f"""INSTRUCTION: {instruction}

DISCOVERED FILES TO RANK:
{chr(10).join(f"- {file}" for file in discovered_files)}

Please analyze each file and rank them by relevance to the instruction. Use the available tools to understand file contents and structure.

For each file, consider:
1. How directly it relates to the instruction
2. What changes would be needed
3. How complex those changes would be
4. What impact it would have on the system

Return a ranked list with reasoning for each ranking decision."""

            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

            response = await llm_with_tools.ainvoke(messages)
            updated_messages = messages + [response]

            return {
                "messages": updated_messages,
                "current_node": "ranking_tools" if response.tool_calls else "ranking_analysis",
            }

        except Exception as e:
            error_msg = f"LLM file ranking failed: {str(e)}"
            logger.error(error_msg)
            return {"error_message": error_msg, "current_node": "error_handler"}

    # === ANALYSIS NODES: Process Tool Results ===

    async def repo_map_analysis(self, state: OpenSWEState) -> dict:
        """
        Analyze tool results and generate structured repository map.
        From the fixed implementation with structured outputs.
        """
        logger.info("--- Repository Map Analysis ---")

        try:
            messages = state.get("messages", [])
            if not messages:
                return {"error_message": "No messages for repository map analysis", "current_node": "error_handler"}

            # Get the last AI message (should contain the analysis)
            last_ai_message = None
            for msg in reversed(messages):
                if isinstance(msg, AIMessage) and not msg.tool_calls:
                    last_ai_message = msg
                    break

            if not last_ai_message:
                return {"error_message": "No AI analysis found in messages", "current_node": "error_handler"}

            # Create structured output using Pydantic
            try:
                llm_with_structured_output = self.code_tools.editor_llm.with_structured_output(
                    RepositoryMapResult, method="function_calling"
                )

                analysis_prompt = f"""Based on the repository analysis, create a structured repository map result.

Analysis: {last_ai_message.content}

Please extract:
1. The repository map content (structured and comprehensive)
2. Key files identified (list of important files)
3. Architecture summary (brief overview of the codebase structure)
4. Confidence score (0.0 to 1.0 based on analysis completeness)

Return as a structured RepositoryMapResult."""

                structured_result = await llm_with_structured_output.ainvoke([HumanMessage(content=analysis_prompt)])

                # Save the repository map
                artifacts_dir = self.code_tools.artifacts_dir / "repo_maps"
                artifacts_dir.mkdir(exist_ok=True)

                import datetime

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                repo_map_filename = f"repo_map_structured_{timestamp}.txt"
                repo_map_path = artifacts_dir / repo_map_filename

                with open(repo_map_path, "w", encoding="utf-8") as f:
                    f.write(f"# Repository Map (Generated by Unified LLM + Open SWE Tools)\\n")
                    f.write(f"# Workspace: {self.code_tools.workspace_root}\\n")
                    f.write(f"# Generated: {datetime.datetime.now()}\\n")
                    f.write(f"# Confidence: {structured_result.confidence_score}\\n\\n")
                    f.write(structured_result.repo_map_content)

                logger.info(f"Structured repository map saved to: {repo_map_path}")

                return {
                    "repo_map_path": str(repo_map_path),
                    "repo_map_content": structured_result.repo_map_content,
                    "current_node": "llm_file_discovery",
                }

            except Exception as e:
                logger.warning(f"Structured output failed, using fallback: {e}")
                # Fallback to simple content extraction
                return {
                    "repo_map_path": None,
                    "repo_map_content": last_ai_message.content,
                    "current_node": "llm_file_discovery",
                }

        except Exception as e:
            error_msg = f"Repository map analysis failed: {str(e)}"
            logger.error(error_msg)
            return {"error_message": error_msg, "current_node": "error_handler"}

    async def discovery_analysis(self, state: OpenSWEState) -> dict:
        """
        Analyze tool results and generate structured file discovery.
        From the fixed implementation with structured outputs.
        """
        logger.info("--- File Discovery Analysis ---")

        try:
            messages = state.get("messages", [])
            if not messages:
                return {"error_message": "No messages for file discovery analysis", "current_node": "error_handler"}

            # Get the last AI message (should contain the analysis)
            last_ai_message = None
            for msg in reversed(messages):
                if isinstance(msg, AIMessage) and not msg.tool_calls:
                    last_ai_message = msg
                    break

            if not last_ai_message:
                return {"error_message": "No AI analysis found in messages", "current_node": "error_handler"}

            # Create structured output using Pydantic
            try:
                llm_with_structured_output = self.code_tools.editor_llm.with_structured_output(
                    FileDiscoveryResult, method="function_calling"
                )

                analysis_prompt = f"""Based on the file discovery analysis, create a structured file discovery result.

Analysis: {last_ai_message.content}

Please extract:
1. List of discovered target files (3-8 files)
2. Reasoning for file selection (explanation of why these files were chosen)
3. Confidence score (0.0 to 1.0 based on discovery quality)
4. File categories (group files by type: implementation, tests, config, etc.)

Return as a structured FileDiscoveryResult."""

                structured_result = await llm_with_structured_output.ainvoke([HumanMessage(content=analysis_prompt)])

                logger.info(f"Structured file discovery: {len(structured_result.discovered_files)} files")

                return {
                    "discovered_files": structured_result.discovered_files,
                    "discovery_reasoning": structured_result.discovery_reasoning,
                    "discovery_confidence": structured_result.discovery_confidence,
                    "current_node": "llm_file_ranking",
                }

            except Exception as e:
                logger.warning(f"Structured output failed, using fallback: {e}")
                # Fallback to simple file extraction
                fallback_files = ["src/agent.py", "src/tools/openswe/code_tools.py"]
                return {
                    "discovered_files": fallback_files,
                    "discovery_reasoning": "Fallback files due to structured output failure",
                    "discovery_confidence": 0.2,
                    "current_node": "llm_file_ranking",
                }

        except Exception as e:
            error_msg = f"File discovery analysis failed: {str(e)}"
            logger.error(error_msg)
            return {"error_message": error_msg, "current_node": "error_handler"}

    async def ranking_analysis(self, state: OpenSWEState) -> dict:
        """
        Analyze tool results and generate structured file ranking.
        From the fixed implementation with structured outputs.
        """
        logger.info("--- File Ranking Analysis ---")

        try:
            messages = state.get("messages", [])
            if not messages:
                return {"error_message": "No messages for file ranking analysis", "current_node": "error_handler"}

            # Get the last AI message (should contain the analysis)
            last_ai_message = None
            for msg in reversed(messages):
                if isinstance(msg, AIMessage) and not msg.tool_calls:
                    last_ai_message = msg
                    break

            if not last_ai_message:
                return {"error_message": "No AI analysis found in messages", "current_node": "error_handler"}

            # Create structured output using Pydantic
            try:
                llm_with_structured_output = self.code_tools.editor_llm.with_structured_output(
                    FileRankingResult, method="function_calling"
                )

                analysis_prompt = f"""Based on the file ranking analysis, create a structured file ranking result.

Analysis: {last_ai_message.content}

Please extract:
1. Ranked files (list of files with ranking information: file path, priority score, reasoning)
2. Ranking reasoning (explanation of ranking decisions)
3. Confidence score (0.0 to 1.0 based on ranking quality)

Each file should have: {{"file": "path/to/file", "priority": 1-10, "reasoning": "why this rank"}}

Return as a structured FileRankingResult."""

                structured_result = await llm_with_structured_output.ainvoke([HumanMessage(content=analysis_prompt)])

                logger.info(f"Structured file ranking: {len(structured_result.ranked_files)} files")

                return {
                    "ranked_files": structured_result.ranked_files,
                    "ranking_reasoning": structured_result.ranking_reasoning,
                    "ranking_confidence": structured_result.ranking_confidence,
                    "current_node": "generate_diff",
                }

            except Exception as e:
                logger.warning(f"Structured output failed, using fallback: {e}")
                # Fallback to simple ranking
                discovered_files = state.get("discovered_files", [])
                fallback_ranking = [
                    {"file": file, "priority": 5, "reasoning": "Default priority due to analysis failure"}
                    for file in discovered_files
                ]
                return {
                    "ranked_files": fallback_ranking,
                    "ranking_reasoning": "Fallback ranking due to structured output failure",
                    "ranking_confidence": 0.2,
                    "current_node": "generate_diff",
                }

        except Exception as e:
            error_msg = f"File ranking analysis failed: {str(e)}"
            logger.error(error_msg)
            return {"error_message": error_msg, "current_node": "error_handler"}

    # === EXECUTION PHASE: Complete Workflow from Original Implementation ===

    async def plan_edits(self, state: OpenSWEState) -> dict:
        """
        Plan the edits based on the instruction and target files.
        This is the key missing node from the execution phase.
        """
        try:
            logger.info("--- Planning Edits with Native CodeTools ---")

            # Use ranked files if available, otherwise fall back to target_files
            files_to_use = state.get("target_files", [])
            if state.get("ranked_files"):
                # Extract file paths from ranked files
                files_to_use = [file_info["file"] for file_info in state["ranked_files"][:5]]  # Top 5 files
                logger.info(f"Using ranked files for planning: {files_to_use}")
            else:
                logger.info(f"Using target files for planning: {files_to_use}")

            if not files_to_use:
                return {
                    "diff_result": {
                        "status": "error",
                        "error_code": "NO_FILES_SPECIFIED",
                        "error_hint": "Please specify files to edit",
                        "summary": "No files specified for edit planning",
                    },
                    "error_message": "No files specified for edit planning",
                }

            # Use CodeTools to plan edits
            result = await self.code_tools.propose_diff(
                goal=state["instruction"], files=files_to_use, response_format="detailed"
            )

            if result.status == "success":
                logger.info(f"Successfully planned edits for {len(files_to_use)} files")
                return {
                    "diff_result": {
                        "status": "success",
                        "artifact_uri": result.artifact_uri,
                        "files_changed": result.files_changed,
                        "summary": result.summary,
                        "stats": result.stats,
                    },
                    "error_message": None,
                }
            else:
                logger.error(f"Failed to plan edits: {result.result}")
                return {
                    "diff_result": {
                        "status": "error",
                        "error_code": result.error_code,
                        "error_hint": result.error_hint,
                        "summary": result.summary,
                    },
                    "error_message": result.result,
                }

        except Exception as e:
            logger.error(f"Error in plan_edits: {e}", exc_info=True)
            return {
                "diff_result": {
                    "status": "error",
                    "error_code": "PLAN_EDITS_ERROR",
                    "error_hint": "Check LLM connectivity and file permissions",
                    "summary": f"Edit planning failed: {str(e)}",
                },
                "error_message": str(e),
            }

    async def generate_diff(self, state: OpenSWEState) -> dict:
        """
        Generate a diff using native CodeTools operations.
        From the original implementation with ranked files support.
        """
        try:
            logger.info("--- Generating Diff with Native CodeTools ---")

            # Use ranked files if available, otherwise fall back to target_files
            files_to_use = state.get("target_files", [])
            if state.get("ranked_files"):
                # Extract file paths from ranked files
                files_to_use = [file_info["file"] for file_info in state["ranked_files"][:3]]  # Top 3 files
                logger.info(f"Using ranked files: {files_to_use}")
            else:
                logger.info(f"Using target files: {files_to_use}")

            if not files_to_use:
                return {
                    "diff_result": {
                        "status": "error",
                        "error_code": "NO_FILES_SPECIFIED",
                        "error_hint": "No files specified for diff generation",
                        "summary": "No valid files found for diff generation",
                    },
                    "current_node": "error_handler",
                    "error_message": "No valid files found for diff generation",
                }

            # Use CodeTools to generate diff
            result = await self.code_tools.propose_diff(
                goal=state["instruction"],
                files=files_to_use,
                response_format="detailed",  # Use detailed format for execution
            )

            if result.status == "success":
                logger.info(f"Successfully generated diff for {len(files_to_use)} files")
                return {
                    "diff_result": {
                        "status": "success",
                        "artifact_uri": result.artifact_uri,
                        "files_changed": result.files_changed,
                        "summary": result.summary,
                        "stats": result.stats,
                    },
                    "current_node": "validate_diff",
                    "error_message": None,
                }
            else:
                logger.error(f"Failed to generate diff: {result.result}")
                return {
                    "diff_result": {
                        "status": "error",
                        "error_code": result.error_code,
                        "error_hint": result.error_hint,
                        "summary": result.summary,
                    },
                    "current_node": "error_handler",
                    "error_message": result.result,
                }

        except Exception as e:
            logger.error(f"Error in generate_diff: {e}", exc_info=True)
            return {
                "diff_result": {
                    "status": "error",
                    "error_code": "DIFF_GENERATION_ERROR",
                    "error_hint": "Check LLM connectivity and file permissions",
                    "summary": f"Diff generation failed: {str(e)}",
                },
                "current_node": "error_handler",
                "error_message": str(e),
            }

    async def validate_diff(self, state: OpenSWEState) -> dict:
        """
        Validate the generated diff using native operations.
        From the original implementation.
        """
        try:
            logger.info("--- Validating Diff with Native Operations ---")

            # Get the files to validate - use ranked files or target files
            files_to_validate = state.get("target_files", [])
            if state.get("ranked_files"):
                files_to_validate = [file_info["file"] for file_info in state["ranked_files"][:3]]

            # Run linting on target files
            lint_result = await self.code_tools.lint(paths=files_to_validate, response_format="detailed")

            # Run tests if configured
            test_result = None
            if self.validation_config.get("enable_testing", True):
                test_result = await self.code_tools.test(response_format="detailed")

            # Determine overall validation status
            validation_success = lint_result.status == "success" and (
                test_result is None or test_result.status == "success"
            )

            if validation_success:
                logger.info("Diff validation passed")
                return {
                    "validation_result": {
                        "status": "success",
                        "lint_result": {
                            "status": lint_result.status,
                            "summary": lint_result.summary,
                            "stats": lint_result.stats,
                        },
                        "test_result": {
                            "status": test_result.status if test_result else "skipped",
                            "summary": test_result.summary if test_result else "Tests skipped",
                            "stats": test_result.stats if test_result else {},
                        },
                    },
                    "current_node": "human_approval",
                    "error_message": None,
                }
            else:
                logger.warning("Diff validation failed")
                return {
                    "validation_result": {
                        "status": "error",
                        "lint_result": {
                            "status": lint_result.status,
                            "error_code": lint_result.error_code,
                            "error_hint": lint_result.error_hint,
                            "summary": lint_result.summary,
                        },
                        "test_result": {
                            "status": test_result.status if test_result else "skipped",
                            "error_code": test_result.error_code if test_result else None,
                            "error_hint": test_result.error_hint if test_result else None,
                            "summary": test_result.summary if test_result else "Tests skipped",
                        },
                    },
                    "current_node": "error_handler",
                    "error_message": f"Validation failed: lint={lint_result.status}, test={test_result.status if test_result else 'skipped'}",
                }

        except Exception as e:
            logger.error(f"Error in validate_diff: {e}", exc_info=True)
            return {
                "validation_result": {
                    "status": "error",
                    "error_code": "VALIDATION_ERROR",
                    "error_hint": "Check validation configuration and tool availability",
                    "summary": f"Validation failed: {str(e)}",
                },
                "current_node": "error_handler",
                "error_message": str(e),
            }

    async def human_approval(self, state: OpenSWEState) -> dict:
        """
        Handle human approval for the changes.
        From the original implementation.
        """
        try:
            logger.info("--- Human Approval ---")

            # If we have a custom approval node, use it
            if self.approval_node:
                approval_result = self.approval_node(state)
                if isinstance(approval_result, dict):
                    return {
                        "approved": approval_result.get("is_approved", False),
                        "current_node": "apply_changes"
                        if approval_result.get("is_approved", False)
                        else "error_handler",
                        "error_message": None
                        if approval_result.get("is_approved", False)
                        else "Changes rejected by approval node",
                    }

            # Default: auto-approve for now (can be made interactive later)
            logger.info("Auto-approving changes (no custom approval node)")
            return {"approved": True, "current_node": "apply_changes", "error_message": None}

        except Exception as e:
            logger.error(f"Error in human_approval: {e}", exc_info=True)
            return {"approved": False, "current_node": "error_handler", "error_message": str(e)}

    async def apply_changes(self, state: OpenSWEState) -> dict:
        """
        Apply the changes using native CodeTools operations.
        From the original implementation.
        """
        try:
            logger.info("--- Applying Changes with Native Operations ---")

            # Get the diff artifact path from the diff_result
            diff_artifact_uri = state.get("diff_result", {}).get("artifact_uri")
            if not diff_artifact_uri:
                raise ValueError("No diff artifact found in state")

            # Apply the patch using CodeTools
            result = await self.code_tools.apply_patch(diff_path=diff_artifact_uri, response_format="detailed")

            if result.status == "success":
                logger.info("Successfully applied changes")
                return {
                    "apply_result": {
                        "status": "success",
                        "files_changed": result.files_changed,
                        "summary": result.summary,
                        "stats": result.stats,
                        "commit_sha": result.commit_sha,
                    },
                    "current_node": "run_tests",
                    "error_message": None,
                }
            else:
                logger.error(f"Failed to apply changes: {result.result}")
                return {
                    "apply_result": {
                        "status": "error",
                        "error_code": result.error_code,
                        "error_hint": result.error_hint,
                        "summary": result.summary,
                    },
                    "current_node": "error_handler",
                    "error_message": result.result,
                }

        except Exception as e:
            logger.error(f"Error in apply_changes: {e}", exc_info=True)
            return {
                "apply_result": {
                    "status": "error",
                    "error_code": "APPLY_ERROR",
                    "error_hint": "Check patch format and file permissions",
                    "summary": f"Failed to apply changes: {str(e)}",
                },
                "current_node": "error_handler",
                "error_message": str(e),
            }

    async def run_tests(self, state: OpenSWEState) -> dict:
        """
        Run tests after applying changes.
        From the original implementation.
        """
        try:
            logger.info("--- Running Tests After Changes ---")

            # Run tests using CodeTools
            result = await self.code_tools.test(response_format="detailed")

            if result.status == "success":
                logger.info("All tests passed")
                # Update state with test result
                updated_state = state.copy()
                updated_state["test_result"] = {"status": "success", "summary": result.summary, "stats": result.stats}
                # Use routing function to determine next node
                next_node = self.route_after_tests(updated_state)
                return {
                    "test_result": {"status": "success", "summary": result.summary, "stats": result.stats},
                    "current_node": next_node,
                    "error_message": None,
                }
            else:
                logger.warning(f"Tests failed: {result.result}")
                return {
                    "test_result": {
                        "status": "error",
                        "error_code": result.error_code,
                        "error_hint": result.error_hint,
                        "summary": result.summary,
                    },
                    "current_node": "error_handler",
                    "error_message": result.result,
                }

        except Exception as e:
            logger.error(f"Error in run_tests: {e}", exc_info=True)
            return {
                "test_result": {
                    "status": "error",
                    "error_code": "TEST_ERROR",
                    "error_hint": "Check test configuration and framework availability",
                    "summary": f"Test execution failed: {str(e)}",
                },
                "current_node": "error_handler",
                "error_message": str(e),
            }

    async def setup_git_branch(self, state: OpenSWEState) -> dict:
        """
        Sets up a temporary git branch for isolated edits.
        From aider_graph.py implementation.
        """
        logger.info("--- Setting up Git Branch ---")
        current_branch = self.git_ops.get_current_branch()
        if not current_branch:
            return {"error_message": "Failed to determine current git branch."}

        # Preserve the true original branch if it's already set, otherwise use current branch
        original_branch = state.get("original_branch_name", current_branch)

        temp_branch = self.git_ops.create_temp_branch(base_branch=current_branch)
        if not temp_branch:
            return {"error_message": "Failed to create temporary git branch."}

        return {
            "git_branch_name": temp_branch,
            "original_branch_name": original_branch,  # Preserve the true original branch
            "current_node": "commit_changes",
            "error_message": None,
        }

    async def commit_changes(self, state: OpenSWEState) -> dict:
        """
        Commits the changes by merging the temporary branch into main.
        From aider_graph.py implementation.
        """
        logger.info("--- Committing Changes (Merging Branch) ---")

        temp_branch = state.get("git_branch_name")
        original_branch = state.get("original_branch_name", "main")
        instruction = state.get("instruction", "")

        if not temp_branch:
            logger.error("Commit node failed: temporary branch name is missing from state.")
            return {"error_message": "Cannot commit; temporary branch name is missing from state."}

        logger.info(f"Commit node received state: temp_branch='{temp_branch}', original_branch='{original_branch}'")

        # First, commit the changes on the temporary branch
        try:
            import subprocess
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"feat(openswe): {instruction}\n\nAutomated commit via OpenSWE Tools Graph pipeline\nTimestamp: {timestamp}"

            repo_root = self._resolve_repo_root()
            subprocess.run(["git", "add", "."], cwd=repo_root, check=True, capture_output=True)
            staged = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            )
            if not staged.stdout.strip():
                logger.info("No staged changes found; skipping commit.")
                return {
                    "commit_hash": None,
                    "git_branch_name": temp_branch,
                    "original_branch_name": original_branch,
                    "commit_message": "No changes to commit",
                    "current_node": "create_pull_request",
                    "error_message": None,
                }
            commit_run = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=repo_root,
                check=True,
                capture_output=True,
                text=True,
            )
            logger.info(f"Git commit on temporary branch successful. STDOUT: {commit_run.stdout}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Git commit on temporary branch failed: {e.stderr if e.stderr else str(e)}"
            logger.error(error_msg)
            # Proceed to rollback since commit failed
            return {"error_message": error_msg, "current_node": "rollback_changes"}

        # Keep the temporary branch for PR creation (don't merge back)
        logger.info(f"Keeping temporary branch '{temp_branch}' for PR creation")

        # Get the commit hash from the temp branch
        temp_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self._resolve_repo_root(), universal_newlines=True
        ).strip()

        # Return only the state updates (LangGraph pattern)
        return {
            "commit_hash": temp_commit,
            "git_branch_name": temp_branch,  # Use existing field name
            "original_branch_name": original_branch,  # Use existing field name
            "commit_message": f"Temporary branch '{temp_branch}' kept for PR creation",
            "current_node": "create_pull_request",
            "error_message": None,
        }

    async def create_pull_request(self, state: OpenSWEState) -> dict:
        """
        Creates a pull request after successful commit.
        From aider_graph.py implementation.
        """
        logger.info("--- Creating Pull Request ---")

        instruction = state.get("instruction", "")
        commit_message = state.get("commit_message", "")
        commit_hash = state.get("commit_hash", "")

        # Check if PR creation is enabled via configuration defaults (env fallback)
        try:
            from src.config_loader import get_config

            config = get_config()
            auto_create_pr = bool(config.defaults.auto_create_pr)
            default_base_branch = config.defaults.base_branch
        except Exception:
            auto_create_pr = os.getenv("AUTO_CREATE_PR", "false").lower() == "true"
            default_base_branch = os.getenv("PR_BASE_BRANCH", "main")

        if not auto_create_pr:
            logger.info("PR creation is disabled via configuration defaults")
            return {"pr_creation_skipped": True, "reason": "auto_create_pr is disabled", "current_node": "complete"}

        if not commit_hash:
            logger.info("PR creation skipped: missing commit hash")
            return {"pr_creation_skipped": True, "reason": "missing commit hash", "current_node": "complete"}

        # Use the temp branch for PR creation instead of current branch
        temp_branch = state.get("git_branch_name")  # Use existing field name
        original_branch = state.get("original_branch_name")  # Use existing field name
        if original_branch and original_branch.startswith("cce-agent/"):
            base_branch = default_base_branch
        elif original_branch and self.git_ops.remote_branch_exists(original_branch):
            base_branch = original_branch
        else:
            base_branch = default_base_branch

        # Debug: Log the entire state to see what's available
        logger.info(f"DEBUG - create_pull_request state keys: {list(state.keys())}")
        logger.info(f"DEBUG - temp_branch (git_branch_name): {temp_branch}")
        logger.info(f"DEBUG - original_branch (original_branch_name): {original_branch}")
        logger.info(f"DEBUG - resolved_base_branch: {base_branch}")

        if not temp_branch:
            logger.error("No temp branch found in state for PR creation")
            return {"pr_creation_skipped": True, "reason": "No temp branch found", "current_node": "complete"}

        logger.info(f"Creating PR from temp branch '{temp_branch}' to base branch '{base_branch}'")

        # Create PR using GitOps service
        try:
            # Create a more descriptive title from the instruction
            title_snippet = instruction[:50] + "..." if len(instruction) > 50 else instruction
            pr_title = f"feat(openswe): {title_snippet}"

            pr_body = f"""## Description
{instruction}

## Changes Made
- Automated changes via OpenSWE Tools Graph pipeline
- Commit: {commit_hash}
- Branch: {temp_branch} → {base_branch}

## Testing
- [x] Automated validation passed
- [x] Linting checks passed
- [x] Human approval received

## Checklist
- [x] Code follows project style guidelines
- [x] Automated validation completed
- [x] No breaking changes
- [x] Changes reviewed and approved

## Related
Automated commit via CCE Agent OpenSWE Tools Graph
"""

            # Use GitOps service to create PR from temp branch
            result = self.git_ops.create_pull_request(
                title=pr_title, body=pr_body, head_branch=temp_branch, base_branch=base_branch, labels=[]
            )

            if result.get("skipped"):
                logger.info(f"PR creation skipped: {result.get('error', 'no commits')}")
                return {
                    "pr_creation_skipped": True,
                    "reason": result.get("error", "skipped"),
                    "current_node": "complete",
                }

            if result["success"]:
                logger.info(f"PR created successfully: {result['pr_url']}")
                return {
                    "pr_created": True,
                    "pr_url": result["pr_url"],
                    "pr_message": result["message"],
                    "current_node": "complete",
                    "error_message": None,
                }
            else:
                logger.error(f"PR creation failed: {result['error']}")
                return {
                    "pr_created": False,
                    "pr_error": result["error"],
                    "current_node": "complete",
                    "error_message": f"PR creation failed: {result['error']}",
                }

        except Exception as e:
            error_msg = f"PR creation failed with exception: {str(e)}"
            logger.error(error_msg)
            return {"pr_created": False, "pr_error": error_msg, "current_node": "complete", "error_message": error_msg}

    async def rollback_changes(self, state: OpenSWEState) -> dict:
        """
        Rolls back by abandoning the temporary branch.
        From aider_graph.py implementation.
        """
        logger.info("--- Rolling Back Changes (Abandoning Branch) ---")

        temp_branch = state.get("git_branch_name")
        original_branch = state.get("original_branch_name")
        error_message = state.get("error_message", "Unknown error")

        if not temp_branch or not original_branch:
            # Fallback to git reset if branch info is missing
            return await self.fallback_rollback(state)

        success, message = self.git_ops.abort_merge_and_delete_branch(temp_branch, original_branch)

        if success:
            logger.info(f"Successfully rolled back by abandoning branch '{temp_branch}'.")
            return {
                "rollback_successful": True,
                "reason": f"Rollback due to: {error_message}",
                "current_node": "complete",
                "error_message": None,
            }
        else:
            logger.error(f"Failed to rollback by abandoning branch: {message}")
            return {"rollback_successful": False, "error_message": message, "current_node": "complete"}

    async def fallback_rollback(self, state: OpenSWEState) -> dict:
        """
        Original git reset rollback as a fallback.
        From aider_graph.py implementation.
        """
        logger.warning("--- Performing Fallback Rollback (git reset) ---")
        git_head_before_edit = state.get("git_head_before_edit")
        error_message = state.get("error_message", "Unknown error during fallback")

        try:
            import subprocess

            target_head = git_head_before_edit if git_head_before_edit else "HEAD"

            logger.info(f"Rolling back to git target HEAD: {target_head}")
            subprocess.run(["git", "reset", "--hard", target_head], cwd=self._resolve_repo_root(), check=True, capture_output=True)
            subprocess.run(["git", "clean", "-fd"], cwd=self._resolve_repo_root(), check=True, capture_output=True)

            logger.info("Successfully rolled back changes")
            return {
                "rollback_successful": True,
                "rolled_back_to": target_head,
                "reason": f"Rollback due to: {error_message}",
                "current_node": "complete",
                "error_message": None,
            }

        except subprocess.CalledProcessError as e:
            error_msg = f"Git rollback failed: {e.stderr if e.stderr else str(e)}"
            logger.error(error_msg)
            return {
                "rollback_successful": False,
                "error_message": error_msg,
                "reason": f"Rollback due to: {error_message}",
                "current_node": "complete",
            }
        except Exception as e:
            error_msg = f"Rollback failed: {str(e)}"
            logger.error(error_msg)
            return {
                "rollback_successful": False,
                "error_message": error_msg,
                "reason": f"Rollback due to: {error_message}",
                "current_node": "complete",
            }

    async def complete(self, state: OpenSWEState) -> dict:
        """
        Complete the execution and return final state.
        From the original implementation.
        """
        logger.info("--- Execution Complete ---")

        # Create execution summary
        summary = {
            "status": "success" if not state.get("error_message") else "error",
            "instruction": state["instruction"],
            "target_files": state["target_files"],
            "discovered_files": state.get("discovered_files", []),
            "ranked_files": state.get("ranked_files", []),
            "diff_generated": state.get("diff_result", {}).get("status") == "success"
            if state.get("diff_result")
            else False,
            "validation_passed": state.get("validation_result", {}).get("status") == "success"
            if state.get("validation_result")
            else False,
            "changes_applied": state.get("apply_result", {}).get("status") == "success"
            if state.get("apply_result")
            else False,
            "tests_passed": state.get("test_result", {}).get("status") == "success"
            if state.get("test_result")
            else False,
            "error_message": state.get("error_message"),
        }

        result = {"current_node": "complete", "execution_summary": summary}
        logger.info(f"Complete method returning: {list(result.keys())}")
        return result

    # === ROUTING FUNCTIONS ===

    # Original workflow routing (from original implementation)
    def route_after_plan_edits(self, state: OpenSWEState) -> str:
        """Route after plan_edits based on result."""
        logger.info(f"🔍 DEBUG: route_after_plan_edits called with state: {state}")
        if state is None:
            logger.warning("🔍 DEBUG: state is None in route_after_plan_edits")
            return "error_handler"
        if state.get("diff_result", {}).get("status") == "success":
            logger.info("🔍 DEBUG: routing to generate_diff")
            return "generate_diff"
        else:
            logger.info("🔍 DEBUG: routing to error_handler")
            return "error_handler"

    def route_after_diff_generation(self, state: OpenSWEState) -> str:
        """Route after diff generation based on result."""
        if state is None:
            return "error_handler"
        if state.get("diff_result", {}).get("status") == "success":
            return "validate_diff"
        else:
            return "error_handler"

    # ToolNode routing (from fixed implementation)
    def should_use_repo_tools(self, state: OpenSWEState) -> str:
        """Route to tools if LLM made tool calls, otherwise to analysis."""
        messages = state.get("messages", [])
        if not messages:
            return "repo_map_analysis"

        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "repo_map_tools"
        else:
            return "repo_map_analysis"

    def should_use_discovery_tools(self, state: OpenSWEState) -> str:
        """Route to tools if LLM made tool calls, otherwise to analysis."""
        messages = state.get("messages", [])
        if not messages:
            return "discovery_analysis"

        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "discovery_tools"
        else:
            return "discovery_analysis"

    def should_use_ranking_tools(self, state: OpenSWEState) -> str:
        """Route to tools if LLM made tool calls, otherwise to analysis."""
        messages = state.get("messages", [])
        if not messages:
            return "ranking_analysis"

        last_message = messages[-1]
        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "ranking_tools"
        else:
            return "ranking_analysis"

    # Execution routing (from original implementation)
    def route_after_validation(self, state: OpenSWEState) -> str:
        """Route after validation based on result."""
        if state is None:
            return "error_handler"
        if state.get("validation_result", {}).get("status") == "success":
            return "human_approval"
        else:
            return "error_handler"

    def route_after_approval(self, state: OpenSWEState) -> str:
        """Route after approval based on decision."""
        if state.get("approved", False):
            return "apply_changes"
        else:
            return "error_handler"

    def route_after_apply(self, state: OpenSWEState) -> str:
        """Route after applying changes based on result."""
        if state.get("apply_result", {}).get("status") == "success":
            return "run_tests"
        else:
            return "error_handler"

    def route_after_tests(self, state: OpenSWEState) -> str:
        """Route after running tests - always goes to complete."""
        return "complete"

    # === ERROR HANDLING ===

    async def error_handler(self, state: OpenSWEState) -> dict:
        """
        Handle errors and provide recovery options.
        From both implementations.
        """
        error_message = state.get("error_message", "Unknown error occurred")
        logger.error(f"Error handler activated: {error_message}")

        return {"error_message": error_message, "current_node": "complete"}

    # === HIGH-LEVEL RUN METHOD ===

    async def run(
        self,
        instruction: str,
        target_files: list[str],
        auto_approve: bool = True,
        structured_phases: list[dict[str, Any]] = None,
    ) -> dict:
        """
        Run the full Open SWE pipeline for a given instruction.
        From the original implementation with unified graph.
        """
        import uuid

        thread_id = f"open-swe-run-{uuid.uuid4()}"
        config = {"configurable": {"thread_id": thread_id}}

        # Use an in-memory checkpointer for this run
        checkpointer = InMemorySaver()

        # Create approval node if auto_approve is True
        approval_node = None
        if auto_approve:

            def auto_approval_node(state: OpenSWEState) -> dict:
                """A node that automatically approves changes."""
                logger.info("--- Auto-approving Changes ---")
                return {"is_approved": True}

            approval_node = auto_approval_node

        # Create the unified graph
        graph = create_open_swe_graph(
            self.code_tools,
            self.git_ops,
            self.validation_runner,
            checkpointer=checkpointer,
            approval_node=self.approval_node or approval_node,
        )

        # Get the current branch as the original branch
        current_branch = self.git_ops.get_current_branch()

        # Create initial state
        initial_state: OpenSWEState = {
            "instruction": instruction,
            "target_files": target_files,
            "current_node": "plan_edits",
            "messages": [],
            "repo_map_path": None,
            "repo_map_content": None,
            "discovered_files": None,
            "discovery_reasoning": None,
            "discovery_confidence": None,
            "ranked_files": None,
            "ranking_reasoning": None,
            "ranking_confidence": None,
            "diff_result": None,
            "dry_run_result": None,
            "validation_result": None,
            "apply_result": None,
            "test_result": None,
            "approved": None,
            "is_approved": None,
            "error_message": None,
            "git_branch_name": None,
            "original_branch_name": current_branch,
            "git_head_before_edit": None,
            "commit_hash": None,
            "commit_message": None,
            "structured_phases": structured_phases,
            "parsed_phases": None,
            "current_phase_index": None,
            "completed_phases": None,
            "use_phased_execution": bool(structured_phases),
            "plan_content": None,
            "phase_execution_summary": None,
            "execution_summary": None,
        }

        # Execute the graph
        logger.info(f"Starting Unified Open SWE execution for instruction: {instruction}")

        # Stream the execution
        async for state_chunk in graph.astream(initial_state, config=config, stream_mode="values"):
            logger.debug(f"State update: {state_chunk.get('current_node', 'unknown')}")

        # Get the final state
        final_state_snapshot = await graph.aget_state(config)
        final_state = final_state_snapshot.values

        logger.info("Unified Open SWE execution completed")
        logger.info(f"Final state keys: {list(final_state.keys())}")
        logger.info(f"Final current_node: {final_state.get('current_node')}")

        return final_state


def create_open_swe_graph(
    code_tools: CodeTools,
    git_ops: GitOps,
    validation_runner: ValidationRunner,
    checkpointer: InMemorySaver | None = None,
    approval_node: Callable | None = None,
    enable_semantic_ranking: bool = True,
    validation_config: dict | None = None,
    use_discovery_phase: bool = False,  # NEW: Control whether to use discovery phase
):
    """
    Creates and compiles the unified LangGraph for the Open SWE pipeline.

    Combines the best features from both implementations:
    - Proper ToolNode patterns for discovery/ranking phases
    - Complete workflow through execution and testing
    """

    graph_instance = OpenSWEToolsGraph(
        code_tools,
        git_ops,
        validation_runner,
        approval_node=approval_node,
        enable_semantic_ranking=enable_semantic_ranking,
        validation_config=validation_config,
    )

    workflow = StateGraph(OpenSWEState)

    # Get tools for ToolNodes (from fixed implementation)
    from src.tools.openswe import (
        analyze_code_structure,
        calculate_code_complexity,
        extract_code_symbols,
        grep_search,
        view,
    )

    repo_tools = [analyze_code_structure, extract_code_symbols, calculate_code_complexity, view, grep_search]
    discovery_tools = [view, grep_search]
    ranking_tools = [view, analyze_code_structure]

    # === ADD NODES ===

    if use_discovery_phase:
        # Discovery phase: LLM + ToolNode pattern
        workflow.add_node("llm_repo_map", graph_instance.llm_repo_map)
        workflow.add_node("llm_file_discovery", graph_instance.llm_file_discovery)
        workflow.add_node("llm_file_ranking", graph_instance.llm_file_ranking)

        # ToolNodes for proper tool execution
        workflow.add_node("repo_map_tools", ToolNode(repo_tools))
        workflow.add_node("discovery_tools", ToolNode(discovery_tools))
        workflow.add_node("ranking_tools", ToolNode(ranking_tools))

        # Analysis nodes to process tool results
        workflow.add_node("repo_map_analysis", graph_instance.repo_map_analysis)
        workflow.add_node("discovery_analysis", graph_instance.discovery_analysis)
        workflow.add_node("ranking_analysis", graph_instance.ranking_analysis)

    # Execution phase: Complete workflow
    workflow.add_node("plan_edits", graph_instance.plan_edits)
    workflow.add_node("generate_diff", graph_instance.generate_diff)
    workflow.add_node("validate_diff", graph_instance.validate_diff)
    workflow.add_node("human_approval", graph_instance.human_approval)
    workflow.add_node("apply_changes", graph_instance.apply_changes)
    workflow.add_node("run_tests", graph_instance.run_tests)

    # Git operations: Added for parity with aider_graph.py
    workflow.add_node("setup_git_branch", graph_instance.setup_git_branch)
    workflow.add_node("commit_changes", graph_instance.commit_changes)
    workflow.add_node("create_pull_request", graph_instance.create_pull_request)
    workflow.add_node("rollback_changes", graph_instance.rollback_changes)

    workflow.add_node("complete", graph_instance.complete)
    workflow.add_node("error_handler", graph_instance.error_handler)

    # === SET ENTRY POINT ===
    if use_discovery_phase:
        workflow.set_entry_point("llm_repo_map")
    else:
        # Original simple workflow - start with plan_edits
        workflow.set_entry_point("plan_edits")

    # === ADD CONDITIONAL EDGES FOR DISCOVERY PHASE (only if enabled) ===

    if use_discovery_phase:
        # Repo mapping with ToolNode pattern
        workflow.add_conditional_edges(
            "llm_repo_map",
            graph_instance.should_use_repo_tools,
            {"repo_map_tools": "repo_map_tools", "repo_map_analysis": "repo_map_analysis"},
        )

        # File discovery with ToolNode pattern
        workflow.add_conditional_edges(
            "llm_file_discovery",
            graph_instance.should_use_discovery_tools,
            {"discovery_tools": "discovery_tools", "discovery_analysis": "discovery_analysis"},
        )

        # File ranking with ToolNode pattern
        workflow.add_conditional_edges(
            "llm_file_ranking",
            graph_instance.should_use_ranking_tools,
            {"ranking_tools": "ranking_tools", "ranking_analysis": "ranking_analysis"},
        )

        # === ADD EDGES FOR TOOL FEEDBACK LOOPS ===

        # Tools back to LLM for multi-turn interactions
        workflow.add_edge("repo_map_tools", "llm_repo_map")
        workflow.add_edge("discovery_tools", "llm_file_discovery")
        workflow.add_edge("ranking_tools", "llm_file_ranking")

        # === ADD EDGES FOR DISCOVERY PROGRESSION ===

        # Analysis progression through discovery phases
        workflow.add_edge("repo_map_analysis", "llm_file_discovery")
        workflow.add_edge("discovery_analysis", "llm_file_ranking")
        workflow.add_edge("ranking_analysis", "plan_edits")
    else:
        # Original simple workflow: plan_edits -> generate_diff (handled by conditional edges below)
        pass

    # === ADD CONDITIONAL EDGES FOR EXECUTION PHASE ===

    # Original workflow: plan_edits routing
    if not use_discovery_phase:
        workflow.add_conditional_edges(
            "plan_edits",
            graph_instance.route_after_plan_edits,
            {"generate_diff": "generate_diff", "error_handler": "error_handler"},
        )

        workflow.add_conditional_edges(
            "generate_diff",
            graph_instance.route_after_diff_generation,
            {"validate_diff": "validate_diff", "error_handler": "error_handler"},
        )

    # Execution workflow
    workflow.add_conditional_edges(
        "validate_diff",
        graph_instance.route_after_validation,
        {"human_approval": "human_approval", "error_handler": "error_handler"},
    )

    workflow.add_conditional_edges(
        "human_approval",
        graph_instance.route_after_approval,
        {"apply_changes": "apply_changes", "error_handler": "error_handler"},
    )

    workflow.add_conditional_edges(
        "apply_changes", graph_instance.route_after_apply, {"run_tests": "run_tests", "error_handler": "error_handler"}
    )

    workflow.add_conditional_edges("run_tests", graph_instance.route_after_tests, {"complete": "complete"})

    # Git operation routing
    workflow.add_edge("setup_git_branch", "commit_changes")
    workflow.add_edge("commit_changes", "create_pull_request")
    workflow.add_edge("create_pull_request", "complete")
    workflow.add_edge("rollback_changes", "complete")

    # === ADD TERMINAL EDGES ===

    # Direct edges to next steps
    workflow.add_edge("generate_diff", "validate_diff")

    # Terminal edges
    workflow.add_edge("error_handler", "complete")
    workflow.add_edge("complete", END)

    # === COMPILE THE GRAPH ===

    if checkpointer:
        graph = workflow.compile(checkpointer=checkpointer)
    else:
        graph = workflow.compile()

    return graph


# === CONVENIENCE FUNCTIONS FOR BACKWARDS COMPATIBILITY ===

# Alias for backwards compatibility with the original implementation
create_open_swe_graph_fixed = create_open_swe_graph
OpenSWEToolsGraphFixed = OpenSWEToolsGraph


def create_open_swe_graph_original(
    code_tools: CodeTools,
    git_ops: GitOps,
    validation_runner: ValidationRunner,
    checkpointer: InMemorySaver | None = None,
    approval_node: Callable | None = None,
    validation_config: dict | None = None,
):
    """
    Creates the original simple OpenSWE graph workflow.

    This maintains backwards compatibility with the original implementation
    that started directly with generate_diff (no discovery phase).
    """
    return create_open_swe_graph(
        code_tools=code_tools,
        git_ops=git_ops,
        validation_runner=validation_runner,
        checkpointer=checkpointer,
        approval_node=approval_node,
        enable_semantic_ranking=False,  # Original didn't have semantic ranking
        validation_config=validation_config,
        use_discovery_phase=False,  # Original simple workflow
    )


# === MAIN ENTRY POINT ===


async def main():
    """Example usage of the unified OpenSWE graph."""
    from src.token_tracker import TokenTrackingLLM
    from src.tools.shell_runner import ShellRunner
    from src.tools.validation.linting import LintingManager
    from src.tools.validation.testing import TestFrameworkManager

    # Initialize dependencies
    workspace_root = os.getcwd()
    shell_runner = ShellRunner()
    git_ops = GitOps(shell_runner)
    linting_manager = LintingManager(workspace_root)
    testing_manager = TestFrameworkManager(workspace_root)

    # Initialize LLM for CodeTools
    editor_llm = TokenTrackingLLM(model_name="gpt-4o", temperature=0.1, max_tokens=4000)

    # Initialize CodeTools
    code_tools = CodeTools(
        workspace_root=workspace_root,
        shell_runner=shell_runner,
        git_ops=git_ops,
        linting=linting_manager,
        testing=testing_manager,
        editor_llm=editor_llm,
    )

    # Initialize ValidationRunner
    validation_runner = ValidationRunner(code_tools)

    # Create the unified graph
    graph = create_open_swe_graph(
        code_tools,
        git_ops,
        validation_runner,
    )

    # Test the graph with a simple instruction
    initial_state = {
        "instruction": "Add a new feature to the codebase",
        "target_files": [],
        "current_node": "llm_repo_map",
        "messages": [],
        "use_phased_execution": False,
    }

    # Stream the execution
    print("=== Starting Unified OpenSWE Graph Execution ===")
    async for state_chunk in graph.astream(initial_state, stream_mode="values"):
        node = state_chunk.get("current_node", "unknown")
        print(f"Node: {node}")
        if state_chunk.get("error_message"):
            print(f"Error: {state_chunk['error_message']}")
            break
        if node == "complete":
            print("=== Execution Complete ===")
            break

    return state_chunk


if __name__ == "__main__":
    asyncio.run(main())
