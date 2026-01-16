import pytest
import numpy as np
from scipy import integrate
import array_api_compat
from array_api_signal import integral as F


def get_backends():
    """Yields parameters for (library_name, array_namespace, device)."""
    # 1. NumPy
    # NOTE: wrapped in extra tuple so pytest treats it as one argument 'backend_data'
    yield pytest.param(("numpy", np, "cpu"), id="numpy")

    # 2. PyTorch (if available)
    try:
        import torch

        yield pytest.param(("torch", torch, "cpu"), id="torch-cpu")
        if torch.cuda.is_available():
            yield pytest.param(("torch", torch, "cuda"), id="torch-cuda")
    except ImportError:
        pass


@pytest.fixture(params=get_backends())
def backend_data(request):
    """
    Returns (name, xp, device).
    """
    return request.param


def to_device(data, xp, device):
    """Helper to move numpy data to the target backend/device."""
    if xp.__name__ == "torch":
        import torch

        # Use simple tensor creation
        return torch.as_tensor(data, device=device)
    return xp.asarray(data)


# -----------------------------------------------------------------------------
# Test Class: Trapezoid
# -----------------------------------------------------------------------------


class TestTrapezoid:

    def test_uniform_1d(self, backend_data):
        name, xp, device = backend_data

        # y = x, Area from 0 to 10 is 50
        y_cpu = np.linspace(0, 10, 11)
        y = to_device(y_cpu, xp, device)

        res = F.trapezoid(y, dx=1.0)

        # FIX: Check attributes instead of generic is_array helper
        assert hasattr(res, "shape")
        assert hasattr(res, "dtype")

        # Check value
        assert float(res) == pytest.approx(50.0)

    def test_explicit_numpy_path(self):
        """Verify that we are indeed using numpy's implementation if available."""
        # Simple spy check if possible, or trust coverage.
        # Here we just ensure it works for older trapz vs newer trapezoid
        y = np.linspace(0, 10, 11)
        res = F.trapezoid(y, dx=1.0)
        assert res == 50.0

    def test_nonuniform_1d(self, backend_data):
        name, xp, device = backend_data

        # x = [0, 1, 3], y = [1, 1, 1]. Area = 3.0
        x_cpu = np.array([0.0, 1.0, 3.0])
        y_cpu = np.array([1.0, 1.0, 1.0])

        x = to_device(x_cpu, xp, device)
        y = to_device(y_cpu, xp, device)

        res = F.trapezoid(y, x=x)
        assert float(res) == pytest.approx(3.0)

    def test_multidim_axis(self, backend_data):
        name, xp, device = backend_data

        # Shape (2, 5). Integrate along axis 1.
        y_cpu = np.ones((2, 5))
        y = to_device(y_cpu, xp, device)

        # Width=4 -> Area=4 for each row
        res = F.trapezoid(y, dx=1.0, axis=1)

        assert res.shape == (2,)
        res_np = array_api_compat.to_device(res, "cpu")
        np.testing.assert_allclose(res_np, [4.0, 4.0])

    def test_matches_numpy_random(self, backend_data):
        name, xp, device = backend_data

        # Random data
        rng = np.random.default_rng(42)
        y_cpu = rng.random((10, 20))
        y = to_device(y_cpu, xp, device)

        my_res = F.trapezoid(y, dx=0.1, axis=-1)
        if hasattr(np, "trapezoid"):
            ref_res = np.trapezoid(y_cpu, dx=0.1, axis=-1)
        else:
            ref_res = np.trapz(y_cpu, dx=0.1, axis=-1)

        # Verify
        my_res_np = array_api_compat.to_device(my_res, "cpu")
        np.testing.assert_allclose(my_res_np, ref_res, rtol=1e-5)


# -----------------------------------------------------------------------------
# Test Class: Simpson
# -----------------------------------------------------------------------------


class TestSimpson:

    def test_exact_odd_samples(self, backend_data):
        """Simpson's rule is exact for polynomials up to degree 3 on uniform grids."""
        name, xp, device = backend_data

        # f(x) = x^2, integrate 0 to 2. Area = 8/3 ~= 2.6667
        # Need 3 points (odd) for minimal Simpson: [0, 1, 2] -> [0, 1, 4]
        x_cpu = np.linspace(0, 2, 3)
        y_cpu = x_cpu**2

        y = to_device(y_cpu, xp, device)

        res = F.simpson(y, dx=1.0)
        assert float(res) == pytest.approx(8.0 / 3.0, rel=1e-6)

    def test_matches_scipy_even_samples(self, backend_data):
        """
        When samples are even, we default to Simpson + Last Interval Trapz.
        We verify this against manual calculation to be robust against SciPy versions.
        """
        name, xp, device = backend_data

        # 4 samples (even). x=[0, 1, 2, 3], y=[0, 1, 4, 9] (y=x^2)
        y_cpu = np.array([0.0, 1.0, 4.0, 9.0])
        y = to_device(y_cpu, xp, device)

        # Execute Implementation
        res = F.simpson(y, dx=1.0)

        # -------------------------------------------------------
        # Manual Verification (Simpson 0..2 + Trapezoid 2..3)
        # -------------------------------------------------------
        # Part 1: Simpson on [0, 1, 4] (h=1)
        # Area = 1/3 * (0 + 4*1 + 4) = 8/3 ≈ 2.6666667
        simpson_part = 8.0 / 3.0

        # Part 2: Trapezoid on [4, 9] (h=1)
        # Area = 1/2 * (4 + 9) = 6.5
        trapz_part = 6.5

        expected_total = simpson_part + trapz_part  # 9.16666666...

        assert float(res) == pytest.approx(expected_total, rel=1e-6)

    def test_multidim_axis(self, backend_data):
        name, xp, device = backend_data

        y_cpu = np.random.rand(5, 7, 5)  # Middle dim is odd
        y = to_device(y_cpu, xp, device)

        res = F.simpson(y, dx=0.5, axis=1)

        # For standard odd usage, we can trust SciPy to be stable
        # (or just trust our math matches logic)
        try:
            # Try new API
            ref = integrate.simpson(y_cpu, dx=0.5, axis=1)
        except AttributeError:
            # Fallback for old Scipy
            ref = integrate.simps(y_cpu, dx=0.5, axis=1)

        assert res.shape == (5, 5)

        res_np = array_api_compat.to_device(res, "cpu")
        np.testing.assert_allclose(res_np, ref, rtol=1e-5)

    def test_fallback_too_few_samples(self, backend_data):
        """If samples < 3, should fall back to trapezoid."""
        name, xp, device = backend_data

        y_cpu = np.array([1.0, 2.0])  # 2 samples
        y = to_device(y_cpu, xp, device)

        # Area = 1.5 * 1.0 = 1.5
        res = F.simpson(y, dx=1.0)
        assert float(res) == pytest.approx(1.5)
