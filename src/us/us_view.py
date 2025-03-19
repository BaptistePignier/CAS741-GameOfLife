import tkinter as tk
from tkinter import ttk

class UsView:
    def __init__(self, root, panel_width, sim_size):
        # Création du panneau de contrôle
        self.control_frame = ttk.Frame(root, width=panel_width, height=sim_size)
        self.control_frame.grid(row=0, column=1, sticky='ns')
        self.control_frame.grid_propagate(False)
        
        # Configuration du grid dans le control_frame
        self.control_frame.grid_columnconfigure(0, weight=1)
        
        # Création des boutons
        self.toggle_button = ttk.Button(self.control_frame, text="Start")
        self.toggle_button.grid(row=0, column=0, pady=10, padx=5, sticky='ew')
        
        self.reset_button = ttk.Button(self.control_frame, text="Reset")
        self.reset_button.grid(row=1, column=0, pady=10, padx=5, sticky='ew')
        
        # Création du slider de vitesse
        ttk.Label(self.control_frame, text="Vitesse de simulation").grid(row=2, column=0, pady=(10,0), padx=5)
        self.speed_slider = ttk.Scale(self.control_frame, from_=1, to=1000, orient='horizontal')
        self.speed_slider.set(10)
        self.speed_slider.grid(row=3, column=0, pady=(0,10), padx=5, sticky='ew')
        
        # Sliders pour les paramètres de la gaussienne
        ttk.Label(self.control_frame, text="α (amplitude)").grid(row=4, column=0, pady=(10,0), padx=5)
        self.alpha_slider = ttk.Scale(self.control_frame, from_=0.1, to=2.0, orient='horizontal')
        self.alpha_slider.set(1.0)
        self.alpha_slider.grid(row=5, column=0, pady=(0,10), padx=5, sticky='ew')
        
        ttk.Label(self.control_frame, text="β (largeur)").grid(row=6, column=0, pady=(10,0), padx=5)
        self.beta_slider = ttk.Scale(self.control_frame, from_=0.1, to=3.0, orient='horizontal')
        self.beta_slider.set(1.0)
        self.beta_slider.grid(row=7, column=0, pady=(0,10), padx=5, sticky='ew')
    
    def get_widgets(self):
        """Retourne tous les widgets importants."""
        return {
            'control_frame': self.control_frame,
            'toggle_button': self.toggle_button,
            'reset_button': self.reset_button,
            'speed_slider': self.speed_slider,
            'alpha_slider': self.alpha_slider,
            'beta_slider': self.beta_slider
        }
    
    def set_toggle_command(self, command):
        """Définit la commande du bouton toggle."""
        self.toggle_button.config(command=command)
    
    def set_reset_command(self, command):
        """Définit la commande du bouton reset."""
        self.reset_button.config(command=command)
    
    def set_speed_command(self, command):
        """Définit la commande du slider de vitesse."""
        self.speed_slider.config(command=command)
    
    def set_gaussian_commands(self, alpha_command, beta_command):
        """Définit les commandes des sliders gaussiens."""
        self.alpha_slider.config(command=alpha_command)
        self.beta_slider.config(command=beta_command)
