"""
Folding/wave folding waveshaping functions for audio signal processing.
"""

import numpy as np
from .utils import sign


def foldback(x, threshold=1.0):
    """
    Aggressive folding with reflection at boundaries, producing odd and even harmonics.
    
    Args:
        x: Input signal (array or scalar)
        threshold: Folding threshold (default: 1.0)
    
    Returns:
        Foldback processed signal
    """
    if threshold <= 0.0:
        return np.zeros_like(x)
    
    x = np.asarray(x)
    # Normalize to threshold
    x_norm = x / threshold
    
    # Fold the signal
    folded = np.abs(x_norm) % 4.0
    folded = np.where(folded <= 2.0, folded, 4.0 - folded)
    folded = np.where(folded <= 1.0, folded, 2.0 - folded)
    
    # Apply original sign
    result = sign(x_norm) * folded * threshold
    return result


def sine_fold(x, threshold=1.0):
    """
    Smooth folding using sine function, creating a musical sound with odd and even harmonics.
    
    Args:
        x: Input signal (array or scalar)
        threshold: Folding threshold (default: 1.0)
    
    Returns:
        Sine folded signal
    """
    if threshold <= 0.0:
        return np.zeros_like(x)
    
    return threshold * np.sin(x * np.pi / threshold)


def triangle_fold(x, threshold=1.0):
    """
    Creates a triangle wave fold with primarily odd harmonics, described as "bright" and harmonic.
    
    Args:
        x: Input signal (array or scalar)
        threshold: Folding threshold (default: 1.0)
    
    Returns:
        Triangle folded signal
    """
    if threshold <= 0.0:
        return np.zeros_like(x)
    
    x = np.asarray(x)
    # Normalize
    x_norm = x / threshold
    
    # Create triangle wave folding
    period = 4.0
    folded = np.abs(x_norm) % period
    folded = np.where(folded <= 1.0, folded, 
                     np.where(folded <= 3.0, 2.0 - folded, folded - 4.0))
    
    return sign(x) * folded * threshold


def bipolar_fold(x, threshold=1.0):
    """
    Maintains signal sign during folding, with an aggressive character and odd/even harmonics.
    
    Args:
        x: Input signal (array or scalar)
        threshold: Folding threshold (default: 1.0)
    
    Returns:
        Bipolar folded signal
    """
    if threshold <= 0.0:
        return np.zeros_like(x)
    
    x = np.asarray(x)
    abs_x = np.abs(x)
    sign_x = sign(x)
    
    # Fold when exceeding threshold
    excess = abs_x - threshold
    folded_excess = np.where(excess > 0, 
                            threshold - (excess % (2.0 * threshold)), 
                            abs_x)
    
    return sign_x * folded_excess


def soft_fold(x, drive=1.0):
    """
    Uses tanh for a controlled, musical folding effect with primarily odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount for folding intensity (default: 1.0)
    
    Returns:
        Soft folded signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    
    return np.tanh(x * drive) + 0.3 * np.tanh(3.0 * x * drive)


def chebyshev_fold(x, order=3):
    """
    Chebyshev polynomial folding for harmonic generation.
    
    Args:
        x: Input signal (array or scalar), should be in [-1, 1]
        order: Chebyshev polynomial order (default: 3)
    
    Returns:
        Chebyshev folded signal
    """
    x = np.clip(x, -1.0, 1.0)  # Ensure input is in valid range
    
    if order == 1:
        return x
    elif order == 2:
        return 2.0 * x * x - 1.0
    elif order == 3:
        return 4.0 * x * x * x - 3.0 * x
    elif order == 4:
        return 8.0 * x**4 - 8.0 * x * x + 1.0
    elif order == 5:
        return 16.0 * x**5 - 20.0 * x**3 + 5.0 * x
    else:
        # General case using recurrence relation
        T0 = np.ones_like(x)
        T1 = x
        for n in range(2, order + 1):
            T2 = 2.0 * x * T1 - T0
            T0, T1 = T1, T2
        return T1