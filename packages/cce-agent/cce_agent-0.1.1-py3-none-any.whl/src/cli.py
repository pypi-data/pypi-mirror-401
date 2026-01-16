#!/usr/bin/env python3
"""
CCE Agent CLI - Formal entrypoint for running CCE workflows.

This module provides a command-line interface for:
1. Running CCE locally on a GitHub issue
2. Launching CCE on a remote GitHub Codespace

Usage:
    python -m src.cli run --issue-url <URL>
    python -m src.cli launch codespace --codespace <NAME> --issue-url <URL>
    python -m src.cli report cycles
"""

import argparse
import asyncio
import json
import os
import re
import shlex
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Add project root to path for imports
sys.path.insert(0, os.path.abspath("."))


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="cce",
        description="Constitutional Context Engineering Agent - Run CCE workflows locally or remotely.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run CCE locally on an issue
  python -m src.cli run --issue-url https://github.com/owner/repo/issues/123

  # Launch CCE on a remote Codespace
  python -m src.cli launch codespace --codespace my-codespace --issue-url https://github.com/owner/repo/issues/123

  # Run with specific modes
  python -m src.cli run --issue-url <URL> --run-mode expert --execution-mode aider
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'run' subcommand - run CCE locally
    run_parser = subparsers.add_parser(
        "run",
        help="Run CCE locally on a GitHub issue",
        description="Execute CCE workflow locally against a GitHub issue.",
    )
    _add_common_args(run_parser)
    _add_run_args(run_parser)

    # 'run-deep-agents' subcommand - run deep agents workflow locally
    deep_parser = subparsers.add_parser(
        "run-deep-agents",
        aliases=["run-deep"],
        help="Run CCE using deep agents workflow locally",
        description="Execute CCE workflow locally using the deep agents engine.",
    )
    _add_common_args(deep_parser)
    _add_deep_agents_args(deep_parser)

    # 'launch' subcommand with nested subcommands
    launch_parser = subparsers.add_parser(
        "launch",
        help="Launch CCE on a remote environment",
        description="Launch CCE on a remote environment (Codespaces, SSH, etc.)",
    )
    launch_subparsers = launch_parser.add_subparsers(dest="target", help="Target environment")

    # 'launch codespace' subcommand
    cs_parser = launch_subparsers.add_parser(
        "codespace",
        aliases=["cs"],
        help="Launch CCE on a GitHub Codespace",
        description="Execute CCE workflow inside a GitHub Codespace.",
    )
    _add_codespace_args(cs_parser)
    _add_common_args(cs_parser)
    _add_run_args(cs_parser, include_workspace=False)  # workspace-root already added by codespace args

    # 'report' subcommand
    report_parser = subparsers.add_parser(
        "report",
        help="Generate analysis reports",
        description="Generate reports from run logs and artifacts.",
    )
    report_subparsers = report_parser.add_subparsers(dest="report_type", help="Available reports")
    cycles_parser = report_subparsers.add_parser(
        "cycles",
        help="Generate cycle analysis report",
        description="Summarize execution cycles across runs.",
    )
    cycles_parser.add_argument(
        "--output-path",
        help="Optional output path for the cycle analysis report",
    )

    return parser


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments shared across commands."""
    parser.add_argument(
        "--issue-url",
        required=True,
        help="GitHub issue URL to process (e.g., https://github.com/owner/repo/issues/123)",
    )
    parser.add_argument(
        "--target-repo",
        help="Target repository slug (owner/repo) for worktree operations when issue is in another repo",
    )
    parser.add_argument(
        "--target-repo-url",
        help="Target repository URL for worktree operations when issue is in another repo",
    )
    parser.add_argument(
        "--base-branch",
        default="auto",
        help="Base branch for git operations (default: auto, uses PR_BASE_BRANCH or repo default)",
    )
    parser.add_argument(
        "--run-mode",
        choices=["demo", "guided", "expert"],
        default="guided",
        help="Run mode controlling autonomy level (default: guided)",
    )
    parser.add_argument(
        "--execution-mode",
        choices=["native", "aider", "hybrid"],
        default="native",
        help="Execution mode for code changes (default: native)",
    )
    parser.add_argument("--artifact-path", help="Directory path to write JSON/MD summary artifacts")


def _add_run_args(parser: argparse.ArgumentParser, include_workspace: bool = True) -> None:
    """Add arguments specific to local run command."""
    if include_workspace:
        parser.add_argument("--workspace-root", default=".", help="Path to workspace root (default: current directory)")
    parser.add_argument(
        "--no-worktree",
        action="store_true",
        default=False,
        help="Run in the provided workspace without creating a git worktree",
    )
    parser.add_argument(
        "--enable-git-workflow",
        action="store_true",
        default=False,
        help="Enable git workflow integration (branch creation, commits)",
    )
    parser.add_argument(
        "--auto-pr", action="store_true", default=None, help="Automatically create a PR after completion"
    )
    parser.add_argument("--no-auto-pr", action="store_true", default=False, help="Disable automatic PR creation")
    parser.add_argument(
        "--use-aider", action="store_true", default=None, help="Enable Aider integration for code editing"
    )
    parser.add_argument("--no-aider", action="store_true", default=False, help="Disable Aider integration")
    parser.add_argument("--prompt-cache", action="store_true", default=None, help="Enable prompt caching")
    parser.add_argument("--no-prompt-cache", action="store_true", default=False, help="Disable prompt caching")
    parser.add_argument(
        "--recursion-limit",
        type=int,
        default=None,
        help=(
            "ReAct (tool loop) recursion limit per execution cycle. "
            "The outer execution graph limit is derived from max cycles."
        ),
    )


def _add_deep_agents_args(parser: argparse.ArgumentParser, include_workspace: bool = True) -> None:
    """Add arguments specific to deep agents execution."""
    if include_workspace:
        parser.add_argument("--workspace-root", default=".", help="Path to workspace root (default: current directory)")
    parser.add_argument(
        "--no-worktree",
        action="store_true",
        default=False,
        help="Run in the provided workspace without creating a git worktree",
    )
    parser.add_argument(
        "--auto-pr",
        action="store_true",
        default=None,
        help="Automatically create a PR after completion",
    )
    parser.add_argument(
        "--no-auto-pr",
        action="store_true",
        default=False,
        help="Disable automatic PR creation",
    )
    parser.set_defaults(read_only=None)
    parser.add_argument(
        "--read-only",
        dest="read_only",
        action="store_true",
        help="Run deep agents in read-only mode (no file edits)",
    )
    parser.add_argument(
        "--edit",
        dest="read_only",
        action="store_false",
        help="Allow deep agents to edit files (default when no flag is provided)",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=None,
        help="Timeout for deep agents execution (default: DEEP_AGENTS_TIMEOUT_SECONDS or 2400)",
    )
    parser.add_argument(
        "--max-cycles",
        type=int,
        default=None,
        help="Maximum deep agents cycles (default: config max_cycles)",
    )
    parser.add_argument(
        "--remaining-steps",
        type=int,
        default=500,
        help="Deep agents remaining_steps budget (default: 500)",
    )


def _add_codespace_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments specific to codespace launcher."""
    parser.add_argument(
        "--codespace", required=True, help="Name of the GitHub Codespace to target (from `gh codespace list`)"
    )
    parser.add_argument(
        "--cli-root",
        default=None,
        help="Path to CCE CLI repo inside the Codespace (dev-only; default: use installed package)",
    )
    parser.add_argument(
        "--auto-install-cli",
        action="store_true",
        default=False,
        help="Install cce-agent in the Codespace if the package is missing",
    )
    parser.add_argument(
        "--cli-version",
        default=None,
        help="Optional cce-agent version to install when using --auto-install-cli",
    )
    parser.add_argument(
        "--workspace-root",
        default=None,
        help="Path to workspace root inside the Codespace (default: /workspaces/<repo>)",
    )
    parser.add_argument(
        "--stream", action="store_true", default=True, help="Stream remote stdout/stderr live (default: enabled)"
    )
    parser.add_argument("--no-stream", action="store_false", dest="stream", help="Disable live streaming of output")
    parser.add_argument(
        "--download-artifacts",
        action="store_true",
        default=False,
        help="Download artifacts from remote after run completes",
    )
    parser.add_argument(
        "--remote-artifact-path",
        default="/tmp/cce-artifacts",
        help="Path on remote to store artifacts (default: /tmp/cce-artifacts)",
    )
    parser.add_argument(
        "--timeout", type=int, default=1800, help="Timeout in seconds for remote execution (default: 1800 = 30 minutes)"
    )
    parser.add_argument(
        "--use-deep-agents",
        action="store_true",
        default=False,
        help="Run deep agents workflow in the Codespace instead of the default engine",
    )
    parser.add_argument(
        "--deep-agents-read-only",
        action="store_true",
        default=False,
        help="Run deep agents in read-only mode (Codespace only)",
    )
    parser.add_argument(
        "--deep-agents-timeout",
        type=int,
        default=None,
        help="Deep agents timeout override in seconds (Codespace only)",
    )
    parser.add_argument(
        "--deep-agents-max-cycles",
        type=int,
        default=None,
        help="Deep agents max cycles override (Codespace only)",
    )
    parser.add_argument(
        "--deep-agents-remaining-steps",
        type=int,
        default=None,
        help="Deep agents remaining_steps override (Codespace only)",
    )


def _running_in_codespace() -> bool:
    return any(
        os.getenv(key)
        for key in (
            "CODESPACES",
            "CODESPACE_NAME",
            "GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN",
            "GITHUB_CODESPACE_TOKEN",
        )
    )


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    return cleaned.strip("-")


def _parse_issue_info(issue_url: str) -> tuple[str, str, int] | None:
    from src.tools.github_extractor import GitHubUtils

    info = GitHubUtils.parse_github_url(issue_url)
    if not info:
        return None
    return info["owner"], info["repo"], info["issue_number"]


def _parse_repo_slug(value: str) -> tuple[str, str] | None:
    if not value:
        return None

    raw = value.strip()
    if not raw:
        return None

    path = raw
    if raw.startswith("git@"):
        _, _, path = raw.partition(":")
    elif raw.startswith(("http://", "https://")):
        from urllib.parse import urlparse

        parsed = urlparse(raw)
        if parsed.netloc not in {"github.com", "www.github.com"}:
            return None
        path = parsed.path.strip("/")

    if path.endswith(".git"):
        path = path[: -len(".git")]

    parts = [part for part in path.strip("/").split("/") if part]
    if len(parts) < 2:
        return None

    owner, repo = parts[0], parts[1]
    if not owner or not repo:
        return None

    return owner, repo


def _resolve_target_repo(args: argparse.Namespace, issue_owner: str, issue_repo: str) -> tuple[str, str]:
    target_repo = _parse_repo_slug(args.target_repo) if getattr(args, "target_repo", None) else None
    target_repo_url = _parse_repo_slug(args.target_repo_url) if getattr(args, "target_repo_url", None) else None

    if getattr(args, "target_repo", None) and target_repo is None:
        raise RuntimeError("Invalid --target-repo value. Expected format: owner/repo")
    if getattr(args, "target_repo_url", None) and target_repo_url is None:
        raise RuntimeError("Invalid --target-repo-url value. Expected format: https://github.com/owner/repo")
    if target_repo and target_repo_url and target_repo != target_repo_url:
        raise RuntimeError(
            f"Target repo mismatch: --target-repo={target_repo[0]}/{target_repo[1]} "
            f"!= --target-repo-url={target_repo_url[0]}/{target_repo_url[1]}"
        )

    return target_repo or target_repo_url or (issue_owner, issue_repo)


def _resolve_repo_root(workspace_root: str) -> str | None:
    from src.tools.shell_runner import ShellRunner

    shell_runner = ShellRunner(workspace_root)
    result = shell_runner.execute("git rev-parse --show-toplevel")
    if result.exit_code == 0 and result.stdout:
        return result.stdout.strip()
    return None


def _git_ref_exists(shell_runner, ref: str) -> bool:
    result = shell_runner.execute(f"git rev-parse --verify --quiet {shlex.quote(ref)}")
    return result.exit_code == 0


def _normalize_base_branch(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized or normalized.lower() == "auto":
        return None
    return normalized


def _resolve_start_point(shell_runner, base_branch: str | None) -> str:
    normalized = _normalize_base_branch(base_branch)
    if normalized:
        if _git_ref_exists(shell_runner, normalized):
            return normalized
        remote_ref = f"origin/{normalized}"
        if _git_ref_exists(shell_runner, remote_ref):
            return remote_ref

    head_ref = shell_runner.execute("git rev-parse --abbrev-ref origin/HEAD")
    if head_ref.exit_code == 0 and head_ref.stdout:
        candidate = head_ref.stdout.strip()
        if _git_ref_exists(shell_runner, candidate):
            return candidate

    for fallback in ("origin/main", "origin/master", "main", "master"):
        if _git_ref_exists(shell_runner, fallback):
            return fallback

    return normalized or "main"


def _ensure_repo_clone(owner: str, repo: str, repo_cache_root: Path) -> Path:
    from src.tools.github_extractor import GitHubUtils
    from src.tools.shell_runner import ShellRunner

    clone_root = repo_cache_root / owner / repo
    if clone_root.exists():
        repo_root = _resolve_repo_root(str(clone_root))
        if repo_root is None:
            raise RuntimeError(f"Existing path is not a git repo: {clone_root}")
        repo_shell = ShellRunner(repo_root)
        repo_info = GitHubUtils.extract_repo_info(repo_shell)
        if repo_info and repo_info != (owner, repo):
            raise RuntimeError(f"Existing repo at {repo_root} does not match {owner}/{repo}")
        return Path(repo_root)

    clone_root.parent.mkdir(parents=True, exist_ok=True)
    shell_runner = ShellRunner(str(clone_root.parent))
    repo_slug = f"{owner}/{repo}"
    clone_path = shlex.quote(str(clone_root))

    https_url = f"https://github.com/{owner}/{repo}.git"
    clone_result = shell_runner.execute(f"git clone {shlex.quote(https_url)} {clone_path}")
    if clone_result.exit_code != 0:
        clone_result = shell_runner.execute(f"gh repo clone {shlex.quote(repo_slug)} {clone_path}")
        if clone_result.exit_code != 0:
            error_detail = clone_result.stderr or clone_result.stdout or "unknown error"
            raise RuntimeError(f"Failed to clone {owner}/{repo}: {error_detail}")

    return clone_root


def _resolve_source_repo_root(owner: str, repo: str, workspace_root: str) -> tuple[Path, str]:
    from src.tools.github_extractor import GitHubUtils
    from src.tools.shell_runner import ShellRunner

    repo_root = _resolve_repo_root(workspace_root)
    if repo_root:
        repo_shell = ShellRunner(repo_root)
        repo_info = GitHubUtils.extract_repo_info(repo_shell)
        if repo_info == (owner, repo):
            return Path(repo_root), "workspace"
        if repo_info:
            print(f"Workspace repo {repo_info[0]}/{repo_info[1]} does not match {owner}/{repo}; using clone.")
        else:
            print("Workspace repo has no origin remote; using clone.")

    repo_cache_root = Path(os.getenv("CCE_REPO_ROOT", Path.home() / ".cce" / "repos")).expanduser()
    return _ensure_repo_clone(owner, repo, repo_cache_root), "clone"


def _resolve_worktree_root(source_repo_root: Path, owner: str, repo: str) -> Path:
    override = os.getenv("CCE_WORKTREE_ROOT")
    if override:
        return Path(override).expanduser() / owner / repo
    return source_repo_root.parent / f"{source_repo_root.name}-worktrees"


def _resolve_auto_pr_flag(args: argparse.Namespace) -> bool | None:
    if getattr(args, "auto_pr", False):
        return True
    if getattr(args, "no_auto_pr", False):
        return False
    return None


def _resolve_pr_settings(args: argparse.Namespace, workspace_root: str) -> tuple[bool | None, str | None]:
    auto_pr_flag = _resolve_auto_pr_flag(args)
    base_branch = _normalize_base_branch(getattr(args, "base_branch", None))
    try:
        from src.config_loader import get_config

        config = get_config(workspace_root=workspace_root)
        auto_create_pr = bool(config.defaults.auto_create_pr)
        if base_branch is None:
            base_branch = config.defaults.base_branch
    except Exception:
        auto_create_pr = os.getenv("AUTO_CREATE_PR", "false").lower() == "true"
        if base_branch is None:
            base_branch = os.getenv("PR_BASE_BRANCH", "main")

    if auto_pr_flag is not None:
        auto_create_pr = auto_pr_flag

    return auto_create_pr, base_branch


def _resolve_use_aider_flag(args: argparse.Namespace) -> bool:
    if getattr(args, "use_aider", False):
        return True
    if getattr(args, "no_aider", False):
        return False
    return getattr(args, "execution_mode", "native") == "aider"


def _ensure_feature_branch(workspace_root: str, base_branch: str | None, ticket_number: int) -> str | None:
    from src.tools.git_ops import GitOps
    from src.tools.shell_runner import ShellRunner

    shell_runner = ShellRunner(workspace_root)
    git_ops = GitOps(shell_runner)
    current_branch = git_ops.get_current_branch()
    if current_branch and current_branch not in {"main", "master", "HEAD"}:
        return current_branch

    start_point = _resolve_start_point(shell_runner, base_branch)
    run_stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    branch_name = f"cce-agent/ticket-{ticket_number}-{run_stamp}"
    checkout_result = shell_runner.execute(
        f"git checkout -b {shlex.quote(branch_name)} {shlex.quote(start_point)}"
    )
    if checkout_result.exit_code != 0:
        print(
            "WARNING: Failed to create feature branch; continuing without branch isolation. "
            f"Details: {checkout_result.stderr or checkout_result.stdout}"
        )
        return current_branch

    print(f"Created feature branch: {branch_name}")
    return branch_name


def _prepare_local_worktree(args: argparse.Namespace, workspace_root: str) -> tuple[str, str | None]:
    if getattr(args, "no_worktree", False) or _running_in_codespace():
        return workspace_root, None

    issue_info = _parse_issue_info(args.issue_url)
    if not issue_info:
        print("WARNING: Could not parse issue URL; skipping worktree setup.")
        return workspace_root, None

    issue_owner, issue_repo, issue_number = issue_info
    owner, repo = _resolve_target_repo(args, issue_owner, issue_repo)
    if (owner, repo) != (issue_owner, issue_repo):
        print(f"Issue is from {issue_owner}/{issue_repo}; using target repo {owner}/{repo} for worktree.")
    source_repo_root, source_kind = _resolve_source_repo_root(owner, repo, workspace_root)
    worktree_root = _resolve_worktree_root(source_repo_root, owner, repo)
    worktree_root.mkdir(parents=True, exist_ok=True)

    run_stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    repo_slug = _slugify(repo) or "repo"
    worktree_dirname = f"issue-{issue_number}-{run_stamp}"
    worktree_path = worktree_root / worktree_dirname
    if worktree_path.exists():
        worktree_path = worktree_root / f"{worktree_dirname}-{os.getpid()}"

    branch_name = f"cce-agent/{repo_slug}-issue-{issue_number}-{run_stamp}"

    from src.tools.shell_runner import ShellRunner

    repo_shell = ShellRunner(str(source_repo_root))
    start_point = _resolve_start_point(repo_shell, args.base_branch)

    print(f"Preparing worktree for {owner}/{repo} ({source_kind})...")
    print(f"Worktree location: {worktree_path}")
    print(f"Worktree branch: {branch_name} (base: {start_point})")

    add_cmd = (
        f"git -C {shlex.quote(str(source_repo_root))} worktree add -b {shlex.quote(branch_name)} "
        f"{shlex.quote(str(worktree_path))} {shlex.quote(start_point)}"
    )
    add_result = repo_shell.execute(add_cmd)
    if add_result.exit_code != 0:
        error_detail = add_result.stderr or add_result.stdout or "unknown error"
        raise RuntimeError(f"Failed to create worktree: {error_detail}")

    return str(worktree_path), str(source_repo_root)


def _get_manifest_path(run_id: str | None) -> str | None:
    if not run_id:
        return None
    try:
        from src.config.artifact_root import get_runs_directory

        manifest_path = get_runs_directory() / run_id / "manifest.json"
        if manifest_path.exists():
            return str(manifest_path)
    except Exception:
        return None
    return None


async def run_local(args: argparse.Namespace) -> int:
    """Execute CCE workflow locally."""
    from src.agent import CCEAgent
    from src.config_loader import get_config, set_config_overrides
    from src.tools.github_extractor import extract_ticket_from_url
    from src.tools.shell_runner import ShellRunner

    workspace_root = os.path.abspath(args.workspace_root)
    try:
        workspace_root, worktree_source = _prepare_local_worktree(args, workspace_root)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 1

    print("=" * 60)
    print("CCE Agent - Local Execution")
    print("=" * 60)
    print(f"Issue URL: {args.issue_url}")
    if args.target_repo or args.target_repo_url:
        issue_info = _parse_issue_info(args.issue_url)
        if issue_info:
            target_owner, target_repo = _resolve_target_repo(args, issue_info[0], issue_info[1])
            print(f"Target Repo: {target_owner}/{target_repo}")
    print(f"Workspace: {workspace_root}")
    if worktree_source:
        print(f"Worktree Source: {worktree_source}")
    base_branch_label = _normalize_base_branch(args.base_branch) or "auto"
    print(f"Base Branch: {base_branch_label}")
    print(f"Run Mode: {args.run_mode}")
    print(f"Execution Mode: {args.execution_mode}")
    if args.recursion_limit is not None:
        print(f"Recursion Limit: {args.recursion_limit}")
    print("=" * 60)

    # Apply config overrides from CLI
    auto_pr = None
    if args.auto_pr:
        auto_pr = True
    elif args.no_auto_pr:
        auto_pr = False

    use_aider = _resolve_use_aider_flag(args)

    prompt_cache = None
    if args.prompt_cache:
        prompt_cache = True
    elif args.no_prompt_cache:
        prompt_cache = False

    base_branch_override = _normalize_base_branch(args.base_branch)
    set_config_overrides(
        base_branch=base_branch_override,
        auto_create_pr=auto_pr,
        use_aider=use_aider,
        prompt_cache=prompt_cache,
        recursion_limit=args.recursion_limit,
    )

    # Set environment variables for run mode and execution mode
    os.environ["RUN_MODE"] = args.run_mode
    os.environ["EXECUTION_MODE"] = args.execution_mode

    # Extract ticket from GitHub
    print("\nExtracting ticket from GitHub...")
    shell_runner = ShellRunner(workspace_root)

    try:
        ticket = await extract_ticket_from_url(args.issue_url, shell_runner)
        if ticket is None:
            print("ERROR: Failed to extract ticket from GitHub")
            print("Ensure `gh` CLI is installed and authenticated.")
            return 1
        print(f"Ticket: #{ticket.number} - {ticket.title}")
    except Exception as e:
        print(f"ERROR: Failed to extract ticket: {e}")
        return 1

    auto_create_pr, pr_base_branch = _resolve_pr_settings(args, workspace_root)
    if args.enable_git_workflow:
        _ensure_feature_branch(workspace_root, pr_base_branch, ticket.number)

    # Initialize and run CCE Agent
    print("\nInitializing CCE Agent...")
    get_config(workspace_root=workspace_root)
    agent = CCEAgent(
        workspace_root=workspace_root,
        git_base_branch=base_branch_override,
        enable_git_workflow=args.enable_git_workflow,
    )

    print("\nRunning CCE workflow...")
    try:
        result = await agent.process_ticket(ticket)
        success = hasattr(result, "status") and result.status in ["success", "completed"]
    except Exception as e:
        print(f"ERROR: CCE workflow failed: {e}")
        success = False
        result = None

    # Write artifacts if path specified
    if args.artifact_path:
        _write_artifacts(args.artifact_path, ticket, result, success)

    # Print summary
    print("\n" + "=" * 60)
    print("CCE WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"Status: {'SUCCESS' if success else 'FAILED'}")
    print(f"Issue: #{ticket.number} - {ticket.title}")
    run_id = getattr(result, "thread_id", None) if result else None
    manifest_path = _get_manifest_path(run_id)
    if run_id:
        print(f"Run ID: {run_id}")
    if manifest_path:
        print(f"Run Manifest: {manifest_path}")

    if args.enable_git_workflow and auto_create_pr and success:
        cycles = getattr(result, "execution_cycles", None) if result else None
        _maybe_create_pr(
            ticket=ticket,
            workspace_root=workspace_root,
            base_branch=pr_base_branch,
            cycles=cycles,
        )

    return 0 if success else 1


def _resolve_deep_agents_read_only(arg_value: bool | None) -> bool:
    if arg_value is not None:
        return arg_value
    env_value = os.getenv("DEEP_AGENTS_READ_ONLY")
    if env_value is None:
        return False
    return env_value.strip().lower() not in ("0", "false", "no", "off")


def _build_deep_agents_instruction(ticket, read_only: bool) -> str:
    if read_only:
        constraints = [
            "- Do NOT modify files or run git commands.",
            "- Produce a concise plan and risk assessment only.",
            "- Provide a final summary at the end.",
            "- Call signal_cycle_complete when finished.",
        ]
    else:
        constraints = [
            "- Do NOT run git commands.",
            "- You MAY read and modify files in the workspace to implement the ticket.",
            "- Start with a concise plan and risk assessment, then implement the highest-priority changes.",
            "- If you modify files, sync them to disk before completing.",
            "- Provide a final summary at the end.",
            "- Call signal_cycle_complete when finished.",
        ]

    return (
        "You are running the CCE workflow in deep agents mode.\n\n"
        f"Ticket #{ticket.number}: {ticket.title}\n"
        f"URL: {ticket.url}\n\n"
        "Ticket Body:\n"
        f"{ticket.description}\n\n"
        "Constraints:\n"
        f"{chr(10).join(constraints)}\n"
    )


def _extract_deep_agents_summary(result: dict[str, Any] | None) -> str | None:
    if not isinstance(result, dict):
        return None
    messages = result.get("messages") or []
    if not messages:
        return None
    last_message = messages[-1]
    return getattr(last_message, "content", str(last_message))


def _extract_tool_outputs(messages: list[Any], tool_name: str) -> list[str]:
    outputs: list[str] = []
    for message in messages:
        if isinstance(message, dict):
            if message.get("type") == "tool" and message.get("name") == tool_name:
                outputs.append(message.get("content", ""))
            continue

        msg_type = getattr(message, "type", None)
        msg_name = getattr(message, "name", None) or getattr(message, "tool_name", None)
        if msg_type == "tool" and msg_name == tool_name:
            outputs.append(getattr(message, "content", ""))
    return outputs


def _format_suggested_test_plan(plan: list[dict[str, Any]]) -> str:
    if not plan:
        return "- No test frameworks detected. Check project docs for recommended commands."

    lines = []
    for entry in plan:
        command = entry.get("command") or ""
        selected_tests = entry.get("selected_tests") or []
        if command:
            line = f"- `{command}`"
        else:
            line = "- (command unavailable)"
        if selected_tests:
            line += f" (targets: {', '.join(selected_tests)})"
        lines.append(line)
    return "\n".join(lines)


def _build_suggested_test_plan(workspace_root: str) -> str:
    from src.agent_testing_improvements import SmartTestDiscovery
    from src.tools.git_ops import GitOps
    from src.tools.shell_runner import ShellRunner
    from src.tools.validation.testing import FrameworkTestManager

    git_ops = GitOps(ShellRunner(workspace_root))
    changed_files: list[str] = []
    try:
        changed_files = git_ops.get_modified_files()
        if not changed_files:
            changed_files = git_ops.get_changed_files("HEAD~1")
    except Exception:
        changed_files = []

    target_files: list[str] | None = None
    if changed_files:
        changed_paths = [path if os.path.isabs(path) else os.path.join(workspace_root, path) for path in changed_files]
        try:
            target_files = SmartTestDiscovery(workspace_root).discover_relevant_tests(changed_paths)
        except Exception:
            target_files = None

    testing = FrameworkTestManager(workspace_root)
    plan_entries = testing.suggest_test_plan(target_files=target_files)
    return _format_suggested_test_plan(plan_entries)


def _extract_deep_agents_test_data(result: dict[str, Any] | None, workspace_root: str) -> tuple[str | None, str | None]:
    if not isinstance(result, dict):
        return None, None

    messages = result.get("messages") or []
    tool_outputs = _extract_tool_outputs(messages, "run_tests")
    test_output = tool_outputs[-1] if tool_outputs else None
    suggested_plan = None

    if not test_output or "No Tests Found" in test_output:
        suggested_plan = _build_suggested_test_plan(workspace_root)

    if test_output and suggested_plan and "Suggested Test Plan" not in test_output:
        test_output = f"{test_output}\n\n### Suggested Test Plan\n{suggested_plan}"

    return test_output, suggested_plan


def _write_deep_agents_artifacts(
    artifact_path: str,
    ticket,
    result: dict[str, Any] | None,
    success: bool,
    run_id: str | None,
    workspace_root: str,
) -> None:
    path = Path(artifact_path)
    path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC).isoformat()
    final_summary = _extract_deep_agents_summary(result)
    tests_output, suggested_plan = _extract_deep_agents_test_data(result, workspace_root)

    summary = {
        "timestamp": timestamp,
        "success": success,
        "ticket": {
            "number": ticket.number,
            "title": ticket.title,
            "url": ticket.url,
            "author": ticket.author,
            "state": ticket.state,
        },
        "run": {
            "id": run_id,
            "manifest_path": None,
        },
        "result": {
            "status": "success" if success else "failed",
            "final_summary": final_summary,
            "tests_summary": tests_output,
            "suggested_test_plan": suggested_plan,
        },
    }

    json_path = path / "cce_summary.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote JSON summary: {json_path}")

    tests_section = tests_output or "Not run"
    suggested_section = ""
    if suggested_plan and "Suggested Test Plan" not in (tests_output or ""):
        suggested_section = f"""\n## Suggested Test Plan\n\n{suggested_plan}\n"""

    md_content = f"""# CCE Run Summary

**Timestamp:** {timestamp}
**Status:** {"SUCCESS" if success else "FAILED"}

## Ticket

- **Number:** #{ticket.number}
- **Title:** {ticket.title}
- **URL:** {ticket.url}
- **Author:** {ticket.author}
- **State:** {ticket.state}

## Run

- **Run ID:** {run_id or "n/a"}
- **Manifest:** n/a

## Tests

{tests_section}
{suggested_section}

## Result

{final_summary or "No summary available"}
"""

    md_path = path / "cce_summary.md"
    with open(md_path, "w") as f:
        f.write(md_content)
    print(f"Wrote Markdown summary: {md_path}")


def _format_cycle_summary_section(cycles: list[Any] | None, commits: list[dict[str, str]]) -> str:
    if cycles:
        entries = []
        for idx, cycle in enumerate(cycles, start=1):
            cycle_number = getattr(cycle, "cycle_number", idx)
            summary = getattr(cycle, "cycle_summary", None) or getattr(cycle, "final_summary", "") or ""
            summary_line = summary.strip().splitlines()[0] if summary else "No summary recorded."
            commit_sha = getattr(cycle, "commit_sha", None) or "n/a"
            tests_run = getattr(cycle, "tests_run", 0)
            tests_passed = getattr(cycle, "tests_passed", 0)
            tests_failed = getattr(cycle, "tests_failed", 0)
            if tests_run:
                tests_line = f"{tests_passed}/{tests_run} passed"
                if tests_failed:
                    tests_line = f"{tests_passed}/{tests_run} passed ({tests_failed} failed)"
            else:
                tests_line = "Not recorded"
            entries.append(
                f"### Cycle {cycle_number}\n- Summary: {summary_line}\n- Commit: `{commit_sha}`\n- Tests: {tests_line}"
            )
        return "\n\n".join(entries)

    if commits:
        entries = []
        for idx, commit in enumerate(commits, start=1):
            sha = commit.get("sha", "")[:8] if commit.get("sha") else "unknown"
            message = commit.get("message", "No message")
            entries.append(f"### Cycle {idx}\n- Commit: `{sha}`\n- Summary: {message}")
        return "\n\n".join(entries)

    return "No cycle data recorded."


def _format_commit_list_section(commits: list[dict[str, str]]) -> str:
    if not commits:
        return "- No commits detected."
    return "\n".join(f"- `{commit.get('sha', '')[:8]}` {commit.get('message', '').strip()}" for commit in commits)


def _build_pr_body(
    ticket,
    cycles: list[Any] | None,
    commits: list[dict[str, str]],
    tests_output: str | None = None,
    suggested_plan: str | None = None,
) -> str:
    cycles_section = _format_cycle_summary_section(cycles, commits)
    commit_section = _format_commit_list_section(commits)

    body = f"""## Summary
- Automated changes via CCE

## Ticket
- {ticket.url}

## Cycles
{cycles_section}

## Commits
{commit_section}
"""

    if tests_output or suggested_plan:
        testing_section = tests_output or "Not run (no test output found)."
        if suggested_plan and "Suggested Test Plan" not in testing_section:
            testing_section = f"{testing_section}\n\n### Suggested Test Plan\n{suggested_plan}"
        body = f"{body}\n## Testing\n{testing_section}\n"

    return body


def _maybe_create_pr(
    ticket,
    workspace_root: str,
    base_branch: str | None,
    cycles: list[Any] | None = None,
    tests_output: str | None = None,
    suggested_plan: str | None = None,
) -> None:
    from src.tools.git_ops import GitOps
    from src.tools.shell_runner import ShellRunner

    shell_runner = ShellRunner(workspace_root)
    git_ops = GitOps(shell_runner)

    if git_ops.has_changes():
        print("WARNING: Uncommitted changes detected; they will not be included in the PR.")

    current_branch = git_ops.get_current_branch()
    if not current_branch:
        print("WARNING: Could not determine branch for PR creation; skipping.")
        return

    if current_branch in {"main", "master", "HEAD"}:
        print("WARNING: Current branch is main/master; skipping PR creation.")
        return

    resolved_base = git_ops.resolve_pr_base_branch(base_branch)
    git_ops.ensure_local_branch(resolved_base)
    commits_since_base = git_ops.get_commits_since_base(resolved_base, current_branch)

    pr_title = f"feat: {ticket.title.strip()}"
    pr_body = _build_pr_body(
        ticket=ticket,
        cycles=cycles,
        commits=commits_since_base,
        tests_output=tests_output,
        suggested_plan=suggested_plan,
    )

    pr_result = git_ops.create_pull_request(
        title=pr_title,
        body=pr_body,
        head_branch=current_branch,
        base_branch=resolved_base,
        labels=[],
    )

    if pr_result.get("skipped"):
        print(f"PR creation skipped: {pr_result.get('error', 'no commits')}")
    elif pr_result.get("success"):
        print(f"PR created successfully: {pr_result.get('pr_url')}")
    else:
        print(f"WARNING: PR creation failed: {pr_result.get('error')}")


async def run_deep_agents(args: argparse.Namespace) -> int:
    """Execute CCE workflow locally using deep agents."""
    from langchain_core.messages import HumanMessage

    from src.config import get_max_execution_cycles
    from src.deep_agents.cce_deep_agent import createCCEDeepAgent
    from src.tools.github_extractor import extract_ticket_from_url
    from src.tools.shell_runner import ShellRunner

    workspace_root = os.path.abspath(args.workspace_root)
    try:
        workspace_root, worktree_source = _prepare_local_worktree(args, workspace_root)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 1
    read_only = _resolve_deep_agents_read_only(args.read_only)
    timeout_seconds = args.timeout_seconds
    if timeout_seconds is None:
        timeout_raw = os.getenv("DEEP_AGENTS_TIMEOUT_SECONDS", "2400")
        try:
            timeout_seconds = int(timeout_raw)
        except ValueError:
            print(f"WARNING: Invalid DEEP_AGENTS_TIMEOUT_SECONDS={timeout_raw}; defaulting to 2400s")
            timeout_seconds = 2400

    max_cycles = args.max_cycles
    if max_cycles is None:
        try:
            max_cycles = get_max_execution_cycles()
        except Exception:
            max_cycles = None

    auto_create_pr, pr_base_branch = _resolve_pr_settings(args, workspace_root)

    print("=" * 60)
    print("CCE Agent - Deep Agents Execution")
    print("=" * 60)
    print(f"Issue URL: {args.issue_url}")
    if args.target_repo or args.target_repo_url:
        issue_info = _parse_issue_info(args.issue_url)
        if issue_info:
            target_owner, target_repo = _resolve_target_repo(args, issue_info[0], issue_info[1])
            print(f"Target Repo: {target_owner}/{target_repo}")
    print(f"Workspace: {workspace_root}")
    if worktree_source:
        print(f"Worktree Source: {worktree_source}")
    print(f"Read Only: {read_only}")
    print(f"Timeout: {timeout_seconds}s" if timeout_seconds else "Timeout: disabled")
    print(f"Max Cycles: {max_cycles if max_cycles is not None else 'default'}")
    print("=" * 60)

    print("\nExtracting ticket from GitHub...")
    shell_runner = ShellRunner(workspace_root)

    try:
        ticket = await extract_ticket_from_url(args.issue_url, shell_runner)
        if ticket is None:
            print("ERROR: Failed to extract ticket from GitHub")
            print("Ensure `gh` CLI is installed and authenticated.")
            return 1
        print(f"Ticket: #{ticket.number} - {ticket.title}")
    except Exception as e:
        print(f"ERROR: Failed to extract ticket: {e}")
        return 1

    if auto_create_pr and not read_only:
        _ensure_feature_branch(workspace_root, pr_base_branch, ticket.number)

    print("\nInitializing Deep Agents...")
    deep_agent = createCCEDeepAgent(workspace_root=workspace_root)

    instruction = _build_deep_agents_instruction(ticket, read_only)
    message = HumanMessage(content=instruction)
    run_id = f"deep-agents-{ticket.number}"
    config = {"configurable": {"thread_id": run_id}}

    if hasattr(deep_agent, "run_with_cycles"):
        run_coro = deep_agent.run_with_cycles(
            [message],
            context_memory={"ticket_url": ticket.url},
            remaining_steps=args.remaining_steps,
            execution_phases=[{"cycle_count": 0, "phase": "ticket_processing"}],
            max_cycles=max_cycles,
            config=config,
        )
    elif hasattr(deep_agent, "invoke_with_filesystem"):
        run_coro = deep_agent.invoke_with_filesystem(
            [message],
            context_memory={"ticket_url": ticket.url},
            remaining_steps=args.remaining_steps,
            execution_phases=[{"cycle_count": 0, "phase": "ticket_processing"}],
            config=config,
        )
    else:
        run_coro = deep_agent.ainvoke(
            {
                "messages": [message],
                "remaining_steps": args.remaining_steps,
                "context_memory": {"ticket_url": ticket.url},
                "execution_phases": [{"cycle_count": 0, "phase": "ticket_processing"}],
            },
            config=config,
        )

    print("\nRunning deep agents workflow...")
    try:
        if timeout_seconds and timeout_seconds > 0:
            result = await asyncio.wait_for(run_coro, timeout=timeout_seconds)
        else:
            result = await run_coro
        success = isinstance(result, dict) and bool(result.get("messages"))
    except TimeoutError:
        print(f"ERROR: Deep agents workflow timed out after {timeout_seconds}s")
        success = False
        result = None
    except Exception as e:
        print(f"ERROR: Deep agents workflow failed: {e}")
        success = False
        result = None

    if args.artifact_path:
        _write_deep_agents_artifacts(args.artifact_path, ticket, result, success, run_id, workspace_root)

    if auto_create_pr and success:
        tests_output, suggested_plan = _extract_deep_agents_test_data(result, workspace_root)
        _maybe_create_pr(
            ticket=ticket,
            workspace_root=workspace_root,
            base_branch=pr_base_branch or "main",
            cycles=None,
            tests_output=tests_output,
            suggested_plan=suggested_plan,
        )

    print("\n" + "=" * 60)
    print("CCE WORKFLOW COMPLETE (DEEP AGENTS)")
    print("=" * 60)
    print(f"Status: {'SUCCESS' if success else 'FAILED'}")
    print(f"Issue: #{ticket.number} - {ticket.title}")
    print(f"Run ID: {run_id}")

    return 0 if success else 1


def _write_artifacts(artifact_path: str, ticket, result, success: bool) -> None:
    """Write JSON and Markdown summary artifacts."""
    path = Path(artifact_path)
    path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC).isoformat()
    run_id = getattr(result, "thread_id", None) if result else None
    manifest_path = _get_manifest_path(run_id)

    # JSON summary
    summary = {
        "timestamp": timestamp,
        "success": success,
        "ticket": {
            "number": ticket.number,
            "title": ticket.title,
            "url": ticket.url,
            "author": ticket.author,
            "state": ticket.state,
        },
        "run": {
            "id": run_id,
            "manifest_path": manifest_path,
        },
        "result": {
            "status": getattr(result, "status", "unknown") if result else "failed",
            "final_summary": getattr(result, "final_summary", None) if result else None,
        },
    }

    json_path = path / "cce_summary.json"
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote JSON summary: {json_path}")

    # Markdown summary
    md_content = f"""# CCE Run Summary

**Timestamp:** {timestamp}
**Status:** {"SUCCESS" if success else "FAILED"}

## Ticket

- **Number:** #{ticket.number}
- **Title:** {ticket.title}
- **URL:** {ticket.url}
- **Author:** {ticket.author}
- **State:** {ticket.state}

## Run

- **Run ID:** {run_id or "n/a"}
- **Manifest:** {manifest_path or "n/a"}

## Result

{getattr(result, "final_summary", "No summary available") if result else "Workflow failed"}
"""

    md_path = path / "cce_summary.md"
    with open(md_path, "w") as f:
        f.write(md_content)
    print(f"Wrote Markdown summary: {md_path}")


def report_cycles(args: argparse.Namespace) -> int:
    """Generate a cycle analysis report from run logs."""
    from src.analysis.cycle_report import generate_cycle_analysis_report

    output_path = Path(args.output_path).expanduser() if args.output_path else None
    report_path = generate_cycle_analysis_report(output_path=output_path)
    print(f"Wrote cycle analysis report to {report_path}")
    return 0


async def launch_codespace(args: argparse.Namespace) -> int:
    """Launch CCE on a remote Codespace."""
    from src.launchers.codespaces import CodespacesLauncher

    print("=" * 60)
    print("CCE Agent - Codespace Launcher")
    print("=" * 60)
    print(f"Codespace: {args.codespace}")
    print(f"CLI Root: {args.cli_root or '(package)'}")
    print(f"Remote Workspace: {args.workspace_root or '(auto)'}")
    print(f"Issue URL: {args.issue_url}")
    base_branch_label = _normalize_base_branch(args.base_branch) or "auto"
    print(f"Base Branch: {base_branch_label}")
    print(f"Run Mode: {args.run_mode}")
    print(f"Execution Mode: {args.execution_mode}")
    if getattr(args, "use_deep_agents", False):
        print("Engine: deep-agents")
    if args.recursion_limit is not None:
        print(f"Recursion Limit: {args.recursion_limit}")
    if args.auto_install_cli:
        print("Auto-install CLI: enabled")
        if args.cli_version:
            print(f"CLI Version: {args.cli_version}")
    print(f"Streaming: {'enabled' if args.stream else 'disabled'}")
    print(f"Timeout: {args.timeout}s")
    print("=" * 60)

    launcher = CodespacesLauncher(
        codespace_name=args.codespace,
        workspace_root=args.workspace_root,
        cli_root=args.cli_root,
    )

    # Validate prerequisites
    print("\nValidating prerequisites...")
    try:
        launcher.validate_prerequisites(auto_install_cli=args.auto_install_cli)
        print("All prerequisites satisfied.")
        if launcher.cli_root:
            print(f"Resolved CLI root: {launcher.cli_root}")
        print(f"Resolved workspace: {launcher.workspace_root}")
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    # Build run options
    auto_pr = _resolve_auto_pr_flag(args)
    use_aider = _resolve_use_aider_flag(args)

    prompt_cache = None
    if args.prompt_cache:
        prompt_cache = True
    elif args.no_prompt_cache:
        prompt_cache = False

    run_options = {
        "base_branch": _normalize_base_branch(args.base_branch),
        "run_mode": args.run_mode,
        "execution_mode": args.execution_mode,
        "artifact_path": args.remote_artifact_path,
        "enable_git_workflow": getattr(args, "enable_git_workflow", False),
        "auto_pr": auto_pr,
        "use_aider": use_aider,
        "prompt_cache": prompt_cache,
        "recursion_limit": args.recursion_limit,
        "use_deep_agents": getattr(args, "use_deep_agents", False),
        "deep_agents_read_only": getattr(args, "deep_agents_read_only", False),
        "deep_agents_timeout": getattr(args, "deep_agents_timeout", None),
        "deep_agents_max_cycles": getattr(args, "deep_agents_max_cycles", None),
        "deep_agents_remaining_steps": getattr(args, "deep_agents_remaining_steps", None),
        "auto_install_cli": args.auto_install_cli,
        "cli_version": args.cli_version,
    }

    # Execute on remote
    print("\nLaunching CCE on remote Codespace...")
    exit_code = launcher.run_cce(issue_url=args.issue_url, stream=args.stream, timeout=args.timeout, **run_options)

    # Download artifacts if requested
    if args.download_artifacts and args.artifact_path:
        print("\nDownloading artifacts...")
        try:
            launcher.download_artifacts(remote_path=args.remote_artifact_path, local_path=args.artifact_path)
            print(f"Artifacts downloaded to: {args.artifact_path}")
        except Exception as e:
            print(f"WARNING: Failed to download artifacts: {e}")

    print("\n" + "=" * 60)
    print("REMOTE EXECUTION COMPLETE")
    print("=" * 60)
    status = "SUCCESS" if exit_code == 0 else "FAILED"
    print(f"Status: {status}")
    print(f"Exit Code: {exit_code}")
    print(f"Remote artifacts: {args.remote_artifact_path}")

    return exit_code


def main() -> int:
    """Main CLI entrypoint."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == "run":
        return asyncio.run(run_local(args))
    if args.command == "run-deep-agents":
        return asyncio.run(run_deep_agents(args))

    elif args.command == "launch":
        if args.target in ("codespace", "cs"):
            return asyncio.run(launch_codespace(args))
        else:
            print(f"ERROR: Unknown launch target: {args.target}")
            print("Available targets: codespace (cs)")
            return 1

    elif args.command == "report":
        if args.report_type == "cycles":
            return report_cycles(args)
        print("ERROR: Unknown report type")
        print("Available reports: cycles")
        return 1

    else:
        print(f"ERROR: Unknown command: {args.command}")
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
