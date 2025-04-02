import numpy as np

class FiModel:
    def __init__(self, mu=0.5, sigma=0.15, growth_mu=0.5, growth_sigma=0.15):
        self.mu = mu        # Center of the ring
        self.sigma = sigma  # Width of the ring
        self.growth_mu = growth_mu
        self.growth_sigma = growth_sigma
        self.R = 13        # Kernel radius (in pixels)
        self.ring_kernel = None
        
        self._update_ring_kernel()
    
    def _gauss(self, x, mu, sigma):
        """Gaussian function to create the ring profile."""
        return np.exp(-0.5 * ((x-mu)/sigma)**2)

    def growth_lenia(self, u):
        return -1 + 2 * self._gauss(u, self.growth_mu, self.growth_sigma)        # Baseline -1, peak +1

    def _update_ring_kernel(self):
        """Update the ring kernel and return it."""
        y, x = np.ogrid[-self.R:self.R, -self.R:self.R]
        distance = np.sqrt((1+x)**2 + (1+y)**2) / self.R

        self.ring_kernel = self._gauss(distance, self.mu, self.sigma)
        self.ring_kernel[distance > 1] = 0               # Cut at d=1
        self.ring_kernel = self.ring_kernel / np.sum(self.ring_kernel)     # Normalize
        return self.ring_kernel
    
    def get_ring_kernel(self):
        """Return the current ring kernel."""
        return self.ring_kernel

    def set_parameters(self, mu=None, sigma=None, growth_mu=None, growth_sigma=None):
        """Update parameters and recalculate the kernel if necessary."""
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
