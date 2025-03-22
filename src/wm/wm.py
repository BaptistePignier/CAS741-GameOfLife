import tkinter as tk
from tkinter import ttk

class WindowManager:
    def __init__(self, root, sim_size, panel_width):
        """Initialise le gestionnaire de fenêtres.
        
        Args:
            root: Fenêtre principale Tkinter
            sim_size (int): Taille de la zone de simulation en pixels
            panel_width (int): Largeur du panneau de contrôle en pixels
        """
        self.root = root
        self.sim_size = sim_size
        self.panel_width = panel_width
        self.sim_view = None
        
        # Configuration de la fenêtre principale
        self.root.title("Jeu de la Vie")
        window_width = sim_size + panel_width
        window_height = sim_size  # Fenêtre carrée pour la simulation
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Configuration du layout principal
        self.setup_main_layout()
        
        # Configuration du panneau de contrôle
        self.setup_control_panel()
        
        # Configuration de la taille des cellules
        self.cell_size = 10
    
    def setup_main_layout(self):
        """Configure le layout principal de la fenêtre."""
        # Zone de simulation (extensible)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Panneau de contrôle (largeur fixe)
        self.root.grid_columnconfigure(1, weight=0, minsize=self.panel_width)
        
        # Empêche le redimensionnement en dessous d'une taille minimale
        min_width = self.panel_width + 300  # 300px minimum pour la simulation
        min_height = 400  # Hauteur minimale raisonnable
        self.root.minsize(min_width, min_height)
    
    def setup_control_panel(self):
        """Configure le panneau de contrôle."""
        # Frame principal des contrôles
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Configuration du grid pour les contrôles
        self.control_frame.grid_columnconfigure(0, weight=1)
        
        # Empêche le redimensionnement horizontal du panneau
        self.control_frame.grid_propagate(False)
        self.control_frame.configure(width=self.panel_width)
    
    def place_views(self, sim_view, us_view, fi_view):
        """Place toutes les vues dans l'interface.
        
        Args:
            sim_view: Vue de la simulation
            us_view: Vue des contrôles utilisateur
            fi_view: Vue de la fonction d'influence
        """
        # Place la vue de simulation
        self.sim_view = sim_view
        sim_canvas = sim_view.get_canvas()
        sim_canvas.grid(row=0, column=0, sticky='nsew')
        
        # Place les vues de contrôle
        us_frame = us_view.get_frame()
        us_frame.grid(row=0, column=0, sticky='ew')
        
        # Séparateur entre les contrôles et le graphe
        ttk.Separator(self.control_frame, orient='horizontal').grid(
            row=1, column=0, sticky='ew', pady=10
        )
        
        # Place la vue de la fonction gaussienne
        fi_frame = fi_view.get_frame()
        fi_frame.grid(row=2, column=0, sticky='ew')
    
    def get_control_frame(self):
        """Retourne le frame de contrôle.
        
        Returns:
            ttk.Frame: Frame contenant les contrôles
        """
        return self.control_frame
