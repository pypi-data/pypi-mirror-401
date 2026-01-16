"""
Namespace wrapper to provide a unified 'xp' object.

This module defines the `SignalNamespace` proxy, which intercepts attributes
to prioritize local signal extensions (integral, windows, etc.) before falling
back to `array-api-extra` and finally the underlying backend.
"""

from types import ModuleType
from typing import Any
import array_api_extra

# Local extensions
from array_api_signal import integral, signal, windows

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# Register modules here to expose them in the unified namespace.
# Order matters: earlier modules take precedence if names collide.
SIGNAL_MODULES = (
    integral,
    signal,
    windows,
)


class SignalNamespace:
    """
    A wrapper around a standard Array API backend (numpy, torch, etc.) that
    augments it with signal processing and extra capabilities.

    This object behaves like the backend module itself, but with extra methods
    injected from `array-api-signal` and `array-api-extra`.
    """

    def __init__(self, backend: ModuleType):
        self._backend = backend
        self.__name__ = backend.__name__

    def __getattr__(self, name: str) -> Any:
        # ---------------------------------------------------------------------
        # 1. Check Local Signal Extensions (Iterative Dispatch)
        # ---------------------------------------------------------------------
        for mod in SIGNAL_MODULES:
            if hasattr(mod, name):
                attr = getattr(mod, name)

                # Special handling: Window functions (hann, tukey) need context.
                # If we found it in _windows, wrap it to inject the backend.
                if mod == windows:
                    return self._wrap_window_func(attr)

                return attr

        # ---------------------------------------------------------------------
        # 2. Check array-api-extra
        # ---------------------------------------------------------------------
        if hasattr(array_api_extra, name):
            return getattr(array_api_extra, name)

        # ---------------------------------------------------------------------
        # 3. Fallback to the underlying backend (sin, cos, matmul)
        # ---------------------------------------------------------------------
        return getattr(self._backend, name)

    def _wrap_window_func(self, func):
        """
        Wraps window functions (hann, tukey) to default to the current backend.

        If the user calls `xp.hann(10)` without a device, this wrapper injects
        `xp=self._backend` into the kwargs so `_windows.py` knows where to
        create the array.
        """

        def wrapper(*args, **kwargs):
            # If 'device' or 'xp' is not passed, inject our backend context.
            if "device" not in kwargs and "xp" not in kwargs:
                kwargs["xp"] = self._backend

            return func(*args, **kwargs)

        return wrapper

    def __repr__(self):
        return f"<SignalNamespace wrapping '{self._backend.__name__}'>"
