"""
Special effects waveshaping functions for audio signal processing.
"""

import numpy as np
from .utils import sign


def bitcrush(x, bits=8):
    """
    Bitcrushing effect: reduces bit depth for digital distortion.
    
    Args:
        x: Input signal (array or scalar)
        bits: Target bit depth (default: 8)
    
    Returns:
        Bitcrushed signal
    """
    if bits <= 0:
        return np.zeros_like(x)
    
    levels = 2.0 ** bits
    return np.round(x * levels) / levels


def downsample(x, factor=2):
    """
    Downsampling effect: sample rate reduction simulation.
    
    Args:
        x: Input signal (array)
        factor: Downsampling factor (default: 2)
    
    Returns:
        Downsampled signal
    """
    x = np.asarray(x)
    if x.ndim == 0:
        return x
    
    # Simple downsampling by taking every nth sample and repeating
    downsampled_indices = np.arange(0, len(x), factor)
    downsampled = x[downsampled_indices]
    
    # Repeat samples to maintain original length
    result = np.repeat(downsampled, factor)[:len(x)]
    return result


def ring_modulation(x, freq=440.0, sample_rate=44100.0, phase=0.0):
    """
    Ring modulation effect.
    
    Args:
        x: Input signal (array or scalar)
        freq: Modulation frequency in Hz (default: 440.0)
        sample_rate: Sample rate in Hz (default: 44100.0)
        phase: Phase offset in radians (default: 0.0)
    
    Returns:
        Ring modulated signal
    """
    x = np.asarray(x)
    if x.ndim == 0:
        # Scalar case
        t = 0.0
    else:
        t = np.arange(len(x)) / sample_rate
    
    modulator = np.sin(2.0 * np.pi * freq * t + phase)
    return x * modulator


def amplitude_modulation(x, freq=5.0, sample_rate=44100.0, depth=0.5, phase=0.0):
    """
    Amplitude modulation effect.
    
    Args:
        x: Input signal (array or scalar)
        freq: Modulation frequency in Hz (default: 5.0)
        sample_rate: Sample rate in Hz (default: 44100.0)
        depth: Modulation depth 0-1 (default: 0.5)
        phase: Phase offset in radians (default: 0.0)
    
    Returns:
        Amplitude modulated signal
    """
    x = np.asarray(x)
    if x.ndim == 0:
        # Scalar case
        t = 0.0
    else:
        t = np.arange(len(x)) / sample_rate
    
    modulator = 1.0 + depth * np.sin(2.0 * np.pi * freq * t + phase)
    return x * modulator


def sample_and_hold(x, hold_time=100):
    """
    Sample and hold effect.
    
    Args:
        x: Input signal (array)
        hold_time: Number of samples to hold each value (default: 100)
    
    Returns:
        Sample and hold processed signal
    """
    x = np.asarray(x)
    if x.ndim == 0:
        return x
    
    result = np.zeros_like(x)
    for i in range(len(x)):
        hold_index = (i // hold_time) * hold_time
        if hold_index < len(x):
            result[i] = x[hold_index]
        else:
            result[i] = x[-1]
    
    return result


def noise_gate(x, threshold=0.1, ratio=10.0):
    """
    Noise gate effect.
    
    Args:
        x: Input signal (array or scalar)
        threshold: Gate threshold (default: 0.1)
        ratio: Gate ratio (default: 10.0)
    
    Returns:
        Noise gated signal
    """
    abs_x = np.abs(x)
    
    # Simple gate: reduce amplitude when below threshold
    gate_factor = np.where(abs_x < threshold, 1.0 / ratio, 1.0)
    return x * gate_factor


def waveshaper_table(x, table):
    """
    Wavetable-based waveshaping using lookup table.
    
    Args:
        x: Input signal (array or scalar), should be in [-1, 1]
        table: Lookup table array for waveshaping
    
    Returns:
        Wavetable shaped signal
    """
    x = np.clip(x, -1.0, 1.0)
    table = np.asarray(table)
    
    # Map x from [-1, 1] to table indices
    indices = ((x + 1.0) * 0.5 * (len(table) - 1)).astype(int)
    indices = np.clip(indices, 0, len(table) - 1)
    
    return table[indices]


def chaos_generator(x, a=3.8):
    """
    Chaotic waveshaping using logistic map.
    
    Args:
        x: Input signal (array or scalar)
        a: Chaos parameter (default: 3.8)
    
    Returns:
        Chaotically shaped signal
    """
    # Normalize input to [0, 1]
    x_norm = (x + 1.0) * 0.5
    x_norm = np.clip(x_norm, 0.0, 1.0)
    
    # Apply logistic map
    chaotic = a * x_norm * (1.0 - x_norm)
    
    # Map back to [-1, 1]
    return 2.0 * chaotic - 1.0


def frequency_shifter(x, shift_hz=100.0, sample_rate=44100.0):
    """
    Simple frequency shifter using ring modulation.
    
    Args:
        x: Input signal (array or scalar)
        shift_hz: Frequency shift in Hz (default: 100.0)
        sample_rate: Sample rate in Hz (default: 44100.0)
    
    Returns:
        Frequency shifted signal
    """
    x = np.asarray(x)
    if x.ndim == 0:
        return x
    
    t = np.arange(len(x)) / sample_rate
    
    # Create quadrature oscillators
    cos_osc = np.cos(2.0 * np.pi * shift_hz * t)
    sin_osc = np.sin(2.0 * np.pi * shift_hz * t)
    
    # Apply Hilbert transform approximation (simplified)
    x_real = x * cos_osc
    x_imag = x * sin_osc
    
    return x_real + x_imag


def granular_effect(x, grain_size=1024, overlap=0.5):
    """
    Simple granular synthesis effect.
    
    Args:
        x: Input signal (array)
        grain_size: Size of each grain in samples (default: 1024)
        overlap: Overlap factor 0-1 (default: 0.5)
    
    Returns:
        Granular processed signal
    """
    x = np.asarray(x)
    if x.ndim == 0:
        return x
    
    hop_size = int(grain_size * (1.0 - overlap))
    result = np.zeros_like(x)
    
    # Create window function
    window = np.hanning(grain_size)
    
    for i in range(0, len(x) - grain_size, hop_size):
        # Extract grain
        grain = x[i:i + grain_size] * window
        
        # Add to result with overlap
        end_idx = min(i + grain_size, len(result))
        result[i:end_idx] += grain[:end_idx - i]
    
    return result