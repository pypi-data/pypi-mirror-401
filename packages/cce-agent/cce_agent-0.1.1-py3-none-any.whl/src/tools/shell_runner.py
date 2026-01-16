import logging
import os
import subprocess
from dataclasses import dataclass

from src.environments.base import ShellResult


@dataclass
class ShellResult:
    """Represents the result of a shell command execution."""

    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration: float


class ShellRunner:
    """A wrapper for executing shell commands."""

    def __init__(self, base_directory: str | None = None):
        """
        Initializes the ShellRunner.
        Args:
            base_directory: The base directory to run commands from. If None, uses the current working directory.
        """
        self.base_directory = base_directory or os.getcwd()
        self.logger = logging.getLogger(__name__)

    def _is_expected_failure(self, command: str, stderr: str) -> bool:
        """
        Determines if a command failure is expected and should not be logged as a warning.

        Args:
            command: The command that was executed
            stderr: The stderr output from the command

        Returns:
            True if this is an expected failure that shouldn't be logged as a warning
        """
        # Git branch deletion failures are often expected
        if "git branch" in command and "delete" in command.lower():
            if "cannot delete branch" in stderr.lower() or "branch not found" in stderr.lower():
                return True

        # Git show-ref failures for non-existent refs are expected
        if "git show-ref" in command and "not found" in stderr.lower():
            return True

        # Git checkout failures for non-existent branches are expected in some contexts
        if "git checkout" in command and "pathspec" in stderr.lower():
            return True

        return False

    def execute(self, command: str, cwd: str | None = None) -> ShellResult:
        """
        Executes a shell command.

        Args:
            command: The command to execute.
            cwd: The working directory for the command. If None, uses the base_directory.

        Returns:
            A ShellResult object with the execution details.
        """
        effective_cwd = cwd or self.base_directory
        self.logger.info(f"Executing command: '{command}' in '{effective_cwd}'")

        try:
            process = subprocess.run(
                command, shell=True, capture_output=True, text=True, cwd=effective_cwd, check=False
            )

            stdout = process.stdout.strip() if process.stdout else ""
            stderr = process.stderr.strip() if process.stderr else ""

            if process.returncode != 0:
                # Only log as warning if stderr contains meaningful error information
                # Skip logging for expected failures (like trying to delete non-existent branches)
                if stderr and not self._is_expected_failure(command, stderr):
                    self.logger.warning(f"Command failed with exit code {process.returncode}")
                    self.logger.warning(f"Stderr: {stderr}")
                else:
                    # Log as debug for expected failures
                    self.logger.debug(f"Command failed with exit code {process.returncode} (expected): {stderr}")

            return ShellResult(
                command=command,
                exit_code=process.returncode,
                stdout=stdout,
                stderr=stderr,
                duration=0.0,  # Placeholder, actual duration calculation would be here
            )
        except subprocess.TimeoutExpired:
            self.logger.warning(f"Command timed out: {command}")
            return ShellResult(
                command=command,
                exit_code=124,  # Exit code for timeout
                stdout="",
                stderr="",
                duration=0.0,  # Placeholder
            )
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during command execution: {e}")
            return ShellResult(
                command=command,
                exit_code=1,  # Generic error code
                stdout="",
                stderr=str(e),
                duration=0.0,  # Placeholder
            )
