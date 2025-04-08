"""Simulation model module.

This module provides the model component for the cellular automata simulation.
It defines the core grid structure and state, implements the update rules for both
discrete (Game of Life) and continuous (Lenia) cellular automata, and provides
various initialization patterns for the grid. The model applies update rules using
convolution with neighborhood kernels and growth functions.
"""

from typing import Callable, Optional
import numpy as np
from scipy.signal import convolve2d

class SimModel:
    """Simulation model component.
    
    This class represents the core simulation model for cellular automata.
    It manages the grid state and provides methods for updating and resetting the simulation.
    """
    # Pre-calculated kernel for neighbor calculation
    
    
    def __init__(self, 
                 width: int = 100, 
                 height: int = 100, 
                 initial_alive_prob: 
                 float = 0.2) -> None:
        
        """Initialize the simulation model.
        
        Args:
            width (int): Grid width in cells
            height (int): Grid height in cells
            initial_alive_prob (float): Initial probability for a cell to be alive
        """
        self.width = width
        self.height = height
        self.initial_alive_prob = initial_alive_prob
        self.grid = None

    def update(self, fct: Callable[[np.ndarray], np.ndarray], nhood: np.ndarray, dt: float) -> None:
        """Update the grid state for one generation.
        
        Applies the cellular automata rules by convolving the neighborhood kernel
        with the current grid, then applying the growth function.
        
        Args:
            fct (function): Growth function to apply
            nhood (numpy.ndarray): Neighborhood kernel
            dt (float): Time step (1.0 for discrete, smaller for continuous)
        """
        neighbors = convolve2d(self.grid, nhood, mode='same', boundary='wrap')
        self.grid = self.grid + dt * fct(neighbors)
        self.grid = np.clip(self.grid, 0, 1)
    
    def get_grid(self) -> np.ndarray:
        """Return the current grid.
        
        Returns:
            numpy.ndarray: Current grid of cells (0 = dead, 1 = alive)
        """
        return self.grid

    def reset_discrete(self, num: int) -> None:
        match num:
            case 0:
                self.random()
            case 1:
                self.planner()
            case _:
                return

    def planner(self) -> None:
        glider_gun = np.array(
            [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

        self.grid = np.zeros((self.width, self.height))
        pos_x = self.width//6
        pos_y = self.height//6
        self.grid[pos_x:(pos_x + glider_gun.shape[1]), pos_y:(pos_y + glider_gun.shape[0])] = glider_gun.T


    def random(self) -> None:
        """Reset the grid with a new random configuration."""
            
        # Optimized generation of the random grid
        self.grid = np.random.choice(
            [0, 1],
            self.width * self.height,
            p=[1-self.initial_alive_prob, self.initial_alive_prob]
        ).reshape(self.height, self.width).astype(np.int8)

    def reset_continuous(self, num: int) -> None:
        """Reset the grid with a continuous pattern based on the numeric value.
        
        Args:
            num (int): Pattern selector:
                - 0: Stain pattern (centered Gaussian spot)
                - 1: Orbium pattern (Lenia spaceship)
                - Other values: No action
        """
        match num:
            case 0:
                self.stain()
            case 1:
                self.orbium()
            case _:
                return

    def stain(self) -> None:
        """Create a centered Gaussian stain pattern.
        
        Initializes the grid with a circular Gaussian pattern centered in the middle.
        """
        n = 256
        m = int(np.ceil((16*n)/9))
        self.grid = np.ones((m, n))
        # Gaussian spot centered in the middle
        radius = 36
        y, x = np.ogrid[-n//2:n//2, -n//2:n//2]
        self.grid = np.exp(-0.5 * (x*x + y*y) / (radius*radius))


    def orbium(self) -> None:
        """Create an Orbium pattern (Lenia spaceship).
        
        Initializes the grid with a pre-defined Orbium pattern, 
        a self-propelled particle in Lenia.
        """
        orbium = np.array([[0,0,0,0,0,0,0.1,0.14,0.1,0,0,0.03,0.03,0,0,0.3,0,0,0,0], [0,0,0,0,0,0.08,0.24,0.3,0.3,0.18,0.14,0.15,0.16,0.15,0.09,0.2,0,0,0,0], [0,0,0,0,0,0.15,0.34,0.44,0.46,0.38,0.18,0.14,0.11,0.13,0.19,0.18,0.45,0,0,0], [0,0,0,0,0.06,0.13,0.39,0.5,0.5,0.37,0.06,0,0,0,0.02,0.16,0.68,0,0,0], [0,0,0,0.11,0.17,0.17,0.33,0.4,0.38,0.28,0.14,0,0,0,0,0,0.18,0.42,0,0], [0,0,0.09,0.18,0.13,0.06,0.08,0.26,0.32,0.32,0.27,0,0,0,0,0,0,0.82,0,0], [0.27,0,0.16,0.12,0,0,0,0.25,0.38,0.44,0.45,0.34,0,0,0,0,0,0.22,0.17,0], [0,0.07,0.2,0.02,0,0,0,0.31,0.48,0.57,0.6,0.57,0,0,0,0,0,0,0.49,0], [0,0.59,0.19,0,0,0,0,0.2,0.57,0.69,0.76,0.76,0.49,0,0,0,0,0,0.36,0], [0,0.58,0.19,0,0,0,0,0,0.67,0.83,0.9,0.92,0.87,0.12,0,0,0,0,0.22,0.07], [0,0,0.46,0,0,0,0,0,0.7,0.93,1,1,1,0.61,0,0,0,0,0.18,0.11], [0,0,0.82,0,0,0,0,0,0.47,1,1,0.98,1,0.96,0.27,0,0,0,0.19,0.1], [0,0,0.46,0,0,0,0,0,0.25,1,1,0.84,0.92,0.97,0.54,0.14,0.04,0.1,0.21,0.05], [0,0,0,0.4,0,0,0,0,0.09,0.8,1,0.82,0.8,0.85,0.63,0.31,0.18,0.19,0.2,0.01], [0,0,0,0.36,0.1,0,0,0,0.05,0.54,0.86,0.79,0.74,0.72,0.6,0.39,0.28,0.24,0.13,0], [0,0,0,0.01,0.3,0.07,0,0,0.08,0.36,0.64,0.7,0.64,0.6,0.51,0.39,0.29,0.19,0.04,0], [0,0,0,0,0.1,0.24,0.14,0.1,0.15,0.29,0.45,0.53,0.52,0.46,0.4,0.31,0.21,0.08,0,0], [0,0,0,0,0,0.08,0.21,0.21,0.22,0.29,0.36,0.39,0.37,0.33,0.26,0.18,0.09,0,0,0], [0,0,0,0,0,0,0.03,0.13,0.19,0.22,0.24,0.24,0.23,0.18,0.13,0.05,0,0,0,0], [0,0,0,0,0,0,0,0,0.02,0.06,0.08,0.09,0.07,0.05,0.01,0,0,0,0,0]]) # pylint: disable=C0301
        n = 128
        m = int(np.ceil((16*n)/9))
        self.grid = np.zeros((n, m))
        pos_x = m//6
        pos_y = n//6
        self.grid[pos_x:(pos_x + orbium.shape[1]), pos_y:(pos_y + orbium.shape[0])] = orbium.T
        
