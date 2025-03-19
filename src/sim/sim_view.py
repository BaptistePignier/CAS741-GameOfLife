import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimView:
    def __init__(self, master, sim_size, cell_size):
        self.sim_size = sim_size
        self.cell_size = cell_size
        
        # Création de la figure matplotlib
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.ax.set_position([0, 0, 1, 1])
        self.cmap = plt.get_cmap('binary')
        
        # Configuration initiale de l'affichage
        self.grid_display = self.ax.imshow(
            [[0]], cmap=self.cmap, interpolation='nearest',
            vmin=0, vmax=1,
            extent=[0, sim_size, 0, sim_size]
        )
        self.ax.axis('off')
        
        # Création du canvas Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().config(
            width=sim_size,
            height=sim_size,
            bd=0,
            highlightthickness=0
        )
    
    def update_display(self, grid):
        """Met à jour l'affichage avec la nouvelle grille."""
        self.grid_display.set_data(grid)
        self.canvas.draw()
    
    def get_canvas(self):
        """Retourne le widget canvas."""
        return self.canvas.get_tk_widget()
