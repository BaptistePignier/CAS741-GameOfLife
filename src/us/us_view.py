import tkinter as tk
from tkinter import ttk

class UsView:
    def __init__(self, control_frame):
        # Création du frame interne
        self.frame = ttk.Frame(control_frame)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Création des widgets
        self._create_control_buttons()
        self._create_speed_frame()
        self._create_gaussian_frame()
    
    def _create_control_buttons(self):
        """Crée les boutons de contrôle."""
        self.toggle_button = ttk.Button(self.frame, text="Démarrer")
        self.toggle_button.grid(row=0, column=0, pady=5)
        
        self.reset_button = ttk.Button(self.frame, text="Réinitialiser")
        self.reset_button.grid(row=1, column=0, pady=5)
    
    def _create_speed_frame(self):
        """Crée le frame de contrôle de la vitesse."""
        speed_frame = ttk.LabelFrame(self.frame, text="Vitesse")
        speed_frame.grid_columnconfigure(0, weight=1)
        speed_frame.grid(row=2, column=0, pady=5, padx=5, sticky='ew')
        
        # Label FPS dynamique
        self.speed_label = ttk.Label(speed_frame, text="FPS : 60")
        self.speed_label.grid(row=0, column=0, pady=(5,0))
        
        # Slider de vitesse
        self.speed_slider = ttk.Scale(
            speed_frame,
            from_=1,
            to=120,
            orient=tk.HORIZONTAL,
            value=60
        )
        self.speed_slider.grid(row=1, column=0, pady=5, padx=10, sticky='ew')
    
    def _create_gaussian_frame(self):
        """Crée le frame des paramètres gaussiens."""
        gaussian_frame = ttk.LabelFrame(self.frame, text="Fonction gaussienne")
        gaussian_frame.grid_columnconfigure(0, weight=1)
        gaussian_frame.grid(row=3, column=0, pady=5, padx=5, sticky='ew')
        
        # Paramètre μ (mu)
        self.mu_label = ttk.Label(gaussian_frame, text="μ : 0.50")
        self.mu_label.grid(row=0, column=0, pady=(5,0))
        
        self.mu_slider = ttk.Scale(
            gaussian_frame,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            value=0.5
        )
        self.mu_slider.grid(row=1, column=0, pady=(0,5), padx=10, sticky='ew')
        
        # Paramètre σ (sigma)
        self.sigma_label = ttk.Label(gaussian_frame, text="σ : 0.15")
        self.sigma_label.grid(row=2, column=0, pady=(5,0))
        
        self.sigma_slider = ttk.Scale(
            gaussian_frame,
            from_=0.05,
            to=0.5,
            orient=tk.HORIZONTAL,
            value=0.15
        )
        self.sigma_slider.grid(row=3, column=0, pady=(0,5), padx=10, sticky='ew')
    
    def _update_speed_label(self, value):
        """Met à jour le label de vitesse."""
        self.speed_label.config(text=f"FPS : {int(float(value))}")
    
    def set_toggle_command(self, command):
        """Configure la commande du bouton toggle."""
        self.toggle_button.config(command=command)
    
    def set_reset_command(self, command):
        """Configure la commande du bouton reset."""
        self.reset_button.config(command=command)
    
    def set_speed_command(self, command):
        """Configure la commande du slider de vitesse."""
        def combined_command(value):
            self._update_speed_label(value)
            command(float(value))
        self.speed_slider.config(command=combined_command)
    
    def set_gaussian_commands(self, mu_command, sigma_command):
        """Configure les commandes des sliders gaussiens."""
        def update_mu(value):
            self.mu_label.config(text=f"μ : {float(value):.2f}")
            mu_command(value)
        
        def update_sigma(value):
            self.sigma_label.config(text=f"σ : {float(value):.2f}")
            sigma_command(value)
        
        self.mu_slider.config(command=update_mu)
        self.sigma_slider.config(command=update_sigma)
    
    def get_frame(self):
        """Retourne le frame interne."""
        return self.frame
    
    def get_widgets(self):
        """Retourne un dictionnaire des widgets pour le modèle."""
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
