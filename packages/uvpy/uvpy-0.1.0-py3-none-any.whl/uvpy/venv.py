# -*- coding: utf-8 -*-
"""
uvpy venv - App Isolation with uv

STDLIB ONLY - no external dependencies!

Manages isolated venvs per app with:
- Portable uv binary from bin/
- Offline installation from pypi/
- No network communication
- Pinned Python version per universe
"""
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional


# Paths - from UVPY_ROOT environment variable
def _get_uvpy_root() -> Path:
    """Return UVPY_ROOT (from env or relative to module)."""
    root = os.environ.get("UVPY_ROOT")
    if root:
        return Path(root)
    # Fallback for direct execution
    return Path(__file__).parent.parent.parent.resolve()


UVPY_ROOT = _get_uvpy_root()
BIN_DIR = UVPY_ROOT / "bin"
PYPI_DIR = UVPY_ROOT / "pypi"
APPS_DIR = UVPY_ROOT / "apps"
PYTHON_DIR = UVPY_ROOT / "python"

# Pinned Python version (must match cli.py)
PYTHON_VERSION_MAJOR = 3
PYTHON_VERSION_MINOR = 12
PYTHON_VERSION = f"{PYTHON_VERSION_MAJOR}.{PYTHON_VERSION_MINOR}"


def get_portable_python() -> Optional[Path]:
    """
    Search for portable Python installation in python/.

    Returns:
        Path to Python interpreter or None
    """
    if not PYTHON_DIR.exists():
        return None

    system = platform.system().lower()

    if system == "windows":
        candidates = [
            PYTHON_DIR / "python.exe",
            PYTHON_DIR / f"python{PYTHON_VERSION}.exe",
            PYTHON_DIR / "Scripts" / "python.exe",
        ]
    else:
        candidates = [
            PYTHON_DIR / "bin" / f"python{PYTHON_VERSION}",
            PYTHON_DIR / "bin" / "python3",
            PYTHON_DIR / "bin" / "python",
            PYTHON_DIR / f"python{PYTHON_VERSION}",
        ]

    for path in candidates:
        if path.exists():
            return path

    return None


def get_python_for_venv() -> Path:
    """
    Return the Python interpreter for venv creation.

    ONLY portable Python from python/ - NO system fallback!
    The universe must have its own Python.

    Raises:
        FileNotFoundError: If no portable Python found
    """
    portable = get_portable_python()
    if portable:
        return portable

    raise FileNotFoundError(
        f"Python {PYTHON_VERSION} not found!\n"
        f"\n"
        f"This uvpy universe requires portable Python {PYTHON_VERSION}.\n"
        f"\n"
        f"Installation:\n"
        f"  cd {UVPY_ROOT}\n"
        f"  curl -LO https://github.com/indygreg/python-build-standalone/releases/download/20240224/cpython-{PYTHON_VERSION}.2+20240224-x86_64-unknown-linux-gnu-install_only.tar.gz\n"
        f"  tar xzf cpython-*.tar.gz\n"
        f"\n"
        f"Expected: {PYTHON_DIR}/bin/python{PYTHON_VERSION}"
    )


def get_uv_binary() -> Optional[Path]:
    """
    Find the appropriate uv binary for the current system.

    Returns:
        Path to uv binary or None if not found
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    # Possible names for uv binary
    candidates = []

    if system == "windows":
        candidates = ["uv.exe", "uv-windows.exe", "uv-win.exe"]
    elif system == "darwin":
        if "arm" in machine or "aarch64" in machine:
            candidates = ["uv-macos-arm64", "uv-macos", "uv"]
        else:
            candidates = ["uv-macos-x86_64", "uv-macos", "uv"]
    else:  # Linux
        if "aarch64" in machine or "arm" in machine:
            candidates = ["uv-linux-aarch64", "uv-linux-arm64", "uv"]
        else:
            candidates = ["uv-linux-x86_64", "uv-linux", "uv"]

    # Search in bin/
    for name in candidates:
        path = BIN_DIR / name
        if path.exists():
            return path

    # Fallback: uv in system PATH
    for name in ["uv", "uv.exe"]:
        try:
            result = subprocess.run(
                ["which" if system != "windows" else "where", name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return Path(result.stdout.strip().split("\n")[0])
        except Exception:
            pass

    return None


def ensure_uv() -> Path:
    """
    Ensure uv is available.

    Returns:
        Path to uv binary

    Raises:
        FileNotFoundError: If uv is not found
    """
    uv = get_uv_binary()
    if uv is None:
        raise FileNotFoundError(
            f"uv not found!\n"
            f"Please copy uv binary to {BIN_DIR}/.\n"
            f"Download: https://github.com/astral-sh/uv/releases"
        )

    # Make executable (Linux/macOS)
    if platform.system() != "Windows":
        uv.chmod(0o755)

    return uv


def get_app_venv(app_name: str) -> Path:
    """Return the path to an app's venv."""
    return APPS_DIR / app_name / ".venv"


def get_app_python(app_name: str) -> Optional[Path]:
    """
    Return the Python interpreter of an app's venv.

    Returns:
        Path to Python interpreter or None
    """
    venv = get_app_venv(app_name)
    if not venv.exists():
        return None

    if platform.system() == "Windows":
        python = venv / "Scripts" / "python.exe"
    else:
        python = venv / "bin" / "python"

    return python if python.exists() else None


def has_pyproject(app_name: str) -> bool:
    """Check if an app has a pyproject.toml."""
    return (APPS_DIR / app_name / "pyproject.toml").exists()


def create_venv(
    app_name: str,
    verbose: bool = False
) -> bool:
    """
    Create a venv for an app with pinned Python version.

    Args:
        app_name: Name of the app
        verbose: Verbose output

    Returns:
        True on success, False on error
    """
    app_dir = APPS_DIR / app_name
    venv_dir = app_dir / ".venv"

    if not app_dir.exists():
        print(f"Error: App '{app_name}' not found")
        return False

    uv = ensure_uv()

    # Find Python for this universe
    try:
        python = get_python_for_venv()
    except FileNotFoundError as e:
        print(str(e))
        return False

    # Create venv with specific Python
    cmd = [str(uv), "venv", str(venv_dir), "--python", str(python)]

    if verbose:
        print(f"Creating venv: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=app_dir, capture_output=not verbose)

    if result.returncode != 0:
        print(f"Error creating venv for '{app_name}'")
        if result.stderr:
            print(result.stderr.decode())
        return False

    return True


def get_dependencies(app_name: str) -> list[str]:
    """
    Read dependencies from pyproject.toml.

    Returns:
        List of dependencies or empty list
    """
    pyproject = APPS_DIR / app_name / "pyproject.toml"
    if not pyproject.exists():
        return []

    try:
        content = pyproject.read_text(encoding="utf-8")
        # Simple parsing - search for dependencies = [...]
        import re
        match = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
        if match:
            deps_str = match.group(1)
            # Extract strings from the list
            deps = re.findall(r'"([^"]+)"', deps_str)
            return [d for d in deps if d.strip()]
    except Exception:
        pass

    return []


def install_dependencies(
    app_name: str,
    verbose: bool = False,
    offline: bool = True
) -> bool:
    """
    Install dependencies for an app from pyproject.toml.

    Args:
        app_name: Name of the app
        verbose: Verbose output
        offline: Only install from local pypi/

    Returns:
        True on success, False on error
    """
    app_dir = APPS_DIR / app_name
    venv_dir = app_dir / ".venv"

    # Read dependencies from pyproject.toml
    deps = get_dependencies(app_name)

    if not deps:
        if verbose:
            print(f"  No dependencies for '{app_name}'")
        return True

    if not venv_dir.exists():
        if not create_venv(app_name, verbose=verbose):
            return False

    uv = ensure_uv()

    # pip install with uv - only dependencies, not the app itself
    cmd = [
        str(uv), "pip", "install",
        "--python", str(get_app_python(app_name)),
    ] + deps

    if offline and PYPI_DIR.exists():
        cmd.extend([
            "--offline",
            "--find-links", str(PYPI_DIR),
            "--no-index",
        ])

    if verbose:
        print(f"  Dependencies: {', '.join(deps)}")
        print(f"  Installing: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=app_dir, capture_output=not verbose)

    if result.returncode != 0:
        print(f"Error installing dependencies for '{app_name}'")
        if result.stderr:
            print(result.stderr.decode())
        return False

    return True


def setup_app(
    app_name: str,
    verbose: bool = False,
    offline: bool = True
) -> bool:
    """
    Create venv and install dependencies for an app.

    Args:
        app_name: Name of the app
        verbose: Verbose output
        offline: Only install from local pypi/

    Returns:
        True on success
    """
    print(f"Setup: {app_name}")

    # Create venv
    if not get_app_venv(app_name).exists():
        if not create_venv(app_name, verbose=verbose):
            return False
        print(f"  venv created")

    # Install dependencies
    if has_pyproject(app_name):
        if not install_dependencies(app_name, verbose=verbose, offline=offline):
            return False
        print(f"  Dependencies installed")
    else:
        print(f"  No pyproject.toml - no dependencies")

    return True


def setup_all_apps(verbose: bool = False, offline: bool = True) -> bool:
    """
    Create venvs for all apps.

    Returns:
        True if all successful
    """
    if not APPS_DIR.exists():
        print(f"Apps directory not found: {APPS_DIR}")
        return False

    success = True
    for app_dir in sorted(APPS_DIR.iterdir()):
        if not app_dir.is_dir():
            continue
        if app_dir.name.startswith(("_", ".")):
            continue
        if not (app_dir / "main.py").exists():
            continue

        if not setup_app(app_dir.name, verbose=verbose, offline=offline):
            success = False

    return success


def run_in_venv(app_name: str, command: list[str], **kwargs) -> subprocess.CompletedProcess:
    """
    Run a command in an app's venv.

    Args:
        app_name: Name of the app
        command: Command as list
        **kwargs: Additional arguments for subprocess.run

    Returns:
        CompletedProcess object
    """
    python = get_app_python(app_name)
    if python is None:
        raise FileNotFoundError(f"No venv for app '{app_name}'")

    # Replace 'python' with venv Python
    if command and command[0] in ("python", "python3"):
        command = [str(python)] + command[1:]

    app_dir = APPS_DIR / app_name
    return subprocess.run(command, cwd=app_dir, **kwargs)


def list_app_venvs() -> dict[str, bool]:
    """
    List all apps and whether they have a venv.

    Returns:
        Dict {app_name: has_venv}
    """
    result = {}
    for app_dir in sorted(APPS_DIR.iterdir()):
        if not app_dir.is_dir():
            continue
        if app_dir.name.startswith(("_", ".")):
            continue
        if not (app_dir / "main.py").exists():
            continue

        result[app_dir.name] = get_app_venv(app_dir.name).exists()

    return result


def lock_app(app_name: str, verbose: bool = False) -> bool:
    """
    Export installed package versions to requirements.lock.

    Args:
        app_name: Name of the app
        verbose: Verbose output

    Returns:
        True on success
    """
    app_dir = APPS_DIR / app_name
    lock_file = app_dir / "requirements.lock"
    python = get_app_python(app_name)

    if python is None:
        print(f"Error: No venv for '{app_name}' - first run 'uvpy venv {app_name}'")
        return False

    uv = ensure_uv()

    # uv pip freeze
    cmd = [str(uv), "pip", "freeze", "--python", str(python)]

    if verbose:
        print(f"Exporting: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error exporting for '{app_name}'")
        if result.stderr:
            print(result.stderr)
        return False

    # Write requirements.lock
    packages = result.stdout.strip()
    if not packages:
        print(f"  No packages in venv for '{app_name}'")
        return True

    lock_file.write_text(
        f"# Pinned versions for {app_name}\n"
        f"# Generated with: uvpy venv lock {app_name}\n"
        f"# Load with: uvpy venv download {app_name}\n"
        f"#\n"
        f"{packages}\n",
        encoding="utf-8"
    )

    pkg_count = len(packages.splitlines())
    print(f"  {lock_file.name}: {pkg_count} packages pinned")

    if verbose:
        for line in packages.splitlines():
            print(f"    {line}")

    return True


def download_packages(
    app_name: str,
    verbose: bool = False,
    platform_spec: Optional[str] = None
) -> bool:
    """
    Download packages from requirements.lock to pypi/.

    Args:
        app_name: Name of the app
        verbose: Verbose output
        platform_spec: Optional platform (e.g. "manylinux2014_x86_64")

    Returns:
        True on success
    """
    app_dir = APPS_DIR / app_name
    lock_file = app_dir / "requirements.lock"

    if not lock_file.exists():
        print(f"Error: {lock_file} not found")
        print(f"  First run 'uvpy venv lock {app_name}'")
        return False

    # Use portable Python for pip (uv has no 'pip download')
    python = get_portable_python()
    if not python:
        print("Error: Portable Python not found")
        return False

    # Create pypi/ if it doesn't exist
    PYPI_DIR.mkdir(exist_ok=True)

    # pip download
    cmd = [
        str(python), "-m", "pip", "download",
        "-r", str(lock_file),
        "--dest", str(PYPI_DIR),
        "--no-deps",  # Dependencies are already in lock_file
    ]

    if platform_spec:
        cmd.extend(["--platform", platform_spec, "--only-binary=:all:"])

    if verbose:
        print(f"Download: {' '.join(cmd)}")

    print(f"  Downloading packages to {PYPI_DIR}/...")

    result = subprocess.run(cmd, capture_output=not verbose)

    if result.returncode != 0:
        print(f"Error downloading for '{app_name}'")
        if result.stderr:
            print(result.stderr.decode())
        return False

    # Count .whl files
    whl_count = len(list(PYPI_DIR.glob("*.whl")))
    print(f"  {whl_count} packages in {PYPI_DIR}/")

    return True


def download_all_packages(verbose: bool = False) -> bool:
    """
    Download packages for all apps with requirements.lock.

    Returns:
        True if all successful
    """
    success = True
    for app_dir in sorted(APPS_DIR.iterdir()):
        if not app_dir.is_dir():
            continue
        if not (app_dir / "requirements.lock").exists():
            continue

        print(f"Download: {app_dir.name}")
        if not download_packages(app_dir.name, verbose=verbose):
            success = False

    return success


# === CLI when called directly ===

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="uvpy venv Manager")
    parser.add_argument("app", nargs="?", help="App name")
    parser.add_argument("--all", action="store_true", help="All apps")
    parser.add_argument("--list", action="store_true", help="List apps")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--online", action="store_true", help="Install online")

    args = parser.parse_args()

    if args.list:
        apps = list_app_venvs()
        print("Apps and venv status:")
        for name, has_venv in apps.items():
            status = "✓" if has_venv else "✗"
            pyproject = "📦" if has_pyproject(name) else "  "
            print(f"  {status} {pyproject} {name}")
        sys.exit(0)

    if args.all:
        success = setup_all_apps(verbose=args.verbose, offline=not args.online)
        sys.exit(0 if success else 1)

    if args.app:
        success = setup_app(args.app, verbose=args.verbose, offline=not args.online)
        sys.exit(0 if success else 1)

    parser.print_help()
