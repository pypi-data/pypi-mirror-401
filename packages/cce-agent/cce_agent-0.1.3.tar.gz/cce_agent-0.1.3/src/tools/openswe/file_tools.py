"""
File Operation Tools

Tools for file viewing, editing, creation, and management.
Includes advanced text editing capabilities and TypeScript configuration.
"""

import asyncio
import json
import logging
import os
import re
import subprocess
import tempfile
from typing import Any

from langchain_core.tools import tool

from .models import (
    PatchApplicationResponse,
)
from src.workspace_context import get_workspace_root

logger = logging.getLogger(__name__)


def _resolve_work_dir(work_dir: str | None) -> str:
    if work_dir and work_dir != ".":
        return work_dir
    resolved = get_workspace_root()
    return resolved or (work_dir or ".")


# Default TypeScript configuration
DEFAULT_TS_CONFIG = {
    "extends": "@tsconfig/recommended",
    "compilerOptions": {
        "target": "ES2021",
        "module": "NodeNext",
        "lib": ["ES2023"],
        "moduleResolution": "nodenext",
        "esModuleInterop": True,
        "noImplicitReturns": True,
        "declaration": True,
        "noFallthroughCasesInSwitch": True,
        "noUnusedLocals": True,
        "noUnusedParameters": True,
        "useDefineForClassFields": True,
        "strictPropertyInitialization": False,
        "allowJs": True,
        "strict": True,
        "strictFunctionTypes": False,
        "outDir": "dist",
        "types": ["node"],
        "resolveJsonModule": True,
    },
    "include": ["**/*.ts"],
    "exclude": ["node_modules", "dist"],
}


async def _apply_patch_with_git(diff_content: str, file_path: str, work_dir: str) -> dict[str, Any]:
    """Apply patch using git apply command"""
    temp_patch_file = None

    try:
        # Create temporary patch file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".diff", delete=False) as f:
            f.write(diff_content)
            temp_patch_file = f.name

        # Execute git apply
        cmd = ["git", "apply", "--verbose", temp_patch_file]
        process = await asyncio.create_subprocess_exec(
            *cmd, cwd=work_dir, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            return {"success": True, "result": "Patch applied successfully using git", "status": "success"}
        else:
            return {
                "success": False,
                "result": f"Git apply failed with exit code {process.returncode}",
                "status": "error",
                "git_error": stderr.decode("utf-8") if stderr else "No error output",
            }

    except Exception as e:
        return {"success": False, "result": f"Error applying patch with git: {str(e)}", "status": "error"}

    finally:
        # Clean up temp file
        if temp_patch_file and os.path.exists(temp_patch_file):
            try:
                os.unlink(temp_patch_file)
            except Exception as e:
                logger.warning(f"Failed to clean up temp patch file: {e}")


@tool
async def apply_patch(diff: str, file_path: str, work_dir: str = ".") -> PatchApplicationResponse:
    """
    Apply a patch to a file using git apply with fallback to diff library.

    Args:
        diff: The patch content in unified diff format
        file_path: Path to the file to patch
        work_dir: Working directory for git operations (default: current directory)

    Returns:
        Dictionary containing patch application results
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        # Read the original file
        full_file_path = os.path.join(work_dir, file_path)
        if not os.path.exists(full_file_path):
            return {"success": False, "result": f"File not found: {file_path}", "status": "error"}

        with open(full_file_path, encoding="utf-8") as f:
            original_content = f.read()

        # Try git apply first
        git_result = await _apply_patch_with_git(diff, file_path, work_dir)

        if git_result["success"]:
            return git_result

        # Fall back to simple string replacement for basic patches
        logger.warning(f"Git apply failed: {git_result['result']}. Attempting simple replacement.")

        # Simple diff application - look for lines starting with + and -
        diff_lines = diff.split("\n")
        modified_content = original_content

        for line in diff_lines:
            if line.startswith("-") and not line.startswith("---"):
                # Remove line
                old_line = line[1:]
                modified_content = modified_content.replace(old_line, "", 1)
            elif line.startswith("+") and not line.startswith("+++"):
                # Add line
                new_line = line[1:]
                # This is a simplified approach - in production you'd want more sophisticated logic
                modified_content += "\n" + new_line

        # Write the modified content
        with open(full_file_path, "w", encoding="utf-8") as f:
            f.write(modified_content)

        return {
            "success": True,
            "result": f"Successfully applied patch to {file_path} using fallback method",
            "status": "success",
            "git_error": git_result.get("git_error"),
        }

    except Exception as e:
        return {"success": False, "result": f"Error applying patch: {str(e)}", "status": "error"}


@tool
async def view(path: str, view_range: str | None = None, work_dir: str = ".") -> dict[str, Any]:
    """
    View file or directory contents.

    Args:
        path: File or directory path to view
        view_range: Line range for files (start, end) - optional
        work_dir: Working directory (default: current directory)

    Returns:
        Dictionary containing view results
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        full_path = os.path.join(work_dir, path)

        # Check if path exists
        if not os.path.exists(full_path):
            return {"success": False, "result": f"Path not found: {path}", "status": "error"}

        # Check if it's a directory
        if os.path.isdir(full_path):
            # List directory contents
            try:
                result = subprocess.run(["ls", "-la", full_path], capture_output=True, text=True, timeout=30)
                if result.returncode != 0:
                    return {"success": False, "result": f"Failed to list directory: {result.stderr}", "status": "error"}
                return {
                    "success": True,
                    "result": f"Directory listing for {path}:\n{result.stdout}",
                    "status": "success",
                }
            except subprocess.TimeoutExpired:
                return {"success": False, "result": "Directory listing timed out", "status": "error"}

        # Read file contents
        try:
            with open(full_path, encoding="utf-8") as f:
                content = f.read()

            # Apply view range if specified
            if view_range:
                lines = content.split("\n")
                try:
                    # Parse view_range as "start,end" string
                    if "," in view_range:
                        start, end = map(int, view_range.split(","))
                    else:
                        start = int(view_range)
                        end = start + 50  # Default range
                    start_index = max(0, start - 1)  # Convert to 0-indexed
                    end_index = end if end != -1 else len(lines)
                    end_index = min(len(lines), end_index)
                except ValueError:
                    # If parsing fails, show full file
                    start_index = 0
                    end_index = len(lines)

                selected_lines = lines[start_index:end_index]
                numbered_lines = [f"{start_index + i + 1}: {line}" for i, line in enumerate(selected_lines)]
                content = "\n".join(numbered_lines)
            else:
                # Return full file with line numbers
                lines = content.split("\n")
                numbered_lines = [f"{i + 1}: {line}" for i, line in enumerate(lines)]
                content = "\n".join(numbered_lines)

            return {"success": True, "result": content, "status": "success"}

        except Exception as e:
            return {"success": False, "result": f"Failed to read file: {str(e)}", "status": "error"}

    except Exception as e:
        return {"success": False, "result": f"Error in view command: {str(e)}", "status": "error"}


@tool
async def text_editor(
    command: str,
    path: str,
    view_range: str | None = None,
    old_str: str | None = None,
    new_str: str | None = None,
    file_text: str | None = None,
    insert_line: int | None = None,
    work_dir: str = ".",
) -> dict[str, Any]:
    """
    Advanced text editor for file operations.

    Args:
        command: Command to execute ("view", "str_replace", "create", "insert")
        path: File or directory path
        view_range: Line range for view command (start, end) - optional
        old_str: Old string for replacement - required for str_replace
        new_str: New string for replacement - required for str_replace
        file_text: File content for creation - required for create
        insert_line: Line number for insertion - required for insert
        work_dir: Working directory (default: current directory)

    Returns:
        Dictionary containing operation results
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        full_path = os.path.join(work_dir, path)

        if command == "view":
            return await view(path, view_range, work_dir)

        elif command == "str_replace":
            if not old_str or new_str is None:
                return {
                    "success": False,
                    "result": "str_replace command requires both old_str and new_str parameters",
                    "status": "error",
                }

            # Read file content
            try:
                with open(full_path, encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                return {"success": False, "result": f"Failed to read file {path}: {str(e)}", "status": "error"}

            # Count occurrences
            occurrences = len(re.findall(re.escape(old_str), content))

            if occurrences == 0:
                return {"success": False, "result": f"No match found for replacement text in {path}", "status": "error"}

            if occurrences > 1:
                return {
                    "success": False,
                    "result": f"Found {occurrences} matches for replacement text in {path}. Please provide more context to make a unique match.",
                    "status": "error",
                }

            # Perform replacement
            new_content = content.replace(old_str, new_str)

            # Write back to file
            try:
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
            except Exception as e:
                return {"success": False, "result": f"Failed to write file {path}: {str(e)}", "status": "error"}

            return {
                "success": True,
                "result": f"Successfully replaced text in {path} at exactly one location.",
                "status": "success",
            }

        elif command == "create":
            if not file_text:
                return {"success": False, "result": "create command requires file_text parameter", "status": "error"}

            # Check if file already exists
            if os.path.exists(full_path):
                return {
                    "success": False,
                    "result": f"File {path} already exists. Use str_replace to modify existing files.",
                    "status": "error",
                }

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # Write file
            try:
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(file_text)
            except Exception as e:
                return {"success": False, "result": f"Failed to create file {path}: {str(e)}", "status": "error"}

            return {"success": True, "result": f"Successfully created file {path}.", "status": "success"}

        elif command == "insert":
            if insert_line is None or new_str is None:
                return {
                    "success": False,
                    "result": "insert command requires both insert_line and new_str parameters",
                    "status": "error",
                }

            # Read file content
            try:
                with open(full_path, encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                return {"success": False, "result": f"Failed to read file {path}: {str(e)}", "status": "error"}

            lines = content.split("\n")

            # Insert at specified line (0 = beginning, 1 = after first line, etc.)
            insert_index = max(0, min(len(lines), insert_line))
            lines.insert(insert_index, new_str)

            new_content = "\n".join(lines)

            # Write back to file
            try:
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
            except Exception as e:
                return {"success": False, "result": f"Failed to write file {path}: {str(e)}", "status": "error"}

            return {
                "success": True,
                "result": f"Successfully inserted text in {path} at line {insert_line}.",
                "status": "success",
            }

        else:
            return {"success": False, "result": f"Unknown command: {command}", "status": "error"}

    except Exception as e:
        return {"success": False, "result": f"Error in text editor command: {str(e)}", "status": "error"}


@tool
async def write_default_tsconfig(work_dir: str = ".") -> dict[str, Any]:
    """
    Write a default TypeScript configuration file.

    Args:
        work_dir: Working directory where to write tsconfig.json (default: current directory)

    Returns:
        Dictionary containing operation results
    """
    try:
        work_dir = _resolve_work_dir(work_dir)
        tsconfig_path = os.path.join(work_dir, "tsconfig.json")

        # Check if tsconfig.json already exists
        if os.path.exists(tsconfig_path):
            return {"success": False, "result": f"tsconfig.json already exists at {tsconfig_path}", "status": "error"}

        # Write the default configuration
        with open(tsconfig_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_TS_CONFIG, f, indent=2)

        return {
            "success": True,
            "result": f"Successfully wrote default tsconfig.json to {tsconfig_path}",
            "status": "success",
        }

    except Exception as e:
        return {"success": False, "result": f"Error writing tsconfig.json: {str(e)}", "status": "error"}


__all__ = ["text_editor", "view", "apply_patch", "write_default_tsconfig"]
