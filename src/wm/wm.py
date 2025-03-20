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
        self.place_control_panel(us_view, fi_view)
    
    def place_simulation_view(self, sim_view):
        """Place la vue de simulation dans la zone principale."""
        canvas = sim_view.get_canvas()
        canvas.grid(row=0, column=0, sticky='nsew')
        
        # Calcul des dimensions de la zone de simulation
        sim_width = self.root.winfo_width() - self.panel_width
        sim_height = self.root.winfo_height()
        sim_view.update_dimensions(sim_width, sim_height)
    
    def place_control_panel(self, us_view, fi_view):
        """Place tous les éléments de contrôle dans le panneau latéral."""
        current_row = 0
        
        # Boutons de contrôle
        us_view.toggle_button.grid(row=current_row, column=0, pady=10, padx=5, sticky='ew')
        current_row += 1
        
        us_view.reset_button.grid(row=current_row, column=0, pady=10, padx=5, sticky='ew')
        current_row += 1
        
        # Contrôle de la vitesse
        ttk.Label(self.control_frame, text="Générations par seconde").grid(
            row=current_row, column=0, pady=(10,0), padx=5)
        current_row += 1
        
        us_view.speed_label.grid(row=current_row, column=0, pady=(5,0), padx=5)
        current_row += 1
        
        us_view.speed_slider.grid(row=current_row, column=0, pady=(0,10), padx=5, sticky='ew')
        current_row += 1
        
        # Section gaussienne
        Separator(self.control_frame, orient='horizontal').grid(
            row=current_row, column=0, pady=10, sticky='ew')
        current_row += 1
        
        ttk.Label(self.control_frame, text="Paramètres de la fonction").grid(
            row=current_row, column=0, pady=(10,0), padx=5)
        current_row += 1
        
        ttk.Label(self.control_frame, text="α (amplitude)").grid(
            row=current_row, column=0, pady=(10,0), padx=5)
        current_row += 1
        
        us_view.alpha_slider.grid(row=current_row, column=0, pady=(0,10), padx=5, sticky='ew')
        current_row += 1
        
        ttk.Label(self.control_frame, text="β (largeur)").grid(
            row=current_row, column=0, pady=(10,0), padx=5)
        current_row += 1
        
        us_view.beta_slider.grid(row=current_row, column=0, pady=(0,10), padx=5, sticky='ew')
        current_row += 1
        
        # Graphe gaussien
        fi_view.canvas.get_tk_widget().grid(
            row=current_row, column=0, pady=10, padx=5, sticky='ew')
    
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
