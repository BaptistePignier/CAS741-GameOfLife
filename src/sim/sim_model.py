import numpy as np
from scipy.signal import convolve2d

class SimModel:
    def __init__(self, width=500, height=500, initial_alive_prob=0.2):
        self.width = width
        self.height = height
        self.grid = np.random.choice(
            [0, 1],
            width * height,
            p=[1-initial_alive_prob, initial_alive_prob]
        ).reshape(height, width)  # Note: numpy utilise (rows, cols) = (height, width)
    
    def update(self):
        """Calcule la génération suivante du jeu de la vie."""
        kernel = np.array([[1, 1, 1],
                          [1, 0, 1],
                          [1, 1, 1]])
        neighbors = convolve2d(self.grid, kernel, mode='same', boundary='wrap')
        new_grid = (neighbors == 3) | ((self.grid == 1) & (neighbors == 2))
        self.grid = new_grid.astype(int)
    
    def reset(self, initial_alive_prob=0.2):
        """Réinitialise la grille avec une nouvelle configuration aléatoire."""
        self.grid = np.random.choice(
            [0, 1],
            self.width * self.height,
            p=[1-initial_alive_prob, initial_alive_prob]
        ).reshape(self.height, self.width)
    
    def get_grid(self):
        """Retourne la grille actuelle."""
        return self.grid
