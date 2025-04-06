# Simulation Module (sim)

The Simulation module manages the cellular automaton grid and its evolution over time. It handles the application of rules to update the state of cells at each step.

## Module Structure

### Classes

#### SimModel

The `SimModel` class manages the grid's state and handles all simulation calculations.

```python
class SimModel:
    def __init__(self, us_model, fi_model):
        """
        Initialize the simulation model.
        
        Args:
            us_model: Reference to the UsModel containing user settings
            fi_model: Reference to the FiModel for evolution rules
        """
```

Key methods:

- `initialize_grid(width, height)`: Creates and initializes the cell grid
- `set_cell(x, y, value)`: Sets the value of a specific cell
- `get_cell(x, y)`: Gets the value of a specific cell
- `randomize_grid(density)`: Randomizes the grid with a given density of live cells
- `clear_grid()`: Sets all cells to dead/zero
- `compute_fft()`: Computes the Fast Fourier Transform for continuous mode
- `update()`: Updates the entire grid based on the current mode and rules
- `reset()`: Resets the simulation to its initial state

#### SimController

The `SimController` class manages the simulation flow and timing.

```python
class SimController:
    def __init__(self, sim_model, us_model):
        """
        Initialize the simulation controller.
        
        Args:
            sim_model: Reference to the SimModel
            us_model: Reference to the UsModel containing user settings
        """
```

Key methods:

- `start()`: Starts the simulation
- `stop()`: Stops the simulation
- `step()`: Advances the simulation by one step
- `reset()`: Resets the simulation to its initial state
- `update()`: Updates the simulation based on current time and speed settings

## Simulation Modes

The module supports two simulation modes:

### Discrete Mode (Conway's Game of Life)

In discrete mode:
- Each cell has a binary state (0 = dead, 1 = alive)
- The update rule is based on counting live neighbors
- For a cell at position (i,j):
  - If alive and has fewer than `survival_min` live neighbors, it dies
  - If alive and has more than `survival_max` live neighbors, it dies
  - If dead and has between `birth_min` and `birth_max` live neighbors, it becomes alive

### Continuous Mode (Lenia)

In continuous mode:
- Each cell has a value between 0 and 1
- Updates are calculated using convolution operations with:
  - A neighborhood kernel defining how cells interact
  - A growth function determining how neighborhoods affect cell states
- The Fast Fourier Transform (FFT) is used to efficiently compute convolutions

## Grid Management

The grid is implemented as a 2D NumPy array, providing efficient operations for both types of cellular automata:

```python
# Create a grid of 100x100 cells
sim_model.initialize_grid(100, 100)

# Randomize with 30% live cells
sim_model.randomize_grid(0.3)

# Get the value of a specific cell
value = sim_model.get_cell(10, 20)

# Set a specific cell
sim_model.set_cell(15, 25, 1)
```

## Performance Considerations

For optimal performance, the simulation uses:

- NumPy arrays for grid representation and mathematical operations
- FFT-based convolution for continuous mode (much faster than direct convolution)
- Time-step management based on the current mode and user settings

## Integration with Other Modules

The Simulation module interacts primarily with:

- **Influence Functions Module**: Provides the rules and functions for determining cell evolution
- **User Interface Module**: Receives control commands and simulation parameters
- **Window Manager**: Coordinates the display of the simulation grid 