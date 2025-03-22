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
        """Met à jour le noyau en anneau avec un profil gaussien."""
        # Créer la matrice de distance
        y, x = np.ogrid[-self.R:self.R+1, -self.R:self.R+1]
        # Distance normalisée par rapport au rayon (entre 0 et 1)
        distance = np.sqrt(x*x + y*y) / self.R
        
        # Créer l'anneau avec un profil gaussien
        self.ring_kernel = self._gauss(distance, self.mu, self.sigma)
        
        # Couper à distance = 1 (au-delà du rayon)
        self.ring_kernel[distance > 1] = 0
        
        # Normaliser pour que la somme soit 1
        self.ring_kernel = self.ring_kernel / np.sum(self.ring_kernel)
    
    def set_parameters(self, mu=None, sigma=None):
        """Met à jour les paramètres de la fonction."""
        update_needed = False
        if mu is not None:
            self.mu = mu
            update_needed = True
        if sigma is not None:
            self.sigma = sigma
            update_needed = True
        if update_needed:
            self._update_ring_kernel()
    
    def get_x_values(self):
        """Retourne les valeurs de x pour le graphe de la gaussienne."""
        return self.x
    
    def get_ring_kernel(self):
        """Retourne le noyau en anneau normalisé."""
        return self.ring_kernel
