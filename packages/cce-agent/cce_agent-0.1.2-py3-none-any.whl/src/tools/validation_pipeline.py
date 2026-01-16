"""
Structured Validation Pipeline

Comprehensive validation system with syntax, security, and quality checks.
Provides structured validation results with actionable feedback.
"""

import logging
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from src.tools.openswe.treesitter_tools import TreeSitterAnalyzer

logger = logging.getLogger(__name__)


@dataclass
class ValidationIssue:
    """Represents a validation issue"""

    severity: str  # error, warning, info
    category: str  # syntax, security, quality, performance
    message: str
    file_path: str
    line_number: int | None = None
    column_number: int | None = None
    rule_id: str | None = None
    suggestion: str | None = None
    context: str | None = None


@dataclass
class ValidationResult:
    """Results of validation pipeline"""

    success: bool
    total_issues: int
    errors: int
    warnings: int
    info: int
    issues: list[ValidationIssue] = field(default_factory=list)
    files_validated: list[str] = field(default_factory=list)
    validation_time: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_issue(self, issue: ValidationIssue):
        """Add a validation issue"""
        self.issues.append(issue)
        self.total_issues += 1

        if issue.severity == "error":
            self.errors += 1
        elif issue.severity == "warning":
            self.warnings += 1
        else:
            self.info += 1

    def get_issues_by_category(self, category: str) -> list[ValidationIssue]:
        """Get issues filtered by category"""
        return [issue for issue in self.issues if issue.category == category]

    def get_issues_by_severity(self, severity: str) -> list[ValidationIssue]:
        """Get issues filtered by severity"""
        return [issue for issue in self.issues if issue.severity == severity]


class ValidationPipeline:
    """Comprehensive validation pipeline with multiple check types"""

    def __init__(self, workspace_root: str):
        """
        Initialize validation pipeline.

        Args:
            workspace_root: Root path of the workspace to validate
        """
        self.workspace_root = Path(workspace_root).resolve()
        self.logger = logging.getLogger(__name__)
        self.analyzer = TreeSitterAnalyzer()

        # Security patterns to check for
        self.security_patterns = {
            "python": [
                (r"eval\s*\(", "Use of eval() function", "DANGEROUS_EVAL"),
                (r"exec\s*\(", "Use of exec() function", "DANGEROUS_EXEC"),
                (r"__import__\s*\(", "Use of __import__() function", "DANGEROUS_IMPORT"),
                (r"pickle\.loads?\s*\(", "Use of pickle.loads()", "DANGEROUS_PICKLE"),
                (r"os\.system\s*\(", "Use of os.system()", "DANGEROUS_SYSTEM"),
                (r"subprocess\.call\s*\(", "Use of subprocess.call()", "DANGEROUS_SUBPROCESS"),
                (r"input\s*\(", "Use of input() without validation", "UNVALIDATED_INPUT"),
                (r"raw_input\s*\(", "Use of raw_input() without validation", "UNVALIDATED_INPUT"),
            ],
            "javascript": [
                (r"eval\s*\(", "Use of eval() function", "DANGEROUS_EVAL"),
                (r"Function\s*\(", "Use of Function constructor", "DANGEROUS_FUNCTION"),
                (r"setTimeout\s*\([^,]*,\s*[^)]*\)", "Use of setTimeout with string", "DANGEROUS_SETTIMEOUT"),
                (r"setInterval\s*\([^,]*,\s*[^)]*\)", "Use of setInterval with string", "DANGEROUS_SETINTERVAL"),
                (r"document\.write\s*\(", "Use of document.write()", "DANGEROUS_DOCUMENT_WRITE"),
                (r"innerHTML\s*=", "Direct innerHTML assignment", "DANGEROUS_INNERHTML"),
            ],
            "java": [
                (r"Runtime\.getRuntime\(\)\.exec\s*\(", "Use of Runtime.exec()", "DANGEROUS_RUNTIME_EXEC"),
                (r"ProcessBuilder\s*\(", "Use of ProcessBuilder", "DANGEROUS_PROCESS_BUILDER"),
                (r"Class\.forName\s*\(", "Use of Class.forName()", "DANGEROUS_CLASS_FORNAME"),
                (r"System\.getProperty\s*\(", "Use of System.getProperty()", "SENSITIVE_SYSTEM_PROPERTY"),
            ],
        }

        # Quality patterns to check for
        self.quality_patterns = {
            "python": [
                (r"print\s*\(", "Use of print() in production code", "QUALITY_PRINT"),
                (r"# TODO", "TODO comment found", "QUALITY_TODO"),
                (r"# FIXME", "FIXME comment found", "QUALITY_FIXME"),
                (r"# HACK", "HACK comment found", "QUALITY_HACK"),
                (r"pass\s*$", "Empty pass statement", "QUALITY_EMPTY_PASS"),
                (r"except\s*:", "Bare except clause", "QUALITY_BARE_EXCEPT"),
            ],
            "javascript": [
                (r"console\.log\s*\(", "Use of console.log() in production", "QUALITY_CONSOLE_LOG"),
                (r"debugger\s*;", "Debugger statement found", "QUALITY_DEBUGGER"),
                (r"// TODO", "TODO comment found", "QUALITY_TODO"),
                (r"// FIXME", "FIXME comment found", "QUALITY_FIXME"),
                (r"// HACK", "HACK comment found", "QUALITY_HACK"),
            ],
        }

    async def validate_syntax(self, files: list[str]) -> ValidationResult:
        """
        Validate syntax of files.

        Args:
            files: List of file paths to validate

        Returns:
            ValidationResult with syntax issues
        """
        result = ValidationResult(success=True, total_issues=0, errors=0, warnings=0, info=0)
        start_time = datetime.now()

        self.logger.info(f"Validating syntax for {len(files)} files")

        for file_path in files:
            try:
                full_path = self.workspace_root / file_path
                if not full_path.exists():
                    result.add_issue(
                        ValidationIssue(
                            severity="error",
                            category="syntax",
                            message=f"File not found: {file_path}",
                            file_path=file_path,
                            rule_id="FILE_NOT_FOUND",
                        )
                    )
                    continue

                # Detect language
                language = self._detect_language(file_path)

                # Use TreeSitter for syntax validation
                try:
                    analysis = await self.analyzer.analyze_file(str(full_path))

                    # Check for basic syntax issues
                    if analysis.line_count == 0:
                        result.add_issue(
                            ValidationIssue(
                                severity="warning",
                                category="syntax",
                                message="Empty file",
                                file_path=file_path,
                                rule_id="EMPTY_FILE",
                            )
                        )

                    # Check for missing imports/exports
                    if language == "python" and not analysis.imports:
                        result.add_issue(
                            ValidationIssue(
                                severity="info",
                                category="syntax",
                                message="No imports found - consider adding necessary imports",
                                file_path=file_path,
                                rule_id="NO_IMPORTS",
                            )
                        )

                except Exception as e:
                    result.add_issue(
                        ValidationIssue(
                            severity="error",
                            category="syntax",
                            message=f"Syntax analysis failed: {str(e)}",
                            file_path=file_path,
                            rule_id="SYNTAX_ANALYSIS_ERROR",
                        )
                    )

                result.files_validated.append(file_path)

            except Exception as e:
                self.logger.error(f"Failed to validate syntax for {file_path}: {e}")
                result.add_issue(
                    ValidationIssue(
                        severity="error",
                        category="syntax",
                        message=f"Validation failed: {str(e)}",
                        file_path=file_path,
                        rule_id="VALIDATION_ERROR",
                    )
                )

        result.validation_time = (datetime.now() - start_time).total_seconds()
        result.success = result.errors == 0

        self.logger.info(f"Syntax validation complete: {result.errors} errors, {result.warnings} warnings")
        return result

    async def validate_security(self, files: list[str]) -> ValidationResult:
        """
        Validate security of files.

        Args:
            files: List of file paths to validate

        Returns:
            ValidationResult with security issues
        """
        result = ValidationResult(success=True, total_issues=0, errors=0, warnings=0, info=0)
        start_time = datetime.now()

        self.logger.info(f"Validating security for {len(files)} files")

        for file_path in files:
            try:
                full_path = self.workspace_root / file_path
                if not full_path.exists():
                    continue

                # Detect language
                language = self._detect_language(file_path)

                # Read file content
                with open(full_path, encoding="utf-8") as f:
                    content = f.read()

                # Check security patterns
                security_patterns = self.security_patterns.get(language, [])

                for pattern, message, rule_id in security_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)

                    for match in matches:
                        line_number = content[: match.start()].count("\n") + 1
                        column_number = match.start() - content.rfind("\n", 0, match.start())

                        result.add_issue(
                            ValidationIssue(
                                severity="error",
                                category="security",
                                message=message,
                                file_path=file_path,
                                line_number=line_number,
                                column_number=column_number,
                                rule_id=rule_id,
                                suggestion="Consider using safer alternatives",
                                context=self._get_context_around_line(content, line_number),
                            )
                        )

                # Check for hardcoded secrets
                secret_patterns = [
                    (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password", "HARDCODED_PASSWORD"),
                    (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key", "HARDCODED_API_KEY"),
                    (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret", "HARDCODED_SECRET"),
                    (r'token\s*=\s*["\'][^"\']+["\']', "Hardcoded token", "HARDCODED_TOKEN"),
                ]

                for pattern, message, rule_id in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)

                    for match in matches:
                        line_number = content[: match.start()].count("\n") + 1

                        result.add_issue(
                            ValidationIssue(
                                severity="error",
                                category="security",
                                message=message,
                                file_path=file_path,
                                line_number=line_number,
                                rule_id=rule_id,
                                suggestion="Use environment variables or secure configuration",
                                context=self._get_context_around_line(content, line_number),
                            )
                        )

                result.files_validated.append(file_path)

            except Exception as e:
                self.logger.error(f"Failed to validate security for {file_path}: {e}")
                result.add_issue(
                    ValidationIssue(
                        severity="error",
                        category="security",
                        message=f"Security validation failed: {str(e)}",
                        file_path=file_path,
                        rule_id="SECURITY_VALIDATION_ERROR",
                    )
                )

        result.validation_time = (datetime.now() - start_time).total_seconds()
        result.success = result.errors == 0

        self.logger.info(f"Security validation complete: {result.errors} errors, {result.warnings} warnings")
        return result

    async def validate_quality(self, files: list[str]) -> ValidationResult:
        """
        Validate code quality of files.

        Args:
            files: List of file paths to validate

        Returns:
            ValidationResult with quality issues
        """
        result = ValidationResult(success=True, total_issues=0, errors=0, warnings=0, info=0)
        start_time = datetime.now()

        self.logger.info(f"Validating quality for {len(files)} files")

        for file_path in files:
            try:
                full_path = self.workspace_root / file_path
                if not full_path.exists():
                    continue

                # Detect language
                language = self._detect_language(file_path)

                # Read file content
                with open(full_path, encoding="utf-8") as f:
                    content = f.read()

                # Check quality patterns
                quality_patterns = self.quality_patterns.get(language, [])

                for pattern, message, rule_id in quality_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)

                    for match in matches:
                        line_number = content[: match.start()].count("\n") + 1
                        column_number = match.start() - content.rfind("\n", 0, match.start())

                        severity = "warning" if "TODO" in rule_id or "FIXME" in rule_id else "info"

                        result.add_issue(
                            ValidationIssue(
                                severity=severity,
                                category="quality",
                                message=message,
                                file_path=file_path,
                                line_number=line_number,
                                column_number=column_number,
                                rule_id=rule_id,
                                context=self._get_context_around_line(content, line_number),
                            )
                        )

                # Check for code complexity
                try:
                    analysis = await self.analyzer.analyze_file(str(full_path))

                    if analysis.complexity_score > 20:
                        result.add_issue(
                            ValidationIssue(
                                severity="warning",
                                category="quality",
                                message=f"High complexity score: {analysis.complexity_score}",
                                file_path=file_path,
                                rule_id="HIGH_COMPLEXITY",
                                suggestion="Consider refactoring to reduce complexity",
                            )
                        )

                    if analysis.line_count > 500:
                        result.add_issue(
                            ValidationIssue(
                                severity="info",
                                category="quality",
                                message=f"Large file: {analysis.line_count} lines",
                                file_path=file_path,
                                rule_id="LARGE_FILE",
                                suggestion="Consider splitting into smaller modules",
                            )
                        )

                except Exception as e:
                    self.logger.warning(f"Failed to analyze complexity for {file_path}: {e}")

                result.files_validated.append(file_path)

            except Exception as e:
                self.logger.error(f"Failed to validate quality for {file_path}: {e}")
                result.add_issue(
                    ValidationIssue(
                        severity="error",
                        category="quality",
                        message=f"Quality validation failed: {str(e)}",
                        file_path=file_path,
                        rule_id="QUALITY_VALIDATION_ERROR",
                    )
                )

        result.validation_time = (datetime.now() - start_time).total_seconds()
        result.success = result.errors == 0

        self.logger.info(f"Quality validation complete: {result.errors} errors, {result.warnings} warnings")
        return result

    async def validate_tests(self, test_pattern: str = "test_*.py") -> ValidationResult:
        """
        Validate test files and test coverage.

        Args:
            test_pattern: Pattern to match test files

        Returns:
            ValidationResult with test validation issues
        """
        result = ValidationResult(success=True, total_issues=0, errors=0, warnings=0, info=0)
        start_time = datetime.now()

        self.logger.info(f"Validating tests with pattern: {test_pattern}")

        try:
            # Find test files
            test_files = []
            # Look for test files in common test directories and src/
            test_directories = ["tests", "test", "src/tests", "src/test", "src"]
            scan_paths = []

            for test_dir in test_directories:
                test_path = os.path.join(self.workspace_root, test_dir)
                if os.path.exists(test_path):
                    scan_paths.append(test_path)

            # If no common test directories found, scan entire repository
            if not scan_paths:
                self.logger.warning(f"No common test directories found, scanning entire repository")
                scan_paths = [self.workspace_root]
            else:
                self.logger.info(
                    f"Scanning test directories: {[os.path.relpath(p, self.workspace_root) for p in scan_paths]}"
                )

            for scan_path in scan_paths:
                for root, dirs, files in os.walk(scan_path):
                    for file in files:
                        if file.endswith(".py") and ("test" in file.lower() or file.startswith("test_")):
                            test_files.append(os.path.relpath(os.path.join(root, file), self.workspace_root))

            if not test_files:
                result.add_issue(
                    ValidationIssue(
                        severity="warning",
                        category="quality",
                        message="No test files found",
                        file_path="workspace",
                        rule_id="NO_TESTS",
                        suggestion="Consider adding test files",
                    )
                )
            else:
                # Validate test files
                for test_file in test_files:
                    try:
                        full_path = self.workspace_root / test_file

                        with open(full_path, encoding="utf-8") as f:
                            content = f.read()

                        # Check for test functions
                        test_functions = re.findall(r"def\s+(test_\w+)", content)

                        if not test_functions:
                            result.add_issue(
                                ValidationIssue(
                                    severity="warning",
                                    category="quality",
                                    message="No test functions found",
                                    file_path=test_file,
                                    rule_id="NO_TEST_FUNCTIONS",
                                    suggestion="Add test functions starting with 'test_'",
                                )
                            )

                        # Check for assertions
                        assertions = re.findall(r"assert\s+", content)

                        if not assertions:
                            result.add_issue(
                                ValidationIssue(
                                    severity="info",
                                    category="quality",
                                    message="No assertions found in test file",
                                    file_path=test_file,
                                    rule_id="NO_ASSERTIONS",
                                    suggestion="Add assertions to validate test results",
                                )
                            )

                        result.files_validated.append(test_file)

                    except Exception as e:
                        self.logger.error(f"Failed to validate test file {test_file}: {e}")
                        result.add_issue(
                            ValidationIssue(
                                severity="error",
                                category="quality",
                                message=f"Test validation failed: {str(e)}",
                                file_path=test_file,
                                rule_id="TEST_VALIDATION_ERROR",
                            )
                        )

            # Try to run tests if pytest is available
            try:
                result_cmd = subprocess.run(
                    ["pytest", "--tb=short", "--quiet"],
                    cwd=self.workspace_root,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result_cmd.returncode != 0:
                    result.add_issue(
                        ValidationIssue(
                            severity="error",
                            category="quality",
                            message="Tests failed to run",
                            file_path="workspace",
                            rule_id="TESTS_FAILED",
                            context=result_cmd.stdout + result_cmd.stderr,
                        )
                    )
                else:
                    result.metadata["test_output"] = result_cmd.stdout

            except (subprocess.TimeoutExpired, FileNotFoundError):
                result.add_issue(
                    ValidationIssue(
                        severity="info",
                        category="quality",
                        message="pytest not available for test execution",
                        file_path="workspace",
                        rule_id="NO_PYTEST",
                    )
                )

        except Exception as e:
            self.logger.error(f"Test validation failed: {e}")
            result.add_issue(
                ValidationIssue(
                    severity="error",
                    category="quality",
                    message=f"Test validation failed: {str(e)}",
                    file_path="workspace",
                    rule_id="TEST_VALIDATION_ERROR",
                )
            )

        result.validation_time = (datetime.now() - start_time).total_seconds()
        result.success = result.errors == 0

        self.logger.info(f"Test validation complete: {result.errors} errors, {result.warnings} warnings")
        return result

    async def validate_all(self, files: list[str], include_tests: bool = True) -> ValidationResult:
        """
        Run all validation checks.

        Args:
            files: List of file paths to validate
            include_tests: Whether to include test validation

        Returns:
            Combined ValidationResult with all issues
        """
        self.logger.info(f"Running comprehensive validation for {len(files)} files")

        # Run all validation checks
        syntax_result = await self.validate_syntax(files)
        security_result = await self.validate_security(files)
        quality_result = await self.validate_quality(files)

        # Combine results
        combined_result = ValidationResult(
            success=True,
            total_issues=0,
            errors=0,
            warnings=0,
            info=0,
            files_validated=list(
                set(syntax_result.files_validated + security_result.files_validated + quality_result.files_validated)
            ),
            validation_time=syntax_result.validation_time
            + security_result.validation_time
            + quality_result.validation_time,
            metadata={
                "syntax_validation": {
                    "issues": syntax_result.total_issues,
                    "errors": syntax_result.errors,
                    "warnings": syntax_result.warnings,
                },
                "security_validation": {
                    "issues": security_result.total_issues,
                    "errors": security_result.errors,
                    "warnings": security_result.warnings,
                },
                "quality_validation": {
                    "issues": quality_result.total_issues,
                    "errors": quality_result.errors,
                    "warnings": quality_result.warnings,
                },
            },
        )

        # Add all issues
        for issue in syntax_result.issues + security_result.issues + quality_result.issues:
            combined_result.add_issue(issue)

        # Add test validation if requested
        if include_tests:
            test_result = await self.validate_tests()
            combined_result.validation_time += test_result.validation_time
            combined_result.metadata["test_validation"] = {
                "issues": test_result.total_issues,
                "errors": test_result.errors,
                "warnings": test_result.warnings,
            }

            for issue in test_result.issues:
                combined_result.add_issue(issue)

        combined_result.success = combined_result.errors == 0

        self.logger.info(
            f"Comprehensive validation complete: {combined_result.errors} errors, {combined_result.warnings} warnings, {combined_result.info} info"
        )
        return combined_result

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".mjs": "javascript",
            ".cjs": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".java": "java",
            ".cpp": "cpp",
            ".cc": "cpp",
            ".cxx": "cpp",
            ".c": "c",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".cs": "csharp",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
        }
        return language_map.get(ext, "unknown")

    def _get_context_around_line(self, content: str, line_number: int, context_lines: int = 3) -> str:
        """Get context around a specific line"""
        lines = content.split("\n")
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)

        context_lines_list = []
        for i in range(start, end):
            prefix = ">>> " if i == line_number - 1 else "    "
            context_lines_list.append(f"{prefix}{i + 1:4d}: {lines[i]}")

        return "\n".join(context_lines_list)


# Global instance for easy access
_validation_pipeline: ValidationPipeline | None = None


def get_validation_pipeline(workspace_root: str = None) -> ValidationPipeline:
    """Get or create global validation pipeline instance"""
    global _validation_pipeline

    if _validation_pipeline is None or (workspace_root and _validation_pipeline.workspace_root != Path(workspace_root)):
        if workspace_root is None:
            workspace_root = os.getcwd()
        _validation_pipeline = ValidationPipeline(workspace_root)

    return _validation_pipeline


__all__ = ["ValidationPipeline", "ValidationResult", "ValidationIssue", "get_validation_pipeline"]
