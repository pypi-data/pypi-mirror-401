import os
import subprocess

from .base import BaseEnvironment, ShellResult


class LocalEnvironment(BaseEnvironment):
    """
    An environment connector that executes commands on the local filesystem.

    This class is the default implementation for running the agent in a local
    development or testing context. It uses the `subprocess` module to
    execute shell commands and standard Python I/O for file operations.
    """

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = os.path.abspath(workspace_root)
        if not os.path.exists(self.workspace_root):
            os.makedirs(self.workspace_root)

    def execute_shell(self, command: str) -> ShellResult:
        """
        Executes a shell command in the local workspace directory.
        """
        process = subprocess.run(
            command,
            shell=True,
            cwd=self.workspace_root,
            capture_output=True,
            text=True,
        )
        return ShellResult(
            exit_code=process.returncode,
            stdout=process.stdout,
            stderr=process.stderr,
        )

    def read_file(self, path: str) -> str:
        """
        Reads a file from the local workspace.
        """
        full_path = os.path.join(self.workspace_root, path)
        with open(full_path) as f:
            return f.read()

    def apply_edit(self, path: str, content: str, edit_format: str = "editor-whole") -> None:
        """
        Applies an edit to a file in the local workspace using the specified format.
        """
        full_path = os.path.join(self.workspace_root, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if edit_format == "editor-diff":
            # Apply diff-based edit logic here
            pass
        else:
            with open(full_path, "w") as f:
                f.write(content)

    def list_dir(self, path: str) -> list[str]:
        """
        Lists the contents of a directory in the local workspace.
        """
        full_path = os.path.join(self.workspace_root, path)
        return os.listdir(full_path)
