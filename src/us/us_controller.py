from . import UsModel

class UsController:
    def __init__(self, view):
        self.model = UsModel()
        self.view = view
        
        # Récupération des widgets
        widgets = view.get_widgets()
        self.model.set_widgets(**widgets)
        
        # Configuration des commandes
        self.setup_commands()
    
    def setup_commands(self):
        """Configure toutes les commandes des widgets."""
        self.view.set_toggle_command(self.toggle_simulation)
        self.view.set_reset_command(self.reset_simulation)
        self.view.set_speed_command(self.update_speed)
        self.view.set_continuous_command(self.toggle_continuous_mode)
        
    
    def set_gaussian_commands(self, mu_command, sigma_command, growth_mu_command, growth_sigma_command):
        """Configure les commandes des sliders gaussiens."""
        def update_mu(value):
            self.view.mu_label.config(text=f"μ : {float(value):.2f}")
            mu_command(value)
        
        def update_sigma(value):
            self.view.sigma_label.config(text=f"σ : {float(value):.2f}")
            sigma_command(value)
            
        def update_growth_mu(value):
            self.view.growth_mu_label.config(text=f"μ : {float(value):.2f}")
            growth_mu_command(value)
        
        def update_growth_sigma(value):
            # Arrondir la valeur au millième
            rounded_value = round(float(value), 3)
            self.view.growth_sigma_label.config(text=f"σ : {rounded_value:.3f}")
            growth_sigma_command(rounded_value)
        
        self.view.mu_slider.config(command=update_mu)
        self.view.sigma_slider.config(command=update_sigma)
        self.view.growth_mu_slider.config(command=update_growth_mu)
        self.view.growth_sigma_slider.config(command=update_growth_sigma)

    def toggle_simulation(self):
        """Gère le démarrage/arrêt de la simulation."""
        self.model.toggle_running_state()
    
    def reset_simulation(self):
        """Réinitialise la simulation."""
        self.model.reset_state()
    
    def get_speed(self):
        """Retourne la vitesse actuelle de simulation.
        
        Returns:
            float: Nombre de générations par seconde
        """
        return self.model.speed
    
    def update_speed(self, value):
        """Met à jour la vitesse de simulation.
        
        Args:
            value (float): Nouvelle vitesse en générations par seconde
        """
        self.model.speed = float(value)
    
    def is_running(self):
        """Retourne l'état actuel de la simulation.
        
        Returns:
            bool: True si la simulation est en cours
        """
        return self.model.is_running

    def toggle_continuous_mode(self):
        """Gère l'activation/désactivation du mode continu."""
        self.model.toggle_continuous_mode()
    
    def is_mode_continuous(self):
        """Retourne l'état actuel du mode continu.
        
        Returns:
            bool: True si le mode continu est activé
        """
        return self.model.is_mode_continuous()
