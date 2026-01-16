"""
Artifact Root Configuration

Centralizes all artifact path management to prevent repo pollution.
All generated outputs (logs, DBs, runs, etc.) should use this module.

This module ensures that all runtime artifacts are written to a single,
configurable location that is git-ignored and outside the tracked source tree.
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def get_artifact_root() -> Path:
    """
    Get the artifact root directory.

    Priority:
    1. CCE_ARTIFACT_ROOT environment variable (if set)
    2. .artifacts/ in repo root (if in a git repo)
    3. ~/.cce-agent/artifacts/ (user home directory)
    4. System temp directory as fallback

    Returns:
        Path to artifact root directory (created if needed)
    """
    # Check environment variable first
    env_root = os.getenv("CCE_ARTIFACT_ROOT")
    if env_root:
        root = Path(env_root).expanduser().resolve()
        root.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Using artifact root from CCE_ARTIFACT_ROOT: {root}")
        return root

    # Try to detect repo root by looking for .git directory
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists():
            # We're in a git repo, use .artifacts/ at repo root
            root = parent / ".artifacts"
            root.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Using artifact root at repo root: {root}")
            return root

    # Fallback to user home directory
    home = Path.home()
    root = home / ".cce-agent" / "artifacts"
    root.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Using artifact root in user home: {root}")
    return root


def get_runs_directory() -> Path:
    """
    Get directory for run outputs.

    Returns:
        Path to runs directory (created if needed)
    """
    runs_dir = get_artifact_root() / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    return runs_dir


def get_logs_directory() -> Path:
    """
    Get directory for log files.

    Returns:
        Path to logs directory (created if needed)
    """
    logs_dir = get_artifact_root() / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def get_checkpoints_directory() -> Path:
    """
    Get directory for checkpoint databases.

    Returns:
        Path to checkpoints directory (created if needed)
    """
    checkpoints_dir = get_artifact_root() / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    return checkpoints_dir


def get_command_outputs_directory() -> Path:
    """
    Get directory for command outputs (plans, research, evaluations, test reports).

    This replaces the previous docs/context_engineering/ subdirectories.

    Returns:
        Path to command outputs directory (created if needed)
    """
    outputs_dir = get_artifact_root() / "command_outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    return outputs_dir


def get_aider_artifacts_directory() -> Path:
    """
    Get directory for AIDER-specific artifacts (repo maps, patches, etc.).

    Returns:
        Path to AIDER artifacts directory (created if needed)
    """
    aider_dir = get_artifact_root() / "aider"
    aider_dir.mkdir(parents=True, exist_ok=True)
    return aider_dir


def get_research_directory() -> Path:
    """
    Get directory for research outputs (replaces docs/context_engineering/research/).

    Returns:
        Path to research directory (created if needed)
    """
    research_dir = get_command_outputs_directory() / "research"
    research_dir.mkdir(parents=True, exist_ok=True)
    return research_dir


def get_plans_directory() -> Path:
    """
    Get directory for plan outputs (replaces docs/context_engineering/plans/).

    Returns:
        Path to plans directory (created if needed)
    """
    plans_dir = get_command_outputs_directory() / "plans"
    plans_dir.mkdir(parents=True, exist_ok=True)
    return plans_dir


def get_evaluations_directory() -> Path:
    """
    Get directory for evaluation outputs (replaces docs/context_engineering/evaluations/).

    Returns:
        Path to evaluations directory (created if needed)
    """
    evaluations_dir = get_command_outputs_directory() / "evaluations"
    evaluations_dir.mkdir(parents=True, exist_ok=True)
    return evaluations_dir


def get_test_reports_directory() -> Path:
    """
    Get directory for test report outputs (replaces docs/context_engineering/test_reports/).

    Returns:
        Path to test reports directory (created if needed)
    """
    test_reports_dir = get_command_outputs_directory() / "test_reports"
    test_reports_dir.mkdir(parents=True, exist_ok=True)
    return test_reports_dir
