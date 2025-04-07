from typing import Any, Optional, Union

class UsModel:
    """User simulation model component.
    
    This class represents the model component for the user simulation module.
    It maintains the simulation state, manages running/paused status, continuous mode,
    reset operations, and user-entered numeric values.
    """
    def __init__(self) -> None:
        """Initialize the user simulation model.
        
        Sets up the default state for simulation control:
        - Default speed of 60 generations per second
        - Simulation initially stopped
        - No reset pending
        - Discrete mode (not continuous) by default
        - Initial numeric value of 0
        """
        self.toggle_button = None
        self.speed = 60.0  # Default speed (generations per second)
        self.is_running = False  # Simulation state
        self.needs_reset = False  # Reset flag
        self.is_continuous = False  # Continuous mode state
        self.continuous_switch = None
        self.numeric_value = 0  # Numeric value entered by the user
    
    def set_widgets(self, toggle_button: Any, continuous_switch: Any) -> None:
        """Store only the reference to the toggle button that needs to be updated."""
        self.toggle_button = toggle_button
        self.continuous_switch = continuous_switch
    
    def toggle_running_state(self) -> bool:
        """Toggle the simulation state.
        
        Returns:
            bool: New simulation state
        """
        self.is_running = not self.is_running
        self.toggle_button.config(text="Stop" if self.is_running else "Start")
        return self.is_running
    
    def reset_state(self) -> None:
        """Reset the simulation state."""
        self.is_running = False
        self.needs_reset = True
        self.toggle_button.config(text="Start")
    
    def acknowledge_reset(self) -> bool:
        """Acknowledge the reset request.
        
        Returns:
            bool: True if a reset was requested
        """
        was_reset = self.needs_reset
        self.needs_reset = False
        return was_reset
    
    def toggle_continuous_mode(self) -> bool:
        """Toggle the continuous mode state.
        
        Returns:
            bool: New continuous mode state
        """
        self.is_continuous = not self.is_continuous
        return self.is_continuous
    
    def is_mode_continuous(self) -> bool:
        """Return the continuous mode state.
        
        Returns:
            bool: True if continuous mode is enabled
        """
        return self.is_continuous
        
    def set_numeric_value(self, value: Union[int, str, None]) -> None:
        """Set the numeric value.
        
        Args:
            value (int or str): The numeric value to store
        """
        if value is None:
            # Do nothing if value is None
            return
            
        try:
            # For strings containing decimal numbers, try to convert to float first
            if isinstance(value, str) and ("." in value or "," in value):
                self.numeric_value = int(float(value))
            else:
                self.numeric_value = int(value)
        except (ValueError, TypeError):
            # If conversion fails, keep the current value
            pass
            
    def get_numeric_value(self) -> int:
        """Get the current numeric value.
        
        Returns:
            int: The numeric value
        """
        return self.numeric_value
            
    
