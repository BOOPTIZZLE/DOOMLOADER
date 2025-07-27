"""
DOOMLOADER - Neural Amp Modeler (NAM) File Support
A tool for loading and processing NAM files for amp simulation.
"""

__version__ = "1.0.0"
__author__ = "DOOMLOADER Team"

from .nam_loader import NAMLoader
from .amp_simulator import AmpSimulator
from .file_handler import FileHandler

__all__ = ['NAMLoader', 'AmpSimulator', 'FileHandler']