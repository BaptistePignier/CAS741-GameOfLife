"""Simulation module.

This module provides components for the core simulation of cellular automata,
including model, view, and controller components for managing the grid state and visualization.
"""

from .sim_model import SimModel
from .sim_view import SimView
from .sim_controller import SimController

__all__ = ['SimModel', 'SimView', 'SimController']