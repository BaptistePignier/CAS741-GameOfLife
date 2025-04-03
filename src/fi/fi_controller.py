import numpy as np
from . import FiModel

class FiController:
    def __init__(self, view, us_controller):
        self.model = FiModel()
        self.view = view
        self.us_controller = us_controller

        # Initial display
        self.view.update_plots(self.model.ring_kernel,self.model.x,self.model.growth_lenia)

        self.us_controller.set_gaussian_commands(
            lambda x: self.update_parameters(mu=x),
            lambda x: self.update_parameters(sigma=x),
            lambda x: self.update_parameters(growth_mu=x),
            lambda x: self.update_parameters(growth_sigma=x)
        )
    
    def get_ring_kernel(self):
        """Retourne le kernel actuel pour utilisation par SimController."""
        return self.model.get_ring_kernel()

    def get_growth_lenia(self):
        """Retourne la fonction de croissance pour utilisation par SimController."""
        return self.model.growth_lenia
    
    def update_parameters(self, mu=None, sigma=None, growth_mu=None, growth_sigma=None):
        """Update parameters and refresh the display."""
        # Parameter update
        self.model.set_parameters(mu, sigma, growth_mu, growth_sigma)
        
        # Display update
        self.view.update_plots(self.model.ring_kernel,self.model.x,self.model.growth_lenia)
    
        
