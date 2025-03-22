import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class FiView:
    def __init__(self, master, figsize=(6, 6)):
        # Création du frame interne
        self.frame = ttk.Frame(master)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        # Création de la figure matplotlib
        self.fig = plt.figure(figsize=figsize, constrained_layout=True)  
        self.fig.set_facecolor('none')  
        
        # Configuration du layout pour avoir des graphiques bien proportionnés
        gs = self.fig.add_gridspec(2, 1, height_ratios=[0.8, 1.2])
        
        # Graphe de la gaussienne (en haut)
        self.ax_gaussian = self.fig.add_subplot(gs[0])
        self.ax_gaussian.set_title('exp(- 0.5 * ((x - μ)/σ)²)')
        
        # Configuration initiale du graphe gaussien
        x_init = [-2, 2]
        y_init = [0, 1]
        self.line, = self.ax_gaussian.plot(x_init, y_init, 'b-', linewidth=2)
        self.ax_gaussian.set_ylim(-0.2, 1.2)
        self.ax_gaussian.grid(True, linestyle='--', alpha=0.3)
        self.ax_gaussian.set_xlabel('x')
        self.ax_gaussian.set_ylabel('y')
        
        # Graphe du noyau en anneau (en bas)
        self.ax_ring = self.fig.add_subplot(gs[1])
        self.ax_ring.set_title('Noyau en anneau')
        
        # Initialisation du graphe du noyau en anneau avec une meilleure résolution
        kernel_size = 27  
        self.ring_image = self.ax_ring.imshow(
            np.zeros((kernel_size, kernel_size)),
            cmap='viridis',
            extent=[-2, 2, -2, 2],
            aspect='equal',
            interpolation='bilinear'  
        )
        self.ax_ring.set_xticks([-2, -1, 0, 1, 2])
        self.ax_ring.set_yticks([-2, -1, 0, 1, 2])
        self.ax_ring.grid(True, linestyle='--', alpha=0.3)
        
        # Création du canvas Tkinter avec une taille minimale
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        canvas_widget.configure(width=200, height=300)  
    
    def update_plot(self, x_values, y_values, y_max=None):
        """Met à jour le graphe gaussien avec les nouvelles valeurs."""
        self.line.set_xdata(x_values)
        self.line.set_ydata(y_values)
        if y_max is not None:
            self.ax_gaussian.set_ylim(-0.2, y_max * 1.2)
        self.canvas.draw()
    
    def update_ring_plot(self, kernel):
        """Met à jour le graphe du noyau en anneau."""
        self.ring_image.set_array(kernel)
        self.canvas.draw()
    
    def get_frame(self):
        """Retourne le frame interne."""
        return self.frame

    def get_canvas(self):
        """Retourne le widget canvas."""
        return self.canvas.get_tk_widget()
