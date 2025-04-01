from . import SimModel

class SimController:
    def __init__(self, view, root, us_controller, fi_controller):
        """Initialise le contrôleur de simulation.
        
        Args:
            view: Instance de SimView
            root: Fenêtre principale Tkinter
            us_controller: Instance de UsController
            fi_controller: Instance de FiController
        """
        self.model = SimModel(view.width, view.height)
        self.view = view
        self.root = root
        self.us_controller = us_controller
        self.fi_controller = fi_controller
        self.min_delay = 16  # ~60 FPS maximum (1000/60 ≈ 16.67ms)
        self.update_timer = None
        self.batch_size = 1  # Nombre de générations par mise à jour
        
    def run(self):
        # Mise à jour initiale de l'affichage
        self.view.update_display(self.model.get_grid())
        
        # Démarrage du timer de mise à jour
        self.update()

    def _update_batch_size(self):
        """Met à jour le nombre de générations à calculer par frame."""
        generations_per_second = self.us_controller.get_speed()
        ideal_delay = 1000 / generations_per_second
        if ideal_delay >= self.min_delay:
            self.batch_size = 1
        else:
            # Calcule combien de générations on peut faire en min_delay ms
            self.batch_size = max(1, int(self.min_delay / ideal_delay))
    
    def update(self):
        """Met à jour le modèle et la vue si la simulation est en cours."""
        # Vérifie si une réinitialisation est demandée
        if self.us_controller.model.acknowledge_reset():
            self.model.reset()
            self.view.update_display(self.model.get_grid())
        
        # Met à jour la simulation si elle est en cours
        if self.us_controller.is_running():
            
            # Transmission des FI au sim_model
            self.model.set_kernel_ring(self.fi_controller.get_ring_kernel())
            
            # Calcule plusieurs générations si nécessaire
            for _ in range(self.batch_size):
                self.model.update_discrete()
            
            # Met à jour l'affichage une seule fois
            self.view.update_display(self.model.get_grid())
            
            # Met à jour le batch size pour la prochaine itération
            self._update_batch_size()
        
        # Planifie la prochaine mise à jour
        generations_per_second = self.us_controller.get_speed()
        delay = max(self.min_delay, int(1000 / generations_per_second))
        self.update_timer = self.root.after(delay, self.update)
    
    def stop(self):
        """Arrête proprement la simulation."""
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None
