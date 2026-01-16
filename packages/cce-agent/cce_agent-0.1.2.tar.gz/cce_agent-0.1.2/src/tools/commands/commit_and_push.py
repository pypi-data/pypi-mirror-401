"""
Commit and Push Command Implementation

This module provides programmatic access to the commit_and_push command
functionality as a LangChain tool, implementing the actual logic from
.cursor/commands/commit_and_push.md
"""

import logging
from typing import Any

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
async def commit_and_push(
    commit_message: str,
    branch: str | None = None,
    push: bool = True,
    create_pr: bool = False,
    create_branch: bool = False,
    base_branch: str = "main",
    pr_title: str | None = None,
    pr_description: str | None = None,
    allow_no_changes: bool = False,
) -> str:
    """
    Commit changes and optionally push to remote repository.
    This implements the actual commit_and_push command logic from .cursor/commands/commit_and_push.md

    Args:
        commit_message: Commit message for the changes
        branch: Target branch (defaults to current branch)
        push: Whether to push to remote repository
        create_pr: Whether to create a PR after successful push
        create_branch: Whether to create a new branch from base_branch
        base_branch: Base branch for new branch creation (defaults to "main")
        pr_title: Custom PR title (defaults to commit message first line)
        pr_description: Custom PR description (defaults to commit message)
        allow_no_changes: Allow skipping commit when no staged changes exist

    Returns:
        Commit and push status
    """
    try:
        # Import here to avoid circular imports
        from ..git_ops import GitOps
        from ..shell_runner import ShellRunner
        from src.workspace_context import get_workspace_root

        # Initialize required services
        workspace_root = get_workspace_root() or "."
        shell_runner = ShellRunner(workspace_root)
        git_ops = GitOps(shell_runner)

        # Phase 0: Create Branch (if requested)
        actual_base_branch = base_branch  # Default to provided base_branch
        if create_branch:
            branch_result = await _create_branch_if_needed(base_branch, git_ops, shell_runner)
            if not branch_result["success"]:
                return f"Branch creation failed: {branch_result['error']}"
            branch = branch_result["branch_name"]
            actual_base_branch = branch_result["base_branch"]  # Use the actual base branch determined

        # Phase 1: Pre-commit Validation
        validation_result = await _validate_before_commit(git_ops, shell_runner, allow_no_changes=allow_no_changes)
        if not validation_result["valid"]:
            return f"Pre-commit validation failed: {validation_result['error']}"

        # Phase 2: Commit Changes
        if validation_result.get("has_staged_changes", True):
            commit_result = await _commit_changes(commit_message, branch, git_ops, shell_runner)
            if not commit_result["success"]:
                return f"Commit failed: {commit_result['error']}"
        else:
            commit_result = {
                "success": True,
                "message": "No staged changes; commit skipped",
                "details": "",
                "commit_hash": None,
            }

        # Phase 3: Push Changes (if requested)
        push_result = {"success": True, "message": "Push skipped"}
        if push:
            rebase_result = {"success": True, "rebased": False}
            if create_pr:
                rebase_result = git_ops.rebase_onto_base(actual_base_branch, branch)
                if not rebase_result.get("success", False):
                    return f"Rebase failed: {rebase_result.get('error', 'unknown error')}"

            push_result = await _push_changes(branch, git_ops, shell_runner, force=rebase_result.get("rebased", False))

        # Phase 4: Create PR (if requested and push was successful)
        pr_result = {"success": True, "message": "PR creation skipped"}
        if create_pr and push and push_result.get("success", False):
            pr_result = await _create_pull_request(
                commit_message, branch, git_ops, shell_runner, pr_title, pr_description, actual_base_branch
            )

        # Phase 5: Post-commit Validation
        post_validation = await _validate_after_commit(git_ops, shell_runner)

        return f"""
Commit and Push Results

Commit: {commit_result.get("message", "Unknown status")}
Push: {push_result.get("message", "Unknown status")}
PR Creation: {pr_result.get("message", "Unknown status")}
Post-validation: {post_validation.get("status", "Unknown status")}

Details:
{commit_result.get("details", "")}
{push_result.get("details", "")}
{pr_result.get("details", "")}
"""

    except Exception as e:
        logger.error(f"Commit and push command failed: {e}")
        return f"Commit and push failed: {str(e)}"


async def _validate_before_commit(git_ops, shell_runner, allow_no_changes: bool = False) -> dict[str, Any]:
    """Validate repository state before committing."""
    try:
        # Check if we're in a git repository
        git_status = shell_runner.execute("git status")
        if git_status.exit_code != 0:
            return {"valid": False, "error": "Not in a git repository"}

        # Check current branch
        current_branch = shell_runner.execute("git branch --show-current")
        if current_branch.exit_code != 0:
            return {"valid": False, "error": "Could not determine current branch"}

        # Check for unstaged changes
        unstaged_changes = shell_runner.execute("git diff --name-only")
        if unstaged_changes.exit_code == 0 and unstaged_changes.stdout.strip():
            return {"valid": False, "error": "Unstaged changes detected. Please stage all changes before committing."}

        # Check for staged changes
        staged_changes = shell_runner.execute("git diff --cached --name-only")
        if staged_changes.exit_code != 0 or not staged_changes.stdout.strip():
            if allow_no_changes:
                return {
                    "valid": True,
                    "has_staged_changes": False,
                    "staged_files": [],
                    "current_branch": current_branch.stdout.strip(),
                }
            return {"valid": False, "error": "No staged changes to commit"}

        return {
            "valid": True,
            "has_staged_changes": True,
            "staged_files": staged_changes.stdout.strip().split("\n"),
            "current_branch": current_branch.stdout.strip(),
        }
    except Exception as e:
        return {"valid": False, "error": f"Pre-commit validation failed: {str(e)}"}


async def _commit_changes(commit_message: str, branch: str | None, git_ops, shell_runner) -> dict[str, Any]:
    """Commit the staged changes."""
    try:
        # Validate commit message
        if not commit_message or len(commit_message.strip()) < 3:
            return {"success": False, "error": "Commit message too short or empty"}

        # Check if we need to switch branches
        if branch:
            current_branch = shell_runner.execute("git branch --show-current")
            if current_branch.exit_code == 0 and current_branch.stdout.strip() != branch:
                # Switch to target branch
                switch_result = shell_runner.execute(f"git checkout {branch}")
                if switch_result.exit_code != 0:
                    return {"success": False, "error": f"Failed to switch to branch {branch}: {switch_result.stderr}"}

        # Perform the commit
        commit_result = shell_runner.execute(f'git commit -m "{commit_message}"')
        if commit_result.exit_code != 0:
            return {"success": False, "error": f"Commit failed: {commit_result.stderr}"}

        # Get commit hash
        commit_hash = shell_runner.execute("git rev-parse HEAD")
        commit_hash_value = commit_hash.stdout.strip() if commit_hash.exit_code == 0 else "unknown"

        return {
            "success": True,
            "message": f"Committed successfully: {commit_hash_value[:8]}",
            "details": commit_result.stdout,
            "commit_hash": commit_hash_value,
        }
    except Exception as e:
        return {"success": False, "error": f"Commit failed: {str(e)}"}


async def _push_changes(branch: str | None, git_ops, shell_runner, force: bool = False) -> dict[str, Any]:
    """Push changes to remote repository."""
    try:
        # Determine target branch
        if not branch:
            current_branch = shell_runner.execute("git branch --show-current")
            if current_branch.exit_code != 0:
                return {"success": False, "error": "Could not determine current branch"}
            branch = current_branch.stdout.strip()

        # Check if remote exists
        remote_result = shell_runner.execute("git remote -v")
        if remote_result.exit_code != 0 or not remote_result.stdout.strip():
            return {"success": False, "error": "No remote repository configured"}

        # Push to remote
        if force:
            push_result = shell_runner.execute(f"git push --force-with-lease origin {branch}")
        else:
            push_result = shell_runner.execute(f"git push origin {branch}")
        if push_result.exit_code != 0:
            return {"success": False, "error": f"Push failed: {push_result.stderr}"}

        return {"success": True, "message": f"Pushed successfully to origin/{branch}", "details": push_result.stdout}
    except Exception as e:
        return {"success": False, "error": f"Push failed: {str(e)}"}


async def _create_pull_request(
    commit_message: str,
    branch: str | None,
    git_ops,
    shell_runner,
    pr_title: str | None = None,
    pr_description: str | None = None,
    base_branch: str = "main",
) -> dict[str, Any]:
    """Create a pull request after successful push."""
    try:
        # Check if GitHub CLI is available
        gh_check = shell_runner.execute("gh --version")
        if gh_check.exit_code != 0:
            return {"success": False, "error": "GitHub CLI (gh) not available"}

        # Determine target branch
        if not branch:
            current_branch = shell_runner.execute("git branch --show-current")
            if current_branch.exit_code != 0:
                return {"success": False, "error": "Could not determine current branch"}
            branch = current_branch.stdout.strip()

        # Check if we're on main/master branch (don't create PR for main branch)
        if branch in ["main", "master"]:
            return {"success": False, "error": "Cannot create PR from main/master branch"}

        # Get remote repository info
        remote_result = shell_runner.execute("git remote get-url origin")
        if remote_result.exit_code != 0:
            return {"success": False, "error": "Could not determine remote repository"}

        resolved_base_branch = git_ops.resolve_pr_base_branch(base_branch)
        if not git_ops.ensure_local_branch(resolved_base_branch):
            return {"success": False, "error": f"Base branch '{resolved_base_branch}' not found locally or on remote"}

        commits_since_base = git_ops.get_commits_since_base(resolved_base_branch, branch)
        if not commits_since_base:
            return {
                "success": True,
                "message": f"PR creation skipped: no commits between {resolved_base_branch} and {branch}",
                "details": "",
                "skipped": True,
            }

        # Use provided PR title or extract from commit message (first line)
        if pr_title:
            final_pr_title = pr_title
        else:
            final_pr_title = commit_message.split("\n")[0].strip()
            if len(final_pr_title) > 50:
                final_pr_title = final_pr_title[:47] + "..."

        # Use provided PR description or commit message
        if pr_description:
            pr_body = pr_description
        else:
            pr_body = commit_message
            if len(pr_body) > 2000:
                pr_body = pr_body[:1997] + "..."

        # Create the pull request with correct base branch
        pr_cmd = (
            f'gh pr create --title "{final_pr_title}" --body "{pr_body}" --head {branch} --base {resolved_base_branch}'
        )
        pr_result = shell_runner.execute(pr_cmd)

        if pr_result.exit_code != 0:
            return {"success": False, "error": f"PR creation failed: {pr_result.stderr}"}

        # Extract PR URL from output
        pr_url = pr_result.stdout.strip()

        # SURGICAL FIX: Checkout back to base branch after PR creation
        checkout_result = shell_runner.execute(f"git checkout {resolved_base_branch}")
        checkout_message = ""
        if checkout_result.exit_code == 0:
            checkout_message = f"\nChecked out back to base branch: {resolved_base_branch}"
        else:
            checkout_message = (
                f"\nWarning: Could not checkout back to {resolved_base_branch}: {checkout_result.stderr}"
            )

        return {
            "success": True,
            "message": f"PR created successfully: {pr_url}{checkout_message}",
            "details": pr_result.stdout,
            "pr_url": pr_url,
        }
    except Exception as e:
        return {"success": False, "error": f"PR creation failed: {str(e)}"}


async def _validate_after_commit(git_ops, shell_runner) -> dict[str, Any]:
    """Validate repository state after commit."""
    try:
        # Check git status
        status_result = shell_runner.execute("git status --porcelain")
        if status_result.exit_code != 0:
            return {"status": "Could not check git status"}

        # Check if working directory is clean
        if status_result.stdout.strip():
            return {"status": "Working directory has uncommitted changes"}

        # Get latest commit info
        latest_commit = shell_runner.execute("git log -1 --oneline")
        if latest_commit.exit_code == 0:
            return {"status": f"Latest commit: {latest_commit.stdout.strip()}"}
        else:
            return {"status": "Could not retrieve latest commit info"}
    except Exception as e:
        return {"status": f"Post-commit validation failed: {str(e)}"}


async def _create_branch_if_needed(base_branch: str, git_ops, shell_runner) -> dict[str, Any]:
    """Create a new temporary branch from current branch (determined via shell runner)."""
    try:
        # Get current branch using shell runner (don't use hardcoded base)
        current_branch_result = shell_runner.execute("git branch --show-current")
        if current_branch_result.exit_code != 0:
            return {"success": False, "error": f"Failed to get current branch: {current_branch_result.stderr}"}

        actual_base_branch = current_branch_result.stdout.strip()
        if not actual_base_branch:
            actual_base_branch = base_branch  # Fallback to provided base_branch

        temp_branch = git_ops.create_temp_branch(base_branch=actual_base_branch)
        if not temp_branch:
            return {"success": False, "error": "Failed to create temporary branch"}

        stage_result = shell_runner.execute("git add .")
        if stage_result.exit_code != 0:
            return {"success": False, "error": f"Failed to stage changes: {stage_result.stderr}"}

        return {"success": True, "branch_name": temp_branch, "base_branch": actual_base_branch}
    except Exception as e:
        return {"success": False, "error": f"Branch creation failed: {str(e)}"}
