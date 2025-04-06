import pytest
from src.us.us_model import UsModel

class TestUsModel:
    @pytest.fixture
    def model(self):
        """Create an instance of the model for testing."""
        return UsModel()
    
    def test_numeric_value_initialization(self, model):
        """Test that the numeric value is correctly initialized."""
        assert model.numeric_value == 0
    
    def test_set_numeric_value_valid_input(self, model):
        """Test that the set_numeric_value method works with valid inputs."""
        # Test with an integer
        model.set_numeric_value(42)
        assert model.numeric_value == 42
        
        # Test with a negative integer
        model.set_numeric_value(-10)
        assert model.numeric_value == -10
        
        # Test with zero
        model.set_numeric_value(0)
        assert model.numeric_value == 0
    
    def test_set_numeric_value_invalid_input(self, model):
        """Test that the set_numeric_value method maintains the current value if the input is invalid."""
        # Set an initial value
        model.set_numeric_value(42)
        assert model.numeric_value == 42
        
        # Test with None (None value must be handled by the method)
        try:
            model.set_numeric_value(None)
            # If no exception is raised, the value should not change
            assert model.numeric_value == 42
        except TypeError:
            # If an exception is raised, we simply test that the value has not changed
            assert model.numeric_value == 42
        
        # Test with an empty string
        model.set_numeric_value("")
        assert model.numeric_value == 42  # The value should not change
        
        # Test with a decimal number (the current implementation converts it to an integer)
        model.set_numeric_value("3.14")
        assert model.numeric_value == 3  # Should be converted to 3, not keep 42

        # Test with non-numeric string
        model.set_numeric_value("a")
        assert model.numeric_value == 3  # Should not change from previous value
    
    def test_toggle_continuous_mode(self, model):
        """Test the toggle_continuous_mode function."""
        # Initial state is False
        assert model.is_continuous == False
        
        # First call: changes to True
        result = model.toggle_continuous_mode()
        assert model.is_continuous == True
        assert result == True
        
        # Second call: returns to False
        result = model.toggle_continuous_mode()
        assert model.is_continuous == False
        assert result == False
    
    def test_toggle_running_state(self, model):
        """Test the toggle_running_state function."""
        # Create a mock for the toggle button
        class MockButton:
            def __init__(self):
                self.text = "Start"
                
            def config(self, **kwargs):
                if "text" in kwargs:
                    self.text = kwargs["text"]
        
        # Configure the model with the mock
        mock_button = MockButton()
        model.toggle_button = mock_button
        
        # Initial state is False
        assert model.is_running == False
        
        # First call: changes to True
        result = model.toggle_running_state()
        assert model.is_running == True
        assert result == True
        assert mock_button.text == "Stop"
        
        # Second call: returns to False
        result = model.toggle_running_state()
        assert model.is_running == False
        assert result == False
        assert mock_button.text == "Start"
    
    def test_reset_state(self, model):
        """Test the reset_state function."""
        # Create a mock for the toggle button
        class MockButton:
            def __init__(self):
                self.text = "Stop"
                
            def config(self, **kwargs):
                if "text" in kwargs:
                    self.text = kwargs["text"]
        
        # Configure the model with the mock
        mock_button = MockButton()
        model.toggle_button = mock_button
        
        # Change the state to simulate a running simulation
        model.is_running = True
        
        # Call reset_state
        model.reset_state()
        
        # Verify that the state has been reset
        assert model.is_running == False
        assert model.needs_reset == True
        assert mock_button.text == "Start"
    
    def test_acknowledge_reset(self, model):
        """Test the acknowledge_reset function."""
        # Initial state is False
        assert model.needs_reset == False
        assert model.acknowledge_reset() == False
        
        # Mark that reset is required
        model.needs_reset = True
        
        # Verify that acknowledge_reset returns True and resets needs_reset to False
        assert model.acknowledge_reset() == True
        assert model.needs_reset == False
        
        # A second call should return False
        assert model.acknowledge_reset() == False 