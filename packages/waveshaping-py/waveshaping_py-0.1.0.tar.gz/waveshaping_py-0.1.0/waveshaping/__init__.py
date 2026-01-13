"""
waveshaping-py: A Python library for audio waveshaping and distortion effects.

This library provides mathematical waveshaping functions for audio signal processing,
ported from the C++ waveshaping library. Designed for non-realtime use with numpy arrays.
"""

from . import clip
from . import saturate
from . import fold
from . import rectify
from . import polynomial
from . import special
from . import utils

from ._version import __version__
__author__ = "Tsuguma Sayutani"
__description__ = "Python library for audio waveshaping and distortion effects"

__all__ = [
    "clip",
    "saturate", 
    "fold",
    "rectify",
    "polynomial",
    "special",
    "utils"
]