"""User settings controller module.

This module provides the controller component for the user settings interface.
It coordinates interactions between the model (UsModel) and view (UsView) components,
handling user input events, managing simulation controls like start/stop, reset,
and continuous mode, and configuring parameter sliders for the simulation functions.
"""

from typing import Any, Callable
from . import UsModel


class UsController:
    """User settings controller component.
    
    This class coordinates interactions between the UsModel and UsView components.
    It handles user input events, updates the model, and ensures the view reflects 
    the current state of the simulation.
    """
    def __init__(self, view: Any) -> None:
        """Initialize the user settings controller.
        
        Sets up the model, connects to the view, and configures the event handlers
        for all user interface elements.
        
        Args:
            view: The UsView instance to control
        """
        self.model = UsModel()
        self.view = view
        
        # Get widgets
        self.model.set_widgets(self.view.toggle_button)
        
        # Configure commands
        self.view.toggle_button.config(command=self.model.toggle_running_state)
        self.view.reset_button.config(command=self.model.reset_state)

        def combined_command(value: str) -> None:
            self.view.speed_label.config(text=f"FPS : {int(float(value))}")
            self.model.speed = float(value)

        self.view.speed_slider.config(command=combined_command)
        
        # Configure numeric entry
        self.view.set_numeric_entry_command(self.update_numeric_value)
    
    def update_numeric_value(self, value: str) -> None:
        """Update the numeric value in the model.
        
        Args:
            value (str): New value from the text entry
        """
        self.model.set_numeric_value(value)
    
    def set_interface_commands(self, 
                               mu_command: Callable[[float], None], 
                               sigma_command: Callable[[float], None], 
                               growth_mu_command: Callable[[float], None], 
                               growth_sigma_command: Callable[[float], None], 
                               continuous_button_command: Callable[[], None]) -> None:
        
        """Configure commands for the interface elements.
        
        Sets up callbacks for the Gaussian parameter sliders and continuous mode switch,
        ensuring that both the view is updated and the external commands are called.
        
        Args:
            mu_command: Function to call when mu value changes
            sigma_command: Function to call when sigma value changes
            growth_mu_command: Function to call when growth mu value changes
            growth_sigma_command: Function to call when growth sigma value changes
            continuous_button_command: Function to call when continuous mode changes
        """
        def update_mu(value: str) -> None:
            self.view.mu_label.config(text=f"μ : {float(value):.2f}")
            mu_command(float(value))
        
        def update_sigma(value: str) -> None:
            self.view.sigma_label.config(text=f"σ : {float(value):.2f}")
            sigma_command(float(value))
            
        def update_growth_mu(value: str) -> None:
            self.view.growth_mu_label.config(text=f"μ : {float(value):.2f}")
            growth_mu_command(float(value))
        
        def update_growth_sigma(value: str) -> None:
            # Round value to thousandth
            rounded_value = round(float(value), 3)
            self.view.growth_sigma_label.config(text=f"σ : {rounded_value:.3f}")
            growth_sigma_command(rounded_value)
        
        def toggle_continous() -> None:
            self.model.toggle_continuous_mode()
            continuous_button_command()

        
        self.view.mu_slider.config(command=update_mu)
        self.view.sigma_slider.config(command=update_sigma)
        self.view.growth_mu_slider.config(command=update_growth_mu)
        self.view.growth_sigma_slider.config(command=update_growth_sigma)
        self.view.continuous_switch.config(command=toggle_continous)

    
    def get_speed(self) -> float:
        """Return the current simulation speed.
        
        Returns:
            float: Number of generations per second
        """
        return self.model.speed
        
    
    def is_running(self) -> bool:
        """Return the current simulation state.
        
        Returns:
            bool: True if the simulation is running
        """
        return self.model.is_running

    
    def is_mode_continuous(self) -> bool:
        """Return the current continuous mode state.
        
        Returns:
            bool: True if continuous mode is enabled
        """
        return self.model.is_mode_continuous()
    
    def get_numeric_value(self) -> int:
        """Return the current numeric value.
        
        Returns:
            int: The numeric value entered by the user
        """
        return self.model.get_numeric_value()
