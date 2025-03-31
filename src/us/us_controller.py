from . import UsModel

class UsController:
    def __init__(self, view, game_controller, gaussian_controller):
        self.model = UsModel()
        self.view = view
        self.game_controller = game_controller
        self.gaussian_controller = gaussian_controller
        
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
        self.view.set_gaussian_commands(
            self.update_gaussian_mu,
            self.update_gaussian_sigma
        )
    
    def toggle_simulation(self):
        """Gère le démarrage/arrêt de la simulation."""
        is_running = self.game_controller.toggle_simulation()
        self.model.update_toggle_button_text(is_running)
    
    def reset_simulation(self):
        """Réinitialise la simulation."""
        self.game_controller.reset_simulation()
        self.model.update_toggle_button_text(False)
    
    def update_speed(self, value):
        """Met à jour la vitesse de simulation."""
        self.game_controller.set_speed(value)
    
    def update_gaussian_mu(self, value):
        """Met à jour le paramètre mu de la gaussienne."""
        self.gaussian_controller.update_parameters(mu=float(value))
    
    def update_gaussian_sigma(self, value):
        """Met à jour le paramètre sigma de la gaussienne."""
        self.gaussian_controller.update_parameters(sigma=float(value))
    
    def stop(self):
        """Arrête la simulation."""
        self.game_controller.stop()
