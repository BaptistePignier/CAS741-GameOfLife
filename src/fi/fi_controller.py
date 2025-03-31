import numpy as np
from . import FiModel

class FiController:
    def __init__(self, view):
        self.model = FiModel()
        self.view = view

        # Affichage initial
        self._update_display()
    
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
