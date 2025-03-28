import tkinter as tk
from sim import SimModel, SimView, SimController
from fi import FiModel, FiView, FiController
from us import UsModel, UsView, UsController
from wm import WindowManager

def main():
    # Configuration initiale
    cell_size = 10  # Taille d'une cellule en pixels
    grid_size = 50  # Nombre de cellules par côté
    sim_size = grid_size * cell_size  # Taille de la zone de simulation
    panel_width = 200  # Largeur du panneau de contrôle
    
    # Création de la fenêtre principale et du gestionnaire de fenêtres
    root = tk.Tk()
    window_manager = WindowManager(root, sim_size, panel_width)
    
    # Initialisation du MVC de la simulation
    sim_model = SimModel(width=grid_size, height=grid_size)
    sim_view = SimView(root, sim_size, sim_size, cell_size)
    sim_controller = SimController(sim_model, sim_view, root)
    
    # Initialisation du MVC de l'interface utilisateur
    us_model = UsModel()
    us_view = UsView(window_manager.get_control_frame())
    
    # Initialisation du MVC de la fonction gaussienne
    fi_model = FiModel()  # μ=0.5, σ=0.15 par défaut
    fi_view = FiView(window_manager.get_control_frame())
    fi_controller = FiController(fi_model, fi_view)
    
    # Configuration du contrôleur de l'interface utilisateur
    us_controller = UsController(us_model, us_view, sim_controller, fi_controller)
    
    # Placement des vues dans l'interface
    window_manager.place_views(sim_view, us_view, fi_view)
    
    # Configuration de la fermeture propre de l'application
    def on_closing():
        us_controller.stop()  # Arrête la simulation
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Affichage initial
    sim_view.update_display(sim_model.get_grid())
    
    # Démarrage de la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()
