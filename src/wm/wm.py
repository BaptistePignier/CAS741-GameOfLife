import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Separator

class WindowManager:
    def __init__(self, root, sim_size, panel_width):
        self.root = root
        self.sim_size = sim_size
        self.panel_width = panel_width
        
        # Configuration de la fenêtre principale
        self.root.title("Jeu de la Vie Interactif")
        self.root.geometry(f"{sim_size + panel_width}x{sim_size}")
        
        # Configuration du layout principal
        self.setup_main_layout()
        
        # Configuration du panneau de contrôle
        self.setup_control_panel()
    
    def setup_main_layout(self):
        """Configure le layout principal de la fenêtre."""
        # Zone principale pour la simulation
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Panneau latéral pour les contrôles
        self.root.columnconfigure(1, weight=0, minsize=self.panel_width)
    
    def setup_control_panel(self):
        """Configure le panneau de contrôle."""
        self.control_frame = ttk.Frame(self.root, width=self.panel_width, height=self.sim_size)
        self.control_frame.grid(row=0, column=1, sticky='ns')
        self.control_frame.grid_propagate(False)
        
        # Configuration du grid pour les éléments de contrôle
        self.control_frame.grid_columnconfigure(0, weight=1)
    
    def place_views(self, sim_view, us_view, fi_view):
        """Place toutes les vues dans l'interface."""
        self.place_simulation_view(sim_view)
        self.place_control_panel(us_view, fi_view)
    
    def place_simulation_view(self, sim_view):
        """Place la vue de simulation dans la zone principale."""
        sim_view.get_canvas().grid(row=0, column=0, sticky='nsew')
    
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
    
    def get_control_frame(self):
        """Retourne le frame de contrôle pour les widgets enfants."""
        return self.control_frame
