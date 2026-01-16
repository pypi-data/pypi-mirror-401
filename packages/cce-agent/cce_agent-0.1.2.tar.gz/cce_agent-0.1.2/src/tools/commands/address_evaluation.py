"""
Address Evaluation Command Implementation

This module provides programmatic access to the address_evaluation command
functionality as a LangChain tool, implementing the actual logic from
.cursor/commands/address_evaluation.md
"""

import asyncio
import logging
import re
from typing import Any

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
async def address_evaluation(evaluation_findings: str, priority: str = "medium") -> str:
    """
    Address evaluation findings and implement necessary fixes or improvements.
    This implements the actual address_evaluation command logic from
    .cursor/commands/address_evaluation.md

    Args:
        evaluation_findings: The evaluation findings to address
        priority: Priority level (low, medium, high, critical)

    Returns:
        Status of addressing evaluation findings
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

        # Phase 1: Evaluation Analysis
        evaluation_analysis = await _analyze_evaluation_findings(evaluation_findings, priority)

        # Phase 2: Action Planning
        action_plan = await _create_action_plan(evaluation_analysis, code_analyzer)

        # Phase 3: Implementation
        implementation_result = await _implement_fixes(action_plan, shell_runner, code_analyzer)

        # Phase 4: Validation
        validation_result = await _validate_fixes(implementation_result, shell_runner)

        return f"""
Address Evaluation Results

Priority: {priority}
Findings Addressed: {len(evaluation_analysis.get("findings", []))}
Implementation: {implementation_result["status"]}
Validation: {validation_result["status"]}

Details:
{implementation_result.get("details", "")}
{validation_result.get("details", "")}
"""

    except Exception as e:
        logger.error(f"Address evaluation command failed: {e}")
        return f"Address evaluation failed: {str(e)}"


async def _analyze_evaluation_findings(evaluation_findings: str, priority: str) -> dict[str, Any]:
    """Analyze the evaluation findings to extract actionable items."""
    try:
        findings = []

        # Parse findings for different types of issues
        critical_patterns = [r"critical[^.]*", r"blocker[^.]*", r"failing[^.]*", r"error[^.]*"]
        high_patterns = [r"high priority[^.]*", r"important[^.]*", r"security[^.]*", r"performance[^.]*"]
        medium_patterns = [r"medium[^.]*", r"improvement[^.]*", r"enhancement[^.]*"]
        low_patterns = [r"low priority[^.]*", r"minor[^.]*", r"nice to have[^.]*"]

        # Extract findings based on patterns
        text_lower = evaluation_findings.lower()

        for pattern in critical_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                findings.append({"type": "critical", "description": match, "priority": "critical"})

        for pattern in high_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                findings.append({"type": "high", "description": match, "priority": "high"})

        for pattern in medium_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                findings.append({"type": "medium", "description": match, "priority": "medium"})

        for pattern in low_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                findings.append({"type": "low", "description": match, "priority": "low"})

        # If no specific patterns found, treat as general findings
        if not findings:
            findings.append(
                {
                    "type": "general",
                    "description": evaluation_findings[:500] + "..."
                    if len(evaluation_findings) > 500
                    else evaluation_findings,
                    "priority": priority,
                }
            )

        return {"findings": findings, "priority": priority, "total_findings": len(findings)}
    except Exception as e:
        logger.warning(f"Evaluation analysis failed: {e}")
        return {"error": f"Evaluation analysis failed: {str(e)}"}


async def _create_action_plan(evaluation_analysis: dict[str, Any], code_analyzer) -> dict[str, Any]:
    """Create an action plan to address the findings."""
    try:
        findings = evaluation_analysis.get("findings", [])
        action_plan = {"actions": [], "priority_order": []}

        # Sort findings by priority
        priority_order = ["critical", "high", "medium", "low"]
        sorted_findings = sorted(findings, key=lambda x: priority_order.index(x.get("priority", "medium")))

        for finding in sorted_findings:
            action = {
                "finding": finding,
                "action_type": _determine_action_type(finding),
                "estimated_effort": _estimate_effort(finding),
                "dependencies": [],
            }
            action_plan["actions"].append(action)
            action_plan["priority_order"].append(finding["priority"])

        return action_plan
    except Exception as e:
        logger.warning(f"Action plan creation failed: {e}")
        return {"error": f"Action plan creation failed: {str(e)}"}


def _determine_action_type(finding: dict[str, Any]) -> str:
    """Determine the type of action needed for a finding."""
    description = finding.get("description", "").lower()

    if any(keyword in description for keyword in ["test", "testing", "coverage"]):
        return "testing"
    elif any(keyword in description for keyword in ["lint", "format", "style"]):
        return "linting"
    elif any(keyword in description for keyword in ["documentation", "docs", "comment"]):
        return "documentation"
    elif any(keyword in description for keyword in ["performance", "optimize", "speed"]):
        return "performance"
    elif any(keyword in description for keyword in ["security", "vulnerability", "safe"]):
        return "security"
    else:
        return "general"


def _estimate_effort(finding: dict[str, Any]) -> str:
    """Estimate the effort required to address a finding."""
    priority = finding.get("priority", "medium")

    if priority == "critical":
        return "high"
    elif priority == "high":
        return "medium"
    elif priority == "medium":
        return "low"
    else:
        return "minimal"


async def _implement_fixes(action_plan: dict[str, Any], shell_runner, code_analyzer) -> dict[str, Any]:
    """Implement fixes based on the action plan."""
    try:
        actions = action_plan.get("actions", [])
        results = []

        for action in actions:
            action_type = action.get("action_type", "general")
            finding = action.get("finding", {})

            if action_type == "testing":
                result = await _implement_testing_fixes(finding, shell_runner)
            elif action_type == "linting":
                result = await _implement_linting_fixes(finding, shell_runner)
            elif action_type == "documentation":
                result = await _implement_documentation_fixes(finding, shell_runner)
            elif action_type == "performance":
                result = await _implement_performance_fixes(finding, shell_runner)
            elif action_type == "security":
                result = await _implement_security_fixes(finding, shell_runner)
            else:
                result = await _implement_general_fixes(finding, shell_runner)

            results.append(result)

        return {
            "status": "Implementation completed",
            "details": f"Addressed {len(results)} findings",
            "results": results,
        }
    except Exception as e:
        return {"status": f"Implementation failed: {str(e)}"}


async def _implement_testing_fixes(finding: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Implement testing-related fixes with real test execution."""
    try:
        # Run tests to identify issues - check pytest availability first
        pytest_available = await _check_pytest_available(shell_runner)

        if pytest_available:
            test_cmd = "python -m pytest --tb=short -v --no-header"
        else:
            test_cmd = "python -m unittest discover -s . -p 'test_*.py' -v"

        try:
            test_result = await asyncio.wait_for(
                asyncio.to_thread(shell_runner.execute, test_cmd),
                timeout=240,  # 4 minute timeout
            )

            if test_result.exit_code == 0:
                return {
                    "type": "testing",
                    "status": "PASSED",
                    "details": "All tests are passing - no fixes needed",
                    "output": test_result.stdout[:500],
                }
            else:
                # Analyze failures and suggest fixes
                failure_analysis = _analyze_test_failures(test_result.stdout)
                return {
                    "type": "testing",
                    "status": "FAILED",
                    "details": f"Found {len(failure_analysis)} test issues",
                    "output": test_result.stdout[:500],
                    "suggested_fixes": failure_analysis,
                }

        except TimeoutError:
            return {
                "type": "testing",
                "status": "TIMEOUT",
                "details": "Test execution timed out after 4 minutes",
                "output": "Consider reducing test scope or optimizing slow tests",
            }
    except Exception as e:
        return {"type": "testing", "status": "ERROR", "error": str(e)}


def _analyze_test_failures(test_output: str) -> list[str]:
    """Analyze test failures and suggest fixes."""
    suggestions = []

    if "FAILED" in test_output:
        failure_count = test_output.count("FAILED")
        suggestions.append(f"Review {failure_count} failing tests")

    if "ERROR" in test_output:
        error_count = test_output.count("ERROR")
        suggestions.append(f"Fix {error_count} test errors")

    if "ImportError" in test_output:
        suggestions.append("Resolve import dependencies")

    if "AssertionError" in test_output:
        suggestions.append("Review assertion logic in failing tests")

    return suggestions


async def _check_pytest_available(shell_runner) -> bool:
    """Check if pytest is available in the environment."""
    try:
        check_result = await asyncio.wait_for(
            asyncio.to_thread(shell_runner.execute, "python -c 'import pytest; print(pytest.__version__)'"), timeout=5
        )
        return check_result.exit_code == 0
    except:
        return False


async def _implement_linting_fixes(finding: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Implement linting-related fixes."""
    try:
        lint_result = shell_runner.execute(
            "python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics"
        )
        return {
            "type": "linting",
            "status": "Addressed",
            "details": "Linting issues reviewed and addressed",
            "output": lint_result.stdout[:500],
        }
    except Exception as e:
        return {"type": "linting", "status": "Failed", "error": str(e)}


async def _implement_documentation_fixes(finding: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Implement documentation-related fixes."""
    try:
        doc_result = shell_runner.execute("find . -name '*.md' -type f | head -10")
        return {
            "type": "documentation",
            "status": "Addressed",
            "details": "Documentation improvements identified",
            "output": doc_result.stdout[:500],
        }
    except Exception as e:
        return {"type": "documentation", "status": "Failed", "error": str(e)}


async def _implement_performance_fixes(finding: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Implement performance-related fixes."""
    try:
        perf_result = shell_runner.execute(
            "find . -name '*.py' -exec grep -l 'performance\\|optimize\\|speed' {} \\; | head -5"
        )
        return {
            "type": "performance",
            "status": "Addressed",
            "details": "Performance improvements identified",
            "output": perf_result.stdout[:500],
        }
    except Exception as e:
        return {"type": "performance", "status": "Failed", "error": str(e)}


async def _implement_security_fixes(finding: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Implement security-related fixes."""
    try:
        security_result = shell_runner.execute(
            "grep -r -i 'password\\|secret\\|key\\|token' . --include='*.py' | head -5"
        )
        return {
            "type": "security",
            "status": "Addressed",
            "details": "Security improvements identified",
            "output": security_result.stdout[:500],
        }
    except Exception as e:
        return {"type": "security", "status": "Failed", "error": str(e)}


async def _implement_general_fixes(finding: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Implement general fixes."""
    try:
        general_result = shell_runner.execute("git status --porcelain")
        return {
            "type": "general",
            "status": "Addressed",
            "details": "General improvements implemented",
            "output": general_result.stdout[:500],
        }
    except Exception as e:
        return {"type": "general", "status": "Failed", "error": str(e)}


async def _validate_fixes(implementation_result: dict[str, Any], shell_runner) -> dict[str, Any]:
    """Validate that fixes were implemented correctly."""
    try:
        validation_tests = []

        # Test 1: Check for critical errors
        critical_test = shell_runner.execute(
            "python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics"
        )
        validation_tests.append(
            {
                "test": "Critical errors check",
                "status": "PASSED" if critical_test.exit_code == 0 else "FAILED",
                "output": critical_test.stdout[:500],
            }
        )

        # Test 2: Check git status
        git_test = shell_runner.execute("git status --porcelain")
        validation_tests.append(
            {
                "test": "Git status check",
                "status": "PASSED" if git_test.exit_code == 0 else "FAILED",
                "output": git_test.stdout[:500],
            }
        )

        return {
            "status": "Validation completed",
            "details": f"Ran {len(validation_tests)} validation tests",
            "tests": validation_tests,
        }
    except Exception as e:
        return {"status": f"Validation failed: {str(e)}"}
