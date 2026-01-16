"""
Validation Tools for Deep Agents

This module provides validation, testing, and linting tools for the deep agent
by leveraging the existing CCE validation infrastructure.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field

# from langgraph.prebuilt import InjectedState  # Removed to avoid Pydantic schema issues

logger = logging.getLogger(__name__)


# Pydantic schemas for validation tools
class ValidateCodeInput(BaseModel):
    """Input schema for validate_code tool."""

    files: list[str] | None = Field(
        default=None, description="Optional list of file paths to validate (defaults to all files)"
    )
    include_tests: bool = Field(default=True, description="Whether to include test execution")


class RunLintingInput(BaseModel):
    """Input schema for run_linting tool."""

    files: list[str] | None = Field(
        default=None, description="Optional list of file paths to lint (defaults to all files)"
    )


class RunTestsInput(BaseModel):
    """Input schema for run_tests tool."""

    test_command: str | None = Field(
        default=None, description="Optional specific test command to run (e.g., 'pytest tests/')"
    )


class CheckSyntaxInput(BaseModel):
    """Input schema for check_syntax tool."""

    files: list[str] | None = Field(
        default=None, description="Optional list of file paths to check (defaults to all files)"
    )


# Import existing validation infrastructure
try:
    from ...tools.git_ops import GitOps
    from ...tools.openswe.code_tools import CodeTools
    from ...tools.shell_runner import ShellRunner
    from ...tools.validation.linting import LintingManager
    from ...tools.validation.testing import FrameworkTestManager
    from ...tools.validation_pipeline import get_validation_pipeline

    VALIDATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Validation tools not available: {e}")
    VALIDATION_AVAILABLE = False


def get_code_tools_instance(workspace_root: str) -> Any | None:
    """Get a CodeTools instance for validation operations."""
    if not VALIDATION_AVAILABLE:
        return None
    resolved_root = _resolve_workspace_root(workspace_root)
    try:
        shell_runner = ShellRunner(resolved_root)
        git_ops = GitOps(shell_runner)
        linting = LintingManager(resolved_root)
        testing = FrameworkTestManager(resolved_root)
        editor_llm = _build_validation_llm()
        if editor_llm is None:
            logger.warning("Validation LLM not configured; cannot initialize CodeTools.")
            return None

        return CodeTools(
            workspace_root=resolved_root,
            shell_runner=shell_runner,
            git_ops=git_ops,
            linting=linting,
            testing=testing,
            editor_llm=editor_llm,
        )
    except Exception as e:
        logger.error(f"Failed to create CodeTools instance: {e}")
        return None


def _resolve_workspace_root(workspace_root: str | None = None) -> str:
    if workspace_root:
        return os.path.abspath(workspace_root)
    try:
        from src.workspace_context import get_workspace_root

        stored_root = get_workspace_root()
        if stored_root:
            return os.path.abspath(stored_root)
    except Exception:
        pass
    return os.getcwd()


def _build_validation_llm() -> Any | None:
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if anthropic_key:
        try:
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                model=os.getenv("VALIDATION_MODEL_ANTHROPIC", "claude-3-haiku-20240307"),
                temperature=0,
                api_key=anthropic_key,
            )
        except Exception as exc:
            logger.warning("Failed to initialize Anthropic validation LLM: %s", exc)

    if openai_key:
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=os.getenv("VALIDATION_MODEL_OPENAI", "gpt-4o-mini"),
                temperature=0,
            )
        except Exception as exc:
            logger.warning("Failed to initialize OpenAI validation LLM: %s", exc)

    return None


def _format_test_run_details(result_metadata: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if not isinstance(result_metadata, dict):
        return lines

    command = result_metadata.get("command")
    if command:
        lines.append(f"- `{command}`")
        return lines

    detailed_results = result_metadata.get("detailed_results") or {}
    if not isinstance(detailed_results, dict):
        return lines

    for _, results in detailed_results.items():
        for result in results or []:
            if hasattr(result, "to_dict"):
                data = result.to_dict()
            elif isinstance(result, dict):
                data = result
            else:
                continue

            framework = data.get("framework", "unknown")
            command = data.get("command") or ""
            selected_tests = data.get("selected_tests") or []
            if command:
                line = f"- {framework}: `{command}`"
            else:
                line = f"- {framework}: (command unavailable)"
            if selected_tests:
                line += f" (selected: {', '.join(selected_tests)})"
            lines.append(line)

    return lines


def _format_suggested_test_plan(testing: FrameworkTestManager) -> list[str]:
    plan_entries = testing.suggest_test_plan()
    if not plan_entries:
        return ["- No test frameworks detected. Check project docs for recommended commands."]

    lines: list[str] = []
    for entry in plan_entries:
        command = entry.get("command") or ""
        selected_tests = entry.get("selected_tests") or []
        if command:
            line = f"- `{command}`"
        else:
            line = "- (command unavailable)"
        if selected_tests:
            line += f" (targets: {', '.join(selected_tests)})"
        lines.append(line)
    return lines


@tool(
    args_schema=ValidateCodeInput,
    description="Run comprehensive validation (linting + testing) on specified files with detailed error reporting",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
async def validate_code(files: list[str] | None = None, include_tests: bool = True) -> str:
    """
    Run comprehensive validation (linting + testing) on specified files.

    Args:
        files: Optional list of file paths to validate (defaults to all files)
        include_tests: Whether to include test execution

    Returns:
        Validation results summary
    """
    if not VALIDATION_AVAILABLE:
        return "❌ Validation tools not available - missing dependencies"

    try:
        workspace_root = _resolve_workspace_root()

        # Get CodeTools instance
        code_tools = get_code_tools_instance(workspace_root)
        if not code_tools:
            return "❌ Failed to initialize validation tools"

        import asyncio

        # Run linting
        logger.info(f"🔍 Running linting on files: {files or 'all'}")
        lint_result = await code_tools.lint(paths=files, response_format="detailed")

        # Run testing if requested
        test_result = None
        if include_tests:
            logger.info("🧪 Running tests...")
            test_result = await code_tools.test(response_format="detailed")

        # Format results
        result_parts = []

        # Linting results
        if lint_result.status == "success":
            result_parts.append("✅ **Linting**: Passed")
            if lint_result.metadata.get("total_issues", 0) > 0:
                result_parts.append(f"   📊 Issues found: {lint_result.metadata['total_issues']}")
        else:
            result_parts.append("❌ **Linting**: Failed")
            result_parts.append(f"   📊 Issues: {lint_result.metadata.get('total_issues', 0)}")

        # Testing results
        if test_result:
            if test_result.status == "success":
                result_parts.append("✅ **Testing**: Passed")
                result_parts.append(
                    f"   📊 Tests: {test_result.metadata.get('total_passed', 0)}/{test_result.metadata.get('total_tests', 0)} passed"
                )
            else:
                result_parts.append("❌ **Testing**: Failed")
                result_parts.append(
                    f"   📊 Tests: {test_result.metadata.get('total_passed', 0)}/{test_result.metadata.get('total_tests', 0)} passed"
                )

        # Overall status
        overall_success = lint_result.status == "success" and (not test_result or test_result.status == "success")
        status_emoji = "✅" if overall_success else "❌"

        return f"{status_emoji} **Validation Complete**\n\n" + "\n".join(result_parts)

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return f"❌ Validation failed: {str(e)}"


@tool(
    args_schema=RunLintingInput,
    description="Check code quality and style with linting tools for specified files",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
async def run_linting(files: list[str] | None = None) -> str:
    """
    Run linting on specified files to check code quality and style.

    Args:
        files: Optional list of file paths to lint (defaults to all files)

    Returns:
        Linting results summary
    """
    if not VALIDATION_AVAILABLE:
        return "❌ Linting tools not available - missing dependencies"

    try:
        workspace_root = _resolve_workspace_root()

        # Get CodeTools instance
        code_tools = get_code_tools_instance(workspace_root)
        if not code_tools:
            return "❌ Failed to initialize linting tools"

        import asyncio

        logger.info(f"🔍 Running linting on files: {files or 'all'}")

        # Handle async execution properly - check if we're in an event loop
        try:
            loop = asyncio.get_running_loop()
            # We're in an event loop, use create_task
            result = await code_tools.lint(paths=files, response_format="detailed")
        except RuntimeError:
            # No event loop running, use asyncio.run
            result = asyncio.run(code_tools.lint(paths=files, response_format="detailed"))

        if result.status == "success":
            issues_count = result.metadata.get("total_issues", 0)
            files_checked = result.metadata.get("total_files", 0)

            if issues_count == 0:
                return f"✅ **Linting Passed**\n\n📊 Checked {files_checked} files - No issues found!"
            else:
                return f"⚠️ **Linting Completed with Issues**\n\n📊 Checked {files_checked} files - {issues_count} issues found\n\n🔧 Consider fixing issues for better code quality"
        else:
            return f"❌ **Linting Failed**\n\n📊 Issues: {result.metadata.get('total_issues', 0)}\n\n🔧 Please review and fix linting errors"

    except Exception as e:
        logger.error(f"Linting failed: {e}")
        return f"❌ Linting failed: {str(e)}"


@tool(
    args_schema=RunTestsInput,
    description="Execute tests to verify functionality with customizable test commands",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
async def run_tests(test_command: str | None = None) -> str:
    """
    Run tests to verify code functionality.

    Args:
        test_command: Optional specific test command to run (e.g., "pytest tests/")

    Returns:
        Test results summary
    """
    if not VALIDATION_AVAILABLE:
        return "❌ Testing tools not available - missing dependencies"

    try:
        workspace_root = _resolve_workspace_root()

        # Get CodeTools instance
        code_tools = get_code_tools_instance(workspace_root)
        if not code_tools:
            return "❌ Failed to initialize testing tools"

        import asyncio

        logger.info(f"🧪 Running tests with command: {test_command or 'auto-detect'}")

        # SURGICAL FIX: Add timeout wrapper to prevent indefinite hangs
        # This allows the deep agents _execute_testing_phase retry mechanism to engage
        try:
            result = await asyncio.wait_for(
                code_tools.test(cmd=test_command, response_format="detailed"),
                timeout=300,  # 5 minute timeout for tool-level protection
            )
        except TimeoutError:
            logger.warning(f"⏰ Deep agents test execution timed out after 300 seconds")
            return f"⏰ **Test Execution Timed Out**\n\n📊 Test execution exceeded 300 second timeout limit.\nThis allows the retry mechanism to attempt different strategies."

        if result.status == "success":
            tests_run = result.metadata.get("total_tests", 0)
            tests_passed = result.metadata.get("total_passed", 0)
            tests_failed = result.metadata.get("total_failed", 0)
            tests_skipped = result.metadata.get("total_skipped", 0)

            if tests_run == 0:
                suggested = _format_suggested_test_plan(code_tools.testing)
                return (
                    "ℹ️ **No Tests Found**\n\n"
                    "📊 No tests were detected in the project\n\n"
                    "### Suggested Test Plan\n"
                    f"{chr(10).join(suggested)}"
                )
            elif tests_failed == 0:
                details = _format_test_run_details(result.metadata)
                details_block = ""
                if details:
                    details_block = f"\n\n### Tests Run\n{chr(10).join(details)}"
                return f"✅ **All Tests Passed**\n\n📊 {tests_passed}/{tests_run} tests passed{details_block}"
            else:
                details = _format_test_run_details(result.metadata)
                details_block = ""
                if details:
                    details_block = f"\n\n### Tests Run\n{chr(10).join(details)}"
                return (
                    f"❌ **Some Tests Failed**\n\n📊 {tests_passed}/{tests_run} tests passed, {tests_failed} failed"
                    f"{details_block}"
                )
        else:
            # IMPROVEMENT: Include detailed error information for better categorization
            error_details = []
            error_details.append(f"📊 Error: {result.result}")

            # Add stderr if it contains useful error information
            if result.metadata.get("stderr"):
                error_details.append("🔍 **Detailed Error Output:**")
                error_details.append(result.metadata["stderr"])

            # Add stdout if it contains useful information (like pytest collection errors)
            if result.metadata.get("stdout"):
                error_details.append("📝 **Test Output:**")
                error_details.append(result.metadata["stdout"])

            details = _format_test_run_details(result.metadata)
            if details:
                error_details.append("### Tests Run")
                error_details.extend(details)

            return f"❌ **Test Execution Failed**\n\n{chr(10).join(error_details)}"

    except Exception as e:
        logger.error(f"Testing failed: {e}")
        return f"❌ Testing failed: {str(e)}"


@tool(
    args_schema=CheckSyntaxInput,
    description="Quick syntax validation for specified files without full linting",
    infer_schema=False,  # Using explicit schema
    parse_docstring=False,
)
async def check_syntax(files: list[str] | None = None) -> str:
    """
    Check syntax of specified files without running full linting.

    Args:
        files: Optional list of file paths to check (defaults to all files)

    Returns:
        Syntax check results
    """
    if not VALIDATION_AVAILABLE:
        return "❌ Syntax checking tools not available - missing dependencies"

    try:
        workspace_root = _resolve_workspace_root()

        # Use validation pipeline for syntax checking
        import asyncio

        from ...tools.validation_pipeline import get_validation_pipeline

        pipeline = get_validation_pipeline()

        # Handle async execution properly - check if we're in an event loop
        try:
            loop = asyncio.get_running_loop()
            # We're in an event loop, use await
            result = await pipeline.validate_syntax(files or [])
        except RuntimeError:
            # No event loop running, use asyncio.run
            result = asyncio.run(pipeline.validate_syntax(files or []))

        if result.success:
            return f"✅ **Syntax Check Passed**\n\n📊 Checked {len(files or [])} files - No syntax errors found"
        else:
            error_count = len(result.get_issues_by_severity("error"))
            warning_count = len(result.get_issues_by_severity("warning"))

            return f"❌ **Syntax Check Failed**\n\n📊 Found {error_count} errors, {warning_count} warnings\n\n🔧 Please fix syntax errors before proceeding"

    except Exception as e:
        logger.error(f"Syntax checking failed: {e}")
        return f"❌ Syntax checking failed: {str(e)}"


# Export validation tools
VALIDATION_TOOLS = [validate_code, run_linting, run_tests, check_syntax]
