import tkinter as tk
from tkinter import ttk

class WindowManager:
    def __init__(self, root, sim_size, panel_width):
        """Initialize the window manager.
        
        Args:
            root: Main Tkinter window
            sim_size (int): Size of simulation area in pixels
            panel_width (int): Width of control panel in pixels
        """
        self.root = root
        self.sim_size = sim_size
        self.panel_width = panel_width
        
        # Configuration of the main window
        self.root.title("Game of Life")
        window_width = sim_size + panel_width
        window_height = sim_size  # Square window for simulation
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Configuration of main layout
        self.setup_main_layout()
        
        # Configuration of control panel
        self.setup_control_panel()
    
    def setup_main_layout(self):
        """Configure the main layout of the window."""
        # Simulation area (expandable)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Control panel (fixed width)
        self.root.grid_columnconfigure(1, weight=0, minsize=self.panel_width)
        
        # Prevents resizing below a minimum size
        min_width = self.panel_width + 300  # 300px minimum for simulation
        min_height = 400  # Reasonable minimum height
        self.root.minsize(min_width, min_height)
    
    def setup_control_panel(self):
        """Configure the control panel."""
        # Main control frame
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Grid configuration for controls
        self.control_frame.grid_columnconfigure(0, weight=1)
        
        # Prevents horizontal resizing of the panel
        self.control_frame.grid_propagate(False)
        self.control_frame.configure(width=self.panel_width)
    
    def place_views(self, sim_view, us_view, fi_view):
        """Place all views in the interface.
        
        Args:
            sim_view: Simulation view
            us_view: User control view
            fi_view: Influence function view
        """
        # Place simulation view
        sim_canvas = sim_view.get_canvas()
        sim_canvas.grid(row=0, column=0, sticky='nsew')
        
        # Place control views
        us_frame = us_view.get_frame()
        us_frame.grid(row=0, column=0, sticky='ew')
        
        # Separator between controls and graph
        ttk.Separator(self.control_frame, orient='horizontal').grid(
            row=1, column=0, sticky='ew', pady=10
        )
        
        # Place gaussian function view
        fi_frame = fi_view.get_frame()
        fi_frame.grid(row=2, column=0, sticky='ew')
    
    def get_control_frame(self):
        """Return the control frame.
        
        Returns:
            ttk.Frame: Frame containing controls
        """
        return self.control_frame
