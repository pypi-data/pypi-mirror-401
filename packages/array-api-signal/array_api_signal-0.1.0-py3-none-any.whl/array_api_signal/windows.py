"""
Window functions for signal processing.

This module provides backend-agnostic implementations of common window functions,
designed to be compatible with the Python Array API Standard. These functions
mimic the behavior of `scipy.signal.windows` but operate directly on the
array backend specified (e.g., NumPy, PyTorch, CuPy).
"""

from types import ModuleType
from typing import Any, Optional, Tuple

# Type alias for clarity
Array = Any


def _get_xp(device: Optional[Any] = None, xp: Optional[ModuleType] = None) -> Any:
    """
    Helper to determine the appropriate array namespace (backend).

    This function attempts to infer the backend based on the provided `device`
    argument or uses the explicitly provided `xp` module.

    Args:
        device: The device object or string specifier.
        xp: Explicit backend module (optional). Prioritized if provided.

    Returns:
        The array namespace module (e.g., `numpy` or `torch`).
    """
    # 0. Explicit Injection (From Wrapper)
    if xp is not None:
        return xp

    # 1. Device Inference
    if device is not None:
        # Check if it is a torch.device object (or similar backend object)
        t = type(device)
        if "torch" in t.__module__:
            import torch

            return torch

        # Check string heuristics for GPU devices
        s = str(device)
        if "cuda" in s or "mps" in s or "xpu" in s:
            import torch

            return torch

    # Default to NumPy for 'cpu' string or None
    import numpy

    return numpy


def _calc_n(M: int, sym: bool, xp: Any, dtype: Any, device: Any) -> Tuple[Array, int]:
    """
    Helper to calculate the domain 'n' and normalization factor 'L'.

    Args:
        M: Number of points in the output window.
        sym: Whether to generate a symmetric window.
        xp: The array namespace to use.
        dtype: The data type of the returned array.
        device: The device on which to place the returned array.

    Returns:
        A tuple containing:
            - n: The domain array [0, 1, ..., M-1].
            - L: The normalization factor (M if periodic, M-1 if symmetric).
    """
    if M < 1:
        return xp.array([], dtype=dtype, device=device), 0

    if M == 1:
        # For M=1, n is [0], but many window formulas divide by L.
        # If sym=True, L=M-1=0, leading to division by zero.
        # Handled by caller or specific window logic, but basic return is here.
        return xp.ones((1,), dtype=dtype, device=device), 0

    n = xp.arange(0, M, dtype=dtype, device=device)

    if sym:
        L = M - 1
    else:
        L = M

    return n, L


def hann(
    M: int,
    sym: bool = True,
    dtype: Optional[Any] = None,
    device: Optional[Any] = None,
    xp: Optional[ModuleType] = None,
) -> Array:
    """
    Return a Hann window.

    The Hann window is a taper formed by using a raised cosine or sine-squared
    with ends that touch zero.

    Args:
        M: Number of points in the output window. If zero or less, an empty
            array is returned.
        sym: When True (default), generates a symmetric window, for use in filter
            design. When False, generates a periodic window, for use in spectral
            analysis.
        dtype: The data type of the returned array.
        device: The device on which to place the returned array.
        xp: Explicit array backend to use (mostly for internal use by the wrapper).

    Returns:
        The window, with the maximum value normalized to 1 (though the value 1
        does not appear if `M` is even and `sym` is True).
    """
    xp = _get_xp(device, xp=xp)

    if M < 1:
        return xp.empty(0, dtype=dtype, device=device)
    if M == 1:
        return xp.ones(1, dtype=dtype, device=device)

    n, L = _calc_n(M, sym, xp, dtype, device)

    # Use explicit pi to match backend precision if possible
    pi = 3.141592653589793

    return 0.5 - 0.5 * xp.cos(2 * pi * n / L)


def hamming(
    M: int,
    sym: bool = True,
    dtype: Optional[Any] = None,
    device: Optional[Any] = None,
    xp: Optional[ModuleType] = None,
) -> Array:
    """
    Return a Hamming window.

    The Hamming window is a taper formed by using a raised cosine with
    non-zero endpoints, optimized to minimize the nearest side lobe.

    Args:
        M: Number of points in the output window. If zero or less, an empty
            array is returned.
        sym: When True (default), generates a symmetric window, for use in filter
            design. When False, generates a periodic window, for use in spectral
            analysis.
        dtype: The data type of the returned array.
        device: The device on which to place the returned array.
        xp: Explicit array backend to use.

    Returns:
        The window, with the maximum value normalized to 1.
    """
    xp = _get_xp(device, xp=xp)

    if M < 1:
        return xp.empty(0, dtype=dtype, device=device)
    if M == 1:
        return xp.ones(1, dtype=dtype, device=device)

    n, L = _calc_n(M, sym, xp, dtype, device)

    pi = 3.141592653589793

    # Coefficients matching scipy.signal.windows.hamming
    alpha = 0.54
    beta = 1 - alpha

    return alpha - beta * xp.cos(2 * pi * n / L)


def tukey(
    M: int,
    alpha: float = 0.5,
    sym: bool = True,
    dtype: Optional[Any] = None,
    device: Optional[Any] = None,
    xp: Optional[ModuleType] = None,
) -> Array:
    """
    Return a Tukey window, also known as a tapered cosine window.

    Args:
        M: Number of points in the output window. If zero or less, an empty
            array is returned.
        alpha: Shape parameter of the Tukey window, representing the fraction of the
            window inside the cosine tapered region.
            If zero, the Tukey window is equivalent to a rectangular window.
            If one, the Tukey window is equivalent to a Hann window.
        sym: When True (default), generates a symmetric window, for use in filter
            design. When False, generates a periodic window, for use in spectral
            analysis.
        dtype: The data type of the returned array.
        device: The device on which to place the returned array.
        xp: Explicit array backend to use.

    Returns:
        The window, with the maximum value normalized to 1.
    """
    xp = _get_xp(device, xp=xp)

    if M < 1:
        return xp.empty(0, dtype=dtype, device=device)

    # Special cases for alpha
    if alpha <= 0:
        return xp.ones(M, dtype=dtype, device=device)
    if alpha >= 1:
        return hann(M, sym=sym, dtype=dtype, device=device, xp=xp)

    n, L = _calc_n(M, sym, xp, dtype, device)
    if L == 0:
        # Case M=1, sym=True handled here to return 1.0
        return xp.ones(1, dtype=dtype, device=device)

    width = (alpha * L) / 2.0
    pi = 3.141592653589793

    # Region 1: Taper up (Left)
    # 0 <= n < width
    r1 = n < width

    # Region 3: Taper down (Right)
    # (L - width) < n <= L
    r3 = n > (L - width)

    # Initialize with 1.0 (Region 2: Flat top)
    w = xp.ones(M, dtype=dtype, device=device)

    def taper(pts: Array) -> Array:
        """Calculate the cosine taper values."""
        val = (pts / width) - 1
        return 0.5 * (1 + xp.cos(pi * val))

    # Apply tapers using 'where' for pure functional masking
    w = xp.where(r1, taper(n), w)
    w = xp.where(r3, taper(L - n), w)

    return w
