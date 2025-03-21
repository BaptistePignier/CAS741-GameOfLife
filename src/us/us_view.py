import tkinter as tk
from tkinter import ttk

class UsView:
    def __init__(self, control_frame):
        # Création du frame interne
        self.frame = ttk.Frame(control_frame)
        
        # Configuration du grid
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Bouton de contrôle
        self.toggle_button = ttk.Button(self.frame, text="Démarrer")
        self.toggle_button.grid(row=0, column=0, pady=5)
        
        # Bouton de réinitialisation
        self.reset_button = ttk.Button(self.frame, text="Réinitialiser")
        self.reset_button.grid(row=1, column=0, pady=5)
        
        # Frame pour la vitesse
        speed_frame = ttk.LabelFrame(self.frame, text="Vitesse")
        speed_frame.grid_columnconfigure(0, weight=1)
        speed_frame.grid(row=2, column=0, pady=5, padx=5, sticky='ew')
        
        # Label et slider pour la vitesse
        self.speed_label = ttk.Label(speed_frame, text="FPS : 60")
        self.speed_label.grid(row=0, column=0, pady=(5,0))
        
        self.speed_slider = ttk.Scale(speed_frame, from_=1, to=120, orient=tk.HORIZONTAL)
        self.speed_slider.set(60)
        self.speed_slider.grid(row=1, column=0, pady=5, padx=10, sticky='ew')
        
        # Frame pour les paramètres gaussiens
        gaussian_frame = ttk.LabelFrame(self.frame, text="Fonction gaussienne")
        gaussian_frame.grid_columnconfigure(0, weight=1)
        gaussian_frame.grid(row=3, column=0, pady=5, padx=5, sticky='ew')
        
        # Label et slider pour mu
        self.mu_label = ttk.Label(gaussian_frame, text="μ : 0.5")
        self.mu_label.grid(row=0, column=0, pady=(5,0))
        
        self.mu_slider = ttk.Scale(gaussian_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL)
        self.mu_slider.set(0.5)
        self.mu_slider.grid(row=1, column=0, pady=(0,5), padx=10, sticky='ew')
        
        # Label et slider pour sigma
        self.sigma_label = ttk.Label(gaussian_frame, text="σ : 0.15")
        self.sigma_label.grid(row=2, column=0, pady=(5,0))
        
        self.sigma_slider = ttk.Scale(gaussian_frame, from_=0.05, to=0.5, orient=tk.HORIZONTAL)
        self.sigma_slider.set(0.15)
        self.sigma_slider.grid(row=3, column=0, pady=(0,5), padx=10, sticky='ew')
    
    def get_frame(self):
        """Retourne le frame interne."""
        return self.frame
    
    def get_widgets(self):
        """Retourne tous les widgets importants."""
        return {
            'toggle_button': self.toggle_button,
            'reset_button': self.reset_button,
            'speed_slider': self.speed_slider,
            'speed_label': self.speed_label,
            'mu_slider': self.mu_slider,
            'sigma_slider': self.sigma_slider,
            'mu_label': self.mu_label,
            'sigma_label': self.sigma_label
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
    
    def _update_mu_label(self, value):
        """Met à jour le label mu."""
        self.mu_label.config(text=f"μ : {float(value):.2f}")
    
    def _update_sigma_label(self, value):
        """Met à jour le label sigma."""
        self.sigma_label.config(text=f"σ : {float(value):.2f}")
    
    def set_speed_command(self, command):
        """Définit la commande du slider de vitesse."""
        def combined_command(value):
            self._update_speed_label(value)
            command(value)
        self.speed_slider.config(command=combined_command)
    
    def set_gaussian_commands(self, mu_command, sigma_command):
        """Définit les commandes des sliders gaussiens."""
        def combined_mu_command(value):
            self._update_mu_label(value)
            mu_command(value)
        
        def combined_sigma_command(value):
            self._update_sigma_label(value)
            sigma_command(value)
        
        self.mu_slider.config(command=combined_mu_command)
        self.sigma_slider.config(command=combined_sigma_command)
