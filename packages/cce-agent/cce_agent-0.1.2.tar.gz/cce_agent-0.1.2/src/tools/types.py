"""
Shared Pydantic models and TypedDicts for CCE Agent tools and graphs.
"""

from typing import Any, TypedDict

# --- AIDER Graph State ---


class AiderState(TypedDict):
    """
    State for the LangGraph AIDER pipeline.

    Contains paths to artifacts and status information, but not the
    artifacts themselves to keep the state object lightweight.
    """

    # Input parameters
    instruction: str
    target_files: list[str]

    # Artifact paths
    repo_map_path: str | None
    patch_preview_path: str | None

    # Status and control flow
    current_node: str
    error_message: str | None
    is_approved: bool

    # GitOps
    git_branch_name: str | None
    original_branch_name: str | None
    git_head_before_edit: str | None
    commit_hash: str | None
    commit_message: str | None

    # Pull Request
    pr_created: bool | None
    pr_url: str | None
    pr_message: str | None
    pr_error: str | None
    pr_creation_skipped: bool | None

    # Validation results
    lint_result_path: str | None
    test_result_path: str | None

    # RankTargets results
    ranked_files: list[dict] | None  # List of files with ranking scores and rationale

    # Phased Execution
    structured_phases: list[dict[str, Any]] | None  # Structured phases from planning
    parsed_phases: list[dict[str, Any]] | None  # Parsed phases for execution
    current_phase_index: int | None  # Current phase being executed
    completed_phases: list[dict[str, Any]] | None  # Completed phase results
    use_phased_execution: bool | None  # Whether to use phased execution
    plan_content: str | None  # Plan content for parsing (fallback)
    phase_execution_summary: str | None  # Summary of phased execution

    # CCE Command results
    research_codebase_result: str | None
    create_plan_result: str | None
    update_plan_result: str | None
    implement_plan_result: str | None
    evaluate_implementation_result: str | None
    address_evaluation_result: str | None
    run_tests_result: str | None
    commit_and_push_result: str | None

    # CCE Command errors
    research_codebase_error: str | None
    create_plan_error: str | None
    update_plan_error: str | None
    implement_plan_error: str | None
    evaluate_implementation_error: str | None
    address_evaluation_error: str | None
    run_tests_error: str | None
    commit_and_push_error: str | None
