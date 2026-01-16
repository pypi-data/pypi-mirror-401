import asyncio
import json
import logging
import os
import subprocess
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

import tiktoken

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    # Load .env from the project root (where this file is located)
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()  # Fallback to default behavior
except ImportError:
    pass  # dotenv not available, continue without it


class ErrorType(Enum):
    """Classification of AIDER errors for retry logic."""

    TEMPORARY = "temporary"  # Network, timeout, rate limit
    PERMANENT = "permanent"  # Invalid command, missing file, permission
    UNKNOWN = "unknown"  # Unclassified errors


@dataclass
class RetryConfig:
    """Configuration for retry logic."""

    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker pattern."""

    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    half_open_max_calls: int = 3


class CircuitBreakerState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, blocking calls
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """Circuit breaker implementation for AIDER integration."""

    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.half_open_calls = 0

    def can_execute(self) -> bool:
        """Check if execution is allowed based on circuit breaker state."""
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            # Check if recovery timeout has passed
            if time.time() - self.last_failure_time >= self.config.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.half_open_calls = 0
                return True
            return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return self.half_open_calls < self.config.half_open_max_calls
        return False

    def record_success(self):
        """Record a successful execution."""
        if self.state == CircuitBreakerState.HALF_OPEN:
            # Success in half-open state, close the circuit
            self.state = CircuitBreakerState.CLOSED
            self.failure_count = 0
        elif self.state == CircuitBreakerState.CLOSED:
            # Reset failure count on success
            self.failure_count = 0

    def record_failure(self):
        """Record a failed execution."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitBreakerState.HALF_OPEN:
            # Failure in half-open state, open the circuit
            self.state = CircuitBreakerState.OPEN
        elif self.state == CircuitBreakerState.CLOSED:
            # Check if we should open the circuit
            if self.failure_count > self.config.failure_threshold:
                self.state = CircuitBreakerState.OPEN


class AiderctlWrapper:
    """A Python wrapper for the aiderctl shell script."""

    def __init__(
        self,
        aiderctl_path: str | None = None,
        cwd: str | None = None,
        force_mode: bool = True,
        strict_mode: bool = True,
        retry_config: RetryConfig | None = None,
        circuit_breaker_config: CircuitBreakerConfig | None = None,
    ):
        self.logger = logging.getLogger(__name__)
        if aiderctl_path is None:
            aiderctl_path = str(Path(__file__).resolve().parents[1] / "aiderctl")
        candidate = Path(aiderctl_path)
        if not candidate.is_absolute():
            candidate = (Path(__file__).resolve().parents[1] / aiderctl_path).resolve()
        self.aiderctl_path = str(candidate)
        self.cwd = cwd or os.getcwd()
        self.force_mode = force_mode
        self.strict_mode = strict_mode
        self._available = None  # Cache availability check

        # Initialize retry and circuit breaker configurations
        self.retry_config = retry_config or RetryConfig()
        self.circuit_breaker_config = circuit_breaker_config or CircuitBreakerConfig()
        self.circuit_breaker = CircuitBreaker(self.circuit_breaker_config)

        # In strict mode, raise error if aiderctl not found (backward compatibility)
        # In non-strict mode, log warning and continue with graceful degradation
        if not Path(self.aiderctl_path).exists():
            error_msg = f"aiderctl script not found at {self.aiderctl_path}"
            if strict_mode:
                raise FileNotFoundError(error_msg)
            else:
                self.logger.warning(f"AIDER Integration: {error_msg}")
                self.logger.info("System will continue with graceful degradation - AIDER-specific features disabled")
                self._available = False

    def _classify_error(self, error_message: str, exit_code: int) -> ErrorType:
        """Classify an error as temporary, permanent, or unknown."""
        error_lower = error_message.lower()

        # Temporary errors (should be retried)
        temporary_indicators = [
            "timeout",
            "timed out",
            "connection",
            "network",
            "rate limit",
            "temporary",
            "retry",
            "service unavailable",
            "service temporarily unavailable",
            "gateway timeout",
            "too many requests",
            "quota exceeded",
            "api key",
            "authentication",
        ]

        # Permanent errors (should not be retried)
        permanent_indicators = [
            "not found",
            "no such file",
            "permission denied",
            "invalid",
            "syntax error",
            "command not found",
            "file exists",
            "already exists",
            "invalid argument",
            "bad request",
            "forbidden",
            "unauthorized",
        ]

        for indicator in temporary_indicators:
            if indicator in error_lower:
                return ErrorType.TEMPORARY

        for indicator in permanent_indicators:
            if indicator in error_lower:
                return ErrorType.PERMANENT

        # Check exit codes
        if exit_code in [124, 125, 126, 127]:  # Common temporary failure codes
            return ErrorType.TEMPORARY
        elif exit_code in [1, 2]:  # Common permanent failure codes
            return ErrorType.PERMANENT

        return ErrorType.UNKNOWN

    def _calculate_retry_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt with exponential backoff and jitter."""
        delay = min(
            self.retry_config.base_delay * (self.retry_config.exponential_base**attempt), self.retry_config.max_delay
        )

        if self.retry_config.jitter:
            # Add jitter to prevent thundering herd
            import random

            jitter_factor = random.uniform(0.5, 1.5)
            delay *= jitter_factor

        return delay

    async def _run_command_with_retry(self, *args: str) -> tuple[bool, str, str]:
        """Run command with retry logic and circuit breaker."""
        # Check circuit breaker
        if not self.circuit_breaker.can_execute():
            error_msg = f"Circuit breaker is OPEN - AIDER integration temporarily disabled due to repeated failures"
            self.logger.warning(error_msg)
            return False, "", error_msg

        last_error = None
        last_stdout = ""
        last_stderr = ""

        for attempt in range(self.retry_config.max_retries + 1):
            try:
                success, stdout, stderr = await self._run_command(*args)

                if success:
                    # Record success in circuit breaker
                    self.circuit_breaker.record_success()
                    return True, stdout, stderr
                else:
                    # Classify the error
                    error_type = self._classify_error(stderr, -1)  # We don't have exit code here
                    last_error = error_type
                    last_stdout = stdout
                    last_stderr = stderr

                    # Don't retry permanent errors
                    if error_type == ErrorType.PERMANENT:
                        self.logger.error(f"Permanent error detected, not retrying: {stderr}")
                        self.circuit_breaker.record_failure()
                        return False, stdout, stderr

                    # Don't retry on last attempt
                    if attempt >= self.retry_config.max_retries:
                        self.logger.error(f"Max retries ({self.retry_config.max_retries}) exceeded")
                        self.circuit_breaker.record_failure()
                        return False, stdout, stderr

                    # Calculate delay and retry
                    delay = self._calculate_retry_delay(attempt)
                    self.logger.warning(
                        f"Attempt {attempt + 1} failed ({error_type.value} error), retrying in {delay:.1f}s: {stderr}"
                    )
                    await asyncio.sleep(delay)

            except Exception as e:
                last_error = ErrorType.UNKNOWN
                last_stderr = str(e)
                self.logger.error(f"Exception during command execution (attempt {attempt + 1}): {e}")

                if attempt >= self.retry_config.max_retries:
                    self.circuit_breaker.record_failure()
                    return False, "", str(e)

                delay = self._calculate_retry_delay(attempt)
                await asyncio.sleep(delay)

        # If we get here, all retries failed
        self.circuit_breaker.record_failure()
        return False, last_stdout, last_stderr

    async def _cleanup_existing_sessions(self) -> None:
        """Clean up any existing aider processes to prevent conflicts."""
        try:
            self.logger.debug("Cleaning up existing aider sessions...")

            # Use pkill to find and kill aider processes
            process = await asyncio.create_subprocess_exec(
                "pkill", "-f", "aider", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                self.logger.info("Cleaned up existing aider sessions")
            elif process.returncode == 1:
                # pkill returns 1 when no processes found - this is normal
                self.logger.debug("No existing aider sessions to clean up")
            else:
                self.logger.warning(f"Session cleanup returned code {process.returncode}: {stderr.decode()}")

        except Exception as e:
            # Don't fail the main operation if cleanup fails
            self.logger.warning(f"Session cleanup failed: {e}")

    async def _run_command(self, *args: str) -> tuple[bool, str, str]:
        """Asynchronously run an aiderctl command and capture its output."""
        # Check availability before running command
        if not self.is_available():
            status = self.get_availability_status()
            error_msg = f"{status['message']}. {status.get('guidance', '')} {status.get('fallback', '')}"
            return False, "", error_msg

        # Clean up any existing aider sessions to prevent conflicts
        await self._cleanup_existing_sessions()

        try:
            Path(self.cwd, "patches").mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            self.logger.warning("Failed to ensure patches directory in %s: %s", self.cwd, exc)

        command = [self.aiderctl_path] + list(args)
        if self.force_mode and "--force" not in command:
            command.append("--force")

        self.logger.info(f"Running command: {' '.join(command)}")

        # Create a copy of the current environment and add the API key if it exists
        env = os.environ.copy()
        if "OPENAI_API_KEY" in os.environ:
            env["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]
            self.logger.info("Propagating OPENAI_API_KEY to aiderctl subprocess.")
        else:
            self.logger.warning("OPENAI_API_KEY not found in environment. AIDER may fail or prompt for a key.")

        process = await asyncio.create_subprocess_exec(
            *command, cwd=self.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
        )

        try:
            # Add timeout to prevent hanging - should be longer than aiderctl's 300s timeout
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=600.0)
            stdout_str = stdout.decode("utf-8").strip()
            stderr_str = stderr.decode("utf-8").strip()
        except TimeoutError:
            self.logger.error("Command timed out after 600 seconds")

            # Try to capture any partial output before killing the process
            try:
                # Give a moment for any buffered output
                await asyncio.sleep(0.1)
                stdout, stderr = await process.communicate()
                partial_stdout = stdout.decode("utf-8", errors="ignore").strip()
                partial_stderr = stderr.decode("utf-8", errors="ignore").strip()

                # Log partial output for debugging
                if partial_stdout:
                    self.logger.error(f"Partial stdout before timeout: {partial_stdout[:500]}...")
                if partial_stderr:
                    self.logger.error(f"Partial stderr before timeout: {partial_stderr[:500]}...")

                # Create timeout artifact for debugging
                self._create_timeout_artifact(command, partial_stdout, partial_stderr)

            except Exception as e:
                self.logger.error(f"Failed to capture partial output: {e}")

            process.kill()
            await process.wait()
            return False, "", "Command timed out after 300 seconds"

        if process.returncode != 0:
            self.logger.error(f"Command failed with exit code {process.returncode}")
            self.logger.error(f"Stderr: {stderr_str}")
            return False, stdout_str, stderr_str

        return True, stdout_str, stderr_str

    def _create_timeout_artifact(self, command: list, partial_stdout: str, partial_stderr: str):
        """Create an artifact file with timeout debugging information."""
        try:
            from datetime import datetime

            # Create artifacts directory if it doesn't exist
            from src.config.artifact_root import get_aider_artifacts_directory

            artifacts_dir = get_aider_artifacts_directory() / "timeouts"
            artifacts_dir.mkdir(parents=True, exist_ok=True)

            # Create timestamped artifact file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            artifact_file = artifacts_dir / f"timeout_{timestamp}.txt"

            with open(artifact_file, "w") as f:
                f.write(f"# AIDER Timeout Debug Artifact\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Command: {' '.join(command)}\n")
                f.write(f"Timeout: 300 seconds\n\n")

                f.write(f"## Partial Output (stdout)\n")
                f.write(f"{partial_stdout}\n\n")

                f.write(f"## Partial Output (stderr)\n")
                f.write(f"{partial_stderr}\n\n")

                f.write(f"## Debug Information\n")
                f.write(f"- Command timed out after 300 seconds\n")
                f.write(f"- This may indicate an issue with the aiderctl script or LLM API\n")
                f.write(f"- Check if the aiderctl script is properly configured\n")
                f.write(f"- Verify API keys and network connectivity\n")

            self.logger.info(f"Timeout artifact created: {artifact_file}")

        except Exception as e:
            self.logger.error(f"Failed to create timeout artifact: {e}")

    def _parse_map_output(self, raw_output: str) -> str:
        """
        Parse AIDER map output to separate logs from actual repository map content.

        AIDER output typically contains:
        1. Log lines with timestamps: "2025-09-08 19:24:43 [INFO] ..."
        2. Actual repository map content after the logs

        Args:
            raw_output: Raw stdout from aiderctl map command

        Returns:
            Clean repository map content without log lines
        """
        if not raw_output:
            return ""

        lines = raw_output.split("\n")
        content_lines = []
        log_pattern_detected = False

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Detect and skip log lines (timestamps with [INFO], [WARN], [ERROR], etc.)
            if (" [INFO] " in line or " [WARN] " in line or " [ERROR] " in line or " [DEBUG] " in line) and (
                "2025-" in line[:20] or "2024-" in line[:20]
            ):
                log_pattern_detected = True
                self.logger.debug(f"Filtering out AIDER log: {line}")
                continue

            # Skip incomplete/truncated lines that look like partial logs
            if log_pattern_detected and (line.startswith("2025-") or line.startswith("2024-")):
                self.logger.debug(f"Filtering out partial AIDER log: {line}")
                continue

            # This looks like actual content
            content_lines.append(line)

        # Join the content lines
        clean_content = "\n".join(content_lines).strip()

        if log_pattern_detected:
            self.logger.info(
                f"Parsed AIDER map output: filtered out logs, extracted {len(clean_content)} chars of repository map content"
            )

        return clean_content

    def is_available(self) -> bool:
        """Check if AIDER is available and can be used."""
        if self._available is not None:
            return self._available

        # Check if aiderctl script exists
        if not Path(self.aiderctl_path).exists():
            self._available = False
            return False

        # Check if script is executable
        if not os.access(self.aiderctl_path, os.X_OK):
            self.logger.warning(f"AIDER Integration: {self.aiderctl_path} exists but is not executable")
            self._available = False
            return False

        self._available = True
        return True

    def get_availability_status(self) -> dict[str, str]:
        """Get detailed information about AIDER availability."""
        if self.is_available():
            return {
                "status": "available",
                "message": "AIDER integration is available and ready to use",
                "path": self.aiderctl_path,
            }
        else:
            # Provide helpful installation guidance
            if not Path(self.aiderctl_path).exists():
                return {
                    "status": "not_found",
                    "message": f"AIDER script not found at {self.aiderctl_path}",
                    "guidance": "Install AIDER with: pip install aider-chat, or ensure aiderctl script is available at the expected path",
                    "fallback": "System will continue with standard editing tools and graceful degradation",
                }
            else:
                return {
                    "status": "not_executable",
                    "message": f"AIDER script found but not executable at {self.aiderctl_path}",
                    "guidance": f"Make script executable with: chmod +x {self.aiderctl_path}",
                    "fallback": "System will continue with standard editing tools",
                }

    async def version(self) -> str:
        """Get the AIDER and wrapper version information."""
        success, stdout, stderr = await self._run_command_with_retry("--version")
        if not success:
            return f"Error getting version: {stderr}"
        return stdout

    async def bootstrap(self) -> bool:
        """
        Bootstrap the AIDER configuration by creating .aider.conf.yml and .aiderignore.
        """
        success, _, stderr = await self._run_command_with_retry("bootstrap")
        if not success:
            self.logger.error(f"Failed to bootstrap AIDER configuration: {stderr}")
        return success

    async def get_map(self, map_tokens: int = 4096, refresh: str = "auto", subtree: str = "src") -> str | None:
        """
        Get the repository map with improved coverage and quality.

        Args:
            map_tokens: The token budget for the map (default 4096 for better performance).
            refresh: The refresh policy (default "always" for fresh content).
            subtree: The path to a subtree to scope the map to.

        Returns:
            The repository map as a string, or None if it fails.
        """
        # Use higher token budget and always refresh for better quality
        args = ["map", "--map-tokens", str(map_tokens), "--refresh", refresh]
        if subtree:
            args.extend(["--subtree", subtree])

        self.logger.info(f"🔍 Generating repository map with {map_tokens} tokens, refresh={refresh}")

        success, stdout, stderr = await self._run_command_with_retry(*args)
        if not success:
            self.logger.error(f"Failed to get repo map: {stderr}")
            self.logger.error(f"Failed to get repo map: {stdout}")
            return None

        # Parse and clean the output - separate logs from actual repository map content
        parsed_output = self._parse_map_output(stdout)

        # Check if the output is a file path (aiderctl returns file paths, not content)
        if parsed_output and parsed_output.startswith("/") and parsed_output.endswith(".txt"):
            try:
                # Read the actual repository map content from the file
                with open(parsed_output, encoding="utf-8") as f:
                    file_content = f.read()
                self.logger.info(f"✅ Repository map read from file: {parsed_output} ({len(file_content)} chars)")
                return file_content
            except Exception as e:
                self.logger.error(f"Failed to read repository map file {parsed_output}: {e}")
                return None

        if parsed_output:
            self.logger.info(f"✅ Repository map generated successfully ({len(parsed_output)} chars)")
        else:
            self.logger.warning("⚠️ Repository map parsing returned empty content")

        return parsed_output

    async def ask(self, message: str, files: list[str] | None = None) -> str:
        """
        Ask a question about the codebase without applying edits.

        Args:
            message: The question to ask.
            files: A list of file paths to include as context.

        Returns:
            The model's response.
        """
        args = ["ask", "--message", message]
        if files:
            for file_path in files:
                args.extend(["--file", file_path])

        success, stdout, stderr = await self._run_command_with_retry(*args)
        if not success:
            return f"Error during 'ask': {stderr}"
        return stdout

    async def edit(
        self,
        message: str,
        files: list[str],
        mode: str = "architect",
        editor_model: str | None = None,
        auto_accept: bool = True,
        use_whole_format: bool = True,
    ) -> tuple[bool, str]:
        """
        Run an edit on the specified files.

        Args:
            message: The instruction for the edit.
            files: The list of file paths to edit.
            mode: The edit mode ('edit' or 'architect').
            editor_model: The model to use for editing (in architect mode).
            auto_accept: Whether to automatically accept the changes.
            use_whole_format: Whether to use whole edit format for better reliability.

        Returns:
            A tuple of (success, message) where message contains stdout or stderr.
        """
        if mode not in ["edit", "architect"]:
            raise ValueError("Mode must be either 'edit' or 'architect'")

        args = [mode, "--message", message]
        if auto_accept:
            args.append("--auto-accept")
        if mode == "architect":
            args.append("--auto-accept-architect")  # Auto-accept architect proposals
            if editor_model:
                args.extend(["--editor-model", editor_model])
        if use_whole_format:
            args.extend(["--edit-format", "whole"])

        for file_path in files:
            args.extend(["--file", file_path])

        success, stdout, stderr = await self._run_command_with_retry(*args)
        return success, stdout if success else stderr

    async def edit_with_models(
        self,
        message: str,
        files: list[str],
        architect_model: str | None = None,
        editor_model: str | None = None,
        auto_accept: bool = False,
    ) -> tuple[bool, str]:
        """
        Run an edit using both architect and editor models on the specified files.

        Args:
            message: The instruction for the edit.
            files: The list of file paths to edit.
            architect_model: The model to use as architect (optional).
            editor_model: The model to use for editing (in architect mode).
            auto_accept: Whether to automatically accept the changes.

        Returns:
            A tuple of (success, message) where message contains stdout or stderr.
        """
        # Use architect mode when we have both models or when explicitly requested
        mode = "architect" if (architect_model or editor_model) else "edit"

        args = [mode, "--message", message]
        if auto_accept:
            args.append("--auto-accept")
        if mode == "architect":
            args.append("--auto-accept-architect")  # Auto-accept architect proposals
            if architect_model:
                args.extend(["--model", architect_model])
            if editor_model:
                args.extend(["--editor-model", editor_model])

        # Always use whole format for better reliability
        args.extend(["--edit-format", "whole"])

        for file_path in files:
            args.extend(["--file", file_path])

        success, stdout, stderr = await self._run_command_with_retry(*args)
        return success, stdout if success else stderr

    async def edit_with_fallback(
        self,
        message: str,
        files: list[str],
        preferred_mode: str = "architect",
        editor_model: str | None = None,
        auto_accept: bool = False,
    ) -> tuple[bool, str]:
        """
        Run an edit with fallback strategy for maximum reliability.

        Tries architect mode first (recommended by aider docs), then falls back to regular edit mode.

        Args:
            message: The instruction for the edit.
            files: The list of file paths to edit.
            preferred_mode: Preferred mode ('architect' or 'edit').
            editor_model: The model to use for editing (in architect mode).
            auto_accept: Whether to automatically accept the changes.

        Returns:
            A tuple of (success, message) where message contains stdout or stderr.
        """
        # Try preferred mode first
        self.logger.info(f"🎯 Attempting edit with {preferred_mode} mode")
        success, output = await self.edit(
            message=message,
            files=files,
            mode=preferred_mode,
            editor_model=editor_model,
            auto_accept=auto_accept,
            use_whole_format=True,
        )

        if success:
            self.logger.info(f"✅ Edit successful with {preferred_mode} mode")
            return success, output

        # Fallback to alternative mode
        fallback_mode = "edit" if preferred_mode == "architect" else "architect"
        self.logger.warning(f"⚠️ {preferred_mode} mode failed, trying fallback to {fallback_mode} mode")

        success, output = await self.edit(
            message=message,
            files=files,
            mode=fallback_mode,
            editor_model=editor_model,
            auto_accept=auto_accept,
            use_whole_format=True,
        )

        if success:
            self.logger.info(f"✅ Edit successful with fallback {fallback_mode} mode")
        else:
            self.logger.error(f"❌ Both {preferred_mode} and {fallback_mode} modes failed")

        return success, output

    def estimate_tokens(self, text: str, model: str = "gpt-4") -> int:
        """
        Estimate token count for text using tiktoken.

        Args:
            text: The text to estimate tokens for.
            model: The model to use for tokenization.

        Returns:
            Estimated token count.
        """
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception as e:
            self.logger.warning(f"Failed to estimate tokens: {e}")
            # Fallback: rough estimate of 4 characters per token
            return len(text) // 4

    def check_context_size(self, message: str, files: list[str], max_tokens: int = 15000) -> dict[str, Any]:
        """
        Check if the context size is within recommended limits.

        Args:
            message: The message to send to aider.
            files: List of files being edited.
            max_tokens: Maximum recommended tokens (default 15k for better performance).

        Returns:
            Dictionary with context size information and recommendations.
        """
        # Estimate tokens for message
        message_tokens = self.estimate_tokens(message)

        # Estimate tokens for file contents (rough estimate)
        file_tokens = 0
        for file_path in files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, encoding="utf-8") as f:
                        content = f.read()
                        file_tokens += self.estimate_tokens(content)
            except Exception as e:
                self.logger.warning(f"Could not read file {file_path}: {e}")

        total_tokens = message_tokens + file_tokens

        result = {
            "message_tokens": message_tokens,
            "file_tokens": file_tokens,
            "total_tokens": total_tokens,
            "max_tokens": max_tokens,
            "within_limit": total_tokens <= max_tokens,
            "recommendations": [],
        }

        if not result["within_limit"]:
            result["recommendations"].extend(
                [
                    "Consider using /drop to remove unnecessary files from context",
                    "Use /clear to remove conversation history",
                    "Break down the task into smaller, focused edits",
                    "Use architect mode for complex changes",
                ]
            )

        if total_tokens > max_tokens * 1.5:
            result["recommendations"].append("Context size is very large - consider using phased execution")

        return result

    async def edit_with_context_check(
        self,
        message: str,
        files: list[str],
        mode: str = "architect",
        editor_model: str | None = None,
        auto_accept: bool = False,
        max_tokens: int = 25000,
    ) -> tuple[bool, str]:
        """
        Run an edit with context size checking and optimization.

        Args:
            message: The instruction for the edit.
            files: The list of file paths to edit.
            mode: The edit mode ('edit' or 'architect').
            editor_model: The model to use for editing (in architect mode).
            auto_accept: Whether to automatically accept the changes.
            max_tokens: Maximum recommended tokens.

        Returns:
            A tuple of (success, message) where message contains stdout or stderr.
        """
        # Check context size
        context_info = self.check_context_size(message, files, max_tokens)

        self.logger.info(f"📊 Context size check:")
        self.logger.info(f"   Message tokens: {context_info['message_tokens']}")
        self.logger.info(f"   File tokens: {context_info['file_tokens']}")
        self.logger.info(f"   Total tokens: {context_info['total_tokens']}/{max_tokens}")

        if not context_info["within_limit"]:
            self.logger.warning(f"⚠️ Context size exceeds recommended limit!")
            for recommendation in context_info["recommendations"]:
                self.logger.warning(f"   💡 {recommendation}")

        # Use fallback strategy for better reliability
        return await self.edit_with_fallback(
            message=message, files=files, preferred_mode=mode, editor_model=editor_model, auto_accept=auto_accept
        )

    async def apply_patch(self, patch_file: str) -> tuple[bool, str]:
        """
        Apply a patch file using aider's --apply flag.

        Args:
            patch_file: Path to the patch file to apply.

        Returns:
            A tuple of (success, output) where output contains stdout or stderr.
        """
        if not os.path.exists(patch_file):
            return False, f"Patch file not found: {patch_file}"

        args = ["--apply", patch_file]
        success, stdout, stderr = await self._run_command_with_retry(*args)
        return success, stdout if success else stderr

    async def lint(self) -> tuple[bool, str]:
        """
        Run the linter on the codebase.

        Returns:
            A tuple of (success, output). Output contains linting results or an error.
        """
        success, stdout, stderr = await self._run_command_with_retry("lint")
        return success, stdout if success else stderr

    async def test(self) -> tuple[bool, str]:
        """
        Run the test suite.

        Returns:
            A tuple of (success, output). Output contains test results or an error.
        """
        success, stdout, stderr = await self._run_command_with_retry("test")
        return success, stdout if success else stderr

    async def info(self) -> dict[str, Any] | None:
        """
        Get information about the AIDER environment, including Tree-sitter status.

        Returns:
            A dictionary with the info, or None if it fails.
        """
        success, stdout, stderr = await self._run_command_with_retry("info", "--format", "json")
        if not success:
            self.logger.error(f"Failed to get info: {stderr}")
            return None
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse JSON from 'info' command: {stdout}")
            return None

    def get_circuit_breaker_status(self) -> dict[str, Any]:
        """Get the current circuit breaker status for monitoring."""
        return {
            "state": self.circuit_breaker.state.value,
            "failure_count": self.circuit_breaker.failure_count,
            "last_failure_time": self.circuit_breaker.last_failure_time,
            "can_execute": self.circuit_breaker.can_execute(),
            "config": {
                "failure_threshold": self.circuit_breaker_config.failure_threshold,
                "recovery_timeout": self.circuit_breaker_config.recovery_timeout,
                "half_open_max_calls": self.circuit_breaker_config.half_open_max_calls,
            },
        }

    def reset_circuit_breaker(self):
        """Reset the circuit breaker to closed state (for testing/recovery)."""
        self.circuit_breaker.state = CircuitBreakerState.CLOSED
        self.circuit_breaker.failure_count = 0
        self.circuit_breaker.last_failure_time = 0.0
        self.circuit_breaker.half_open_calls = 0
        self.logger.info("Circuit breaker reset to CLOSED state")
