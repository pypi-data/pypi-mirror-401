"""Dependency installation helpers for validation and testing."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .node_tooling import detect_package_manager, load_package_json


def _auto_install_enabled() -> bool:
    value = os.getenv("CCE_AUTO_INSTALL_DEPS", "1").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _force_install_enabled() -> bool:
    value = os.getenv("CCE_FORCE_INSTALL_DEPS", "0").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _run_command(
    command: list[str],
    workspace_root: Path,
    logger: logging.Logger,
    timeout: int = 1200,
) -> dict[str, Any]:
    env = os.environ.copy()
    env["COREPACK_ENABLE_DOWNLOAD_PROMPT"] = "0"
    env.setdefault("CI", "1")

    try:
        result = subprocess.run(
            command,
            cwd=workspace_root,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "command": command,
            "error": f"Command timed out after {timeout} seconds",
        }
    except Exception as exc:  # pragma: no cover - safety net
        return {"success": False, "command": command, "error": str(exc)}

    if result.returncode != 0:
        logger.warning("Dependency install failed: %s", result.stderr.strip() or result.stdout.strip())
        return {
            "success": False,
            "command": command,
            "exit_code": result.returncode,
            "stderr": result.stderr,
            "stdout": result.stdout,
        }

    return {"success": True, "command": command, "stdout": result.stdout}


def _node_install_command(workspace_root: Path) -> list[str] | None:
    package_json = workspace_root / "package.json"
    if not package_json.exists():
        return None

    manager = detect_package_manager(workspace_root) or "npm"
    if not shutil.which(manager):
        return None

    if manager == "npm":
        if (workspace_root / "package-lock.json").exists() or (workspace_root / "npm-shrinkwrap.json").exists():
            return ["npm", "ci", "--no-audit", "--no-fund"]
        return ["npm", "install", "--no-audit", "--no-fund", "--no-package-lock"]

    if manager == "pnpm":
        return ["pnpm", "install"]

    if manager == "yarn":
        package_info = load_package_json(workspace_root) or {}
        manager_spec = str(package_info.get("packageManager", ""))
        if manager_spec.startswith("yarn@"):
            version = manager_spec.split("@", 1)[1]
            major = int(version.split(".", 1)[0]) if version.split(".", 1)[0].isdigit() else 1
            if major >= 2:
                return ["yarn", "install", "--immutable"]
        return ["yarn", "install", "--frozen-lockfile"]

    return [manager, "install"]


def _python_install_command(workspace_root: Path) -> list[str] | None:
    requirements = workspace_root / "requirements.txt"
    dev_requirements = workspace_root / "requirements-dev.txt"
    pyproject = workspace_root / "pyproject.toml"
    poetry_lock = workspace_root / "poetry.lock"
    pipfile = workspace_root / "Pipfile"
    pipfile_lock = workspace_root / "Pipfile.lock"

    if poetry_lock.exists() and shutil.which("poetry"):
        return ["poetry", "install", "--no-interaction", "--no-ansi"]

    if pipfile.exists() or pipfile_lock.exists():
        if shutil.which("pipenv"):
            return ["pipenv", "install", "--dev"]

    if dev_requirements.exists():
        return ["python", "-m", "pip", "install", "-r", str(dev_requirements)]
    if requirements.exists():
        return ["python", "-m", "pip", "install", "-r", str(requirements)]

    if pyproject.exists():
        return ["python", "-m", "pip", "install", "."]

    return None


def _go_install_command(workspace_root: Path) -> list[str] | None:
    if (workspace_root / "go.mod").exists() and shutil.which("go"):
        return ["go", "mod", "download"]
    return None


def _rust_install_command(workspace_root: Path) -> list[str] | None:
    if (workspace_root / "Cargo.toml").exists() and shutil.which("cargo"):
        return ["cargo", "fetch"]
    return None


class DependencyInstaller:
    """Installs language-specific dependencies when missing."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.logger = logging.getLogger(__name__)
        self._attempted: set[str] = set()

    def ensure_for_languages(self, languages: list[str]) -> bool:
        if not _auto_install_enabled():
            return False

        attempted_any = False
        for language in languages:
            if language in self._attempted:
                continue
            if language in {"javascript", "typescript", "solidity"}:
                attempted_any |= self._ensure_node()
            elif language == "python":
                attempted_any |= self._ensure_python()
            elif language == "go":
                attempted_any |= self._ensure_go()
            elif language == "rust":
                attempted_any |= self._ensure_rust()
            self._attempted.add(language)

        return attempted_any

    def _ensure_node(self) -> bool:
        package_json = self.workspace_root / "package.json"
        if not package_json.exists():
            return False

        node_modules = self.workspace_root / "node_modules"
        if node_modules.exists() and not _force_install_enabled():
            return False

        command = _node_install_command(self.workspace_root)
        if not command:
            self.logger.warning("No Node.js package manager detected; skipping dependency install.")
            return False

        self.logger.info("Installing Node.js dependencies with: %s", " ".join(command))
        result = _run_command(command, self.workspace_root, self.logger)
        return bool(result.get("success"))

    def _ensure_python(self) -> bool:
        command = _python_install_command(self.workspace_root)
        if not command:
            return False

        if not shutil.which(command[0]):
            self.logger.warning("Python package manager '%s' not available; skipping dependency install.", command[0])
            return False

        self.logger.info("Installing Python dependencies with: %s", " ".join(command))
        result = _run_command(command, self.workspace_root, self.logger)
        return bool(result.get("success"))

    def _ensure_go(self) -> bool:
        command = _go_install_command(self.workspace_root)
        if not command:
            return False

        self.logger.info("Fetching Go modules with: %s", " ".join(command))
        result = _run_command(command, self.workspace_root, self.logger)
        return bool(result.get("success"))

    def _ensure_rust(self) -> bool:
        command = _rust_install_command(self.workspace_root)
        if not command:
            return False

        self.logger.info("Fetching Rust crates with: %s", " ".join(command))
        result = _run_command(command, self.workspace_root, self.logger)
        return bool(result.get("success"))
