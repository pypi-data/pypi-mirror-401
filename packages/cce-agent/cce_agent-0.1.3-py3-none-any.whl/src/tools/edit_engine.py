from ..environments.base import BaseEnvironment
from .aider.wrapper import AiderctlWrapper
from .code_analyzer import CodeAnalyzer
from .git_ops import GitOps
from .shell_runner import ShellRunner


class EditEngine:
    """
    The EditEngine is responsible for orchestrating the application of edits,
    including validation and rollback.
    """

    def __init__(
        self,
        env: BaseEnvironment,
        shell_runner: ShellRunner,
        code_analyzer: CodeAnalyzer,
        git_ops: GitOps,
        aider_wrapper: AiderctlWrapper,
    ):
        self.env = env
        self.shell_runner = shell_runner
        self.code_analyzer = code_analyzer
        self.git_ops = git_ops
        self.aider_wrapper = aider_wrapper
