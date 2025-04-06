import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class SimView:
    """Simulation view component.
    
    This class represents the view component for the simulation module.
    It manages the visualization of the cellular automaton grid using matplotlib
    and provides methods to update the display when the grid state changes.
    """
    def __init__(self, master, width, height):
        """Initialize the simulation view.
        
        Args:
            master: Parent Tkinter widget
            width (int): Grid width in cells
            height (int): Grid height in cells
        """
        self.width = width
        self.height = height
        self.master = master
        self.current_grid = None
        
        # Creation of matplotlib figure with fixed size
        self.fig = plt.figure(figsize=(width/100, height/100))  # Standard DPI = 100
        self.fig.set_facecolor('none')  # Transparent background
        
        # Optimized axis configuration
        self.ax = self.fig.add_subplot(111)
        self.ax.set_position([0, 0, 1, 1])  # Use all available space
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_frame_on(False)
        
        # Display configuration with optimized colormap
        self.grid_display = self.ax.imshow(
            np.zeros((height, width)),  # Initial grid size (will be updated)
            cmap='binary',
            interpolation='nearest',
            aspect='equal',
            vmin=0,
            vmax=1
        )
        
        # Creation of Tkinter canvas with fixed size
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        
        # Configuration of view limits
        self.ax.set_xlim(-0.5, width-0.5)  # Grid centering
        self.ax.set_ylim(-0.5, height-0.5)  # Grid centering
        
        # Disable unused matplotlib events to improve performance
        for event_name in ['button_press_event', 'button_release_event', 'motion_notify_event']:
            callbacks = self.canvas.callbacks.callbacks.get(event_name, {})
            if callbacks and 0 in callbacks:
                self.canvas.mpl_disconnect(callbacks[0])

    
    def update_display(self, grid):
        """Update the grid display.
        
        Args:
            grid (numpy.ndarray): New grid to display
        """
        self.grid_display.set_array(grid)
        self.canvas.draw()
    
    def get_canvas(self):
        """Return the canvas widget.
        
        Returns:
            tkinter.Widget: Tkinter canvas widget
        """
        return self.canvas_widget
    
    def __del__(self):
        """Clean up matplotlib resources."""
        plt.close(self.fig)
