"""
PER Datasets - A module for loading reservoir datasets
"""

__version__ = "0.0.3-alpha"

from .talkaholic.reservoir import Reservoir
from .reservoir import load_random, load
from .utils.init import initialize
from . import workflows
from .visual import Visualizer

# Instantiate the visualizer as a singleton object for generic access
visual = Visualizer()

__all__ = ['load_random', 'load', 'Reservoir', '__version__', 'initialize', 'workflows', 'visual']