import logging
import os
import shlex
import tempfile
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .shell_runner import ShellRunner


def _get_default_base_branch() -> str:
    try:
        from src.config_loader import get_config

        return get_config().defaults.base_branch
    except Exception:
        return "main"


@dataclass
class CommitResult:
    """Result of a git commit attempt."""

    success: bool
    commit_sha: str | None = None
    error: str | None = None
    stdout: str = ""
    stderr: str = ""


class GitOps:
    """A service for handling Git operations via the ShellRunner."""

    def __init__(self, shell: ShellRunner):
        self.shell = shell
        self.logger = logging.getLogger(__name__)

    def git_status(self) -> str:
        """Gets the current git status."""
        result = self.shell.execute("git status --porcelain")
        if result.exit_code == 0:
            return result.stdout or "Working tree is clean."
        return f"Error getting git status:\n{result.stderr}"

    def git_diff(self) -> str:
        """Gets the current git diff."""
        result = self.shell.execute("git diff")
        if result.exit_code == 0:
            return result.stdout or "No changes to diff."
        return f"Error getting git diff:\n{result.stderr}"

    def has_changes(self) -> bool:
        """Returns True when there are uncommitted changes."""
        result = self.shell.execute("git status --porcelain")
        if result.exit_code != 0:
            self.logger.error(f"Error checking for changes: {result.stderr}")
            return False
        return bool(result.stdout.strip())

    def add_all(self) -> bool:
        """Stage all changes in the working tree."""
        result = self.shell.execute("git add -A")
        if result.exit_code != 0:
            self.logger.error(f"Failed to stage changes: {result.stderr}")
            return False
        return True

    def commit(self, message: str) -> CommitResult:
        """Commit staged changes with the provided message."""
        cleaned_message = (message or "").strip()
        if not cleaned_message:
            return CommitResult(success=False, error="Commit message is empty")

        message_file = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as handle:
                handle.write(cleaned_message)
                message_file = handle.name

            result = self.shell.execute(f"git commit -F {message_file}")
            if result.exit_code != 0:
                return CommitResult(
                    success=False,
                    error=f"Commit failed: {result.stderr}",
                    stdout=result.stdout,
                    stderr=result.stderr,
                )

            sha_result = self.shell.execute("git rev-parse HEAD")
            commit_sha = sha_result.stdout.strip() if sha_result.exit_code == 0 else None
            if not commit_sha:
                self.logger.warning("Commit succeeded but commit SHA could not be read")

            return CommitResult(
                success=True,
                commit_sha=commit_sha,
                stdout=result.stdout,
                stderr=result.stderr,
            )
        finally:
            if message_file:
                try:
                    os.unlink(message_file)
                except OSError:
                    pass

    def get_current_branch(self) -> str | None:
        """Gets the current active branch name."""
        result = self.shell.execute("git rev-parse --abbrev-ref HEAD")
        if result.exit_code == 0 and result.stdout:
            return result.stdout.strip()
        self.logger.error(f"Error getting current branch: {result.stderr}")
        return None

    def _local_branch_exists(self, branch: str) -> bool:
        if not branch:
            return False
        ref = f"refs/heads/{branch}"
        result = self.shell.execute(f"git show-ref --verify --quiet {shlex.quote(ref)}")
        return result.exit_code == 0

    def _remote_branch_exists(self, branch: str, remote: str = "origin") -> bool:
        if not branch:
            return False
        ref = f"refs/remotes/{remote}/{branch}"
        result = self.shell.execute(f"git show-ref --verify --quiet {shlex.quote(ref)}")
        return result.exit_code == 0

    def _resolve_default_base_branch(self, remote: str = "origin") -> str:
        head_result = self.shell.execute(f"git rev-parse --abbrev-ref {remote}/HEAD")
        if head_result.exit_code == 0 and head_result.stdout:
            head_ref = head_result.stdout.strip()
            if head_ref.startswith(f"{remote}/"):
                return head_ref[len(remote) + 1 :]
            return head_ref

        for fallback in ("main", "master"):
            if self._remote_branch_exists(fallback, remote) or self._local_branch_exists(fallback):
                return fallback

        return _get_default_base_branch()

    def resolve_pr_base_branch(self, base_branch: str | None, remote: str = "origin") -> str:
        candidate = base_branch or _get_default_base_branch()
        if self._remote_branch_exists(candidate, remote) or self._local_branch_exists(candidate):
            return candidate

        fallback = self._resolve_default_base_branch(remote)
        if fallback != candidate:
            self.logger.warning(
                "Base branch '%s' not found; falling back to '%s' for PR creation",
                candidate,
                fallback,
            )
        return fallback

    def ensure_local_branch(self, branch: str, remote: str = "origin") -> bool:
        if self._local_branch_exists(branch):
            return True
        if not self._remote_branch_exists(branch, remote):
            return False

        fetch_ref = f"{branch}:{branch}"
        result = self.shell.execute(f"git fetch {remote} {shlex.quote(fetch_ref)}")
        return result.exit_code == 0

    def remote_branch_exists(self, branch: str, remote: str = "origin") -> bool:
        """Check whether a branch exists on the remote."""
        return self._remote_branch_exists(branch, remote)

    def create_temp_branch(self, base_branch: str | None = None) -> str | None:
        """Creates a new temporary branch from the base branch."""
        if base_branch is None:
            base_branch = _get_default_base_branch()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"cce-agent/cce-edit-{timestamp}"

        # Ensure the base branch exists and is checked out
        self.shell.execute(f"git checkout {base_branch}")

        result = self.shell.execute(f"git checkout -b {branch_name}")
        if result.exit_code == 0:
            self.logger.info(f"Created and switched to temporary branch: {branch_name}")
            return branch_name

        self.logger.error(f"Failed to create temporary branch '{branch_name}': {result.stderr}")
        return None

    def merge_and_delete_branch(self, branch_name: str, target_branch: str = "main") -> tuple[bool, str]:
        """Merges the specified branch into the target and deletes it."""
        current_branch = self.get_current_branch()

        # If we're already on the target branch and trying to delete the current branch,
        # just return success since there's nothing to merge
        if branch_name == current_branch and current_branch == target_branch:
            msg = f"Already on target branch '{target_branch}' and trying to delete current branch. No merge needed."
            self.logger.info(msg)
            return True, msg

        # Switch to the target branch
        checkout_result = self.shell.execute(f"git checkout {target_branch}")
        if checkout_result.exit_code != 0:
            msg = f"Failed to switch to target branch '{target_branch}': {checkout_result.stderr}"
            self.logger.error(msg)
            return False, msg

        # Merge the temporary branch (only if it's different from the target branch)
        if branch_name != target_branch:
            merge_result = self.shell.execute(f"git merge --no-ff {branch_name}")
            if merge_result.exit_code != 0:
                msg = f"Failed to merge branch '{branch_name}': {merge_result.stderr}"
                self.logger.error(msg)
                # Attempt to abort the merge on failure
                self.shell.execute("git merge --abort")
                return False, msg

        # Now we're on the target branch, so we can safely delete the temporary branch
        delete_result = self.shell.execute(f"git branch -d {branch_name}")
        if delete_result.exit_code != 0:
            msg = f"Warning: Failed to delete branch '{branch_name}': {delete_result.stderr}"
            self.logger.warning(msg)
            return True, f"Merge successful, but failed to delete branch. Details: {msg}"

        # Push the target branch to remote after successful merge
        push_success = self.push_branch(target_branch)
        if not push_success:
            self.logger.warning(f"Merge successful but failed to push '{target_branch}' to remote")

        msg = f"Successfully merged and deleted branch '{branch_name}' into '{target_branch}'."
        self.logger.info(msg)
        return True, msg

    def abort_merge_and_delete_branch(self, branch_name: str, original_branch: str) -> tuple[bool, str]:
        """Abandons the temporary branch and returns to the original branch."""
        current_branch = self.get_current_branch()

        # If we're already on the original branch, just clean up
        if current_branch == original_branch:
            # Clean the working directory completely
            reset_result = self.shell.execute("git reset --hard HEAD")
            if reset_result.exit_code != 0:
                msg = f"Warning: Failed to reset working directory on branch '{original_branch}': {reset_result.stderr}"
                self.logger.warning(msg)
        else:
            # Switch back to the original branch
            checkout_result = self.shell.execute(f"git checkout {original_branch}")
            if checkout_result.exit_code != 0:
                msg = f"CRITICAL: Failed to switch back to original branch '{original_branch}'. Manual intervention required. Error: {checkout_result.stderr}"
                self.logger.critical(msg)
                return False, msg

            # Clean the working directory completely
            reset_result = self.shell.execute("git reset --hard HEAD")
            if reset_result.exit_code != 0:
                msg = f"Warning: Failed to reset working directory on branch '{original_branch}': {reset_result.stderr}"
                self.logger.warning(msg)
                # Don't return here, still try to delete the temp branch

        # Now we're on the original branch, so we can safely delete the temporary branch
        delete_result = self.shell.execute(f"git branch -D {branch_name}")  # Force delete
        if delete_result.exit_code != 0:
            msg = f"Warning: Failed to force-delete temporary branch '{branch_name}': {delete_result.stderr}"
            self.logger.warning(msg)
            return False, msg

        msg = f"Successfully abandoned and deleted branch '{branch_name}'."
        self.logger.info(msg)
        return True, msg

    def get_changed_files(self, since: str = "HEAD~1") -> list[str]:
        """Get list of files changed since specified commit."""
        result = self.shell.execute(f"git diff --name-only {since}")
        if result.exit_code == 0:
            return [f.strip() for f in result.stdout.split("\n") if f.strip()]
        return []

    def get_staged_files(self) -> list[str]:
        """Get list of staged files."""
        result = self.shell.execute("git diff --name-only --staged")
        if result.exit_code == 0:
            return [f.strip() for f in result.stdout.split("\n") if f.strip()]
        return []

    def get_modified_files(self) -> list[str]:
        """Get list of modified files (staged + unstaged)."""
        staged = self.get_staged_files()
        unstaged = self.get_changed_files("HEAD")
        return list(set(staged + unstaged))

    def get_commits_since_base(self, base_branch: str, head_branch: str | None = None) -> list[dict[str, str]]:
        """Get commits between base and head branches."""
        if not head_branch:
            head_branch = self.get_current_branch()
            if not head_branch:
                return []

        merge_base_result = self.shell.execute(
            f"git merge-base {shlex.quote(base_branch)} {shlex.quote(head_branch)}"
        )
        if merge_base_result.exit_code != 0:
            self.logger.error(
                f"Failed to determine merge base for {base_branch}..{head_branch}: {merge_base_result.stderr}"
            )
            return []

        merge_base = merge_base_result.stdout.strip()
        format_arg = shlex.quote("%H%x7c%s")
        log_result = self.shell.execute(
            f"git log --pretty=format:{format_arg} {shlex.quote(merge_base)}..{shlex.quote(head_branch)}"
        )
        if log_result.exit_code != 0:
            self.logger.error(f"Failed to list commits for {base_branch}..{head_branch}: {log_result.stderr}")
            return []

        commits: list[dict[str, str]] = []
        for line in log_result.stdout.splitlines():
            if not line.strip():
                continue
            sha, _, message = line.partition("|")
            commits.append({"sha": sha, "message": message})
        return commits

    def rebase_onto_base(
        self, base_branch: str, head_branch: str | None = None, remote: str = "origin"
    ) -> dict[str, Any]:
        """Rebase head branch onto base branch, returning status and whether rebase occurred."""
        if not head_branch:
            head_branch = self.get_current_branch()
            if not head_branch:
                return {"success": False, "error": "Could not determine current branch"}

        if head_branch == base_branch:
            return {"success": True, "rebased": False, "message": "Head branch is base branch"}

        fetch_result = self.shell.execute(f"git fetch {remote} {base_branch}")
        if fetch_result.exit_code != 0:
            self.logger.warning(f"Failed to fetch {remote}/{base_branch}: {fetch_result.stderr}")

        behind_result = self.shell.execute(f"git rev-list --left-right --count {base_branch}...{head_branch}")
        if behind_result.exit_code != 0:
            return {"success": False, "error": f"Failed to compare branches: {behind_result.stderr}"}

        try:
            behind_count = int(behind_result.stdout.strip().split()[0])
        except (IndexError, ValueError):
            behind_count = 0

        if behind_count == 0:
            return {"success": True, "rebased": False, "message": "Branch already up to date with base"}

        checkout_result = self.shell.execute(f"git checkout {head_branch}")
        if checkout_result.exit_code != 0:
            return {"success": False, "error": f"Failed to checkout {head_branch}: {checkout_result.stderr}"}

        rebase_result = self.shell.execute(f"git rebase {base_branch}")
        if rebase_result.exit_code != 0:
            self.shell.execute("git rebase --abort")
            return {"success": False, "error": f"Rebase failed: {rebase_result.stderr}"}

        return {"success": True, "rebased": True, "message": f"Rebased {head_branch} onto {base_branch}"}

    def push_branch(self, branch_name: str | None = None, remote: str = "origin", force: bool = False) -> bool:
        """Push the specified branch to remote repository."""
        if not branch_name:
            branch_name = self.get_current_branch()
            if not branch_name:
                self.logger.error("Could not determine branch to push")
                return False

        self.logger.info(f"Pushing branch '{branch_name}' to remote '{remote}'")
        if force:
            result = self.shell.execute(f"git push --force-with-lease {remote} {branch_name}")
        else:
            result = self.shell.execute(f"git push {remote} {branch_name}")

        if result.exit_code == 0:
            self.logger.info(f"Successfully pushed branch '{branch_name}' to remote")
            return True
        else:
            self.logger.error(f"Failed to push branch '{branch_name}': {result.stderr}")
            return False

    def publish_branch(
        self, branch_name: str | None = None, remote: str = "origin", set_upstream: bool = True
    ) -> tuple[bool, str]:
        """Publish a branch to remote repository with optional upstream tracking."""
        if not branch_name:
            branch_name = self.get_current_branch()
            if not branch_name:
                return False, "Could not determine branch to publish"

        # First, try to push with upstream setting if requested
        if set_upstream:
            self.logger.info(f"Publishing branch '{branch_name}' to remote '{remote}' with upstream tracking")
            result = self.shell.execute(f"git push -u {remote} {branch_name}")
        else:
            self.logger.info(f"Publishing branch '{branch_name}' to remote '{remote}'")
            result = self.shell.execute(f"git push {remote} {branch_name}")

        if result.exit_code == 0:
            msg = f"Successfully published branch '{branch_name}' to remote '{remote}'"
            self.logger.info(msg)
            return True, msg
        else:
            # If upstream push fails, try regular push
            if set_upstream:
                self.logger.warning(f"Upstream push failed, trying regular push: {result.stderr}")
                result = self.shell.execute(f"git push {remote} {branch_name}")
                if result.exit_code == 0:
                    msg = f"Successfully published branch '{branch_name}' to remote '{remote}' (without upstream)"
                    self.logger.info(msg)
                    return True, msg

            error_msg = f"Failed to publish branch '{branch_name}': {result.stderr}"
            self.logger.error(error_msg)
            return False, error_msg

    def _format_pr_body_from_commits(
        self,
        commits: list[dict[str, str]],
        base_branch: str,
        head_branch: str,
    ) -> str:
        lines = [
            "## Summary",
            f"- {len(commits)} commits from {head_branch} onto {base_branch}",
            "",
            "## Cycle Commits",
        ]
        for commit in commits:
            sha = (commit.get("sha") or "")[:7]
            message = (commit.get("message") or "").strip()
            if not message:
                continue
            suffix = f" ({sha})" if sha else ""
            lines.append(f"- {message}{suffix}")
        return "\n".join(lines).strip()

    def create_pull_request(
        self,
        title: str,
        body: str = "",
        head_branch: str | None = None,
        base_branch: str | None = None,
        labels: list[str] | None = None,
        draft: bool = False,
    ) -> dict[str, Any]:
        """Create a pull request using GitHub CLI."""
        try:
            # Check if GitHub CLI is available
            gh_check = self.shell.execute("gh --version")
            if gh_check.exit_code != 0:
                return {"success": False, "error": "GitHub CLI (gh) not available"}

            # Determine head branch
            if not head_branch:
                head_branch = self.get_current_branch()
                if not head_branch:
                    return {"success": False, "error": "Could not determine current branch"}

            # Check if we're on main/master branch (don't create PR for main branch)
            if head_branch in ["main", "master"]:
                return {"success": False, "error": "Cannot create PR from main/master branch"}

            base_branch = self.resolve_pr_base_branch(base_branch)
            if not self.ensure_local_branch(base_branch):
                return {
                    "success": False,
                    "error": f"Base branch '{base_branch}' not found locally or on remote",
                }

            rebase_result = self.rebase_onto_base(base_branch, head_branch)
            if not rebase_result.get("success", False):
                return {"success": False, "error": f"Rebase failed: {rebase_result.get('error', 'unknown error')}"}

            commits_since_base = self.get_commits_since_base(base_branch, head_branch)
            if not commits_since_base:
                return {
                    "success": False,
                    "error": "No commits between base and head; skipping PR creation",
                    "skipped": True,
                    "commits_since_base": [],
                }

            if not body:
                body = self._format_pr_body_from_commits(
                    commits_since_base,
                    base_branch=base_branch,
                    head_branch=head_branch,
                )

            # Push the head branch to remote before creating PR
            push_success = self.push_branch(head_branch, force=rebase_result.get("rebased", False))
            if not push_success:
                return {"success": False, "error": f"Failed to push branch '{head_branch}' to remote"}

            # Build the command
            cmd_parts = ["gh", "pr", "create", "--title", title, "--head", head_branch, "--base", base_branch]

            # Add body if provided
            if body:
                # Create temporary file for body
                import tempfile

                with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md") as f:
                    f.write(body)
                    body_file = f.name
                cmd_parts.extend(["--body-file", body_file])

            # Add labels if provided
            if labels:
                for label in labels:
                    cmd_parts.extend(["--label", label])

            # Add draft flag if requested
            if draft:
                cmd_parts.append("--draft")

            # Execute the command with proper quoting
            quoted_parts = []
            for part in cmd_parts:
                if " " in part or any(char in part for char in ['"', "'", "!", ":", "#"]):
                    quoted_parts.append(f'"{part}"')
                else:
                    quoted_parts.append(part)
            result = self.shell.execute(" ".join(quoted_parts))

            # Clean up temporary file if created
            if body and "body_file" in locals():
                try:
                    os.unlink(body_file)
                except:
                    pass

            if result.exit_code != 0:
                return {"success": False, "error": f"PR creation failed: {result.stderr}"}

            # Extract PR URL from output
            pr_url = result.stdout.strip()

            return {
                "success": True,
                "message": f"PR created successfully: {pr_url}",
                "details": result.stdout,
                "pr_url": pr_url,
                "commits_since_base": commits_since_base,
                "rebase_status": rebase_result,
            }

        except Exception as e:
            return {"success": False, "error": f"PR creation failed: {str(e)}"}

    def get_pull_request_info(self, pr_number: int) -> dict[str, Any]:
        """Get information about a specific pull request."""
        try:
            result = self.shell.execute(
                f"gh pr view {pr_number} --json number,title,body,headRefName,baseRefName,state,url"
            )
            if result.exit_code != 0:
                return {"success": False, "error": f"Failed to get PR info: {result.stderr}"}

            import json

            pr_data = json.loads(result.stdout)

            return {"success": True, "data": pr_data}

        except Exception as e:
            return {"success": False, "error": f"Failed to get PR info: {str(e)}"}

    def list_pull_requests(self, state: str = "open", head_branch: str | None = None) -> dict[str, Any]:
        """List pull requests with optional filtering."""
        try:
            cmd_parts = ["gh", "pr", "list", "--json", "number,title,headRefName,baseRefName,state,url"]

            if state:
                cmd_parts.extend(["--state", state])

            if head_branch:
                cmd_parts.extend(["--head", head_branch])

            result = self.shell.execute(" ".join(cmd_parts))
            if result.exit_code != 0:
                return {"success": False, "error": f"Failed to list PRs: {result.stderr}"}

            import json

            prs_data = json.loads(result.stdout)

            return {"success": True, "data": prs_data}

        except Exception as e:
            return {"success": False, "error": f"Failed to list PRs: {str(e)}"}

    def close_pull_request(self, pr_number: int, delete_branch: bool = False) -> dict[str, Any]:
        """Close a pull request and optionally delete the branch."""
        try:
            # Close the PR
            result = self.shell.execute(f"gh pr close {pr_number}")
            if result.exit_code != 0:
                return {"success": False, "error": f"Failed to close PR: {result.stderr}"}

            # Delete branch if requested
            if delete_branch:
                # Get PR info to find the head branch
                pr_info = self.get_pull_request_info(pr_number)
                if pr_info.get("success") and pr_info.get("data", {}).get("headRefName"):
                    head_branch = pr_info["data"]["headRefName"]
                    delete_result = self.shell.execute(f"git branch -D {head_branch}")
                    if delete_result.exit_code != 0:
                        return {
                            "success": True,
                            "message": f"PR closed but failed to delete branch {head_branch}: {delete_result.stderr}",
                        }

            return {"success": True, "message": f"PR #{pr_number} closed successfully"}

        except Exception as e:
            return {"success": False, "error": f"Failed to close PR: {str(e)}"}
