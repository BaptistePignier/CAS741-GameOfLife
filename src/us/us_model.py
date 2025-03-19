class UsModel:
    def __init__(self):
        self.panel_width = 200
        self.control_frame = None
        self.toggle_button = None
        self.reset_button = None
        self.speed_slider = None
        self.alpha_slider = None
        self.beta_slider = None
        
    def set_widgets(self, control_frame, toggle_button, reset_button, 
                   speed_slider, alpha_slider, beta_slider):
        """Stocke les références aux widgets."""
        self.control_frame = control_frame
        self.toggle_button = toggle_button
        self.reset_button = reset_button
        self.speed_slider = speed_slider
        self.alpha_slider = alpha_slider
        self.beta_slider = beta_slider
    
    def update_toggle_button_text(self, is_running):
        """Met à jour le texte du bouton toggle."""
        self.toggle_button.config(text="Stop" if is_running else "Start")
    
    def get_panel_width(self):
        """Retourne la largeur du panneau de contrôle."""
        return self.panel_width
