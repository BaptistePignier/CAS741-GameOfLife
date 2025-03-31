import numpy as np
from scipy.signal import convolve2d

class SimModel:
    # Kernel pré-calculé pour le calcul des voisins
    
    
    def __init__(self, width=500, height=500, initial_alive_prob=0.2):
        """Initialise le modèle de simulation.
        
        Args:
            width (int): Largeur de la grille en cellules
            height (int): Hauteur de la grille en cellules
            initial_alive_prob (float): Probabilité initiale qu'une cellule soit vivante
        """
        self.width = width
        self.height = height
        self.initial_alive_prob = initial_alive_prob
        # Utilise int8 au lieu de int64 pour réduire l'utilisation mémoire
        self.grid = np.zeros((height, width), dtype=np.int8)
        self.reset()
    
    def growth_GoL(self, u):
        mask1 = (u >= 1) & (u <= 3)
        mask2 = (u > 3) & (u <= 4)    
        return -1 + (u - 1) * mask1 + 8 * (1 - u/4) * mask2

    def update(self):
        """Calcule la génération suivante du jeu de la vie.
        
        Utilise une convolution 2D avec un kernel pré-calculé pour compter les voisins,
        puis applique les règles du jeu de la vie de manière vectorisée.
        """
        NEIGHBORS_KERNEL = np.array([[1, 1, 1],
                               [1, 0, 1],
                               [1, 1, 1]], dtype=np.int8)
        # Calcul optimisé des voisins avec le kernel pré-calculé
        neighbors = convolve2d(self.grid, NEIGHBORS_KERNEL,
                             mode='same', boundary='wrap')
        
        # Application vectorisée des règles du jeu
        # Une cellule survit si elle a 2 ou 3 voisins
        # Une cellule naît si elle a exactement 3 voisins
        
        # Mise à jour de la grille en une seule opération
        self.grid = self.grid + self.growth_GoL(neighbors)
        self.grid = np.clip(self.grid, 0, 1)
    
   

    def reset(self, prob=None):
        """Réinitialise la grille avec une nouvelle configuration aléatoire.
        
        Args:
            prob (float, optional): Nouvelle probabilité pour les cellules vivantes.
                                  Si None, utilise la probabilité initiale.
        """
        if prob is not None and 0 <= prob <= 1:
            self.initial_alive_prob = prob
            
        # Génération optimisée de la grille aléatoire
        self.grid = np.random.choice(
            [0, 1],
            self.width * self.height,
            p=[1-self.initial_alive_prob, self.initial_alive_prob]
        ).reshape(self.height, self.width).astype(np.int8)
    
    def get_grid(self):
        """Retourne la grille actuelle.
        
        Returns:
            numpy.ndarray: Grille actuelle de cellules (0 = morte, 1 = vivante)
        """
        return self.grid
