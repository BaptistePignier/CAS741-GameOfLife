import numpy as np

class FiModel:
    def __init__(self, mu=0.5, sigma=0.15, growth_mu=0.5, growth_sigma=0.15):
        self.mu = mu        # Centre de l'anneau
        self.sigma = sigma  # Largeur de l'anneau
        self.growth_mu = growth_mu
        self.growth_sigma = growth_sigma
        self.R = 13        # Rayon du noyau (en pixels)
        self.ring_kernel = None
        
        self._update_ring_kernel()
    
    def _gauss(self, x, mu, sigma):
        """Fonction gaussienne pour créer le profil de l'anneau."""
        return np.exp(-0.5 * ((x-mu)/sigma)**2)

    def growth_lenia(self, u):
        return -1 + 2 * self._gauss(u, self.growth_mu, self.growth_sigma)        # Baseline -1, peak +1

    def _update_ring_kernel(self):
        """Met à jour le noyau en anneau et le retourne."""
        y, x = np.ogrid[-self.R:self.R, -self.R:self.R]
        distance = np.sqrt((1+x)**2 + (1+y)**2) / self.R

        self.ring_kernel = self._gauss(distance, self.mu, self.sigma)
        self.ring_kernel[distance > 1] = 0               # Cut at d=1
        self.ring_kernel = self.ring_kernel / np.sum(self.ring_kernel)     # Normalize
        return self.ring_kernel
    
    def get_ring_kernel(self):
        """Retourne le noyau en anneau actuel."""
        return self.ring_kernel

    def set_parameters(self, mu=None, sigma=None, growth_mu=None, growth_sigma=None):
        """Met à jour les paramètres et recalcule le noyau si nécessaire."""
        update_kernel = False
        
        if mu is not None:
            self.mu = float(mu)
            update_kernel = True
            
        if sigma is not None:
            self.sigma = float(sigma)
            update_kernel = True
            
        if growth_mu is not None:
            self.growth_mu = float(growth_mu)
            
        if growth_sigma is not None:
            self.growth_sigma = float(growth_sigma)
        
        return self._update_ring_kernel() if update_kernel else None
