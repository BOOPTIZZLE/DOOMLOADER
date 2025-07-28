"""
DOOMLOADER - Audio file loader and processor

A Python library for loading and processing audio files with various effects.
"""

__version__ = "0.1.0-alpha"
__author__ = "BOOPTIZZLE"

from .loader import AudioLoader
from .processor import AudioProcessor

__all__ = ["AudioLoader", "AudioProcessor"]