"""
CCE configuration loader.

Loads cce_config.yaml and provides defaults with environment fallbacks.
CLI overrides can be applied per run without editing files.
"""

import importlib.resources as resources
import logging
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

_MISSING = object()


@dataclass
class LangsmithConfig:
    project: str = "cce-agent"
    prompt_hub_enabled: bool = False
    prompt_hub_namespace: str = "cce"
    prompt_hub_allowlist: list[str] = field(default_factory=list)
    prompt_hub_sync_mode: str = "pull"


@dataclass
class GitConfig:
    pr_template_dir: str = "docs/templates/pr_templates"
    default_template: str = "feature"
    default_labels: list[str] = field(default_factory=list)
    auto_assign_reviewers: list[str] = field(default_factory=list)


@dataclass
class ExecutionLimitsConfig:
    max_cycles: int = 50
    soft_limit: int = 20
    recursion_limit: int = 200


@dataclass
class FileDiscoveryConfig:
    summary_max_chars: int = 30000


@dataclass
class DefaultsConfig:
    base_branch: str = "auto"
    auto_create_pr: bool = True
    use_aider: bool = False
    prompt_cache: bool = True


@dataclass
class RunModeConfig:
    mode: str = "guided"
    interrupts_enabled: bool = True
    orientation_checkpoint: bool = True
    evaluation_checkpoint: bool = True
    critical_files_checkpoint: bool = False
    logging_level: str = "standard"
    allow_mode_switching: bool = True


@dataclass
class CCEConfig:
    langsmith: LangsmithConfig = field(default_factory=LangsmithConfig)
    git: GitConfig = field(default_factory=GitConfig)
    execution: ExecutionLimitsConfig = field(default_factory=ExecutionLimitsConfig)
    file_discovery: FileDiscoveryConfig = field(default_factory=FileDiscoveryConfig)
    defaults: DefaultsConfig = field(default_factory=DefaultsConfig)
    run_mode: RunModeConfig = field(default_factory=RunModeConfig)
    config_path: str | None = None


@dataclass
class ConfigOverrides:
    base_branch: str | None = None
    auto_create_pr: bool | None = None
    use_aider: bool | None = None
    prompt_cache: bool | None = None
    recursion_limit: int | None = None
    run_mode: str | None = None


_config: CCEConfig | None = None
_overrides = ConfigOverrides()


def _parse_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "1", "yes", "on"):
            return True
        if normalized in ("false", "0", "no", "off"):
            return False
    return default


def _parse_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        if not value.strip():
            return []
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(value).strip()] if str(value).strip() else []


def _parse_int(value: Any, default: int) -> int:
    if isinstance(value, bool):
        return default
    if value is None:
        return default
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _lookup(config_data: dict[str, Any], path: list[str]) -> Any:
    current: Any = config_data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return _MISSING
        current = current[key]
    return current


def _resolve_value(config_value: Any, env_key: str, default: Any, parser=None) -> Any:
    if config_value is not _MISSING and config_value is not None:
        return parser(config_value) if parser else config_value
    env_value = os.getenv(env_key)
    if env_value is not None:
        return parser(env_value) if parser else env_value
    return default


def _resolve_pr_template_dir(config_value: Any, workspace_root: str | None) -> str:
    raw_value = _resolve_value(config_value, "PR_TEMPLATE_DIR", "docs/templates/pr_templates")
    candidate = Path(str(raw_value))
    if candidate.is_absolute():
        return str(candidate)

    base_dir = Path(workspace_root).expanduser() if workspace_root else Path.cwd()
    workspace_candidate = base_dir / candidate
    if workspace_candidate.exists():
        return str(candidate)

    try:
        package_candidate = resources.files("src") / "templates" / "pr_templates"
        if package_candidate.is_dir():
            return os.fspath(package_candidate)
    except Exception as exc:
        logger.debug("Failed to resolve packaged PR templates: %s", exc)

    return str(candidate)


def _normalize_branch(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None
    normalized = str(value).strip()
    return normalized or None


def _detect_default_branch(workspace_root: str | None) -> str | None:
    if not workspace_root:
        return None
    try:
        result = subprocess.run(
            ["git", "-C", workspace_root, "rev-parse", "--abbrev-ref", "origin/HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        logger.debug("Failed to detect default branch: %s", exc)
        return None

    if result.returncode != 0:
        return None

    ref = result.stdout.strip()
    if not ref:
        return None
    if ref.startswith("origin/"):
        return ref.split("/", 1)[1] or None
    return ref


def _resolve_base_branch(value: Any, workspace_root: str | None) -> str:
    normalized = _normalize_branch(value)
    if not normalized or normalized.lower() == "auto":
        detected = _detect_default_branch(workspace_root)
        return detected or "main"
    return normalized


def _get_config_path(config_path: str | None = None, workspace_root: str | None = None) -> Path | None:
    if config_path:
        path = Path(config_path).expanduser()
        return path if path.exists() else None

    env_path = os.getenv("CCE_CONFIG_PATH")
    if env_path:
        path = Path(env_path).expanduser()
        return path if path.exists() else None

    base_dir = Path(workspace_root).expanduser() if workspace_root else Path.cwd()
    candidate = base_dir / "cce_config.yaml"
    return candidate if candidate.exists() else None


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            logger.warning("Config file %s did not parse to a dict; using defaults.", path)
            return {}
        return data
    except Exception as exc:
        logger.warning("Failed to load config file %s: %s", path, exc)
        return {}


def _apply_overrides(config: CCEConfig, overrides: ConfigOverrides) -> None:
    if overrides.base_branch is not None:
        config.defaults.base_branch = overrides.base_branch
    if overrides.auto_create_pr is not None:
        config.defaults.auto_create_pr = overrides.auto_create_pr
    if overrides.use_aider is not None:
        config.defaults.use_aider = overrides.use_aider
    if overrides.prompt_cache is not None:
        config.defaults.prompt_cache = overrides.prompt_cache
    if overrides.recursion_limit is not None:
        config.execution.recursion_limit = overrides.recursion_limit
    if overrides.run_mode is not None:
        config.run_mode.mode = overrides.run_mode


def load_config(config_path: str | None = None, workspace_root: str | None = None) -> CCEConfig:
    path = _get_config_path(config_path=config_path, workspace_root=workspace_root)
    config_data: dict[str, Any] = _load_yaml(path) if path else {}

    project_value = _lookup(config_data, ["langsmith", "project"])
    prompt_hub_enabled_value = _lookup(config_data, ["langsmith", "prompt_hub_enabled"])
    prompt_hub_namespace_value = _lookup(config_data, ["langsmith", "prompt_hub_namespace"])
    prompt_hub_allowlist_value = _lookup(config_data, ["langsmith", "prompt_hub_allowlist"])
    prompt_hub_sync_mode_value = _lookup(config_data, ["langsmith", "prompt_hub_sync_mode"])
    base_branch_value = _lookup(config_data, ["defaults", "base_branch"])
    auto_pr_value = _lookup(config_data, ["defaults", "auto_create_pr"])
    use_aider_value = _lookup(config_data, ["defaults", "use_aider"])
    prompt_cache_value = _lookup(config_data, ["defaults", "prompt_cache"])
    max_cycles_value = _lookup(config_data, ["execution", "max_cycles"])
    soft_limit_value = _lookup(config_data, ["execution", "soft_limit"])
    recursion_limit_value = _lookup(config_data, ["execution", "recursion_limit"])
    summary_max_chars_value = _lookup(config_data, ["file_discovery", "summary_max_chars"])

    pr_template_dir_value = _lookup(config_data, ["git", "pr_template_dir"])
    default_template_value = _lookup(config_data, ["git", "default_template"])
    default_labels_value = _lookup(config_data, ["git", "default_labels"])
    reviewers_value = _lookup(config_data, ["git", "auto_assign_reviewers"])

    # Run mode configuration
    run_mode_value = _lookup(config_data, ["run_mode", "mode"])
    interrupts_enabled_value = _lookup(config_data, ["run_mode", "interrupts_enabled"])
    orientation_checkpoint_value = _lookup(config_data, ["run_mode", "orientation_checkpoint"])
    evaluation_checkpoint_value = _lookup(config_data, ["run_mode", "evaluation_checkpoint"])
    critical_files_checkpoint_value = _lookup(config_data, ["run_mode", "critical_files_checkpoint"])
    logging_level_value = _lookup(config_data, ["run_mode", "logging_level"])
    allow_mode_switching_value = _lookup(config_data, ["run_mode", "allow_mode_switching"])

    config = CCEConfig(
        langsmith=LangsmithConfig(
            project=_resolve_value(project_value, "LANGSMITH_PROJECT", "cce-agent"),
            prompt_hub_enabled=_resolve_value(
                prompt_hub_enabled_value,
                "LANGSMITH_PROMPT_HUB_ENABLED",
                False,
                parser=lambda v: _parse_bool(v, False),
            ),
            prompt_hub_namespace=_resolve_value(
                prompt_hub_namespace_value,
                "LANGSMITH_PROMPT_HUB_NAMESPACE",
                "cce",
            ),
            prompt_hub_allowlist=_resolve_value(
                prompt_hub_allowlist_value,
                "LANGSMITH_PROMPT_HUB_ALLOWLIST",
                [],
                parser=_parse_list,
            ),
            prompt_hub_sync_mode=_resolve_value(
                prompt_hub_sync_mode_value,
                "LANGSMITH_PROMPT_HUB_SYNC_MODE",
                "pull",
            ),
        ),
        git=GitConfig(
            pr_template_dir=_resolve_pr_template_dir(pr_template_dir_value, workspace_root),
            default_template=_resolve_value(default_template_value, "PR_DEFAULT_TEMPLATE", "feature"),
            default_labels=_resolve_value(default_labels_value, "PR_DEFAULT_LABELS", [], parser=_parse_list),
            auto_assign_reviewers=_resolve_value(reviewers_value, "PR_AUTO_ASSIGN_REVIEWERS", [], parser=_parse_list),
        ),
        execution=ExecutionLimitsConfig(
            max_cycles=_resolve_value(
                max_cycles_value,
                "CCE_MAX_CYCLES",
                50,
                parser=lambda v: _parse_int(v, 50),
            ),
            soft_limit=_resolve_value(
                soft_limit_value,
                "CCE_SOFT_LIMIT",
                20,
                parser=lambda v: _parse_int(v, 20),
            ),
            recursion_limit=(
                _resolve_value(
                    recursion_limit_value,
                    "CCE_RECURSION_LIMIT",
                    200,
                    parser=lambda v: _parse_int(v, 200),
                )
            ),
        ),
        file_discovery=FileDiscoveryConfig(
            summary_max_chars=_parse_int(
                summary_max_chars_value if summary_max_chars_value is not _MISSING else 30000,
                30000,
            ),
        ),
        defaults=DefaultsConfig(
            base_branch=_resolve_base_branch(
                _resolve_value(
                    base_branch_value,
                    "PR_BASE_BRANCH",
                    "auto",
                    parser=_normalize_branch,
                ),
                workspace_root,
            ),
            auto_create_pr=_resolve_value(auto_pr_value, "AUTO_CREATE_PR", True, parser=lambda v: _parse_bool(v, True)),
            use_aider=_resolve_value(use_aider_value, "FEATURE_AIDER", False, parser=lambda v: _parse_bool(v, False)),
            prompt_cache=_resolve_value(
                prompt_cache_value,
                "FEATURE_PROMPT_CACHE",
                True,
                parser=lambda v: _parse_bool(v, True),
            ),
        ),
        run_mode=RunModeConfig(
            mode=_resolve_value(run_mode_value, "CCE_RUN_MODE", "guided"),
            interrupts_enabled=_resolve_value(
                interrupts_enabled_value,
                "CCE_INTERRUPTS_ENABLED",
                True,
                parser=lambda v: _parse_bool(v, True),
            ),
            orientation_checkpoint=_resolve_value(
                orientation_checkpoint_value,
                "CCE_ORIENTATION_CHECKPOINT",
                True,
                parser=lambda v: _parse_bool(v, True),
            ),
            evaluation_checkpoint=_resolve_value(
                evaluation_checkpoint_value,
                "CCE_EVALUATION_CHECKPOINT",
                True,
                parser=lambda v: _parse_bool(v, True),
            ),
            critical_files_checkpoint=_resolve_value(
                critical_files_checkpoint_value,
                "CCE_CRITICAL_FILES_CHECKPOINT",
                False,
                parser=lambda v: _parse_bool(v, False),
            ),
            logging_level=_resolve_value(logging_level_value, "CCE_LOGGING_LEVEL", "standard"),
            allow_mode_switching=_resolve_value(
                allow_mode_switching_value,
                "CCE_ALLOW_MODE_SWITCHING",
                True,
                parser=lambda v: _parse_bool(v, True),
            ),
        ),
        config_path=str(path) if path else None,
    )

    return config


def get_config(config_path: str | None = None, workspace_root: str | None = None) -> CCEConfig:
    global _config
    if _config is None:
        _config = load_config(config_path=config_path, workspace_root=workspace_root)
        _apply_overrides(_config, _overrides)
    return _config


def reset_config() -> None:
    """Reset the config singleton and all overrides to default state."""
    global _config, _overrides
    _config = None
    _overrides = ConfigOverrides()


def set_config_overrides(
    base_branch: str | None = None,
    auto_create_pr: bool | None = None,
    use_aider: bool | None = None,
    prompt_cache: bool | None = None,
    recursion_limit: int | None = None,
    run_mode: str | None = None,
) -> None:
    global _overrides, _config
    if base_branch is not None:
        _overrides.base_branch = base_branch
    if auto_create_pr is not None:
        _overrides.auto_create_pr = auto_create_pr
    if use_aider is not None:
        _overrides.use_aider = use_aider
    if prompt_cache is not None:
        _overrides.prompt_cache = prompt_cache
    if recursion_limit is not None:
        _overrides.recursion_limit = recursion_limit
    if run_mode is not None:
        _overrides.run_mode = run_mode
    _config = None
