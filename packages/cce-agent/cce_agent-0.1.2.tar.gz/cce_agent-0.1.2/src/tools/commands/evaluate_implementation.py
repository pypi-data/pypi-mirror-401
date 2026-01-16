"""
Evaluate Implementation Command Implementation

This module provides programmatic access to the evaluate_implementation command
functionality as a LangChain tool, implementing the actual logic from
.cursor/commands/evaluate_implementation.md
"""

import asyncio
import logging
import re
from datetime import datetime
from typing import Any

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
async def evaluate_implementation(github_ticket_url: str | None = None, context: str | None = None) -> str:
    """
    Evaluate an implementation against a GitHub ticket or requirements.
    This implements the actual evaluate_implementation command logic from
    .cursor/commands/evaluate_implementation.md

    Args:
        github_ticket_url: The GitHub ticket URL or issue number to evaluate against
        context: Any specific areas of concern or focus for the evaluation

    Returns:
        Evaluation results and recommendations
    """
    try:
        # Import here to avoid circular imports
        from ..code_analyzer import CodeAnalyzer
        from ..shell_runner import ShellRunner
        from src.workspace_context import get_workspace_root

        # Initialize required services
        workspace_root = get_workspace_root() or "."
        shell_runner = ShellRunner(workspace_root)
        code_analyzer = CodeAnalyzer(shell_runner)

        # Phase 1: Context Analysis
        ticket_analysis = await _analyze_github_ticket(github_ticket_url, shell_runner)

        # Phase 2: Implementation Analysis
        implementation_analysis = await _analyze_implementation(ticket_analysis, code_analyzer)

        # Phase 3: Testing and Validation
        testing_results = await _run_evaluation_tests(implementation_analysis, shell_runner)

        # Phase 4: Documentation and Reporting
        evaluation_report = await _create_evaluation_report(
            github_ticket_url, context, ticket_analysis, implementation_analysis, testing_results
        )

        return evaluation_report

    except Exception as e:
        logger.error(f"Evaluate implementation command failed: {e}")
        return f"Evaluation failed: {str(e)}"


async def _analyze_github_ticket(github_ticket_url: str | None, shell_runner) -> dict[str, Any]:
    """Analyze GitHub ticket if provided."""
    try:
        if not github_ticket_url:
            return {"valid": False, "content": "No GitHub ticket provided"}

        # Extract issue number or URL
        issue_match = re.search(r"#(\d+)", github_ticket_url)
        url_match = re.search(r"github\.com/([^/]+)/([^/]+)/issues/(\d+)", github_ticket_url)

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
                        return {"valid": True, "content": result.stdout, "issue_number": issue_number}

        elif url_match:
            owner, repo, issue_number = url_match.groups()
            cmd = f"gh issue view {issue_number} --repo {owner}/{repo}"
            result = shell_runner.execute(cmd)
            if result.exit_code == 0:
                return {"valid": True, "content": result.stdout, "issue_number": issue_number}

        return {"valid": False, "content": "Failed to fetch GitHub ticket"}
    except Exception as e:
        logger.warning(f"GitHub ticket analysis failed: {e}")
        return {"valid": False, "content": f"GitHub ticket analysis failed: {str(e)}"}


async def _analyze_implementation(ticket_analysis: dict[str, Any], code_analyzer) -> dict[str, Any]:
    """Analyze the current implementation."""
    try:
        # Get current codebase state
        current_files = code_analyzer.list_files(".")

        # Look for recent changes
        git_log = code_analyzer.shell.execute("git log --oneline -10")
        recent_commits = git_log.stdout if git_log.exit_code == 0 else "No recent commits found"

        # Check for test files
        test_files = []
        for line in current_files.split("\n"):
            if "test" in line.lower() and line.strip():
                test_files.append(line.strip())

        return {
            "current_files": current_files[:20],  # First 20 files
            "recent_commits": recent_commits,
            "test_files": test_files[:10],  # First 10 test files
        }
    except Exception as e:
        logger.warning(f"Implementation analysis failed: {e}")
        return {"error": f"Implementation analysis failed: {str(e)}"}


async def _run_evaluation_tests(implementation_analysis: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Run evaluation tests."""
    try:
        # Run linting
        lint_result = shell_runner.execute(
            "python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics"
        )
        lint_status = "PASSED" if lint_result.exit_code == 0 else "FAILED"

        # Run actual tests with timeout - check pytest availability first
        pytest_available = await _check_pytest_available(shell_runner)

        if pytest_available:
            test_cmd = "python -m pytest --tb=short -q"
        else:
            test_cmd = "python -m unittest discover -s . -p 'test_*.py' -q"

        try:
            test_result = await asyncio.wait_for(
                asyncio.to_thread(shell_runner.execute, test_cmd),
                timeout=180,  # 3 minute timeout for evaluation tests
            )
            test_status = "PASSED" if test_result.exit_code == 0 else "FAILED"
            test_output = test_result.stdout
            framework_used = "pytest" if pytest_available else "unittest"
            test_output = f"[{framework_used}] {test_output}"
        except TimeoutError:
            test_status = "TIMEOUT"
            test_output = "Test execution timed out after 3 minutes"
        except Exception as e:
            test_status = "ERROR"
            test_output = f"Test execution error: {str(e)}"

        return {
            "linting": {"status": lint_status, "output": lint_result.stdout},
            "testing": {"status": test_status, "output": test_output},
        }
    except Exception as e:
        logger.warning(f"Evaluation tests failed: {e}")
        return {"error": f"Evaluation tests failed: {str(e)}"}


async def _check_pytest_available(shell_runner) -> bool:
    """Check if pytest is available in the environment."""
    try:
        check_result = await asyncio.wait_for(
            asyncio.to_thread(shell_runner.execute, "python -c 'import pytest; print(pytest.__version__)'"), timeout=5
        )
        return check_result.exit_code == 0
    except:
        return False


async def _create_evaluation_report(
    github_ticket_url: str | None,
    context: str | None,
    ticket_analysis: dict[str, Any],
    implementation_analysis: dict[str, Any],
    testing_results: dict[str, Any],
) -> str:
    """Create the evaluation report."""
    try:
        # Create evaluations directory if it doesn't exist
        from src.config.artifact_root import get_evaluations_directory

        evaluations_dir = get_evaluations_directory()
        # Generate filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")  # Include time for uniqueness
        issue_num = ticket_analysis.get("issue_number", "unknown")
        filename = f"{timestamp}_evaluation_issue_{issue_num}.md"
        filepath = evaluations_dir / filename

        # Get current branch
        from ..shell_runner import ShellRunner

        from src.workspace_context import get_workspace_root

        workspace_root = get_workspace_root() or "."
        shell_runner = ShellRunner(workspace_root)
        branch_result = shell_runner.execute("git branch --show-current")
        current_branch = branch_result.stdout.strip() if branch_result.exit_code == 0 else "unknown"

        # Create document content
        content = f"""# Implementation Evaluation

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC
**Repository**: cce-agent
**Branch**: {current_branch}
**GitHub Ticket**: {github_ticket_url or "Not provided"}

## Evaluation Context
{context or "No specific context provided"}

## GitHub Ticket Analysis
{ticket_analysis.get("content", "No ticket analysis available")}

## Implementation Analysis

### Current Codebase State
{implementation_analysis.get("current_files", "No file analysis available")}

### Recent Changes
{implementation_analysis.get("recent_commits", "No recent commits found")}

### Test Coverage
{implementation_analysis.get("test_files", "No test files found")}

## Testing Results

### Linting
**Status**: {testing_results.get("linting", {}).get("status", "UNKNOWN")}
**Output**: {testing_results.get("linting", {}).get("output", "No linting output")}

### Testing
**Status**: {testing_results.get("testing", {}).get("status", "UNKNOWN")}
**Output**: {testing_results.get("testing", {}).get("output", "No testing output")}

## Evaluation Summary

### Automated Verification
- [ ] Linting passes without critical errors
- [ ] Tests pass with adequate coverage
- [ ] No regressions in existing functionality
- [ ] Code follows project standards

### Manual Verification
- [ ] Implementation matches ticket requirements
- [ ] Feature works as expected when tested
- [ ] Performance is acceptable
- [ ] Documentation is updated
- [ ] Edge cases are handled appropriately

## Recommendations

Based on the evaluation:

1. **Code Quality**: Review linting results and address any critical issues
2. **Testing**: Ensure adequate test coverage for new functionality
3. **Documentation**: Update documentation to reflect changes
4. **Integration**: Verify integration with existing systems

## Next Steps

1. Address any critical issues identified in the evaluation
2. Run additional tests if needed
3. Update documentation as required
4. Prepare for deployment if all criteria are met

## References

- **Evaluation Document**: `{filepath}`
- **GitHub Ticket**: {github_ticket_url or "Not provided"}
- **Evaluation performed on**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

        # Write document
        with open(filepath, "w") as f:
            f.write(content)

        return f"Evaluation completed. Report created at: {filepath}\n\n{content}"

    except Exception as e:
        logger.error(f"Failed to create evaluation report: {e}")
        return f"Evaluation completed but failed to create report: {str(e)}"
