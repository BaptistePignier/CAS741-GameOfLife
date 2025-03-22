class UsModel:
    def __init__(self):
        self.panel_width = 200
        self.toggle_button = None  # Seul widget nécessaire pour la gestion d'état
    
    def set_widgets(self, toggle_button, **kwargs):
        """Stocke uniquement la référence au bouton toggle qui a besoin d'être mis à jour."""
        self.toggle_button = toggle_button
    
    def update_toggle_button_text(self, is_running):
        """Met à jour le texte du bouton toggle."""
        self.toggle_button.config(text="Stop" if is_running else "Démarrer")
    
    def get_panel_width(self):
        """Retourne la largeur du panneau de contrôle."""
        return self.panel_width
