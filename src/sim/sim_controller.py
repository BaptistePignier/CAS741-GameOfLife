from . import SimModel
import numpy as np

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
        
    def run(self):
        # Vérifie le mode (continu ou discret) pour l'initialisation
        if self.us_controller.is_mode_continuous():
            self.reset_continuous()
        else:
            self.reset_discrete()
        
        # Mise à jour initiale de l'affichage
        self.view.update_display(self.model.get_grid())
        
        # Démarrage du timer de mise à jour
        self.update()

    def update(self):
        """Met à jour le modèle et la vue si la simulation est en cours."""
        # Vérifie si une réinitialisation est demandée
        if self.us_controller.model.acknowledge_reset():
            # Vérifie le mode (continu ou discret) pour la réinitialisation
            if self.us_controller.is_mode_continuous():
                self.reset_continuous()
            else:
                self.reset_discrete()
            self.view.update_display(self.model.get_grid())
        
        # Met à jour la simulation si elle est en cours
        if self.us_controller.is_running():
            
            # Transmission des FI au sim_model
            self.model.set_kernel_ring(self.fi_controller.get_ring_kernel())
            self.model.set_growth_lenia(self.fi_controller.get_growth_lenia())

            # Calcule une génération selon le mode (continu ou discret)
            if self.us_controller.is_mode_continuous():
                self.model.update_continuous()
            else:
                self.model.update_discrete()
            
            # Met à jour l'affichage
            self.view.update_display(self.model.get_grid())
        
        # Planifie la prochaine mise à jour
        generations_per_second = self.us_controller.get_speed()
        delay = max(self.min_delay, int(1000 / generations_per_second))
        self.update_timer = self.root.after(delay, self.update)
    
    def stop(self):
        """Arrête le timer de mise à jour."""
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None

    def reset_discrete(self, prob=None):
        """Réinitialise la grille avec une nouvelle configuration aléatoire.
        
        Args:
            prob (float, optional): Nouvelle probabilité pour les cellules vivantes.
                                  Si None, utilise la probabilité initiale.
        """
        if prob is not None and 0 <= prob <= 1:
            self.model.initial_alive_prob = prob
            
        # Génération optimisée de la grille aléatoire
        self.model.grid = np.random.choice(
            [0, 1],
            self.model.width * self.model.height,
            p=[1-self.model.initial_alive_prob, self.model.initial_alive_prob]
        ).reshape(self.model.height, self.model.width).astype(np.int8)

    def reset_continuous(self):
        N = 256
        M = int(np.ceil((16*N)/9))
        self.model.grid = np.ones((M, N))
        # Gaussian spot centered in the middle
        radius = 36
        y, x = np.ogrid[-N//2:N//2, -M//2:M//2]
        self.model.grid = np.exp(-0.5 * (x*x + y*y) / (radius*radius))