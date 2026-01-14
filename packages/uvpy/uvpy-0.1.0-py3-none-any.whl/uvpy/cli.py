# -*- coding: utf-8 -*-
"""
uvpy - Portable Python App Framework

Two modes:
1. Portable (UVPY_ROOT set): With portable Python, uv, offline pypi/
2. Installed (pip install uvpy): Standard Python, apps from ./apps/

Features:
- Isolated venvs per app (via uv)
- Offline installation from local pypi/ (portable only)
- Sandbox: localhost only, no telemetry
"""
import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from . import __version__


# === Mode Detection ===

def is_portable_mode() -> bool:
    """Check if uvpy is running in portable mode."""
    return "UVPY_ROOT" in os.environ


def get_uvpy_root() -> Optional[Path]:
    """Return UVPY_ROOT if in portable mode."""
    root = os.environ.get("UVPY_ROOT")
    return Path(root) if root else None


def check_python_version() -> None:
    """
    Check if Python version matches the universe.
    Only relevant in portable mode.
    """
    if not is_portable_mode():
        return

    # Pinned Python version for the portable universe
    PYTHON_VERSION_MAJOR = 3
    PYTHON_VERSION_MINOR = 12

    current = sys.version_info

    if current.major != PYTHON_VERSION_MAJOR or current.minor != PYTHON_VERSION_MINOR:
        print(f"ERROR: Python version not compatible!")
        print(f"")
        print(f"  Expected:  Python {PYTHON_VERSION_MAJOR}.{PYTHON_VERSION_MINOR}.x")
        print(f"  Found:     Python {current.major}.{current.minor}.{current.micro}")
        print(f"")
        print(f"This uvpy universe is built for Python {PYTHON_VERSION_MAJOR}.{PYTHON_VERSION_MINOR}.")
        print(f"All packages in pypi/ are compiled for cp{PYTHON_VERSION_MAJOR}{PYTHON_VERSION_MINOR}.")
        print(f"")
        print(f"Solutions:")
        print(f"  1. Use Python {PYTHON_VERSION_MAJOR}.{PYTHON_VERSION_MINOR}")
        print(f"  2. Use a different uvpy universe for Python {current.major}.{current.minor}")
        sys.exit(1)


# === Path Configuration ===

def get_default_apps_path() -> Path:
    """Get default apps path based on mode."""
    if is_portable_mode():
        return get_uvpy_root() / "apps"
    # Installed mode: apps in current working directory
    return Path.cwd() / "apps"


def get_default_extrapy_path() -> Path:
    """Get default extrapy path based on mode."""
    if is_portable_mode():
        return get_uvpy_root() / "extrapy"
    return Path.cwd() / "extrapy"


def setup_logging(level: Optional[str] = None) -> None:
    """Configure logging based on environment variable."""
    level = level or os.environ.get("UVPY_LOG")
    if not level:
        logging.disable(logging.CRITICAL)
        return

    numeric_level = getattr(logging, level.upper(), logging.WARNING)
    logging.basicConfig(
        level=numeric_level,
        format="[%(levelname)s] %(message)s"
    )


def setup_extrapy(extrapy_path: Path) -> None:
    """
    Add extrapy paths to sys.path.

    Supports:
    - Directories with Python packages
    - .egg files
    - .whl files
    - .so/.pyd files (Nuitka/Cython)
    """
    if not extrapy_path.exists():
        logging.warning(f"extrapy path does not exist: {extrapy_path}")
        return

    # Main directory first
    sys.path.insert(0, str(extrapy_path))
    logging.info(f"extrapy: {extrapy_path}")

    # Search contents
    for item in sorted(extrapy_path.iterdir()):
        if item.name.startswith(("_", ".")):
            continue

        if item.suffix in (".egg", ".whl"):
            sys.path.insert(0, str(item))
            logging.info(f"  + {item.name}")
        elif item.is_dir():
            # Subdirectory as separate package source
            sys.path.insert(0, str(item))
            logging.info(f"  + {item.name}/")


# === App Class ===

class App:
    """Represents a loaded app."""

    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.manifest = {}
        self.module = None
        self._load_manifest()

    def _load_manifest(self) -> None:
        """Load manifest.json if present."""
        manifest_path = self.path / "manifest.json"
        if manifest_path.exists():
            try:
                self.manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as e:
                logging.warning(f"Error loading {manifest_path}: {e}")

    @property
    def description(self) -> str:
        return self.manifest.get("description", "")

    @property
    def version(self) -> str:
        return self.manifest.get("version", "")

    def load_module(self):
        """Load the main.py module of the app."""
        if self.module is not None:
            return self.module

        main_path = self.path / "main.py"
        if not main_path.exists():
            raise FileNotFoundError(f"main.py not found: {main_path}")

        import importlib.util
        spec = importlib.util.spec_from_file_location(f"apps.{self.name}", main_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load {main_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[f"apps.{self.name}"] = module
        spec.loader.exec_module(module)
        self.module = module
        return module

    def register(self, subparser: argparse.ArgumentParser) -> None:
        """Register CLI arguments via the app."""
        try:
            module = self.load_module()
            if hasattr(module, "register"):
                module.register(subparser)
        except Exception as e:
            logging.error(f"Error registering '{self.name}': {e}")

    def has_venv(self) -> bool:
        """Check if the app has a venv."""
        venv_path = self.path / ".venv"
        return venv_path.exists() and venv_path.is_dir()

    def run(self, args: argparse.Namespace, raw_args: list[str] = None) -> int:
        """
        Run the app.

        - With .venv/ (portable mode): Via uv run (isolated)
        - Without .venv/: In-process (for simple apps)
        """
        if self.has_venv() and is_portable_mode():
            return self._run_with_uv(raw_args or [])
        else:
            return self._run_in_process(args)

    def _run_with_uv(self, raw_args: list[str]) -> int:
        """Run the app via uv run in its venv."""
        import subprocess

        uvpy_root = get_uvpy_root()
        if not uvpy_root:
            logging.error("UVPY_ROOT not set")
            return 1

        uv_path = self._find_uv(uvpy_root)
        app_runner = Path(__file__).parent / "app_runner.py"

        if not uv_path:
            logging.error("uv not found in bin/")
            return 1

        if not app_runner.exists():
            logging.error(f"app_runner.py not found: {app_runner}")
            return 1

        cmd = [
            str(uv_path), "run",
            "--directory", str(self.path),
            "--offline",
            "--no-sync",
            "python", str(app_runner), str(self.path)
        ] + raw_args

        logging.debug(f"uv run: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd)
            return result.returncode
        except Exception as e:
            logging.error(f"Error starting '{self.name}': {e}")
            return 1

    def _find_uv(self, uvpy_root: Path) -> Path | None:
        """Find the uv binary."""
        import platform

        bin_dir = uvpy_root / "bin"
        system = platform.system().lower()

        if system == "windows":
            candidates = [bin_dir / "uv.exe"]
        elif system == "darwin":
            candidates = [bin_dir / "uv-macos", bin_dir / "uv"]
        else:
            candidates = [bin_dir / "uv"]

        for uv in candidates:
            if uv.exists() and os.access(uv, os.X_OK):
                return uv

        return None

    def _run_in_process(self, args: argparse.Namespace) -> int:
        """Run the app in the current process (for apps without venv)."""
        try:
            module = self.load_module()
            if hasattr(module, "run"):
                result = module.run(args)
                return result if isinstance(result, int) else 0
            else:
                logging.error(f"App '{self.name}' has no run() function")
                return 1
        except Exception as e:
            logging.error(f"Error in app '{self.name}': {e}")
            if os.environ.get("UVPY_DEBUG"):
                raise
            return 1


# === App Discovery ===

def discover_apps(apps_path: Path) -> dict[str, App]:
    """
    Find all apps in the apps/ directory.

    An app is a directory with at least a main.py file.
    """
    apps = {}

    if not apps_path.exists():
        logging.warning(f"Apps path does not exist: {apps_path}")
        return apps

    for item in sorted(apps_path.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith(("_", ".")):
            continue

        main_py = item / "main.py"
        if not main_py.exists():
            logging.debug(f"Skipping {item.name}: no main.py")
            continue

        try:
            app = App(item)
            apps[app.name] = app
            logging.info(f"App found: {app.name}")
        except Exception as e:
            logging.warning(f"Error loading app '{item.name}': {e}")

    return apps


# === Argument Parser ===

def create_parser(apps: dict[str, App], portable: bool = False) -> argparse.ArgumentParser:
    """Create the argument parser with all app subcommands."""
    parser = argparse.ArgumentParser(
        prog="uvpy",
        description="uvpy - Portable Python App Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"uvpy {__version__}"
    )

    parser.add_argument(
        "--list-apps",
        action="store_true",
        help="Show all available apps"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output"
    )

    if portable:
        parser.add_argument(
            "--security-info",
            action="store_true",
            help="Show security settings"
        )

    # Subparser for apps
    if apps:
        subparsers = parser.add_subparsers(
            dest="app",
            title="Apps",
            description="Available apps (use '<app> --help' for details)"
        )

        for name, app in apps.items():
            subparser = subparsers.add_parser(
                name,
                help=app.description,
                formatter_class=argparse.RawDescriptionHelpFormatter
            )
            app.register(subparser)

    return parser


# === Display Functions ===

def show_security_info() -> None:
    """Show active security settings."""
    from . import sandbox

    print("=== uvpy Security Settings ===\n")

    print("Sandbox Status:", "ACTIVE" if sandbox.is_active() else "INACTIVE")
    print()

    print("Network Restrictions:")
    print("  - Only localhost connections allowed")
    print("  - Allowed hosts: localhost, 127.0.0.1, ::1, 0.0.0.0")
    print("  - External HTTP/HTTPS requests blocked")
    print()

    print("Telemetry disabled for:")
    print("  - Streamlit (STREAMLIT_BROWSER_GATHER_USAGE_STATS=false)")
    print("  - Matplotlib (MPLBACKEND=Agg)")
    print("  - Sentry (SENTRY_DSN='')")
    print("  - Google Analytics")
    print("  - PIP update checks")
    print()

    print("Environment variables:")
    for key in sorted(os.environ.keys()):
        if any(x in key.upper() for x in ["STREAMLIT", "SENTRY", "PROXY", "ANALYTICS"]):
            print(f"  {key}={os.environ[key]}")


def list_apps(apps: dict[str, App]) -> None:
    """Print a formatted list of all apps."""
    if not apps:
        print("No apps found.")
        return

    print(f"Available apps ({len(apps)}):\n")

    max_name_len = max(len(name) for name in apps.keys())

    for name, app in sorted(apps.items()):
        version_str = f" v{app.version}" if app.version else ""
        desc = app.description or "(no description)"
        print(f"  {name:<{max_name_len}}  {desc}{version_str}")

    print(f"\nUse 'uvpy <app> --help' for details on an app.")


# === Command Handlers ===

def handle_venv_command() -> Optional[int]:
    """
    Handle 'uvpy venv' commands separately.
    Only available in portable mode.

    Returns:
        Exit code or None if not a venv command
    """
    if len(sys.argv) < 2 or sys.argv[1] != "venv":
        return None

    if not is_portable_mode():
        print("ERROR: 'uvpy venv' is only available in portable mode.")
        print()
        print("  The venv command requires:")
        print("  - Portable Python in python/")
        print("  - uv binary in bin/")
        print("  - Offline packages in pypi/")
        print()
        print("  Use the portable uvpy bundle for this feature.")
        return 1

    from . import venv as venv_module

    # Parse venv command arguments
    venv_args = sys.argv[2:]

    if not venv_args or "--help" in venv_args or "-h" in venv_args:
        print("Usage: uvpy venv <command> [OPTIONS] [APP]")
        print()
        print("Commands:")
        print("  <app>           Set up venv for app")
        print("  --all           Set up all apps")
        print("  --list          Show apps and venv status")
        print("  lock <app>      Pin versions in requirements.lock")
        print("  download <app>  Download pinned packages to pypi/")
        print()
        print("Options:")
        print("  --verbose, -v   Verbose output")
        print("  --online        Install online (instead of from pypi/)")
        print()
        print("Workflow for offline deployment:")
        print("  1. uvpy venv dashboard --online   # Install online")
        print("  2. uvpy venv lock dashboard       # Pin versions")
        print("  3. uvpy venv download dashboard   # Download to pypi/")
        print("  4. uvpy venv dashboard            # Install offline")
        return 0

    verbose = "--verbose" in venv_args or "-v" in venv_args
    online = "--online" in venv_args

    # --list
    if "--list" in venv_args:
        apps = venv_module.list_app_venvs()
        print("Apps and venv status:\n")
        for name, has_venv in apps.items():
            status = "✓ venv" if has_venv else "✗ no venv"
            pyproject = "📦" if venv_module.has_pyproject(name) else "  "
            lock = "🔒" if (venv_module.APPS_DIR / name / "requirements.lock").exists() else "  "
            print(f"  {pyproject} {lock} {name:15} {status}")
        return 0

    # --all
    if "--all" in venv_args:
        success = venv_module.setup_all_apps(verbose=verbose, offline=not online)
        return 0 if success else 1

    # lock <app>
    if "lock" in venv_args:
        idx = venv_args.index("lock")
        if idx + 1 < len(venv_args) and not venv_args[idx + 1].startswith("-"):
            app_name = venv_args[idx + 1]
            success = venv_module.lock_app(app_name, verbose=verbose)
            return 0 if success else 1
        else:
            print("Error: Specify app name after 'lock'")
            return 1

    # download <app>
    if "download" in venv_args:
        idx = venv_args.index("download")
        if idx + 1 < len(venv_args) and not venv_args[idx + 1].startswith("-"):
            app_name = venv_args[idx + 1]
            success = venv_module.download_packages(app_name, verbose=verbose)
            return 0 if success else 1
        elif "--all" in venv_args:
            success = venv_module.download_all_packages(verbose=verbose)
            return 0 if success else 1
        else:
            print("Error: Specify app name after 'download'")
            return 1

    # Set up single app
    app_name = None
    for arg in venv_args:
        if not arg.startswith("-"):
            app_name = arg
            break

    if app_name:
        success = venv_module.setup_app(app_name, verbose=verbose, offline=not online)
        return 0 if success else 1

    print("Error: Specify command or app name")
    return 1


def _list_pypi_packages(pypi_dir: Path) -> int:
    """List all available packages in pypi/."""
    if not pypi_dir.exists():
        print(f"pypi/ directory not found: {pypi_dir}")
        return 1

    whl_files = sorted(pypi_dir.glob("*.whl"))

    if not whl_files:
        print("No packages in pypi/.")
        print()
        print("Download packages with:")
        print("  uvpy download --online numpy pandas matplotlib")
        return 0

    # Extract package names and versions
    # Format: name-version-python-abi-platform.whl
    packages: dict[str, list[str]] = {}

    for whl in whl_files:
        # Parse wheel filename: name-version-...
        parts = whl.name.split("-")
        if len(parts) >= 2:
            # Name can contain underscores, version is always part 2
            name = parts[0].lower().replace("_", "-")
            version = parts[1]

            if name not in packages:
                packages[name] = []
            if version not in packages[name]:
                packages[name].append(version)

    # Print sorted
    print(f"Available packages in pypi/ ({len(packages)} packages, {len(whl_files)} files):\n")

    max_name_len = max(len(name) for name in packages.keys()) if packages else 10

    for name in sorted(packages.keys()):
        versions = sorted(packages[name], reverse=True)
        versions_str = ", ".join(versions[:3])
        if len(versions) > 3:
            versions_str += f", ... (+{len(versions) - 3})"
        print(f"  {name:<{max_name_len}}  {versions_str}")

    print()
    print(f"Total: {len(whl_files)} .whl files")

    return 0


def handle_download_command() -> Optional[int]:
    """
    Handle 'uvpy download' commands separately.
    Only available in portable mode.

    Download is only allowed with --online (security).
    Default is offline mode, which blocks downloads.

    Returns:
        Exit code or None if not a download command
    """
    if len(sys.argv) < 2 or sys.argv[1] != "download":
        return None

    if not is_portable_mode():
        print("ERROR: 'uvpy download' is only available in portable mode.")
        print()
        print("  Use the portable uvpy bundle for this feature.")
        return 1

    import subprocess

    args = sys.argv[2:]
    uvpy_root = get_uvpy_root()
    pypi_dir = uvpy_root / "pypi"

    if not args or "--help" in args or "-h" in args:
        print("Usage: uvpy download [--list] [--online] <package> [<package>...]")
        print()
        print("Download Python packages to pypi/.")
        print()
        print("IMPORTANT: Only use in non-critical environments!")
        print("           Download is blocked in offline mode (default).")
        print()
        print("Options:")
        print("  --list          Show available packages in pypi/")
        print("  --online        Allow download (REQUIRED for download)")
        print("  --verbose, -v   Verbose output")
        print()
        print("Examples:")
        print("  uvpy download --list")
        print("  uvpy download --online numpy")
        print("  uvpy download --online numpy==1.26.4 pandas==2.2.0")
        print("  uvpy download --online matplotlib scipy xarray")
        return 0

    # --list: Show available packages
    if "--list" in args:
        return _list_pypi_packages(pypi_dir)

    # Check if --online is set
    if "--online" not in args:
        print("ERROR: Download not allowed in offline mode!")
        print()
        print("  This command is only available with --online")
        print("  in non-critical environments for security reasons.")
        print()
        print("  Example: uvpy download --online numpy==1.26.4")
        return 1

    # Parse arguments
    verbose = "--verbose" in args or "-v" in args
    packages = [a for a in args if not a.startswith("-")]

    if not packages:
        print("ERROR: No packages specified")
        return 1

    # Find Python
    python = uvpy_root / "python" / "bin" / "python3.12"
    if not python.exists():
        python = uvpy_root / "python" / "python.exe"  # Windows
    if not python.exists():
        print(f"ERROR: Python not found")
        return 1

    # Create pypi/ if it doesn't exist
    pypi_dir.mkdir(exist_ok=True)

    # Run pip download
    cmd = [
        str(python), "-m", "pip", "download",
        "--dest", str(pypi_dir),
        "--only-binary=:all:",
    ] + packages

    if verbose:
        print(f"Download: {' '.join(cmd)}")

    print(f"Downloading {len(packages)} package(s) to {pypi_dir}/...")
    print()

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print()
        print("ERROR during download")
        return 1

    # Count .whl files
    whl_count = len(list(pypi_dir.glob("*.whl")))
    print()
    print(f"Done. {whl_count} packages in {pypi_dir}/")

    return 0


# === Main Entry Point ===

def main() -> int:
    """Main entry point."""
    # Check Python version (only in portable mode)
    check_python_version()

    portable = is_portable_mode()

    # Handle venv command separately (before sandbox for uv access)
    venv_result = handle_venv_command()
    if venv_result is not None:
        return venv_result

    # Handle download command separately (before sandbox for network access)
    download_result = handle_download_command()
    if download_result is not None:
        return download_result

    # === ACTIVATE SANDBOX (after venv/download, before app execution) ===
    if portable:
        from . import sandbox
        sandbox.activate()
    # ==========================================================

    # Logging setup
    setup_logging()

    # Detect debug mode early
    if "--debug" in sys.argv:
        os.environ["UVPY_DEBUG"] = "1"
        os.environ["UVPY_LOG"] = "DEBUG"
        setup_logging("DEBUG")

    # Set up extrapy (portable only)
    if portable:
        extrapy_path = Path(os.environ.get("UVPY_EXTRAPY", get_default_extrapy_path()))
        setup_extrapy(extrapy_path)

    # Discover apps
    apps_path = Path(os.environ.get("UVPY_APPS", get_default_apps_path()))
    apps = discover_apps(apps_path)

    # Create parser
    parser = create_parser(apps, portable=portable)

    # Parse arguments
    args, remaining = parser.parse_known_args()

    # --security-info (portable only)
    if portable and getattr(args, 'security_info', False):
        show_security_info()
        return 0

    # --list-apps
    if args.list_apps:
        list_apps(apps)
        return 0

    # No app specified
    if not args.app:
        parser.print_help()
        return 0

    # Run app
    if args.app in apps:
        app = apps[args.app]

        # Extract raw arguments for uv run
        # sys.argv: ['uvpy', 'dashboard', '--name', 'foo']
        # raw_args: ['--name', 'foo']
        try:
            app_index = sys.argv.index(args.app)
            raw_args = sys.argv[app_index + 1:]
        except ValueError:
            raw_args = []

        return app.run(args, raw_args)
    else:
        print(f"Unknown app: {args.app}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
