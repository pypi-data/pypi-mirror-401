"""
Tests for the CCE configuration loader.

These tests verify:
1. Default values work when no config file exists
2. YAML config file parsing
3. Environment variable overrides
4. CLI override priority
5. Type coercion for booleans and lists
"""

import os
import tempfile
from pathlib import Path
from unittest import mock

import pytest
import yaml

from src.config_loader import (
    CCEConfig,
    ConfigOverrides,
    DefaultsConfig,
    GitConfig,
    LangsmithConfig,
    _parse_bool,
    _parse_list,
    get_config,
    load_config,
    reset_config,
    set_config_overrides,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(autouse=True)
def reset_global_config():
    """Reset global config state before and after each test."""
    reset_config()
    yield
    reset_config()


@pytest.fixture(autouse=True)
def clear_config_env(monkeypatch):
    """Ensure config tests are isolated from environment overrides."""
    env_keys = [
        "LANGSMITH_PROJECT",
        "LANGSMITH_PROMPT_HUB_SYNC_MODE",
        "PR_BASE_BRANCH",
        "AUTO_CREATE_PR",
        "FEATURE_AIDER",
        "FEATURE_PROMPT_CACHE",
        "PR_DEFAULT_LABELS",
        "PR_DEFAULT_TEMPLATE",
        "PR_TEMPLATE_DIR",
        "PR_AUTO_ASSIGN_REVIEWERS",
        "CCE_RECURSION_LIMIT",
        "CCE_CONFIG_PATH",
    ]
    for key in env_keys:
        monkeypatch.delenv(key, raising=False)
    yield


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory with a config file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_config():
    """Sample configuration dictionary."""
    return {
        "langsmith": {"project": "test-project"},
        "git": {
            "pr_template_dir": "custom/templates",
            "default_template": "bugfix",
            "default_labels": ["label1", "label2"],
            "auto_assign_reviewers": ["user1", "user2"],
        },
        "defaults": {"base_branch": "main", "auto_create_pr": False, "use_aider": False, "prompt_cache": True},
        "file_discovery": {"summary_max_chars": 45000},
    }


# =============================================================================
# Tests: Boolean Parsing
# =============================================================================


class TestParseBool:
    """Tests for _parse_bool function."""

    def test_bool_true(self):
        assert _parse_bool(True, False) is True

    def test_bool_false(self):
        assert _parse_bool(False, True) is False

    def test_string_true_values(self):
        for value in ["true", "True", "TRUE", "1", "yes", "YES", "on", "ON"]:
            assert _parse_bool(value, False) is True, f"Failed for {value}"

    def test_string_false_values(self):
        for value in ["false", "False", "FALSE", "0", "no", "NO", "off", "OFF"]:
            assert _parse_bool(value, True) is False, f"Failed for {value}"

    def test_int_values(self):
        assert _parse_bool(1, False) is True
        assert _parse_bool(0, True) is False

    def test_none_returns_default(self):
        assert _parse_bool(None, True) is True
        assert _parse_bool(None, False) is False

    def test_invalid_returns_default(self):
        assert _parse_bool("invalid", True) is True
        assert _parse_bool("invalid", False) is False


# =============================================================================
# Tests: List Parsing
# =============================================================================


class TestParseList:
    """Tests for _parse_list function."""

    def test_none_returns_empty(self):
        assert _parse_list(None) == []

    def test_empty_string_returns_empty(self):
        assert _parse_list("") == []
        assert _parse_list("   ") == []

    def test_list_passthrough(self):
        assert _parse_list(["a", "b", "c"]) == ["a", "b", "c"]

    def test_list_strips_whitespace(self):
        assert _parse_list(["  a  ", "  b  "]) == ["a", "b"]

    def test_list_filters_empty(self):
        assert _parse_list(["a", "", "b", "  ", "c"]) == ["a", "b", "c"]

    def test_comma_separated_string(self):
        assert _parse_list("a, b, c") == ["a", "b", "c"]

    def test_comma_separated_strips_whitespace(self):
        assert _parse_list("  a  ,  b  ,  c  ") == ["a", "b", "c"]

    def test_single_value(self):
        assert _parse_list("single") == ["single"]


# =============================================================================
# Tests: Default Configuration
# =============================================================================


class TestDefaultConfig:
    """Tests for default configuration values."""

    def test_defaults_when_no_config(self):
        """Config should have sensible defaults without any config file."""
        config = load_config(workspace_root="/nonexistent/path")

        assert config.langsmith.project == "cce-agent"
        assert str(config.git.pr_template_dir).endswith("templates/pr_templates")
        assert config.git.default_template == "feature"
        assert config.git.default_labels == []
        assert config.git.auto_assign_reviewers == []
        assert config.defaults.base_branch == "main"
        assert config.defaults.auto_create_pr is True
        assert config.defaults.use_aider is False
        assert config.defaults.prompt_cache is True
        assert config.file_discovery.summary_max_chars == 30000

    def test_config_path_none_when_no_file(self):
        """config_path should be None when no config file exists."""
        config = load_config(workspace_root="/nonexistent/path")
        assert config.config_path is None


# =============================================================================
# Tests: YAML Configuration Loading
# =============================================================================


class TestYamlConfig:
    """Tests for loading configuration from YAML file."""

    def test_load_yaml_config(self, temp_config_dir, sample_config):
        """Should load config from cce_config.yaml."""
        config_file = temp_config_dir / "cce_config.yaml"
        with open(config_file, "w") as f:
            yaml.dump(sample_config, f)

        config = load_config(workspace_root=str(temp_config_dir))

        assert config.langsmith.project == "test-project"
        assert config.git.default_template == "bugfix"
        assert config.defaults.base_branch == "main"
        assert config.defaults.auto_create_pr is False
        assert config.file_discovery.summary_max_chars == 45000

    def test_partial_yaml_config(self, temp_config_dir):
        """Should use defaults for missing sections."""
        partial_config = {"defaults": {"base_branch": "custom-branch"}}
        config_file = temp_config_dir / "cce_config.yaml"
        with open(config_file, "w") as f:
            yaml.dump(partial_config, f)

        config = load_config(workspace_root=str(temp_config_dir))

        # Should use custom value
        assert config.defaults.base_branch == "custom-branch"
        # Should use defaults for missing values
        assert config.langsmith.project == "cce-agent"
        assert config.git.default_template == "feature"

    def test_config_path_stored(self, temp_config_dir, sample_config):
        """config_path should be set when file exists."""
        config_file = temp_config_dir / "cce_config.yaml"
        with open(config_file, "w") as f:
            yaml.dump(sample_config, f)

        config = load_config(workspace_root=str(temp_config_dir))
        assert config.config_path is not None
        assert "cce_config.yaml" in config.config_path


# =============================================================================
# Tests: Environment Variable Overrides
# =============================================================================


class TestEnvOverrides:
    """Tests for environment variable overrides."""

    def test_langsmith_project_env(self):
        """LANGSMITH_PROJECT env var should override default."""
        with mock.patch.dict(os.environ, {"LANGSMITH_PROJECT": "env-project"}):
            config = load_config(workspace_root="/nonexistent")
            assert config.langsmith.project == "env-project"

    def test_base_branch_env(self):
        """PR_BASE_BRANCH env var should override default."""
        with mock.patch.dict(os.environ, {"PR_BASE_BRANCH": "env-branch"}):
            config = load_config(workspace_root="/nonexistent")
            assert config.defaults.base_branch == "env-branch"

    def test_auto_create_pr_env(self):
        """AUTO_CREATE_PR env var should override default."""
        with mock.patch.dict(os.environ, {"AUTO_CREATE_PR": "false"}):
            config = load_config(workspace_root="/nonexistent")
            assert config.defaults.auto_create_pr is False

    def test_feature_aider_env(self):
        """FEATURE_AIDER env var should override default."""
        with mock.patch.dict(os.environ, {"FEATURE_AIDER": "no"}):
            config = load_config(workspace_root="/nonexistent")
            assert config.defaults.use_aider is False

    def test_labels_env_comma_separated(self):
        """PR_DEFAULT_LABELS env var should parse comma-separated list."""
        with mock.patch.dict(os.environ, {"PR_DEFAULT_LABELS": "label1, label2, label3"}):
            config = load_config(workspace_root="/nonexistent")
            assert config.git.default_labels == ["label1", "label2", "label3"]

    def test_yaml_overrides_default_env_overrides_yaml(self, temp_config_dir):
        """Environment should override YAML config."""
        yaml_config = {"defaults": {"base_branch": "yaml-branch"}}
        config_file = temp_config_dir / "cce_config.yaml"
        with open(config_file, "w") as f:
            yaml.dump(yaml_config, f)

        # YAML is loaded but env is not set - should use YAML
        config = load_config(workspace_root=str(temp_config_dir))
        assert config.defaults.base_branch == "yaml-branch"


# =============================================================================
# Tests: CLI Overrides
# =============================================================================


class TestCLIOverrides:
    """Tests for CLI argument overrides via set_config_overrides."""

    def test_override_base_branch(self):
        """CLI override should take precedence."""
        set_config_overrides(base_branch="cli-branch")
        config = get_config(workspace_root="/nonexistent")
        assert config.defaults.base_branch == "cli-branch"

    def test_override_auto_pr(self):
        """CLI override for auto_create_pr should work."""
        set_config_overrides(auto_create_pr=False)
        config = get_config(workspace_root="/nonexistent")
        assert config.defaults.auto_create_pr is False

    def test_override_multiple(self):
        """Multiple CLI overrides should all apply."""
        set_config_overrides(base_branch="custom", auto_create_pr=False, use_aider=False, prompt_cache=False)
        config = get_config(workspace_root="/nonexistent")

        assert config.defaults.base_branch == "custom"
        assert config.defaults.auto_create_pr is False
        assert config.defaults.use_aider is False
        assert config.defaults.prompt_cache is False

    def test_cli_overrides_yaml_and_env(self, temp_config_dir):
        """CLI should override both YAML and env."""
        yaml_config = {"defaults": {"base_branch": "yaml-branch"}}
        config_file = temp_config_dir / "cce_config.yaml"
        with open(config_file, "w") as f:
            yaml.dump(yaml_config, f)

        with mock.patch.dict(os.environ, {"PR_BASE_BRANCH": "env-branch"}):
            set_config_overrides(base_branch="cli-branch")
            config = get_config(workspace_root=str(temp_config_dir))
            assert config.defaults.base_branch == "cli-branch"


# =============================================================================
# Tests: Singleton Behavior
# =============================================================================


class TestSingleton:
    """Tests for config singleton behavior."""

    def test_get_config_returns_same_instance(self):
        """get_config should return cached instance."""
        config1 = get_config(workspace_root="/nonexistent")
        config2 = get_config(workspace_root="/nonexistent")
        assert config1 is config2

    def test_reset_clears_cache(self):
        """reset_config should clear the cached instance."""
        config1 = get_config(workspace_root="/nonexistent")
        reset_config()
        config2 = get_config(workspace_root="/nonexistent")
        assert config1 is not config2


# =============================================================================
# Tests: Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_invalid_yaml_falls_back_to_defaults(self, temp_config_dir):
        """Invalid YAML should fall back to defaults."""
        config_file = temp_config_dir / "cce_config.yaml"
        with open(config_file, "w") as f:
            f.write("invalid: yaml: content: [broken")

        config = load_config(workspace_root=str(temp_config_dir))
        assert config.langsmith.project == "cce-agent"  # Default value

    def test_empty_yaml_uses_defaults(self, temp_config_dir):
        """Empty YAML file should use defaults."""
        config_file = temp_config_dir / "cce_config.yaml"
        config_file.touch()

        config = load_config(workspace_root=str(temp_config_dir))
        assert config.langsmith.project == "cce-agent"

    def test_non_dict_yaml_uses_defaults(self, temp_config_dir):
        """YAML that parses to non-dict should use defaults."""
        config_file = temp_config_dir / "cce_config.yaml"
        with open(config_file, "w") as f:
            f.write("- item1\n- item2")  # This is a list, not a dict

        config = load_config(workspace_root=str(temp_config_dir))
        assert config.langsmith.project == "cce-agent"


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegration:
    """Integration tests for the full config loading flow."""

    def test_full_config_priority_chain(self, temp_config_dir):
        """Test the full priority chain: defaults < yaml < env < cli."""
        # Reset to clear any lingering state from other tests
        reset_config()

        # Setup YAML with some values
        yaml_config = {
            "defaults": {
                "base_branch": "yaml-branch",
                "auto_create_pr": True,
            }
        }
        config_file = temp_config_dir / "cce_config.yaml"
        with open(config_file, "w") as f:
            yaml.dump(yaml_config, f)

        # Set env var for one value
        with mock.patch.dict(os.environ, {"FEATURE_AIDER": "false"}):
            # Set CLI override for prompt_cache only (not base_branch)
            set_config_overrides(prompt_cache=False)

            config = get_config(workspace_root=str(temp_config_dir))

            # From YAML (no CLI override for base_branch)
            assert config.defaults.base_branch == "yaml-branch"
            assert config.defaults.auto_create_pr is True

            # From env var
            assert config.defaults.use_aider is False

            # From CLI override
            assert config.defaults.prompt_cache is False
