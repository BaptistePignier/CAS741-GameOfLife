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
        
        # Figure unique avec deux sous-graphiques
        self.fig, (self.ax_con_nhood, self.ax_growth) = plt.subplots(2, 1)
        self.fig.set_facecolor('white')
        
        # Ajustement des marges pour donner plus d'espace aux graduations et titres
        # Augmenter la marge gauche pour les graduations et les étiquettes d'axe Y
        # Augmenter la marge supérieure pour les titres
        self.fig.subplots_adjust(left=0.22, right=0.95, top=0.92, bottom=0.1, hspace=0.4)
        
        # Configuration de l'axe pour le kernel
        self.ax_con_nhood.set_xticks([])
        self.ax_con_nhood.set_yticks([])
        self.ax_con_nhood.set_title("Neighborhood visualization", pad=10)
        
        # Configuration de l'axe pour la croissance
        # Garder les graduations pour mieux visualiser les valeurs
        self.ax_growth.set_title("Growth function", pad=10)
        
        # Un seul canvas pour les deux graphiques
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')
        
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
        x_init = [0, 0.3]
        y_init = [0, 0]
        self.growth_line, = self.ax_growth.plot(x_init, y_init, 'g-', linewidth=2)
        self.ax_growth.set_ylim(-1.2, 1.2)
        
        self.ax_growth.grid(True, linestyle='--', alpha=0.3)
        
        # Mise à jour initiale du canvas
        self.canvas.draw()

    def update_growth_plot(self, x_values, y_values):
        """Met à jour le graphique de croissance."""
        self.growth_line.set_xdata(x_values)
        self.growth_line.set_ydata(y_values)
        self.canvas.draw_idle()
    
    def update_growth_axes(self, xmin, xmax, ymin, ymax, continuous=True):
        """Met à jour les limites et les graduations des axes du graphique de croissance.
        
        Args:
            xmin, xmax: limites de l'axe x
            ymin, ymax: limites de l'axe y
            continuous: si True, configure pour mode continu (Lenia), sinon pour mode discret (GoL)
        """
        self.ax_growth.set_xlim(xmin, xmax)
        self.ax_growth.set_ylim(ymin, ymax)
        
        if continuous:
            # Graduations pour le mode continu (Lenia)
            self.ax_growth.set_xticks(np.linspace(xmin, xmax, 7))
            self.ax_growth.set_yticks(np.linspace(-1, 1, 5))
            # Formatter avec une seule décimale
            self.ax_growth.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
        else:
            # Graduations pour le mode discret (GoL)
            self.ax_growth.set_xticks(range(0, 9))
            self.ax_growth.set_yticks([-1, -0.5, 0, 0.5, 1])
            # Pour le mode discret, utiliser des entiers
            self.ax_growth.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        
        # Ajustement de l'espacement des étiquettes
        self.ax_growth.tick_params(axis='both', which='major', labelsize=9)
        self.ax_growth.tick_params(axis='y', pad=8)  # Plus d'espace pour les étiquettes de l'axe y
        
        self.canvas.draw_idle()
        
    def update_nhood_plot(self, kernel):
        """Méthode de compatibilité qui appelle update_con_nhood_plot."""
        self.con_nhood_image.set_array(kernel)
        self.canvas.draw_idle()

    def get_frame(self):
        """Renvoie le frame principal."""
        return self.frame

    def get_canvas(self):
        """Renvoie les widgets canvas."""
        return None, self.canvas.get_tk_widget(), self.canvas.get_tk_widget()
