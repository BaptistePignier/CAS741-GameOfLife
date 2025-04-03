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
        self.frame.grid_rowconfigure(0, weight=1)  # Kernel
        self.frame.grid_rowconfigure(1, weight=1)  # Growth
        
        # Figure unique avec deux sous-graphiques
        self.fig, (self.ax_con_nhood, self.ax_growth) = plt.subplots(2, 1, figsize=(6, 6), 
                                               gridspec_kw={'height_ratios': [2, 1]})
        self.fig.set_facecolor('white')
        self.fig.tight_layout(pad=3)
        
        # Configuration de l'axe pour le kernel
        self.ax_con_nhood.set_xticks([])
        self.ax_con_nhood.set_yticks([])
        self.ax_con_nhood.set_title("Neighborhood visualization")
        
        # Configuration de l'axe pour la croissance
        self.ax_growth.set_xticks([])
        self.ax_growth.set_yticks([])
        self.ax_growth.set_title("Growth function")
        
        # Un seul canvas pour les deux graphiques
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=2, sticky='nsew')
        
        # Initialisation du graphique kernel
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
        
        # Initialisation du graphique de croissance
        x_init = [0, 1]
        y_init = [0, 0]
        self.growth_line, = self.ax_growth.plot(x_init, y_init, 'g-', linewidth=2)
        self.ax_growth.set_ylim(-0.2, 1.2)
        self.ax_growth.grid(True, linestyle='--', alpha=0.3)
        
        # Mise à jour initiale du canvas
        self.canvas.draw()

    def update_growth_plot(self, x_values, y_values, y_max=None):
        """Met à jour le graphique de croissance."""
        self.growth_line.set_xdata(x_values)
        self.growth_line.set_ydata(y_values)
        if y_max is not None:
            self.ax_growth.set_ylim(-0.2, y_max * 1.2)
        self.canvas.draw_idle()
    
    def update_con_nhood_plot(self, kernel):
        """Met à jour le graphique du voisinage de connectivité."""
        self.con_nhood_image.set_array(kernel)
        self.canvas.draw_idle()
        
    def update_nhood_plot(self, kernel):
        """Méthode de compatibilité qui appelle update_con_nhood_plot."""
        self.update_con_nhood_plot(kernel)

    def get_frame(self):
        """Renvoie le frame principal."""
        return self.frame

    def get_canvas(self):
        """Renvoie les widgets canvas."""
        return None, self.canvas.get_tk_widget(), self.canvas.get_tk_widget()
        
    def update_gaussian_plot(self, x_values, y_values, y_max=None):
        """Méthode fictive pour compatibilité avec le contrôleur."""
        pass
        