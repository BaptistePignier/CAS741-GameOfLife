# Architecture Overview

The Game of Life project is structured according to a modular architecture that separates the different concerns of the application. This separation allows for better maintainability, testability, and extensibility of the code.

## Module Structure

The application is divided into four main modules:

### Influence Functions Module (fi)

This module manages the rules that determine the evolution of cells in the cellular automaton:

- **Neighborhood**: Defines how cells interact with their neighbors
- **Growth Functions**: Determines how a cell's state evolves based on its neighborhood

### Simulation Module (sim)

This module manages the state of the simulation grid and its evolution over time:

- **Grid**: Two-dimensional representation of cells
- **Update**: Application of evolution rules at each step of the simulation

### User Interface Module (us)

This module manages the controls and parameters that the user can adjust:

- **Simulation Controls**: Start, stop, reset
- **Parameters**: Speed, continuous/discrete mode, Gaussian parameters

### Window Manager Module (wm)

This module manages the organization of the graphical interface:

- **Layout**: Organization of the various visual elements
- **Window**: Management of size, fullscreen, etc.

## Data Flow

The following diagram illustrates how data flows between the different modules:

```
+-----------+     +----------+     +------------+
|    us     |     |    fi    |     |    sim     |
| (control) |---->|  (rules) |---->|(simulation)|
+-----------+     +----------+     +------------+
      |                                  |
      v                                  v
  +---------------------------------+  +-----+
  |       User Interface (Tkinter)  |  | View |
  +---------------------------------+  +-----+
```

1. The user interacts with the controls (`us`)
2. These interactions can modify the evolution rules (`fi`) 
3. The simulation (`sim`) uses these rules to update the grid
4. The view displays the current state of the simulation
5. The window manager (`wm`) coordinates the overall display

## Module Dependencies

The project uses a well-defined dependency structure:

- `main.py` coordinates the initialization of all modules
- `wm` does not depend on any other module
- `us` does not depend on any other module
- `fi` depends on `us` for information about the current mode
- `sim` depends on both `us` and `fi` for mode and evolution rules

This architecture allows modifying one module without necessarily affecting the others, facilitating maintenance and extension of the project. 