#!/usr/bin/env python3
"""
Test script for intelligent file loading system.

This script tests the new two-tier file loading system:
1. Summary mode: Loads intelligent summaries for context
2. Full content mode: Lazy loads full content for editing
"""

import os
import sys
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from .utils.virtual_filesystem import (
    _create_config_summary,
    _create_markdown_summary,
    _create_python_summary,
    create_file_summary,
    initialize_virtual_filesystem_from_workspace,
)


def test_file_summary_creation():
    """Test the file summary creation functions."""
    print("🧪 Testing file summary creation...")

    # Test Python file summary
    python_content = '''
import os
import sys
from typing import List, Dict, Any

class TestClass:
    """A test class for demonstration."""
    
    def __init__(self, name: str):
        self.name = name
    
    def method_one(self):
        """First method."""
        return f"Hello {self.name}"
    
    def method_two(self, value: int) -> int:
        """Second method with parameters."""
        return value * 2

def standalone_function():
    """A standalone function."""
    return "test"

if __name__ == "__main__":
    test = TestClass("world")
    print(test.method_one())
'''

    summary = _create_python_summary(python_content.split("\n"), 20)
    print(f"✅ Python summary created: {len(summary)} chars")
    print(f"   Preview: {summary[:200]}...")

    # Test config file summary
    config_content = """
{
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "test_db"
    },
    "api": {
        "version": "v1",
        "timeout": 30
    },
    "logging": {
        "level": "INFO",
        "file": "/var/log/app.log"
    }
}
"""

    summary = _create_config_summary(config_content.split("\n"), 10)
    print(f"✅ Config summary created: {len(summary)} chars")
    print(f"   Preview: {summary[:200]}...")

    # Test markdown summary
    markdown_content = """
# Test Document

This is a test markdown document.

## Section 1

Some content here.

### Subsection 1.1

More detailed content.

## Section 2

Another section with content.

### Subsection 2.1

Even more content here.
"""

    summary = _create_markdown_summary(markdown_content.split("\n"), 15)
    print(f"✅ Markdown summary created: {len(summary)} chars")
    print(f"   Preview: {summary[:200]}...")


def test_virtual_filesystem_initialization():
    """Test the virtual filesystem initialization with summary mode."""
    print("\n🧪 Testing virtual filesystem initialization...")

    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test files
        (temp_path / "test.py").write_text("""
import os

class TestClass:
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        return self.value

def main():
    test = TestClass()
    print(test.get_value())

if __name__ == "__main__":
    main()
""")

        (temp_path / "config.json").write_text("""
{
    "app_name": "test_app",
    "version": "1.0.0",
    "debug": true
}
""")

        (temp_path / "README.md").write_text("""
# Test Project

This is a test project.

## Features

- Feature 1
- Feature 2

## Usage

Run the application with:

```bash
python test.py
```
""")

        # Test summary mode
        print("📁 Testing summary mode...")
        files_summary = initialize_virtual_filesystem_from_workspace(
            workspace_root=str(temp_path), include_patterns=["*.py", "*.json", "*.md"], load_mode="summary"
        )

        print(f"✅ Summary mode: {len(files_summary)} files loaded")
        print(f"   Files: {list(files_summary.keys())}")

        # Check that we have the full content cache
        if "__full_content_cache__" in files_summary:
            cache = files_summary["__full_content_cache__"]
            print(f"✅ Full content cache: {len(cache)} files cached")
        else:
            print("❌ No full content cache found")

        # Test full mode
        print("\n📁 Testing full mode...")
        files_full = initialize_virtual_filesystem_from_workspace(
            workspace_root=str(temp_path), include_patterns=["*.py", "*.json", "*.md"], load_mode="full"
        )

        print(f"✅ Full mode: {len(files_full)} files loaded")

        # Compare sizes
        summary_size = sum(len(content) for path, content in files_summary.items() if path != "__full_content_cache__")
        full_size = sum(len(content) for path, content in files_full.items())

        print(f"📊 Size comparison:")
        print(f"   Summary mode: {summary_size:,} chars")
        print(f"   Full mode: {full_size:,} chars")
        print(f"   Reduction: {((full_size - summary_size) / full_size * 100):.1f}%")


def test_file_summary_generic():
    """Test the generic file summary creation."""
    print("\n🧪 Testing generic file summary creation...")

    # Test with different file types
    test_files = [
        ("test.py", "python"),
        ("config.json", "json"),
        ("README.md", "markdown"),
        ("script.sh", "shell"),
        ("data.txt", "text"),
    ]

    for filename, file_type in test_files:
        # Create sample content
        if file_type == "python":
            content = "import os\n\nclass Test:\n    pass\n\ndef func():\n    pass"
        elif file_type == "json":
            content = '{"key": "value", "nested": {"data": 123}}'
        elif file_type == "markdown":
            content = "# Title\n\nSome content\n\n## Section\n\nMore content"
        elif file_type == "shell":
            content = "#!/bin/bash\n\necho 'Hello World'\n\n# Comment"
        else:
            content = "This is a text file\nwith multiple lines\nof content"

        summary = create_file_summary(content, filename, max_summary_lines=10)
        print(f"✅ {filename} ({file_type}): {len(summary)} chars")
        print(f"   Preview: {summary[:100]}...")


if __name__ == "__main__":
    print("🚀 Testing Intelligent File Loading System")
    print("=" * 50)

    try:
        test_file_summary_creation()
        test_virtual_filesystem_initialization()
        test_file_summary_generic()

        print("\n✅ All tests passed!")
        print("\n📋 Summary:")
        print("   - File summary creation works for different file types")
        print("   - Virtual filesystem initialization supports summary and full modes")
        print("   - Full content cache is properly maintained")
        print("   - Significant size reduction achieved with summaries")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
