# -*- coding: utf-8 -*-
"""
uvpy - Entry point for python -m uvpy

Enables:
  python -m uvpy --help
  python -m uvpy hello
"""
from .cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
