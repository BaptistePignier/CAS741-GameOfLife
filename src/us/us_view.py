import tkinter as tk
from tkinter import ttk

class UsView:
    """User simulation view component.
    
    This class represents the view component for the user simulation module.
    It provides the user interface elements for controlling the simulation,
    including buttons, sliders, and other input controls.
    """
    def __init__(self, control_frame):
        """Initialize the user simulation view.
        
        Creates the UI frame and adds all control elements including:
        - Start/Stop toggle button
        - Reset button
        - Continuous mode checkbox
        - Numeric entry field
        - Speed control slider
        - Gaussian function parameter sliders
        - Growth function parameter sliders
        
        Args:
            control_frame: The parent tkinter container widget
        """
        # Creation of internal frame
        self.frame = ttk.Frame(control_frame)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Creation of widgets
        self._create_control_buttons()
        self._create_speed_frame()
        self._create_gaussian_frame()
    
    def _create_control_buttons(self):
        """Create control buttons."""
        self.toggle_button = ttk.Button(self.frame, text="Start")
        self.toggle_button.grid(row=0, column=0, pady=5)
        
        # Frame for reset button and continuous switch
        reset_frame = ttk.Frame(self.frame)
        reset_frame.grid(row=1, column=0, pady=5)
        reset_frame.grid_columnconfigure(0, weight=1)
        reset_frame.grid_columnconfigure(1, weight=1)
        
        # Reset button
        self.reset_button = ttk.Button(reset_frame, text="Reset")
        self.reset_button.grid(row=1, column=0, pady=5, padx=5)
        
        # Frame for continuous switch and the numeric entry
        continuous_frame = ttk.Frame(reset_frame)
        continuous_frame.grid(row=1, column=1, pady=5, padx=5)
        continuous_frame.grid_columnconfigure(0, weight=1)
        continuous_frame.grid_columnconfigure(1, weight=2)
        
        # Sub-frame for the numeric text field
        numeric_frame = ttk.Frame(continuous_frame)
        numeric_frame.grid(row=0, column=0, padx=(0, 10))
        
        # Label for the numeric field
        numeric_label = ttk.Label(numeric_frame, text="Number:")
        numeric_label.pack(anchor=tk.CENTER, pady=(0, 3))
        
        # Text field for entering a number
        self.numeric_entry = ttk.Entry(numeric_frame, width=5)
        self.numeric_entry.insert(0, "0")  # Default value
        self.numeric_entry.pack(anchor=tk.CENTER)
        
        # Sub-frame for the continuous checkbox
        cont_switch_frame = ttk.Frame(continuous_frame)
        cont_switch_frame.grid(row=0, column=1)
        
        # Label for continuous switch
        continuous_label = ttk.Label(cont_switch_frame, text="Continuous")
        continuous_label.pack(anchor=tk.CENTER, pady=(0, 3))
                
        # Continuous switch (using Checkbutton as switch)
        self.continuous_switch = ttk.Checkbutton(cont_switch_frame)
        self.continuous_switch.pack(anchor=tk.CENTER)
    
    def _create_speed_frame(self):
        """Create speed control frame."""
        speed_frame = ttk.LabelFrame(self.frame, text="Speed")
        speed_frame.grid_columnconfigure(0, weight=1)
        speed_frame.grid(row=2, column=0, pady=5, padx=5, sticky='ew')
        
        # Dynamic FPS label
        self.speed_label = ttk.Label(speed_frame, text="FPS : 60")
        self.speed_label.grid(row=0, column=0, pady=(5,0))
        
        # Speed slider
        self.speed_slider = ttk.Scale(
            speed_frame,
            from_=1,
            to=120,
            orient=tk.HORIZONTAL,
            value=60
        )
        self.speed_slider.grid(row=1, column=0, pady=5, padx=10, sticky='ew')
    
    def _create_gaussian_frame(self):
        """Create gaussian parameters frame."""
        gaussian_frame = ttk.LabelFrame(self.frame, text="Gaussian Function")
        gaussian_frame.grid_columnconfigure(0, weight=1)
        gaussian_frame.grid(row=3, column=0, pady=5, padx=5, sticky='ew')
        
        # μ (mu) parameter
        self.mu_label = ttk.Label(gaussian_frame, text="μ : 0.50")
        self.mu_label.grid(row=0, column=0, pady=(5,0))
        
        self.mu_slider = ttk.Scale(
            gaussian_frame,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            value=0.5
        )
        self.mu_slider.grid(row=1, column=0, pady=(0,5), padx=10, sticky='ew')
        
        # σ (sigma) parameter
        self.sigma_label = ttk.Label(gaussian_frame, text="σ : 0.15")
        self.sigma_label.grid(row=2, column=0, pady=(5,0))
        
        self.sigma_slider = ttk.Scale(
            gaussian_frame,
            from_=0.05,
            to=0.5,
            orient=tk.HORIZONTAL,
            value=0.15
        )
        self.sigma_slider.grid(row=3, column=0, pady=(0,5), padx=10, sticky='ew')

        # New frame for growth function
        growth_frame = ttk.LabelFrame(self.frame, text="Growth Function")
        growth_frame.grid_columnconfigure(0, weight=1)
        growth_frame.grid(row=4, column=0, pady=5, padx=5, sticky='ew')
        
        # μ (mu) parameter for growth
        self.growth_mu_label = ttk.Label(growth_frame, text="μ : 0.15")
        self.growth_mu_label.grid(row=0, column=0, pady=(5,0))
        
        self.growth_mu_slider = ttk.Scale(
            growth_frame,
            from_=0.0,
            to=0.30,
            orient=tk.HORIZONTAL,
            value=0.15
        )
        self.growth_mu_slider.grid(row=1, column=0, pady=(0,5), padx=10, sticky='ew')
        
        # σ (sigma) parameter for growth
        self.growth_sigma_label = ttk.Label(growth_frame, text="σ : 0.015")
        self.growth_sigma_label.grid(row=2, column=0, pady=(5,0))
        
        self.growth_sigma_slider = ttk.Scale(
            growth_frame,
            from_=0.0,
            to=0.1,
            orient=tk.HORIZONTAL,
            value=0.015
        )
        self.growth_sigma_slider.grid(row=3, column=0, pady=(0,5), padx=10, sticky='ew')

    
    def get_frame(self):
        """Get the main frame of the view.
        
        Returns:
            ttk.Frame: The main frame containing all view components
        """
        return self.frame
    
    def set_numeric_entry_command(self, command):
        """Configure the command for the numeric text field.
        
        Args:
            command (function): The function to call when the content changes
        """
        # Intermediate function to be called when a change occurs
        def on_value_change(*args):
            command(self.numeric_entry.get())
        
        # Control variable to track changes
        self.numeric_var = tk.StringVar()
        self.numeric_var.trace_add("write", on_value_change)
        self.numeric_entry.config(textvariable=self.numeric_var)

