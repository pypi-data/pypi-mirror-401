"""
Saturation waveshaping functions for audio signal processing.
"""

import numpy as np
from scipy.special import erf
from .utils import sign


def tanh_sat(x, drive=1.0):
    """
    Tanh saturation: mild to aggressive, odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Tanh saturated signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return np.tanh(x * drive)


def atan_sat(x, drive=1.0):
    """
    Arctangent saturation: mild character, odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Arctangent saturated signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return (2.0 / np.pi) * np.arctan(x * drive)


def erf_sat(x, drive=1.0):
    """
    Error function saturation: smooth character, odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Error function saturated signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return erf(x * drive * np.sqrt(np.pi / 2.0))


def exponential(x, drive=1.0):
    """
    Exponential saturation: exponential character, odd and even harmonics.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Exponentially saturated signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return sign(x) * (1.0 - np.exp(-np.abs(x) * drive))


def gaussian(x, drive=1.0):
    """
    Gaussian-like saturation: gaussian character, odd harmonics.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Gaussian saturated signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return sign(x) * np.sqrt(1.0 - np.exp(-x * x * drive))


def power_sat(x, drive=1.0, power=2.0):
    """
    Power saturation: algebraic character, customizable harmonics.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
        power: Power exponent (default: 2.0)
    
    Returns:
        Power saturated signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return sign(x) * (1.0 - (1.0 / (1.0 + np.abs(x * drive) ** power)))


def tube_sat(x, drive=1.0):
    """
    Tube-like saturation: warm tube character.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Tube-style saturated signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    
    x_driven = x * drive
    abs_x = np.abs(x_driven)
    
    # Asymmetric saturation for tube-like character
    return np.where(x_driven >= 0,
                   x_driven / (1.0 + x_driven),
                   x_driven / (1.0 - 0.7 * x_driven))


def sigmoid_sat(x, drive=1.0):
    """
    Sigmoid saturation: S-curve saturation.
    
    Args:
        x: Input signal (array or scalar)
        drive: Drive amount (default: 1.0)
    
    Returns:
        Sigmoid saturated signal
    """
    if drive <= 0.0:
        return np.zeros_like(x)
    return (2.0 / (1.0 + np.exp(-x * drive))) - 1.0