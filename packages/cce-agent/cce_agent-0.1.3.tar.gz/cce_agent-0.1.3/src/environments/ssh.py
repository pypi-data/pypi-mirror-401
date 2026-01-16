import logging
import os

import paramiko

from .base import BaseEnvironment, ShellResult


class CodespacesSSHEnvironment(BaseEnvironment):
    """
    An environment that connects to a GitHub Codespace via SSH.

    This class implements the `BaseEnvironment` interface for a remote
    Codespace, using the `paramiko` library to execute commands and
    manage files over a persistent SSH connection.
    """

    def __init__(self, host: str, username: str, key_path: str, workspace_root: str):
        self.host = host
        self.workspace_root = workspace_root
        self._ssh: paramiko.SSHClient = None
        self._sftp: paramiko.SFTPClient = None
        self.logger = logging.getLogger(__name__)
        self._ensure_github_auth()

    def _ensure_github_auth(self):
        """
        Ensures GitHub authentication is working by applying the auth fix directly in Python.
        This addresses the Cursor/Codespaces token refresh issue by using the GH_PAT secret.
        """
        import os
        import subprocess

        self.logger.info("Ensuring GitHub CLI authentication...")

        # Get the GH_PAT from environment (available as codespace secret)
        gh_pat = os.environ.get("GH_PAT")
        if not gh_pat:
            self.logger.error("GH_PAT environment variable not found")
            raise ConnectionError(
                "GH_PAT environment variable is not set. Please ensure it's configured as a codespace secret."
            )

        # Remove the Codespaces-scoped token from our process environment
        # This prevents conflicts with the personal access token
        original_github_token = os.environ.get("GITHUB_TOKEN")
        if "GITHUB_TOKEN" in os.environ:
            self.logger.info("Temporarily removing GITHUB_TOKEN to use GH_PAT")
            del os.environ["GITHUB_TOKEN"]

        try:
            self.logger.info("Authenticating with GitHub using GH_PAT...")

            # Login with the PAT directly using subprocess.Popen for stdin control
            process = subprocess.Popen(
                ["gh", "auth", "login", "--hostname", "github.com", "--with-token"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate(input=gh_pat)

            if process.returncode != 0:
                self.logger.error(f"GitHub auth login failed: {stderr}")
                raise ConnectionError(f"GitHub authentication failed: {stderr}")

            self.logger.info("GitHub auth login successful")

            # Setup git to use the new authentication
            result = subprocess.run(["gh", "auth", "setup-git"], capture_output=True, text=True, check=False)

            if result.returncode != 0:
                self.logger.warning(f"GitHub auth setup-git had issues: {result.stderr}")
            else:
                self.logger.info("GitHub auth setup-git completed")

            # Verify the authentication worked
            verify_result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, check=False)

            if verify_result.returncode == 0:
                self.logger.info("GitHub CLI authentication verification successful")
                self.logger.debug(f"Auth status: {verify_result.stdout}")
            else:
                self.logger.warning(f"Auth verification had issues: {verify_result.stderr}")

        except Exception as e:
            # Restore original token if something went wrong
            if original_github_token:
                os.environ["GITHUB_TOKEN"] = original_github_token
            self.logger.error(f"Failed to set up GitHub authentication: {e}")
            raise ConnectionError(f"Cannot fix GitHub authentication: {e}") from e

    def execute_shell(self, command: str, timeout: int = 60) -> ShellResult:
        """
        Executes a shell command in the remote workspace using a direct
        `gh cs ssh` call, which is more robust than managing a paramiko Transport.
        """
        import subprocess

        self.logger.info(f"Executing command via 'gh cs ssh': {command}")

        # Construct the full command to be executed remotely
        # The `--` separates `gh` flags from the command to be run on the remote host.
        full_command = ["gh", "cs", "ssh", "--codespace", self.host, "--", f"cd {self.workspace_root} && {command}"]

        try:
            process = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,  # We handle the exit code manually
            )

            self.logger.info(f"Command executed. Exit code: {process.returncode}")

            return ShellResult(
                exit_code=process.returncode,
                stdout=process.stdout,
                stderr=process.stderr,
            )
        except FileNotFoundError:
            self.logger.error("`gh` CLI not found. Please ensure it is installed and in your PATH.")
            raise
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out after {timeout} seconds: {command}")
            return ShellResult(exit_code=124, stdout="", stderr="Command timed out.")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during shell execution: {e}")
            return ShellResult(exit_code=1, stdout="", stderr=str(e))

    def read_file(self, path: str) -> str:
        """Reads a file from the remote workspace using `gh`."""
        # Use `cat` to read the file content remotely
        result = self.execute_shell(f"cat '{path}'")
        if result.exit_code == 0:
            return result.stdout
        raise FileNotFoundError(f"Could not read file {path}. Stderr: {result.stderr}")

    def write_file(self, path: str, content: str) -> None:
        """Writes to a file in the remote workspace using `gh`."""
        # Use `tee` to write the content to the file.
        # We need to escape the content to handle special characters.
        import shlex

        escaped_content = shlex.quote(content)

        remote_dir = os.path.dirname(path)
        if remote_dir:
            self.execute_shell(f"mkdir -p '{remote_dir}'")

        command = f"echo {escaped_content} | tee '{path}' > /dev/null"
        result = self.execute_shell(command)
        if result.exit_code != 0:
            raise OSError(f"Could not write to file {path}. Stderr: {result.stderr}")

    def list_dir(self, path: str) -> list[str]:
        """Lists the contents of a directory in the remote workspace."""
        result = self.execute_shell(f"ls -A '{path}'")
        if result.exit_code == 0:
            return result.stdout.splitlines()
        raise OSError(f"Could not list directory {path}. Stderr: {result.stderr}")
