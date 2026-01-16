#!/usr/bin/env python3
"""
CCE Agent module entrypoint.

Allows running CCE via: python -m src
"""

from src.cli import main

if __name__ == "__main__":
    exit(main())
