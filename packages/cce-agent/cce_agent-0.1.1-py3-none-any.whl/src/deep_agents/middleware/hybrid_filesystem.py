"""
Hybrid filesystem middleware for CCE deep agents.

Loads workspace files into the virtual filesystem before agent execution,
tracks changes in state, and syncs updates back to disk after execution.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from langchain.agents.middleware.types import AgentMiddleware

from ..hybrid_filesystem_tools import (
    HYBRID_FILESYSTEM_TOOLS,
    initialize_virtual_filesystem_from_workspace,
    sync_virtual_to_real_filesystem,
)
from ..state import CCEDeepAgentState

logger = logging.getLogger(__name__)


class HybridFilesystemMiddleware(AgentMiddleware):
    """Middleware that initializes and persists the hybrid filesystem state."""

    state_schema = CCEDeepAgentState

    def __init__(
        self,
        *,
        workspace_root: str = ".",
        include_patterns: list[str] | None = None,
        load_mode: str = "summary",
        enable_logging: bool = True,
    ) -> None:
        super().__init__()
        self.workspace_root = os.path.abspath(workspace_root)
        self.include_patterns = include_patterns
        self.load_mode = load_mode
        self.enable_logging = enable_logging
        self.tools = HYBRID_FILESYSTEM_TOOLS

    def _ensure_changed_files(self, state: dict[str, Any], updates: dict[str, Any]) -> None:
        changed_files = state.get("changed_files")
        if not isinstance(changed_files, list):
            updates["changed_files"] = []

    def _needs_files_init(self, files: Any) -> bool:
        if not isinstance(files, dict):
            return True
        if not files:
            return True
        return len(files) == 1 and "__full_content_cache__" in files

    def _initialize_files(self) -> dict[str, str]:
        return initialize_virtual_filesystem_from_workspace(
            workspace_root=self.workspace_root,
            include_patterns=self.include_patterns,
            load_mode=self.load_mode,
        )

    def before_agent(self, state: dict[str, Any], runtime) -> dict[str, Any] | None:  # type: ignore[override]
        updates: dict[str, Any] = {}
        files = state.get("files")
        if self._needs_files_init(files):
            virtual_files = self._initialize_files()
            updates["files"] = virtual_files
            updates["changed_files"] = []
            if self.enable_logging:
                logger.info(
                    "Hybrid filesystem initialized with %d entries",
                    len(virtual_files) if isinstance(virtual_files, dict) else 0,
                )
        else:
            self._ensure_changed_files(state, updates)

        return updates or None

    async def abefore_agent(self, state: dict[str, Any], runtime) -> dict[str, Any] | None:  # type: ignore[override]
        return self.before_agent(state, runtime)

    def after_agent(self, state: dict[str, Any], runtime) -> dict[str, Any] | None:  # type: ignore[override]
        files = state.get("files")
        changed_files = state.get("changed_files")
        if not isinstance(files, dict) or not isinstance(changed_files, list):
            return None

        changed_set = {path for path in changed_files if path and path != "__full_content_cache__"}
        if not changed_set:
            return None

        files_to_sync = {path: content for path, content in files.items() if path != "__full_content_cache__"}
        if not files_to_sync:
            return {"changed_files": []}

        sync_virtual_to_real_filesystem(files_to_sync, self.workspace_root, changed_set)
        if self.enable_logging:
            logger.info("Hybrid filesystem synced %d file(s) to disk", len(changed_set))
        return {"changed_files": []}

    async def aafter_agent(self, state: dict[str, Any], runtime) -> dict[str, Any] | None:  # type: ignore[override]
        return self.after_agent(state, runtime)
