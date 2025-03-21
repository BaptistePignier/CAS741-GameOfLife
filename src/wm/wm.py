import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Separator

class WindowManager:
    def __init__(self, root, sim_size, panel_width):
        self.root = root
        self.sim_size = sim_size
        self.panel_width = panel_width
        self.sim_view = None  # Référence à la vue de simulation
        
        # Configuration de la fenêtre principale
        self.root.title("Jeu de la Vie Interactif")
        window_width = sim_size + panel_width
        window_height = int(sim_size * 0.75)  # Ratio initial pour la fenêtre
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Configuration du layout principal
        self.setup_main_layout()
        
        # Configuration du panneau de contrôle
        self.setup_control_panel()
        
        # Calcul des dimensions de la grille
        self.cell_size = 10  # Taille fixe des cellules
        self.calculate_grid_dimensions()
        
        # Configuration du gestionnaire de redimensionnement
        self.root.bind('<Configure>', self._on_window_resize)
    
    def setup_main_layout(self):
        """Configure le layout principal de la fenêtre."""
        # Zone principale pour la simulation
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Panneau latéral pour les contrôles
        self.root.columnconfigure(1, weight=0, minsize=self.panel_width)
    
    def setup_control_panel(self):
        """Configure le panneau de contrôle."""
        self.control_frame = ttk.Frame(self.root, width=self.panel_width)
        self.control_frame.grid(row=0, column=1, sticky='nsew')
        self.control_frame.grid_propagate(False)
        
        # Configuration du grid pour les éléments de contrôle
        self.control_frame.grid_columnconfigure(0, weight=1)
    
    def place_views(self, sim_view, us_view, fi_view):
        """Place toutes les vues dans l'interface."""
        self.sim_view = sim_view  # Sauvegarde la référence
        self.place_simulation_view(sim_view)
        
        # Place les contrôles utilisateur dans le panneau latéral
        us_frame = us_view.get_frame()
        us_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Place la vue de la fonction gaussienne en bas du panneau de contrôle
        fi_frame = fi_view.get_frame()
        fi_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        
        # Configure le redimensionnement
        self.control_frame.grid_rowconfigure(1, weight=1)  # Le graphique peut s'étendre
    
    def place_simulation_view(self, sim_view):
        """Place la vue de simulation dans la zone principale."""
        canvas = sim_view.get_canvas()
        canvas.grid(row=0, column=0, sticky='nsew')
        
        # Calcul des dimensions de la zone de simulation
        sim_width = self.root.winfo_width() - self.panel_width
        sim_height = self.root.winfo_height()
        sim_view.update_dimensions(sim_width, sim_height)
    
    def place_control_panel(self, us_view):
        """Place tous les éléments de contrôle dans le panneau latéral."""
        us_view.get_frame().grid(row=0, column=0, sticky='nsew')
    
    def calculate_grid_dimensions(self):
        """Calcule les dimensions de la grille basées sur l'espace disponible."""
        sim_width = self.root.winfo_width() - self.panel_width
        sim_height = self.root.winfo_height()
        
        # Calcul du nombre de cellules dans chaque dimension
        self.grid_width = sim_width // self.cell_size
        self.grid_height = sim_height // self.cell_size
    
    def get_grid_dimensions(self):
        """Retourne les dimensions actuelles de la grille."""
        return self.grid_width, self.grid_height
    
    def get_window_dimensions(self):
        """Retourne les dimensions actuelles de la fenêtre de simulation."""
        return (self.root.winfo_width() - self.panel_width,
                self.root.winfo_height())
    
    def _on_window_resize(self, event):
        """Gère le redimensionnement de la fenêtre."""
        if event.widget == self.root and self.sim_view is not None:
            # Mise à jour des dimensions de la simulation
            sim_width = self.root.winfo_width() - self.panel_width
            sim_height = self.root.winfo_height()
            self.sim_view.update_dimensions(sim_width, sim_height)
            self.calculate_grid_dimensions()
    
    def get_control_frame(self):
        """Retourne le frame de contrôle pour les widgets enfants."""
        return self.control_frame
