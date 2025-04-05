from . import UsModel

class UsController:
    def __init__(self, view):
        self.model = UsModel()
        self.view = view
        
        # Get widgets
        self.model.set_widgets(**view.get_widgets())
        
        # Configure commands
        self.view.toggle_button.config(command=self.model.toggle_running_state)
        self.view.reset_button.config(command=self.model.reset_state)

        def combined_command(value):
            self.view._update_speed_label(value)
            self.model.speed = float(value)

        self.view.speed_slider.config(command=combined_command)
    
    
    def set_gaussian_commands(self, mu_command, sigma_command, growth_mu_command, growth_sigma_command, continuous_button_command):
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
        
        def toggle_continous():
            self.model.toggle_continuous_mode()
            continuous_button_command()

        
        self.view.mu_slider.config(command=update_mu)
        self.view.sigma_slider.config(command=update_sigma)
        self.view.growth_mu_slider.config(command=update_growth_mu)
        self.view.growth_sigma_slider.config(command=update_growth_sigma)
        self.view.continuous_switch.config(command=toggle_continous)

    
    def get_speed(self):
        """Return the current simulation speed.
        
        Returns:
            float: Number of generations per second
        """
        return self.model.speed
        
    
    def is_running(self):
        """Return the current simulation state.
        
        Returns:
            bool: True if the simulation is running
        """
        return self.model.is_running

    
    def is_mode_continuous(self):
        """Return the current continuous mode state.
        
        Returns:
            bool: True if continuous mode is enabled
        """
        return self.model.is_mode_continuous()
