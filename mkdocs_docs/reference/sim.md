# Simulation Module (sim)

The Simulation module manages the cellular automaton itself, including the grid, evolution rules, and update loop. It supports both the traditional Game of Life (discrete mode) and Lenia (continuous mode).

## Module Structure

### Classes

#### SimModel

The `SimModel` class is responsible for the grid and cellular automaton logic.

```python
class SimModel:
    def __init__(self, width: int = 500, height: int = 500, initial_alive_prob: float = 0.2) -> None:
        """Initialize the simulation model.
        
        Args:
            width (int): Grid width in cells
            height (int): Grid height in cells
            initial_alive_prob (float): Initial probability for a cell to be alive
        """
```

Main methods:

- `update(fct: Callable[[np.ndarray], np.ndarray], nhood: np.ndarray, dt: float) -> None`: Updates the grid state for one generation
- `get_grid() -> np.ndarray`: Returns the current grid
- `reset_discrete(prob: Optional[float] = None) -> None`: Resets the grid with a new random configuration
- `reset_continuous(num: int) -> None`: Resets the grid with a continuous pattern based on the numeric value
- `stain() -> None`: Creates a centered Gaussian stain pattern
- `orbium() -> None`: Creates an Orbium pattern (Lenia spaceship)

#### SimController

The `SimController` class coordinates the model and view, managing the animation loop.

```python
class SimController:
    def __init__(self, view: Any, root: Any, us_controller: Any, fi_controller: Any) -> None:
        """Initialize the simulation controller.
        
        Args:
            view: SimView instance
            root: Main Tkinter window
            us_controller: UsController instance
            fi_controller: FiController instance
        """
```

Main methods:

- `run() -> None`: Starts the simulation
- `update() -> None`: Updates the model and view if the simulation is running
- `stop() -> None`: Stops the update timer
- `reset() -> None`: Resets the simulation grid

#### SimView

The `SimView` class manages the visualization of the cellular automaton grid.

```python
class SimView:
    def __init__(self, master: Any, width: int, height: int) -> None:
        """Initialize the simulation view.
        
        Args:
            master: Parent Tkinter widget
            width (int): Grid width in cells
            height (int): Grid height in cells
        """
```

Main methods:

- `update_display(grid: np.ndarray) -> None`: Updates the grid display
- `get_canvas() -> Any`: Returns the canvas widget
- `__del__() -> None`: Cleans up matplotlib resources

## Simulation Flow

1. Initialization:
   - `SimController` initializes the model and view
   - The grid is configured based on the current mode (continuous or discrete)

2. Update loop:
   - `SimController.update()` is called periodically
   - If the simulation is running, the model is updated
   - The view is refreshed with the new grid state

3. Reset:
   - When the user triggers a reset, `SimController.reset()` is called
   - A new grid is generated based on the current mode

## Cellular Automaton Algorithm

### Discrete Mode (Game of Life)

1. For each cell, count the number of live neighbors
2. Apply the Game of Life growth function:
   - A living cell survives if it has 2 or 3 living neighbors
   - A dead cell becomes alive if it has exactly 3 living neighbors

### Continuous Mode (Lenia)

1. Convolve the grid with the neighborhood kernel
2. Apply the Lenia growth function which depends on mu and sigma parameters
3. Update the grid with a small time step (dt) for a smooth transition

## Initialization Patterns

### Discrete Mode

- Random initialization with a configurable probability for live cells

### Continuous Mode

Two predefined patterns:

1. **Stain**: A centered Gaussian stain that develops organically
2. **Orbium**: A Lenia "glider" that moves across the grid

## Usage Examples

### Updating the simulation grid

```python
# Get the growth function and neighborhood kernel
growth_function = fi_controller.get_growth_fct()
neighborhood = fi_controller.get_nhood()
step = fi_controller.get_step()

# Update the grid
sim_model.update(growth_function, neighborhood, step)
```

### Resetting the simulation

```python
# Reset in discrete mode
sim_model.reset_discrete(prob=0.2)  # 20% probability for live cells

# Reset in continuous mode with a specific pattern
sim_model.reset_continuous(num=1)  # Use the Orbium pattern
```

## Integration with Other Modules

The Simulation module interacts with:

- **Functional Input Module**: Gets the neighborhood and growth functions
- **User Settings Module**: Receives simulation control commands (start/stop/reset)
- **Window Manager Module**: Integrates into the global application user interface 