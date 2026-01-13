"""
Clipping waveshaping functions for audio signal processing.
"""

import numpy as np
from .utils import clamp, sign


def hard(x, threshold=1.0):
    """
    Hard clipping: Aggressive, preserves sign.
    
    Args:
        x: Input signal (array or scalar)
        threshold: Clipping threshold (default: 1.0)
    
    Returns:
        Hard clipped signal
    """
    if threshold <= 0.0:
        return np.zeros_like(x)
    return clamp(x, -threshold, threshold)


def soft(x, drive=1.0):
    """
    Soft clipping using tanh: Mild, odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Soft clipped signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return np.tanh(x * drive)


def atan_clip(x, drive=1.0):
    """
    Arctangent clipping: Mild, odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Arctangent clipped signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return np.arctan(x * drive) * (2.0 / np.pi)


def algebraic(x):
    """
    Algebraic clipping: Mild, odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
    
    Returns:
        Algebraically clipped signal
    """
    return x / np.sqrt(1.0 + x * x)


def soft_limit(x):
    """
    Soft limit clipping: Very mild, odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
    
    Returns:
        Soft limited signal
    """
    return (2.0 / np.pi) * np.arctan(x)


def cubic(x):
    """
    Cubic clipping: Smooth, odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
    
    Returns:
        Cubic clipped signal
    """
    x = np.asarray(x)
    abs_x = np.abs(x)
    sign_x = sign(x)
    
    # Case 1: |x| >= 1.0
    result = sign_x.copy()
    
    # Case 2: |x| <= 1/3
    mask1 = abs_x <= (1.0 / 3.0)
    result = np.where(mask1, 2.0 * x, result)
    
    # Case 3: 1/3 < |x| < 1.0  
    mask2 = (abs_x > (1.0 / 3.0)) & (abs_x < 1.0)
    cubic_part = sign_x * (3.0 - (2.0 - 3.0 * abs_x) ** 2) / 3.0
    result = np.where(mask2, cubic_part, result)
    
    return result


def sinusoidal(x, drive=1.0):
    """
    Sinusoidal clipping: Musical, harmonic.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Sinusoidally clipped signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return np.sin(x * drive * np.pi / 2.0)