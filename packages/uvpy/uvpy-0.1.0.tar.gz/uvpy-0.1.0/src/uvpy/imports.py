# -*- coding: utf-8 -*-
"""
uvpy Imports - Safe Package Imports

STDLIB ONLY - no external dependencies!

Provides helper functions to safely import packages
without crashing due to missing packages or GUI dependencies.
"""
import sys
from typing import Any, Optional


def try_import(name: str, package: Optional[str] = None, fallback: Any = None) -> Optional[Any]:
    """
    Try to import a module.

    Args:
        name: Module name (e.g. "numpy" or "matplotlib.pyplot")
        package: Optional package for relative imports
        fallback: Return value if import fails (default: None)

    Returns:
        The module or fallback if not available
    """
    try:
        import importlib
        return importlib.import_module(name, package)
    except Exception:
        return fallback


def require(name: str, message: Optional[str] = None) -> Any:
    """
    Import a module or raise ImportError.

    Args:
        name: Module name
        message: Optional error message (can use {name} as placeholder)

    Returns:
        The imported module

    Raises:
        ImportError: If the module is not available
    """
    module = try_import(name)
    if module is None:
        if message:
            msg = message.format(name=name)
        else:
            msg = f"Package '{name}' is required but not installed."
        raise ImportError(msg)
    return module


def is_available(*names: str) -> bool:
    """
    Check if modules are available without importing them.

    Args:
        *names: One or more module names

    Returns:
        True if all modules are available
    """
    import importlib.util
    for name in names:
        try:
            spec = importlib.util.find_spec(name)
            if spec is None:
                return False
        except (ModuleNotFoundError, ValueError):
            return False
    return True


class LazyModule:
    """
    Lazy-loading module wrapper.

    Delays the import until first attribute access.

    Example:
        np = LazyModule("numpy")
        # numpy is only imported here:
        result = np.array([1, 2, 3])
    """

    def __init__(self, name: str):
        self._name = name
        self._module = None

    def _load(self):
        if self._module is None:
            module = try_import(self._name)
            if module is None:
                raise ImportError(f"Module '{self._name}' could not be imported")
            self._module = module
        return self._module

    def __getattr__(self, attr: str) -> Any:
        if attr.startswith('_'):
            return object.__getattribute__(self, attr)
        return getattr(self._load(), attr)

    def __repr__(self) -> str:
        return f"LazyModule({self._name!r})"


def optional_import(name: str, default_return: Any = None):
    """
    Decorator for functions that need an optional module.

    Args:
        name: Module name
        default_return: Return value if module is not available

    Example:
        @optional_import("numpy", default_return=[])
        def calculate(np):
            return np.array([1, 2, 3]).tolist()

        result = calculate()  # [] if numpy is missing
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            module = try_import(name)
            if module is None:
                return default_return
            return func(module, *args, **kwargs)
        return wrapper
    return decorator


def get_version(name: str) -> Optional[str]:
    """Return the version of a module or None."""
    module = try_import(name)
    if module is None:
        return None
    return getattr(module, "__version__", None)


# === Special import functions for problematic packages ===

def import_numpy():
    """
    Import numpy safely.
    Returns None if not available.
    """
    return try_import("numpy")


def import_pandas():
    """
    Import pandas safely.
    Returns None if not available.
    """
    return try_import("pandas")


def import_matplotlib(backend: Optional[str] = None):
    """
    Import matplotlib safely with headless backend.

    MPLBACKEND is already set to 'Agg' by sandbox.py,
    but this function ensures it.

    Args:
        backend: Optional backend (default: Agg)

    Returns:
        matplotlib module or None
    """
    import os

    # Set backend BEFORE importing matplotlib
    if backend:
        os.environ["MPLBACKEND"] = backend
    elif "MPLBACKEND" not in os.environ:
        os.environ["MPLBACKEND"] = "Agg"

    return try_import("matplotlib")


def import_matplotlib_pyplot():
    """
    Import matplotlib.pyplot safely.

    Sets Agg backend to avoid X11 errors.
    """
    import os
    if "MPLBACKEND" not in os.environ:
        os.environ["MPLBACKEND"] = "Agg"

    return try_import("matplotlib.pyplot")


def import_streamlit():
    """
    Import streamlit safely.
    Telemetry is disabled by sandbox.py.
    """
    return try_import("streamlit")


def import_scipy():
    """Import scipy safely."""
    return try_import("scipy")


def import_xarray():
    """Import xarray safely."""
    return try_import("xarray")


# === Package info for --info output ===

KNOWN_PACKAGES = [
    "numpy",
    "pandas",
    "scipy",
    "matplotlib",
    "xarray",
    "streamlit",
    "plotly",
    "sklearn",
    "skimage",
    "PIL",
    "h5py",
    "tables",
    "openpyxl",
    "xlrd",
    "requests",
]


def list_available_packages() -> dict[str, Optional[str]]:
    """
    Return a dict with package names and versions.
    Packages not installed have None as version.
    """
    result = {}
    for name in KNOWN_PACKAGES:
        result[name] = get_version(name)
    return result


def print_package_info() -> None:
    """Print a formatted list of packages."""
    packages = list_available_packages()

    print("Available packages:")
    for name, version in sorted(packages.items()):
        if version:
            print(f"  {name:15} {version}")
        else:
            print(f"  {name:15} (not installed)")
