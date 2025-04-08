# Tests for CAS741-GameOfLife

This folder contains unit tests for the Game of Life project. These tests use the pytest framework.

## Test Structure

The tests are organized as follows:

- `test_fi_model.py`: Tests for the FiModel model functions, particularly the mathematical functions used for neighborhood and growth calculations.
- `test_us_model.py`: Tests for the UsModel model functions, particularly simulation state management and numeric value handling.
- `test_math_functions.py`: More in-depth tests of the mathematical properties of the functions used in the project.

## Running the Tests

To run all tests, from the project root:

```bash
python -m pytest test
```

To run a specific test file:

```bash
python -m pytest test/test_fi_model.py
```

To run a specific test:

```bash
python -m pytest test/test_fi_model.py::TestFiModel::test_growth_lenia
```

## Test Coverage

The tests primarily cover:

1. **Gaussian functions**: Testing the mathematical properties of the Gaussian function used for neighborhood calculation.
2. **Growth functions**: 
   - `growth_lenia`: The growth function for continuous mode
   - `growth_GoL`: The growth function for discrete mode (Conway's Game of Life)
3. **UsModel management**:
   - Tests for the `toggle_continuous_mode` function
   - Tests for the `toggle_running_state` function
   - Tests for numeric value management

## Adding New Tests

To add new tests:

1. Create a new test file with the prefix `test_` (for example, `test_new_module.py`)
2. Implement your tests using pytest conventions
3. Run the tests to ensure they work correctly 