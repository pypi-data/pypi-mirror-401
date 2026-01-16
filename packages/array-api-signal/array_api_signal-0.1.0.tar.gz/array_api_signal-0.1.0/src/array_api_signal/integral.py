"""
Integration routines for the Array API Standard.

This module provides backend-agnostic implementations of common integration
methods (Trapezoidal, Simpson's), dispatching to native optimizations
(Torch, NumPy) where available.
"""

from typing import Optional, Any
import array_api_compat
from array_api_compat import is_torch_namespace, is_numpy_namespace

# Type alias for clarity, though technically it's just 'object' in the Array API
Array = Any


def trapezoid(
    y: Array, x: Optional[Array] = None, dx: float = 1.0, axis: int = -1
) -> Array:
    """
    Integrate along the given axis using the composite trapezoidal rule.

    Parameters
    ----------
    y : array
        Input array to integrate.
    x : array, optional
        The sample points corresponding to the `y` values. If ``None``, the
        sample points are assumed to be evenly spaced `dx` apart. The default
        is ``None``.
    dx : float, optional
        The spacing between sample points when `x` is ``None``. The default is 1.0.
    axis : int, optional
        The axis along which to integrate. The default is -1 (the last axis).

    Returns
    -------
    out : array
        Definite integral as approximated by the trapezoidal rule.
    """
    xp = array_api_compat.array_namespace(y)

    # -------------------------------------------------------------------------
    # 1. Torch Dispatch (Native Optimization)
    # -------------------------------------------------------------------------
    if is_torch_namespace(xp):
        import torch

        if x is not None:
            return torch.trapezoid(y, x, dim=axis)
        return torch.trapezoid(y, dx=dx, dim=axis)

    # -------------------------------------------------------------------------
    # 2. NumPy Dispatch (Optimization & Version Compatibility)
    # -------------------------------------------------------------------------
    if is_numpy_namespace(xp):
        # NumPy 2.0+ uses 'trapezoid'
        if hasattr(xp, "trapezoid"):
            return xp.trapezoid(y, x=x, dx=dx, axis=axis)
        # NumPy 1.x uses 'trapz'
        elif hasattr(xp, "trapz"):
            return xp.trapz(y, x=x, dx=dx, axis=axis)

    # -------------------------------------------------------------------------
    # 3. Standard API Dispatch
    # -------------------------------------------------------------------------
    # Generic catch-all for any other backend (e.g., Dask, CuPy) that happens
    # to implement the standard 2.0+ 'trapezoid' method.
    if hasattr(xp, "trapezoid"):
        return xp.trapezoid(y, x=x, dx=dx, axis=axis)

    # -------------------------------------------------------------------------
    # 4. Fallback Implementation (Pure Array API)
    # -------------------------------------------------------------------------
    # Ensure axis is at the end for consistent slicing logic
    if axis != -1:
        y = xp.moveaxis(y, axis, -1)
        if x is not None:
            x = xp.moveaxis(x, axis, -1)

    if x is None:
        # Uniform spacing formula: dx * (sum(y) - 0.5 * (y_first + y_last))
        # This is numerically stable and avoids slicing internal points.
        total_sum = xp.sum(y, axis=-1)
        edges = 0.5 * (y[..., 0] + y[..., -1])
        return dx * (total_sum - edges)
    else:
        # Non-uniform spacing formula: 0.5 * sum((y_i + y_{i-1}) * (x_i - x_{i-1}))
        d_x = xp.diff(x, axis=-1)
        y_avg = 0.5 * (y[..., 1:] + y[..., :-1])
        return xp.sum(y_avg * d_x, axis=-1)


def simpson(
    y: Array, x: Optional[Array] = None, dx: float = 1.0, axis: int = -1
) -> Array:
    """
    Integrate along the given axis using the composite Simpson's rule.

    If the number of samples is even, the last interval is integrated using the
    trapezoidal rule. This matches the behavior of ``scipy.integrate.simpson``
    with ``even='last'``.

    Parameters
    ----------
    y : array
        Input array to integrate.
    x : array, optional
        The sample points corresponding to the `y` values. If ``None``, the
        sample points are assumed to be evenly spaced `dx` apart.

        **Note:** If `x` is provided (non-uniform sampling), this function
        currently falls back to the Trapezoidal rule for robustness, as
        non-uniform Simpson's rule requires complex weighting logic.
    dx : float, optional
        The spacing between sample points when `x` is ``None``. The default is 1.0.
    axis : int, optional
        The axis along which to integrate. The default is -1.

    Returns
    -------
    out : array
        The estimated integral.
    """
    xp = array_api_compat.array_namespace(y)

    # Move target axis to -1 for consistent slicing
    if axis != -1:
        y = xp.moveaxis(y, axis, -1)
        if x is not None:
            x = xp.moveaxis(x, axis, -1)

    n_samples = y.shape[-1]

    # Edge Case: Not enough samples for Simpson's rule (requires 3+)
    if n_samples < 3:
        return trapezoid(y, x=x, dx=dx, axis=-1)

    # -------------------------------------------------------------------------
    # CASE 1: Odd number of samples (Exact Simpson's Rule)
    # -------------------------------------------------------------------------
    if n_samples % 2 == 1:
        if x is None:
            # Formula: dx/3 * (y[0] + y[-1] + 4*sum(odd_indices) + 2*sum(even_indices))
            # Indices: 0, 1, 2, 3, 4 ...
            # Edges:   0, -1
            # Odd (4x): 1, 3, 5 ... (slice 1::2)
            # Even (2x): 2, 4, 6 ... (slice 2:-1:2)

            s = y[..., 0] + y[..., -1]
            s += 4.0 * xp.sum(y[..., 1::2], axis=-1)
            s += 2.0 * xp.sum(y[..., 2:-1:2], axis=-1)
            return s * (dx / 3.0)
        else:
            # Fallback: Non-uniform Simpson's rule is computationally heavy to
            # vectorize efficiently across all backends. We fall back to
            # trapezoid for robustness.
            return trapezoid(y, x=x, axis=-1)

    # -------------------------------------------------------------------------
    # CASE 2: Even number of samples (Simpson + Last Interval Trapz)
    # -------------------------------------------------------------------------
    else:
        # 1. Integrate 0..N-2 using Simpson (N-1 points, which is odd)
        # Note: We pass axis=-1 because we already moved the axis at the top.
        simp_val = simpson(
            y[..., :-1], x=x[..., :-1] if x is not None else None, dx=dx, axis=-1
        )

        # 2. Integrate the last interval (N-2 to N-1) using Trapezoid
        if x is not None:
            last_dx = x[..., -1] - x[..., -2]
        else:
            last_dx = dx

        trap_val = 0.5 * last_dx * (y[..., -2] + y[..., -1])

        return simp_val + trap_val
