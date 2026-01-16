from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ShellResult:
    """
    Represents the result of a shell command execution.
    """

    exit_code: int
    stdout: str
    stderr: str


class BaseEnvironment(ABC):
    """
    Defines the abstract interface for an execution environment.

    This class provides a contract for interacting with a workspace,
    whether it is local or remote. All environment connectors must
    implement these methods.
    """

    @abstractmethod
    def execute_shell(self, command: str) -> ShellResult:
        """
        Executes a shell command in the environment.
        """
        pass

    @abstractmethod
    def read_file(self, path: str) -> str:
        """
        Writes content to a file in the environment using the specified format.
        """
        pass

    @abstractmethod
    def apply_edit(self, path: str, content: str, edit_format: str = "editor-whole") -> None:
        """
        Applies an edit to a file in the environment using the specified format.
        """
        pass

    @abstractmethod
    def list_dir(self, path: str) -> list[str]:
        """
        Lists the contents of a directory in the environment.
        """
        pass
