import os

_WORKSPACE_ROOT: str | None = None


def set_workspace_root(root: str | None) -> None:
    global _WORKSPACE_ROOT
    if root:
        _WORKSPACE_ROOT = os.path.abspath(root)
    else:
        _WORKSPACE_ROOT = None


def get_workspace_root(default: str | None = None) -> str | None:
    if _WORKSPACE_ROOT:
        return _WORKSPACE_ROOT
    return default
