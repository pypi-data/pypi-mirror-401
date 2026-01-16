import pytest
import numpy as np
import array_api_compat
from array_api_signal import signal as S
from scipy import ndimage


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------
def get_backends():
    yield pytest.param(("numpy", np, "cpu"), id="numpy")
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


def to_device(data, xp, device):
    if xp.__name__ == "torch":
        import torch

        return torch.as_tensor(data, device=device)
    return xp.asarray(data)


def to_cpu(data):
    """Convert any backend array to numpy cpu."""
    return array_api_compat.to_device(data, "cpu")


# -----------------------------------------------------------------------------
# Test Class: Gaussian Filter
# -----------------------------------------------------------------------------
class TestGaussianFilter:

    def test_matches_scipy_1d(self, backend_data):
        """Verify 1D Gaussian matches scipy.ndimage.gaussian_filter1d."""
        name, xp, device = backend_data

        # Impulse signal
        x_cpu = np.zeros(50)
        x_cpu[25] = 1.0

        x = to_device(x_cpu, xp, device)
        sigma = 2.0

        # Run Ours
        res = S.gaussian_filter1d(x, sigma=sigma, mode="constant", cval=0.0)

        # Run Scipy
        ref = ndimage.gaussian_filter1d(x_cpu, sigma=sigma, mode="constant", cval=0.0)

        # Compare
        res_np = to_cpu(res)
        np.testing.assert_allclose(res_np, ref, atol=1e-5)

    def test_multi_channel_axis(self, backend_data):
        """Ensure axis argument works correctly for batch processing."""
        name, xp, device = backend_data

        # Shape: (Batch=3, Time=20)
        x_cpu = np.random.randn(3, 20)
        x = to_device(x_cpu, xp, device)

        # Filter along time (axis 1)
        res = S.gaussian_filter1d(x, sigma=1.0, axis=1)

        assert res.shape == (3, 20)

        # Sanity check: Signals should be smoother (lower variance of diff)
        diff_raw = xp.std(xp.diff(x, axis=1))
        diff_smooth = xp.std(xp.diff(res, axis=1))

        # Cast to python float for assertion
        assert float(diff_smooth) < float(diff_raw)

    def test_gradients_torch(self):
        """Specific test for PyTorch to ensure gradients flow through."""
        try:
            import torch
        except ImportError:
            pytest.skip("Torch not installed")

        x = torch.randn(1, 100, requires_grad=True)
        res = S.gaussian_filter1d(x, sigma=2.0)

        loss = res.sum()
        loss.backward()

        assert x.grad is not None
        assert torch.any(x.grad != 0)

    def test_mode_reflect(self, backend_data):
        """Test default reflection padding."""
        name, xp, device = backend_data

        # Step function
        # NOTE: Length must be > padding radius (4*sigma) for Torch reflect
        # sigma=5.0 -> radius=20. So length must be > 20.
        x_cpu = np.ones(50)
        x = to_device(x_cpu, xp, device)

        # With reflection, boundaries should remain roughly stable
        res = S.gaussian_filter1d(x, sigma=5.0, mode="reflect")

        res_np = to_cpu(res)
        # Should be very close to 1.0 everywhere
        np.testing.assert_allclose(res_np, 1.0, atol=1e-3)
