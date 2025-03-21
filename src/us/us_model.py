class UsModel:
    def __init__(self):
        self.panel_width = 200
        self.toggle_button = None
        self.reset_button = None
        self.speed_slider = None
        self.mu_slider = None
        self.sigma_slider = None
        
    def set_widgets(self, toggle_button, reset_button, speed_slider, mu_slider, sigma_slider, **kwargs):
        """Stocke les références aux widgets de contrôle. Ignore les labels qui ne sont pas nécessaires."""
        self.toggle_button = toggle_button
        self.reset_button = reset_button
        self.speed_slider = speed_slider
        self.mu_slider = mu_slider
        self.sigma_slider = sigma_slider
    
    def update_toggle_button_text(self, is_running):
        """Met à jour le texte du bouton toggle."""
        self.toggle_button.config(text="Stop" if is_running else "Start")
    
    def get_panel_width(self):
        """Retourne la largeur du panneau de contrôle."""
        return self.panel_width
