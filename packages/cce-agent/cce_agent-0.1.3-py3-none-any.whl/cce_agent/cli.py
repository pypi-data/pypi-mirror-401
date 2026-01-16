"""Package entrypoint for the CCE CLI."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the packaged "src" module is resolved ahead of any target repo "src/".
package_root = Path(__file__).resolve().parent.parent
if str(package_root) not in sys.path:
    sys.path.insert(0, str(package_root))

from src.cli import create_parser, main

__all__ = ["create_parser", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
