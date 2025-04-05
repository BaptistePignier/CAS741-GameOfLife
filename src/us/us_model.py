class UsModel:
    def __init__(self):
        self.toggle_button = None
        self.speed = 60.0  # Default speed (generations per second)
        self.is_running = False  # Simulation state
        self.needs_reset = False  # Reset flag
        self.is_continuous = False  # Continuous mode state
        self.continuous_switch = None
        self.numeric_value = 0  # Valeur numérique saisie par l'utilisateur
    
    def set_widgets(self, toggle_button, continuous_switch):
        """Store only the reference to the toggle button that needs to be updated."""
        self.toggle_button = toggle_button
        self.continuous_switch = continuous_switch
    
    def toggle_running_state(self):
        """Toggle the simulation state.
        
        Returns:
            bool: New simulation state
        """
        self.is_running = not self.is_running
        self.toggle_button.config(text="Stop" if self.is_running else "Start")
        return self.is_running
    
    def reset_state(self):
        """Reset the simulation state."""
        self.is_running = False
        self.needs_reset = True
        self.toggle_button.config(text="Start")
    
    def acknowledge_reset(self):
        """Acknowledge the reset request.
        
        Returns:
            bool: True if a reset was requested
        """
        was_reset = self.needs_reset
        self.needs_reset = False
        return was_reset
    
    def toggle_continuous_mode(self):
        """Toggle the continuous mode state.
        
        Returns:
            bool: New continuous mode state
        """
        self.is_continuous = not self.is_continuous
        return self.is_continuous
    
    def is_mode_continuous(self):
        """Return the continuous mode state.
        
        Returns:
            bool: True if continuous mode is enabled
        """
        return self.is_continuous
        
    def set_numeric_value(self, value):
        """Définir la valeur numérique.
        
        Args:
            value (int): La valeur numérique à stocker
        """
        try:
            self.numeric_value = int(value)
        except ValueError:
            # Si la conversion échoue, garder la valeur actuelle
            pass
            
    
