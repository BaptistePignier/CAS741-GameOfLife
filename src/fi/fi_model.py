import numpy as np

class FiModel:
    def __init__(self, mu=0.5, sigma=0.15, growth_mu=0.5, growth_sigma=0.15):
        self.mu = mu        # Center of the ring
        self.sigma = sigma  # Width of the ring
        self.growth_mu = growth_mu
        self.growth_sigma = growth_sigma
        self.R = 13        # Kernel radius (in pixels)
        self.con_nhood = None
        
        self.dis_nhood = np.array([ [0, 0, 0, 0, 0],
                                    [0, 1, 1, 1, 0],
                                    [0, 1, 0, 1, 0],
                                    [0, 1, 1, 1, 0],
                                    [0, 0, 0, 0, 0]], dtype=np.int8)

        self.x = np.linspace(-2, 2, 1000)

        self._update_con_nhood()
        
    
    def _gauss(self, x, mu, sigma):
        """Gaussian function to create the ring profile."""
        return np.exp(-0.5 * ((x-mu)/sigma)**2)

    def growth_lenia(self, u):
        return -1 + 2 * self._gauss(u, self.growth_mu, self.growth_sigma)        # Baseline -1, peak +1

    def _update_con_nhood(self):
        """Update the connectivity neighborhood and return it."""
        y, x = np.ogrid[-self.R:self.R, -self.R:self.R]
        distance = np.sqrt((1+x)**2 + (1+y)**2) / self.R

        self.con_nhood = self._gauss(distance, self.mu, self.sigma)
        self.con_nhood[distance > 1] = 0               # Cut at d=1
        self.con_nhood = self.con_nhood / np.sum(self.con_nhood)     # Normalize


    def get_con_nhood(self):
        """Return the current connectivity neighborhood."""
        return self.con_nhood
    
    def get_dis_nhood(self):
        """Return the current connectivity neighborhood."""
        return self.dis_nhood

    def set_parameters(self, mu=None, sigma=None, growth_mu=None, growth_sigma=None):
        """Update parameters and recalculate the kernel if necessary."""
        
        if mu is not None:
            self.mu = float(mu)
            
        if sigma is not None:
            self.sigma = float(sigma)
            
        if growth_mu is not None:
            self.growth_mu = float(growth_mu)
            
        if growth_sigma is not None:
            self.growth_sigma = float(growth_sigma)
        
        self._update_con_nhood()
        


        
        
