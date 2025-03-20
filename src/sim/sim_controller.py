class SimController:
    def __init__(self, model, view, root):
        self.model = model
        self.view = view
        self.root = root
        self.running = False
        self.generations_per_second = 60  # Générations par seconde par défaut
        self.min_delay = 20  # Délai minimum entre les mises à jour (ms)
        self.update_timer = None  # Timer pour les mises à jour
        
    def update(self):
        """Met à jour le modèle et la vue si la simulation est en cours."""
        if self.running:
            # Calcul du nombre de générations à calculer
            ideal_delay = 1000 / self.generations_per_second
            if ideal_delay >= self.min_delay:
                # Vitesse normale : une génération par mise à jour
                self.model.update()
            else:
                # Haute vitesse : plusieurs générations par mise à jour
                generations_per_update = int(self.min_delay / ideal_delay)
                for _ in range(generations_per_update):
                    self.model.update()
            
            # Mise à jour de l'affichage
            self.view.update_display(self.model.get_grid())
            
            # Planification de la prochaine mise à jour
            delay = max(int(ideal_delay), self.min_delay)
            self.update_timer = self.root.after(delay, self.update)
    
    def toggle_simulation(self):
        """Démarre ou arrête la simulation."""
        self.running = not self.running
        self.view.paused = not self.running
        if self.running:
            self.update()
        elif self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None
        return self.running
    
    def reset_simulation(self):
        """Réinitialise la simulation."""
        self.running = False
        self.view.paused = True
        self.model.reset()
        self.view.update_display(self.model.get_grid())
    
    def set_speed(self, generations_per_second):
        """Définit la vitesse de simulation en générations par seconde."""
        self.generations_per_second = int(float(generations_per_second))
    
    def is_running(self):
        """Retourne l'état actuel de la simulation."""
        return self.running
    
    def stop(self):
        """Arrête la simulation et l'animation."""
        self.running = False
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
            self.update_timer = None
        self.view.stop_animation()
