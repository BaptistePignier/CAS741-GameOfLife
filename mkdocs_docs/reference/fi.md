# Functional Input Module (fi)

The Functional Input module manages the rules that determine cell evolution in the cellular automaton. It includes two main components:

1. **Neighborhood Functions**: Define how cells interact with their neighbors
2. **Growth Functions**: Determine how a cell's state evolves based on its neighborhood

## Module Structure

### Classes

#### FiModel

The `FiModel` class manages all calculations related to neighborhoods and growth functions.

```python
class FiModel:
    def __init__(self, mu: float = 0.5, sigma: float = 0.15, 
                 growth_mu: float = 0.15, growth_sigma: float = 0.015) -> None:
        """Initialize the function influence model.
        
        Args:
            mu (float): Center of the kernel ring. Default is 0.5.
            sigma (float): Width of the kernel ring. Default is 0.15.
            growth_mu (float): Center parameter for growth function. Default is 0.15.
            growth_sigma (float): Width parameter for growth function. Default is 0.015.
        """
```

Main methods:

- `_gauss(x: Union[float, np.ndarray], mu: float, sigma: float) -> Union[float, np.ndarray]`: Gaussian function used for continuous neighborhoods
- `growth_lenia(u: Union[float, np.ndarray]) -> Union[float, np.ndarray]`: Lenia growth function for continuous mode
- `growth_GoL(u: Union[float, np.ndarray]) -> Union[float, np.ndarray]`: Conway's Game of Life growth function
- `_update_con_nhood() -> None`: Updates the continuous neighborhood kernel
- `get_con_nhood() -> np.ndarray`: Returns the current continuous neighborhood kernel
- `get_dis_nhood() -> np.ndarray`: Returns the current discrete neighborhood kernel
- `set_nhood_params(mu: Optional[float] = None, sigma: Optional[float] = None) -> None`: Sets parameters for the neighborhood function
- `set_growth_params(g_mu: Optional[float] = None, g_sigma: Optional[float] = None) -> None`: Sets parameters for the growth function

#### FiController

The `FiController` class handles user interactions with growth and neighborhood functions.

```python
class FiController:
    def __init__(self, view: Any, us_controller: Any) -> None:
        """Initialize the function influence controller.
        
        Sets up the model, connects to the view, and registers with the user settings controller.
        
        Args:
            view: The FiView instance to control
            us_controller: The UsController instance to interact with
        """
```

Main methods:

- `get_nhood() -> np.ndarray`: Gets the appropriate neighborhood kernel based on current mode
- `get_growth_fct() -> Callable[[np.ndarray], np.ndarray]`: Gets the appropriate growth function based on current mode
- `get_step() -> float`: Gets the appropriate simulation step value based on current mode
- `update_nhood_params(mu: Optional[float] = None, sigma: Optional[float] = None) -> None`: Updates neighborhood parameters in the model and refreshes display
- `update_growth_params(g_mu: Optional[float] = None, g_sigma: Optional[float] = None) -> None`: Updates growth function parameters in the model and refreshes display
- `update_nhood_display() -> None`: Updates the neighborhood visualization in the view
- `update_growth_display() -> None`: Updates the growth function visualization in the view
- `update_displays() -> None`: Updates all display elements in the view

#### FiView

The `FiView` class displays visualizations of neighborhood and growth functions.

```python
class FiView:
    def __init__(self, master: Any) -> None:
        """Initialize the function influence view.
        
        Creates a frame with two visualization plots:
        - The top plot displays the neighborhood kernel
        - The bottom plot displays the growth function
        
        Args:
            master: The parent tkinter container widget
        """
```

Main methods:

- `update_growth_plot(x_values: np.ndarray, y_values: np.ndarray) -> None`: Updates the growth function graph with new data
- `update_growth_axes(xmin: float, xmax: float, ymin: float, ymax: float, continuous: bool = True) -> None`: Updates the limits and tick marks of the growth function graph axes
- `update_nhood_plot(kernel: np.ndarray) -> None`: Updates the neighborhood visualization with a new kernel
- `get_frame() -> ttk.Frame`: Gets the main frame of the view
- `get_canvas() -> Tuple[None, Any, Any]`: Gets the canvas widgets for external access

## Key Concepts

### Neighborhood Function

The neighborhood function defines how each cell interacts with surrounding cells. In our implementation:

- **Continuous Mode**: Uses a Gaussian function to create a smooth neighborhood kernel
- **Discrete Mode**: Uses a simple binary kernel (alive/dead)

### Growth Function

The growth function determines how a cell's state changes based on its neighborhood:

- **Lenia**: A continuous growth function where:
  - u is the current neighborhood value
  - growth_mu and growth_sigma determine the position and width of the response curve
  
- **Game of Life**: A discrete growth function where:
  - A living cell survives if it has between 2 and 3 living neighbors
  - A dead cell becomes alive if it has exactly 3 living neighbors

## Usage Examples

### Setting up Lenia mode (continuous)

```python
# Get the growth function and neighborhood kernel for Lenia
growth_function = fi_controller.get_growth_fct()  # Returns the growth_lenia function
nhood = fi_controller.get_nhood()  # Returns the continuous kernel
step = fi_controller.get_step()  # Returns 0.1 for continuous mode
```

### Setting up Game of Life mode (discrete)

```python
# Get the growth function and neighborhood kernel for Game of Life
growth_function = fi_controller.get_growth_fct()  # Returns the growth_GoL function
nhood = fi_controller.get_nhood()  # Returns the discrete kernel
step = fi_controller.get_step()  # Returns 1 for discrete mode
```

## Integration with Other Modules

The Functional Input module interacts primarily with:

- **User Settings Module**: Receives configuration parameters from user inputs
- **Simulation Module**: Provides growth and neighborhood functions for grid updates 