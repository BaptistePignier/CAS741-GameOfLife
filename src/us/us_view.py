import tkinter as tk
from tkinter import ttk

class UsView:
    def __init__(self, control_frame):
        # Création des boutons
        self.toggle_button = ttk.Button(control_frame, text="Start")
        self.reset_button = ttk.Button(control_frame, text="Reset")
        
        # Label pour afficher la vitesse actuelle
        self.speed_label = ttk.Label(control_frame, text="FPS : 60")
        
        # Création du slider de vitesse (générations par seconde)
        self.speed_slider = ttk.Scale(
            control_frame,
            from_=1,
            to=200,
            orient='horizontal',
            command=self._update_speed_label
        )
        self.speed_slider.set(60)  # 60 générations par seconde par défaut
        
        # Création des sliders gaussiens
        self.alpha_slider = ttk.Scale(control_frame, from_=0.1, to=2.0, orient='horizontal')
        self.alpha_slider.set(1.0)
        
        self.beta_slider = ttk.Scale(control_frame, from_=0.1, to=3.0, orient='horizontal')
        self.beta_slider.set(1.0)
    
    def get_widgets(self):
        """Retourne tous les widgets importants."""
        return {
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
    
    def _update_speed_label(self, value):
        """Met à jour le label de vitesse."""
        self.speed_label.config(text=f"FPS : {int(float(value))}")
        
    def set_speed_command(self, command):
        """Définit la commande du slider de vitesse."""
        # Combine la mise à jour du label avec la commande originale
        def combined_command(value):
            self._update_speed_label(value)
            command(value)
        self.speed_slider.config(command=combined_command)
    
    def set_gaussian_commands(self, alpha_command, beta_command):
        """Définit les commandes des sliders gaussiens."""
        self.alpha_slider.config(command=alpha_command)
        self.beta_slider.config(command=beta_command)
    

