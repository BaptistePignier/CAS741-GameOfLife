import tkinter as tk
from sim import SimModel, SimView, SimController
from fi import FiModel, FiView, FiController
from us import UsModel, UsView, UsController
from wm import WindowManager

def main():
    # Configuration initiale
    cell_size = 10
    grid_height = 500  # Nombre de cellules en hauteur
    grid_width = int(grid_height * 1.33)  # Ratio 4:3 pour la largeur
    
    # Calcul des dimensions de la fenêtre
    sim_height = grid_height * cell_size
    sim_width = grid_width * cell_size
    panel_width = 200
    
    # Création de la fenêtre principale et du gestionnaire de fenêtres
    root = tk.Tk()
    window_manager = WindowManager(root, sim_width, panel_width)
    
    # Initialisation du MVC du jeu de la vie
    sim_model = SimModel(width=grid_width, height=grid_height)
    sim_view = SimView(root, sim_width, sim_height, cell_size)
    sim_controller = SimController(sim_model, sim_view, root)
    
    # Initialisation du MVC de l'interface utilisateur
    us_model = UsModel()
    us_view = UsView(window_manager.get_control_frame())
    
    # Initialisation du MVC de la fonction gaussienne
    fi_model = FiModel()
    fi_view = FiView(window_manager.get_control_frame())
    fi_controller = FiController(fi_model, fi_view)
    
    # Configuration du contrôleur de l'interface utilisateur
    us_controller = UsController(us_model, us_view, sim_controller, fi_controller)
    
    # Placement de toutes les vues dans l'interface
    window_manager.place_views(sim_view, us_view, fi_view)
    
    # Configuration de la fermeture de la fenêtre
    def on_closing():
        us_controller.stop()
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Affichage initial
    sim_view.update_display(sim_model.get_grid())
    
    # Démarrage de la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()
