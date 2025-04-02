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
        if self.us_controller.is_mode_continuous():
            self.reset_continuous()
        else:
            self.reset_discrete()
        
        # Initial display update
        self.view.update_display(self.model.get_grid())
        
        # Start the update timer
        self.update()

    def update(self):
        """Update the model and view if the simulation is running."""
        # Check if a reset is requested
        if self.us_controller.model.acknowledge_reset():
            # Check the mode (continuous or discrete) for reset
            if self.us_controller.is_mode_continuous():
                self.reset_continuous()
            else:
                self.reset_discrete()
            self.view.update_display(self.model.get_grid())
        
        # Update the simulation if it's running
        if self.us_controller.is_running():
            
            # Pass FIs to sim_model
            self.model.set_kernel_ring(self.fi_controller.get_ring_kernel())
            self.model.set_growth_lenia(self.fi_controller.get_growth_lenia())

            # Calculate a generation based on mode (continuous or discrete)
            if self.us_controller.is_mode_continuous():
                self.model.update_continuous()
            else:
                self.model.update_discrete()
            
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

    def reset_discrete(self, prob=None):
        """Reset the grid with a new random configuration.
        
        Args:
            prob (float, optional): New probability for live cells.
                                  If None, uses the initial probability.
        """
        if prob is not None and 0 <= prob <= 1:
            self.model.initial_alive_prob = prob
            
        # Optimized generation of the random grid
        self.model.grid = np.random.choice(
            [0, 1],
            self.model.width * self.model.height,
            p=[1-self.model.initial_alive_prob, self.model.initial_alive_prob]
        ).reshape(self.model.height, self.model.width).astype(np.int8)

    def reset_continuous(self):
        N = 256
        M = int(np.ceil((16*N)/9))
        self.model.grid = np.ones((M, N))
        # Gaussian spot centered in the middle
        radius = 36
        y, x = np.ogrid[-N//2:N//2, -M//2:M//2]
        self.model.grid = np.exp(-0.5 * (x*x + y*y) / (radius*radius))