"""
Intelligent Test Selection Service

Provides test-to-source mapping and change-based test selection.
"""

import ast
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class TestSourceMapper:
    """Maps source files to their corresponding test files."""

    def __init__(self):
        self.source_to_tests: dict[str, set[str]] = {}
        self.test_to_sources: dict[str, set[str]] = {}
        self.test_metadata: dict[str, dict] = {}

    def build_mapping(self, project_root: str = ".") -> None:
        """Build comprehensive source-to-test mapping."""
        self._discover_test_files(project_root)
        self._analyze_import_relationships()
        self._build_naming_relationships()

    def _discover_test_files(self, project_root: str) -> None:
        """Discover all test files in the project."""
        test_patterns = ["test_*.py", "*_test.py"]
        test_dirs = ["tests/", "./"]

        for test_dir in test_dirs:
            test_path = Path(project_root) / test_dir
            if test_path.exists():
                for pattern in test_patterns:
                    for test_file in test_path.rglob(pattern):
                        if not any(part.startswith(".") for part in test_file.parts):
                            test_file_str = str(test_file.relative_to(project_root))
                            self._analyze_test_file(test_file_str, test_file)

    def _analyze_import_relationships(self) -> None:
        """Analyze import relationships between test files and source files."""
        # This method analyzes the import relationships discovered in test files
        # and maps them to source files for intelligent test selection
        pass

    def _analyze_test_file(self, test_file_path: str, test_file: Path) -> None:
        """Analyze a single test file for imports and dependencies."""
        try:
            with open(test_file) as f:
                content = f.read()

            # Parse AST to find imports
            tree = ast.parse(content)
            imports = self._extract_imports(tree)

            # Store test metadata
            self.test_metadata[test_file_path] = {
                "imports": imports,
                "functions": self._extract_test_functions(tree),
                "classes": self._extract_test_classes(tree),
            }

            # Map imports to source files
            for import_path in imports:
                source_file = self._import_to_source_file(import_path)
                if source_file:
                    if source_file not in self.source_to_tests:
                        self.source_to_tests[source_file] = set()
                    self.source_to_tests[source_file].add(test_file_path)

                    if test_file_path not in self.test_to_sources:
                        self.test_to_sources[test_file_path] = set()
                    self.test_to_sources[test_file_path].add(source_file)

        except Exception as e:
            logger.warning(f"Failed to analyze test file {test_file_path}: {e}")

    def _extract_imports(self, tree: ast.AST) -> list[str]:
        """Extract import statements from AST."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        imports.append(f"{node.module}.{alias.name}")
        return imports

    def _extract_test_functions(self, tree: ast.AST) -> list[str]:
        """Extract test function names."""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                functions.append(node.name)
        return functions

    def _extract_test_classes(self, tree: ast.AST) -> list[str]:
        """Extract test class names."""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and ("test" in node.name.lower() or node.name.startswith("Test")):
                classes.append(node.name)
        return classes

    def _import_to_source_file(self, import_path: str) -> str | None:
        """Convert import path to source file path."""
        # Handle relative imports within project
        if import_path.startswith("src.") or import_path.startswith("."):
            # Convert to file path
            parts = import_path.replace("src.", "").replace(".", "/").split(".")
            potential_paths = [
                f"src/{'/'.join(parts)}.py",
                f"{'/'.join(parts)}.py",
                f"src/{'/'.join(parts[:-1])}/__init__.py",
            ]

            for path in potential_paths:
                if os.path.exists(path):
                    return path

        return None

    def _build_naming_relationships(self) -> None:
        """Build relationships based on naming conventions."""
        # Find test files that match source files by naming convention
        test_files = list(self.test_metadata.keys())

        for test_file in test_files:
            # Extract potential source file names
            test_name = Path(test_file).stem

            # Common patterns: test_module.py -> module.py, module_test.py -> module.py
            if test_name.startswith("test_"):
                source_name = test_name[5:]  # Remove 'test_' prefix
            elif test_name.endswith("_test"):
                source_name = test_name[:-5]  # Remove '_test' suffix
            else:
                continue

            # Look for corresponding source files
            potential_sources = [
                f"src/{source_name}.py",
                f"src/{source_name}/__init__.py",
                f"{source_name}.py",
                f"src/tools/{source_name}.py",
                f"src/tools/commands/{source_name}.py",
            ]

            for source_path in potential_sources:
                if os.path.exists(source_path):
                    if source_path not in self.source_to_tests:
                        self.source_to_tests[source_path] = set()
                    self.source_to_tests[source_path].add(test_file)

                    if test_file not in self.test_to_sources:
                        self.test_to_sources[test_file] = set()
                    self.test_to_sources[test_file].add(source_path)

    def get_tests_for_source(self, source_file: str) -> list[str]:
        """Get test files that should run for a given source file."""
        return list(self.source_to_tests.get(source_file, set()))

    def get_tests_for_changes(self, changed_files: list[str]) -> list[str]:
        """Get test files that should run for a list of changed files."""
        relevant_tests = set()

        for file in changed_files:
            tests = self.get_tests_for_source(file)
            relevant_tests.update(tests)

        return list(relevant_tests)


class IntelligentTestSelector:
    """Combines multiple strategies to select relevant tests."""

    def __init__(self, git_ops):
        self.git_ops = git_ops
        self.mapper = TestSourceMapper()
        self.mapper.build_mapping()

    def select_tests_for_changes(self, max_tests: int = 20) -> list[str]:
        """Select tests based on recent changes."""
        changed_files = self.git_ops.get_modified_files()
        if not changed_files:
            changed_files = self.git_ops.get_changed_files("HEAD~1")

        if not changed_files:
            # No changes detected, return subset of all tests
            return self._get_default_test_selection(max_tests)

        # Get tests directly related to changes
        relevant_tests = self.mapper.get_tests_for_changes(changed_files)

        # If not enough relevant tests, add default tests
        if len(relevant_tests) < max_tests:
            default_tests = self._get_default_test_selection(max_tests - len(relevant_tests))
            for test in default_tests:
                if test not in relevant_tests:
                    relevant_tests.append(test)

        return relevant_tests[:max_tests]

    def _get_default_test_selection(self, max_tests: int) -> list[str]:
        """Get default test selection when no changes detected."""
        all_tests = list(self.mapper.test_metadata.keys())

        # Prioritize core tests
        priority_patterns = ["test_phase9_", "test_connection", "test_validation", "test_agent"]

        priority_tests = []
        other_tests = []

        for test in all_tests:
            if any(pattern in test for pattern in priority_patterns):
                priority_tests.append(test)
            else:
                other_tests.append(test)

        # Return mix of priority and other tests
        selected = priority_tests[: max_tests // 2] + other_tests[: max_tests // 2]
        return selected[:max_tests]
