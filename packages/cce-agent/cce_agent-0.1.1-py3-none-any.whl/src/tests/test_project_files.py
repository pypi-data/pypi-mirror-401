import re
import tomllib
from pathlib import Path


def _load_pyproject() -> dict:
    return tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))


def test_pyproject_has_project_metadata() -> None:
    data = _load_pyproject()
    project = data["project"]
    assert project["name"] == "cce-agent"

    dependencies = project.get("dependencies", [])
    assert any(dep.startswith("langgraph") for dep in dependencies)
    assert any(dep.startswith("langchain-core") for dep in dependencies)


def test_pyproject_has_dev_dependencies() -> None:
    data = _load_pyproject()
    dev_deps = data["project"]["optional-dependencies"]["dev"]
    assert any("pytest" in dep for dep in dev_deps)
    assert any(dep.startswith("ruff") for dep in dev_deps)


def test_ruff_config_present() -> None:
    data = _load_pyproject()
    ruff = data["tool"]["ruff"]
    assert ruff["line-length"] == 120
    assert "target-version" in ruff


def test_makefile_has_standard_targets() -> None:
    makefile = Path("Makefile").read_text(encoding="utf-8")
    targets = {
        line.split(":")[0]
        for line in makefile.splitlines()
        if re.match(r"^[A-Za-z0-9_.-]+:", line)
    }

    required = {
        "install-dev",
        "format",
        "lint",
        "typecheck",
        "test",
        "test-unit",
        "test-integration",
    }
    missing = required - targets
    assert not missing, f"Missing Makefile targets: {sorted(missing)}"
