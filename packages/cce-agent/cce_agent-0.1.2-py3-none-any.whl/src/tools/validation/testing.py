"""
Validation Pipeline - Testing Integration

AIDER-inspired testing integration for the CCE agent's validation pipeline.
Detects project test frameworks and runs them with structured output parsing.
"""

import fnmatch
import json
import logging
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .node_tooling import package_json_uses_tool, resolve_node_command


@dataclass
class TestResult:
    """Result of a testing operation"""

    success: bool
    framework: str
    exit_code: int
    stdout: str
    stderr: str
    tests_run: int
    tests_passed: int
    tests_failed: int
    tests_skipped: int
    failures: list[dict[str, Any]]
    duration: float
    command: list[str] = field(default_factory=list)
    selected_tests: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        command = " ".join(self.command) if self.command else ""
        return {
            "success": self.success,
            "framework": self.framework,
            "exit_code": self.exit_code,
            "stdout": self.stdout[:1000] + "..." if len(self.stdout) > 1000 else self.stdout,
            "stderr": self.stderr[:1000] + "..." if len(self.stderr) > 1000 else self.stderr,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "tests_failed": self.tests_failed,
            "tests_skipped": self.tests_skipped,
            "failures": self.failures,
            "duration": self.duration,
            "command": command,
            "selected_tests": self.selected_tests,
        }


@dataclass
class TestFrameworkConfig:
    """Configuration for a test framework"""

    name: str
    command: list[str]
    config_files: list[str]
    test_patterns: list[str]
    output_format: str
    parse_function: str


class FrameworkTestManager:
    """Manages testing operations across different languages and frameworks"""

    _NODE_TOOL_NAMES = {"jest", "mocha", "vitest"}
    _PACKAGE_JSON_TOOL_CONFIGS = {"jest": ["jest"], "mocha": ["mocha"], "vitest": ["vitest"]}

    # Test framework configurations
    FRAMEWORKS = {
        "python": [
            TestFrameworkConfig(
                name="pytest",
                command=["pytest", "--tb=short", "-v"],
                config_files=["pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini"],
                test_patterns=["test_*.py", "*_test.py", "tests/"],
                output_format="text",
                parse_function="_parse_pytest_output",
            ),
            TestFrameworkConfig(
                name="unittest",
                command=["python", "-m", "unittest", "discover", "-v"],
                config_files=[],
                test_patterns=["test_*.py", "*_test.py"],
                output_format="text",
                parse_function="_parse_unittest_output",
            ),
        ],
        "javascript": [
            TestFrameworkConfig(
                name="jest",
                command=["jest", "--json"],
                config_files=["jest.config.js", "jest.config.json", "package.json"],
                test_patterns=["*.test.js", "*.spec.js", "__tests__/"],
                output_format="json",
                parse_function="_parse_jest_output",
            ),
            TestFrameworkConfig(
                name="mocha",
                command=["mocha", "--reporter", "json"],
                config_files=[".mocharc.json", ".mocharc.js", "mocha.opts"],
                test_patterns=["test/", "spec/", "*.test.js", "*.spec.js"],
                output_format="json",
                parse_function="_parse_mocha_output",
            ),
            TestFrameworkConfig(
                name="vitest",
                command=["vitest", "run", "--reporter=json"],
                config_files=[
                    "vitest.config.ts",
                    "vitest.config.js",
                    "vitest.config.mjs",
                    "vitest.config.cjs",
                    "package.json",
                ],
                test_patterns=["*.test.js", "*.spec.js", "__tests__/"],
                output_format="json",
                parse_function="_parse_vitest_output",
            ),
        ],
        "typescript": [
            TestFrameworkConfig(
                name="jest",
                command=["jest", "--json"],
                config_files=["jest.config.js", "jest.config.json", "package.json"],
                test_patterns=["*.test.ts", "*.spec.ts", "__tests__/"],
                output_format="json",
                parse_function="_parse_jest_output",
            ),
            TestFrameworkConfig(
                name="vitest",
                command=["vitest", "run", "--reporter=json"],
                config_files=[
                    "vitest.config.ts",
                    "vitest.config.js",
                    "vitest.config.mjs",
                    "vitest.config.cjs",
                    "package.json",
                ],
                test_patterns=["*.test.ts", "*.spec.ts", "__tests__/"],
                output_format="json",
                parse_function="_parse_vitest_output",
            ),
        ],
        "go": [
            TestFrameworkConfig(
                name="go test",
                command=["go", "test", "-v", "-json"],
                config_files=["go.mod"],
                test_patterns=["*_test.go"],
                output_format="json",
                parse_function="_parse_go_test_output",
            )
        ],
        "rust": [
            TestFrameworkConfig(
                name="cargo test",
                command=["cargo", "test"],
                config_files=["Cargo.toml"],
                test_patterns=["tests/", "*_test.rs"],
                output_format="text",
                parse_function="_parse_cargo_test_output",
            )
        ],
        "solidity": [
            TestFrameworkConfig(
                name="forge test",
                command=["forge", "test", "--json"],
                config_files=["foundry.toml"],
                test_patterns=["test/", "*.t.sol"],
                output_format="json",
                parse_function="_parse_forge_test_output",
            ),
            TestFrameworkConfig(
                name="hardhat test",
                command=["npx", "hardhat", "test"],
                config_files=[
                    "hardhat.config.js",
                    "hardhat.config.ts",
                    "hardhat.config.cjs",
                    "hardhat.config.mjs",
                ],
                test_patterns=["test/", "*.test.js", "*.spec.js", "*.test.ts", "*.spec.ts"],
                output_format="text",
                parse_function="_parse_hardhat_test_output",
            ),
        ],
    }

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.logger = logging.getLogger(__name__)

        # Cache detected frameworks
        self._detected_frameworks: dict[str, list[TestFrameworkConfig]] | None = None

    def detect_frameworks(self, force_refresh: bool = False) -> dict[str, list[TestFrameworkConfig]]:
        """Detect available test frameworks in the project"""
        if self._detected_frameworks and not force_refresh:
            return self._detected_frameworks

        detected = {}

        for language, frameworks in self.FRAMEWORKS.items():
            available_frameworks = []

            for framework_config in frameworks:
                resolved_command = self._resolve_framework_command(framework_config)
                if not resolved_command:
                    continue

                # Check if framework command is available
                if self._is_command_available(resolved_command):
                    # Check if project has relevant config files or test patterns
                    if self._has_config_or_tests(framework_config):
                        available_frameworks.append(framework_config)
                        self.logger.info(f"Detected {framework_config.name} for {language}")

            if available_frameworks:
                detected[language] = available_frameworks

        self._detected_frameworks = detected
        return detected

    def _is_command_available(self, command: list[str]) -> bool:
        """Check if a command is available"""
        try:
            # Handle special cases
            if command[0] == "python" and len(command) > 2 and command[2] == "unittest":
                # Check if unittest module is available
                result = subprocess.run(
                    [command[0], "-m", "unittest", "--help"], capture_output=True, timeout=5, cwd=self.workspace_root
                )
                return result.returncode == 0
            else:
                # Check if command exists
                result = subprocess.run(
                    [command[0], "--version"], capture_output=True, timeout=5, cwd=self.workspace_root
                )
                return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _resolve_framework_command(self, framework_config: TestFrameworkConfig) -> list[str] | None:
        tool_name = framework_config.command[0]

        if tool_name in self._NODE_TOOL_NAMES:
            resolved = resolve_node_command(tool_name, self.workspace_root)
            if not resolved:
                return None
            return resolved + framework_config.command[1:]

        return framework_config.command.copy()

    def _has_config_or_tests(self, framework_config: TestFrameworkConfig) -> bool:
        """Check if project has config files or test files"""
        tool_name = framework_config.command[0]
        if tool_name in self._NODE_TOOL_NAMES:
            config_keys = self._PACKAGE_JSON_TOOL_CONFIGS.get(tool_name)
            if package_json_uses_tool(self.workspace_root, tool_name, config_keys):
                return True

        # Check for config files
        for config_file in framework_config.config_files:
            if config_file == "package.json" and tool_name in self._NODE_TOOL_NAMES:
                continue
            if (self.workspace_root / config_file).exists():
                return True

        # Check for test patterns
        for pattern in framework_config.test_patterns:
            if "/" in pattern:
                # Directory pattern
                if (self.workspace_root / pattern.rstrip("/")).exists():
                    return True
            else:
                # File pattern
                if list(self.workspace_root.rglob(pattern)):
                    return True

        return False

    def _select_target_files_for_framework(
        self, framework_config: TestFrameworkConfig, target_files: list[str] | None
    ) -> list[str]:
        if not target_files:
            return []

        if framework_config.name in {"cargo test", "forge test", "hardhat test"}:
            return []

        test_files: list[str] = []
        for file_path in target_files:
            normalized = str(file_path)
            file_name = Path(normalized).name
            for pattern in framework_config.test_patterns:
                if "*" in pattern:
                    if fnmatch.fnmatch(file_name, pattern) or fnmatch.fnmatch(normalized, pattern):
                        test_files.append(normalized)
                        break
                elif pattern.endswith("/"):
                    pattern_root = pattern.rstrip("/")
                    if f"/{pattern_root}/" in normalized or normalized.endswith(pattern_root):
                        test_files.append(normalized)
                        break
        return test_files

    def suggest_test_plan(self, target_files: list[str] | None = None) -> list[dict[str, Any]]:
        """Build a suggested test plan without executing tests."""
        detected_frameworks = self.detect_frameworks()
        plan: list[dict[str, Any]] = []

        for language, frameworks in detected_frameworks.items():
            for framework_config in frameworks:
                command = self._resolve_framework_command(framework_config)
                if not command:
                    continue

                selected_tests = self._select_target_files_for_framework(framework_config, target_files)
                command_used = command.copy()

                if framework_config.name == "go test" and not selected_tests:
                    command_used.append("./...")
                if selected_tests:
                    command_used.extend(selected_tests)

                plan.append(
                    {
                        "language": language,
                        "framework": framework_config.name,
                        "command": " ".join(command_used),
                        "selected_tests": selected_tests,
                    }
                )

        return plan

    def run_tests(
        self, target_files: list[str] | None = None, languages: list[str] | None = None, fast_mode: bool = False
    ) -> dict[str, list[TestResult]]:
        """Run detected test frameworks"""
        detected_frameworks = self.detect_frameworks()
        results = {}

        # Filter by requested languages
        if languages:
            detected_frameworks = {k: v for k, v in detected_frameworks.items() if k in languages}

        for language, frameworks in detected_frameworks.items():
            language_results = []

            for framework_config in frameworks:
                try:
                    result = self._run_single_framework(framework_config, target_files, fast_mode)
                    language_results.append(result)
                except Exception as e:
                    self.logger.error(f"Failed to run {framework_config.name}: {e}")
                    # Create error result
                    error_result = TestResult(
                        success=False,
                        framework=framework_config.name,
                        exit_code=-1,
                        stdout="",
                        stderr=str(e),
                        tests_run=0,
                        tests_passed=0,
                        tests_failed=1,
                        tests_skipped=0,
                        failures=[{"error": str(e)}],
                        duration=0.0,
                    )
                    language_results.append(error_result)

            if language_results:
                results[language] = language_results

        return results

    def _run_single_framework(
        self, framework_config: TestFrameworkConfig, target_files: list[str] | None = None, fast_mode: bool = False
    ) -> TestResult:
        """Run a single test framework and parse its output"""
        command = self._resolve_framework_command(framework_config)
        if not command:
            return TestResult(
                success=False,
                framework=framework_config.name,
                exit_code=-1,
                stdout="",
                stderr=f"Unable to resolve command for {framework_config.name}",
                tests_run=0,
                tests_passed=0,
                tests_failed=1,
                tests_skipped=0,
                failures=[{"error": f"Unable to resolve command for {framework_config.name}"}],
                duration=0.0,
            )

        selected_tests: list[str] = []

        # Add fast mode options
        if fast_mode:
            if framework_config.name == "pytest":
                command.extend(["-x", "--tb=no"])  # Stop on first failure, no traceback
            elif framework_config.name == "jest":
                command.extend(["--bail", "--silent"])

        if framework_config.name == "go test" and not target_files:
            command.append("./...")
        if framework_config.name == "cargo test" and target_files:
            target_files = None
        if framework_config.name in {"forge test", "hardhat test"} and target_files:
            target_files = None

        selected_tests = self._select_target_files_for_framework(framework_config, target_files)
        if selected_tests:
            command.extend(selected_tests)

        # Run the test framework
        try:
            import time

            start_time = time.time()

            # SURGICAL FIX: Add process group management to prevent zombie pytest processes
            # This ensures clean process termination and allows timeout to work properly
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout
                cwd=self.workspace_root,
                start_new_session=True,  # Create new process group for clean termination
            )

            duration = time.time() - start_time

            # Parse output using the appropriate parser
            parse_func = getattr(self, framework_config.parse_function)
            test_data = parse_func(result.stdout, result.stderr)

            return TestResult(
                success=result.returncode == 0,
                framework=framework_config.name,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                tests_run=test_data["tests_run"],
                tests_passed=test_data["tests_passed"],
                tests_failed=test_data["tests_failed"],
                tests_skipped=test_data["tests_skipped"],
                failures=test_data["failures"],
                duration=duration,
                command=command,
                selected_tests=selected_tests,
            )

        except subprocess.TimeoutExpired:
            return TestResult(
                success=False,
                framework=framework_config.name,
                exit_code=-1,
                stdout="",
                stderr="Tests timed out after 10 minutes",
                tests_run=0,
                tests_passed=0,
                tests_failed=1,
                tests_skipped=0,
                failures=[{"error": "Test timeout"}],
                duration=600.0,
                command=command,
                selected_tests=selected_tests,
            )

    def _parse_pytest_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse pytest text output"""
        data = {"tests_run": 0, "tests_passed": 0, "tests_failed": 0, "tests_skipped": 0, "failures": []}

        # Look for summary line like "5 failed, 3 passed, 1 skipped in 2.34s"
        summary_pattern = r"(\d+)\s+failed.*?(\d+)\s+passed.*?(\d+)\s+skipped"
        summary_match = re.search(summary_pattern, stdout)

        if summary_match:
            data["tests_failed"] = int(summary_match.group(1))
            data["tests_passed"] = int(summary_match.group(2))
            data["tests_skipped"] = int(summary_match.group(3))
        else:
            # Try simpler patterns
            failed_match = re.search(r"(\d+) failed", stdout)
            passed_match = re.search(r"(\d+) passed", stdout)
            skipped_match = re.search(r"(\d+) skipped", stdout)

            if failed_match:
                data["tests_failed"] = int(failed_match.group(1))
            if passed_match:
                data["tests_passed"] = int(passed_match.group(1))
            if skipped_match:
                data["tests_skipped"] = int(skipped_match.group(1))

        data["tests_run"] = data["tests_passed"] + data["tests_failed"] + data["tests_skipped"]

        # Extract failure details
        failure_pattern = r"FAILED (.+?) - (.+)"
        for match in re.finditer(failure_pattern, stdout):
            data["failures"].append({"test": match.group(1), "message": match.group(2)})

        return data

    def _parse_unittest_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse unittest text output"""
        data = {"tests_run": 0, "tests_passed": 0, "tests_failed": 0, "tests_skipped": 0, "failures": []}

        # Look for summary line like "Ran 10 tests in 0.123s"
        run_pattern = r"Ran (\d+) tests"
        run_match = re.search(run_pattern, stderr)
        if run_match:
            data["tests_run"] = int(run_match.group(1))

        # Check for failures and errors
        if "FAILED" in stderr:
            # Parse failure details
            failure_pattern = r"FAIL: (.+)"
            error_pattern = r"ERROR: (.+)"

            for match in re.finditer(failure_pattern, stderr):
                data["failures"].append({"test": match.group(1), "type": "failure"})

            for match in re.finditer(error_pattern, stderr):
                data["failures"].append({"test": match.group(1), "type": "error"})

            data["tests_failed"] = len(data["failures"])
            data["tests_passed"] = data["tests_run"] - data["tests_failed"]
        else:
            data["tests_passed"] = data["tests_run"]

        return data

    def _parse_jest_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse Jest JSON output"""
        data = {"tests_run": 0, "tests_passed": 0, "tests_failed": 0, "tests_skipped": 0, "failures": []}

        if stdout.strip():
            json_text = stdout.strip()
            if not json_text.startswith("{"):
                start = json_text.find("{")
                end = json_text.rfind("}")
                if start != -1 and end != -1 and end > start:
                    json_text = json_text[start : end + 1]

            try:
                result = json.loads(json_text)
                data["tests_run"] = result.get("numTotalTests", 0)
                data["tests_passed"] = result.get("numPassedTests", 0)
                data["tests_failed"] = result.get("numFailedTests", 0)
                data["tests_skipped"] = result.get("numPendingTests", 0)

                for test_result in result.get("testResults", []):
                    for assertion in test_result.get("assertionResults", []):
                        if assertion.get("status") == "failed":
                            failure_messages = assertion.get("failureMessages", [])
                            data["failures"].append(
                                {
                                    "test": assertion.get("fullName", ""),
                                    "message": failure_messages[0] if failure_messages else "",
                                }
                            )
                return data
            except json.JSONDecodeError:
                pass

        # Fallback to text parsing if JSON is unavailable
        summary_pattern = r"Tests:\s*(\d+)\s*failed.*?(\d+)\s*passed.*?(\d+)\s*total"
        summary_match = re.search(summary_pattern, stdout)

        if summary_match:
            data["tests_failed"] = int(summary_match.group(1))
            data["tests_passed"] = int(summary_match.group(2))
            data["tests_run"] = int(summary_match.group(3))

        failure_pattern = r"● (.+)"
        for match in re.finditer(failure_pattern, stdout):
            data["failures"].append({"test": match.group(1), "type": "failure"})

        return data

    def _parse_mocha_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse Mocha JSON output"""
        data = {"tests_run": 0, "tests_passed": 0, "tests_failed": 0, "tests_skipped": 0, "failures": []}

        try:
            if stdout.strip():
                result = json.loads(stdout)

                data["tests_run"] = result.get("stats", {}).get("tests", 0)
                data["tests_passed"] = result.get("stats", {}).get("passes", 0)
                data["tests_failed"] = result.get("stats", {}).get("failures", 0)
                data["tests_skipped"] = result.get("stats", {}).get("pending", 0)

                # Extract failure details
                for failure in result.get("failures", []):
                    data["failures"].append(
                        {
                            "test": failure.get("fullTitle", ""),
                            "message": failure.get("err", {}).get("message", ""),
                            "stack": failure.get("err", {}).get("stack", ""),
                        }
                    )

        except json.JSONDecodeError:
            self.logger.warning("Failed to parse Mocha JSON output")

        return data

    def _parse_vitest_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse Vitest JSON output."""
        data = {"tests_run": 0, "tests_passed": 0, "tests_failed": 0, "tests_skipped": 0, "failures": []}

        try:
            if stdout.strip():
                json_text = stdout.strip()
                if not json_text.startswith("{"):
                    start = json_text.find("{")
                    end = json_text.rfind("}")
                    if start != -1 and end != -1 and end > start:
                        json_text = json_text[start : end + 1]

                result = json.loads(json_text)
                data["tests_run"] = result.get("numTotalTests", 0)
                data["tests_passed"] = result.get("numPassedTests", 0)
                data["tests_failed"] = result.get("numFailedTests", 0)
                data["tests_skipped"] = result.get("numPendingTests", 0)

                for test_result in result.get("testResults", []):
                    for assertion in test_result.get("assertionResults", []):
                        if assertion.get("status") == "failed":
                            failure_messages = assertion.get("failureMessages", [])
                            data["failures"].append(
                                {
                                    "test": assertion.get("fullName", ""),
                                    "message": failure_messages[0] if failure_messages else "",
                                }
                            )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse Vitest JSON output")

        return data

    def _parse_go_test_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse go test JSON output."""
        data = {"tests_run": 0, "tests_passed": 0, "tests_failed": 0, "tests_skipped": 0, "failures": []}
        output_buffer: dict[str, list[str]] = {}

        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            action = event.get("Action")
            test_name = event.get("Test")
            if action == "output" and test_name:
                output_buffer.setdefault(test_name, []).append(event.get("Output", "").strip())
                continue
            if action in {"pass", "fail", "skip"} and test_name:
                if action == "pass":
                    data["tests_passed"] += 1
                elif action == "fail":
                    data["tests_failed"] += 1
                    message = "\n".join(output_buffer.get(test_name, []))
                    data["failures"].append(
                        {
                            "test": test_name,
                            "message": message,
                        }
                    )
                else:
                    data["tests_skipped"] += 1

        data["tests_run"] = data["tests_passed"] + data["tests_failed"] + data["tests_skipped"]

        if data["tests_run"] == 0 and stderr.strip():
            data["tests_failed"] = 1
            data["tests_run"] = 1
            data["failures"].append({"test": "", "message": stderr.strip()})

        return data

    def _parse_cargo_test_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse cargo test text output."""
        data = {"tests_run": 0, "tests_passed": 0, "tests_failed": 0, "tests_skipped": 0, "failures": []}
        combined = "\n".join([stdout, stderr])
        summary_pattern = r"test result: (?:ok|FAILED)\\.\\s+(\\d+) passed; (\\d+) failed; (\\d+) ignored; (\\d+) measured; (\\d+) filtered out"
        failure_pattern = r"^test (.+?) \\.{3} FAILED$"

        for line in combined.split("\n"):
            line = line.strip()
            if not line:
                continue
            summary_match = re.search(summary_pattern, line)
            if summary_match:
                data["tests_passed"] += int(summary_match.group(1))
                data["tests_failed"] += int(summary_match.group(2))
                data["tests_skipped"] += int(summary_match.group(3))
                continue
            failure_match = re.match(failure_pattern, line)
            if failure_match:
                data["failures"].append({"test": failure_match.group(1), "message": "test failed"})

        data["tests_run"] = data["tests_passed"] + data["tests_failed"] + data["tests_skipped"]
        if data["tests_run"] == 0 and data["failures"]:
            data["tests_failed"] = len(data["failures"])
            data["tests_run"] = data["tests_failed"]
        if data["tests_run"] == 0 and stderr.strip():
            data["tests_failed"] = 1
            data["tests_run"] = 1
            data["failures"].append({"test": "", "message": stderr.strip()})

        return data

    def _parse_forge_test_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse forge test JSON output."""
        data = {"tests_run": 0, "tests_passed": 0, "tests_failed": 0, "tests_skipped": 0, "failures": []}

        def _record_result(status: str | None, name: str = "", message: str = "") -> None:
            status_text = str(status or "").lower()
            if status_text in {"pass", "passed", "success", "ok"}:
                data["tests_passed"] += 1
            elif status_text in {"skip", "skipped"}:
                data["tests_skipped"] += 1
            else:
                data["tests_failed"] += 1
                data["failures"].append({"test": name, "message": message or "test failed"})

        payloads = []
        if stdout.strip():
            try:
                payloads.append(json.loads(stdout))
            except json.JSONDecodeError:
                for line in stdout.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        payloads.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

        for payload in payloads:
            if not isinstance(payload, dict):
                continue
            results = payload.get("results")
            if isinstance(results, dict):
                for file_results in results.values():
                    if not isinstance(file_results, dict):
                        continue
                    for contract_results in file_results.values():
                        if not isinstance(contract_results, dict):
                            continue
                        for test_name, test_result in contract_results.items():
                            if not isinstance(test_result, dict):
                                continue
                            status = test_result.get("status") or test_result.get("result")
                            success = test_result.get("success")
                            if status is None and success is not None:
                                status = "pass" if success else "fail"
                            message = (
                                test_result.get("reason")
                                or test_result.get("error")
                                or test_result.get("message")
                                or ""
                            )
                            _record_result(status, test_name, message)
                continue

            status = payload.get("status") or payload.get("result")
            success = payload.get("success")
            if status is None and success is not None:
                status = "pass" if success else "fail"
            if status is not None:
                name = payload.get("test") or payload.get("name") or ""
                message = payload.get("reason") or payload.get("error") or payload.get("message") or ""
                _record_result(status, name, message)

        data["tests_run"] = data["tests_passed"] + data["tests_failed"] + data["tests_skipped"]
        if data["tests_run"] == 0 and stderr.strip():
            data["tests_failed"] = 1
            data["tests_run"] = 1
            data["failures"].append({"test": "", "message": stderr.strip()})

        return data

    def _parse_hardhat_test_output(self, stdout: str, stderr: str) -> dict[str, Any]:
        """Parse hardhat test output."""
        data = {"tests_run": 0, "tests_passed": 0, "tests_failed": 0, "tests_skipped": 0, "failures": []}
        combined = "\n".join([stdout, stderr])

        passing_match = re.search(r"(\d+)\s+passing", combined)
        failing_match = re.search(r"(\d+)\s+failing", combined)
        pending_match = re.search(r"(\d+)\s+pending", combined)

        if passing_match:
            data["tests_passed"] = int(passing_match.group(1))
        if failing_match:
            data["tests_failed"] = int(failing_match.group(1))
        if pending_match:
            data["tests_skipped"] = int(pending_match.group(1))

        for line in combined.split("\n"):
            match = re.match(r"^\s*\d+\)\s+(.+)$", line.strip())
            if match:
                data["failures"].append({"test": match.group(1), "message": "test failed"})

        data["tests_run"] = data["tests_passed"] + data["tests_failed"] + data["tests_skipped"]
        if data["tests_run"] == 0 and stderr.strip():
            data["tests_failed"] = 1
            data["tests_run"] = 1
            data["failures"].append({"test": "", "message": stderr.strip()})

        return data

    def get_summary(self, results: dict[str, list[TestResult]]) -> dict[str, Any]:
        """Generate a summary of test results"""
        total_run = 0
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        failed_frameworks = []
        successful_frameworks = []
        all_failures = []

        for language, framework_results in results.items():
            for result in framework_results:
                total_run += result.tests_run
                total_passed += result.tests_passed
                total_failed += result.tests_failed
                total_skipped += result.tests_skipped
                all_failures.extend(result.failures)

                if result.success:
                    successful_frameworks.append(f"{language}:{result.framework}")
                else:
                    failed_frameworks.append(f"{language}:{result.framework}")

        return {
            "total_run": total_run,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_skipped": total_skipped,
            "failed_frameworks": failed_frameworks,
            "successful_frameworks": successful_frameworks,
            "all_failures": all_failures,
            "overall_success": len(failed_frameworks) == 0 and total_failed == 0,
        }

    def should_block_commit(self, results: dict[str, list[TestResult]], allow_skipped: bool = True) -> tuple[bool, str]:
        """Determine if test results should block a commit"""
        summary = self.get_summary(results)

        if summary["failed_frameworks"]:
            return True, f"Test frameworks failed: {', '.join(summary['failed_frameworks'])}"

        if summary["total_failed"] > 0:
            return True, f"Found {summary['total_failed']} failing tests"

        if not allow_skipped and summary["total_skipped"] > 0:
            return True, f"Found {summary['total_skipped']} skipped tests"

        if summary["total_run"] == 0:
            return True, "No tests were run"

        return False, f"All {summary['total_passed']} tests passed"
