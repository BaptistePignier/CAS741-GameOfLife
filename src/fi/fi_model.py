import numpy as np

class FiModel:
    def __init__(self, mu=0.5, sigma=0.15):
        self.mu = mu        # Centre de l'anneau
        self.sigma = sigma  # Largeur de l'anneau
        self.x = np.linspace(-2, 2, 100)
        self.R = 13        # Rayon du noyau (en pixels)
        self.ring_kernel = None
        
        self._update_ring_kernel()
    
    def _gauss(self, x, mu, sigma):
        """Fonction gaussienne pour créer le profil de l'anneau."""
        return np.exp(-0.5 * ((x-mu)/sigma)**2)
    
    def _update_ring_kernel(self):
        print("maj calc")
        y, x = np.ogrid[-self.R:self.R, -self.R:self.R]
        distance = np.sqrt((1+x)**2 + (1+y)**2) / self.R

        self.ring_kernel = self._gauss(distance, self.mu, self.sigma)
        self.ring_kernel[distance > 1] = 0               # Cut at d=1
        self.ring_kernel = self.ring_kernel / np.sum(self.ring_kernel)     # Normalize
        print(self.ring_kernel)
        
    def get_ring_kernel(self):
        """Retourne le noyau en anneau actuel."""
        return self.ring_kernel

    def get_x_values(self):
        """Retourne les valeurs de x pour le graphe de la gaussienne."""
        return self.x

    def set_parameters(self, mu=None, sigma=None):
        """Met à jour les paramètres de la fonction."""
        if mu is not None:
            self.mu = mu
        if sigma is not None:
            self.sigma = sigma
        if mu is not None or sigma is not None:
            self._update_ring_kernel()
            return self.ring_kernel
        return None
