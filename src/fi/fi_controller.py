"""Functional inputs controller module.

This module provides the controller component for the functional inputs module.
It coordinates interactions between the model (FiModel) and view (FiView) components,
and handles communications with the user settings controller. It manages updates
to neighborhood and growth function parameters based on user interactions.
"""

from typing import Callable, Any, Optional
import numpy as np
from .fi_model import FiModel



class FiController:
    """Functional input controller component.
    
    This class coordinates interactions between the FiModel and FiView components.
    It manages updates to neighborhood and growth function parameters and ensures
    the view is synchronized with the model.
    """
    def __init__(self, view: Any, us_controller: Any) -> None:
        """Initialize the functional input controller.
        
        Sets up the model, connects to the view, and registers with the user settings controller.
        
        Args:
            view: The FiView instance to control
            us_controller: The UsController instance to interact with
        """
        self.model = FiModel()
        self.view = view
        self.us_controller = us_controller

        # Initial display
        self.update_displays()

        self.us_controller.set_continuous_switch_callback(self.update_displays)

        self.us_controller.set_nhood_callbacks(
            lambda x: self.update_nhood_params(mu=x),
            lambda x: self.update_nhood_params(sigma=x)
        )

        self.us_controller.set_growth_callback(
            lambda x: self.update_growth_params(g_mu=x),
            lambda x: self.update_growth_params(g_sigma=x),
        )
    
    def get_nhood(self) -> np.ndarray:
        """Get the appropriate neighborhood kernel based on current mode.
        
        Returns:
            numpy.ndarray: Either continuous or discrete neighborhood kernel
        """
        if self.us_controller.is_mode_continuous():
            return self.model.get_con_nhood()
        return self.model.get_dis_nhood()

    
    def get_growth_fct(self) -> Callable[[np.ndarray], np.ndarray]:
        """Get the appropriate growth function based on current mode.
        
        Returns:
            function: Either Lenia or GoL growth function
        """
        if self.us_controller.is_mode_continuous():
            return self.model.growth_lenia
        return self.model.growth_gol

    def get_step(self) -> float:
        """Get the appropriate simulation step value based on current mode.
        
        Returns:
            float: Step value (0.1 for continuous mode, 1 for discrete mode)
        """
        if self.us_controller.is_mode_continuous():
            return 0.1
        return 1

    def update_nhood_params(self, 
                            mu: Optional[float] = None, 
                            sigma: Optional[float] = None) -> None:
        
        """Update neighborhood parameters in the model and refresh display.
        
        Args:
            mu (float, optional): New center value for the ring. If None, keeps current value.
            sigma (float, optional): New width value for the ring. If None, keeps current value.
        """
        self.model.set_nhood_params(mu,sigma)
        self.update_nhood_display()

    def update_growth_params(self, 
                             g_mu: Optional[float] = None, 
                             g_sigma: Optional[float] = None) -> None:
        
        """Update growth function parameters in the model and refresh display.
        
        Args:
            g_mu (float, optional): New center value for growth function.
            g_sigma (float, optional): New width value for growth function.
        """
        self.model.set_growth_params(g_mu,g_sigma)
        self.update_growth_display()

    
    def update_nhood_display(self) -> None:
        """Update the neighborhood visualization in the view.
        
        Selects the appropriate kernel (continuous or discrete) based on current mode
        and updates the view.
        """
        # Update the nhood plot
        if self.us_controller.is_mode_continuous():
            self.view.update_nhood_plot(self.model.get_con_nhood())
        else:
            self.view.update_nhood_plot(self.model.get_dis_nhood())

    def update_growth_display(self) -> None:
        """Update the growth function visualization in the view.
        
        Generates appropriate data for the current growth function (either Lenia or GoL)
        and updates the plot and axes in the view.
        """
        # Update the growth plot
        if self.us_controller.is_mode_continuous():
            x = np.arange(0, 0.3, 0.001)
            y_growth = self.model.growth_lenia(x)
            self.view.update_growth_plot(x, y_growth)
            self.view.update_growth_axes(0, 0.3, continuous=True)
        else:
            x = np.asarray([0,1,2,3,4,5,6,7,8])
            y_growth = self.model.growth_gol(x)
            self.view.update_growth_plot(x, y_growth)
            self.view.update_growth_axes(0, 8,  continuous=False)

    def update_displays(self) -> None:
        """Update all display elements in the view.
        
        This is a convenience method that updates both neighborhood and growth
        function visualizations.
        """
        self.update_nhood_display()
        self.update_growth_display()
        
        
       
        
