from . import SimModel

class SimController:
    def __init__(self, view, root):
        """Initialise le contrôleur de simulation.
        
        Args:
            view: Instance de SimView
            root: Fenêtre principale Tkinter
        """
        grid_size = 100  # Nombre de cellules par côté
        self.model = SimModel(grid_size, grid_size)
        self.view = view
        self.root = root
        self.running = False
        self.generations_per_second = 60  # FPS par défaut
        self.min_delay = 16  # ~60 FPS maximum (1000/60 ≈ 16.67ms)
        self.update_timer = None
        self.batch_size = 1  # Nombre de générations par mise à jour
        self._update_batch_size()
        
        # Mise à jour initiale de l'affichage
        self.view.update_display(self.model.get_grid())
    
    def _update_batch_size(self):
        """Met à jour le nombre de générations à calculer par frame."""
        ideal_delay = 1000 / self.generations_per_second
        if ideal_delay >= self.min_delay:
            self.batch_size = 1
        else:
            # Calcule combien de générations on peut faire en min_delay ms
            self.batch_size = max(1, int(self.min_delay / ideal_delay))
    
    def update(self):
        """Met à jour le modèle et la vue si la simulation est en cours."""
        if not self.running:
            return
            
        # Calcule plusieurs générations si nécessaire
        for _ in range(self.batch_size):
            self.model.update_discrete()
        
        # Met à jour l'affichage une seule fois
        self.view.update_display(self.model.get_grid())
        
        # Planifie la prochaine mise à jour
        delay = max(self.min_delay, int(1000 / self.generations_per_second))
        self.update_timer = self.root.after(delay, self.update)
    
    def toggle_simulation(self):
        """Démarre ou arrête la simulation.
        
        Returns:
            bool: True si la simulation est en cours, False sinon
        """
        self.running = not self.running
        if self.running:
            self.update()
        elif self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None
        return self.running
    
    def reset_simulation(self):
        """Réinitialise la simulation."""
        self.running = False
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None
        self.model.reset()
        self.view.update_display(self.model.get_grid())
    
    def set_speed(self, generations_per_second):
        """Définit la vitesse de simulation.
        
        Args:
            generations_per_second (float): Nombre de générations par seconde
        """
        self.generations_per_second = float(generations_per_second)
        self._update_batch_size()
    
    def stop(self):
        """Arrête proprement la simulation."""
        self.running = False
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None
