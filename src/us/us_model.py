class UsModel:
    def __init__(self):
        self.panel_width = 200
        self.toggle_button = None
        self.speed = 60.0  # Vitesse par défaut (générations par seconde)
        self.is_running = False  # État de la simulation
        self.needs_reset = False  # Flag pour la réinitialisation
    
    def set_widgets(self, toggle_button, **kwargs):
        """Stocke uniquement la référence au bouton toggle qui a besoin d'être mis à jour."""
        self.toggle_button = toggle_button
    
    def update_toggle_button_text(self, is_running):
        """Met à jour le texte du bouton toggle.
        
        Args:
            is_running (bool): True si la simulation est en cours
        """
        self.is_running = is_running
        self.toggle_button.config(text="Stop" if is_running else "Start")
    
    def toggle_running_state(self):
        """Inverse l'état de la simulation.
        
        Returns:
            bool: Nouvel état de la simulation
        """
        self.is_running = not self.is_running
        self.toggle_button.config(text="Stop" if self.is_running else "Start")
        return self.is_running
    
    def reset_state(self):
        """Réinitialise l'état de la simulation."""
        self.is_running = False
        self.needs_reset = True
        self.toggle_button.config(text="Start")
    
    def acknowledge_reset(self):
        """Acquitte la demande de réinitialisation.
        
        Returns:
            bool: True si une réinitialisation était demandée
        """
        was_reset = self.needs_reset
        self.needs_reset = False
        return was_reset
    
    def get_panel_width(self):
        """Retourne la largeur du panneau de contrôle."""
        return self.panel_width
