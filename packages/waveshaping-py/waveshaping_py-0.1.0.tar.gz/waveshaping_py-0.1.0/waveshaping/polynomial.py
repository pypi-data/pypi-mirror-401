"""
Polynomial waveshaping functions for audio signal processing.
"""

import numpy as np


def quadratic(x, a=0.5, b=0.5):
    """
    Quadratic polynomial waveshaping: f(x) = a*x + b*x^2
    
    Args:
        x: Input signal (array or scalar)
        a: Linear coefficient (default: 0.5)
        b: Quadratic coefficient (default: 0.5)
    
    Returns:
        Quadratic shaped signal
    """
    return a * x + b * x * x


def cubic(x, a=1.0, b=0.0, c=-1.0/3.0):
    """
    Cubic polynomial waveshaping: f(x) = a*x + b*x^2 + c*x^3
    
    Args:
        x: Input signal (array or scalar)
        a: Linear coefficient (default: 1.0)
        b: Quadratic coefficient (default: 0.0)
        c: Cubic coefficient (default: -1/3)
    
    Returns:
        Cubic shaped signal
    """
    return a * x + b * x * x + c * x * x * x


def quartic(x, a=1.0, b=0.0, c=0.0, d=0.25):
    """
    Quartic polynomial waveshaping: f(x) = a*x + b*x^2 + c*x^3 + d*x^4
    
    Args:
        x: Input signal (array or scalar)
        a: Linear coefficient (default: 1.0)
        b: Quadratic coefficient (default: 0.0)
        c: Cubic coefficient (default: 0.0)
        d: Quartic coefficient (default: 0.25)
    
    Returns:
        Quartic shaped signal
    """
    x2 = x * x
    return a * x + b * x2 + c * x2 * x + d * x2 * x2


def odd_polynomial(x, coeffs=[1.0, -1.0/3.0, 1.0/5.0]):
    """
    Odd polynomial waveshaping: f(x) = sum(coeffs[i] * x^(2*i+1))
    Only odd harmonics are generated.
    
    Args:
        x: Input signal (array or scalar)
        coeffs: List of coefficients for odd powers (default: [1, -1/3, 1/5])
    
    Returns:
        Odd polynomial shaped signal
    """
    result = np.zeros_like(x)
    for i, coeff in enumerate(coeffs):
        power = 2 * i + 1
        result += coeff * (x ** power)
    return result


def even_polynomial(x, coeffs=[0.0, 0.5, -0.25]):
    """
    Even polynomial waveshaping: f(x) = sum(coeffs[i] * x^(2*i))
    Only even harmonics are generated.
    
    Args:
        x: Input signal (array or scalar)
        coeffs: List of coefficients for even powers (default: [0, 0.5, -0.25])
    
    Returns:
        Even polynomial shaped signal
    """
    result = np.zeros_like(x)
    for i, coeff in enumerate(coeffs):
        power = 2 * i
        if power == 0:
            result += coeff
        else:
            result += coeff * (x ** power)
    return result


def legendre_polynomial(x, order=3):
    """
    Legendre polynomial waveshaping.
    
    Args:
        x: Input signal (array or scalar), should be in [-1, 1]
        order: Polynomial order (default: 3)
    
    Returns:
        Legendre polynomial shaped signal
    """
    x = np.clip(x, -1.0, 1.0)  # Ensure input is in valid range
    
    if order == 0:
        return np.ones_like(x)
    elif order == 1:
        return x
    elif order == 2:
        return 0.5 * (3.0 * x * x - 1.0)
    elif order == 3:
        return 0.5 * (5.0 * x * x * x - 3.0 * x)
    elif order == 4:
        return 0.125 * (35.0 * x**4 - 30.0 * x * x + 3.0)
    elif order == 5:
        return 0.125 * (63.0 * x**5 - 70.0 * x**3 + 15.0 * x)
    else:
        # General case using recurrence relation
        P0 = np.ones_like(x)
        P1 = x
        for n in range(2, order + 1):
            P2 = ((2.0 * n - 1.0) * x * P1 - (n - 1.0) * P0) / n
            P0, P1 = P1, P2
        return P1


def hermite_polynomial(x, order=3):
    """
    Hermite polynomial waveshaping.
    
    Args:
        x: Input signal (array or scalar)
        order: Polynomial order (default: 3)
    
    Returns:
        Hermite polynomial shaped signal
    """
    if order == 0:
        return np.ones_like(x)
    elif order == 1:
        return 2.0 * x
    elif order == 2:
        return 4.0 * x * x - 2.0
    elif order == 3:
        return 8.0 * x * x * x - 12.0 * x
    elif order == 4:
        return 16.0 * x**4 - 48.0 * x * x + 12.0
    else:
        # General case using recurrence relation
        H0 = np.ones_like(x)
        H1 = 2.0 * x
        for n in range(2, order + 1):
            H2 = 2.0 * x * H1 - 2.0 * (n - 1) * H0
            H0, H1 = H1, H2
        return H1


def custom_polynomial(x, coefficients):
    """
    Custom polynomial waveshaping with arbitrary coefficients.
    f(x) = sum(coefficients[i] * x^i)
    
    Args:
        x: Input signal (array or scalar)
        coefficients: List of polynomial coefficients [a0, a1, a2, ...]
    
    Returns:
        Custom polynomial shaped signal
    """
    result = np.zeros_like(x)
    for i, coeff in enumerate(coefficients):
        if i == 0:
            result += coeff
        else:
            result += coeff * (x ** i)
    return result


def normalized_polynomial(x, coefficients):
    """
    Normalized polynomial that ensures output stays in reasonable range.
    
    Args:
        x: Input signal (array or scalar)
        coefficients: List of polynomial coefficients
    
    Returns:
        Normalized polynomial shaped signal
    """
    result = custom_polynomial(x, coefficients)
    
    # Normalize to prevent excessive amplitude
    max_val = np.max(np.abs(result))
    if max_val > 1.0:
        result = result / max_val
    
    return result