"""
Validation Pipeline - Linting Integration

AIDER-inspired linting integration for the CCE agent's validation pipeline.
Detects project linters and runs them with structured output parsing.
"""

import json
import logging
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .node_tooling import package_json_uses_tool, resolve_node_command


@dataclass
class LintResult:
    """Result of a linting operation"""

    success: bool
    linter: str
    exit_code: int
    stdout: str
    stderr: str
    issues: list[dict[str, Any]]
    total_issues: int
    error_count: int
    warning_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "linter": self.linter,
            "exit_code": self.exit_code,
            "stdout": self.stdout[:1000] + "..." if len(self.stdout) > 1000 else self.stdout,
            "stderr": self.stderr[:1000] + "..." if len(self.stderr) > 1000 else self.stderr,
            "issues": self.issues,
            "total_issues": self.total_issues,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
        }


@dataclass
class LinterConfig:
    """Configuration for a linter"""

    name: str
    command: list[str]
    config_files: list[str]
    extensions: list[str]
    output_format: str
    parse_function: str


class LintingManager:
    """Manages linting operations across different languages and tools"""

    _NODE_TOOL_NAMES = {"eslint", "tsc", "stylelint", "htmlhint", "solhint"}
    _PACKAGE_JSON_TOOL_CONFIGS = {"eslint": ["eslintConfig"], "stylelint": ["stylelint"], "htmlhint": ["htmlhint"]}
    _MAKEFILE_NAMES = {"Makefile", "makefile", "GNUmakefile"}

    # Linter configurations
    LINTERS = {
        "python": [
            LinterConfig(
                name="flake8",
                command=["flake8"],
                config_files=[".flake8", "setup.cfg", "tox.ini", "pyproject.toml"],
                extensions=[".py"],
                output_format="text",
                parse_function="_parse_flake8_text",
            ),
            LinterConfig(
                name="pylint",
                command=["pylint", "--output-format=json"],
                config_files=[".pylintrc", "pyproject.toml"],
                extensions=[".py"],
                output_format="json",
                parse_function="_parse_pylint_output",
            ),
            LinterConfig(
                name="mypy",
                command=["mypy", "--show-error-codes", "--show-column-numbers"],
                config_files=["mypy.ini", ".mypy.ini", "pyproject.toml", "setup.cfg"],
                extensions=[".py"],
                output_format="text",
                parse_function="_parse_mypy_output",
            ),
        ],
        "javascript": [
            LinterConfig(
                name="eslint",
                command=["eslint", "--format=json"],
                config_files=[
                    ".eslintrc",
                    ".eslintrc.js",
                    ".eslintrc.cjs",
                    ".eslintrc.json",
                    ".eslintrc.yml",
                    ".eslintrc.yaml",
                    "eslint.config.js",
                    "eslint.config.cjs",
                    "eslint.config.mjs",
                    "package.json",
                ],
                extensions=[".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx"],
                output_format="json",
                parse_function="_parse_eslint_output",
            )
        ],
        "typescript": [
            LinterConfig(
                name="tsc",
                command=["tsc", "--noEmit", "--pretty", "false"],
                config_files=["tsconfig.json"],
                extensions=[".ts", ".tsx"],
                output_format="text",
                parse_function="_parse_tsc_output",
            )
        ],
        "shell": [
            LinterConfig(
                name="shellcheck",
                command=["shellcheck", "-f", "json"],
                config_files=[".shellcheckrc"],
                extensions=[".sh", ".bash"],
                output_format="json",
                parse_function="_parse_shellcheck_output",
            )
        ],
        "powershell": [
            LinterConfig(
                name="PSScriptAnalyzer",
                command=[
                    "pwsh",
                    "-NoProfile",
                    "-Command",
                    "Invoke-ScriptAnalyzer -Path . -Recurse | ConvertTo-Json -Depth 5",
                ],
                config_files=["PSScriptAnalyzerSettings.psd1"],
                extensions=[".ps1", ".psm1"],
                output_format="json",
                parse_function="_parse_psscriptanalyzer_output",
            )
        ],
        "makefile": [
            LinterConfig(
                name="checkmake",
                command=["checkmake"],
                config_files=["Makefile", "makefile", "GNUmakefile"],
                extensions=[".mk"],
                output_format="text",
                parse_function="_parse_checkmake_output",
            )
        ],
        "yaml": [
            LinterConfig(
                name="yamllint",
                command=["yamllint", "-f", "parsable"],
                config_files=[".yamllint", ".yamllint.yml", ".yamllint.yaml"],
                extensions=[".yml", ".yaml"],
                output_format="text",
                parse_function="_parse_yamllint_output",
            )
        ],
        "json": [
            LinterConfig(
                name="jq",
                command=["jq", "."],
                config_files=[],
                extensions=[".json"],
                output_format="text",
                parse_function="_parse_jq_output",
            )
        ],
        "toml": [
            LinterConfig(
                name="taplo",
                command=["taplo", "check"],
                config_files=["taplo.toml", ".taplo.toml"],
                extensions=[".toml"],
                output_format="text",
                parse_function="_parse_taplo_output",
            )
        ],
        "sql": [
            LinterConfig(
                name="sqlfluff",
                command=["sqlfluff", "lint", "--format", "json"],
                config_files=[".sqlfluff", "pyproject.toml", "setup.cfg", "tox.ini"],
                extensions=[".sql"],
                output_format="json",
                parse_function="_parse_sqlfluff_output",
            ),
            LinterConfig(
                name="sqlfmt",
                command=["sqlfmt", "--check"],
                config_files=["pyproject.toml"],
                extensions=[".sql"],
                output_format="text",
                parse_function="_parse_sqlfmt_output",
            ),
        ],
        "terraform": [
            LinterConfig(
                name="tflint",
                command=["tflint", "--format", "json"],
                config_files=[".tflint.hcl"],
                extensions=[".tf", ".tfvars"],
                output_format="json",
                parse_function="_parse_tflint_output",
            ),
            LinterConfig(
                name="terraform validate",
                command=["terraform", "validate", "-json"],
                config_files=[],
                extensions=[".tf", ".tfvars"],
                output_format="json",
                parse_function="_parse_terraform_validate_output",
            ),
        ],
        "kubernetes": [
            LinterConfig(
                name="kubeval",
                command=["kubeval", "--output", "json"],
                config_files=[],
                extensions=[".yml", ".yaml"],
                output_format="json",
                parse_function="_parse_kubeval_output",
            ),
            LinterConfig(
                name="kube-linter",
                command=["kube-linter", "lint", "--format", "json"],
                config_files=[],
                extensions=[".yml", ".yaml"],
                output_format="json",
                parse_function="_parse_kube_linter_output",
            ),
        ],
        "github_actions": [
            LinterConfig(
                name="actionlint",
                command=["actionlint", "-format", "json"],
                config_files=[".github/actionlint.yaml", ".github/actionlint.yml"],
                extensions=[".yml", ".yaml"],
                output_format="json",
                parse_function="_parse_actionlint_output",
            )
        ],
        "solidity": [
            LinterConfig(
                name="solhint",
                command=["solhint", "--formatter", "json"],
                config_files=[
                    ".solhint.json",
                    ".solhint.yaml",
                    ".solhint.yml",
                    ".solhint.js",
                    ".solhint.cjs",
                ],
                extensions=[".sol"],
                output_format="json",
                parse_function="_parse_solhint_output",
            ),
            LinterConfig(
                name="slither",
                command=["slither", ".", "--json", "-"],
                config_files=[],
                extensions=[".sol"],
                output_format="json",
                parse_function="_parse_slither_output",
            ),
        ],
        "go": [
            LinterConfig(
                name="golangci-lint",
                command=["golangci-lint", "run", "--out-format", "json"],
                config_files=[".golangci.yml", ".golangci.yaml", ".golangci.toml"],
                extensions=[".go"],
                output_format="json",
                parse_function="_parse_golangci_output",
            ),
            LinterConfig(
                name="go vet",
                command=["go", "vet"],
                config_files=["go.mod"],
                extensions=[".go"],
                output_format="text",
                parse_function="_parse_go_vet_output",
            ),
        ],
        "rust": [
            LinterConfig(
                name="clippy",
                command=["cargo", "clippy", "--message-format", "json"],
                config_files=["Cargo.toml", "clippy.toml", ".clippy.toml"],
                extensions=[".rs"],
                output_format="json",
                parse_function="_parse_clippy_output",
            ),
            LinterConfig(
                name="rustfmt",
                command=["cargo", "fmt", "--check"],
                config_files=["Cargo.toml", "rustfmt.toml"],
                extensions=[".rs"],
                output_format="text",
                parse_function="_parse_rustfmt_output",
            ),
        ],
        "dockerfile": [
            LinterConfig(
                name="hadolint",
                command=["hadolint", "--format", "json"],
                config_files=[".hadolint.yaml", ".hadolint.yml", ".hadolint"],
                extensions=[".dockerfile"],
                output_format="json",
                parse_function="_parse_hadolint_output",
            ),
        ],
        "xml": [
            LinterConfig(
                name="xmllint",
                command=["xmllint", "--noout"],
                config_files=[],
                extensions=[".xml"],
                output_format="text",
                parse_function="_parse_xmllint_output",
            )
        ],
        "html": [
            LinterConfig(
                name="htmlhint",
                command=["htmlhint", "--format", "json"],
                config_files=[
                    ".htmlhintrc",
                    ".htmlhintrc.json",
                    ".htmlhintrc.js",
                    ".htmlhintrc.yml",
                    ".htmlhintrc.yaml",
                ],
                extensions=[".html", ".htm"],
                output_format="json",
                parse_function="_parse_htmlhint_output",
            )
        ],
        "css": [
            LinterConfig(
                name="stylelint",
                command=["stylelint", "--formatter", "json"],
                config_files=[
                    ".stylelintrc",
                    ".stylelintrc.json",
                    ".stylelintrc.yaml",
                    ".stylelintrc.yml",
                    ".stylelintrc.js",
                    ".stylelintrc.cjs",
                    ".stylelintrc.mjs",
                    "stylelint.config.js",
                    "stylelint.config.cjs",
                    "stylelint.config.mjs",
                    "package.json",
                ],
                extensions=[".css", ".scss", ".sass"],
                output_format="json",
                parse_function="_parse_stylelint_output",
            )
        ],
    }

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.logger = logging.getLogger(__name__)

        # Cache detected linters
        self._detected_linters: dict[str, list[LinterConfig]] | None = None

    def detect_linters(self, force_refresh: bool = False) -> dict[str, list[LinterConfig]]:
        """Detect available linters in the project"""
        if self._detected_linters and not force_refresh:
            return self._detected_linters

        detected = {}

        for language, linters in self.LINTERS.items():
            available_linters = []

            for linter_config in linters:
                resolved_command = self._resolve_linter_command(linter_config)
                if not resolved_command:
                    continue

                # Check if linter command is available
                if self._is_command_available(resolved_command):
                    # Check if project has relevant config files or file types
                    if self._has_config_or_files(linter_config):
                        available_linters.append(linter_config)
                        self.logger.info(f"Detected {linter_config.name} for {language}")

            if available_linters:
                detected[language] = available_linters

        self._detected_linters = detected
        return detected

    def _is_command_available(self, command: list[str] | str) -> bool:
        """Check if a command is available in PATH"""
        try:
            base_command = command[0] if isinstance(command, list) else command
            version_command = [base_command, "--version"]
            subprocess.run(version_command, capture_output=True, timeout=5, cwd=self.workspace_root)
            return True
        except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _resolve_linter_command(self, linter_config: LinterConfig) -> list[str] | None:
        """Resolve a linter command, including local Node.js tool installs."""
        tool_name = linter_config.command[0]

        if tool_name in self._NODE_TOOL_NAMES:
            resolved = resolve_node_command(tool_name, self.workspace_root)
            if not resolved:
                return None
            return resolved + linter_config.command[1:]

        return linter_config.command.copy()

    def _has_config_or_files(self, linter_config: LinterConfig) -> bool:
        """Check if project has config files or relevant file types"""
        tool_name = linter_config.command[0]
        if tool_name in self._NODE_TOOL_NAMES:
            config_keys = self._PACKAGE_JSON_TOOL_CONFIGS.get(tool_name)
            if package_json_uses_tool(self.workspace_root, tool_name, config_keys):
                return True

        # Check for config files
        for config_file in linter_config.config_files:
            if config_file == "package.json" and tool_name in self._NODE_TOOL_NAMES:
                continue
            if (self.workspace_root / config_file).exists():
                return True

        if linter_config.name == "hadolint":
            if self._list_dockerfiles():
                return True

        if linter_config.name in {"tflint", "terraform validate"}:
            if self._list_terraform_files():
                return True

        if linter_config.name in {"kubeval", "kube-linter"}:
            if self._list_kubernetes_manifests():
                return True

        if linter_config.name == "actionlint":
            if self._list_github_actions_workflows():
                return True

        # Check for relevant file extensions
        for ext in linter_config.extensions:
            if list(self.workspace_root.rglob(f"*{ext}")):
                return True

        return False

    def _list_dockerfiles(self) -> list[Path]:
        docker_files = []
        patterns = ["Dockerfile", "Dockerfile.*", "*.dockerfile", "dockerfile", "dockerfile.*"]
        for pattern in patterns:
            docker_files.extend(self.workspace_root.rglob(pattern))
        unique_files = []
        seen = set()
        for path in docker_files:
            if path not in seen:
                unique_files.append(path)
                seen.add(path)
        return unique_files

    def _is_dockerfile_path(self, path: str) -> bool:
        name = Path(path).name
        if name in {"Dockerfile", "dockerfile"}:
            return True
        if name.startswith("Dockerfile.") or name.startswith("dockerfile."):
            return True
        return name.lower().endswith(".dockerfile")

    def _list_terraform_files(self) -> list[Path]:
        terraform_files = []
        patterns = ["*.tf", "*.tfvars"]
        for pattern in patterns:
            for path in self.workspace_root.rglob(pattern):
                if ".terraform" in path.parts:
                    continue
                terraform_files.append(path)
        unique_files = []
        seen = set()
        for path in terraform_files:
            if path not in seen:
                unique_files.append(path)
                seen.add(path)
        return unique_files

    def _list_solidity_files(self) -> list[Path]:
        solidity_files = []
        skip_dirs = {"node_modules", "dist", "build", "__pycache__", ".git"}
        for path in self.workspace_root.rglob("*.sol"):
            if any(part in skip_dirs for part in path.parts):
                continue
            solidity_files.append(path)
        unique_files = []
        seen = set()
        for path in solidity_files:
            if path not in seen:
                unique_files.append(path)
                seen.add(path)
        return unique_files

    def _collect_terraform_directories(self, target_files: list[str] | None = None) -> list[Path]:
        if target_files:
            candidates = []
            for file_path in target_files:
                if not file_path.endswith((".tf", ".tfvars")):
                    continue
                path = Path(file_path)
                if not path.is_absolute():
                    path = self.workspace_root / path
                candidates.append(path)
        else:
            candidates = self._list_terraform_files()

        directories = []
        seen = set()
        for path in candidates:
            if ".terraform" in path.parts or not path.exists():
                continue
            directory = path.parent
            if directory not in seen:
                directories.append(directory)
                seen.add(directory)
        return directories

    def _list_github_actions_workflows(self) -> list[Path]:
        workflows_dir = self.workspace_root / ".github" / "workflows"
        if not workflows_dir.exists():
            return []
        workflow_files = []
        for ext in (".yml", ".yaml"):
            workflow_files.extend(workflows_dir.rglob(f"*{ext}"))
        unique_files = []
        seen = set()
        for path in workflow_files:
            if path not in seen:
                unique_files.append(path)
                seen.add(path)
        return unique_files

    def _is_github_actions_workflow_path(self, path: str) -> bool:
        path_obj = Path(path)
        if not path_obj.is_absolute():
            path_obj = self.workspace_root / path_obj
        try:
            relative = path_obj.relative_to(self.workspace_root)
        except ValueError:
            return False
        if len(relative.parts) < 3:
            return False
        if relative.parts[0] != ".github" or relative.parts[1] != "workflows":
            return False
        return relative.suffix in {".yml", ".yaml"}

    def _list_kubernetes_manifests(self, target_files: list[str] | None = None) -> list[Path]:
        max_size = 2 * 1024 * 1024
        if target_files:
            candidate_paths = []
            for file_path in target_files:
                if not file_path.endswith((".yml", ".yaml")):
                    continue
                path = Path(file_path)
                if not path.is_absolute():
                    path = self.workspace_root / path
                candidate_paths.append(path)
        else:
            candidate_paths = []
            for ext in (".yml", ".yaml"):
                candidate_paths.extend(self.workspace_root.rglob(f"*{ext}"))

        manifests = []
        seen = set()
        skip_dirs = {".git", "node_modules", "dist", "build", "__pycache__", ".terraform"}
        for path in candidate_paths:
            if any(part in skip_dirs for part in path.parts):
                continue
            try:
                if path.stat().st_size > max_size:
                    continue
            except OSError:
                continue
            if path in seen:
                continue
            if self._is_kubernetes_manifest_file(path):
                manifests.append(path)
                seen.add(path)
        return manifests

    def _is_kubernetes_manifest_file(self, path: Path) -> bool:
        if path.suffix not in {".yml", ".yaml"}:
            return False
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return False
        if not re.search(r"(?m)^\\s*apiVersion\\s*:", content):
            return False
        if not re.search(r"(?m)^\\s*kind\\s*:", content):
            return False
        return True

    def _normalize_issue_path(self, issue: dict[str, Any], cwd: Path) -> None:
        file_path = issue.get("file")
        if not file_path:
            return
        path = Path(file_path)
        if not path.is_absolute():
            path = cwd / path
        try:
            issue["file"] = str(path.relative_to(self.workspace_root))
        except ValueError:
            issue["file"] = str(path)

    def run_linters(
        self, target_files: list[str] | None = None, languages: list[str] | None = None
    ) -> dict[str, list[LintResult]]:
        """Run detected linters on specified files or entire project"""
        detected_linters = self.detect_linters()
        results = {}

        # Filter by requested languages
        if languages:
            detected_linters = {k: v for k, v in detected_linters.items() if k in languages}

        for language, linters in detected_linters.items():
            language_results = []

            for linter_config in linters:
                try:
                    result = self._run_single_linter(linter_config, target_files)
                    language_results.append(result)
                except Exception as e:
                    self.logger.error(f"Failed to run {linter_config.name}: {e}")
                    # Create error result
                    error_result = LintResult(
                        success=False,
                        linter=linter_config.name,
                        exit_code=-1,
                        stdout="",
                        stderr=str(e),
                        issues=[],
                        total_issues=0,
                        error_count=1,
                        warning_count=0,
                    )
                    language_results.append(error_result)

            if language_results:
                results[language] = language_results

        return results

    def _run_single_linter(self, linter_config: LinterConfig, target_files: list[str] | None = None) -> LintResult:
        """Run a single linter and parse its output"""
        command = self._resolve_linter_command(linter_config)
        if not command:
            return LintResult(
                success=False,
                linter=linter_config.name,
                exit_code=-1,
                stdout="",
                stderr=f"Unable to resolve command for {linter_config.name}",
                issues=[],
                total_issues=0,
                error_count=1,
                warning_count=0,
            )

        if linter_config.name == "jq":
            return self._run_jq_linter(linter_config, target_files)

        if linter_config.name == "sqlfluff":
            dialect = os.getenv("SQLFLUFF_DIALECT", "").strip()
            if dialect:
                command.extend(["--dialect", dialect])

        # Add target files or default to current directory
        if target_files and linter_config.name == "PSScriptAnalyzer":
            target_files = None
        if target_files and linter_config.name in {"clippy", "rustfmt"}:
            target_files = None
        if target_files and linter_config.name in {"tflint", "terraform validate"}:
            terraform_dirs = self._collect_terraform_directories(target_files)
            if terraform_dirs:
                return self._run_directory_linter(linter_config, command, terraform_dirs)
            return LintResult(
                success=True,
                linter=linter_config.name,
                exit_code=0,
                stdout="",
                stderr="",
                issues=[],
                total_issues=0,
                error_count=0,
                warning_count=0,
            )
        if target_files and linter_config.name == "slither":
            target_files = None

        if target_files:
            # Filter files by extension or name patterns
            if linter_config.name == "hadolint":
                relevant_files = [f for f in target_files if self._is_dockerfile_path(f)]
            elif linter_config.name in {"kubeval", "kube-linter"}:
                relevant_paths = self._list_kubernetes_manifests(target_files)
                relevant_files = []
                for path in relevant_paths:
                    try:
                        relevant_files.append(str(path.relative_to(self.workspace_root)))
                    except ValueError:
                        relevant_files.append(str(path))
            elif linter_config.name == "actionlint":
                relevant_files = []
                for file_path in target_files:
                    if self._is_github_actions_workflow_path(file_path):
                        path = Path(file_path)
                        if path.is_absolute():
                            try:
                                path = path.relative_to(self.workspace_root)
                            except ValueError:
                                path = Path(file_path)
                        relevant_files.append(str(path))
            else:
                relevant_files = [f for f in target_files if any(f.endswith(ext) for ext in linter_config.extensions)]
                if linter_config.name == "checkmake":
                    relevant_files.extend(
                        [f for f in target_files if Path(f).name in self._MAKEFILE_NAMES and f not in relevant_files]
                    )
            if relevant_files:
                command.extend(relevant_files)
            else:
                # No relevant files, skip this linter
                return LintResult(
                    success=True,
                    linter=linter_config.name,
                    exit_code=0,
                    stdout="",
                    stderr="",
                    issues=[],
                    total_issues=0,
                    error_count=0,
                    warning_count=0,
                )
        else:
            # Add default target (usually current directory or specific patterns)
            if linter_config.name in {"clippy", "rustfmt"}:
                if (self.workspace_root / "Cargo.toml").exists() or list(self.workspace_root.rglob("*.rs")):
                    pass
                else:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name in {"tflint", "terraform validate"}:
                terraform_dirs = self._collect_terraform_directories()
                if terraform_dirs:
                    return self._run_directory_linter(linter_config, command, terraform_dirs)
                return LintResult(
                    success=True,
                    linter=linter_config.name,
                    exit_code=0,
                    stdout="",
                    stderr="",
                    issues=[],
                    total_issues=0,
                    error_count=0,
                    warning_count=0,
                )
            elif linter_config.name == "hadolint":
                docker_files = self._list_dockerfiles()
                if docker_files:
                    command.extend([str(f.relative_to(self.workspace_root)) for f in docker_files[:50]])
                else:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name in {"kubeval", "kube-linter"}:
                manifest_files = self._list_kubernetes_manifests()
                if manifest_files:
                    command.extend([str(f.relative_to(self.workspace_root)) for f in manifest_files[:50]])
                else:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name == "actionlint":
                workflow_files = self._list_github_actions_workflows()
                if workflow_files:
                    command.extend([str(f.relative_to(self.workspace_root)) for f in workflow_files[:50]])
                else:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name == "solhint":
                solidity_files = self._list_solidity_files()
                if solidity_files:
                    command.extend([str(f.relative_to(self.workspace_root)) for f in solidity_files[:50]])
                else:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name == "slither":
                solidity_files = self._list_solidity_files()
                if not solidity_files:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name in {"golangci-lint", "go vet"}:
                go_files = list(self.workspace_root.rglob("*.go"))
                if go_files:
                    command.append("./...")
                else:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name == "shellcheck":
                shell_files = []
                for ext in linter_config.extensions:
                    shell_files.extend(self.workspace_root.rglob(f"*{ext}"))
                if shell_files:
                    command.extend([str(f.relative_to(self.workspace_root)) for f in shell_files[:50]])
                else:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name == "checkmake":
                makefiles = [path for path in self.workspace_root.rglob("*") if path.name in self._MAKEFILE_NAMES]
                if makefiles:
                    command.extend([str(f.relative_to(self.workspace_root)) for f in makefiles[:10]])
                else:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name == "PSScriptAnalyzer":
                pass
            elif linter_config.name in {"yamllint", "taplo", "xmllint", "htmlhint", "stylelint", "sqlfluff", "sqlfmt"}:
                config_files = []
                for ext in linter_config.extensions:
                    config_files.extend(self.workspace_root.rglob(f"*{ext}"))
                if config_files:
                    command.extend([str(f.relative_to(self.workspace_root)) for f in config_files[:50]])
                else:
                    return LintResult(
                        success=True,
                        linter=linter_config.name,
                        exit_code=0,
                        stdout="",
                        stderr="",
                        issues=[],
                        total_issues=0,
                        error_count=0,
                        warning_count=0,
                    )
            elif linter_config.name == "mypy" or linter_config.name == "flake8":
                command.append(".")
            elif linter_config.name == "pylint":
                # Find Python files
                py_files = list(self.workspace_root.rglob("*.py"))
                if py_files:
                    command.extend([str(f.relative_to(self.workspace_root)) for f in py_files[:50]])  # Limit files
                else:
                    command.append(".")
            else:
                command.append(".")

        # Run the linter
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=self.workspace_root,
            )

            # Parse output using the appropriate parser
            parse_func = getattr(self, linter_config.parse_function)
            issues = parse_func(result.stdout, result.stderr)

            # Count issues by severity
            error_count = sum(1 for issue in issues if issue.get("severity") == "error")
            warning_count = sum(1 for issue in issues if issue.get("severity") == "warning")

            return LintResult(
                success=error_count == 0,  # Success based on actual errors, not exit code
                linter=linter_config.name,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                issues=issues,
                total_issues=len(issues),
                error_count=error_count,
                warning_count=warning_count,
            )

        except subprocess.TimeoutExpired:
            return LintResult(
                success=False,
                linter=linter_config.name,
                exit_code=-1,
                stdout="",
                stderr="Linter timed out after 5 minutes",
                issues=[],
                total_issues=0,
                error_count=1,
                warning_count=0,
            )

    def _run_jq_linter(self, linter_config: LinterConfig, target_files: list[str] | None = None) -> LintResult:
        """Run jq against JSON files and aggregate errors with file attribution."""
        command = self._resolve_linter_command(linter_config)
        if not command:
            return LintResult(
                success=False,
                linter=linter_config.name,
                exit_code=-1,
                stdout="",
                stderr=f"Unable to resolve command for {linter_config.name}",
                issues=[],
                total_issues=0,
                error_count=1,
                warning_count=0,
            )

        if target_files:
            json_files = [f for f in target_files if f.endswith(".json")]
        else:
            json_files = [str(f.relative_to(self.workspace_root)) for f in self.workspace_root.rglob("*.json")]

        if not json_files:
            return LintResult(
                success=True,
                linter=linter_config.name,
                exit_code=0,
                stdout="",
                stderr="",
                issues=[],
                total_issues=0,
                error_count=0,
                warning_count=0,
            )

        issues = []
        stdout_parts = []
        stderr_parts = []
        exit_code = 0

        for file_path in json_files[:50]:
            try:
                result = subprocess.run(
                    command + [file_path],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=self.workspace_root,
                )
            except subprocess.TimeoutExpired:
                issues.append(
                    {
                        "file": file_path,
                        "line": 0,
                        "column": 0,
                        "code": "",
                        "message": "jq timed out after 60 seconds",
                        "severity": "error",
                    }
                )
                exit_code = max(exit_code, 1)
                continue

            stdout_parts.append(result.stdout)
            stderr_parts.append(result.stderr)

            if result.returncode != 0:
                exit_code = max(exit_code, result.returncode)
                issues.extend(self._parse_jq_output(result.stdout, result.stderr, file_path))

        error_count = sum(1 for issue in issues if issue.get("severity") == "error")
        warning_count = sum(1 for issue in issues if issue.get("severity") == "warning")

        return LintResult(
            success=error_count == 0,
            linter=linter_config.name,
            exit_code=exit_code,
            stdout="".join(stdout_parts),
            stderr="".join(stderr_parts),
            issues=issues,
            total_issues=len(issues),
            error_count=error_count,
            warning_count=warning_count,
        )

    def _run_directory_linter(
        self, linter_config: LinterConfig, command: list[str], directories: list[Path]
    ) -> LintResult:
        issues = []
        stdout_parts = []
        stderr_parts = []
        exit_code = 0
        parse_func = getattr(self, linter_config.parse_function)

        for directory in directories[:20]:
            try:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd=directory,
                )
            except subprocess.TimeoutExpired:
                try:
                    directory_label = str(directory.relative_to(self.workspace_root))
                except ValueError:
                    directory_label = str(directory)
                issues.append(
                    {
                        "file": directory_label,
                        "line": 0,
                        "column": 0,
                        "code": "",
                        "message": f"{linter_config.name} timed out after 5 minutes",
                        "severity": "error",
                    }
                )
                exit_code = max(exit_code, 1)
                continue

            stdout_parts.append(result.stdout)
            stderr_parts.append(result.stderr)

            parsed = parse_func(result.stdout, result.stderr)
            for issue in parsed:
                self._normalize_issue_path(issue, directory)
            issues.extend(parsed)
            exit_code = max(exit_code, result.returncode)

        error_count = sum(1 for issue in issues if issue.get("severity") == "error")
        warning_count = sum(1 for issue in issues if issue.get("severity") == "warning")

        return LintResult(
            success=error_count == 0,
            linter=linter_config.name,
            exit_code=exit_code,
            stdout="".join(stdout_parts),
            stderr="".join(stderr_parts),
            issues=issues,
            total_issues=len(issues),
            error_count=error_count,
            warning_count=warning_count,
        )

    def _parse_flake8_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse flake8 JSON output"""
        issues = []

        # Try JSON format first
        try:
            if stdout.strip():
                data = json.loads(stdout)
                for item in data:
                    issues.append(
                        {
                            "file": item.get("filename", ""),
                            "line": item.get("line_number", 0),
                            "column": item.get("column_number", 0),
                            "code": item.get("code", ""),
                            "message": item.get("text", ""),
                            "severity": "error" if item.get("code", "").startswith("E") else "warning",
                        }
                    )
        except json.JSONDecodeError:
            # Fallback to text parsing
            issues = self._parse_flake8_text(stdout, stderr)

        return issues

    def _parse_flake8_text(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse flake8 text output as fallback"""
        issues = []
        pattern = r"^(.+?):(\d+):(\d+):\s*([EW]\d+)\s*(.+)$"

        for line in stdout.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                file_path, line_num, col_num, code, message = match.groups()
                issues.append(
                    {
                        "file": file_path,
                        "line": int(line_num),
                        "column": int(col_num),
                        "code": code,
                        "message": message.strip(),
                        "severity": "error" if code.startswith("E") else "warning",
                    }
                )

        return issues

    def _parse_pylint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse pylint JSON output"""
        issues = []

        try:
            if stdout.strip():
                data = json.loads(stdout)
                for item in data:
                    issues.append(
                        {
                            "file": item.get("path", ""),
                            "line": item.get("line", 0),
                            "column": item.get("column", 0),
                            "code": item.get("message-id", ""),
                            "message": item.get("message", ""),
                            "severity": item.get("type", "warning"),
                        }
                    )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse pylint JSON output")

        return issues

    def _parse_mypy_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse mypy text output"""
        issues = []
        pattern = r"^(.+?):(\d+):(?:(\d+):)?\s*(error|warning|note):\s*(.+)$"

        for line in stdout.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                file_path, line_num, col_num, severity, message = match.groups()
                issues.append(
                    {
                        "file": file_path,
                        "line": int(line_num),
                        "column": int(col_num) if col_num else 0,
                        "code": "",
                        "message": message.strip(),
                        "severity": severity,
                    }
                )

        return issues

    def _parse_eslint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse ESLint JSON output"""
        issues = []

        try:
            if stdout.strip():
                data = json.loads(stdout)
                for file_result in data:
                    file_path = file_result.get("filePath", "")
                    for message in file_result.get("messages", []):
                        issues.append(
                            {
                                "file": file_path,
                                "line": message.get("line", 0),
                                "column": message.get("column", 0),
                                "code": message.get("ruleId", ""),
                                "message": message.get("message", ""),
                                "severity": "error" if message.get("severity") == 2 else "warning",
                            }
                        )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse ESLint JSON output")

        return issues

    def _parse_tsc_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse TypeScript compiler output"""
        issues = []
        pattern = r"^(.+?)\((\d+),(\d+)\):\s*(error|warning)\s*TS(\d+):\s*(.+)$"

        for line in stdout.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                file_path, line_num, col_num, severity, code, message = match.groups()
                issues.append(
                    {
                        "file": file_path,
                        "line": int(line_num),
                        "column": int(col_num),
                        "code": f"TS{code}",
                        "message": message.strip(),
                        "severity": severity,
                    }
                )

        return issues

    def _parse_shellcheck_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse shellcheck JSON output"""
        issues = []

        try:
            if stdout.strip():
                data = json.loads(stdout)
                for item in data.get("comments", []):
                    level = str(item.get("level", "")).lower()
                    issues.append(
                        {
                            "file": item.get("file", ""),
                            "line": item.get("line", 0),
                            "column": item.get("column", 0),
                            "code": f"SC{item.get('code')}" if item.get("code") is not None else "",
                            "message": item.get("message", ""),
                            "severity": "error" if level == "error" else "warning",
                        }
                    )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse shellcheck JSON output")

        return issues

    def _parse_psscriptanalyzer_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse PSScriptAnalyzer JSON output"""
        issues = []

        try:
            if stdout.strip():
                data = json.loads(stdout)
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    severity = str(item.get("Severity", "warning")).lower()
                    issues.append(
                        {
                            "file": item.get("ScriptName", ""),
                            "line": item.get("Line", 0),
                            "column": item.get("Column", 0),
                            "code": item.get("RuleName", ""),
                            "message": item.get("Message", ""),
                            "severity": "error" if severity == "error" else "warning",
                        }
                    )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse PSScriptAnalyzer JSON output")

        return issues

    def _parse_checkmake_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse checkmake text output"""
        issues = []
        pattern = r"^(.+?):(\d+)(?::(\d+))?:\s*(.+)$"

        for line in stdout.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                file_path, line_num, col_num, message = match.groups()
                normalized_message = message.strip()
                severity = "error" if "error" in normalized_message.lower() else "warning"
                issues.append(
                    {
                        "file": file_path,
                        "line": int(line_num),
                        "column": int(col_num) if col_num else 0,
                        "code": "",
                        "message": normalized_message,
                        "severity": severity,
                    }
                )

        return issues

    def _parse_yamllint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse yamllint parsable output"""
        issues = []
        pattern = r"^(.+?):(\d+):(\d+): \[(\w+)\] (.+)$"

        for line in stdout.split("\n"):
            match = re.match(pattern, line.strip())
            if not match:
                continue
            file_path, line_num, col_num, level, message = match.groups()
            code = ""
            rule_match = re.search(r"\(([^)]+)\)\s*$", message)
            if rule_match:
                code = rule_match.group(1)
                message = message[: rule_match.start()].strip()
            severity = "error" if level.lower() == "error" else "warning"
            issues.append(
                {
                    "file": file_path,
                    "line": int(line_num),
                    "column": int(col_num),
                    "code": code,
                    "message": message,
                    "severity": severity,
                }
            )

        return issues

    def _parse_jq_output(self, stdout: str, stderr: str, file_path: str | None = None) -> list[dict[str, Any]]:
        """Parse jq stderr output for JSON validation errors."""
        issues = []
        pattern = r"^parse error: (.+) at line (\d+), column (\d+)$"

        for line in stderr.split("\n"):
            line = line.strip()
            if not line:
                continue
            match = re.match(pattern, line)
            if match:
                message, line_num, col_num = match.groups()
                issues.append(
                    {
                        "file": file_path or "",
                        "line": int(line_num),
                        "column": int(col_num),
                        "code": "",
                        "message": message,
                        "severity": "error",
                    }
                )
            else:
                issues.append(
                    {
                        "file": file_path or "",
                        "line": 0,
                        "column": 0,
                        "code": "",
                        "message": line,
                        "severity": "error",
                    }
                )

        return issues

    def _parse_taplo_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse taplo check output"""
        issues = []
        combined = "\n".join([stdout, stderr])
        current_message = None

        for line in combined.split("\n"):
            line = line.rstrip()
            if line.startswith("error:"):
                current_message = line.split("error:", 1)[1].strip()
                continue
            match = re.match(r"^ --> (.+?):(\d+):(\d+)$", line)
            if match:
                file_path, line_num, col_num = match.groups()
                issues.append(
                    {
                        "file": file_path,
                        "line": int(line_num),
                        "column": int(col_num),
                        "code": "",
                        "message": current_message or "TOML validation error",
                        "severity": "error",
                    }
                )

        return issues

    def _parse_sqlfluff_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse sqlfluff JSON output"""
        issues = []

        def _safe_int(value: Any) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        try:
            if stdout.strip():
                data = json.loads(stdout)
                if isinstance(data, dict):
                    file_entries = data.get("files") or data.get("results") or data.get("data") or []
                else:
                    file_entries = data
                if not isinstance(file_entries, list):
                    file_entries = []
                for entry in file_entries:
                    if not isinstance(entry, dict):
                        continue
                    file_path = entry.get("filepath") or entry.get("path") or entry.get("file", "")
                    violations = entry.get("violations") or entry.get("linting_violations") or entry.get("errors") or []
                    for violation in violations:
                        if not isinstance(violation, dict):
                            continue
                        severity_value = violation.get("severity") or violation.get("type") or violation.get("level")
                        severity = "warning"
                        if severity_value is not None:
                            if isinstance(severity_value, (int, float)):
                                severity = "error" if severity_value >= 1 else "warning"
                            else:
                                severity_text = str(severity_value).lower()
                                if "error" in severity_text or "fatal" in severity_text:
                                    severity = "error"
                                elif "warn" in severity_text:
                                    severity = "warning"
                                elif severity_text.isdigit():
                                    severity = "error" if int(severity_text) >= 1 else "warning"
                        issues.append(
                            {
                                "file": file_path,
                                "line": _safe_int(violation.get("line_no") or violation.get("line")),
                                "column": _safe_int(violation.get("line_pos") or violation.get("column")),
                                "code": violation.get("code") or violation.get("rule", ""),
                                "message": violation.get("description")
                                or violation.get("message")
                                or violation.get("text", ""),
                                "severity": severity,
                            }
                        )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse sqlfluff JSON output")

        return issues

    def _parse_sqlfmt_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse sqlfmt check output"""
        issues = []
        combined = "\n".join([stdout, stderr]).strip()
        if not combined:
            return issues

        reformatting_detected = False
        reformat_tokens = (
            "would reformat",
            "would be reformatted",
            "needs formatting",
            "not formatted",
            "needs reformat",
            "reformat required",
            "unformatted",
            "would format",
        )

        for line in combined.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            lower = stripped.lower()
            if any(token in lower for token in reformat_tokens):
                reformatting_detected = True
                file_match = re.search(
                    r"(?:would reformat|would be reformatted|needs formatting|not formatted|needs reformat|reformat required|unformatted|would format)[:\\s]+(.+)$",
                    stripped,
                    re.IGNORECASE,
                )
                file_path = file_match.group(1).strip() if file_match else ""
                issues.append(
                    {
                        "file": file_path,
                        "line": 0,
                        "column": 0,
                        "code": "sqlfmt",
                        "message": stripped,
                        "severity": "error",
                    }
                )
                continue

            file_match = re.search(r"([A-Za-z0-9_./\\-]+\\.sql)$", stripped)
            if reformatting_detected and file_match:
                issues.append(
                    {
                        "file": file_match.group(1),
                        "line": 0,
                        "column": 0,
                        "code": "sqlfmt",
                        "message": "SQL file requires formatting",
                        "severity": "error",
                    }
                )
                continue

            if "error" in lower or "failed" in lower:
                issues.append(
                    {
                        "file": "",
                        "line": 0,
                        "column": 0,
                        "code": "sqlfmt",
                        "message": stripped,
                        "severity": "error",
                    }
                )

        return issues

    def _parse_tflint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse tflint JSON output"""
        issues = []

        def _safe_int(value: Any) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        try:
            if stdout.strip():
                data = json.loads(stdout)
                entries = []
                if isinstance(data, dict):
                    entries = data.get("issues") or data.get("Issues") or data.get("errors") or []
                elif isinstance(data, list):
                    entries = data

                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    rule = entry.get("rule") or {}
                    if isinstance(rule, dict):
                        code = rule.get("name") or rule.get("id") or ""
                        severity_value = rule.get("severity") or ""
                    else:
                        code = str(rule) if rule else ""
                        severity_value = ""
                    range_info = entry.get("range") or entry.get("location") or {}
                    filename = ""
                    line = 0
                    column = 0
                    if isinstance(range_info, dict):
                        filename = (
                            range_info.get("filename")
                            or range_info.get("file")
                            or range_info.get("path")
                            or range_info.get("name")
                            or ""
                        )
                        start = range_info.get("start") or {}
                        line = _safe_int(start.get("line") or range_info.get("line"))
                        column = _safe_int(start.get("column") or range_info.get("column"))
                    severity_text = str(severity_value).lower()
                    severity = "error" if "error" in severity_text or "fatal" in severity_text else "warning"
                    issues.append(
                        {
                            "file": filename,
                            "line": line,
                            "column": column,
                            "code": code,
                            "message": entry.get("message") or entry.get("detail") or "",
                            "severity": severity,
                        }
                    )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse tflint JSON output")

        return issues

    def _parse_terraform_validate_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse terraform validate JSON output"""
        issues = []

        def _safe_int(value: Any) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        try:
            if stdout.strip():
                data = json.loads(stdout)
                diagnostics = []
                if isinstance(data, dict):
                    diagnostics = data.get("diagnostics") or []
                elif isinstance(data, list):
                    diagnostics = data

                for diag in diagnostics:
                    if not isinstance(diag, dict):
                        continue
                    summary = diag.get("summary") or ""
                    detail = diag.get("detail") or ""
                    message = f"{summary}: {detail}".strip(": ") if detail else summary
                    range_info = diag.get("range") or {}
                    filename = range_info.get("filename") or range_info.get("file") or ""
                    start = range_info.get("start") or {}
                    severity_text = str(diag.get("severity") or "error").lower()
                    severity = "warning" if "warning" in severity_text else "error"
                    issues.append(
                        {
                            "file": filename,
                            "line": _safe_int(start.get("line")),
                            "column": _safe_int(start.get("column")),
                            "code": diag.get("detail") or diag.get("summary") or "",
                            "message": message,
                            "severity": severity,
                        }
                    )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse terraform validate JSON output")

        return issues

    def _parse_kubeval_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse kubeval JSON output"""
        issues = []

        try:
            if stdout.strip():
                data = json.loads(stdout)
                items = []
                if isinstance(data, dict):
                    items = data.get("items") or data.get("results") or data.get("reports") or []
                elif isinstance(data, list):
                    items = data

                for item in items:
                    if not isinstance(item, dict):
                        continue
                    filename = item.get("filename") or item.get("file") or item.get("path") or ""
                    errors = item.get("errors") or item.get("warnings") or []
                    if not errors and item.get("valid") is False:
                        issues.append(
                            {
                                "file": filename,
                                "line": 0,
                                "column": 0,
                                "code": "kubeval",
                                "message": item.get("error") or "Kubernetes manifest failed validation",
                                "severity": "error",
                            }
                        )
                    for error in errors:
                        if not isinstance(error, dict):
                            continue
                        message = error.get("message") or error.get("detail") or error.get("reason") or ""
                        field = error.get("field")
                        if field:
                            message = f"{message} (field: {field})"
                        severity_text = str(error.get("severity") or "error").lower()
                        severity = "warning" if "warning" in severity_text else "error"
                        issues.append(
                            {
                                "file": filename,
                                "line": 0,
                                "column": 0,
                                "code": error.get("code") or error.get("type") or "kubeval",
                                "message": message or "Kubernetes manifest failed validation",
                                "severity": severity,
                            }
                        )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse kubeval JSON output")

        return issues

    def _parse_kube_linter_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse kube-linter JSON output"""
        issues = []

        def _safe_int(value: Any) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        try:
            if stdout.strip():
                data = json.loads(stdout)
                reports = []
                if isinstance(data, dict):
                    reports = (
                        data.get("reports") or data.get("Reports") or data.get("diagnostics") or data.get("items") or []
                    )
                elif isinstance(data, list):
                    reports = data

                for report in reports:
                    if not isinstance(report, dict):
                        continue
                    diagnostic = report.get("diagnostic") or report.get("Diagnostic") or {}
                    location = report.get("location") or diagnostic.get("location") or {}
                    filename = (
                        location.get("path")
                        or location.get("file")
                        or location.get("filename")
                        or report.get("file")
                        or ""
                    )
                    line = _safe_int(location.get("line") or report.get("line"))
                    column = _safe_int(location.get("column") or report.get("column"))
                    message = (
                        diagnostic.get("message")
                        or report.get("message")
                        or report.get("description")
                        or "Kubernetes manifest failed linting"
                    )
                    severity_text = str(diagnostic.get("severity") or report.get("severity") or "warning").lower()
                    severity = "error" if "error" in severity_text or "fatal" in severity_text else "warning"
                    issues.append(
                        {
                            "file": filename,
                            "line": line,
                            "column": column,
                            "code": report.get("check")
                            or diagnostic.get("check")
                            or report.get("code")
                            or "kube-linter",
                            "message": message,
                            "severity": severity,
                        }
                    )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse kube-linter JSON output")

        return issues

    def _parse_actionlint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse actionlint JSON output"""
        issues = []

        def _safe_int(value: Any) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        try:
            if stdout.strip():
                data = json.loads(stdout)
                entries = []
                if isinstance(data, dict):
                    entries = data.get("errors") or data.get("issues") or data.get("reports") or []
                elif isinstance(data, list):
                    entries = data

                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    position = entry.get("pos") or entry.get("position") or {}
                    filename = entry.get("file") or entry.get("path") or entry.get("filename") or ""
                    line = _safe_int(entry.get("line") or position.get("line"))
                    column = _safe_int(entry.get("column") or position.get("column") or entry.get("col"))
                    message = entry.get("message") or entry.get("detail") or ""
                    severity_text = str(entry.get("severity") or entry.get("kind") or "error").lower()
                    severity = "warning" if "warning" in severity_text else "error"
                    issues.append(
                        {
                            "file": filename,
                            "line": line,
                            "column": column,
                            "code": entry.get("code") or entry.get("rule") or "actionlint",
                            "message": message,
                            "severity": severity,
                        }
                    )
        except json.JSONDecodeError:
            pattern_with_column = r"^(.+?):(\d+):(\d+):\s*(.+)$"
            pattern_no_column = r"^(.+?):(\d+):\s*(.+)$"
            for line in stdout.split("\n"):
                match = re.match(pattern_with_column, line.strip())
                if match:
                    file_path, line_num, col_num, message = match.groups()
                    issues.append(
                        {
                            "file": file_path,
                            "line": int(line_num),
                            "column": int(col_num),
                            "code": "actionlint",
                            "message": message.strip(),
                            "severity": "error",
                        }
                    )
                    continue
                match = re.match(pattern_no_column, line.strip())
                if match:
                    file_path, line_num, message = match.groups()
                    issues.append(
                        {
                            "file": file_path,
                            "line": int(line_num),
                            "column": 0,
                            "code": "actionlint",
                            "message": message.strip(),
                            "severity": "error",
                        }
                    )

        return issues

    def _parse_solhint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse solhint JSON output"""
        issues = []

        def _safe_int(value: Any) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        try:
            if stdout.strip():
                data = json.loads(stdout)
                file_results = data if isinstance(data, list) else [data]
                for file_result in file_results:
                    if not isinstance(file_result, dict):
                        continue
                    file_path = file_result.get("filePath") or file_result.get("file") or ""
                    messages = file_result.get("messages") or file_result.get("errors") or []
                    for message in messages:
                        if not isinstance(message, dict):
                            continue
                        severity_value = message.get("severity")
                        severity = "warning"
                        if isinstance(severity_value, (int, float)):
                            severity = "error" if int(severity_value) >= 2 else "warning"
                        elif isinstance(severity_value, str) and severity_value.lower() == "error":
                            severity = "error"
                        issues.append(
                            {
                                "file": file_path,
                                "line": _safe_int(message.get("line")),
                                "column": _safe_int(message.get("column")),
                                "code": message.get("ruleId") or message.get("rule") or "",
                                "message": message.get("message") or "",
                                "severity": severity,
                            }
                        )
        except json.JSONDecodeError:
            pattern = r"^(.+?):(\d+):(\d+):\s*(.+)$"
            for line in stdout.split("\n"):
                match = re.match(pattern, line.strip())
                if match:
                    file_path, line_num, col_num, message = match.groups()
                    issues.append(
                        {
                            "file": file_path,
                            "line": int(line_num),
                            "column": int(col_num),
                            "code": "solhint",
                            "message": message.strip(),
                            "severity": "error",
                        }
                    )

        return issues

    def _parse_slither_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse slither JSON output"""
        issues = []

        def _safe_int(value: Any) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        def _impact_to_severity(impact: str | None) -> str:
            impact_text = str(impact or "").lower()
            if "high" in impact_text or "critical" in impact_text:
                return "error"
            if "medium" in impact_text:
                return "warning"
            if "low" in impact_text or "informational" in impact_text:
                return "warning"
            return "warning"

        try:
            if stdout.strip():
                data = json.loads(stdout)
                results = data.get("results") if isinstance(data, dict) else {}
                detectors = []
                if isinstance(results, dict):
                    detectors = results.get("detectors") or []
                elif isinstance(results, list):
                    detectors = results

                for detector in detectors:
                    if not isinstance(detector, dict):
                        continue
                    description = detector.get("description") or detector.get("message") or ""
                    check = detector.get("check") or detector.get("id") or "slither"
                    severity = _impact_to_severity(detector.get("impact"))
                    elements = detector.get("elements") or []
                    if not elements:
                        issues.append(
                            {
                                "file": "",
                                "line": 0,
                                "column": 0,
                                "code": check,
                                "message": description,
                                "severity": severity,
                            }
                        )
                    for element in elements:
                        if not isinstance(element, dict):
                            continue
                        mapping = element.get("source_mapping") or element.get("sourceMapping") or {}
                        filename = (
                            mapping.get("filename_short") or mapping.get("filename") or element.get("source") or ""
                        )
                        lines = mapping.get("lines") or []
                        line = _safe_int(lines[0]) if lines else 0
                        column = _safe_int(mapping.get("starting_column") or mapping.get("column"))
                        issues.append(
                            {
                                "file": filename,
                                "line": line,
                                "column": column,
                                "code": check,
                                "message": description,
                                "severity": severity,
                            }
                        )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse slither JSON output")

        return issues

    def _parse_golangci_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse golangci-lint JSON output"""
        issues = []

        def _safe_int(value: Any) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        try:
            if stdout.strip():
                data = json.loads(stdout)
                items = []
                if isinstance(data, dict):
                    items = data.get("Issues") or data.get("issues") or []
                elif isinstance(data, list):
                    items = data
                if not isinstance(items, list):
                    items = []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    pos = item.get("Pos") or item.get("pos") or {}
                    if not isinstance(pos, dict):
                        pos = {}
                    file_path = pos.get("Filename") or pos.get("filename") or item.get("Path") or item.get("path") or ""
                    line_num = _safe_int(pos.get("Line") or pos.get("line"))
                    col_num = _safe_int(pos.get("Column") or pos.get("column"))
                    severity = "error"
                    severity_value = item.get("Severity") or item.get("severity")
                    if severity_value is not None:
                        if isinstance(severity_value, (int, float)):
                            severity = "error" if severity_value >= 1 else "warning"
                        else:
                            severity_text = str(severity_value).lower()
                            if "warn" in severity_text or "info" in severity_text:
                                severity = "warning"
                            elif severity_text.isdigit():
                                severity = "error" if int(severity_text) >= 1 else "warning"
                    issues.append(
                        {
                            "file": file_path,
                            "line": line_num,
                            "column": col_num,
                            "code": item.get("FromLinter") or item.get("fromLinter") or item.get("RuleID") or "",
                            "message": item.get("Text") or item.get("text") or item.get("Message") or "",
                            "severity": severity,
                        }
                    )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse golangci-lint JSON output")

        return issues

    def _parse_go_vet_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse go vet text output"""
        issues = []
        combined = "\n".join([stdout, stderr])
        pattern = r"^(.+?):(\d+):(?:(\d+):)?\s*(.+)$"

        for line in combined.split("\n"):
            line = line.strip()
            if not line:
                continue
            match = re.match(pattern, line)
            if match:
                file_path, line_num, col_num, message = match.groups()
                issues.append(
                    {
                        "file": file_path,
                        "line": int(line_num),
                        "column": int(col_num) if col_num else 0,
                        "code": "govet",
                        "message": message.strip(),
                        "severity": "error",
                    }
                )
            else:
                issues.append(
                    {
                        "file": "",
                        "line": 0,
                        "column": 0,
                        "code": "govet",
                        "message": line,
                        "severity": "error",
                    }
                )

        return issues

    def _parse_clippy_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse cargo clippy JSON output"""
        issues = []

        def _safe_int(value: Any) -> int:
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0

        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(payload, dict):
                continue
            if payload.get("reason") != "compiler-message":
                continue
            message = payload.get("message", {})
            if not isinstance(message, dict):
                continue
            spans = message.get("spans", [])
            if not spans:
                continue
            primary_span = spans[0]
            file_path = primary_span.get("file_name", "")
            line_num = _safe_int(primary_span.get("line_start"))
            col_num = _safe_int(primary_span.get("column_start"))
            level = str(message.get("level", "warning")).lower()
            code = ""
            code_obj = message.get("code")
            if isinstance(code_obj, dict):
                code = code_obj.get("code", "")
            issues.append(
                {
                    "file": file_path,
                    "line": line_num,
                    "column": col_num,
                    "code": code,
                    "message": message.get("message", ""),
                    "severity": "error" if level == "error" else "warning",
                }
            )

        return issues

    def _parse_rustfmt_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse cargo fmt --check output"""
        issues = []
        combined = "\n".join([stdout, stderr]).strip()
        if not combined:
            return issues

        for line in combined.split("\n"):
            line = line.strip()
            if not line:
                continue
            file_match = re.search(r"([A-Za-z0-9_./\\-]+\\.rs)", line)
            issues.append(
                {
                    "file": file_match.group(1) if file_match else "",
                    "line": 0,
                    "column": 0,
                    "code": "rustfmt",
                    "message": line,
                    "severity": "error",
                }
            )

        return issues

    def _parse_hadolint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse hadolint JSON output"""
        issues = []

        try:
            if stdout.strip():
                data = json.loads(stdout)
                items = data
                if isinstance(data, dict):
                    items = data.get("issues") or data.get("Issues") or []
                if not isinstance(items, list):
                    items = []
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    level = str(item.get("level", "")).lower()
                    issues.append(
                        {
                            "file": item.get("file", ""),
                            "line": item.get("line", 0),
                            "column": item.get("column", 0),
                            "code": item.get("code", ""),
                            "message": item.get("message", ""),
                            "severity": "error" if level == "error" else "warning",
                        }
                    )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse hadolint JSON output")

        return issues

    def _parse_xmllint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse xmllint stderr output"""
        issues = []
        pattern = r"^(.+?):(\d+):\s*(.+)$"

        for line in stderr.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                file_path, line_num, message = match.groups()
                issues.append(
                    {
                        "file": file_path,
                        "line": int(line_num),
                        "column": 0,
                        "code": "",
                        "message": message.strip(),
                        "severity": "error",
                    }
                )

        return issues

    def _parse_htmlhint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse htmlhint JSON output"""
        issues = []

        try:
            if stdout.strip():
                data = json.loads(stdout)
                for file_result in data:
                    file_path = file_result.get("file", "")
                    for message in file_result.get("messages", []):
                        level = str(message.get("type", "")).lower()
                        issues.append(
                            {
                                "file": file_path,
                                "line": message.get("line", 0),
                                "column": message.get("col", 0),
                                "code": message.get("rule", ""),
                                "message": message.get("message", ""),
                                "severity": "error" if level == "error" else "warning",
                            }
                        )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse htmlhint JSON output")

        return issues

    def _parse_stylelint_output(self, stdout: str, stderr: str) -> list[dict[str, Any]]:
        """Parse stylelint JSON output"""
        issues = []

        try:
            if stdout.strip():
                data = json.loads(stdout)
                for file_result in data:
                    file_path = file_result.get("source", "")
                    for warning in file_result.get("warnings", []):
                        severity = str(warning.get("severity", "warning")).lower()
                        issues.append(
                            {
                                "file": file_path,
                                "line": warning.get("line", 0),
                                "column": warning.get("column", 0),
                                "code": warning.get("rule", ""),
                                "message": warning.get("text", ""),
                                "severity": "error" if severity == "error" else "warning",
                            }
                        )
        except json.JSONDecodeError:
            self.logger.warning("Failed to parse stylelint JSON output")

        return issues

    def get_summary(self, results: dict[str, list[LintResult]]) -> dict[str, Any]:
        """Generate a summary of linting results"""
        total_issues = 0
        total_errors = 0
        total_warnings = 0
        failed_linters = []
        successful_linters = []

        for language, linter_results in results.items():
            for result in linter_results:
                total_issues += result.total_issues
                total_errors += result.error_count
                total_warnings += result.warning_count

                if result.success:
                    successful_linters.append(f"{language}:{result.linter}")
                else:
                    failed_linters.append(f"{language}:{result.linter}")

        return {
            "total_issues": total_issues,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "failed_linters": failed_linters,
            "successful_linters": successful_linters,
            "overall_success": len(failed_linters) == 0 and total_errors == 0,
        }

    def should_block_commit(
        self, results: dict[str, list[LintResult]], block_on_errors: bool = True, block_on_warnings: bool = False
    ) -> tuple[bool, str]:
        """Determine if linting results should block a commit"""
        summary = self.get_summary(results)

        if summary["failed_linters"]:
            return True, f"Linting failed: {', '.join(summary['failed_linters'])}"

        if block_on_errors and summary["total_errors"] > 0:
            return True, f"Found {summary['total_errors']} linting errors"

        if block_on_warnings and summary["total_warnings"] > 0:
            return True, f"Found {summary['total_warnings']} linting warnings"

        return False, "Linting passed"
