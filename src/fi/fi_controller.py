import numpy as np

class FiController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Affichage initial
        self.update_display()
    
    def update_parameters(self, mu=None, sigma=None):
        """Met à jour les paramètres et rafraîchit l'affichage."""
        # Mise à jour des paramètres et récupération du nouveau noyau si changé
        new_kernel = self.model.set_parameters(mu, sigma)
        if new_kernel is not None:
            self.view.update_ring_plot(new_kernel)
        
        # Mise à jour du graphe gaussien
        x = self.model.get_x_values()
        y = self.model._gauss(x, self.model.mu, self.model.sigma)
        self.view.update_plot(x, y)
    
    def update_display(self):
        """Met à jour tous les graphiques."""
        # Mise à jour du graphe gaussien
        x_values = self.model.get_x_values()
        y_values = self.model._gauss(x_values, self.model.mu, self.model.sigma)
        self.view.update_plot(x_values, y_values, max(y_values))
        
        # Mise à jour du filtre en anneau
        kernel = self.model.get_ring_kernel()
        self.view.update_ring_plot(kernel)
