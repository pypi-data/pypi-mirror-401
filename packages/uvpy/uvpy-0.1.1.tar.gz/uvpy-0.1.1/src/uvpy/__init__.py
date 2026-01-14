# -*- coding: utf-8 -*-
"""
uvpy - Portable Python App Framework

A framework for isolated Python apps with:
- Portable Python (optional)
- Isolated venvs per app (via uv)
- Offline installation from local pypi/
- Sandbox: localhost only, no telemetry
"""

try:
    from importlib.metadata import version as _get_version
    __version__ = _get_version("uvpy")
except Exception:
    __version__ = "0.1.0"

# Python version for portable universe (single source of truth)
PYTHON_VERSION_MAJOR = 3
PYTHON_VERSION_MINOR = 12
PYTHON_VERSION = f"{PYTHON_VERSION_MAJOR}.{PYTHON_VERSION_MINOR}"

from .sandbox import activate as activate_sandbox
from .imports import try_import, require, is_available, LazyModule, optional_import

__all__ = [
    "__version__",
    "PYTHON_VERSION_MAJOR",
    "PYTHON_VERSION_MINOR",
    "PYTHON_VERSION",
    "activate_sandbox",
    "try_import",
    "require",
    "is_available",
    "LazyModule",
    "optional_import",
]
