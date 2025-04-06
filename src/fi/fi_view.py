import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.ticker as ticker

class FiView:
    def __init__(self, master):
        # Main frame
        self.frame = ttk.Frame(master)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        # Single figure with two subplots
        self.fig, (self.ax_con_nhood, self.ax_growth) = plt.subplots(2, 1)
        self.fig.set_facecolor('white')
        
        # Adjust margins to give more space for tick marks and titles
        # Increase left margin for tick marks and Y-axis labels
        # Increase top margin for titles
        self.fig.subplots_adjust(left=0.22, right=0.95, top=0.92, bottom=0.1, hspace=0.4)
        
        # Configure axis for the kernel
        self.ax_con_nhood.set_xticks([])
        self.ax_con_nhood.set_yticks([])
        self.ax_con_nhood.set_title("Neighborhood visualization", pad=10)
        
        # Configure axis for the growth function
        # Keep the tick marks to better visualize the values
        self.ax_growth.set_title("Growth function", pad=10)
        
        # Single canvas for both graphs
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        # Initialize kernel graph
        empty_kernel = np.zeros((26, 26))
        self.con_nhood_image = self.ax_con_nhood.imshow(
            empty_kernel,
            cmap='viridis',
            interpolation='nearest',
            aspect='equal',
            extent=[-1, 1, -1, 1],
            vmin=0,
            vmax=0.005
        )
        self.ax_con_nhood.grid(True, linestyle='--', alpha=0.3)
        
        # Initialize growth function graph
        x_init = [0, 0.3]
        y_init = [0, 0]
        self.growth_line, = self.ax_growth.plot(x_init, y_init, 'g-', linewidth=2)
        self.ax_growth.set_ylim(-1.2, 1.2)
        
        self.ax_growth.grid(True, linestyle='--', alpha=0.3)
        
        # Initial canvas update
        self.canvas.draw()

    def update_growth_plot(self, x_values, y_values):
        """Updates the growth function graph."""
        self.growth_line.set_xdata(x_values)
        self.growth_line.set_ydata(y_values)
        self.canvas.draw_idle()
    
    def update_growth_axes(self, xmin, xmax, ymin, ymax, continuous=True):
        """Updates the limits and tick marks of the growth function graph axes.
        
        Args:
            xmin, xmax: limits of the x-axis
            ymin, ymax: limits of the y-axis
            continuous: if True, configures for continuous mode (Lenia), otherwise for discrete mode (GoL)
        """
        self.ax_growth.set_xlim(xmin, xmax)
        self.ax_growth.set_ylim(ymin, ymax)
        
        if continuous:
            # Tick marks for continuous mode (Lenia)
            self.ax_growth.set_xticks(np.linspace(xmin, xmax, 7))
            self.ax_growth.set_yticks(np.linspace(-1, 1, 5))
            # Format with a single decimal place
            self.ax_growth.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
        else:
            # Tick marks for discrete mode (GoL)
            self.ax_growth.set_xticks(range(0, 9))
            self.ax_growth.set_yticks([-1, -0.5, 0, 0.5, 1])
            # For discrete mode, use integers
            self.ax_growth.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        
        # Adjust label spacing
        self.ax_growth.tick_params(axis='both', which='major', labelsize=9)
        self.ax_growth.tick_params(axis='y', pad=8)  # More space for Y-axis labels
        
        self.canvas.draw_idle()
        
    def update_nhood_plot(self, kernel):
        """Compatibility method that calls update_con_nhood_plot."""
        self.con_nhood_image.set_array(kernel)
        self.canvas.draw_idle()

    def get_frame(self):
        """Returns the main frame."""
        return self.frame

    def get_canvas(self):
        """Returns the canvas widgets."""
        return None, self.canvas.get_tk_widget(), self.canvas.get_tk_widget()
