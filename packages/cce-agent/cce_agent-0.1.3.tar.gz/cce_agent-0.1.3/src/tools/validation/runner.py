"""
Provides a ValidationRunner to orchestrate linting and testing.
"""

import logging
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Structured result for a validation run."""

    success: bool
    lint_success: bool
    test_success: bool
    lint_output_path: str | None = None
    test_output_path: str | None = None
    error_message: str | None = None


class ValidationRunner:
    """Orchestrates calls to aiderctl for linting and testing."""

    def __init__(self, backend):
        """
        Initialize ValidationRunner with a backend.

        Args:
            backend: Either AiderctlWrapper or CodeTools instance
        """
        self.backend = backend
        self.logger = logging.getLogger(__name__)

    async def run_validation(self) -> ValidationResult:
        """
        Runs both linting and testing and returns an aggregated result.
        """
        self.logger.info("Starting validation pipeline...")

        try:
            # Check if backend is CodeTools or AiderctlWrapper
            if hasattr(self.backend, "lint") and hasattr(self.backend, "test"):
                # CodeTools backend
                lint_result = await self.backend.lint()
                test_result = await self.backend.test()

                lint_success = lint_result.status == "success"
                lint_output = lint_result.result
                test_success = test_result.status == "success"
                test_output = test_result.result
            else:
                # AiderctlWrapper backend (legacy)
                lint_task = self.backend.lint()
                test_task = self.backend.test()

                lint_success, lint_output = await lint_task
                test_success, test_output = await test_task

            # Check if linting actually found errors (not just if command succeeded)
            lint_has_errors = False
            if lint_success and lint_output:
                # Extract the actual lint log file path from the output
                import json
                import os

                lint_log_path = None
                for line in lint_output.split("\n"):
                    if ".artifacts/aider/logs/lint_" in line and ".json" in line:
                        # Extract the log file path
                        parts = line.split()
                        for part in parts:
                            if ".artifacts/aider/logs/lint_" in part and ".json" in part:
                                lint_log_path = part.strip()
                                break
                        if lint_log_path:
                            break

                if lint_log_path and os.path.exists(lint_log_path):
                    try:
                        with open(lint_log_path) as f:
                            lint_data = json.load(f)
                        aider_output = lint_data.get("aider_output", "")
                        # Check if linting found errors (E=error, W=warning, F=fatal)
                        if "E" in aider_output or "W" in aider_output or "F" in aider_output:
                            lint_has_errors = True
                            self.logger.warning("Linting found errors in code")
                    except Exception as e:
                        self.logger.error(f"Failed to parse lint log: {e}")

            # Check if tests actually failed (not just if command succeeded)
            test_has_failures = False
            if test_success and test_output:
                # Extract the actual test log file path from the output
                test_log_path = None
                for line in test_output.split("\n"):
                    if ".artifacts/aider/logs/test_" in line and ".json" in line:
                        # Extract the log file path
                        parts = line.split()
                        for part in parts:
                            if ".artifacts/aider/logs/test_" in part and ".json" in part:
                                test_log_path = part.strip()
                                break
                        if test_log_path:
                            break

                if test_log_path and os.path.exists(test_log_path):
                    try:
                        with open(test_log_path, encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        # Try to parse as JSON, but handle malformed JSON gracefully
                        try:
                            test_data = json.loads(content)
                            aider_output = test_data.get("aider_output", "")
                        except json.JSONDecodeError:
                            # If JSON parsing fails, treat the entire content as the output
                            aider_output = content

                        # Check if tests failed
                        if "FAILED" in aider_output or "ERROR" in aider_output or "failed" in aider_output.lower():
                            test_has_failures = True
                            self.logger.warning("Tests failed")
                    except Exception as e:
                        self.logger.error(f"Failed to parse test log: {e}")

            # Overall success means both commands succeeded AND no errors were found
            overall_success = lint_success and test_success and not lint_has_errors and not test_has_failures

            error_message = None
            if not overall_success:
                errors = []
                if not lint_success:
                    errors.append(f"Linting command failed. Report: {lint_output}")
                elif lint_has_errors:
                    errors.append(f"Linting found errors in code. Report: {lint_output}")
                if not test_success:
                    errors.append(f"Test command failed. Report: {test_output}")
                elif test_has_failures:
                    errors.append(f"Tests failed. Report: {test_output}")
                error_message = "\n".join(errors)
                self.logger.warning(f"Validation failed: {error_message}")
            else:
                self.logger.info("Validation pipeline completed successfully.")

            return ValidationResult(
                success=overall_success,
                lint_success=lint_success and not lint_has_errors,
                test_success=test_success and not test_has_failures,
                lint_output_path=lint_output,  # Always provide the path, even if lint failed
                test_output_path=test_output,  # Always provide the path, even if test failed
                error_message=error_message,
            )

        except Exception as e:
            self.logger.error(f"An unexpected error occurred during validation: {e}", exc_info=True)
            return ValidationResult(
                success=False,
                lint_success=False,
                test_success=False,
                error_message=f"An unexpected error occurred: {e}",
            )
