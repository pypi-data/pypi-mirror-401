from __future__ import annotations

from src.launchers.codespaces import CodespacesLauncher


def _build_base_command(launcher: CodespacesLauncher, auto_install_cli: bool, cli_version: str | None) -> str:
    return launcher._build_remote_command(
        issue_url="https://github.com/owner/repo/issues/1",
        base_branch="main",
        run_mode="guided",
        execution_mode="native",
        artifact_path="/tmp/cce-artifacts",
        recursion_limit=None,
        use_deep_agents=False,
        deep_agents_read_only=False,
        deep_agents_timeout=None,
        deep_agents_max_cycles=None,
        deep_agents_remaining_steps=None,
        enable_git_workflow=False,
        auto_pr=None,
        use_aider=None,
        prompt_cache=None,
        auto_install_cli=auto_install_cli,
        cli_version=cli_version,
    )


def test_codespaces_package_mode_command() -> None:
    launcher = CodespacesLauncher(
        codespace_name="dummy",
        workspace_root="/workspaces/repo",
        cli_root=None,
    )
    command = _build_base_command(launcher, auto_install_cli=True, cli_version="1.2.3")
    assert "cce_agent.cli" in command
    assert "AUTO_INSTALL_CLI=1" in command
    assert "cce-agent==${CCE_CLI_VERSION}" in command


def test_codespaces_repo_mode_command() -> None:
    launcher = CodespacesLauncher(
        codespace_name="dummy",
        workspace_root="/workspaces/repo",
        cli_root="/workspaces/cce-agent",
    )
    command = _build_base_command(launcher, auto_install_cli=False, cli_version=None)
    assert "src.cli" in command
    assert "requirements.txt" in command
