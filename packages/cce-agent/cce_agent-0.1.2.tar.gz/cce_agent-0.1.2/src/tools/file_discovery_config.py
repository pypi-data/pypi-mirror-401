"""
File Discovery Configuration

This file controls what files and directories are included/excluded
during the file discovery process.
"""

# Directories to include in file discovery
ALLOWED_DIRECTORIES = [
    "./app",
    "./components",
    "./lib",
    "./scripts",
    "./styles",
    "./src",
]

# Directories to exclude from file discovery
EXCLUDED_DIRECTORIES = [
    "debug_context",
    "patches",
    "runs",
    "notebooks",
    "scratch",
    "docs",
    "graph_visualizations",
    "node_modules",
    "__pycache__",
    ".git",
    "dist",
    "build",
]

# File patterns to exclude
EXCLUDED_FILE_PATTERNS = [
    "*.pyc",
    "*.log",
    "*.tmp",
    ".DS_Store",
    "*.swp",
    "*.md",
    "*.txt",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.svg",
]

# File extensions to include (only these will be discovered)
ALLOWED_FILE_EXTENSIONS = [
    ".py",
    ".js",
    ".mjs",
    ".cjs",
    ".sh",
    ".bash",
    ".ps1",
    ".psm1",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".cs",
    ".php",
    ".rb",
    ".go",
    ".rs",
    ".swift",
    ".kt",
    ".scala",
    ".sql",
    ".sol",
    ".tf",
    ".tfvars",
    ".dockerfile",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".xml",
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".sass",
]

# File names to include (extensions are not required)
ALLOWED_FILE_NAMES = [
    "Makefile",
    "makefile",
    "GNUmakefile",
    "Dockerfile",
    "Dockerfile.*",
    "dockerfile",
    "dockerfile.*",
]

# Maximum number of files to discover
MAX_FILES_LIMIT = 200


def get_discovery_config():
    """Get the current file discovery configuration."""
    return {
        "allowed_directories": ALLOWED_DIRECTORIES,
        "excluded_directories": EXCLUDED_DIRECTORIES,
        "excluded_file_patterns": EXCLUDED_FILE_PATTERNS,
        "allowed_file_extensions": ALLOWED_FILE_EXTENSIONS,
        "allowed_file_names": ALLOWED_FILE_NAMES,
        "max_files_limit": MAX_FILES_LIMIT,
    }
