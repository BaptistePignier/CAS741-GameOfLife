# User Settings Module (us)

The User Settings module manages the user interface for simulation control. It allows the user to:

1. Start, stop, and reset the simulation
2. Adjust the simulation speed
3. Toggle between continuous (Lenia) and discrete (Game of Life) modes
4. Configure the neighborhood and growth function parameters

## Module Structure

### Classes

#### UsModel

The `UsModel` class stores the simulation state and user parameters.

```python
class UsModel:
    def __init__(self) -> None:
        """Initialize the user settings model.
        
        Sets up the default state for simulation control:
        - Default speed of 60 generations per second
        - Simulation initially stopped
        - No reset pending
        - Discrete mode (not continuous) by default
        - Initial numeric value of 0
        """
```

Main methods:

- `set_widgets(toggle_button: Any, continuous_switch: Any) -> None`: Stores references to widgets that need to be updated
- `toggle_running_state() -> bool`: Toggles the simulation state and returns the new state
- `reset_state() -> None`: Resets the simulation state
- `acknowledge_reset() -> bool`: Confirms the reset request and returns the previous state
- `toggle_continuous_mode() -> bool`: Toggles the continuous mode and returns the new state
- `is_mode_continuous() -> bool`: Returns the continuous mode state
- `set_numeric_value(value: Union[int, str, None]) -> None`: Sets the numeric value
- `get_numeric_value() -> int`: Returns the current numeric value

#### UsController

The `UsController` class coordinates interactions between the model and the view.

```python
class UsController:
    def __init__(self, view: Any) -> None:
        """Initialize the user settings controller.
        
        Sets up the model, connects to the view, and configures the event handlers
        for all user interface elements.
        
        Args:
            view: The UsView instance to control
        """
```

Main methods:

- `update_numeric_value(value: str) -> None`: Updates the numeric value in the model
- `set_interface_commands(mu_command: Callable[[float], None], sigma_command: Callable[[float], None], growth_mu_command: Callable[[float], None], growth_sigma_command: Callable[[float], None], continuous_button_command: Callable[[], None]) -> None`: Configures commands for interface elements
- `get_speed() -> float`: Returns the current simulation speed
- `is_running() -> bool`: Returns the current simulation state
- `is_mode_continuous() -> bool`: Returns the continuous mode state
- `get_numeric_value() -> int`: Returns the current numeric value

#### UsView

The `UsView` class manages the user interface for simulation controls.

```python
class UsView:
    def __init__(self, control_frame: Any) -> None:
        """Initialize the user settings view.
        
        Creates the UI frame and adds all control elements including:
        - Start/Stop toggle button
        - Reset button
        - Continuous mode checkbox
        - Numeric entry field
        - Speed control slider
        - Gaussian function parameter sliders
        - Growth function parameter sliders
        
        Args:
            control_frame: The parent tkinter container widget
        """
```

Main methods:

- `_create_control_buttons() -> None`: Creates control buttons
- `_create_speed_frame() -> None`: Creates the speed control frame
- `_create_gaussian_frame() -> None`: Creates the Gaussian parameters frame
- `get_frame() -> ttk.Frame`: Gets the main frame of the view
- `set_numeric_entry_command(command: Callable[[str], None]) -> None`: Configures the command for the numeric text field

## Interaction Flow

1. The user interacts with controls in `UsView`
2. `UsController` receives these interactions and updates `UsModel`
3. `UsController` also notifies other application controllers of relevant changes

## Main Events

### Execution Control

- **Start/Stop**: Starts or stops the simulation flow
- **Reset**: Clears the current grid and configures a new initial grid
- **Speed**: Adjusts the number of generations per second

### Mode Configuration

- **Continuous Mode**: Toggles between:
  - Discrete mode (traditional Game of Life with live/dead cells)
  - Continuous mode (Lenia with state values between 0 and 1)

### Function Parameters

- **Neighborhood Parameters**:
  - μ (mu): Center of the kernel ring (from 0 to 1)
  - σ (sigma): Width of the kernel ring (from 0.05 to 0.5)

- **Growth Parameters**:
  - μ (mu): Center of the growth function (from 0 to 0.30)
  - σ (sigma): Width of the growth function (from 0 to 0.1)

## Usage Examples

### Starting and stopping the simulation

```python
# Check if the simulation is running
is_running = us_controller.is_running()

# The simulation will start or stop when the user presses the toggle button
# the controller then calls:
us_model.toggle_running_state()
```

### Toggling between continuous and discrete modes

```python
# Check the current mode
is_continuous = us_controller.is_mode_continuous()

# Toggle the mode when the user presses the switch
# the controller then calls:
us_model.toggle_continuous_mode()
```

### Getting the numeric value entered by the user

```python
# Get the current numeric value
num_value = us_controller.get_numeric_value()
```

## Integration with Other Modules

The User Settings module interacts with:

- **Functional Input Module**: Provides user parameters for neighborhood and growth functions
- **Simulation Module**: Controls simulation execution and provides speed and mode parameters