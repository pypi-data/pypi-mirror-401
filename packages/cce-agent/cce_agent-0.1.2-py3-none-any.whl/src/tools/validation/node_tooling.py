"""Utility helpers for resolving Node.js tooling in local projects."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

_LOCKFILE_PRIORITY = [
    ("pnpm-lock.yaml", "pnpm"),
    ("yarn.lock", "yarn"),
    ("package-lock.json", "npm"),
    ("npm-shrinkwrap.json", "npm"),
]


def detect_package_manager(workspace_root: Path) -> str | None:
    """Detect the preferred package manager using lock files or package.json."""
    for lockfile, manager in _LOCKFILE_PRIORITY:
        if (workspace_root / lockfile).exists():
            return manager

    package_json = workspace_root / "package.json"
    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

        package_manager = data.get("packageManager", "")
        if isinstance(package_manager, str):
            if package_manager.startswith("pnpm@"):  # e.g. pnpm@8.6.0
                return "pnpm"
            if package_manager.startswith("yarn@"):  # e.g. yarn@3.5.1
                return "yarn"
            if package_manager.startswith("npm@"):  # e.g. npm@10.2.0
                return "npm"

    return None


def load_package_json(workspace_root: Path) -> dict[str, Any] | None:
    """Load package.json as a dictionary when available."""
    package_json = workspace_root / "package.json"
    if not package_json.exists():
        return None

    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None

    return data if isinstance(data, dict) else None


def extract_package_scripts(package_json: dict[str, Any]) -> dict[str, str]:
    """Extract string-valued scripts from package.json."""
    scripts = package_json.get("scripts", {})
    if not isinstance(scripts, dict):
        return {}

    return {name: cmd for name, cmd in scripts.items() if isinstance(cmd, str)}


def package_json_uses_tool(workspace_root: Path, tool: str, config_keys: list[str] | None = None) -> bool:
    """Check package.json for tool config or script usage."""
    data = load_package_json(workspace_root)
    if not data:
        return False

    if config_keys:
        for key in config_keys:
            if key in data:
                return True

    scripts = extract_package_scripts(data)
    return any(command_mentions_tool(command, tool) for command in scripts.values())


def command_mentions_tool(command: str, tool: str) -> bool:
    """Detect tool usage in a script command."""
    pattern = rf"(?:^|\\s|[/\\\\]){re.escape(tool)}(?:$|\\s)"
    return re.search(pattern, command) is not None


def resolve_node_command(tool: str, workspace_root: Path) -> list[str] | None:
    """Resolve a Node.js tool command from PATH, local bin, or package manager exec."""
    if shutil.which(tool):
        return [tool]

    local_bin = workspace_root / "node_modules" / ".bin" / tool
    if local_bin.exists():
        return [str(local_bin)]

    for suffix in (".cmd", ".ps1"):
        candidate = local_bin.with_suffix(suffix)
        if candidate.exists():
            return [str(candidate)]

    package_manager = detect_package_manager(workspace_root)
    if package_manager and shutil.which(package_manager):
        return _build_exec_command(package_manager, tool)

    return None


def _build_exec_command(package_manager: str, tool: str) -> list[str]:
    if package_manager == "npm":
        return ["npm", "exec", "--", tool]
    if package_manager == "pnpm":
        return ["pnpm", "exec", tool]
    if package_manager == "yarn":
        return ["yarn", "run", tool]
    return [package_manager, "exec", tool]
