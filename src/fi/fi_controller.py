import numpy as np
from . import FiModel

class FiController:
    def __init__(self, view, us_controller):
        self.model = FiModel()
        self.view = view
        self.us_controller = us_controller

        # Affichage initial
        self._update_display()

        self.us_controller.set_gaussian_commands(
            lambda x: self.update_parameters(mu=x),
            lambda x: self.update_parameters(sigma=x),
            lambda x: self.update_parameters(growth_mu=x),
            lambda x: self.update_parameters(growth_sigma=x)
        )
    
    def get_ring_kernel(self):
        return self.model.get_ring_kernel()
    
    def update_parameters(self, mu=None, sigma=None, growth_mu=None, growth_sigma=None):
        """Met à jour les paramètres et rafraîchit l'affichage."""

        # Mise à jour des paramètres
        self.model.set_parameters(mu, sigma, growth_mu, growth_sigma)
        
        # Mise à jour de l'affichage
        self._update_display()
    
    def _update_display(self):
        """Met à jour tous les éléments d'affichage."""
        # Création des valeurs x pour les deux graphiques
        x = np.linspace(-2, 2, 100)
        
        # Mise à jour du graphique de l'anneau
        self.view.update_ring_plot(self.model.get_ring_kernel())
        
        # Mise à jour des graphiques gaussiens
        y_ring = self.model._gauss(x, self.model.mu, self.model.sigma)
        self.view.update_gaussian_plot(x, y_ring)
        
        y_growth = self.model._gauss(x, self.model.growth_mu, self.model.growth_sigma)
        self.view.update_growth_plot(x, y_growth)
