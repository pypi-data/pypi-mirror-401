from pathlib import Path

from src.prompts.manager import PromptManager


def test_prompt_folder_structure() -> None:
    base = Path("src/prompts")
    required_dirs = [
        "identity",
        "phases",
        "tools",
        "frameworks",
        "guardrails",
    ]

    for directory in required_dirs:
        assert (base / directory).is_dir(), f"Missing prompt directory: {directory}"

    assert (base / "README.md").exists(), "Missing src/prompts/README.md"

    phase_files = ["orient.md", "execute.md", "reconcile.md", "decide.md"]
    for filename in phase_files:
        assert (base / "phases" / filename).exists(), f"Missing phase prompt: {filename}"


def test_prompt_manager_uses_prompt_hub_over_disk(tmp_path: Path) -> None:
    prompt_dir = tmp_path / "identity"
    prompt_dir.mkdir(parents=True)
    prompt_file = prompt_dir / "cce_identity.md"
    prompt_file.write_text("local content", encoding="utf-8")

    manager = PromptManager(base_path=str(tmp_path))
    manager._prompt_hub_enabled = True
    manager._prompt_hub_sync_mode = "pull"
    manager._prompt_hub_allowlist = {"identity/cce_identity.md"}
    manager._load_template_from_prompt_hub = lambda _path: "hub content"

    manager._cache.clear()
    content = manager.load_template("identity/cce_identity.md", use_cache=False)
    assert content == "hub content"


def test_prompt_manager_falls_back_to_disk_when_hub_missing(tmp_path: Path) -> None:
    prompt_dir = tmp_path / "identity"
    prompt_dir.mkdir(parents=True)
    prompt_file = prompt_dir / "cce_identity.md"
    prompt_file.write_text("local content", encoding="utf-8")

    manager = PromptManager(base_path=str(tmp_path))
    manager._prompt_hub_enabled = True
    manager._prompt_hub_sync_mode = "pull"
    manager._prompt_hub_allowlist = {"identity/cce_identity.md"}
    manager._load_template_from_prompt_hub = lambda _path: None

    manager._cache.clear()
    content = manager.load_template("identity/cce_identity.md", use_cache=False)
    assert content == "local content"
