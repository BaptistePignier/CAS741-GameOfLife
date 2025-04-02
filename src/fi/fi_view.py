import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FiView:
    def __init__(self, master, figsize=(6, 6)):
        # Main frame
        self.frame = ttk.Frame(master)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=2)  # 2/3 for the top
        self.frame.grid_rowconfigure(1, weight=1)  # 1/3 for the bottom
        
        # Top frame (gaussian + kernel)
        self.top_frame = ttk.LabelFrame(self.frame, text="Gaussian function and kernel")
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)  # Gaussian
        self.top_frame.grid_rowconfigure(1, weight=2)  # Kernel
        
        # Frame for the gaussian
        self.gaussian_frame = ttk.Frame(self.top_frame)
        self.gaussian_frame.grid(row=0, column=0, sticky='nsew')
        self.gaussian_frame.grid_columnconfigure(0, weight=1)
        self.gaussian_frame.grid_rowconfigure(0, weight=1)
        
        # Frame for the kernel
        self.ring_frame = ttk.Frame(self.top_frame)
        self.ring_frame.grid(row=1, column=0, sticky='nsew')
        self.ring_frame.grid_columnconfigure(0, weight=1)
        self.ring_frame.grid_rowconfigure(0, weight=1)
        
        # Bottom frame (growth)
        self.bottom_frame = ttk.LabelFrame(self.frame, text="Growth function")
        self.bottom_frame.grid(row=1, column=0, sticky='nsew')
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        
        # Configuration of figures with adapted sizes
        # The gaussian takes 1/3 of the top frame height
        self.gaussian_fig = plt.figure(constrained_layout=True, figsize=(3, 1))
        self.gaussian_fig.set_facecolor('white')
        self.ax_gaussian = self.gaussian_fig.add_subplot(111)
        self.ax_gaussian.set_xticks([])
        self.ax_gaussian.set_yticks([])
        
        # The kernel takes 2/3 of the top frame height
        self.ring_fig = plt.figure(constrained_layout=True, figsize=(3, 2))
        self.ring_fig.set_facecolor('white')
        self.ax_ring = self.ring_fig.add_subplot(111)
        self.ax_ring.set_xticks([])
        self.ax_ring.set_yticks([])
        
        # The growth takes the full bottom frame height
        self.growth_fig = plt.figure(constrained_layout=True, figsize=(3, 1.5))
        self.growth_fig.set_facecolor('white')
        self.ax_growth = self.growth_fig.add_subplot(111)
        self.ax_growth.set_xticks([])
        self.ax_growth.set_yticks([])
        
        # Canvas configuration
        self.gaussian_canvas = FigureCanvasTkAgg(self.gaussian_fig, master=self.gaussian_frame)
        self.gaussian_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        self.ring_canvas = FigureCanvasTkAgg(self.ring_fig, master=self.ring_frame)
        self.ring_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        self.growth_canvas = FigureCanvasTkAgg(self.growth_fig, master=self.bottom_frame)
        self.growth_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        # Initial configuration of graphs
        x_init = [0, 1]
        y_init = [0, 0]
        
        # Gaussian graph
        self.line, = self.ax_gaussian.plot(x_init, y_init, 'b-', linewidth=2)
        self.ax_gaussian.set_ylim(-0.2, 1.2)
        self.ax_gaussian.grid(True, linestyle='--', alpha=0.3)
        
        # Kernel graph
        empty_kernel = np.zeros((26, 26))
        self.ring_image = self.ax_ring.imshow(
            empty_kernel,
            cmap='viridis',
            interpolation='nearest',
            aspect='equal',
            extent=[-1, 1, -1, 1],
            vmin=0,
            vmax=0.005
        )
        self.ax_ring.grid(True, linestyle='--', alpha=0.3)
        
        # Growth graph
        self.growth_line, = self.ax_growth.plot(x_init, y_init, 'g-', linewidth=2)
        self.ax_growth.set_ylim(-0.2, 1.2)
        self.ax_growth.grid(True, linestyle='--', alpha=0.3)
        
        # Initial canvas update
        self.gaussian_canvas.draw()
        self.ring_canvas.draw()
        self.growth_canvas.draw()
    
    def update_gaussian_plot(self, x_values, y_values, y_max=None):
        self.line.set_xdata(x_values)
        self.line.set_ydata(y_values)
        if y_max is not None:
            self.ax_gaussian.set_ylim(-0.2, y_max * 1.2)
        self.gaussian_canvas.draw_idle()

    def update_growth_plot(self, x_values, y_values, y_max=None):
        self.growth_line.set_xdata(x_values)
        self.growth_line.set_ydata(y_values)
        if y_max is not None:
            self.ax_growth.set_ylim(-0.2, y_max * 1.2)
        self.growth_canvas.draw_idle()
    
    def update_ring_plot(self, kernel):
        """Update the ring kernel graph."""
        self.ring_image.set_array(kernel)
        self.ring_canvas.draw_idle()

    def get_frame(self):
        """Return the main frame."""
        return self.frame

    def get_canvas(self):
        """Return the canvas widgets."""
        return self.gaussian_canvas.get_tk_widget(), self.ring_canvas.get_tk_widget(), self.growth_canvas.get_tk_widget()
