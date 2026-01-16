"""
Run Tests Command Implementation

This module provides programmatic access to the run_tests command
functionality as a LangChain tool, implementing the actual logic from
.cursor/commands/run_tests.md
"""

import asyncio
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
async def run_tests(test_pattern: str | None = None, test_type: str = "all") -> str:
    """
    Run tests for the codebase with optional filtering.
    This implements the actual run_tests command logic from .cursor/commands/run_tests.md

    Args:
        test_pattern: Optional pattern to filter tests (e.g., "test_auth*")
        test_type: Type of tests to run (all, unit, integration, e2e)

    Returns:
        Test execution results and status
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

        # Phase 1: Test Discovery
        test_discovery = await _discover_tests(test_pattern, test_type, code_analyzer, shell_runner, workspace_root)

        # Phase 2: Test Execution
        test_results = await _execute_tests(test_discovery, shell_runner)

        # Phase 3: Results Analysis
        analysis_results = await _analyze_test_results(test_results, shell_runner)

        # Phase 4: Reporting
        test_report = await _create_test_report(test_pattern, test_type, test_discovery, test_results, analysis_results)

        return test_report

    except Exception as e:
        logger.error(f"Run tests command failed: {e}")
        return f"Test execution failed: {str(e)}"


async def _discover_tests(
    test_pattern: str | None, test_type: str, code_analyzer, shell_runner, workspace_root: str
) -> dict[str, Any]:
    """Discover tests with intelligent selection."""
    try:
        # Initialize intelligent selector for change-based types
        if test_type in ["changes", "quick"]:
            from src.tools.git_ops import GitOps
            from src.tools.test_selector import IntelligentTestSelector

            git_ops = GitOps(shell_runner)
            selector = IntelligentTestSelector(git_ops)

            # Get test files based on type
            if test_type == "changes":
                # Select tests based on code changes
                test_files = selector.select_tests_for_changes(max_tests=15)
            elif test_type == "quick":
                # Quick selection with intelligent prioritization
                test_files = selector.select_tests_for_changes(max_tests=8)
        else:
            # Standard discovery with pattern matching
            test_files = _discover_tests_by_pattern(test_pattern, test_type, workspace_root)["test_files"]

        # Apply pattern filter if provided
        if test_pattern:
            filtered_files = []
            for test_file in test_files:
                if re.search(test_pattern, test_file):
                    filtered_files.append(test_file)
            test_files = filtered_files

        return {
            "test_files": test_files,
            "total_count": len(test_files),
            "pattern": test_pattern,
            "type": test_type,
            "selection_method": "intelligent" if test_type in ["changes", "quick"] else "standard",
        }
    except Exception as e:
        logger.warning(f"Intelligent test discovery failed: {e}")
        # Fallback to basic discovery
        return _discover_tests_by_pattern(test_pattern, test_type, workspace_root)


def _discover_tests_by_pattern(test_pattern: str | None, test_type: str, workspace_root: str) -> dict[str, Any]:
    """Basic pattern-based test discovery as fallback."""

    test_files = []
    current_dir = Path(workspace_root)

    # Look for test files with proper patterns and exclude cache/build directories
    for py_file in current_dir.glob("test_*.py"):
        if not any(part.startswith(".") for part in py_file.parts):
            test_files.append(str(py_file))

    # Also check tests/ directory if it exists
    tests_dir = current_dir / "tests"
    if tests_dir.exists():
        for py_file in tests_dir.rglob("test_*.py"):
            if not any(part.startswith(".") for part in py_file.parts):
                test_files.append(str(py_file))
        for py_file in tests_dir.rglob("*_test.py"):
            if not any(part.startswith(".") for part in py_file.parts):
                test_files.append(str(py_file))

    # Remove duplicates and sort
    test_files = sorted(list(set(test_files)))

    # Apply type-based filtering
    if test_type == "quick":
        # Legacy quick test selection
        test_files = [
            f
            for f in test_files
            if any(pattern in f for pattern in ["test_phase9_1", "test_phase9_2", "test_validation", "test_connection"])
        ][:4]  # Limit to 4 test files max
    elif test_type == "unit":
        test_files = [f for f in test_files if "unit" in f.lower() or "test_" in f.lower()]
    elif test_type == "integration":
        test_files = [f for f in test_files if "integration" in f.lower()]
    elif test_type == "e2e":
        test_files = [f for f in test_files if "e2e" in f.lower() or "end_to_end" in f.lower()]

    return {
        "test_files": test_files,
        "total_count": len(test_files),
        "pattern": test_pattern,
        "type": test_type,
        "selection_method": "basic",
    }


async def _execute_tests(test_discovery: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Execute the discovered tests with proper timeout handling."""
    try:
        test_files = test_discovery.get("test_files", [])
        test_type = test_discovery.get("type", "all")

        if not test_files:
            return {"status": "NO_TESTS", "output": "No test files found matching criteria"}

        # Execute tests with timeout
        results = await _execute_tests_with_timeout(test_files, shell_runner, timeout=300)

        return results
    except Exception as e:
        logger.warning(f"Test execution failed: {e}")
        return {"error": f"Test execution failed: {str(e)}"}


async def _execute_tests_with_timeout(test_files: list[str], shell_runner, timeout: int = 300) -> dict[str, Any]:
    """Execute tests with timeout handling to prevent hanging."""
    results = {}

    # Check test framework availability first
    pytest_available = await _check_pytest_available(shell_runner)

    if pytest_available:
        # Try pytest
        pytest_cmd = f"python -m pytest {' '.join(test_files)} -v --tb=short --no-header"

        try:
            pytest_result = await asyncio.wait_for(_run_subprocess_command(pytest_cmd, shell_runner), timeout=timeout)
            results["pytest"] = {
                "exit_code": pytest_result.exit_code,
                "stdout": pytest_result.stdout,
                "stderr": pytest_result.stderr,
                "timed_out": False,
                "framework": "pytest",
            }
            return results
        except TimeoutError:
            results["pytest"] = {
                "exit_code": 124,  # Standard timeout exit code
                "stdout": "",
                "stderr": f"Test execution timed out after {timeout} seconds",
                "timed_out": True,
                "framework": "pytest",
            }
            return results
        except Exception as e:
            logger.warning(f"pytest failed: {e}, falling back to unittest")

    # Use unittest as fallback (or primary if pytest not available)
    unittest_cmd = "python -m unittest discover -s . -p 'test_*.py' -v"
    try:
        unittest_result = await asyncio.wait_for(_run_subprocess_command(unittest_cmd, shell_runner), timeout=timeout)
        results["unittest"] = {
            "exit_code": unittest_result.exit_code,
            "stdout": unittest_result.stdout,
            "stderr": unittest_result.stderr,
            "timed_out": False,
            "framework": "unittest",
        }
    except TimeoutError:
        results["unittest"] = {
            "exit_code": 124,
            "stdout": "",
            "stderr": f"Test execution timed out after {timeout} seconds",
            "timed_out": True,
            "framework": "unittest",
        }
    except Exception:
        # Final fallback: direct Python execution of test files
        results["direct"] = await _execute_tests_directly(test_files, shell_runner, timeout)

    return results


async def _check_pytest_available(shell_runner) -> bool:
    """Check if pytest is available in the environment."""
    try:
        check_result = await asyncio.wait_for(
            _run_subprocess_command("python -c 'import pytest; print(pytest.__version__)'", shell_runner), timeout=5
        )
        return check_result.exit_code == 0
    except:
        return False


async def _execute_tests_directly(test_files: list[str], shell_runner, timeout: int) -> dict[str, Any]:
    """Direct execution of test files as last resort."""
    try:
        # Execute each test file individually with Python
        results = []
        for test_file in test_files[:5]:  # Limit to first 5 files to avoid hanging
            cmd = f"python {test_file}"
            try:
                result = await asyncio.wait_for(
                    _run_subprocess_command(cmd, shell_runner), timeout=timeout // len(test_files) or 30
                )
                results.append(f"{test_file}: {'PASSED' if result.exit_code == 0 else 'FAILED'}")
            except TimeoutError:
                results.append(f"{test_file}: TIMEOUT")

        return {
            "exit_code": 0,
            "stdout": "\n".join(results),
            "stderr": "Direct test file execution (fallback method)",
            "timed_out": False,
            "framework": "direct",
        }
    except Exception as e:
        return {
            "exit_code": 1,
            "stdout": "",
            "stderr": f"All test execution methods failed: {str(e)}",
            "timed_out": False,
            "framework": "failed",
        }


async def _run_subprocess_command(cmd: str, shell_runner):
    """Wrapper to make shell_runner.execute async-compatible."""
    return await asyncio.to_thread(shell_runner.execute, cmd)


async def _analyze_test_results(test_results: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Analyze test execution results."""
    try:
        analysis = {
            "overall_status": "UNKNOWN",
            "passed_tests": 0,
            "failed_tests": 0,
            "total_tests": 0,
            "coverage": "N/A",
        }

        # Analyze pytest results
        if "pytest" in test_results:
            pytest_output = test_results["pytest"]["stdout"]
            if "passed" in pytest_output.lower():
                analysis["overall_status"] = "PASSED"
            elif "failed" in pytest_output.lower():
                analysis["overall_status"] = "FAILED"

            # Extract test counts
            passed_match = re.search(r"(\d+) passed", pytest_output)
            failed_match = re.search(r"(\d+) failed", pytest_output)

            if passed_match:
                analysis["passed_tests"] = int(passed_match.group(1))
            if failed_match:
                analysis["failed_tests"] = int(failed_match.group(1))

            analysis["total_tests"] = analysis["passed_tests"] + analysis["failed_tests"]

        # Try to get coverage if available
        coverage_cmd = "python -m coverage report --show-missing 2>/dev/null || echo 'No coverage available'"
        coverage_result = shell_runner.execute(coverage_cmd)
        if coverage_result.exit_code == 0 and "No coverage available" not in coverage_result.stdout:
            analysis["coverage"] = coverage_result.stdout

        return analysis
    except Exception as e:
        logger.warning(f"Test analysis failed: {e}")
        return {"error": f"Test analysis failed: {str(e)}"}


async def _create_test_report(
    test_pattern: str | None,
    test_type: str,
    test_discovery: dict[str, Any],
    test_results: dict[str, Any],
    analysis_results: dict[str, Any],
) -> str:
    """Create the test execution report."""
    try:
        # Create test reports directory if it doesn't exist
        from src.config.artifact_root import get_test_reports_directory

        reports_dir = get_test_reports_directory()
        # Generate filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        safe_pattern = re.sub(r"[^\w.-]+", "_", test_pattern) if test_pattern else ""
        safe_pattern = safe_pattern.replace("/", "_").replace("\\", "_")
        pattern_suffix = f"_{safe_pattern}" if safe_pattern else ""
        type_suffix = f"_{test_type}" if test_type != "all" else ""
        filename = f"{timestamp}_test_report{pattern_suffix}{type_suffix}.md"
        filepath = reports_dir / filename

        # Get current branch
        from ..shell_runner import ShellRunner
        from src.workspace_context import get_workspace_root

        workspace_root = get_workspace_root() or "."
        shell_runner = ShellRunner(workspace_root)
        branch_result = shell_runner.execute("git branch --show-current")
        current_branch = branch_result.stdout.strip() if branch_result.exit_code == 0 else "unknown"

        # Create document content
        content = f"""# Test Execution Report

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC
**Repository**: cce-agent
**Branch**: {current_branch}
**Test Pattern**: {test_pattern or "All tests"}
**Test Type**: {test_type}

## Test Discovery

**Total Test Files Found**: {test_discovery.get("total_count", 0)}

### Test Files:
{chr(10).join(f"- {file}" for file in test_discovery.get("test_files", [])[:20])}

## Test Execution Results

### Overall Status: {analysis_results.get("overall_status", "UNKNOWN")}

**Passed Tests**: {analysis_results.get("passed_tests", 0)}
**Failed Tests**: {analysis_results.get("failed_tests", 0)}
**Total Tests**: {analysis_results.get("total_tests", 0)}

### Coverage
{analysis_results.get("coverage", "No coverage information available")}

## Detailed Results

### Pytest Results
```
{test_results.get("pytest", {}).get("stdout", "No pytest results")}
```

### Individual Test Results
"""

        # Add individual test results
        individual_results = test_results.get("individual", [])
        for result in individual_results[:10]:  # Limit to first 10
            content += f"""
#### {result.get("file", "Unknown file")}
**Status**: {"PASSED" if result.get("exit_code") == 0 else "FAILED"}
**Output**: {result.get("stdout", "No output")[:500]}...
"""

        content += f"""
## Summary

- **Test Pattern**: {test_pattern or "All tests"}
- **Test Type**: {test_type}
- **Files Tested**: {test_discovery.get("total_count", 0)}
- **Overall Status**: {analysis_results.get("overall_status", "UNKNOWN")}
- **Pass Rate**: {(analysis_results.get("passed_tests", 0) / max(analysis_results.get("total_tests", 1), 1) * 100):.1f}%

## Recommendations

1. **Review Failed Tests**: Address any failing tests identified in the results
2. **Improve Coverage**: Consider adding tests for uncovered code areas
3. **Test Organization**: Ensure tests are properly organized and named
4. **Continuous Integration**: Set up automated test execution in CI/CD pipeline

## References

- **Test Report**: `{filepath}`
- **Test execution performed on**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Branch**: {current_branch}
"""

        # Write document
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)

        return f"Test execution completed. Report created at: {filepath}\n\n{content}"

    except Exception as e:
        logger.error(f"Failed to create test report: {e}")
        return f"Test execution completed but failed to create report: {str(e)}"
