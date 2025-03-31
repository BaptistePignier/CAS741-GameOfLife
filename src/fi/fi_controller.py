import numpy as np

class FiController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Cache pour éviter les recalculs inutiles
        self.last_mu = None
        self.last_sigma = None
        self.last_growth_mu = None
        self.last_growth_sigma = None
        
        # Affichage initial
        self.update_display()
    
    def update_parameters(self, mu=None, sigma=None, growth_mu=None, growth_sigma=None):
        """Met à jour les paramètres et rafraîchit l'affichage."""
        # Évite les mises à jour si les paramètres n'ont pas changé
        if (mu == self.last_mu and sigma == self.last_sigma and 
            growth_mu == self.last_growth_mu and growth_sigma == self.last_growth_sigma):
            return
            
        # Mise à jour des paramètres et récupération du nouveau noyau si changé
        new_kernel = self.model.set_parameters(mu, sigma, growth_mu, growth_sigma)
        if new_kernel is not None:
            self.view.update_ring_plot(new_kernel)
        
        # Mise à jour du graphe gaussien
        x = self.model.get_x_values()
        if mu is not None or sigma is not None:
            y = self.model._gauss(x, self.model.mu, self.model.sigma)
            self.view.update_plot(x, y)
        
        if growth_mu is not None or growth_sigma is not None:
            y = self.model._gauss(x, self.model.growth_mu, self.model.growth_sigma)
            self.view.update_plot(x, y, is_growth=True)
        
        # Mise à jour du cache
        self.last_mu = mu
        self.last_sigma = sigma
        self.last_growth_mu = growth_mu
        self.last_growth_sigma = growth_sigma
    
    def update_display(self):
        """Met à jour tous les graphiques."""
        # Mise à jour du graphe gaussien
        x_values = self.model.get_x_values()
        y_values = self.model._gauss(x_values, self.model.mu, self.model.sigma)
        self.view.update_plot(x_values, y_values, max(y_values))
        
        # Mise à jour du filtre en anneau
        kernel = self.model.get_ring_kernel()
        self.view.update_ring_plot(kernel)
