import pytest
import sys
import os

# Add the parent directory to PYTHONPATH to allow module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def app_path():
    """Returns the base path of the application."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(scope="session")
def test_data_path():
    """Returns the path to the test data."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

# Configure pytest to avoid Tkinter resource warnings
@pytest.fixture(autouse=True)
def suppress_tk_warnings():
    """Suppresses Tkinter-related warnings during tests."""
    import warnings
    warnings.filterwarnings("ignore", category=ResourceWarning) 