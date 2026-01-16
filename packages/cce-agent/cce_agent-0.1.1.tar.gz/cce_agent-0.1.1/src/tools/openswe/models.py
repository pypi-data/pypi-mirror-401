"""
Pydantic models for OpenSWE tools structured outputs.

This module defines structured output models for all OpenSWE tools to ensure
consistent, validated return types and better integration with LangGraph.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# --- Base Response Models ---


class BaseToolResponse(BaseModel):
    """Base response model for all OpenSWE tools."""

    model_config = ConfigDict(strict=True, extra="forbid")

    success: bool = Field(description="Whether the operation was successful")
    result: str = Field(description="Main result message or content")
    status: str = Field(description="Status: 'success' or 'error'")
    metadata: dict[str, Any] | None = Field(default=None, description="Additional metadata")
    error_code: str | None = Field(default=None, description="Error code if applicable")
    error_hint: str | None = Field(default=None, description="Actionable error guidance")


# --- TreeSitter Analysis Models ---


class CodeSymbol(BaseModel):
    """Represents a code symbol (function, class, variable, etc.)."""

    model_config = ConfigDict(strict=True, extra="forbid")

    name: str = Field(description="Name of the symbol")
    line_number: int = Field(description="Line number where symbol is defined")
    text: str = Field(description="Full text of the symbol definition")
    type: str = Field(description="Type of symbol (function, class, variable, etc.)")


class CodeAnalysisResult(BaseModel):
    """Result of code structure analysis."""

    model_config = ConfigDict(strict=True, extra="forbid")

    language: str = Field(description="Programming language detected")
    functions: list[CodeSymbol] = Field(description="List of functions found")
    classes: list[CodeSymbol] = Field(description="List of classes found")
    imports: list[CodeSymbol] = Field(description="List of imports found")
    variables: list[CodeSymbol] = Field(description="List of variables found")
    comments: list[str] = Field(description="List of comments found")
    ast_summary: str = Field(description="Summary of AST structure")
    complexity_score: float = Field(description="Code complexity score (0.0-1.0)")
    line_count: int = Field(description="Total number of lines")


class CodeAnalysisResponse(BaseToolResponse):
    """Response for code analysis operations."""

    analysis: CodeAnalysisResult | None = Field(default=None, description="Detailed analysis results")


class SymbolExtractionResult(BaseModel):
    """Result of symbol extraction operation."""

    symbols: list[CodeSymbol] = Field(description="List of extracted symbols")
    symbol_count: int = Field(description="Total number of symbols found")
    symbol_types: dict[str, int] = Field(description="Count of each symbol type")


class SymbolExtractionResponse(BaseToolResponse):
    """Response for symbol extraction operations."""

    extraction: SymbolExtractionResult | None = Field(default=None, description="Symbol extraction results")


class ComplexityMetrics(BaseModel):
    """Code complexity metrics."""

    cyclomatic_complexity: int = Field(description="Cyclomatic complexity score")
    cognitive_complexity: int = Field(description="Cognitive complexity score")
    nesting_depth: int = Field(description="Maximum nesting depth")
    function_count: int = Field(description="Number of functions")
    class_count: int = Field(description="Number of classes")
    line_count: int = Field(description="Total line count")
    comment_ratio: float = Field(description="Ratio of comments to code")


class ComplexityAnalysisResponse(BaseToolResponse):
    """Response for complexity analysis operations."""

    metrics: ComplexityMetrics | None = Field(default=None, description="Complexity metrics")


# --- File Operations Models ---


class PatchApplicationResult(BaseModel):
    """Result of patch application operation."""

    files_changed: list[str] = Field(description="List of files that were modified")
    lines_added: int = Field(description="Number of lines added")
    lines_removed: int = Field(description="Number of lines removed")
    conflicts: list[str] = Field(description="List of merge conflicts if any")
    method_used: str = Field(description="Method used for applying patch (git, manual, etc.)")


class PatchApplicationResponse(BaseToolResponse):
    """Response for patch application operations."""

    patch_result: PatchApplicationResult | None = Field(default=None, description="Patch application details")


class FileViewResult(BaseModel):
    """Result of file viewing operation."""

    content: str = Field(description="File or directory content")
    file_type: str = Field(description="Type: 'file' or 'directory'")
    size: int = Field(description="File size in bytes")
    line_count: int | None = Field(default=None, description="Number of lines (for files)")
    encoding: str = Field(description="File encoding")
    last_modified: datetime | None = Field(default=None, description="Last modification time")


class FileViewResponse(BaseToolResponse):
    """Response for file viewing operations."""

    view_result: FileViewResult | None = Field(default=None, description="File view details")


class TextEditResult(BaseModel):
    """Result of text editing operation."""

    operation: str = Field(description="Type of operation performed")
    lines_modified: int = Field(description="Number of lines modified")
    content_preview: str = Field(description="Preview of modified content")
    backup_created: bool = Field(description="Whether a backup was created")


class TextEditResponse(BaseToolResponse):
    """Response for text editing operations."""

    edit_result: TextEditResult | None = Field(default=None, description="Text editing details")


# --- Development Tools Models ---


class GrepSearchResult(BaseModel):
    """Result of grep search operation."""

    matches: list[dict[str, Any]] = Field(description="List of search matches")
    match_count: int = Field(description="Total number of matches found")
    files_searched: int = Field(description="Number of files searched")
    pattern: str = Field(description="Search pattern used")
    exit_code: int = Field(description="Exit code from grep command")


class GrepSearchResponse(BaseToolResponse):
    """Response for grep search operations."""

    search_result: GrepSearchResult | None = Field(default=None, description="Search results")


class InstallationResult(BaseModel):
    """Result of dependency installation operation."""

    packages_installed: list[str] = Field(description="List of packages installed")
    installation_time: float = Field(description="Installation time in seconds")
    output: str = Field(description="Installation output")
    warnings: list[str] = Field(description="Installation warnings")


class InstallationResponse(BaseToolResponse):
    """Response for installation operations."""

    installation: InstallationResult | None = Field(default=None, description="Installation details")


class ShellExecutionResult(BaseModel):
    """Result of shell command execution."""

    stdout: str = Field(description="Standard output")
    stderr: str = Field(description="Standard error")
    exit_code: int = Field(description="Exit code")
    execution_time: float = Field(description="Execution time in seconds")
    command: str = Field(description="Command that was executed")


class ShellExecutionResponse(BaseToolResponse):
    """Response for shell execution operations."""

    execution: ShellExecutionResult | None = Field(default=None, description="Execution details")


class SafetyEvaluationResult(BaseModel):
    """Result of command safety evaluation."""

    is_safe: bool = Field(description="Whether the command is considered safe")
    risk_level: str = Field(description="Risk level: low, medium, high, critical")
    concerns: list[str] = Field(description="List of safety concerns")
    recommendations: list[str] = Field(description="Safety recommendations")
    confidence: float = Field(description="Confidence score (0.0-1.0)")


class SafetyEvaluationResponse(BaseToolResponse):
    """Response for safety evaluation operations."""

    evaluation: SafetyEvaluationResult | None = Field(default=None, description="Safety evaluation details")


# --- Workflow Tools Models ---


class PlanItem(BaseModel):
    """Individual plan item."""

    id: str = Field(description="Unique identifier for the plan item")
    description: str = Field(description="Description of the plan item")
    status: str = Field(description="Status: pending, in_progress, completed, failed")
    priority: int = Field(description="Priority level (1-5)")


class SessionPlanResult(BaseModel):
    """Result of session plan creation."""

    plan_id: str = Field(description="Unique plan identifier")
    title: str = Field(description="Plan title")
    plan_items: list[PlanItem] = Field(description="List of plan items")
    reasoning: str = Field(description="Reasoning for the plan")
    created_at: datetime = Field(description="Plan creation timestamp")
    estimated_duration: str | None = Field(default=None, description="Estimated completion time")


class SessionPlanResponse(BaseToolResponse):
    """Response for session plan operations."""

    plan: SessionPlanResult | None = Field(default=None, description="Session plan details")


class PlanUpdateResult(BaseModel):
    """Result of plan update operation."""

    update_id: str = Field(description="Unique update identifier")
    plan_id: str = Field(description="Plan being updated")
    changes: list[str] = Field(description="List of changes made")
    reasoning: str = Field(description="Reasoning for the update")
    updated_at: datetime = Field(description="Update timestamp")


class PlanUpdateResponse(BaseToolResponse):
    """Response for plan update operations."""

    update: PlanUpdateResult | None = Field(default=None, description="Plan update details")


class TaskCompletionResult(BaseModel):
    """Result of task completion operation."""

    task_id: str = Field(description="Task identifier")
    summary: str = Field(description="Task completion summary")
    completed_at: datetime = Field(description="Completion timestamp")
    duration: float | None = Field(default=None, description="Task duration in seconds")
    artifacts: list[str] = Field(description="List of artifacts created")


class TaskCompletionResponse(BaseToolResponse):
    """Response for task completion operations."""

    completion: TaskCompletionResult | None = Field(default=None, description="Task completion details")


class ErrorDiagnosisResult(BaseModel):
    """Result of error diagnosis operation."""

    diagnosis_id: str = Field(description="Unique diagnosis identifier")
    error_type: str = Field(description="Type of error diagnosed")
    root_cause: str = Field(description="Identified root cause")
    symptoms: list[str] = Field(description="List of error symptoms")
    recommendations: list[str] = Field(description="List of recommended fixes")
    severity: str = Field(description="Error severity: low, medium, high, critical")


class ErrorDiagnosisResponse(BaseToolResponse):
    """Response for error diagnosis operations."""

    diagnosis: ErrorDiagnosisResult | None = Field(default=None, description="Error diagnosis details")


# --- Web Tools Models ---


class WebContentResult(BaseModel):
    """Result of web content retrieval."""

    url: str = Field(description="URL that was accessed")
    content: str = Field(description="Retrieved content")
    content_type: str = Field(description="Content type (text/html, text/plain, etc.)")
    status_code: int = Field(description="HTTP status code")
    response_time: float = Field(description="Response time in seconds")
    content_length: int = Field(description="Content length in bytes")


class WebContentResponse(BaseToolResponse):
    """Response for web content operations."""

    content_result: WebContentResult | None = Field(default=None, description="Web content details")


class DocumentSearchResult(BaseModel):
    """Result of document search operation."""

    query: str = Field(description="Search query used")
    matches: list[dict[str, Any]] = Field(description="List of search matches")
    match_count: int = Field(description="Number of matches found")
    search_time: float = Field(description="Search time in seconds")


class DocumentSearchResponse(BaseToolResponse):
    """Response for document search operations."""

    search_result: DocumentSearchResult | None = Field(default=None, description="Document search details")


# --- GitHub Tools Models ---


class GitHubOperationResult(BaseModel):
    """Result of GitHub operation."""

    operation_type: str = Field(description="Type of GitHub operation")
    github_id: str | None = Field(default=None, description="GitHub object ID")
    url: str | None = Field(default=None, description="GitHub URL")
    status: str = Field(description="Operation status")


class GitHubOperationResponse(BaseToolResponse):
    """Response for GitHub operations."""

    github_result: GitHubOperationResult | None = Field(default=None, description="GitHub operation details")


# --- HTTP Tools Models ---


class HTTPResponseResult(BaseModel):
    """Result of HTTP request operation."""

    url: str = Field(description="Requested URL")
    method: str = Field(description="HTTP method used")
    status_code: int = Field(description="HTTP status code")
    headers: dict[str, str] = Field(description="Response headers")
    body: str = Field(description="Response body")
    response_time: float = Field(description="Response time in seconds")


class HTTPResponse(BaseToolResponse):
    """Response for HTTP request operations."""

    http_result: HTTPResponseResult | None = Field(default=None, description="HTTP response details")


# --- Web Search Models ---


class SearchResult(BaseModel):
    """Individual search result."""

    title: str = Field(description="Result title")
    url: str = Field(description="Result URL")
    snippet: str = Field(description="Result snippet")
    relevance_score: float = Field(description="Relevance score (0.0-1.0)")


class WebSearchResult(BaseModel):
    """Result of web search operation."""

    query: str = Field(description="Search query")
    results: list[SearchResult] = Field(description="List of search results")
    total_results: int = Field(description="Total number of results")
    search_time: float = Field(description="Search time in seconds")


class WebSearchResponse(BaseToolResponse):
    """Response for web search operations."""

    search_result: WebSearchResult | None = Field(default=None, description="Web search details")
