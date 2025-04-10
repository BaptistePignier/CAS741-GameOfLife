"""Window Manager module (wm).

This module contains the WindowManager class which manages the main application window.
It handles window layout, window state (fullscreen, maximized), and the placement
of different views within the application interface.
"""

import tkinter as tk
from tkinter import ttk
import platform
from typing import Any

class WindowManager:
    """Window management component.
    
    This class manages the main application window, handling layout, 
    window state (fullscreen, maximized), and the placement of different views.
    It serves as the container for all visual components of the application.
    """
    def __init__(self, root: tk.Tk, sim_size: int, panel_width: int) -> None:
        """Initialize the window manager.
        
        Args:
            root: Main Tkinter window
            sim_size (int): Size of simulation area in pixels
            panel_width (int): Width of control panel in pixels
        """
        self.root = root
        self.sim_size = sim_size
        self.panel_width = panel_width
        self.is_fullscreen = False
        
        # Configuration of the main window
        self.root.title("Game of Life")
        window_width = sim_size + panel_width
        window_height = sim_size  # Square window for simulation
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Configuration of fullscreen mode
        self.root.bind("<F11>", lambda event: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda event: self.exit_fullscreen())
        
        # Configuration of main layout
        self.setup_main_layout()
        
        # Configuration of control panel
        self.setup_control_panel()
    
    def toggle_fullscreen(self) -> None:
        """Toggle fullscreen mode."""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
    
    def exit_fullscreen(self) -> None:
        """Exit fullscreen mode."""
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
    
    def maximize_window(self) -> None:
        """Maximize the window without fullscreen mode.
        
        Uses platform-specific methods to maximize the window.
        """
        if platform.system() == "Windows":
            self.root.state('zoomed')
        else:  # Linux, macOS
            # For Unix systems, maximize using Tk attributes
            # which are more widely supported than '-zoomed'
            self.root.attributes('-zoomed', True)  # First try with -zoomed
            # Fallback solution - get screen dimensions and apply them
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(f"{screen_width}x{screen_height}+0+0")
    
    def setup_main_layout(self) -> None:
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
    
    def setup_control_panel(self) -> None:
        """Configure the control panel."""
        # Main control frame
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Grid configuration for controls
        self.control_frame.grid_columnconfigure(0, weight=1)
        
        # Prevents horizontal resizing of the panel
        self.control_frame.grid_propagate(False)
        self.control_frame.configure(width=self.panel_width)
    
    def place_views(self, sim_view: Any, us_view: Any, fi_view: Any) -> None:
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
    
    def get_control_frame(self) -> ttk.Frame:
        """Return the control frame.
        
        Returns:
            ttk.Frame: Frame containing controls
        """
        return self.control_frame
