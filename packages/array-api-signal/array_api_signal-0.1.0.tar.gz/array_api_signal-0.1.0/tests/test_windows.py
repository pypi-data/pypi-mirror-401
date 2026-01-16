import pytest
import numpy as np
import array_api_compat
from array_api_signal import windows as W

# Optional Scipy for ground truth
try:
    from scipy import signal

    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
def get_backends():
    # Numpy (CPU)
    yield pytest.param(("numpy", np, "cpu"), id="numpy")

    # Torch (CPU/GPU)
    try:
        import torch

        yield pytest.param(("torch", torch, "cpu"), id="torch-cpu")
        if torch.cuda.is_available():
            yield pytest.param(("torch", torch, "cuda"), id="torch-cuda")
    except ImportError:
        pass


@pytest.fixture(params=get_backends())
def backend_data(request):
    return request.param


def to_cpu(data):
    return array_api_compat.to_device(data, "cpu")


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


class TestWindows:

    @pytest.mark.skipif(not HAVE_SCIPY, reason="Scipy required for verification")
    def test_hann_matches_scipy(self, backend_data):
        name, xp, device = backend_data
        M = 51

        # NOTE: For 'torch-cpu', the fixture device is string 'cpu'.
        # If we pass just 'cpu', W.hann defaults to Numpy.
        # For this test, verifying values against SciPy using Numpy backend is fine/safe
        # because the math is backend-agnostic.
        # But if we strictly want to test the backend logic, we rely on 'device' handling below.

        # We pass the device string; if 'cpu' it might return numpy array
        # but values should still match.
        res_sym = W.hann(M, sym=True, device=device)
        ref_sym = signal.windows.hann(M, sym=True)
        np.testing.assert_allclose(to_cpu(res_sym), ref_sym, atol=1e-6)

        # Test Periodic
        res_per = W.hann(M, sym=False, device=device)
        ref_per = signal.windows.hann(M, sym=False)
        np.testing.assert_allclose(to_cpu(res_per), ref_per, atol=1e-6)

    @pytest.mark.skipif(not HAVE_SCIPY, reason="Scipy required for verification")
    def test_hamming_matches_scipy(self, backend_data):
        name, xp, device = backend_data
        M = 51

        res = W.hamming(M, sym=True, device=device)
        ref = signal.windows.hamming(M, sym=True)

        np.testing.assert_allclose(to_cpu(res), ref, atol=1e-6)

    @pytest.mark.skipif(not HAVE_SCIPY, reason="Scipy required for verification")
    @pytest.mark.parametrize("alpha", [0.25, 0.5, 0.75])
    def test_tukey_matches_scipy(self, backend_data, alpha):
        name, xp, device = backend_data
        M = 100

        res = W.tukey(M, alpha=alpha, sym=True, device=device)
        ref = signal.windows.tukey(M, alpha=alpha, sym=True)

        np.testing.assert_allclose(to_cpu(res), ref, atol=1e-6)

    def test_tukey_edge_cases(self, backend_data):
        """Test alpha=0 (Rect) and alpha=1 (Hann)"""
        name, xp, device = backend_data
        M = 20

        # Alpha=0 -> Ones
        res_0 = W.tukey(M, alpha=0.0, device=device)
        np.testing.assert_allclose(to_cpu(res_0), np.ones(M))

        # Alpha=1 -> Hann
        res_1 = W.tukey(M, alpha=1.0, device=device)
        res_hann = W.hann(M, device=device)
        np.testing.assert_allclose(to_cpu(res_1), to_cpu(res_hann))

    def test_device_placement(self, backend_data):
        """Ensure the returned array is on the requested device."""
        name, xp, device = backend_data

        # This is primarily for Torch
        if name == "torch":
            import torch

            # Pass a real torch.device object to force Torch backend
            # (Passing string 'cpu' defaults to Numpy, which is intended behavior)
            dev_obj = torch.device(device)
            res = W.hann(10, device=dev_obj)

            assert isinstance(res, torch.Tensor)

            # Check device string match
            if "cuda" in str(device):
                assert res.is_cuda
            else:
                assert not res.is_cuda
