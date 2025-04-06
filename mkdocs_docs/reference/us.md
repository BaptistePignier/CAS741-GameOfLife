# User Interface Module (us)

The User Interface module manages all user controls and settings that affect the simulation. It handles user inputs and maintains the current state of simulation parameters.

## Module Structure

### Classes

#### UsModel

The `UsModel` class stores all user-configurable settings for the application.

```python
class UsModel:
    def __init__(self):
        """
        Initialize the user settings model with default values.
        """
```

Key attributes:

- `is_running`: Whether the simulation is currently running
- `is_continuous`: Whether the simulation is in continuous mode (Lenia) or discrete mode (Game of Life)
- `speed`: The simulation speed factor
- `numeric_value`: A generic numeric value for various settings
- `width`: Grid width in cells
- `height`: Grid height in cells
- Various parameters for both continuous and discrete modes

Key methods:

- `toggle_running()`: Switches between running and paused states
- `toggle_mode()`: Switches between continuous and discrete modes
- `set_speed(value)`: Sets the simulation speed
- `set_numeric_value(value)`: Sets a generic numeric value
- `reset()`: Resets all settings to default values

#### UsController

The `UsController` class handles user interactions with the interface controls.

```python
class UsController:
    def __init__(self, us_model, us_view):
        """
        Initialize the user interface controller.
        
        Args:
            us_model: Reference to the UsModel
            us_view: Reference to the UsView
        """
```

Key methods:

- `toggle_running()`: Handles start/stop button clicks
- `toggle_mode()`: Handles mode switch button clicks
- `update_speed(value)`: Handles speed slider changes
- `update_numeric(value)`: Handles generic numeric value changes
- `reset()`: Handles reset button clicks

#### UsView

The `UsView` class displays all user interface controls and updates them based on the current model state.

```python
class UsView:
    def __init__(self, parent):
        """
        Initialize the user interface view.
        
        Args:
            parent: Parent widget
        """
```

Key methods:

- `create_widgets()`: Creates all interface controls
- `update_running_display()`: Updates the start/stop button display
- `update_mode_display()`: Updates the mode switch button display
- `update_speed_display()`: Updates the speed slider display
- `update_display()`: Updates all interface elements based on the current model state

## User Controls

### Simulation Flow Controls

- **Start/Stop Button**: Toggle the simulation between running and paused states
- **Step Button**: Advance the simulation by one step (only active when paused)
- **Reset Button**: Reset the simulation to its initial state

### Mode Controls

- **Mode Switch**: Toggle between discrete (Game of Life) and continuous (Lenia) modes
- **Randomize Button**: Reset the grid with random cell states

### Parameter Controls

#### Common Parameters

- **Speed Slider**: Adjust the simulation speed
- **Grid Size Controls**: Set the width and height of the simulation grid

#### Discrete Mode Parameters

- **Birth Range**: Set the number of live neighbors required for a dead cell to become alive
- **Survival Range**: Set the number of live neighbors required for a live cell to remain alive

#### Continuous Mode Parameters

- **Neighborhood Parameters**: Control the Gaussian kernel parameters
- **Growth Parameters**: Control the growth function parameters

## Integration with Other Modules

The User Interface module interacts primarily with:

- **Simulation Module**: Sends commands to control the simulation flow
- **Influence Functions Module**: Provides parameter values that affect the evolution rules

## Usage Examples

### Controlling the simulation

```python
# Toggle the simulation state (start/stop)
us_controller.toggle_running()

# Reset the simulation
us_controller.reset()

# Change the simulation speed
us_controller.update_speed(2.0)
```

### Changing simulation parameters

```python
# Switch to continuous mode
us_model.is_continuous = True

# Set specific parameters
us_model.growth_mean = 0.15
us_model.growth_variance = 0.015

# Update the UI to reflect these changes
us_view.update_display()
```