import pytest
import numpy as np
from src.fi.fi_model import FiModel

class TestMathFunctions:
    @pytest.fixture
    def model(self):
        """Create an instance of the model for testing."""
        return FiModel()
    
    def test_gaussian_properties(self, model):
        """Test the mathematical properties of the Gaussian function."""
        # Test parameters
        mu = 0.5
        sigma = 0.2
        x = np.linspace(-1, 2, 300)
        
        # Calculate the Gaussian function
        y = model._gauss(x, mu, sigma)
        
        # Property 1: The maximum value should be at x = mu
        max_index = np.argmax(y)
        assert np.isclose(x[max_index], mu, atol=0.01)
        
        # Property 2: The value at the peak should be 1.0 or very close
        assert np.isclose(y[max_index], 1.0, atol=1e-3)
        
        # Property 3: The function is symmetric around mu
        # For each point to the left of mu, check that the corresponding point to the right has the same value
        x_left = x[x < mu]
        for i, x_val in enumerate(x_left):
            distance = mu - x_val
            x_right = mu + distance
            if x_right <= x[-1]:  # Check that x_right is in our domain
                y_left = model._gauss(x_val, mu, sigma)
                y_right = model._gauss(x_right, mu, sigma)
                assert np.isclose(y_left, y_right, atol=1e-10)
        
        # Property 4: At mu ± sigma, the value is exp(-0.5) ≈ 0.607
        value_at_plus_sigma = model._gauss(mu + sigma, mu, sigma)
        value_at_minus_sigma = model._gauss(mu - sigma, mu, sigma)
        expected = np.exp(-0.5)
        assert np.isclose(value_at_plus_sigma, expected, atol=1e-10)
        assert np.isclose(value_at_minus_sigma, expected, atol=1e-10)
    
    def test_lenia_growth_properties(self, model):
        """Test the properties of the Lenia growth function."""
        # Parameters
        growth_mu = model.growth_mu
        growth_sigma = model.growth_sigma
        x = np.linspace(0, 0.3, 100)
        
        # Calculate the growth function
        y = model.growth_lenia(x)
        
        # Property 1: The value at x=0 should be -1 + 2*gauss(0, growth_mu, growth_sigma)
        expected_at_zero = -1 + 2 * model._gauss(0, growth_mu, growth_sigma)
        assert np.isclose(y[0], expected_at_zero, atol=1e-10)
        
        # Property 2: The maximum value should be at x = growth_mu
        max_index = np.argmax(y)
        assert np.isclose(x[max_index], growth_mu, atol=0.01)
        
        # Property 3: The maximum value should be close to 1.0
        # Numerical precision can cause minor deviations
        assert np.isclose(y[max_index], 1.0, atol=0.02)
        
        # Property 4: The function should be negative for x very different from growth_mu
        far_from_mu = growth_mu + 5 * growth_sigma
        if far_from_mu <= 1.0:  # Check that the value is in a reasonable domain
            assert model.growth_lenia(far_from_mu) < 0
    
            
    def test_kernel_normalization(self, model):
        """Check that the kernel is properly normalized to a sum of 1."""
        nhood = model.get_con_nhood()
        
        # The sum of the kernel elements should be equal to 1
        assert np.isclose(np.sum(nhood), 1.0, atol=1e-10)
        
        # After modifying the parameters, the kernel should still be normalized
        model.set_nhood_params(mu=0.7, sigma=0.1)
        nhood_new = model.get_con_nhood()
        assert np.isclose(np.sum(nhood_new), 1.0, atol=1e-10) 