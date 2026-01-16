"""
CCE Launchers - Remote execution environments for CCE Agent.

This package provides launchers for executing CCE workflows in remote
environments such as GitHub Codespaces, SSH hosts, etc.
"""

from .codespaces import CodespacesLauncher

__all__ = ["CodespacesLauncher"]
