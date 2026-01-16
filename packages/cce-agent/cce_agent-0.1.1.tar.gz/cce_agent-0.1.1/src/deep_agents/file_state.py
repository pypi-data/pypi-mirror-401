"""
Utilities for working with deepagents FileData entries in CCE state.
"""

from __future__ import annotations
from deepagents.backends.state import create_file_data, file_data_to_string, update_file_data
from deepagents.middleware.filesystem import FileData

FileEntry = FileData | str


def file_entry_to_text(entry: FileEntry) -> str:
    """Convert FileData or raw string entries into text."""
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict) and "content" in entry:
        try:
            return file_data_to_string(entry)
        except Exception:
            content = entry.get("content", [])
            if isinstance(content, list):
                return "\n".join(content)
            return str(content)
    return ""


def make_file_entry(content: str, created_at: str | None = None, modified_at: str | None = None) -> FileData:
    """Create a FileData entry with optional timestamps."""
    file_data = create_file_data(content, created_at=created_at)
    if modified_at:
        file_data["modified_at"] = modified_at
    return file_data


def update_file_entry(existing: FileEntry | None, content: str, modified_at: str | None = None) -> FileData:
    """Update a FileData entry or create a new one from content."""
    if isinstance(existing, dict) and "content" in existing:
        updated = update_file_data(existing, content)
        if modified_at:
            updated["modified_at"] = modified_at
        return updated
    return make_file_entry(content, modified_at=modified_at)


def file_entry_size(entry: FileEntry) -> int:
    """Return the character size of a file entry."""
    return len(file_entry_to_text(entry))
