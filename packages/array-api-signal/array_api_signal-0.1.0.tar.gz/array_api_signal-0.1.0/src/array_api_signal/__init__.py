"""
array-api-signal
================

Signal processing primitives (windows, filters, integration) for the Python Array API Standard.
"""

from array_api_compat import array_namespace as _compat_get_ns
from array_api_signal.wrapper import SignalNamespace

# -----------------------------------------------------------------------------
# 1. Re-export extensions for direct access (xp.simpson)
# -----------------------------------------------------------------------------
from array_api_extra import *
from array_api_signal.integral import simpson, trapezoid
from array_api_signal.signal import gaussian_filter1d, convolve
from array_api_signal.windows import hann, hamming, tukey


# -----------------------------------------------------------------------------
# 2. Unified Namespace Factory
# -----------------------------------------------------------------------------
def array_namespace(*arrays) -> SignalNamespace:
    """
    Return a unified Array API namespace object for the input arrays.

    The returned object ('xp') behaves like the underlying backend (e.g., NumPy, Torch),
    but includes all 'array-api-signal' extensions (simpson, hann, pad, etc.).

    Usage:
        >>> import array_api_signal as aps
        >>> x = torch.ones(5)
        >>> xp = aps.array_namespace(x)
        >>> xp.sin(x)       # Calls torch.sin
        >>> xp.simpson(x)   # Calls array_api_signal.simpson
        >>> xp.hann(10)     # Returns torch tensor (inferred context)
    """
    if not arrays:
        # Default to NumPy if no context provided (standard behavior)
        import numpy

        return SignalNamespace(numpy)

    backend = _compat_get_ns(*arrays)
    return SignalNamespace(backend)


def get_namespace(*arrays) -> SignalNamespace:
    """Alias for array_namespace."""
    return array_namespace(*arrays)


# -----------------------------------------------------------------------------
# 3. Dynamic Dispatch for Top-Level Module Usage
# -----------------------------------------------------------------------------
from array_api_compat import array_namespace as _get_ns


def __getattr__(name):
    return _make_dispatcher(name)


def _make_dispatcher(name):
    def wrapper(x, *args, **kwargs):
        xp = _get_ns(x)
        if hasattr(xp, name):
            return getattr(xp, name)(x, *args, **kwargs)
        raise AttributeError(f"The backend '{xp.__name__}' has no attribute '{name}'")

    return wrapper
