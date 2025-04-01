import tkinter as tk
from sim import SimView, SimController
from fi import FiView, FiController
from us import UsView, UsController
from wm import WindowManager

def main():
    """Point d'entrée principal de l'application."""
    # Configuration de la taille de la simulation
    grid_size = 100  # Taille de la grille en cellules
    panel_width = 200  # Largeur du panneau de contrôle en pixels
    
    # Création de la fenêtre principale
    root = tk.Tk()
    window_manager = WindowManager(root, grid_size, panel_width)
    
    # Initialisation du MVC de l'interface utilisateur
    us_view = UsView(window_manager.get_control_frame())
    us_controller = UsController(us_view)
    
    # Initialisation du MVC des fonctions d'influence
    fi_view = FiView(window_manager.get_control_frame())
    fi_controller = FiController(fi_view, us_controller)
    
    # Initialisation du MVC de la simulation
    sim_view = SimView(root, grid_size, grid_size)
    sim_controller = SimController(sim_view, root, us_controller, fi_controller)
    
    # Placement des vues dans l'interface
    window_manager.place_views(sim_view, us_view, fi_view)
    
    # Démarrage de la simulation
    sim_controller.run()
    
    # Configuration de la fermeture propre de l'application
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Lancement de la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()
