from .shell_runner import ShellRunner


class CodeAnalyzer:
    """A service for analyzing the codebase, such as listing files."""

    def __init__(self, shell: ShellRunner):
        self.shell = shell

    def list_files(self, path: str = ".") -> str:
        """Lists files in the specified directory."""
        # A more sophisticated implementation will use ignore patterns, etc.
        result = self.shell.execute(f"find {path} -type f | head -n 100")
        if result.exit_code == 0:
            return result.stdout or f"No files found in {path}."
        return f"Error listing files:\n{result.stderr}"
