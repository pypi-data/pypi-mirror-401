"""
GitHub Ticket Extraction Utility

Provides comprehensive GitHub ticket extraction using gh CLI with structured JSON parsing.
Converts GitHub issues into enhanced Ticket objects with comments and metadata.
"""

import json
import logging
import re
from datetime import datetime
from typing import Any

from ..models import GitHubComment, Ticket


class GitHubTicketExtractor:
    """Extracts and parses GitHub tickets using gh CLI with --json output."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    async def from_url(url: str, shell_runner) -> Ticket | None:
        """
        Create Ticket from GitHub URL with full metadata.

        Args:
            url: GitHub issue URL (e.g., https://github.com/owner/repo/issues/123)
            shell_runner: Shell runner instance for executing commands

        Returns:
            Ticket object with full metadata or None if extraction fails
        """
        extractor = GitHubTicketExtractor()

        # Parse URL to extract owner, repo, and issue number
        url_info = extractor._parse_url(url)
        if not url_info:
            extractor.logger.error(f"Failed to parse GitHub URL: {url}")
            return None

        owner, repo, issue_number = url_info
        return await extractor.from_issue_number(issue_number, owner, repo, shell_runner)

    @staticmethod
    async def from_issue_number(issue_number: int, repo_owner: str, repo_name: str, shell_runner) -> Ticket | None:
        """
        Create Ticket from issue number with full metadata.

        Args:
            issue_number: GitHub issue number
            repo_owner: Repository owner/organization
            repo_name: Repository name
            shell_runner: Shell runner instance for executing commands

        Returns:
            Ticket object with full metadata or None if extraction fails
        """
        extractor = GitHubTicketExtractor()

        try:
            # Use gh CLI to get issue data in JSON format with comments
            cmd = f"gh issue view {issue_number} --repo {repo_owner}/{repo_name} --json number,title,body,state,author,labels,assignees,milestone,comments,reactionGroups,createdAt,updatedAt,url"

            extractor.logger.debug(f"Executing: {cmd}")
            result = shell_runner.execute(cmd)

            if result.exit_code != 0:
                extractor.logger.error(f"gh command failed: {result.stderr}")
                return None

            # Parse JSON response
            try:
                json_data = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                extractor.logger.error(f"Failed to parse JSON response: {e}")
                return None

            # Convert to Ticket object
            return extractor._parse_gh_json(json_data)

        except Exception as e:
            extractor.logger.error(f"GitHub ticket extraction failed: {e}")
            return None

    def _parse_url(self, url: str) -> tuple[str, str, int] | None:
        """
        Parse GitHub URL into (owner, repo, issue_number).

        Supports formats:
        - https://github.com/owner/repo/issues/123
        - http://github.com/owner/repo/issues/123
        - github.com/owner/repo/issues/123

        Args:
            url: GitHub URL string

        Returns:
            Tuple of (owner, repo, issue_number) or None if parsing fails
        """
        patterns = [
            r"https?://github\.com/([^/]+)/([^/]+)/issues/(\d+)",
            r"github\.com/([^/]+)/([^/]+)/issues/(\d+)",
            r"([^/]+)/([^/]+)/issues/(\d+)",  # Short format
            r"([^/]+)/([^/]+)#(\d+)",  # Even shorter format
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, repo, issue_number = match.groups()
                # Clean up repo name (remove .git suffix if present)
                repo = repo.replace(".git", "")
                return owner, repo, int(issue_number)

        # Try issue number only format (#123)
        issue_match = re.search(r"#(\d+)", url)
        if issue_match:
            # Need to get repo info from git remote
            return None  # Will be handled by calling code

        return None

    def _parse_gh_json(self, json_data: dict[str, Any]) -> Ticket:
        """
        Parse gh issue view --json output into Ticket object.

        Args:
            json_data: JSON data from gh issue view command

        Returns:
            Ticket object with all available metadata
        """
        # Parse basic fields
        number = json_data.get("number", 0)
        title = json_data.get("title", "")
        description = json_data.get("body", "")
        url = json_data.get("url", f"https://github.com/unknown/repo/issues/{number}")
        state = json_data.get("state", "open").lower()

        # Parse author
        author_data = json_data.get("author", {})
        author = author_data.get("login", "") if author_data else ""

        # Parse labels
        labels_data = json_data.get("labels", [])
        labels = [label.get("name", "") for label in labels_data if isinstance(label, dict)]

        # Parse assignees
        assignees_data = json_data.get("assignees", [])
        assignees = [assignee.get("login", "") for assignee in assignees_data if isinstance(assignee, dict)]

        # Parse milestone
        milestone_data = json_data.get("milestone", {})
        milestone = milestone_data.get("title", None) if milestone_data else None

        # Parse timestamps
        created_at = self._parse_datetime(json_data.get("createdAt"))
        updated_at = self._parse_datetime(json_data.get("updatedAt"))

        # Parse reactions (GitHub API uses reactionGroups format)
        reaction_groups_data = json_data.get("reactionGroups", [])
        reactions = {}
        if reaction_groups_data:
            for reaction_group in reaction_groups_data:
                if isinstance(reaction_group, dict):
                    content = reaction_group.get("content", "")
                    count = reaction_group.get("users", {}).get("totalCount", 0)
                    if content and count > 0:
                        reactions[content] = count

        # Parse comments
        comments_data = json_data.get("comments", [])
        comments = self._parse_comments(comments_data)

        return Ticket(
            number=number,
            title=title,
            description=description,
            url=url,
            labels=labels,
            created_at=created_at,
            updated_at=updated_at,
            state=state,
            author=author,
            assignees=assignees,
            milestone=milestone,
            comments=comments,
            reactions=reactions,
        )

    def _parse_comments(self, comments_data: list[dict[str, Any]]) -> list[GitHubComment]:
        """
        Parse comments from GitHub JSON into GitHubComment objects.

        Args:
            comments_data: List of comment dictionaries from GitHub API

        Returns:
            List of GitHubComment objects
        """
        comments = []

        for comment_data in comments_data:
            if not isinstance(comment_data, dict):
                continue

            # Parse comment fields
            comment_id = comment_data.get("id", 0)

            author_data = comment_data.get("author", {})
            author = author_data.get("login", "unknown") if author_data else "unknown"

            body = comment_data.get("body", "")
            created_at = self._parse_datetime(comment_data.get("createdAt"))
            updated_at = self._parse_datetime(comment_data.get("updatedAt"))

            # Parse comment reactions (GitHub API uses reactionGroups format)
            reaction_groups_data = comment_data.get("reactionGroups", [])
            reactions = {}
            if reaction_groups_data:
                for reaction_group in reaction_groups_data:
                    if isinstance(reaction_group, dict):
                        content = reaction_group.get("content", "")
                        count = reaction_group.get("users", {}).get("totalCount", 0)
                        if content and count > 0:
                            reactions[content] = count

            comment = GitHubComment(
                id=comment_id,
                author=author,
                body=body,
                created_at=created_at or datetime.now(),
                updated_at=updated_at or datetime.now(),
                reactions=reactions,
            )

            comments.append(comment)

        return comments

    def _parse_datetime(self, date_string: str | None) -> datetime | None:
        """
        Parse GitHub datetime string into datetime object.

        Args:
            date_string: ISO format datetime string from GitHub

        Returns:
            datetime object or None if parsing fails
        """
        if not date_string:
            return None

        try:
            # GitHub uses ISO format: 2023-12-01T12:34:56Z
            if date_string.endswith("Z"):
                date_string = date_string[:-1] + "+00:00"
            return datetime.fromisoformat(date_string)
        except (ValueError, AttributeError) as e:
            self.logger.warning(f"Failed to parse datetime '{date_string}': {e}")
            return None


class GitHubUtils:
    """Utility functions for GitHub operations."""

    @staticmethod
    def extract_repo_info(shell_runner) -> tuple[str, str] | None:
        """
        Get repo owner/name from git remote.

        Args:
            shell_runner: Shell runner instance

        Returns:
            Tuple of (owner, repo_name) or None if extraction fails
        """
        try:
            result = shell_runner.execute("git remote get-url origin")
            if result.exit_code != 0:
                return None

            repo_url = result.stdout.strip()

            # Parse various git remote URL formats
            patterns = [
                r"https://github\.com/([^/]+)/([^/]+)\.git",
                r"https://github\.com/([^/]+)/([^/]+)",
                r"git@github\.com:([^/]+)/([^/]+)\.git",
                r"git@github\.com:([^/]+)/([^/]+)",
            ]

            for pattern in patterns:
                match = re.search(pattern, repo_url)
                if match:
                    owner, repo = match.groups()
                    return owner, repo.replace(".git", "")

            return None

        except Exception:
            return None

    @staticmethod
    def parse_github_url(url: str) -> dict[str, Any] | None:
        """
        Parse various GitHub URL formats into components.

        Args:
            url: GitHub URL in various formats

        Returns:
            Dictionary with parsed components or None if parsing fails
        """
        extractor = GitHubTicketExtractor()
        url_info = extractor._parse_url(url)

        if url_info:
            owner, repo, issue_number = url_info
            return {
                "owner": owner,
                "repo": repo,
                "issue_number": issue_number,
                "url": f"https://github.com/{owner}/{repo}/issues/{issue_number}",
            }

        return None


# Convenience functions for easy usage
async def extract_ticket_from_url(url: str, shell_runner) -> Ticket | None:
    """
    Convenience function to extract ticket from URL.

    Args:
        url: GitHub issue URL
        shell_runner: Shell runner instance

    Returns:
        Ticket object or None if extraction fails
    """
    return await GitHubTicketExtractor.from_url(url, shell_runner)


async def extract_ticket_from_issue(issue_number: int, owner: str, repo: str, shell_runner) -> Ticket | None:
    """
    Convenience function to extract ticket from issue number.

    Args:
        issue_number: GitHub issue number
        owner: Repository owner
        repo: Repository name
        shell_runner: Shell runner instance

    Returns:
        Ticket object or None if extraction fails
    """
    return await GitHubTicketExtractor.from_issue_number(issue_number, owner, repo, shell_runner)
