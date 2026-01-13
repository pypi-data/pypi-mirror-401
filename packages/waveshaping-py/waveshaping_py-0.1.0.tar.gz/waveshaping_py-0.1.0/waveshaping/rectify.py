"""
Rectification waveshaping functions for audio signal processing.
"""

import numpy as np
from .utils import sign


def half_wave(x, threshold=0.0):
    """
    Half-wave rectification: passes positive values, zeros negative values.
    
    Args:
        x: Input signal (array or scalar)
        threshold: Threshold for rectification (default: 0.0)
    
    Returns:
        Half-wave rectified signal
    """
    return np.maximum(x - threshold, 0.0)


def full_wave(x):
    """
    Full-wave rectification: takes absolute value of input.
    
    Args:
        x: Input signal (array or scalar)
    
    Returns:
        Full-wave rectified signal
    """
    return np.abs(x)


def precision_rectifier(x, threshold=0.7):
    """
    Precision rectifier: enhanced half-wave with adjustable threshold.
    
    Args:
        x: Input signal (array or scalar)
        threshold: Rectification threshold (default: 0.7)
    
    Returns:
        Precision rectified signal
    """
    return np.where(x > threshold, x, 0.0)


def soft_rectifier(x, smoothness=0.1):
    """
    Soft rectification using smooth transition.
    
    Args:
        x: Input signal (array or scalar)
        smoothness: Smoothness parameter (default: 0.1)
    
    Returns:
        Soft rectified signal
    """
    return 0.5 * (x + np.sqrt(x * x + smoothness))


def tube_rectifier(x, threshold=0.7, knee=0.3):
    """
    Tube-style rectifier with soft knee.
    
    Args:
        x: Input signal (array or scalar)
        threshold: Rectification threshold (default: 0.7)
        knee: Knee smoothness (default: 0.3)
    
    Returns:
        Tube rectified signal
    """
    x = np.asarray(x)
    
    # Below threshold: zero output
    # Above threshold + knee: linear
    # In between: smooth transition
    
    result = np.zeros_like(x)
    
    # Linear region
    linear_mask = x >= (threshold + knee)
    result = np.where(linear_mask, x - threshold, result)
    
    # Knee region
    knee_mask = (x > threshold) & (x < (threshold + knee))
    t = (x - threshold) / knee
    smooth_t = t * t * (3.0 - 2.0 * t)  # Smooth step
    knee_output = smooth_t * knee
    result = np.where(knee_mask, knee_output, result)
    
    return result


def envelope_follower(x, attack=0.1, release=0.01):
    """
    Envelope follower using rectification and smoothing.
    
    Args:
        x: Input signal (array or scalar)
        attack: Attack time coefficient (default: 0.1)
        release: Release time coefficient (default: 0.01)
    
    Returns:
        Envelope followed signal
    """
    x = np.asarray(x)
    rectified = np.abs(x)
    
    if rectified.ndim == 0:  # Scalar input
        return float(rectified)
    
    # Simple envelope following
    envelope = np.zeros_like(rectified)
    envelope[0] = rectified[0]
    
    for i in range(1, len(rectified)):
        if rectified[i] > envelope[i-1]:
            # Attack
            envelope[i] = envelope[i-1] + attack * (rectified[i] - envelope[i-1])
        else:
            # Release  
            envelope[i] = envelope[i-1] + release * (rectified[i] - envelope[i-1])
    
    return envelope


def peak_detector(x, decay=0.99):
    """
    Peak detection with decay.
    
    Args:
        x: Input signal (array or scalar)
        decay: Decay factor (default: 0.99)
    
    Returns:
        Peak detected signal
    """
    x = np.asarray(x)
    rectified = np.abs(x)
    
    if rectified.ndim == 0:  # Scalar input
        return float(rectified)
    
    peaks = np.zeros_like(rectified)
    peaks[0] = rectified[0]
    
    for i in range(1, len(rectified)):
        peaks[i] = max(rectified[i], peaks[i-1] * decay)
    
    return peaks