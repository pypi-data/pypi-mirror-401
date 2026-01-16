import pytest
import numpy as np
import array_api_signal as aps


class TestUnifiedNamespace:
    """Tests for the dispatch logic and namespace structure."""

    def test_no_args_defaults_numpy(self):
        """aps.array_namespace() with no args should default to NumPy wrapper."""
        xp = aps.array_namespace()
        # This triggers wrapper.py getattr -> windows.hann
        w = xp.hann(5)
        assert isinstance(w, np.ndarray)
        assert len(w) == 5

    def test_collision_priority(self):
        """Ensure our local modules take precedence over extra/backend."""
        x = np.ones(10)
        xp = aps.array_namespace(x)

        # 'pad' is in extra (re-exported), not local signal/integral
        assert hasattr(xp, "pad")

        # 'simpson' is local.
        assert xp.simpson.__module__.startswith("array_api_signal")


class TestBackendSupport:
    """Tests verifying behavior across different backends."""

    def test_numpy_dispatch(self):
        """Test that the wrapper correctly handles NumPy backend."""
        x = np.ones(10)

        # Get unified xp
        xp = aps.array_namespace(x)

        # 1. Check Standard API (Fallback to backend)
        assert xp.sin(0) == 0.0

        # 2. Check Extra API (array-api-extra)
        assert hasattr(xp, "pad")
        assert hasattr(xp, "kron")

        # 3. Check Signal API (Our Extension)
        res = xp.simpson(x)
        # Allow scalar float or 0-dim array return types
        assert isinstance(res, float) or np.isscalar(res) or res.ndim == 0

        # 4. Check Context-Aware Creation (Windows)
        # xp wraps numpy, so hann should return numpy array
        w = xp.hann(10)
        assert isinstance(w, np.ndarray)
        assert len(w) == 10

    def test_torch_dispatch(self):
        """Test that the wrapper correctly handles Torch backend."""
        try:
            import torch
        except ImportError:
            pytest.skip("Torch not installed")

        x = torch.ones(10)
        xp = aps.array_namespace(x)

        # 1. Standard
        res = xp.sin(x)
        assert isinstance(res, torch.Tensor)

        # 2. Signal Extension
        res = xp.simpson(x)
        assert isinstance(res, torch.Tensor)

        # 3. Creation (Should return Tensor because xp wraps Torch)
        w = xp.hann(10)
        assert isinstance(w, torch.Tensor)
        assert not w.requires_grad  # Windows should be static
