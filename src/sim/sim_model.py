import numpy as np
from scipy.signal import convolve2d

class SimModel:
    # Pre-calculated kernel for neighbor calculation
    
    
    def __init__(self, width=500, height=500, initial_alive_prob=0.2):
        """Initialize the simulation model.
        
        Args:
            width (int): Grid width in cells
            height (int): Grid height in cells
            initial_alive_prob (float): Initial probability for a cell to be alive
        """
        self.width = width
        self.height = height
        self.initial_alive_prob = initial_alive_prob

    def update(self,fct,nhood,dt):
        neighbors = convolve2d(self.grid, nhood, mode='same', boundary='wrap')
        self.grid = self.grid + dt * fct(neighbors)
        self.grid = np.clip(self.grid, 0, 1)
    
    def get_grid(self):
        """Return the current grid.
        
        Returns:
            numpy.ndarray: Current grid of cells (0 = dead, 1 = alive)
        """
        return self.grid


    def reset_discrete(self, prob=None):
        """Reset the grid with a new random configuration.
        
        Args:
            prob (float, optional): New probability for live cells.
                                  If None, uses the initial probability.
        """
        if prob is not None and 0 <= prob <= 1:
            self.initial_alive_prob = prob
            
        # Optimized generation of the random grid
        self.grid = np.random.choice(
            [0, 1],
            self.width * self.height,
            p=[1-self.initial_alive_prob, self.initial_alive_prob]
        ).reshape(self.height, self.width).astype(np.int8)

    def reset_continuous(self):
        N = 256
        M = int(np.ceil((16*N)/9))
        self.grid = np.ones((M, N))
        # Gaussian spot centered in the middle
        radius = 36
        y, x = np.ogrid[-N//2:N//2, -M//2:M//2]
        self.grid = np.exp(-0.5 * (x*x + y*y) / (radius*radius))
