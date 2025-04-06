# Influence Functions Module (fi)

The Influence Functions module manages the rules that determine cell evolution in the cellular automaton. It includes two main components:

1. **Neighborhood Functions**: Define how cells interact with their neighbors
2. **Growth Functions**: Determine how a cell's state evolves based on its neighborhood

## Module Structure

### Classes

#### FiModel

The `FiModel` class manages all calculations related to neighborhoods and growth functions.

```python
class FiModel:
    def __init__(self, us_model):
        """
        Initialize the FiModel with a reference to the user settings model.
        
        Args:
            us_model: Reference to the UsModel containing user settings
        """
```

Key methods:

- `_gauss(x, mu, sigma)`: Gaussian function used for continuous neighborhoods
- `growth_lenia(U, mu, sigma, b)`: Lenia growth function for continuous mode
- `growth_GoL(U, b_low, b_high, s_low, s_high)`: Conway's Game of Life growth function
- `_update_con_nhood()`: Updates the continuous neighborhood kernel
- `get_con_nhood()`: Returns the current continuous neighborhood kernel
- `get_dis_nhood()`: Returns the current discrete neighborhood kernel
- `set_nhood_params(radius, mu, sigma)`: Sets parameters for the neighborhood function
- `set_growth_params(b_low, b_high, s_low, s_high, mu, sigma, b)`: Sets parameters for the growth function

#### FiController

The `FiController` class handles user interactions with growth and neighborhood functions.

```python
class FiController:
    def __init__(self, fi_model, fi_view, us_model):
        """
        Initialize the FiController.
        
        Args:
            fi_model: Reference to the FiModel
            fi_view: Reference to the FiView
            us_model: Reference to the UsModel
        """
```

Key methods:

- `update_nhood()`: Updates the neighborhood based on current parameters
- `update_growth()`: Updates the growth function based on current parameters

#### FiView

The `FiView` class displays visualizations of neighborhood and growth functions.

```python
class FiView:
    def __init__(self, parent, fi_model, us_model):
        """
        Initialize the FiView.
        
        Args:
            parent: Parent widget
            fi_model: Reference to the FiModel
            us_model: Reference to the UsModel
        """
```

Key methods:

- `create_widgets()`: Creates all visualization widgets
- `update_nhood_plot()`: Updates the visualization of the neighborhood function
- `update_growth_plot()`: Updates the visualization of the growth function

## Key Concepts

### Neighborhood Function

The neighborhood function defines how each cell interacts with surrounding cells. In our implementation:

- **Continuous Mode**: Uses a Gaussian function to create a smooth neighborhood kernel
- **Discrete Mode**: Uses a simple binary kernel (alive/dead)

### Growth Function

The growth function determines how a cell's state changes based on its neighborhood:

- **Lenia**: A continuous growth function where:
  - U is the current neighborhood value
  - mu and sigma determine the position and width of the response curve
  - b is a growth parameter
  
- **Game of Life**: A discrete growth function where:
  - A living cell survives if it has between s_low and s_high living neighbors
  - A dead cell becomes alive if it has between b_low and b_high living neighbors

## Usage Examples

### Setting up the Game of Life rule

```python
# Standard Conway's Game of Life
fi_model.set_growth_params(b_low=3, b_high=3, s_low=2, s_high=3)
```

### Setting up a continuous neighborhood

```python
# Gaussian neighborhood with radius 3
fi_model.set_nhood_params(radius=3, mu=0.5, sigma=0.15)
```

## Integration with Other Modules

The Influence Functions module interacts primarily with:

- **User Interface Module**: Receives parameter settings from user inputs
- **Simulation Module**: Provides growth and neighborhood functions for grid updates 