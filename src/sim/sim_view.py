import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class SimView:
    def __init__(self, master, width, height, cell_size):
        """Initialise la vue de simulation.
        
        Args:
            master: Widget parent Tkinter
            width (int): Largeur de la fenêtre en pixels
            height (int): Hauteur de la fenêtre en pixels
            cell_size (int): Taille d'une cellule en pixels
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.master = master
        self.current_grid = None
        
        # Calcul des dimensions de la grille
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        
        # Création de la figure matplotlib avec une taille fixe
        self.fig = plt.figure(figsize=(width/100, height/100))  # DPI standard = 100
        self.fig.set_facecolor('none')  # Fond transparent
        
        # Configuration optimisée de l'axe
        self.ax = self.fig.add_subplot(111)
        self.ax.set_position([0, 0, 1, 1])  # Utilise tout l'espace
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_frame_on(False)
        
        # Configuration de l'affichage avec une colormap optimisée
        self.grid_display = self.ax.imshow(
            np.zeros((self.grid_height, self.grid_width)),
            cmap='binary',
            interpolation='nearest',
            aspect='equal',
            vmin=0,
            vmax=1
        )
        
        # Création du canvas Tkinter avec une taille fixe
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.configure(
            width=width,
            height=height,
            bd=0,
            highlightthickness=0
        )
        
        # Configuration des limites de la vue
        self.ax.set_xlim(0, self.grid_width)
        self.ax.set_ylim(0, self.grid_height)
        
        # Désactive les événements matplotlib inutiles pour améliorer les performances
        self.canvas.mpl_disconnect(self.canvas.callbacks.callbacks['button_press_event'][0])
        self.canvas.mpl_disconnect(self.canvas.callbacks.callbacks['button_release_event'][0])
        self.canvas.mpl_disconnect(self.canvas.callbacks.callbacks['motion_notify_event'][0])
        
        # Pré-allocation du buffer pour éviter les allocations répétées
        self._grid_buffer = np.zeros((self.grid_height, self.grid_width))
    
    def update_display(self, grid):
        """Met à jour l'affichage de la grille.
        
        Args:
            grid (numpy.ndarray): Nouvelle grille à afficher
        """
        # Mise à jour optimisée de l'affichage
        if grid is not None and grid.shape == self._grid_buffer.shape:
            # Évite la copie si la grille n'a pas changé
            if not np.array_equal(self._grid_buffer, grid):
                np.copyto(self._grid_buffer, grid)
                self.grid_display.set_array(self._grid_buffer)
                self.canvas.draw()
    
    def get_canvas(self):
        """Retourne le widget canvas.
        
        Returns:
            tkinter.Widget: Widget canvas Tkinter
        """
        return self.canvas.get_tk_widget()
    
    def __del__(self):
        """Nettoyage des ressources matplotlib."""
        plt.close(self.fig)
