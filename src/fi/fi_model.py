from typing import Optional, Union
import numpy as np


class FiModel:
    def __init__(self,  mu: float = 0.5, 
                        sigma: float = 0.15, 
                        growth_mu: float = 0.15, 
                        growth_sigma: float = 0.015) -> None:
        
        """Initialize the functional input model.
        
        Args:
            mu (float): Center of the kernel ring. Default is 0.5.
            sigma (float): Width of the kernel ring. Default is 0.15.
            growth_mu (float): Center parameter for growth function. Default is 0.15.
            growth_sigma (float): Width parameter for growth function. Default is 0.015.
        """
        self.mu = mu        # Center of the ring
        self.sigma = sigma  # Width of the ring
        self.growth_mu = growth_mu
        self.growth_sigma = growth_sigma
        
        self.con_nhood = None
        
        self.dis_nhood = np.array([ [0, 0, 0, 0, 0],
                                    [0, 1, 1, 1, 0],
                                    [0, 1, 0, 1, 0],
                                    [0, 1, 1, 1, 0],
                                    [0, 0, 0, 0, 0]], dtype=np.int8)
        self._update_con_nhood()
        
    
    def _gauss(self, 
               x: Union[float, np.ndarray], 
               mu: float, 
               sigma: float) -> Union[float, np.ndarray]:
        
        """Compute a Gaussian function.
        
        Calculates the Gaussian function value at point(s) x with given parameters.
        
        Args:
            x (float or numpy.ndarray): Input value(s) where to evaluate the function
            mu (float): Center of the Gaussian (mean)
            sigma (float): Width of the Gaussian (standard deviation)
            
        Returns:
            float or numpy.ndarray: Gaussian function values at the input points
        """
        return np.exp(-0.5 * ((x-mu)/sigma)**2)

    def growth_lenia(self, u: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Compute the Lenia growth function.
        
        The Lenia growth function is a continuous function based on a Gaussian.
        It maps input values to the range [-1, 1], with a peak at growth_mu.
        
        Args:
            u (float or numpy.ndarray): Input value(s), represents the potential
            
        Returns:
            float or numpy.ndarray: Growth values ranging from -1 to 1
        """
        # Baseline -1, peak +1
        return -1 + 2 * self._gauss(u, self.growth_mu, self.growth_sigma)
        
    def growth_gol(self,u):

        """Compute the Game of Life growth function.
        
        Implements the rules of Conway's Game of Life as a continuous function.
        Classic rules are: survival with 2-3 neighbors, birth with exactly 3 neighbors.
        
        Args:
            u (float or numpy.ndarray): Input value(s), represents the number of neighbors
            
        Returns:
            float or numpy.ndarray: Growth values where:
                - Positive values indicate birth or survival
                - Negative values indicate death
                - Value magnitude indicates the strength of the change
        """
        
        mask_birth = u == 3
        mask_survive = (u == 2) | (u == 3)
        
        mask_death = ~(mask_birth | mask_survive)

        # - birth → +1
        # - survive → 0
        # - death → -1

        return 1 * mask_birth + 0 * mask_survive -1 * mask_death

    def _update_con_nhood(self) -> None:
        """Update the continuous neighborhood kernel.
        
        Generates a 2D Gaussian ring pattern based on the current mu and sigma values.
        The kernel is normalized so the sum of all elements equals 1.
        """
        r = 13
        y, x = np.ogrid[-r:r, -r:r]
        distance = np.sqrt((1+x)**2 + (1+y)**2) / r

        self.con_nhood = self._gauss(distance, self.mu, self.sigma)
        self.con_nhood[distance > 1] = 0               # Cut at d=1
        self.con_nhood = self.con_nhood / np.sum(self.con_nhood)     # Normalize


    def get_con_nhood(self) -> np.ndarray:
        """Get the continuous neighborhood kernel.
        
        Returns:
            numpy.ndarray: 2D array representing the continuous neighborhood kernel
        """
        return self.con_nhood
    
    def get_dis_nhood(self) -> np.ndarray:
        """Get the discrete neighborhood kernel.
        
        Returns:
            numpy.ndarray: 2D array representing the discrete neighborhood (Moore neighborhood)
        """
        return self.dis_nhood

    def set_nhood_params(self, mu: Optional[float] = None, sigma: Optional[float] = None) -> None:
        """Set the parameters for the continuous neighborhood.
        
        Updates the mu and/or sigma parameters and recalculates the continuous
        neighborhood kernel.
        
        Args:
            mu (float, optional): New center value for the ring. If None, keeps current value.
            sigma (float, optional): New width value for the ring. If None, keeps current value.
        """
        if mu is not None:
            self.mu = float(mu)
            
        if sigma is not None:
            self.sigma = float(sigma)
        self._update_con_nhood()

    def set_growth_params(self, 
                          g_mu: Optional[float] = None, 
                          g_sigma: Optional[float] = None) -> None:
        
        """Set the parameters for the growth function.
        
        Updates the growth_mu and/or growth_sigma parameters used by the growth functions.
        
        Args:
            g_mu (float, optional): New center value for growth function. 
            If None, keeps current value.

            g_sigma (float, optional): New width value for growth function. 
            If None, keeps current value.
        """
        if g_mu is not None:
            self.growth_mu = float(g_mu)
            
        if g_sigma is not None:
            self.growth_sigma = float(g_sigma)
        
        


        
        
