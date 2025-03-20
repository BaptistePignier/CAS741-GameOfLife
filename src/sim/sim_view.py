import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

class SimView:
    def __init__(self, master, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.current_grid = None
        self.master = master
        
        # Création de la figure matplotlib sans dimensions fixes
        self.fig = plt.figure(constrained_layout=True)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal')  # Garde les cellules carrées
        self.cmap = plt.get_cmap('binary')
        
        # Configuration initiale de l'affichage
        self.grid_display = self.ax.imshow(
            [[0]], cmap=self.cmap, interpolation='nearest',
            vmin=0, vmax=1,
            extent=[0, width/cell_size, 0, height/cell_size]  # Utilise les dimensions en nombre de cellules
        )
        
        # Configuration des limites initiales pour le zoom
        self.ax.set_xlim(0, width/cell_size)
        self.ax.set_ylim(0, height/cell_size)
        self.ax.grid(True, color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_frame_on(False)
        
        # Création du canvas Tkinter avec les dimensions correctes
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().config(
            width=width,
            height=height,
            bd=0,
            highlightthickness=0
        )
        
        # Configuration des événements de zoom et pan
        self.zoom_scale = 1.5
        self.canvas.mpl_connect('scroll_event', self._on_scroll)
        self.canvas.mpl_connect('button_press_event', self._on_press)
        self.canvas.mpl_connect('button_release_event', self._on_release)
        self.canvas.mpl_connect('motion_notify_event', self._on_motion)
        self._pan_start = None
        
        # Configuration de l'animation
        self._setup_animation()
        
        # Garde une référence forte à l'animation
        self._keep_ref = None
        
    def _on_scroll(self, event):
        """Gestion du zoom avec la molette de la souris"""
        if event.inaxes != self.ax:
            return
            
        # Facteur de zoom basé sur la direction du scroll
        scale = self.zoom_scale if event.button == 'up' else 1/self.zoom_scale
        
        # Position actuelle du curseur
        x_data, y_data = event.xdata, event.ydata
        
        # Limites actuelles
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        
        # Calcul des nouvelles limites
        x_range = (x_max - x_min) / scale
        y_range = (y_max - y_min) / scale
        
        # Centre le zoom sur la position du curseur
        self.ax.set_xlim([x_data - x_range * (x_data - x_min)/(x_max - x_min),
                         x_data + x_range * (x_max - x_data)/(x_max - x_min)])
        self.ax.set_ylim([y_data - y_range * (y_data - y_min)/(y_max - y_min),
                         y_data + y_range * (y_max - y_data)/(y_max - y_min)])
        
        self.canvas.draw_idle()
    
    def _on_press(self, event):
        """Début du pan avec le clic de souris"""
        if event.inaxes != self.ax or event.button != 1:
            return
        self._pan_start = (event.xdata, event.ydata)
        self.canvas.get_tk_widget().config(cursor="fleur")
    
    def _on_release(self, event):
        """Fin du pan"""
        self._pan_start = None
        self.canvas.get_tk_widget().config(cursor="")
    
    def _on_motion(self, event):
        """Déplacement pendant le pan"""
        if self._pan_start is None or event.inaxes != self.ax:
            return
            
        dx = event.xdata - self._pan_start[0]
        dy = event.ydata - self._pan_start[1]
        
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        
        self.ax.set_xlim(x_min - dx, x_max - dx)
        self.ax.set_ylim(y_min - dy, y_max - dy)
        
        self.canvas.draw_idle()
        
    def _setup_animation(self):
        """Configure l'animation matplotlib."""
        self._keep_ref = FuncAnimation(
            self.fig,
            self._update_frame,
            interval=20,  # 20ms = 50fps max
            blit=True,
            cache_frame_data=False,
            save_count=None
        )
        self.paused = True
    
    def _update_frame(self, frame):
        """Fonction d'update pour FuncAnimation."""
        if self.current_grid is not None:
            self.grid_display.set_array(self.current_grid)
        return [self.grid_display]
    
    def update_display(self, grid):
        """Met à jour l'affichage avec la nouvelle grille."""
        self.current_grid = grid
        if hasattr(self, 'grid_display'):
            self.grid_display.set_array(grid)
            self.canvas.draw_idle()
    
    def get_canvas(self):
        """Retourne le widget canvas."""
        return self.canvas.get_tk_widget()
    
    def stop_animation(self):
        """Arrête l'animation proprement."""
        if self._keep_ref is not None:
            self._keep_ref.event_source.stop()
            self._keep_ref = None
    
    def update_dimensions(self, width, height):
        """Met à jour les dimensions de la vue."""
        self.width = width
        self.height = height
        
        # Met à jour les dimensions du widget Tkinter
        self.canvas.get_tk_widget().config(
            width=width,
            height=height
        )
        
        # Force le redimensionnement de la figure matplotlib
        self.fig.set_size_inches(width/100, height/100)
        self.canvas.draw()
    
    def __del__(self):
        """Nettoyage des ressources."""
        self.stop_animation()
        plt.close(self.fig)
