class SimController:
    def __init__(self, model, view, root):
        self.model = model
        self.view = view
        self.root = root
        self.running = False
        self.speed = 10  # Délai en millisecondes
        
    def update(self):
        """Met à jour le modèle et la vue si la simulation est en cours."""
        if self.running:
            self.model.update()
            self.view.update_display(self.model.get_grid())
            self.root.after(self.speed, self.update)
    
    def toggle_simulation(self):
        """Démarre ou arrête la simulation."""
        self.running = not self.running
        if self.running:
            self.update()
        return self.running
    
    def reset_simulation(self):
        """Réinitialise la simulation."""
        self.running = False
        self.model.reset()
        self.view.update_display(self.model.get_grid())
    
    def set_speed(self, speed):
        """Définit la vitesse de simulation."""
        self.speed = int(float(speed))
    
    def is_running(self):
        """Retourne l'état actuel de la simulation."""
        return self.running
    
    def stop(self):
        """Arrête la simulation."""
        self.running = False
