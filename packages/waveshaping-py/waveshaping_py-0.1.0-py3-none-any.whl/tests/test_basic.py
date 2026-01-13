"""
Basic tests for waveshaping-py library.
"""

import numpy as np
import pytest
import sys
import os

# Add the parent directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import waveshaping as ws


class TestClip:
    def test_soft_clip(self):
        x = np.array([0.5, -0.8, 1.2])
        result = ws.clip.soft(x, drive=1.0)
        assert result.shape == x.shape
        assert np.all(np.abs(result) <= 1.0)  # Soft clipping should bound output
    
    def test_hard_clip(self):
        x = np.array([0.5, -0.8, 1.2])
        threshold = 0.7
        result = ws.clip.hard(x, threshold=threshold)
        assert np.all(np.abs(result) <= threshold)
        assert result[0] == 0.5  # Should not clip
        assert result[1] == -0.7  # Should clip
        assert result[2] == 0.7   # Should clip


class TestSaturate:
    def test_tanh_sat(self):
        x = np.array([0.0, 1.0, -1.0])
        result = ws.saturate.tanh_sat(x, drive=1.0)
        assert result.shape == x.shape
        assert result[0] == 0.0
        assert np.all(np.abs(result) <= 1.0)
    
    def test_tube_sat(self):
        x = np.array([0.5, -0.5])
        result = ws.saturate.tube_sat(x, drive=1.0)
        assert result.shape == x.shape
        # Tube saturation should be asymmetric
        assert result[0] != -result[1]


class TestFold:
    def test_sine_fold(self):
        x = np.array([0.0, 1.0, -1.0])
        result = ws.fold.sine_fold(x, threshold=1.0)
        assert result.shape == x.shape
        assert result[0] == 0.0
    
    def test_foldback(self):
        x = np.array([0.5, 1.5, -1.5])
        result = ws.fold.foldback(x, threshold=1.0)
        assert result.shape == x.shape


class TestRectify:
    def test_half_wave(self):
        x = np.array([0.5, -0.5, 0.0])
        result = ws.rectify.half_wave(x)
        assert result.shape == x.shape
        assert result[0] == 0.5
        assert result[1] == 0.0
        assert result[2] == 0.0
    
    def test_full_wave(self):
        x = np.array([0.5, -0.5, 0.0])
        result = ws.rectify.full_wave(x)
        assert result.shape == x.shape
        assert result[0] == 0.5
        assert result[1] == 0.5
        assert result[2] == 0.0


class TestPolynomial:
    def test_quadratic(self):
        x = np.array([0.0, 1.0, -1.0])
        result = ws.polynomial.quadratic(x, a=1.0, b=0.5)
        expected = x + 0.5 * x * x
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_cubic(self):
        x = np.array([0.0, 1.0, -1.0])
        result = ws.polynomial.cubic(x, a=1.0, b=0.0, c=-1.0/3.0)
        assert result.shape == x.shape


class TestSpecial:
    def test_bitcrush(self):
        x = np.array([0.5, -0.8, 1.0])
        result = ws.special.bitcrush(x, bits=4)
        assert result.shape == x.shape
        # Bitcrushing should quantize values
        levels = 2.0 ** 4
        expected = np.round(x * levels) / levels
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_ring_modulation(self):
        x = np.array([1.0])
        result = ws.special.ring_modulation(x, freq=440.0, sample_rate=44100.0)
        assert result.shape == x.shape


class TestUtils:
    def test_clamp(self):
        x = np.array([0.5, -1.5, 1.5])
        result = ws.utils.clamp(x, -1.0, 1.0)
        expected = np.array([0.5, -1.0, 1.0])
        np.testing.assert_array_equal(result, expected)
    
    def test_safe_divide(self):
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([2.0, 0.0, 1.0])
        result = ws.utils.safe_divide(x, y, fallback=0.0)
        expected = np.array([0.5, 0.0, 3.0])
        np.testing.assert_array_equal(result, expected)


class TestScalarInputs:
    """Test that all functions work with scalar inputs."""
    
    def test_scalar_clip(self):
        result = ws.clip.soft(0.8)
        assert isinstance(result, (float, np.floating))
    
    def test_scalar_saturate(self):
        result = ws.saturate.tanh_sat(0.8)
        assert isinstance(result, (float, np.floating))
    
    def test_scalar_fold(self):
        result = ws.fold.sine_fold(0.8)
        assert isinstance(result, (float, np.floating))


if __name__ == "__main__":
    pytest.main([__file__])