from . import UsModel

class UsController:
    def __init__(self, view):
        self.model = UsModel()
        self.view = view
        
        # Get widgets
        self.model.set_widgets(**view.get_widgets())
        
        # Configure commands
        self.setup_commands()
    
    def setup_commands(self):
        """Configure all widget commands."""
        self.view.set_toggle_command(self.toggle_simulation)
        self.view.set_reset_command(self.reset_simulation)
        self.view.set_speed_command(self.update_speed)
        self.view.set_continuous_command(self.toggle_continuous_mode)
        
    
    def set_gaussian_commands(self, mu_command, sigma_command, growth_mu_command, growth_sigma_command):
        """Configure gaussian slider commands."""
        def update_mu(value):
            self.view.mu_label.config(text=f"μ : {float(value):.2f}")
            mu_command(value)
        
        def update_sigma(value):
            self.view.sigma_label.config(text=f"σ : {float(value):.2f}")
            sigma_command(value)
            
        def update_growth_mu(value):
            self.view.growth_mu_label.config(text=f"μ : {float(value):.2f}")
            growth_mu_command(value)
        
        def update_growth_sigma(value):
            # Round value to thousandth
            rounded_value = round(float(value), 3)
            self.view.growth_sigma_label.config(text=f"σ : {rounded_value:.3f}")
            growth_sigma_command(rounded_value)
        
        self.view.mu_slider.config(command=update_mu)
        self.view.sigma_slider.config(command=update_sigma)
        self.view.growth_mu_slider.config(command=update_growth_mu)
        self.view.growth_sigma_slider.config(command=update_growth_sigma)

    def toggle_simulation(self):
        """Handle start/stop of the simulation."""
        self.model.toggle_running_state()
    
    def reset_simulation(self):
        """Reset the simulation."""
        self.model.reset_state()
    
    def get_speed(self):
        """Return the current simulation speed.
        
        Returns:
            float: Number of generations per second
        """
        return self.model.speed
    
    def update_speed(self, value):
        """Update the simulation speed.
        
        Args:
            value (float): New speed in generations per second
        """
        self.model.speed = float(value)
    
    def is_running(self):
        """Return the current simulation state.
        
        Returns:
            bool: True if the simulation is running
        """
        return self.model.is_running

    def toggle_continuous_mode(self):
        """Handle enable/disable of continuous mode."""
        self.model.toggle_continuous_mode()
    
    def is_mode_continuous(self):
        """Return the current continuous mode state.
        
        Returns:
            bool: True if continuous mode is enabled
        """
        return self.model.is_mode_continuous()
