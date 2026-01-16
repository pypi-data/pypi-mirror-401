"""
Signal processing filters and convolution tools.

This module provides backend-agnostic implementations of common signal processing
operations, such as Gaussian filtering and convolution. It employs a hybrid
dispatch strategy:

1.  Dispatches to `scipy.ndimage` for NumPy arrays (CPU optimization).
2.  Dispatches to `torch.nn.functional` for PyTorch tensors (GPU optimization).
3.  Falls back to FFT-based convolution for generic Array API backends (JAX, CuPy).
"""

import math
from typing import Optional, Any, Literal
import array_api_compat
from array_api_compat import is_torch_namespace, is_numpy_namespace
import array_api_extra as xpx

# Type alias for clarity
Array = Any


def gaussian_filter1d(
    input: Array,
    sigma: float,
    axis: int = -1,
    mode: Literal["reflect", "constant", "nearest", "mirror", "wrap"] = "reflect",
    cval: float = 0.0,
    truncate: float = 4.0,
) -> Array:
    """
    One-dimensional Gaussian filter.

    Args:
        input: Input array.
        sigma: Standard deviation for Gaussian kernel.
        axis: The axis of `input` along which to calculate. Default is -1.
        mode: The `array_api_extra.pad` mode parameter ('reflect', 'constant', etc.).
        cval: Value to fill past edges of input if `mode` is 'constant'.
        truncate: Truncate the filter at this many standard deviations. Default is 4.0.

    Returns:
        The smoothed array.
    """
    xp = array_api_compat.array_namespace(input)

    # -------------------------------------------------------------------------
    # 1. NumPy Optimization (CPU)
    # -------------------------------------------------------------------------
    # If we are on CPU/NumPy, rely on SciPy for speed/correctness if available.
    if is_numpy_namespace(xp):
        try:
            from scipy.ndimage import gaussian_filter1d as _scipy_gauss

            return _scipy_gauss(
                input, sigma, axis=axis, mode=mode, cval=cval, truncate=truncate
            )
        except ImportError:
            pass  # Fallback to generic implementation

    # -------------------------------------------------------------------------
    # 2. Kernel Generation (Generic)
    # -------------------------------------------------------------------------
    # Calculate radius of the kernel
    radius = int(truncate * sigma + 0.5)

    # Create the generic 1D kernel
    # x ranges from -radius to radius
    x_range = xp.arange(-radius, radius + 1, dtype=input.dtype, device=input.device)
    phi_x = xp.exp(-0.5 * (x_range / sigma) ** 2)
    phi_x = phi_x / xp.sum(phi_x)  # Normalize

    # -------------------------------------------------------------------------
    # 3. PyTorch Optimization (GPU)
    # -------------------------------------------------------------------------
    if is_torch_namespace(xp):
        import torch.nn.functional as F

        # Torch conv1d expects (Batch, Channel, Length).
        # We need to reshape input to match this, then reshape back.

        # 1. Move target axis to the end
        if axis != -1 and axis != input.ndim - 1:
            input_perm = xp.moveaxis(input, axis, -1)
        else:
            input_perm = input

        # 2. Flatten other dimensions into "Batch"
        original_shape = input_perm.shape
        L = original_shape[-1]
        input_reshaped = input_perm.reshape(-1, 1, L)  # (N, 1, L)

        # 3. Prepare Kernel (OutChan, InChan/Groups, K) -> (1, 1, K)
        kernel = phi_x.reshape(1, 1, -1)

        # 4. Pad
        # Torch padding is (Left, Right, Top, Bottom...).
        # xpx.pad uses ((before, after), ...) tuple.
        # We map xpx modes to torch modes where possible.
        torch_mode = mode
        if mode == "mirror":
            torch_mode = "reflect"  # Torch doesn't strictly distinguish
        if mode == "wrap":
            torch_mode = "circular"

        # Manual padding because conv1d 'padding' arg only supports zeros/valid.
        # We leverage F.pad for complex modes.
        input_padded = F.pad(
            input_reshaped, (radius, radius), mode=torch_mode, value=cval
        )

        # 5. Convolve
        out = F.conv1d(input_padded, kernel)

        # 6. Reshape back
        out = out.reshape(original_shape)
        if axis != -1 and axis != input.ndim - 1:
            out = xp.moveaxis(out, -1, axis)

        return out

    # -------------------------------------------------------------------------
    # 4. Generic Implementation (FFT or Direct)
    # -------------------------------------------------------------------------
    # Fallback for generic backends (JAX, Dask, etc.)
    # We use a simple convolution approach: Pad -> Dot Product windowing

    return convolve(input, phi_x, axis=axis, mode=mode, cval=cval)


def convolve(
    in1: Array, in2: Array, axis: int = -1, mode: str = "reflect", cval: float = 0.0
) -> Array:
    """
    Convolve `in1` with a 1D kernel `in2` along `axis`.

    This implementation relies on FFT-based convolution, which is efficient for
    large kernels on accelerators (GPUs). It performs a 'same' convolution,
    centering the result.

    Args:
        in1: Input signal array.
        in2: 1D Kernel array.
        axis: The axis along which to convolve.
        mode: The padding mode ('reflect', 'constant', etc.).
        cval: Fill value if `mode` is 'constant'.

    Returns:
        The result of the convolution, with the same shape as `in1`.

    Raises:
        ValueError: If `in2` is not 1D.
        NotImplementedError: If the backend does not support FFT operations.
    """
    xp = array_api_compat.array_namespace(in1)

    # Normalize Kernel (ensure 1D)
    if in2.ndim != 1:
        raise ValueError("Kernel 'in2' must be 1D")

    kernel_len = in2.shape[0]
    radius = kernel_len // 2

    # Move axis to end
    if axis != -1:
        in1 = xp.moveaxis(in1, axis, -1)

    # Pad Input
    # We use array-api-extra for backend-agnostic padding
    # Pad tuple: ((0,0), ... (radius, radius))
    pads = [(0, 0)] * in1.ndim
    pads[-1] = (radius, radius)

    padded = xpx.pad(in1, tuple(pads), mode=mode, constant_values=cval)

    # --- FFT Convolution Implementation ---
    # This is generally robust for larger kernels on accelerators

    # 1. Check for FFT support in namespace
    if not hasattr(xp, "fft"):
        raise NotImplementedError(f"Backend {xp.__name__} does not expose xp.fft")

    # 2. Compute FFT size (Linear convolution size)
    # Standard "fft convolution" logic: FFT size >= L + K - 1
    sz = in1.shape[-1] + kernel_len - 1

    # FFT
    # Note: broadcasting in2 (kernel) against in1
    # in1: (..., Time), in2: (Time) -> Needs broadcasting

    X = xp.fft.rfft(in1, n=sz, axis=-1)
    K = xp.fft.rfft(in2, n=sz, axis=-1)

    # Multiply (Broadcasting automatically handles batch dims of X)
    Y = X * K

    # IFFT
    out_full = xp.fft.irfft(Y, n=sz, axis=-1)

    # Crop to 'same' size (centered)
    start = (kernel_len - 1) // 2
    out = out_full[..., start : start + in1.shape[-1]]

    # Restore Axis
    if axis != -1:
        out = xp.moveaxis(out, -1, axis)

    return out
