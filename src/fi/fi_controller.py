import numpy as np
from . import FiModel

class FiController:
    def __init__(self, view, us_controller):
        self.model = FiModel()
        self.view = view
        self.us_controller = us_controller

        # Initial display
        self.update_displays()

        self.us_controller.set_interface_commands(
            lambda x: self.update_nhood_params(mu=x),
            lambda x: self.update_nhood_params(sigma=x),
            lambda x: self.update_growth_params(g_mu=x),
            lambda x: self.update_growth_params(g_sigma=x),
            lambda : self.update_displays()
        )
    
    def get_nhood(self):
        if self.us_controller.is_mode_continuous():
            return self.model.get_con_nhood()
        return self.model.get_dis_nhood()

    
    def get_growth_fct(self):
        if self.us_controller.is_mode_continuous():

            return self.model.growth_lenia
        return self.model.growth_GoL

    def get_step(self):
        if self.us_controller.is_mode_continuous():
            return 0.1
        return 1

    def update_nhood_params(self, mu=None, sigma=None):
        self.model.set_nhood_params(mu,sigma)
        self.update_nhood_display()

    def update_growth_params(self, g_mu=None, g_sigma=None):
        self.model.set_growth_params(g_mu,g_sigma)
        self.update_growth_display()

    
    def update_nhood_display(self):
        # Update the nhood plot
        if self.us_controller.is_mode_continuous():
            self.view.update_nhood_plot(self.model.get_con_nhood())
        else:
            self.view.update_nhood_plot(self.model.get_dis_nhood())

    def update_growth_display(self):
        # Update the growth plot
        if self.us_controller.is_mode_continuous():
            x = np.arange(0, 0.3, 0.001)
            y_growth = self.model.growth_lenia(x)
            self.view.update_growth_plot(x, y_growth)
            self.view.update_growth_axes(0, 0.3, -1.2, 1.2, continuous=True)
        else:
            # Utiliser une plage plus précise pour mieux représenter growth_GoL
            x = np.linspace(0, 8, 100)  # Points plus nombreux et répartis uniformément
            y_growth = self.model.growth_GoL(x)
            self.view.update_growth_plot(x, y_growth)
            # Ajuster les limites des axes pour growth_GoL
            self.view.update_growth_axes(0, 8, -1.2, 1.2, continuous=False)

    def update_displays(self):
        """Update all display elements."""
        self.update_nhood_display()
        self.update_growth_display()
        
        
       
        
