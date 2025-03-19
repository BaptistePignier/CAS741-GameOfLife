import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FiView:
    def __init__(self, master, figsize=(2, 2)):
        # Création de la figure matplotlib
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_title('α⋅exp(-βx²)')
        
        # Configuration initiale du graphe
        x_init = [-2, 2]
        y_init = [0, 1]
        self.line, = self.ax.plot(x_init, y_init)
        self.ax.set_ylim(-0.2, 1.2)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Création du canvas Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        if master is not None:
            self.canvas.get_tk_widget().grid(row=3, column=0, pady=10, padx=5, sticky='ew')
    
    def update_plot(self, x_values, y_values, y_max=None):
        """Met à jour le graphe avec les nouvelles valeurs."""
        self.line.set_xdata(x_values)
        self.line.set_ydata(y_values)
        if y_max is not None:
            self.ax.set_ylim(-0.2, y_max * 1.2)
        self.canvas.draw()
    
    def get_canvas(self):
        """Retourne le widget canvas."""
        return self.canvas.get_tk_widget()
