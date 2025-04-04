from . import SimModel
import numpy as np

class SimController:
    def __init__(self, view, root, us_controller, fi_controller):
        """Initialize the simulation controller.
        
        Args:
            view: SimView instance
            root: Main Tkinter window
            us_controller: UsController instance
            fi_controller: FiController instance
        """
        self.model = SimModel(view.width, view.height)
        self.view = view
        self.root = root
        self.us_controller = us_controller
        self.fi_controller = fi_controller
        self.min_delay = 16  # ~60 FPS maximum (1000/60 ≈ 16.67ms)
        self.update_timer = None
        
    def run(self):
        # Check mode (continuous or discrete) for initialization
        self.reset()
        
        # Initial display update
        self.view.update_display(self.model.get_grid())
        
        # Start the update timer
        self.update()

    def update(self):
        """Update the model and view if the simulation is running."""
        # Check if a reset is requested
        if self.us_controller.model.acknowledge_reset():
            # Check the mode (continuous or discrete) for reset
            self.reset()
            self.view.update_display(self.model.get_grid())
        
        # Update the simulation if it's running
        if self.us_controller.is_running():

            # Calculate a generation based on mode (continuous or discrete)
            if self.us_controller.is_mode_continuous():

                self.model.update(self.fi_controller.get_growth_lenia(),self.fi_controller.get_con_nhood(),0.1)
            else:
                self.model.update(self.fi_controller.get_growth_GoL(),self.fi_controller.get_dis_nhood(),1)
            
            # Update the display
            self.view.update_display(self.model.get_grid())
        
        # Schedule the next update
        generations_per_second = self.us_controller.get_speed()
        delay = max(self.min_delay, int(1000 / generations_per_second))
        self.update_timer = self.root.after(delay, self.update)
    
    def stop(self):
        """Stop the update timer."""
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None
    
    def reset(self):
        if self.us_controller.is_mode_continuous():
            self.model.reset_continuous()
        else:
            self.model.reset_discrete()