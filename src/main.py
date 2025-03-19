import tkinter as tk
from sim import SimModel, SimView, SimController
from fi import FiModel, FiView, FiController
from us import UsModel, UsView, UsController

def main():
    # Configuration initiale
    N = 500
    cell_size = 10
    sim_size = N * cell_size
    
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Jeu de la Vie Interactif")
    
    # Configuration de la grille
    panel_width = 200
    root.geometry(f"{sim_size + panel_width}x{sim_size}")
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=0, minsize=panel_width)
    root.rowconfigure(0, weight=1)
    
    # Initialisation du MVC du jeu de la vie
    sim_model = SimModel(size=N)
    sim_view = SimView(root, sim_size, cell_size)
    sim_controller = SimController(sim_model, sim_view, root)
    
    # Initialisation du MVC de l'interface utilisateur
    us_model = UsModel()
    us_view = UsView(root, panel_width, sim_size)
    
    # Initialisation du MVC de la fonction gaussienne
    fi_model = FiModel()
    fi_view = FiView(us_view.control_frame)  # Utilise le control_frame comme master
    fi_controller = FiController(fi_model, fi_view)
    
    # Configuration du contrôleur de l'interface utilisateur
    us_controller = UsController(us_model, us_view, sim_controller, fi_controller)
    
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
