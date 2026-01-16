"""
Testing Phase Improvements for CCE Agent

This module contains the improved testing phase functionality that extends
the existing Step 14 implementation with smart test discovery, intelligent
validation scoping, incremental retries, and targeted fix strategies.

These improvements leverage existing tools from the codebase:
- src/deep_agents/code_analyzer.py for AST analysis
- src/tools/git_ops.py for change detection
- src/tools/validation/* for validation frameworks
"""

import logging
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

# Import existing tools that we'll leverage
from src.deep_agents.code_analyzer import analyze_python_file
from src.models import TestAttempt
from src.tools.git_ops import GitOps
from src.tools.shell_runner import ShellRunner

logger = logging.getLogger(__name__)


@dataclass
class TestRelevanceScore:
    """Scoring information for test relevance"""

    test_file: str
    score: int
    reasons: list[str]
    import_matches: list[str]
    name_matches: list[str]
    recently_modified: bool


@dataclass
class RetryState:
    """State tracking for incremental retries"""

    attempt: int
    max_attempts: int
    attempted_fixes: list[str]
    successful_fixes: list[str]
    persistent_errors: list[str]
    validation_cache: dict[str, Any]
    error_categories: dict[str, list[str]]


@dataclass
class ValidationScope:
    """Scope definition for targeted validation"""

    files: list[str]
    lines: dict[str, list[int]]
    error_types: list[str]
    severity_threshold: str


def get_max_test_retries(default: int = 5) -> int:
    """Read MAX test retries from env with safe defaults."""
    raw_value = os.getenv("CCE_MAX_TEST_RETRIES", str(default))
    try:
        parsed = int(raw_value)
    except ValueError:
        return default
    return max(parsed, 1)


def should_retry_test_failure(attempt_number: int, max_attempts: int, has_failures: bool) -> bool:
    """Decide whether to retry tests based on attempt count and failures."""
    return has_failures and attempt_number < max_attempts


def build_test_attempt(
    test_path: str,
    attempt_number: int,
    passed: bool,
    failure_reason: str | None = None,
    fix_applied: str | None = None,
) -> TestAttempt:
    """Construct a TestAttempt record with consistent defaults."""
    return TestAttempt(
        test_path=test_path,
        attempt_number=attempt_number,
        passed=passed,
        failure_reason=failure_reason,
        fix_applied=fix_applied,
        timestamp=datetime.now(),
    )


class SmartTestDiscovery:
    """Smart test discovery using AST-based dependency analysis"""

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.git_ops = GitOps(ShellRunner(workspace_root))
        self.logger = logging.getLogger(__name__)

    def discover_relevant_tests(self, changed_files: list[str]) -> list[str]:
        """
        Discover tests relevant to changed files using dependency analysis.

        Args:
            changed_files: List of files that were changed

        Returns:
            List of relevant test files, ordered by relevance score
        """
        try:
            self.logger.info(f"🔍 [SMART DISCOVERY] Analyzing {len(changed_files)} changed files")

            if not changed_files:
                return self._fallback_test_discovery()

            # Step 1: Analyze changed files to understand their structure
            file_dependencies = {}
            for file_path in changed_files:
                if file_path.endswith(".py") and os.path.exists(file_path):
                    dependencies = self._analyze_file_dependencies(file_path)
                    file_dependencies[file_path] = dependencies

            # Step 2: Find all potential test files
            potential_tests = self._find_test_files()

            # Step 3: Score each test file for relevance
            test_scores = []
            for test_file in potential_tests:
                score = self._score_test_relevance(test_file, changed_files, file_dependencies)
                if score.score > 0:
                    test_scores.append(score)

            # Step 4: Sort by score and return top results
            test_scores.sort(key=lambda x: x.score, reverse=True)

            # Limit to top 10 most relevant tests to avoid overwhelming
            relevant_tests = [score.test_file for score in test_scores[:10]]

            self.logger.info(f"✅ [SMART DISCOVERY] Found {len(relevant_tests)} relevant tests")
            for score in test_scores[:5]:  # Log top 5 for debugging
                self.logger.info(f"   📋 {score.test_file} (score: {score.score}) - {', '.join(score.reasons[:2])}")

            return relevant_tests

        except Exception as e:
            self.logger.error(f"❌ [SMART DISCOVERY] Failed: {e}")
            return self._fallback_test_discovery()

    def _analyze_file_dependencies(self, file_path: str) -> dict[str, Any]:
        """Analyze a Python file's dependencies using existing code analyzer"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Use existing AST analyzer
            structure = analyze_python_file(content, file_path)

            return {
                "imports": structure.imports,
                "classes": [cls["name"] for cls in structure.classes],
                "functions": [func["name"] for func in structure.functions],
                "constants": [const["name"] for const in structure.constants],
                "file_path": file_path,
                "structure": structure,
            }

        except Exception as e:
            self.logger.warning(f"⚠️ [SMART DISCOVERY] Failed to analyze {file_path}: {e}")
            return {"imports": [], "classes": [], "functions": [], "constants": []}

    def _find_test_files(self) -> list[str]:
        """Find all potential test files in the workspace"""
        test_files = []

        # Common test patterns
        test_patterns = ["test_*.py", "*_test.py", "tests.py"]

        # Common test directories
        test_dirs = ["tests", "test", "src/tests", "src/test"]

        try:
            # Search in test directories
            for test_dir in test_dirs:
                test_dir_path = os.path.join(self.workspace_root, test_dir)
                if os.path.exists(test_dir_path):
                    for root, dirs, files in os.walk(test_dir_path):
                        for file in files:
                            if file.endswith(".py") and any(
                                file.startswith("test_") or file.endswith("_test.py") or file == "tests.py"
                                for _ in [None]
                            ):
                                test_files.append(os.path.join(root, file))

            # Also search for test files alongside source files - GENERIC approach
            for root, dirs, files in os.walk(os.path.join(self.workspace_root, "src")):
                for file in files:
                    if (file.startswith("test_") or file.endswith("_test.py")) and file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        # GENERIC: Only include if it actually contains test functions/classes
                        if self._contains_test_functions(file_path):
                            test_files.append(file_path)

        except Exception as e:
            self.logger.warning(f"⚠️ [SMART DISCOVERY] Error finding test files: {e}")

        return list(set(test_files))  # Remove duplicates

    def _contains_test_functions(self, file_path: str) -> bool:
        """
        GENERIC: Check if a file actually contains test functions or classes.

        Looks for:
        1. Test functions: def test_*
        2. Test classes that inherit from unittest.TestCase or contain test methods
        3. Pytest-style test classes with test methods
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            import re

            # Check for test functions (most reliable indicator)
            if re.search(r"def test_\w+\(", content):
                return True

            # Check for test classes - but be more strict
            test_class_matches = re.findall(r"class (Test\w+):", content)
            if test_class_matches:
                # GENERIC: Check if the test class actually contains test methods or inherits from TestCase
                for class_name in test_class_matches:
                    # Look for test methods within the class
                    class_content_pattern = rf"class {re.escape(class_name)}:.*?(?=class|\Z)"
                    class_match = re.search(class_content_pattern, content, re.DOTALL)
                    if class_match:
                        class_content = class_match.group(0)
                        # Check for test methods or TestCase inheritance
                        if (
                            re.search(r"def test_\w+\(", class_content)
                            or "TestCase" in class_content
                            or "@pytest" in class_content
                        ):
                            return True

            return False
        except Exception:
            return False  # If we can't read it, assume it's not a test

    def _score_test_relevance(
        self, test_file: str, changed_files: list[str], file_dependencies: dict[str, Any]
    ) -> TestRelevanceScore:
        """Score a test file's relevance to changed files"""
        score = 0
        reasons = []
        import_matches = []
        name_matches = []

        try:
            # Analyze the test file
            test_dependencies = self._analyze_file_dependencies(test_file)

            # Score 1: Direct import relationships (highest priority)
            for changed_file in changed_files:
                if changed_file in file_dependencies:
                    changed_deps = file_dependencies[changed_file]

                    # Check if test imports from changed file
                    changed_module = self._file_path_to_module(changed_file)
                    for test_import in test_dependencies["imports"]:
                        if changed_module and changed_module in test_import:
                            score += 100
                            reasons.append(f"imports from {changed_module}")
                            import_matches.append(test_import)

                    # Check if test imports same modules as changed file
                    for changed_import in changed_deps["imports"]:
                        if changed_import in test_dependencies["imports"]:
                            score += 20
                            reasons.append(f"shares import: {changed_import}")
                            import_matches.append(changed_import)

            # Score 2: Naming conventions (medium priority)
            for changed_file in changed_files:
                changed_basename = os.path.basename(changed_file).replace(".py", "")
                test_basename = os.path.basename(test_file).replace(".py", "")

                # Direct naming match
                if f"test_{changed_basename}" == test_basename or f"{changed_basename}_test" == test_basename:
                    score += 80
                    reasons.append(f"naming match with {changed_basename}")
                    name_matches.append(changed_basename)

                # Partial naming match
                elif (
                    changed_basename in test_basename
                    or test_basename.replace("test_", "").replace("_test", "") in changed_basename
                ):
                    score += 40
                    reasons.append(f"partial naming match with {changed_basename}")
                    name_matches.append(changed_basename)

            # Score 3: Directory proximity (low priority)
            for changed_file in changed_files:
                changed_dir = os.path.dirname(changed_file)
                test_dir = os.path.dirname(test_file)

                if changed_dir in test_dir or test_dir in changed_dir:
                    score += 10
                    reasons.append("in related directory")

            # Score 4: Recent modifications (bonus)
            recently_modified = self._is_recently_modified(test_file)
            if recently_modified:
                score += 5
                reasons.append("recently modified")

        except Exception as e:
            self.logger.warning(f"⚠️ [SMART DISCOVERY] Failed to score {test_file}: {e}")

        return TestRelevanceScore(
            test_file=test_file,
            score=score,
            reasons=reasons,
            import_matches=import_matches,
            name_matches=name_matches,
            recently_modified=recently_modified,
        )

    def _file_path_to_module(self, file_path: str) -> str | None:
        """Convert file path to Python module name"""
        try:
            # Remove workspace root and convert to module notation
            relative_path = os.path.relpath(file_path, self.workspace_root)
            module_path = relative_path.replace("/", ".").replace("\\", ".").replace(".py", "")

            # Handle common patterns
            if module_path.startswith("src."):
                return module_path
            elif not module_path.startswith("."):
                return f"src.{module_path}"

            return module_path

        except Exception:
            return None

    def _is_recently_modified(self, file_path: str) -> bool:
        """Check if file was recently modified using git"""
        try:
            # Check if file was modified in last 10 commits
            recent_files = self.git_ops.get_changed_files("HEAD~10")
            return file_path in recent_files
        except Exception:
            return False

    def _fallback_test_discovery(self) -> list[str]:
        """Fallback test discovery when smart discovery fails"""
        self.logger.warning("🔄 [SMART DISCOVERY] Using fallback discovery")

        # Find a few basic test files to run
        fallback_tests = []
        test_patterns = ["tests/test*.py", "src/tests/test*.py"]

        for pattern in test_patterns:
            pattern_path = os.path.join(self.workspace_root, pattern.replace("*", ""))
            if os.path.exists(os.path.dirname(pattern_path)):
                for root, dirs, files in os.walk(os.path.dirname(pattern_path)):
                    for file in files[:3]:  # Limit to first 3 files
                        if file.startswith("test_") and file.endswith(".py"):
                            fallback_tests.append(os.path.join(root, file))
                    break  # Only check first level

        return fallback_tests[:5]  # Return max 5 fallback tests


class IntelligentValidationScoping:
    """Intelligent validation scoping to reduce linting noise"""

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.git_ops = GitOps(ShellRunner(workspace_root))
        self.logger = logging.getLogger(__name__)

    def create_validation_scope(self, changed_files: list[str]) -> ValidationScope:
        """
        Create a focused validation scope based on changed files and lines.

        Args:
            changed_files: List of files that were changed

        Returns:
            ValidationScope object defining what to validate
        """
        try:
            self.logger.info(f"🎯 [VALIDATION SCOPE] Creating scope for {len(changed_files)} files")

            if not changed_files:
                return ValidationScope(files=[], lines={}, error_types=["syntax", "import"], severity_threshold="error")

            # Get actual changed lines using git diff
            changed_lines = self._get_changed_lines(changed_files)

            # Define validation scope
            scope = ValidationScope(
                files=changed_files[:5],  # Limit to 5 most important files
                lines=changed_lines,
                error_types=["syntax", "import", "undefined"],  # Focus on critical errors
                severity_threshold="warning",  # Include warnings, but filter later
            )

            self.logger.info(
                f"✅ [VALIDATION SCOPE] Scope created: {len(scope.files)} files, "
                f"{sum(len(lines) for lines in scope.lines.values())} lines"
            )

            return scope

        except Exception as e:
            self.logger.error(f"❌ [VALIDATION SCOPE] Failed to create scope: {e}")
            # Return minimal scope
            return ValidationScope(
                files=changed_files[:3], lines={}, error_types=["syntax"], severity_threshold="error"
            )

    def _get_changed_lines(self, changed_files: list[str]) -> dict[str, list[int]]:
        """Get specific line numbers that changed using git diff"""
        changed_lines = {}

        try:
            diff_output = self.git_ops.git_diff()
            if not diff_output or diff_output == "No changes to diff.":
                # Fallback: assume all lines in small files are relevant
                for file_path in changed_files:
                    if os.path.exists(file_path):
                        try:
                            with open(file_path, encoding="utf-8") as f:
                                total_lines = len(f.readlines())
                            # For small files, validate all lines
                            if total_lines <= 50:
                                changed_lines[file_path] = list(range(1, total_lines + 1))
                            else:
                                # For larger files, validate first 20 lines as sample
                                changed_lines[file_path] = list(range(1, 21))
                        except Exception:
                            changed_lines[file_path] = []
                return changed_lines

            # Parse git diff output to extract changed line numbers
            current_file = None
            for line in diff_output.split("\n"):
                if line.startswith("diff --git"):
                    # Extract file path from diff header
                    match = re.search(r"b/(.+)$", line)
                    if match:
                        current_file = match.group(1)
                        if current_file in changed_files:
                            changed_lines[current_file] = []
                        else:
                            current_file = None

                elif line.startswith("@@") and current_file:
                    # Parse hunk header to get line numbers: @@ -old_start,old_count +new_start,new_count @@
                    match = re.search(r"\+(\d+)(?:,(\d+))?", line)
                    if match:
                        new_start = int(match.group(1))
                        new_count = int(match.group(2)) if match.group(2) else 1
                        # Add the changed line range
                        line_range = list(range(new_start, new_start + new_count))
                        changed_lines[current_file].extend(line_range)

        except Exception as e:
            self.logger.warning(f"⚠️ [VALIDATION SCOPE] Failed to parse diff: {e}")

        return changed_lines

    def filter_validation_results(self, validation_output: str, scope: ValidationScope) -> str:
        """Filter validation results to only actionable issues within scope"""
        try:
            if not validation_output:
                return "No validation issues found."

            lines = validation_output.split("\n")
            filtered_lines = []
            actionable_count = 0

            for line in lines:
                # Check if this is an issue line (typically contains file:line: format)
                issue_match = re.search(r"([^:]+):(\d+):", line)
                if issue_match:
                    file_path = issue_match.group(1)
                    line_num = int(issue_match.group(2))

                    # Check if this file is in our scope
                    if any(
                        file_path.endswith(scoped_file) or scoped_file.endswith(file_path)
                        for scoped_file in scope.files
                    ):
                        # Check if this line is in our changed lines (if we have specific lines)
                        if scope.lines:
                            relevant_lines = []
                            for scoped_file in scope.files:
                                if file_path.endswith(scoped_file) or scoped_file.endswith(file_path):
                                    relevant_lines.extend(scope.lines.get(scoped_file, []))

                            if relevant_lines and line_num not in relevant_lines:
                                continue  # Skip issues on unchanged lines

                        # Check severity (filter out info-level issues)
                        if "error" in line.lower() or "warning" in line.lower() or scope.severity_threshold == "info":
                            filtered_lines.append(line)
                            actionable_count += 1
                else:
                    # Include context lines and summaries
                    if line.strip() and not line.startswith(" "):
                        filtered_lines.append(line)

            if actionable_count == 0:
                return "✅ No actionable validation issues found in changed areas."

            result = f"🎯 Filtered validation results ({actionable_count} actionable issues):\n"
            result += "\n".join(filtered_lines)

            return result

        except Exception as e:
            self.logger.error(f"❌ [VALIDATION SCOPE] Failed to filter results: {e}")
            return validation_output  # Return original if filtering fails


class ErrorCategorization:
    """Categorize and prioritize different types of errors"""

    ERROR_PATTERNS = {
        "syntax_errors": [
            r"SyntaxError:",
            r"invalid syntax",
            r"unexpected token",
            r"missing \):",
            r"missing :",
        ],
        "import_errors": [
            r"ImportError:",
            r"ModuleNotFoundError:",
            r"No module named",
            r"cannot import name",
            r"ERROR collecting.*ImportError",
            r"Hint: make sure your test modules",
        ],
        "collection_errors": [
            r"ERROR collecting",
            r"Interrupted: \d+ error during collection",
            r"no tests collected.*error",
            r"Test command completed with exit code [1-9]",  # Any non-zero exit code
        ],
        "undefined_variables": [
            r"NameError:",
            r"name .+ is not defined",
            r"undefined variable",
        ],
        "runtime_errors": [
            r"AttributeError:",
            r"TypeError:",
            r"ValueError:",
            r"KeyError:",
            r"IndexError:",
            r"RuntimeError:",
        ],
        "test_assertion_failures": [
            r"AssertionError:",
            r"assert .+ failed",
            r"expected .+ but got",
        ],
        "style_issues": [
            r"E\d+:",  # PEP8 error codes
            r"W\d+:",  # PEP8 warning codes
            r"line too long",
            r"trailing whitespace",
        ],
    }

    ERROR_PRIORITY = {
        "collection_errors": 90,  # High priority - tests can't even run
        "syntax_errors": 100,
        "import_errors": 80,
        "runtime_errors": 70,
        "undefined_variables": 60,
        "test_assertion_failures": 40,
        "style_issues": 20,
    }

    @classmethod
    def categorize_error(cls, error_text: str) -> tuple[str, int]:
        """Categorize an error and return its category and priority"""
        for category, patterns in cls.ERROR_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, error_text, re.IGNORECASE):
                    priority = cls.ERROR_PRIORITY.get(category, 0)
                    return category, priority

        return "unknown", 0

    @classmethod
    def categorize_errors(cls, error_list: list[str]) -> dict[str, list[str]]:
        """Categorize a list of errors by type"""
        categories = {cat: [] for cat in cls.ERROR_PATTERNS.keys()}
        categories["unknown"] = []

        for error in error_list:
            category, _ = cls.categorize_error(error)
            categories[category].append(error)

        return categories

    @classmethod
    def get_retry_strategy(cls, attempt: int, error_categories: dict[str, list[str]]) -> dict[str, Any]:
        """
        GENERIC retry strategy that focuses on the error category with the most errors.

        This prevents the bug where we focus on categories with no errors.
        """
        # GENERIC FIX: Find the error category with the most errors
        error_counts = {}
        for category, errors in error_categories.items():
            if errors and category != "unknown":  # Exclude unknown and empty categories
                error_counts[category] = len(errors)

        # If no errors found, fall back to default
        if not error_counts:
            return {"focus": "syntax_errors", "max_fixes": 3, "scope": "file_level", "timeout": 90}

        # GENERIC: Sort by error count and priority, then select the best focus
        priority_order = cls.ERROR_PRIORITY

        # Sort by: 1) Error count (descending), 2) Priority (descending)
        sorted_categories = sorted(
            error_counts.items(), key=lambda x: (x[1], priority_order.get(x[0], 0)), reverse=True
        )

        focus_category = sorted_categories[0][0]  # Category with most errors and highest priority
        error_count = sorted_categories[0][1]

        # GENERIC: Determine scope and timeout based on error type and attempt
        if focus_category in ["syntax_errors", "undefined_variables"]:
            scope = "specific_lines"
            base_timeout = 60
        elif focus_category in ["import_errors", "collection_errors"]:
            scope = "file_level"
            base_timeout = 90
        else:
            scope = "full_context"
            base_timeout = 120

        # Increase timeout for later attempts and more errors
        timeout = base_timeout + (attempt - 1) * 30 + min(error_count * 10, 60)

        # More fixes for categories with more errors
        max_fixes = min(3 + error_count, 7)  # Scale with error count, cap at 7

        return {"focus": focus_category, "max_fixes": max_fixes, "scope": scope, "timeout": timeout}
