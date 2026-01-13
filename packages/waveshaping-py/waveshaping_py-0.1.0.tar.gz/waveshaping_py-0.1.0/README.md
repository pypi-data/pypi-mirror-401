# waveshaping-py

A Python library for audio waveshaping and distortion effects, ported from the C++ waveshaping library. Designed for non-realtime audio processing using numpy arrays.

## Overview

This library provides mathematical waveshaping functions for audio signal processing, including:

- **Clipping**: Hard, soft, cubic, algebraic, and sinusoidal clipping
- **Saturation**: Tanh, arctangent, error function, exponential, and tube-style saturation
- **Folding**: Foldback, sine folding, triangle folding, soft folding, and Chebyshev folding
- **Rectification**: Half-wave, full-wave, precision, soft, and tube rectification
- **Polynomial**: Quadratic, cubic, odd/even polynomials, Legendre and Hermite polynomials
- **Special Effects**: Bitcrushing, ring modulation, amplitude modulation, noise gating, and more

## Installation

### From PyPI (when published)

```bash
pip install waveshaping-py
```

### From Source

```bash
git clone https://github.com/tsugumasa320/waveshaping-py.git
cd waveshaping-py
pip install -e .
```

## Quick Start

```python
import numpy as np
import waveshaping as ws

# Create a test signal
t = np.linspace(0, 1, 44100)
signal = np.sin(2 * np.pi * 440 * t)

# Apply soft clipping
clipped = ws.clip.soft(signal, drive=2.0)

# Apply tube saturation
saturated = ws.saturate.tube_sat(signal, drive=1.5)

# Apply wave folding
folded = ws.fold.sine_fold(signal, threshold=0.8)
```

## Module Structure

- `waveshaping.clip`: Clipping functions
- `waveshaping.saturate`: Saturation functions
- `waveshaping.fold`: Wave folding functions
- `waveshaping.rectify`: Rectification functions
- `waveshaping.polynomial`: Polynomial waveshaping
- `waveshaping.special`: Special effects
- `waveshaping.utils`: Utility functions

## Examples

### Clipping

```python
import waveshaping.clip as clip

# Hard clipping with threshold
hard_clipped = clip.hard(signal, threshold=0.7)

# Soft clipping with drive
soft_clipped = clip.soft(signal, drive=3.0)

# Cubic smooth clipping
cubic_clipped = clip.cubic(signal)
```

### Saturation

```python
import waveshaping.saturate as saturate

# Tanh saturation
tanh_sat = saturate.tanh_sat(signal, drive=2.0)

# Tube-style saturation
tube_sat = saturate.tube_sat(signal, drive=1.5)

# Exponential saturation
exp_sat = saturate.exponential(signal, drive=1.2)
```

### Wave Folding

```python
import waveshaping.fold as fold

# Sine folding
sine_folded = fold.sine_fold(signal, threshold=0.8)

# Foldback distortion
foldback = fold.foldback(signal, threshold=0.6)

# Chebyshev polynomial folding
cheb_folded = fold.chebyshev_fold(signal, order=5)
```

## Requirements

- Python >= 3.7
- numpy >= 1.19.0
- scipy >= 1.5.0

## Development

### Installing for Development

```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black waveshaping/
```

## License

MIT License - see LICENSE file for details.

## Acknowledgments

This library is inspired by and ported from the C++ waveshaping library. Mathematical implementations are based on established digital signal processing literature including "DAFX - Digital Audio Effects" and "Designing Audio Effect Plugins in C++".

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.