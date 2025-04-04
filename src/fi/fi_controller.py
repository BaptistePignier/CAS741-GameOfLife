import numpy as np
from . import FiModel

class FiController:
    def __init__(self, view, us_controller):
        self.model = FiModel()
        self.view = view
        self.us_controller = us_controller

        # Initial display
        self._update_display()

        self.us_controller.set_gaussian_commands(
            lambda x: self.update_parameters(mu=x),
            lambda x: self.update_parameters(sigma=x),
            lambda x: self.update_parameters(growth_mu=x),
            lambda x: self.update_parameters(growth_sigma=x)
        )
    
    def get_con_nhood(self):
        return self.model.get_con_nhood()


    def get_dis_nhood(self):
        return self.model.get_dis_nhood()
    
    def get_growth_lenia(self):
        return self.model.growth_lenia
    
    def update_parameters(self, mu=None, sigma=None, growth_mu=None, growth_sigma=None):
        """Update parameters and refresh the display."""
        # Parameter update
        self.model.set_parameters(mu, sigma, growth_mu, growth_sigma)
        
        # Display update
        self._update_display()
    
    def _update_display(self):
        """Update all display elements."""
        # Create x values for growth graph
        x = np.linspace(-2, 2, 1000)
        
        # Update the nhood plot
        if self.us_controller.is_mode_continuous():

            self.view.update_nhood_plot(self.model.get_con_nhood())
        else:
            self.view.update_nhood_plot(self.model.get_dis_nhood())
        
        # Update the growth plot
        y_growth = self.model._gauss(x, self.model.growth_mu, self.model.growth_sigma)
        self.view.update_growth_plot(x, y_growth)
    
        
