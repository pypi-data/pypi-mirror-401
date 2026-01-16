"""
Workflows module for per_datasets
"""

from .add import add
from .substract import subtract
from .pinn import pinn

__all__ = ['add', 'subtract', 'pinn']