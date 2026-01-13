"""
Mathematical utility functions for waveshaping operations.
"""

import numpy as np
from typing import Union

ArrayLike = Union[float, np.ndarray]


def clamp(x: ArrayLike, min_val: float = -1.0, max_val: float = 1.0) -> ArrayLike:
    """
    Clamp values to a specified range, handling NaN values.
    
    Args:
        x: Input array or scalar
        min_val: Minimum value (default: -1.0)
        max_val: Maximum value (default: 1.0)
    
    Returns:
        Clamped values
    """
    return np.clip(x, min_val, max_val)


def safe_divide(x, y, fallback=0.0):
    """
    Safe division that prevents division by zero or near-zero values.
    
    Args:
        x: Numerator
        y: Denominator  
        fallback: Value to return when division would fail (default: 0.0)
    
    Returns:
        Safe division result
    """
    return np.where(np.abs(y) > 1e-10, x / y, fallback)


def normalize(x, target_range=(-1.0, 1.0)):
    """
    Normalize values to a target range.
    
    Args:
        x: Input array or scalar
        target_range: Tuple of (min, max) for target range (default: (-1, 1))
    
    Returns:
        Normalized values
    """
    x = np.asarray(x)
    x_min, x_max = np.min(x), np.max(x)
    
    if x_max == x_min:
        return np.zeros_like(x)
    
    normalized = (x - x_min) / (x_max - x_min)
    target_min, target_max = target_range
    return normalized * (target_max - target_min) + target_min


def sign(x):
    """
    Return the sign of the input.
    
    Args:
        x: Input array or scalar
    
    Returns:
        Sign values (-1, 0, or 1)
    """
    return np.sign(x)


def fast_tanh(x):
    """
    Fast approximation of hyperbolic tangent.
    For non-realtime use, just use numpy's tanh for accuracy.
    
    Args:
        x: Input array or scalar
    
    Returns:
        Hyperbolic tangent values
    """
    return np.tanh(x)