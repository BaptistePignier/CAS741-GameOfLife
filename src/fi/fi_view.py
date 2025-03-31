import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FiView:
    def __init__(self, master, figsize=(6, 6)):
        """Initializes the FiView with frames and plots for displaying gaussian, kernel, and growth functions.
        
        Args:
            master: The parent Tkinter widget.
            figsize (tuple): The size of the matplotlib figures.
        """
        # Frame principal
        self.frame = ttk.Frame(master)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=2)  # 2/3 pour le haut
        self.frame.grid_rowconfigure(1, weight=1)  # 1/3 pour le bas
        
        # Frame du haut (gaussienne + noyau)
        self.top_frame = ttk.LabelFrame(self.frame, text="Fonction gaussienne et noyau")
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)  # Gaussienne
        self.top_frame.grid_rowconfigure(1, weight=2)  # Noyau
        
        # Frame pour la gaussienne
        self.gaussian_frame = ttk.Frame(self.top_frame)
        self.gaussian_frame.grid(row=0, column=0, sticky='nsew')
        self.gaussian_frame.grid_columnconfigure(0, weight=1)
        self.gaussian_frame.grid_rowconfigure(0, weight=1)
        
        # Frame pour le noyau
        self.ring_frame = ttk.Frame(self.top_frame)
        self.ring_frame.grid(row=1, column=0, sticky='nsew')
        self.ring_frame.grid_columnconfigure(0, weight=1)
        self.ring_frame.grid_rowconfigure(0, weight=1)
        
        # Frame du bas (croissance)
        self.bottom_frame = ttk.LabelFrame(self.frame, text="Fonction de croissance")
        self.bottom_frame.grid(row=1, column=0, sticky='nsew')
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        
        # Configuration des figures avec des tailles adaptées
        # La gaussienne prend 1/3 de la hauteur du top frame
        self.gaussian_fig = plt.figure(constrained_layout=True, figsize=(3, 1))
        self.gaussian_fig.set_facecolor('white')
        self.ax_gaussian = self.gaussian_fig.add_subplot(111)
        self.ax_gaussian.set_xticks([])
        self.ax_gaussian.set_yticks([])
        
        # Le noyau prend 2/3 de la hauteur du top frame
        self.ring_fig = plt.figure(constrained_layout=True, figsize=(3, 2))
        self.ring_fig.set_facecolor('white')
        self.ax_ring = self.ring_fig.add_subplot(111)
        self.ax_ring.set_xticks([])
        self.ax_ring.set_yticks([])
        
        # La croissance prend toute la hauteur du bottom frame
        self.growth_fig = plt.figure(constrained_layout=True, figsize=(3, 1.5))
        self.growth_fig.set_facecolor('white')
        self.ax_growth = self.growth_fig.add_subplot(111)
        self.ax_growth.set_xticks([])
        self.ax_growth.set_yticks([])
        
        # Configuration des canvas
        self.gaussian_canvas = FigureCanvasTkAgg(self.gaussian_fig, master=self.gaussian_frame)
        self.gaussian_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        self.ring_canvas = FigureCanvasTkAgg(self.ring_fig, master=self.ring_frame)
        self.ring_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        self.growth_canvas = FigureCanvasTkAgg(self.growth_fig, master=self.bottom_frame)
        self.growth_canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
        # Configuration initiale des graphiques
        x_init = [0, 1]
        y_init = [0, 0]
        
        # Graphe gaussien
        self.line, = self.ax_gaussian.plot(x_init, y_init, 'b-', linewidth=2)
        self.ax_gaussian.set_xlim(0, 1)
        self.ax_gaussian.set_ylim(-0.2, 1.2)
        self.ax_gaussian.grid(True, linestyle='--', alpha=0.3)
        
        # Graphe du noyau
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
        
        # Graphe de croissance
        self.growth_line, = self.ax_growth.plot(x_init, y_init, 'g-', linewidth=2)
        self.ax_growth.set_xlim(0, 1)
        self.ax_growth.set_ylim(-0.2, 1.2)
        self.ax_growth.grid(True, linestyle='--', alpha=0.3)
        
        # Mise à jour initiale des canvas
        self.gaussian_canvas.draw()
        self.ring_canvas.draw()
        self.growth_canvas.draw()
    
    def update_plot(self, x_values, y_values, y_max=None, is_growth=False):
        """Met à jour le graphe gaussien avec les nouvelles valeurs."""
        if is_growth:
            self.growth_line.set_xdata(x_values)
            self.growth_line.set_ydata(y_values)
            if y_max is not None:
                self.ax_growth.set_ylim(-0.2, y_max * 1.2)
            self.growth_canvas.draw_idle()
        else:
            self.line.set_xdata(x_values)
            self.line.set_ydata(y_values)
            if y_max is not None:
                self.ax_gaussian.set_ylim(-0.2, y_max * 1.2)
            self.gaussian_canvas.draw_idle()
    
    def update_ring_plot(self, kernel):
        """Met à jour le graphe du noyau en anneau."""
        self.ring_image.set_array(kernel)
        self.ring_canvas.draw_idle()

    def get_frame(self):
        """Retourne le frame principal."""
        return self.frame

    def get_canvas(self):
        """Retourne les widgets canvas."""
        return self.gaussian_canvas.get_tk_widget(), self.ring_canvas.get_tk_widget(), self.growth_canvas.get_tk_widget()
