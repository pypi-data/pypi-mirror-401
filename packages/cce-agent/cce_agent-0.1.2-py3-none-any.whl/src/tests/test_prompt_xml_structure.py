import re
from pathlib import Path

REQUIRED_TAGS = {
    "objective",
    "quick_start",
    "success_criteria",
}

ALLOWED_TAGS = REQUIRED_TAGS | {
    "context",
    "workflow",
    "constraints",
    "guardrails",
    "examples",
    "tools",
    "thinking",
}

TAG_RE = re.compile(r"</?([A-Za-z][A-Za-z0-9_-]*)(?:\s+[^>]*)?>")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _validate_required_tags(text: str, path: Path) -> None:
    for tag in REQUIRED_TAGS:
        if f"<{tag}>" not in text or f"</{tag}>" not in text:
            raise AssertionError(f"{path}: missing required <{tag}> tag pair")


def _validate_tag_nesting(text: str, path: Path) -> None:
    cleaned = COMMENT_RE.sub("", text)
    stack: list[tuple[str, int]] = []

    for match in TAG_RE.finditer(cleaned):
        tag = match.group(1)
        if tag not in ALLOWED_TAGS:
            continue

        is_close = match.group(0).startswith("</")
        if not is_close:
            stack.append((tag, match.start()))
            continue

        if not stack:
            raise AssertionError(f"{path}: closing </{tag}> without opener")

        last_tag, last_pos = stack.pop()
        if last_tag != tag:
            raise AssertionError(f"{path}: mismatched closing </{tag}> for <{last_tag}> opened at {last_pos}")

    if stack:
        remaining = ", ".join([f"<{tag}>" for tag, _ in stack])
        raise AssertionError(f"{path}: unclosed tags: {remaining}")


def test_prompt_files_have_xml_structure() -> None:
    prompt_files = sorted(Path("src/prompts").rglob("*.md"))
    assert prompt_files, "No prompt files found under src/prompts"

    for path in prompt_files:
        text = path.read_text(encoding="utf-8")
        _validate_required_tags(text, path)
        _validate_tag_nesting(text, path)
