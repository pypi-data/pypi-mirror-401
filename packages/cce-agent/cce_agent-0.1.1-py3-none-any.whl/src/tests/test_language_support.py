from src.tools.file_discovery_config import ALLOWED_FILE_EXTENSIONS
from src.tools.validation.linting import LintingManager
from src.tools.validation.testing import FrameworkTestManager


def _collect_extensions(configs) -> set[str]:
    return {ext for config in configs for ext in config.extensions}


def _collect_patterns(configs) -> set[str]:
    return {pattern for config in configs for pattern in config.test_patterns}


def test_linting_supports_language_configs() -> None:
    linters = LintingManager.LINTERS
    expected_languages = {
        "javascript",
        "typescript",
        "go",
        "rust",
        "shell",
        "powershell",
        "yaml",
        "json",
        "toml",
        "xml",
        "sql",
        "terraform",
        "kubernetes",
        "solidity",
        "dockerfile",
        "html",
        "css",
    }
    missing = expected_languages - set(linters.keys())
    assert not missing, f"Missing linting configs: {sorted(missing)}"

    assert ".go" in _collect_extensions(linters["go"])
    assert ".rs" in _collect_extensions(linters["rust"])
    assert ".sol" in _collect_extensions(linters["solidity"])
    assert ".tf" in _collect_extensions(linters["terraform"])
    assert ".yaml" in _collect_extensions(linters["yaml"])
    assert ".json" in _collect_extensions(linters["json"])
    assert ".toml" in _collect_extensions(linters["toml"])
    assert ".dockerfile" in _collect_extensions(linters["dockerfile"])
    assert ".html" in _collect_extensions(linters["html"])
    assert ".css" in _collect_extensions(linters["css"])
    assert ".sh" in _collect_extensions(linters["shell"])


def test_testing_supports_frameworks() -> None:
    frameworks = FrameworkTestManager.FRAMEWORKS
    expected = {"javascript", "typescript", "go", "rust", "solidity"}
    missing = expected - set(frameworks.keys())
    assert not missing, f"Missing testing frameworks: {sorted(missing)}"

    assert "*_test.go" in _collect_patterns(frameworks["go"])
    assert "*_test.rs" in _collect_patterns(frameworks["rust"])
    assert "*.t.sol" in _collect_patterns(frameworks["solidity"])


def test_file_discovery_includes_languages() -> None:
    required_extensions = {
        ".js",
        ".ts",
        ".go",
        ".rs",
        ".sol",
        ".tf",
        ".yaml",
        ".json",
        ".toml",
        ".xml",
        ".html",
        ".css",
        ".dockerfile",
        ".sh",
    }
    missing = required_extensions - set(ALLOWED_FILE_EXTENSIONS)
    assert not missing, f"Missing file discovery extensions: {sorted(missing)}"
