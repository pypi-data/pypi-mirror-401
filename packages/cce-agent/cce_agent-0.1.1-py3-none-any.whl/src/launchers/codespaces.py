"""
GitHub Codespaces Launcher for CCE Agent.

This module provides the CodespacesLauncher class for executing CCE workflows
inside a GitHub Codespace environment via `gh codespace ssh`.
"""

import json
import logging
import os
import queue
import re
import shlex
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class LauncherError(Exception):
    """Base exception for launcher errors."""

    message: str
    suggestion: str | None = None
    def __str__(self) -> str:
        msg = self.message
        if self.suggestion:
            msg += f"\n\nSuggestion: {self.suggestion}"
        return msg


class PrerequisiteError(LauncherError):
    """Raised when a prerequisite check fails."""

    pass


class CodespaceNotFoundError(LauncherError):
    """Raised when the specified Codespace cannot be found."""

    pass


class RemoteExecutionError(LauncherError):
    """Raised when remote command execution fails."""

    pass


@dataclass
class CodespaceInfo:
    """Information about a GitHub Codespace."""

    name: str
    state: str
    repository: str
    branch: str

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "CodespaceInfo":
        return cls(
            name=data.get("name", ""),
            state=data.get("state", ""),
            repository=data.get("repository", ""),
            branch=data.get("gitStatus", {}).get("ref", ""),
        )


class CodespacesLauncher:
    """
    Launcher for executing CCE workflows inside a GitHub Codespace.

    This class handles:
    - Prerequisite validation (gh CLI, auth, codespace existence)
    - Remote command construction and execution via `gh codespace ssh`
    - Live streaming of remote stdout/stderr
    - Artifact download via `gh codespace cp`

    Example:
        launcher = CodespacesLauncher(
            codespace_name="my-codespace",
            workspace_root="/workspaces/cce-agent"
        )
        launcher.validate_prerequisites()
        exit_code = launcher.run_cce(
            issue_url="https://github.com/owner/repo/issues/123",
            stream=True
        )
    """

    def __init__(
        self,
        codespace_name: str,
        workspace_root: str | None = None,
        cli_root: str | None = None,
    ):
        """
        Initialize the Codespaces launcher.

        Args:
            codespace_name: Name of the target Codespace (from `gh codespace list`)
            workspace_root: Path to the workspace root inside the Codespace
        """
        self.codespace_name = codespace_name
        self.workspace_root = workspace_root
        self.cli_root = cli_root
        self._codespace_info: CodespaceInfo | None = None
        self.logger = logging.getLogger(__name__)

    # =========================================================================
    # Prerequisite Validation
    # =========================================================================

    def validate_prerequisites(self, auto_install_cli: bool = False) -> None:
        """
        Validate all prerequisites for launching CCE on a Codespace.

        Raises:
            PrerequisiteError: If any prerequisite check fails
            CodespaceNotFoundError: If the specified Codespace doesn't exist
        """
        self._check_gh_cli_installed()
        self._check_gh_authenticated()
        self._check_codespace_exists()
        self._resolve_workspace_root()
        self._check_codespace_running()
        self._check_ssh_connectivity()
        self._check_cli_available(auto_install_cli=auto_install_cli)
        self._check_workspace_root()
        self._check_required_secrets()

    def _check_gh_cli_installed(self) -> None:
        """Check that the GitHub CLI is installed."""
        try:
            result = subprocess.run(["gh", "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise PrerequisiteError(
                    message="GitHub CLI (gh) is not properly installed.",
                    suggestion="Install with: brew install gh (macOS) or see https://cli.github.com/",
                )
            self.logger.debug(f"gh CLI version: {result.stdout.strip()}")
        except FileNotFoundError:
            raise PrerequisiteError(
                message="GitHub CLI (gh) is not installed or not in PATH.",
                suggestion="Install with: brew install gh (macOS) or apt install gh (Ubuntu)",
            )
        except subprocess.TimeoutExpired:
            raise PrerequisiteError(
                message="GitHub CLI (gh) timed out during version check.", suggestion="Check your system and try again."
            )

    def _check_gh_authenticated(self) -> None:
        """Check that the user is authenticated with GitHub CLI."""
        try:
            result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                raise PrerequisiteError(message="Not authenticated with GitHub CLI.", suggestion="Run: gh auth login")
            self.logger.debug(f"gh auth status: {result.stdout.strip()}")
        except subprocess.TimeoutExpired:
            raise PrerequisiteError(
                message="GitHub CLI authentication check timed out.",
                suggestion="Check your network connection and try again.",
            )

    def _check_codespace_exists(self) -> None:
        """Check that the specified Codespace exists."""
        try:
            result = subprocess.run(
                [
                    "gh",
                    "codespace",
                    "view",
                    "--codespace",
                    self.codespace_name,
                    "--json",
                    "name,state,repository,gitStatus",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                if "not found" in result.stderr.lower() or "could not find" in result.stderr.lower():
                    raise CodespaceNotFoundError(
                        message=f"Codespace '{self.codespace_name}' not found.",
                        suggestion="Run `gh codespace list` to see available Codespaces.",
                    )
                raise PrerequisiteError(
                    message=f"Failed to query Codespace: {result.stderr}",
                    suggestion="Ensure the Codespace name is correct.",
                )

            data = json.loads(result.stdout)
            self._codespace_info = CodespaceInfo.from_json(data)
            self.logger.info(f"Found Codespace: {self._codespace_info.name} (state: {self._codespace_info.state})")

        except json.JSONDecodeError as e:
            raise PrerequisiteError(
                message=f"Failed to parse Codespace info: {e}",
                suggestion="Try running `gh codespace view --codespace {name}` manually.",
            )
        except subprocess.TimeoutExpired:
            raise PrerequisiteError(
                message="Codespace query timed out.", suggestion="Check your network connection and try again."
            )

    def _resolve_workspace_root(self) -> None:
        """Resolve the workspace root based on codespace repo when not explicitly set."""
        if self.workspace_root:
            return

        if self._codespace_info is None:
            self._check_codespace_exists()

        repo = self._codespace_info.repository if self._codespace_info else ""
        repo_name = repo.split("/")[-1] if repo else ""
        if repo_name:
            self.workspace_root = f"/workspaces/{repo_name}"
            self.logger.info("Resolved workspace root to %s based on repo %s", self.workspace_root, repo)
            return

        self.workspace_root = "/workspaces/cce-agent"
        self.logger.info("Falling back to workspace root %s", self.workspace_root)

    def _resolve_cli_root(self) -> None:
        """Resolve the CLI root if explicitly provided."""
        if self.cli_root:
            return

    def _check_codespace_running(self) -> None:
        """Check that the Codespace is running and reachable."""
        if self._codespace_info is None:
            self._check_codespace_exists()

        if self._codespace_info.state.lower() != "available":
            print(f"Codespace is in state '{self._codespace_info.state}'. Attempting to connect...")
            try:
                result = self._run_remote_command("echo 'connectivity-test'", timeout=120)
                if result.returncode != 0 or "connectivity-test" not in result.stdout:
                    raise PrerequisiteError(
                        message="Codespace is not running and could not be started automatically.",
                        suggestion="Open the Codespace or run `gh codespace ssh -c <name>` to start it, then retry.",
                    )
                print("Codespace is reachable.")

                # Refresh info
                self._codespace_info = None
                self._check_codespace_exists()

            except subprocess.TimeoutExpired:
                raise PrerequisiteError(
                    message="Codespace startup timed out.",
                    suggestion="Open the Codespace or run `gh codespace ssh -c <name>` to start it, then retry.",
                )

    def _run_remote_command(self, command: str, timeout: int = 30) -> subprocess.CompletedProcess:
        """Run a command inside the Codespace via gh codespace ssh."""
        return subprocess.run(
            ["gh", "codespace", "ssh", "--codespace", self.codespace_name, "--", command],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

    def _check_ssh_connectivity(self) -> None:
        """Verify that SSH connectivity to the Codespace works."""
        try:
            result = self._run_remote_command("echo 'connectivity-test'", timeout=30)
        except subprocess.TimeoutExpired:
            raise PrerequisiteError(
                message="SSH connectivity check timed out.",
                suggestion="Ensure the Codespace is running and reachable, then try again.",
            )
        if result.returncode != 0 or "connectivity-test" not in result.stdout:
            raise PrerequisiteError(
                message="SSH connection to the Codespace failed.",
                suggestion="Ensure the Codespace has SSH server support (sshd) and try again.",
            )

    def _check_workspace_root(self) -> None:
        """Ensure the workspace root exists in the Codespace."""
        self._resolve_workspace_root()
        escaped_workspace = shlex.quote(self.workspace_root)
        result = self._run_remote_command(f"test -d {escaped_workspace}", timeout=30)
        if result.returncode != 0:
            raise PrerequisiteError(
                message=f"Workspace path not found: {self.workspace_root}",
                suggestion="Confirm the repo is checked out and pass --workspace-root if needed.",
            )

    def _check_cli_root(self) -> None:
        """Ensure the CLI root exists and contains the CCE CLI entrypoint."""
        if not self.cli_root:
            return
        self._resolve_cli_root()
        escaped_cli = shlex.quote(self.cli_root)
        result = self._run_remote_command(f"test -f {escaped_cli}/src/cli.py", timeout=30)
        if result.returncode != 0:
            raise PrerequisiteError(
                message=f"CCE CLI not found at: {self.cli_root}",
                suggestion="Clone the cce-agent repo in the Codespace and pass --cli-root to its path.",
            )

    def _check_cli_package(self) -> bool:
        """Check whether the cce-agent package is available in the Codespace."""
        result = self._run_remote_command("python -m cce_agent.cli --help", timeout=30)
        return result.returncode == 0

    def _check_cli_available(self, auto_install_cli: bool) -> None:
        """Ensure either repo-based CLI or packaged CLI is available."""
        if self.cli_root:
            self._check_cli_root()
            return
        if self._check_cli_package():
            return
        if auto_install_cli:
            # Defer installation to the bootstrap command.
            return
        raise PrerequisiteError(
            message="CCE CLI package not found in the Codespace.",
            suggestion="Install with `pip install cce-agent` or pass --auto-install-cli/--cli-root.",
        )

    def _check_required_secrets(self) -> None:
        """Ensure required LLM secrets are available in the Codespace."""
        self._resolve_workspace_root()
        self._resolve_cli_root()
        escaped_workspace = shlex.quote(self.workspace_root)
        escaped_cli = shlex.quote(self.cli_root) if self.cli_root else None
        script = (
            'check_env_file() { file="$1"; '
            'if [ -f "$file" ]; then '
            "awk -F= 'BEGIN{found=0} "
            "/^[[:space:]]*(export[[:space:]]+)?(OPENAI_API_KEY|ANTHROPIC_API_KEY)=/ {"
            'val=$0; sub(/^[^=]*=/, "", val); gsub(/^\"|\"$/, "", val); '
            "if (length(val) > 0) found=1 } "
            "END{exit(found?0:1)}' "
            '"$file"; '
            "return $?; "
            "fi; "
            "return 1; "
            "}; "
            'if [ -n "$OPENAI_API_KEY" ] || [ -n "$ANTHROPIC_API_KEY" ]; then exit 0; fi; '
            f"check_env_file {escaped_workspace}/.env && exit 0; "
            + (
                f"if [ {escaped_cli} != {escaped_workspace} ]; then "
                f"check_env_file {escaped_cli}/.env && exit 0; "
                "fi; "
                if escaped_cli
                else ""
            )
            + "exit 1"
        )
        command = "sh -lc " + shlex.quote(script)
        result = self._run_remote_command(command, timeout=30)
        if result.returncode != 0:
            raise PrerequisiteError(
                message="Missing OPENAI_API_KEY or ANTHROPIC_API_KEY in the Codespace environment.",
                suggestion="Add the secret in GitHub Codespaces settings and restart the Codespace.",
            )

    # =========================================================================
    # Remote Execution
    # =========================================================================

    def run_cce(
        self,
        issue_url: str,
        stream: bool = True,
        timeout: int = 1800,
        base_branch: str | None = None,
        run_mode: str = "guided",
        execution_mode: str = "native",
        artifact_path: str = "/tmp/cce-artifacts",
        recursion_limit: int | None = None,
        use_deep_agents: bool = False,
        deep_agents_read_only: bool = False,
        deep_agents_timeout: int | None = None,
        deep_agents_max_cycles: int | None = None,
        deep_agents_remaining_steps: int | None = None,
        enable_git_workflow: bool = False,
        auto_pr: bool | None = None,
        use_aider: bool | None = None,
        prompt_cache: bool | None = None,
        auto_install_cli: bool = False,
        cli_version: str | None = None,
        **kwargs,
    ) -> int:
        """
        Execute CCE on the remote Codespace.

        Args:
            issue_url: GitHub issue URL to process
            stream: Whether to stream stdout/stderr live
            timeout: Timeout in seconds for the remote execution
            base_branch: Base branch for git operations (None to auto-resolve)
            run_mode: Run mode (demo, guided, expert)
            execution_mode: Execution mode (native, aider, hybrid)
            artifact_path: Path on remote to store artifacts
            recursion_limit: LangGraph recursion limit override
            use_deep_agents: Use deep agents CLI path instead of default engine
            deep_agents_read_only: Run deep agents in read-only mode
            deep_agents_timeout: Deep agents timeout override
            deep_agents_max_cycles: Deep agents max cycles override
            deep_agents_remaining_steps: Deep agents remaining_steps override
            enable_git_workflow: Whether to enable git workflow
            auto_pr: Whether to auto-create a PR (True/False/None)
            use_aider: Whether to enable Aider (True/False/None)
            prompt_cache: Whether to enable prompt caching (True/False/None)
            auto_install_cli: Whether to install the cce-agent package if missing
            cli_version: Optional cce-agent version to install
            **kwargs: Additional arguments (ignored)

        Returns:
            Exit code from the remote execution
        """
        self._resolve_workspace_root()
        # Build the remote command
        remote_cmd = self._build_remote_command(
            issue_url=issue_url,
            base_branch=base_branch,
            run_mode=run_mode,
            execution_mode=execution_mode,
            artifact_path=artifact_path,
            recursion_limit=recursion_limit,
            use_deep_agents=use_deep_agents,
            deep_agents_read_only=deep_agents_read_only,
            deep_agents_timeout=deep_agents_timeout,
            deep_agents_max_cycles=deep_agents_max_cycles,
            deep_agents_remaining_steps=deep_agents_remaining_steps,
            enable_git_workflow=enable_git_workflow,
            auto_pr=auto_pr,
            use_aider=use_aider,
            prompt_cache=prompt_cache,
            auto_install_cli=auto_install_cli,
            cli_version=cli_version,
        )

        # Print redacted command for visibility
        redacted_cmd = self._redact_command(remote_cmd)
        print(f"\nRemote command: {redacted_cmd}\n")

        # Execute via gh codespace ssh
        full_command = ["gh", "codespace", "ssh", "--codespace", self.codespace_name, "--", remote_cmd]

        self.logger.info(f"Executing: {' '.join(full_command[:5])}...")

        if stream:
            return self._execute_streaming(full_command, timeout)
        else:
            return self._execute_buffered(full_command, timeout)

    def _build_remote_command(
        self,
        issue_url: str,
        base_branch: str | None,
        run_mode: str,
        execution_mode: str,
        artifact_path: str,
        recursion_limit: int | None,
        use_deep_agents: bool,
        deep_agents_read_only: bool,
        deep_agents_timeout: int | None,
        deep_agents_max_cycles: int | None,
        deep_agents_remaining_steps: int | None,
        enable_git_workflow: bool,
        auto_pr: bool | None,
        use_aider: bool | None,
        prompt_cache: bool | None,
        auto_install_cli: bool,
        cli_version: str | None,
    ) -> str:
        """Build the command to execute on the remote Codespace."""
        self._resolve_workspace_root()
        self._resolve_cli_root()

        # Escape all user-provided values
        escaped_issue_url = shlex.quote(issue_url)
        escaped_workspace = shlex.quote(self.workspace_root)
        escaped_cli_root = shlex.quote(self.cli_root) if self.cli_root else ""
        escaped_artifact_path = shlex.quote(artifact_path)
        base_branch_value = base_branch or ""
        escaped_base_branch = shlex.quote(base_branch_value)
        escaped_run_mode = shlex.quote(run_mode)
        escaped_execution_mode = shlex.quote(execution_mode)
        escaped_recursion_limit = shlex.quote(str(recursion_limit)) if recursion_limit is not None else None
        escaped_cli_version = shlex.quote(cli_version) if cli_version else ""
        escaped_deep_agents_timeout = (
            shlex.quote(str(deep_agents_timeout)) if deep_agents_timeout is not None else None
        )
        escaped_deep_agents_max_cycles = (
            shlex.quote(str(deep_agents_max_cycles)) if deep_agents_max_cycles is not None else None
        )
        escaped_deep_agents_remaining_steps = (
            shlex.quote(str(deep_agents_remaining_steps)) if deep_agents_remaining_steps is not None else None
        )

        python_bin = os.path.join(self.cli_root, "venv", "bin", "python") if self.cli_root else "python"
        escaped_python_bin = shlex.quote(python_bin)

        deep_agents_read_only_export = "1" if deep_agents_read_only else "0"
        auto_install_cli_export = "1" if auto_install_cli else "0"
        use_repo_cli_export = "1" if self.cli_root else "0"

        # Build the full bootstrap + run command
        # 1. Change to CLI directory
        # 2. Ensure we're in a venv if available
        # 3. Run CCE
        bootstrap_parts = [
            f"cd {escaped_cli_root}" if self.cli_root else f"cd {escaped_workspace}",
            "echo '=== CCE Remote Execution Starting ==='",
            'echo "CLI Root: $(pwd)"' if self.cli_root else 'echo "CLI Root: (package)"',
            f'echo "Target Workspace: {self.workspace_root}"',
            "echo \"CLI repo branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'N/A')\""
            if self.cli_root
            else "echo \"CLI repo branch: (package)\"",
            f"echo \"Target repo branch: $(git -C {escaped_workspace} rev-parse --abbrev-ref HEAD 2>/dev/null || "
            "echo 'N/A')\"",
            "set -a",
            f"if [ -f {escaped_workspace}/.env ]; then . {escaped_workspace}/.env; fi",
            f"if [ -n \"{escaped_cli_root}\" ] && [ -f {escaped_cli_root}/.env ]; then . {escaped_cli_root}/.env; fi",
            "set +a",
            f"BASE_BRANCH={escaped_base_branch}",
            'RESOLVED_BASE_BRANCH="$BASE_BRANCH"',
            'if [ -z "$RESOLVED_BASE_BRANCH" ] || [ "$RESOLVED_BASE_BRANCH" = "auto" ]; then '
            'RESOLVED_BASE_BRANCH="${PR_BASE_BRANCH:-}"; fi',
            f'if [ -z "$RESOLVED_BASE_BRANCH" ] || [ "$RESOLVED_BASE_BRANCH" = "auto" ]; then '
            f'RESOLVED_BASE_BRANCH=$(git -C {escaped_workspace} symbolic-ref --short refs/remotes/origin/HEAD '
            '2>/dev/null | sed "s|^origin/||"); fi',
            'if [ -z "$RESOLVED_BASE_BRANCH" ]; then RESOLVED_BASE_BRANCH=main; fi',
            'echo "Resolved base branch: $RESOLVED_BASE_BRANCH"',
            f"export DEEP_AGENTS_READ_ONLY={deep_agents_read_only_export}",
            f"export AUTO_INSTALL_CLI={auto_install_cli_export}",
            f"export USE_REPO_CLI={use_repo_cli_export}",
            f"export CCE_CLI_VERSION={escaped_cli_version}",
            # Ensure gh + git can authenticate for pushes/PR creation in the Codespace.
            # GitHub CLI honors GH_TOKEN, and `gh auth setup-git` configures git to use it as a credential helper.
            'export GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"',
            'if [ -n "$GH_TOKEN" ]; then gh auth setup-git -h github.com >/dev/null 2>&1 || true; fi',
            "echo '=== Preparing target repo workspace ==='",
            (
                f"if git -C {escaped_workspace} rev-parse --is-inside-work-tree >/dev/null 2>&1; then "
                f"if [ -d {escaped_workspace}/.artifacts ]; then "
                f"mkdir -p {escaped_artifact_path}/workspace_scratch && "
                f"mv {escaped_workspace}/.artifacts "
                f"{escaped_artifact_path}/workspace_scratch/.artifacts-$(date +%Y%m%d-%H%M%S) || true; "
                "fi; "
                f"if [ -n \"$(git -C {escaped_workspace} status --porcelain)\" ]; then "
                "echo 'ERROR: Target repo has uncommitted changes (please clean before running):'; "
                f"git -C {escaped_workspace} status --porcelain; exit 2; "
                "fi; "
                f"if git -C {escaped_workspace} rev-parse --verify --quiet \"$RESOLVED_BASE_BRANCH\"; then "
                f"git -C {escaped_workspace} checkout \"$RESOLVED_BASE_BRANCH\"; "
                f"elif git -C {escaped_workspace} rev-parse --verify --quiet \"origin/$RESOLVED_BASE_BRANCH\"; then "
                f"git -C {escaped_workspace} checkout -B \"$RESOLVED_BASE_BRANCH\" "
                f"\"origin/$RESOLVED_BASE_BRANCH\"; "
                "else echo \"WARNING: base branch $RESOLVED_BASE_BRANCH not found; staying on current branch\"; fi; "
                "else echo 'WARNING: target workspace is not a git repo; skipping checkout'; fi"
            ),
            # Ensure all agent artifacts land in a known, downloadable location (and avoid polluting the target repo).
            f"mkdir -p {escaped_artifact_path}",
            f"export CCE_ARTIFACT_ROOT={escaped_artifact_path}",
            # Keep tracing enabled, but allow LangSmith to compress runs (prevents oversized multipart payloads).
            "export LANGSMITH_DISABLE_RUN_COMPRESSION=false",
            # Codespaces can be slower (dependency installs, large repos). Ensure per-cycle timeouts
            # don't kill long-running tool calls like package installs.
            'export CCE_REACT_TIMEOUT="${CCE_REACT_TIMEOUT:-1800}"',
            'export CCE_LLM_INVOKE_TIMEOUT="${CCE_LLM_INVOKE_TIMEOUT:-600}"',
            "export PYTHONUNBUFFERED=1",
            f"PYTHON_BIN={escaped_python_bin}",
            'if [ ! -x "$PYTHON_BIN" ]; then PYTHON_BIN=python; fi',
            'echo "Python: $PYTHON_BIN"',
            # Ensure dependencies are installed for repo-based execution
            (
                "{ $PYTHON_BIN -m pip install -q -r requirements.txt 2>/dev/null || true; }"
                if self.cli_root
                else "true"
            ),
            # Ensure the package is available when not using repo-based CLI
            (
                "if [ \"$USE_REPO_CLI\" = \"0\" ]; then "
                "if ! $PYTHON_BIN -m cce_agent.cli --help >/dev/null 2>&1; then "
                "if [ \"$AUTO_INSTALL_CLI\" = \"1\" ]; then "
                "VENV_DIR=\"${CCE_CLI_VENV:-$HOME/.cce/venv}\"; "
                "mkdir -p \"$VENV_DIR\"; "
                "if [ ! -x \"$VENV_DIR/bin/python\" ]; then python -m venv \"$VENV_DIR\"; fi; "
                "PYTHON_BIN=\"$VENV_DIR/bin/python\"; "
                "$PYTHON_BIN -m pip install -q --upgrade pip; "
                "if [ -n \"$CCE_CLI_VERSION\" ]; then "
                "$PYTHON_BIN -m pip install -q \"cce-agent==${CCE_CLI_VERSION}\"; "
                "else "
                "$PYTHON_BIN -m pip install -q cce-agent; "
                "fi; "
                "else "
                "echo 'ERROR: cce-agent package not installed. Use --auto-install-cli or install manually.'; "
                "exit 2; "
                "fi; "
                "fi; "
                "fi"
            ),
            "echo '=== Running CCE ==='",
            (
                f"$PYTHON_BIN -m "
                f"{'src.cli' if self.cli_root else 'cce_agent.cli'} run-deep-agents --issue-url {escaped_issue_url} "
                f"--workspace-root {escaped_workspace} --artifact-path {escaped_artifact_path}"
                + " --no-worktree"
                + ' --base-branch "$RESOLVED_BASE_BRANCH"'
                + (" --read-only" if deep_agents_read_only else " --edit")
                + (f" --timeout-seconds {escaped_deep_agents_timeout}" if escaped_deep_agents_timeout else "")
                + (f" --max-cycles {escaped_deep_agents_max_cycles}" if escaped_deep_agents_max_cycles else "")
                + (f" --remaining-steps {escaped_deep_agents_remaining_steps}" if escaped_deep_agents_remaining_steps else "")
                + (" --auto-pr" if auto_pr is True else "")
                + (" --no-auto-pr" if auto_pr is False else "")
            )
            if use_deep_agents
            else (
                f"$PYTHON_BIN -m "
                f"{'src.cli' if self.cli_root else 'cce_agent.cli'} run --issue-url {escaped_issue_url} "
                f"--workspace-root {escaped_workspace} "
                f"--base-branch \"$RESOLVED_BASE_BRANCH\" --run-mode {escaped_run_mode} "
                f"--execution-mode {escaped_execution_mode} --artifact-path {escaped_artifact_path} --no-worktree"
                + (f" --recursion-limit {escaped_recursion_limit}" if escaped_recursion_limit else "")
                + (" --enable-git-workflow" if enable_git_workflow else "")
                + (" --auto-pr" if auto_pr is True else "")
                + (" --no-auto-pr" if auto_pr is False else "")
                + (" --use-aider" if use_aider is True else "")
                + (" --no-aider" if use_aider is False else "")
                + (" --prompt-cache" if prompt_cache is True else "")
                + (" --no-prompt-cache" if prompt_cache is False else "")
            ),
        ]

        return " && ".join(bootstrap_parts)

    def _execute_streaming(self, command: list[str], timeout: int) -> int:
        """Execute command with live streaming of output."""
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered
            )
            if process.stdout is None:
                raise RemoteExecutionError(
                    message="Failed to capture remote output stream.",
                    suggestion="Try running without --stream to debug.",
                )

            output_queue: queue.Queue[str | None] = queue.Queue()

            def _reader() -> None:
                for line in process.stdout:
                    output_queue.put(line)
                output_queue.put(None)

            reader_thread = threading.Thread(target=_reader, daemon=True)
            reader_thread.start()

            start_time = time.monotonic()

            while True:
                if timeout and (time.monotonic() - start_time) > timeout:
                    process.kill()
                    process.wait()
                    raise RemoteExecutionError(
                        message=f"Remote execution timed out after {timeout} seconds.",
                        suggestion="Increase timeout with --timeout flag or check for issues in the Codespace.",
                    )

                try:
                    line = output_queue.get(timeout=0.5)
                except queue.Empty:
                    if process.poll() is not None and not reader_thread.is_alive():
                        break
                    continue

                if line is None:
                    break
                print(line, end="", flush=True)

            return process.wait()

        except RemoteExecutionError:
            raise
        except Exception as e:
            raise RemoteExecutionError(
                message=f"Remote execution failed: {e}", suggestion="Check gh CLI setup and Codespace connectivity."
            )

    def _execute_buffered(self, command: list[str], timeout: int) -> int:
        """Execute command and buffer output."""
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)

            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

            return result.returncode

        except subprocess.TimeoutExpired:
            raise RemoteExecutionError(
                message=f"Remote execution timed out after {timeout} seconds.",
                suggestion="Increase timeout with --timeout flag.",
            )

    # =========================================================================
    # Artifact Management
    # =========================================================================

    def download_artifacts(
        self,
        remote_path: str,
        local_path: str,
    ) -> None:
        """
        Download artifacts from the remote Codespace.

        Args:
            remote_path: Path on the remote Codespace
            local_path: Local path to download to

        Raises:
            RemoteExecutionError: If download fails
        """
        # Create local directory
        os.makedirs(local_path, exist_ok=True)

        # Use gh codespace cp to download
        # Format: gh codespace cp remote:<path> <local_path> --codespace <name>
        remote_spec = f"remote:{remote_path}"

        command = [
            "gh",
            "codespace",
            "cp",
            "--codespace",
            self.codespace_name,
            "--expand",
            "--recursive",
            remote_spec,
            local_path,
        ]

        self.logger.info(f"Downloading artifacts: {remote_path} -> {local_path}")

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)

            if result.returncode != 0:
                raise RemoteExecutionError(
                    message=f"Failed to download artifacts: {result.stderr}",
                    suggestion="Check that the remote path exists and is accessible.",
                )

            self.logger.info(f"Artifacts downloaded successfully to {local_path}")

        except subprocess.TimeoutExpired:
            raise RemoteExecutionError(
                message="Artifact download timed out.", suggestion="Check network connection and try again."
            )

    def upload_file(
        self,
        local_path: str,
        remote_path: str,
    ) -> None:
        """
        Upload a file to the remote Codespace.

        Args:
            local_path: Local file path
            remote_path: Path on the remote Codespace

        Raises:
            RemoteExecutionError: If upload fails
        """
        remote_spec = f"remote:{remote_path}"

        command = ["gh", "codespace", "cp", "--codespace", self.codespace_name, "--expand", local_path, remote_spec]

        self.logger.info(f"Uploading: {local_path} -> {remote_path}")

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=60)

            if result.returncode != 0:
                raise RemoteExecutionError(
                    message=f"Failed to upload file: {result.stderr}",
                    suggestion="Check that the local file exists and remote path is writable.",
                )

        except subprocess.TimeoutExpired:
            raise RemoteExecutionError(
                message="File upload timed out.", suggestion="Check network connection and try again."
            )

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def _redact_command(self, command: str) -> str:
        """Redact sensitive values from a command string."""
        redacted = command
        patterns = [
            (re.compile(r"(?i)(token|key|secret|password|passwd|auth|authorization)=([^\\s'\"&]+)"), r"\1=REDACTED"),
            (
                re.compile(
                    r"(?i)\\b(OPENAI_API_KEY|ANTHROPIC_API_KEY|GH_PAT|GITHUB_TOKEN|GITLAB_TOKEN|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY)=([^\\s'\"&]+)"
                ),
                r"\1=REDACTED",
            ),
            (re.compile(r"(?i)(https?://)([^/@\\s]+)@"), r"\1REDACTED@"),
            (re.compile(r"\\b(ghp_[A-Za-z0-9]{10,}|github_pat_[A-Za-z0-9_]{10,}|sk-[A-Za-z0-9]{10,})\\b"), "REDACTED"),
        ]
        for pattern, replacement in patterns:
            redacted = pattern.sub(replacement, redacted)
        return redacted

    def get_codespace_info(self) -> CodespaceInfo | None:
        """Get cached Codespace information."""
        return self._codespace_info

    def check_ssh_connectivity(self) -> bool:
        """
        Check if SSH connectivity to the Codespace works.

        Returns:
            True if connectivity works, False otherwise
        """
        try:
            result = self._run_remote_command("echo 'connectivity-test'", timeout=30)
            return result.returncode == 0 and "connectivity-test" in result.stdout
        except Exception:
            return False
