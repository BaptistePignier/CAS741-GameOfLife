"""Function influence module.

This module provides components for managing and visualizing the influence functions
used in cellular automata, including growth functions and neighborhood kernels.
"""

__all__ = ['FiModel', 'FiView', 'FiController']

# Import classes when accessed, not at module load time
from .fi_model import FiModel
from .fi_view import FiView
from .fi_controller import FiController
