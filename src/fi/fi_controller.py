class FiController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.update_display()
    
    def update_parameters(self, alpha=None, beta=None):
        """Met à jour les paramètres et rafraîchit l'affichage."""
        self.model.set_parameters(alpha=alpha, beta=beta)
        self.update_display()
    
    def update_display(self):
        """Met à jour l'affichage avec les valeurs actuelles."""
        x_values = self.model.get_x_values()
        y_values = self.model.calculate()
        self.view.update_plot(x_values, y_values, y_max=self.model.alpha)
