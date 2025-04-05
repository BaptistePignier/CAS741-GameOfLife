import numpy as np

class FiModel:
    def __init__(self, mu=0.5, sigma=0.15, growth_mu=0.15, growth_sigma=0.015):
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


    def growth_GoL(self, u):

        """Fonction de croissance pour le Jeu de la Vie de Conway.
        Règles classiques: survie avec 2-3 voisins, naissance avec 3 voisins.
        Le paramètre u représente le nombre de voisins pour chaque cellule.
        Retourne les changements d'état (-1=mort, 0=inchangé, +1=naissance).

        """
        # Valeurs clés des règles du Jeu de la Vie
        SURVIVAL_MIN = 2  # Une cellule vivante survit avec au moins 2 voisins
        SURVIVAL_MAX = 3  # Une cellule vivante survit avec au plus 3 voisins

        BIRTH = 3         # Une cellule morte naît avec exactement 3 voisins

        # L'intervalle [1,3] capture les cas où u-1 génère le bon changement (+0 ou +1)

        mask1 = (u >= 1) & (u <= SURVIVAL_MAX)
 
        # L'intervalle ]3,4] capture le cas spécial entre 3 et 4 voisins

        mask2 = (u > BIRTH) & (u <= 4)
 
        return -1 + (u - 1) * mask1 + 8 * (1 - u/4) * mask2
    
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

    def set_nhood_params(self, mu=None, sigma=None):
        if mu is not None:
            self.mu = float(mu)
            
        if sigma is not None:
            self.sigma = float(sigma)
        self._update_con_nhood()

    def set_growth_params(self, g_mu=None, g_sigma=None):
        if g_mu is not None:
            self.growth_mu = float(g_mu)
            
        if g_sigma is not None:
            self.growth_sigma = float(g_sigma)
        
        


        
        
