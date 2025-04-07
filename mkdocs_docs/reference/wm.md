# Window Manager Module (wm)

The Window Manager module manages the main application window, handling layout, window state (fullscreen, maximized), and the placement of different views. It serves as the container for all visual components of the application.

## Module Structure

### Classes

#### WindowManager

The `WindowManager` class manages the main window and organizes the different views.

```python
class WindowManager:
    def __init__(self, root: tk.Tk, sim_size: int, panel_width: int) -> None:
        """Initialize the window manager.
        
        Args:
            root: Main Tkinter window
            sim_size (int): Size of simulation area in pixels
            panel_width (int): Width of control panel in pixels
        """
```

Main methods:

- `toggle_fullscreen() -> None`: Toggles fullscreen mode
- `exit_fullscreen() -> None`: Exits fullscreen mode
- `maximize_window() -> None`: Maximizes the window without fullscreen mode
- `setup_main_layout() -> None`: Configures the main window layout
- `setup_control_panel() -> None`: Configures the control panel
- `place_views(sim_view: Any, us_view: Any, fi_view: Any) -> None`: Places all views in the interface
- `get_control_frame() -> ttk.Frame`: Returns the control frame

## Window Layout

The window is organized into two main sections:

1. **Simulation Area**: An expandable area that occupies the majority of the window space, containing the cellular automaton grid
2. **Control Panel**: A fixed-width panel on the right side, containing all user controls

```
+----------------------------------+-------------+
|                                  |             |
|                                  |   Simulation|
|                                  |   Control   |
|        Simulation Area           |             |
|                                  |             |
|                                  |-------------|
|                                  |   Influence |
|                                  |   Functions |
|                                  |             |
+----------------------------------+-------------+
```

## Window State Management

The window manager provides three display modes:

1. **Normal**: Default window size
2. **Maximized**: The window occupies all available space but retains the title bar and borders
3. **Fullscreen**: The window occupies the entire screen, without title bar or borders

The following keyboard shortcuts are configured:

- **F11**: Toggles fullscreen mode
- **Escape**: Exits fullscreen mode

## View Integration

The window manager is responsible for integrating the different views from other modules:

1. **SimView**: Placed in the main simulation area
2. **UsView**: Placed in the upper part of the control panel
3. **FiView**: Placed in the lower part of the control panel

## Resizing Constraints

To ensure a consistent user experience, the window manager imposes resizing constraints:

- **Minimum size**: The window cannot be resized below a minimum size (300px for simulation + control panel width × 400px height)
- **Control panel**: Maintains a fixed width even when the window is resized
- **Simulation area**: Expands to occupy additional space when the window is enlarged

## Usage Examples

### Creating the main interface

```python
# Create the main window
root = tk.Tk()
window_manager = WindowManager(root, sim_size=500, panel_width=300)

# Initialize views
sim_view = SimView(root, 500, 500)
us_view = UsView(window_manager.get_control_frame())
fi_view = FiView(window_manager.get_control_frame())

# Place views
window_manager.place_views(sim_view, us_view, fi_view)

# Start in maximized window
window_manager.maximize_window()
```

### Managing fullscreen mode

```python
# Toggle fullscreen mode
window_manager.toggle_fullscreen()

# Exit fullscreen mode
window_manager.exit_fullscreen()
```

## Adaptation to Different Platforms

The Window Manager module is designed to adapt to different platforms (Windows, Linux, macOS) by using platform-specific methods for operations such as window maximization. This ensures a consistent user experience across all operating systems. 