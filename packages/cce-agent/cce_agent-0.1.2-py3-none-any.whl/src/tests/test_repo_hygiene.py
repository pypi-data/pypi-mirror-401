import os
import subprocess
from pathlib import Path

from src.config.artifact_root import get_artifact_root


def test_gitignore_includes_core_patterns() -> None:
    contents = Path(".gitignore").read_text(encoding="utf-8")
    required_patterns = [
        ".artifacts/",
        "__pycache__/",
        "*.pyc",
        ".env",
    ]
    missing = [pattern for pattern in required_patterns if pattern not in contents]
    assert not missing, f"Missing .gitignore patterns: {missing}"

    log_patterns = {"*.log", "**/logs/", "logs/"}
    assert any(pattern in contents for pattern in log_patterns), "Missing log exclusion pattern in .gitignore"


def _run_guardrail(changed_files: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["CHANGED_FILES"] = "\n".join(changed_files)
    return subprocess.run(
        ["bash", "scripts/pre-commit-check-artifacts.sh"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_guardrail_passes_clean_files() -> None:
    result = _run_guardrail(["src/agent.py", "docs/readme.md"])
    assert result.returncode == 0


def test_guardrail_blocks_forbidden_artifacts() -> None:
    result = _run_guardrail(["__pycache__/module.pyc", "runs/output.txt"])
    assert result.returncode == 1
    combined = (result.stdout or "") + (result.stderr or "")
    assert "FORBIDDEN ARTIFACT" in combined


def test_artifact_root_env_override(monkeypatch, tmp_path: Path) -> None:
    override = tmp_path / "custom_artifacts"
    monkeypatch.setenv("CCE_ARTIFACT_ROOT", str(override))

    root = get_artifact_root()
    assert root == override.resolve()
    assert root.exists()


def test_artifact_root_prefers_git_repo(monkeypatch, tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".git").mkdir()

    monkeypatch.delenv("CCE_ARTIFACT_ROOT", raising=False)
    monkeypatch.chdir(repo)

    root = get_artifact_root()
    assert root == (repo / ".artifacts").resolve()


def test_artifact_root_falls_back_to_home(monkeypatch, tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    home = tmp_path / "home"
    home.mkdir()

    monkeypatch.delenv("CCE_ARTIFACT_ROOT", raising=False)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.chdir(workspace)

    root = get_artifact_root()
    assert root == (home / ".cce-agent" / "artifacts").resolve()
