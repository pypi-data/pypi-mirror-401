"""
Example usage of the waveshaping-py library.

This script demonstrates various waveshaping effects that can be applied to audio signals.
"""

import numpy as np
import matplotlib.pyplot as plt

# Import waveshaping modules
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import waveshaping as ws


def create_test_signal(duration=1.0, sample_rate=44100, frequency=440.0, amplitude=0.8):
    """Create a test sine wave signal."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    return t, amplitude * np.sin(2 * np.pi * frequency * t)


def plot_comparison(original, processed, title, sample_rate=44100):
    """Plot comparison between original and processed signals."""
    plt.figure(figsize=(12, 8))
    
    # Time domain plot
    plt.subplot(2, 2, 1)
    t = np.arange(len(original)) / sample_rate
    plt.plot(t[:1000], original[:1000], label='Original', alpha=0.7)
    plt.plot(t[:1000], processed[:1000], label='Processed', alpha=0.8)
    plt.title(f'{title} - Time Domain')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Transfer function plot
    plt.subplot(2, 2, 2)
    plt.scatter(original[::100], processed[::100], alpha=0.5, s=1)
    plt.plot([-1, 1], [-1, 1], 'r--', alpha=0.5, label='Linear')
    plt.title(f'{title} - Transfer Function')
    plt.xlabel('Input')
    plt.ylabel('Output')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Frequency domain plots
    freqs = np.fft.fftfreq(len(original), 1/sample_rate)
    orig_fft = np.abs(np.fft.fft(original))
    proc_fft = np.abs(np.fft.fft(processed))
    
    plt.subplot(2, 2, 3)
    plt.semilogy(freqs[:len(freqs)//2], orig_fft[:len(freqs)//2], label='Original', alpha=0.7)
    plt.semilogy(freqs[:len(freqs)//2], proc_fft[:len(freqs)//2], label='Processed', alpha=0.8)
    plt.title(f'{title} - Frequency Domain')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, 5000)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Harmonic content
    plt.subplot(2, 2, 4)
    fundamental_idx = np.argmax(orig_fft[:len(freqs)//2])
    harmonics = []
    for i in range(1, 10):
        harmonic_idx = fundamental_idx * i
        if harmonic_idx < len(proc_fft)//2:
            harmonics.append(proc_fft[harmonic_idx])
        else:
            break
    
    plt.bar(range(1, len(harmonics) + 1), harmonics, alpha=0.7)
    plt.title(f'{title} - Harmonic Content')
    plt.xlabel('Harmonic Number')
    plt.ylabel('Magnitude')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def main():
    """Main example function."""
    print("Waveshaping-py Library Examples")
    print("=" * 40)
    
    # Create test signal
    sample_rate = 44100
    t, signal = create_test_signal(duration=0.1, sample_rate=sample_rate, amplitude=0.9)
    
    print(f"Created test signal: {len(signal)} samples at {sample_rate} Hz")
    print(f"Signal range: {np.min(signal):.3f} to {np.max(signal):.3f}")
    
    # Example 1: Clipping Effects
    print("\n1. Clipping Effects:")
    
    # Soft clipping
    soft_clipped = ws.clip.soft(signal, drive=3.0)
    print(f"   Soft clipping (drive=3.0): range {np.min(soft_clipped):.3f} to {np.max(soft_clipped):.3f}")
    
    # Hard clipping
    hard_clipped = ws.clip.hard(signal, threshold=0.5)
    print(f"   Hard clipping (threshold=0.5): range {np.min(hard_clipped):.3f} to {np.max(hard_clipped):.3f}")
    
    # Cubic clipping
    cubic_clipped = ws.clip.cubic(signal)
    print(f"   Cubic clipping: range {np.min(cubic_clipped):.3f} to {np.max(cubic_clipped):.3f}")
    
    # Example 2: Saturation Effects
    print("\n2. Saturation Effects:")
    
    # Tanh saturation
    tanh_sat = ws.saturate.tanh_sat(signal, drive=2.5)
    print(f"   Tanh saturation (drive=2.5): range {np.min(tanh_sat):.3f} to {np.max(tanh_sat):.3f}")
    
    # Tube saturation
    tube_sat = ws.saturate.tube_sat(signal, drive=1.8)
    print(f"   Tube saturation (drive=1.8): range {np.min(tube_sat):.3f} to {np.max(tube_sat):.3f}")
    
    # Exponential saturation
    exp_sat = ws.saturate.exponential(signal, drive=1.5)
    print(f"   Exponential saturation (drive=1.5): range {np.min(exp_sat):.3f} to {np.max(exp_sat):.3f}")
    
    # Example 3: Wave Folding
    print("\n3. Wave Folding Effects:")
    
    # Sine folding
    sine_folded = ws.fold.sine_fold(signal, threshold=0.7)
    print(f"   Sine folding (threshold=0.7): range {np.min(sine_folded):.3f} to {np.max(sine_folded):.3f}")
    
    # Foldback
    foldback = ws.fold.foldback(signal, threshold=0.6)
    print(f"   Foldback (threshold=0.6): range {np.min(foldback):.3f} to {np.max(foldback):.3f}")
    
    # Chebyshev folding
    cheb_folded = ws.fold.chebyshev_fold(signal, order=5)
    print(f"   Chebyshev folding (order=5): range {np.min(cheb_folded):.3f} to {np.max(cheb_folded):.3f}")
    
    # Example 4: Polynomial Waveshaping
    print("\n4. Polynomial Waveshaping:")
    
    # Cubic polynomial
    cubic_poly = ws.polynomial.cubic(signal, a=1.0, b=0.0, c=-0.5)
    print(f"   Cubic polynomial: range {np.min(cubic_poly):.3f} to {np.max(cubic_poly):.3f}")
    
    # Odd polynomial (generates odd harmonics only)
    odd_poly = ws.polynomial.odd_polynomial(signal, coeffs=[1.0, -0.3, 0.1])
    print(f"   Odd polynomial: range {np.min(odd_poly):.3f} to {np.max(odd_poly):.3f}")
    
    # Example 5: Special Effects
    print("\n5. Special Effects:")
    
    # Bitcrushing
    bitcrushed = ws.special.bitcrush(signal, bits=6)
    print(f"   Bitcrush (6-bit): range {np.min(bitcrushed):.3f} to {np.max(bitcrushed):.3f}")
    
    # Ring modulation
    ring_mod = ws.special.ring_modulation(signal, freq=100.0, sample_rate=sample_rate)
    print(f"   Ring modulation (100 Hz): range {np.min(ring_mod):.3f} to {np.max(ring_mod):.3f}")
    
    # Example 6: Rectification
    print("\n6. Rectification Effects:")
    
    # Half-wave rectification
    half_wave = ws.rectify.half_wave(signal)
    print(f"   Half-wave rectifier: range {np.min(half_wave):.3f} to {np.max(half_wave):.3f}")
    
    # Soft rectification
    soft_rect = ws.rectify.soft_rectifier(signal, smoothness=0.1)
    print(f"   Soft rectifier: range {np.min(soft_rect):.3f} to {np.max(soft_rect):.3f}")
    
    # Plot some examples (if matplotlib is available)
    try:
        plot_comparison(signal, soft_clipped, "Soft Clipping (drive=3.0)", sample_rate)
        plot_comparison(signal, tube_sat, "Tube Saturation (drive=1.8)", sample_rate)
        plot_comparison(signal, sine_folded, "Sine Folding (threshold=0.7)", sample_rate)
        plot_comparison(signal, bitcrushed, "Bitcrush (6-bit)", sample_rate)
    except ImportError:
        print("\nMatplotlib not available for plotting. Install with: pip install matplotlib")
    
    print("\nExample completed! Try experimenting with different parameters.")


if __name__ == "__main__":
    main()