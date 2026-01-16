"""
Migration Strategy (Deprecated).

The legacy integration-based migration system was removed during the
issue-126 consolidation. This module remains as a compatibility shim
to avoid import errors in downstream tooling.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class MigrationPhase(Enum):
    """Migration phases for the gradual transition."""

    PREPARATION = "preparation"
    TOOL_MIGRATION = "tool_migration"
    GRAPH_MIGRATION = "graph_migration"
    COMMAND_MIGRATION = "command_migration"
    STAKEHOLDER_MIGRATION = "stakeholder_migration"
    CONTEXT_MIGRATION = "context_migration"
    MCP_MIGRATION = "mcp_migration"
    INFRASTRUCTURE_MIGRATION = "infrastructure_migration"
    VALIDATION = "validation"
    COMPLETION = "completion"


class MigrationStatus(Enum):
    """Status of migration phases."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class MigrationPhaseResult:
    """Result of a migration phase."""

    phase: MigrationPhase
    status: MigrationStatus
    start_time: float
    end_time: float | None = None
    duration: float | None = None
    success: bool = False
    error: str | None = None
    metrics: dict[str, Any] | None = None
    rollback_required: bool = False


@dataclass
class MigrationConfig:
    """Configuration for the migration strategy."""

    enable_gradual_migration: bool = True
    enable_backward_compatibility: bool = True
    enable_rollback: bool = True
    enable_validation: bool = True
    migration_timeout: float = 3600.0
    phase_timeout: float = 300.0
    validation_timeout: float = 60.0
    rollback_timeout: float = 180.0


class CCE_MigrationStrategy:
    """
    Compatibility shim for the deprecated migration strategy.

    The original integration modules were removed as part of issue-126,
    so migration execution now returns a warning.
    """

    def __init__(self, config: MigrationConfig | None = None) -> None:
        self.logger = logging.getLogger(f"{__name__}.CCE_MigrationStrategy")
        self.config = config or MigrationConfig()
        self.migration_phases = list(MigrationPhase)
        self.migration_results: list[MigrationPhaseResult] = []
        self.current_phase: MigrationPhase | None = None
        self.migration_start_time: float | None = None
        self.migration_end_time: float | None = None

        self.logger.warning("CCE_MigrationStrategy is deprecated; integration modules were removed in issue-126.")

    async def execute_gradual_migration(self) -> dict[str, Any]:
        """Return a warning payload indicating migration is no longer supported."""
        self.migration_start_time = time.time()
        self.migration_end_time = self.migration_start_time
        return {
            "success": False,
            "phases_completed": 0,
            "phases_failed": len(self.migration_phases),
            "total_duration": 0.0,
            "phase_results": [],
            "errors": ["Migration strategy deprecated after issue-126 consolidation"],
            "warnings": ["Legacy integration modules were removed; migration no longer runs"],
        }

    def get_migration_status(self) -> dict[str, Any]:
        """Return a minimal status payload."""
        return {
            "current_phase": self.current_phase.value if self.current_phase else None,
            "phases_completed": 0,
            "phases_failed": len(self.migration_phases),
            "total_phases": len(self.migration_phases),
            "migration_duration": 0.0,
            "backward_compatibility": {"enabled": False},
            "phase_results": [],
        }


_migration_strategy_instance: CCE_MigrationStrategy | None = None


def get_migration_strategy(config: MigrationConfig | None = None) -> CCE_MigrationStrategy:
    """Get the global migration strategy instance."""
    global _migration_strategy_instance
    if _migration_strategy_instance is None:
        _migration_strategy_instance = CCE_MigrationStrategy(config)
    return _migration_strategy_instance


async def execute_migration(config: MigrationConfig | None = None) -> dict[str, Any]:
    """Execute the migration strategy."""
    strategy = get_migration_strategy(config)
    return await strategy.execute_gradual_migration()


def get_migration_status() -> dict[str, Any]:
    """Get current migration status."""
    strategy = get_migration_strategy()
    return strategy.get_migration_status()
