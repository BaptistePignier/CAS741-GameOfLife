import tkinter as tk
from sim import SimModel, SimView, SimController
from fi import FiModel, FiView, FiController
from us import UsModel, UsView, UsController
from wm import WindowManager

def main():
    # Configuration initiale
    
    sim_size = 1500
    panel_width = 200  # Largeur du panneau de contrôle
    
    # Création de la fenêtre principale et du gestionnaire de fenêtres
    root = tk.Tk()
    window_manager = WindowManager(root, sim_size, panel_width)
    
    # Initialisation du MVC de la simulation
    sim_view = SimView(root, sim_size, sim_size)
    sim_controller = SimController(sim_view, root)
    
    # Initialisation du MVC de l'interface utilisateur
    us_view = UsView(window_manager.get_control_frame())
    
    # Initialisation du MVC de la fonction gaussienne
    fi_model = FiModel()  # μ=0.5, σ=0.15 par défaut
    fi_view = FiView(window_manager.get_control_frame())
    fi_controller = FiController(fi_model, fi_view)
    
    # Configuration du contrôleur de l'interface utilisateur
    us_controller = UsController(us_view, sim_controller, fi_controller)
    
    # Ajout des commandes pour les sliders de la fonction de croissance
    us_view.set_gaussian_commands(
        lambda x: fi_controller.update_parameters(mu=x),
        lambda x: fi_controller.update_parameters(sigma=x),
        lambda x: fi_controller.update_parameters(growth_mu=x),
        lambda x: fi_controller.update_parameters(growth_sigma=x)
    )
    
    # Placement des vues dans l'interface
    window_manager.place_views(sim_view, us_view, fi_view)
    
    # Configuration de la fermeture propre de l'application
    def on_closing():
        us_controller.stop()  # Arrête la simulation
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Démarrage de la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main()
