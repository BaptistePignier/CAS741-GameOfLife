import tkinter as tk
from sim import SimView, SimController
from fi import FiView, FiController
from us import UsView, UsController
from wm import WindowManager

def main():
    # Configuration initiale
    
    sim_size = 1500
    panel_width = 200  # Largeur du panneau de contrôle
    
    # Création de la fenêtre principale et du gestionnaire de fenêtres
    root = tk.Tk()
    window_manager = WindowManager(root, sim_size, panel_width)
    
    # Initialisation du MVC de l'interface utilisateur
    fi_view = FiView(window_manager.get_control_frame())
    fi_controller = FiController(fi_view)
    
    us_view = UsView(window_manager.get_control_frame())
    us_controller = UsController(us_view, fi_controller)  # Initialisation temporaire

    # Initialisation du MVC de la simulation
    sim_view = SimView(root, sim_size, sim_size)
    # Création du contrôleur de simulation avec le contrôleur utilisateur
    sim_controller = SimController(sim_view, root, us_controller)
    
    # Placement des vues dans l'interface
    window_manager.place_views(sim_view, us_view, fi_view)

    # Démarrage de la simulation
    sim_controller.run()

    # Configuration de la fermeture propre de l'application
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Démarrage de la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()
