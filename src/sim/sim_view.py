import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

class SimView:
    def __init__(self, master, sim_size, cell_size):
        self.sim_size = sim_size
        self.cell_size = cell_size
        self.current_grid = None
        self.master = master
        
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
        
        # Configuration de l'animation
        self._setup_animation()
        
        # Garde une référence forte à l'animation
        self._keep_ref = None
        
    def _setup_animation(self):
        """Configure l'animation matplotlib."""
        self._keep_ref = FuncAnimation(
            self.fig,
            self._update_frame,
            interval=20,  # 20ms = 50fps max
            blit=True,
            cache_frame_data=False
        )
    
    def _update_frame(self, frame):
        """Fonction d'update pour FuncAnimation."""
        if self.current_grid is not None:
            self.grid_display.set_array(self.current_grid)
        return [self.grid_display]
    
    def update_display(self, grid):
        """Met à jour l'affichage avec la nouvelle grille."""
        self.current_grid = grid
    
    def get_canvas(self):
        """Retourne le widget canvas."""
        return self.canvas.get_tk_widget()
    
    def stop_animation(self):
        """Arrête l'animation proprement."""
        if self._keep_ref is not None:
            self._keep_ref.event_source.stop()
            self._keep_ref = None
    
    def __del__(self):
        """Nettoyage des ressources."""
        self.stop_animation()
        plt.close(self.fig)
