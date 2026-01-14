# -*- coding: utf-8 -*-
"""
uvpy App Runner - Executes apps in their venv.

Called by uvpy via `uv run`:
    uv run --directory apps/<app> python /path/to/app_runner.py <app_path> [args...]

This script:
1. Activates the sandbox (security)
2. Loads the app from main.py
3. Parses CLI arguments
4. Executes app.run(args)
"""
import sys
import os
import argparse
import importlib.util
from pathlib import Path


def activate_sandbox() -> None:
    """Activate the security sandbox."""
    # sandbox.py is in the same directory as app_runner.py
    runner_dir = Path(__file__).parent
    sandbox_path = runner_dir / "sandbox.py"

    if sandbox_path.exists():
        spec = importlib.util.spec_from_file_location("sandbox", sandbox_path)
        sandbox = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sandbox)
        sandbox.activate()


def load_app_module(app_path: Path):
    """Load main.py of the app."""
    main_py = app_path / "main.py"

    if not main_py.exists():
        print(f"ERROR: {main_py} not found", file=sys.stderr)
        sys.exit(1)

    spec = importlib.util.spec_from_file_location("main", main_py)
    module = importlib.util.module_from_spec(spec)

    # Add app directory to sys.path
    sys.path.insert(0, str(app_path))

    spec.loader.exec_module(module)
    return module


def main() -> int:
    """Main function of the App Runner."""
    if len(sys.argv) < 2:
        print("Usage: app_runner.py <app_path> [args...]", file=sys.stderr)
        return 1

    app_path = Path(sys.argv[1]).resolve()
    app_args = sys.argv[2:]

    # Activate sandbox (security)
    activate_sandbox()

    # Load app module
    module = load_app_module(app_path)

    # Create parser and register arguments
    parser = argparse.ArgumentParser(
        prog=app_path.name,
        description=getattr(module, "__doc__", None)
    )

    if hasattr(module, "register"):
        module.register(parser)

    # Parse arguments
    args = parser.parse_args(app_args)

    # Execute app
    if hasattr(module, "run"):
        result = module.run(args)
        return result if isinstance(result, int) else 0
    else:
        print(f"ERROR: App '{app_path.name}' has no run() function", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
