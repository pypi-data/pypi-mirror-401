# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet

### Changed
- Nothing yet

### Fixed
- Nothing yet

## [0.1.0] - 2026-01-10

### Added
- Initial release of waveshaping-py library
- Complete port from C++ waveshaping library
- Support for clipping effects:
  - Hard clipping with adjustable threshold
  - Soft clipping using tanh
  - Cubic smooth clipping
  - Arctangent clipping
  - Algebraic clipping
  - Soft limit clipping
  - Sinusoidal clipping
- Support for saturation effects:
  - Tanh saturation with drive control
  - Tube-style asymmetric saturation
  - Exponential saturation
  - Gaussian saturation
  - Error function saturation
  - Power saturation with adjustable exponent
  - Sigmoid saturation
- Support for wave folding effects:
  - Sine wave folding
  - Aggressive foldback distortion
  - Triangle wave folding
  - Bipolar folding
  - Soft folding using tanh
  - Chebyshev polynomial folding
- Support for rectification effects:
  - Half-wave rectification
  - Full-wave rectification
  - Precision rectifier with threshold
  - Soft rectification with smooth transition
  - Tube-style rectification with knee
  - Envelope follower
  - Peak detector with decay
- Support for polynomial waveshaping:
  - Quadratic polynomial
  - Cubic polynomial
  - Quartic polynomial
  - Odd polynomial (odd harmonics only)
  - Even polynomial (even harmonics only)
  - Legendre polynomial series
  - Hermite polynomial series
  - Custom polynomial with arbitrary coefficients
  - Normalized polynomial with amplitude control
- Support for special effects:
  - Bitcrushing with adjustable bit depth
  - Ring modulation
  - Amplitude modulation
  - Sample and hold
  - Noise gating
  - Wavetable-based waveshaping
  - Chaos generation using logistic map
  - Frequency shifting
  - Granular effects
- Utility functions:
  - Value clamping with NaN handling
  - Safe division
  - Signal normalization
  - Sign function
  - Fast tanh approximation
- Comprehensive test suite
- Example scripts and Jupyter notebook tutorial
- Complete documentation with usage examples
- Type hints for better IDE support
- Support for both scalar and array inputs
- NumPy-based implementation optimized for non-realtime use

### Technical Details
- Python 3.7+ support
- Dependencies: numpy >= 1.19.0, scipy >= 1.5.0
- MIT License
- Packaging ready for PyPI distribution
- Development tools configuration (black, flake8, mypy, pytest)

### Documentation
- Comprehensive README with installation and usage instructions
- API documentation with parameter descriptions
- Jupyter notebook tutorial with visualizations
- Example scripts demonstrating all features
- Mathematical background and algorithm references