# -*- coding: utf-8 -*-
"""
uvpy Sandbox - Security Layer

STDLIB ONLY - no external dependencies!

Blocks:
- Network connections except localhost
- Telemetry from Streamlit, Matplotlib, etc.

Must be loaded BEFORE all other imports.
"""
import os
import socket
import sys

_original_socket_connect = None
_sandbox_active = False

# Allowed hosts (localhost variants)
ALLOWED_HOSTS = frozenset({
    "localhost",
    "127.0.0.1",
    "::1",
    "0.0.0.0",
})

# Allowed IP prefixes
ALLOWED_IP_PREFIXES = (
    "127.",
    "::1",
    "0.0.0.0",
)


def _is_allowed_host(host: str) -> bool:
    """Check if a host is allowed."""
    if not host:
        return True

    host_lower = str(host).lower().strip()

    if host_lower in ALLOWED_HOSTS:
        return True

    for prefix in ALLOWED_IP_PREFIXES:
        if host_lower.startswith(prefix):
            return True

    return False


def _restricted_connect(self, address):
    """Replace socket.connect() with localhost restriction."""
    host = None

    if isinstance(address, tuple) and len(address) >= 1:
        host = address[0]
    elif isinstance(address, str):
        host = address

    if not _is_allowed_host(host):
        raise PermissionError(
            f"[uvpy Sandbox] Network access blocked: {host}\n"
            f"Only localhost connections are allowed."
        )

    return _original_socket_connect(self, address)


def _set_env_defaults() -> None:
    """
    Set environment variables BEFORE importing packages.

    These variables prevent:
    - Telemetry/Analytics
    - GUI backends that require X11
    - Auto-updates
    """
    env_vars = {
        # Matplotlib: Headless backend (no X11 required)
        "MPLBACKEND": "Agg",

        # Streamlit: No telemetry
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
        "STREAMLIT_SERVER_ENABLE_STATIC_SERVING": "false",
        "STREAMLIT_GLOBAL_DEVELOPMENT_MODE": "false",

        # Plotly: No external rendering
        "PLOTLY_RENDERER": "png",

        # Jupyter: Standard directories
        "JUPYTER_PLATFORM_DIRS": "1",

        # No auto-updates
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "NO_UPDATE_NOTIFIER": "1",

        # No proxy (prevents data leak)
        "no_proxy": "*",
        "NO_PROXY": "*",

        # Disable Sentry
        "SENTRY_DSN": "",
        "SENTRY_ENVIRONMENT": "",

        # Disable Google Analytics
        "GOOGLE_ANALYTICS_TRACKING_ID": "",

        # Tkinter: No GUI errors on headless
        "TK_SILENCE_DEPRECATION": "1",
    }

    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value


def _patch_urllib() -> None:
    """Patch urllib.request.urlopen (stdlib, always available)."""
    try:
        import urllib.request
        from urllib.parse import urlparse

        _original = urllib.request.urlopen

        def _restricted(url, *args, **kwargs):
            url_str = str(url.full_url if hasattr(url, 'full_url') else url)
            parsed = urlparse(url_str)
            host = parsed.hostname or ""

            if not _is_allowed_host(host):
                raise PermissionError(
                    f"[uvpy Sandbox] URL access blocked: {url_str}\n"
                    f"Only localhost URLs are allowed."
                )

            return _original(url, *args, **kwargs)

        urllib.request.urlopen = _restricted
    except Exception:
        pass


def _patch_imported_http_libs() -> None:
    """
    Patch HTTP libraries ONLY if they are already imported.
    Does NOT import them (would force dependencies).
    """
    # requests (only if already imported)
    if "requests" in sys.modules:
        try:
            from urllib.parse import urlparse
            requests = sys.modules["requests"]
            _original = requests.Session.request

            def _restricted(self, method, url, *args, **kwargs):
                parsed = urlparse(str(url))
                if not _is_allowed_host(parsed.hostname or ""):
                    raise PermissionError(
                        f"[uvpy Sandbox] HTTP access blocked: {url}"
                    )
                return _original(self, method, url, *args, **kwargs)

            requests.Session.request = _restricted
        except Exception:
            pass

    # httpx (only if already imported)
    if "httpx" in sys.modules:
        try:
            from urllib.parse import urlparse
            httpx = sys.modules["httpx"]
            _original = httpx.Client.request

            def _restricted(self, method, url, *args, **kwargs):
                parsed = urlparse(str(url))
                if not _is_allowed_host(parsed.hostname or ""):
                    raise PermissionError(
                        f"[uvpy Sandbox] HTTP access blocked: {url}"
                    )
                return _original(self, method, url, *args, **kwargs)

            httpx.Client.request = _restricted
        except Exception:
            pass


def _install_import_hook() -> None:
    """
    Install an import hook that patches HTTP libraries
    as soon as they are imported.
    """
    class SandboxImportHook:
        """Patches HTTP libraries on import."""

        _libs_to_patch = {"requests", "httpx"}
        _patched = set()

        def find_module(self, name, path=None):
            if name in self._libs_to_patch and name not in self._patched:
                return self
            return None

        def load_module(self, name):
            # Remove ourselves temporarily to avoid recursion
            if self in sys.meta_path:
                sys.meta_path.remove(self)

            try:
                # Normal import
                import importlib
                module = importlib.import_module(name)

                # Now patch
                self._patched.add(name)
                _patch_imported_http_libs()

                return module
            finally:
                # Re-add hook
                if self not in sys.meta_path:
                    sys.meta_path.insert(0, self)

    # Install hook only once
    for hook in sys.meta_path:
        if isinstance(hook, SandboxImportHook):
            return

    sys.meta_path.insert(0, SandboxImportHook())


def activate() -> None:
    """Activate all sandbox restrictions."""
    global _original_socket_connect, _sandbox_active

    if _sandbox_active:
        return

    # 1. Set environment variables (BEFORE all imports!)
    _set_env_defaults()

    # 2. Restrict socket connections
    _original_socket_connect = socket.socket.connect
    socket.socket.connect = _restricted_connect

    # 3. Patch urllib (stdlib, always available)
    _patch_urllib()

    # 4. Install import hook for requests/httpx
    _install_import_hook()

    # 5. If already imported, patch now
    _patch_imported_http_libs()

    _sandbox_active = True


def deactivate() -> None:
    """Deactivate the sandbox (for tests)."""
    global _original_socket_connect, _sandbox_active

    if not _sandbox_active:
        return

    if _original_socket_connect:
        socket.socket.connect = _original_socket_connect

    _sandbox_active = False


def is_active() -> bool:
    """Return whether the sandbox is active."""
    return _sandbox_active
