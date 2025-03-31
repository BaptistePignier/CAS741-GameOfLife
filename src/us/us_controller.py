from . import UsModel

class UsController:
    def __init__(self, view, sim_controller, fi_controller):
        self.model = UsModel()
        self.view = view
        self.sim_controller = sim_controller
        self.fi_controller = fi_controller
        
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
        self.set_gaussian_commands(
            lambda x: self.fi_controller.update_parameters(mu=x),
            lambda x: self.fi_controller.update_parameters(sigma=x),
            lambda x: self.fi_controller.update_parameters(growth_mu=x),
            lambda x: self.fi_controller.update_parameters(growth_sigma=x)
        )
    
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
            self.view.growth_sigma_label.config(text=f"σ : {float(value):.2f}")
            growth_sigma_command(value)
        
        self.view.mu_slider.config(command=update_mu)
        self.view.sigma_slider.config(command=update_sigma)
        self.view.growth_mu_slider.config(command=update_growth_mu)
        self.view.growth_sigma_slider.config(command=update_growth_sigma)

    def toggle_simulation(self):
        """Gère le démarrage/arrêt de la simulation."""
        is_running = self.sim_controller.toggle_simulation()
        self.model.update_toggle_button_text(is_running)
    
    def reset_simulation(self):
        """Réinitialise la simulation."""
        self.sim_controller.reset_simulation()
        self.model.update_toggle_button_text(False)
    
    def update_speed(self, value):
        """Met à jour la vitesse de simulation."""
        self.sim_controller.set_speed(value)
    
    def update_gaussian_mu(self, value):
        """Met à jour le paramètre mu de la gaussienne."""
        self.fi_controller.update_parameters(mu=float(value))
    
    def update_gaussian_sigma(self, value):
        """Met à jour le paramètre sigma de la gaussienne."""
        self.fi_controller.update_parameters(sigma=float(value))
    
    def stop(self):
        """Arrête la simulation."""
        self.sim_controller.stop()
