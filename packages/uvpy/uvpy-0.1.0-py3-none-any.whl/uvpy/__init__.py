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

from .sandbox import activate as activate_sandbox
from .imports import try_import, require, is_available, LazyModule, optional_import

__all__ = [
    "__version__",
    "activate_sandbox",
    "try_import",
    "require",
    "is_available",
    "LazyModule",
    "optional_import",
]
