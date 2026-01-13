"""
Simple example of waveshaping-py usage.
"""

import numpy as np
import sys
import os

# Add parent directory to path to import waveshaping
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import waveshaping as ws

# Create a simple sine wave
t = np.linspace(0, 1, 44100)  # 1 second at 44.1kHz
frequency = 440  # A4 note
signal = 0.8 * np.sin(2 * np.pi * frequency * t)

print("Original signal range:", np.min(signal), "to", np.max(signal))

# Apply different waveshaping effects
print("\nApplying waveshaping effects:")

# 1. Soft clipping
clipped = ws.clip.soft(signal, drive=2.0)
print(f"Soft clipped: {np.min(clipped):.3f} to {np.max(clipped):.3f}")

# 2. Tube saturation
saturated = ws.saturate.tube_sat(signal, drive=1.5)
print(f"Tube saturated: {np.min(saturated):.3f} to {np.max(saturated):.3f}")

# 3. Wave folding
folded = ws.fold.sine_fold(signal, threshold=0.7)
print(f"Sine folded: {np.min(folded):.3f} to {np.max(folded):.3f}")

# 4. Polynomial shaping
poly_shaped = ws.polynomial.cubic(signal, a=1.0, c=-0.3)
print(f"Cubic polynomial: {np.min(poly_shaped):.3f} to {np.max(poly_shaped):.3f}")

# 5. Bitcrushing
bitcrushed = ws.special.bitcrush(signal, bits=8)
print(f"Bitcrushed: {np.min(bitcrushed):.3f} to {np.max(bitcrushed):.3f}")

print("\nDone! All effects applied successfully.")