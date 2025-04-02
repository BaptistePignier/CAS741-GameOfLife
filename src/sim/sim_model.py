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


        self.kernel_ring = None
        self.growth_lenia = None
    
    def set_kernel_ring(self, kernel_ring):
        self.kernel_ring = kernel_ring

    def set_growth_lenia(self, growth_lenia):
        self.growth_lenia = growth_lenia

    def growth_GoL(self, u):
        mask1 = (u >= 1) & (u <= 3)
        mask2 = (u > 3) & (u <= 4)
        return -1 + (u - 1) * mask1 + 8 * (1 - u/4) * mask2

    def update_discrete(self):
        NEIGHBORS_KERNEL = np.array([[1, 1, 1],
                               [1, 0, 1],
                               [1, 1, 1]], dtype=np.int8)
        neighbors = convolve2d(self.grid, NEIGHBORS_KERNEL, mode='same', boundary='wrap')
        
        self.grid = self.grid + self.growth_GoL(neighbors)
        self.grid = np.clip(self.grid, 0, 1)
    
    def update_continuous(self):
        neighbors = convolve2d(self.grid, self.kernel_ring, mode='same', boundary='wrap')
        self.grid = self.grid + 0.1 * self.growth_lenia(neighbors)
        self.grid = np.clip(self.grid, 0, 1)

    
    
    def get_grid(self):
        """Return the current grid.
        
        Returns:
            numpy.ndarray: Current grid of cells (0 = dead, 1 = alive)
        """
        return self.grid
