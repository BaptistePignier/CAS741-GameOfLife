import tkinter as tk
from sim import SimView, SimController
from fi import FiView, FiController
from us import UsView, UsController
from wm import WindowManager

def main():
    """Main entry point of the application."""
    # Configuration of the simulation size
    grid_size = 100  # Grid size in cells
    panel_width = 300  # Control panel width in pixels
    
    # Creation of the main window
    root = tk.Tk()
    window_manager = WindowManager(root, grid_size, panel_width)
    
    # Initialization of the user interface MVC
    us_view = UsView(window_manager.get_control_frame())
    us_controller = UsController(us_view)
    
    # Initialization of the influence functions MVC
    fi_view = FiView(window_manager.get_control_frame())
    fi_controller = FiController(fi_view, us_controller)
    
    # Initialization of the simulation MVC
    sim_view = SimView(root, grid_size, grid_size)
    sim_controller = SimController(sim_view, root, us_controller, fi_controller)
    
    # Placement of views in the interface
    window_manager.place_views(sim_view, us_view, fi_view)
    
    # Starting the simulation
    sim_controller.run()
    
    # Configuration for proper application closure
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Démarrer en fenêtre maximisée
    window_manager.maximize_window()
    
    # Launch of the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
