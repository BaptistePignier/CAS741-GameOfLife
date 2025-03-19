import numpy as np
from scipy.signal import convolve2d

class SimModel:
    def __init__(self, size=500, initial_alive_prob=0.2):
        self.size = size
        self.grid = np.random.choice([0, 1], size*size, p=[1-initial_alive_prob, initial_alive_prob]).reshape(size, size)
    
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
        self.grid = np.random.choice([0, 1], self.size*self.size, 
                                   p=[1-initial_alive_prob, initial_alive_prob]).reshape(self.size, self.size)
    
    def get_grid(self):
        """Retourne la grille actuelle."""
        return self.grid
