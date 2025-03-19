import numpy as np

class FiModel:
    def __init__(self, alpha=1.0, beta=1.0):
        self.alpha = alpha  # amplitude
        self.beta = beta    # largeur
        self.x = np.linspace(-2, 2, 100)
    
    def calculate(self):
        """Calcule les valeurs de la fonction gaussienne."""
        return self.alpha * np.exp(-self.beta * self.x**2)
    
    def set_parameters(self, alpha=None, beta=None):
        """Met à jour les paramètres de la fonction."""
        if alpha is not None:
            self.alpha = alpha
        if beta is not None:
            self.beta = beta
    
    def get_x_values(self):
        """Retourne les valeurs x."""
        return self.x
