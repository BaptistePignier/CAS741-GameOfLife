import numpy as np

def growth_gol(u):

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

        # Ici on encode :
        # - birth → +1
        # - survive → 0
        # - death → -1

        return 1 * mask_birth + 0 * mask_survive -1 * mask_death



print(growth_gol()