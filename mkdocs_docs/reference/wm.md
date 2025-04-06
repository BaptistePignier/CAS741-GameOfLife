# Window Manager Module (wm)

The Window Manager module is responsible for managing the application's main window, organizing the layout of interface elements, and coordinating the interactions between different visual components.

## Module Structure

### Main Class: WindowManager

The `WindowManager` class manages the main application window and organizes the layout of all UI components.

```python
class WindowManager:
    def __init__(self, root):
        """
        Initialize the window manager.
        
        Args:
            root: The root Tkinter window
        """
```

Key methods:

- `create_layout()`: Creates the main application layout
- `configure_window()`: Sets window properties like size, title, etc.
- `add_component(component, section)`: Adds a UI component to a specific section
- `get_section(section_name)`: Returns a reference to a specific layout section
- `resize_window(width, height)`: Resizes the application window
- `enter_fullscreen()`: Switches to fullscreen mode
- `exit_fullscreen()`: Exits fullscreen mode

## Layout Organization

The window manager organizes the application interface into several main sections:

### Control Section

Located on the left side of the window, this section contains:
- Simulation control buttons (Start/Stop, Reset, etc.)
- Parameter sliders and input fields
- Mode selection options

### Visualization Section

Located in the center, this section contains:
- The cellular automaton grid display
- Status information about the current state

### Graph Section

Located on the right side, this section contains:
- Neighborhood function visualization
- Growth function visualization
- Any additional graphs or visual aids

## Window Features

The window manager provides several features to enhance the user experience:

### Resizing and Fullscreen

The application window can be:
- Resized to fit user needs
- Switched to fullscreen mode for better visualization
- Adapted to different screen resolutions

### Layout Adaptation

The interface layout automatically adjusts to:
- Window size changes
- Component additions or removals
- Visibility changes of optional components

### Keyboard Shortcuts

Several keyboard shortcuts are implemented for common actions:
- F11: Toggle fullscreen mode
- Escape: Exit fullscreen mode
- Space: Start/Stop simulation
- R: Reset simulation

## Integration with Other Modules

The Window Manager interacts with:

- **User Interface Module**: Places UI controls in the appropriate sections
- **Simulation Module**: Allocates space for the grid display
- **Influence Functions Module**: Organizes function visualizations

## Usage Example

```python
import tkinter as tk
from wm import WindowManager
from us import UsView
from sim import SimView
from fi import FiView

# Create the root window
root = tk.Tk()

# Initialize the window manager
window_manager = WindowManager(root)

# Configure the window
window_manager.configure_window(
    title="Game of Life Simulator",
    width=1200,
    height=800
)

# Create the main layout
window_manager.create_layout()

# Create module views
us_view = UsView(window_manager.get_section("control"))
sim_view = SimView(window_manager.get_section("visualization"))
fi_view = FiView(window_manager.get_section("graph"))

# Start the application
root.mainloop()
``` 