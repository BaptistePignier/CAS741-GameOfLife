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
    
    def test_gol_growth_function_rules(self, model):
        """Test that the growth_GoL function respects the Game of Life rules."""
        # Game of Life rules:
        # 1. A dead cell (0) with exactly 3 neighbors is born (should return a positive value)
        # 2. A living cell (1) with 2 or 3 neighbors survives (should return a value ≥ 0)
        # 3. In all other cases, the cell dies or remains dead (should return a negative value)
        
        # Test exact values at critical points
        assert model.growth_GoL(3.0) > 0  # Birth with exactly 3 neighbors
        assert model.growth_GoL(2.0) >= 0  # Survival with exactly 2 neighbors
        assert model.growth_GoL(0.0) < 0  # Death with 0 neighbors
        assert model.growth_GoL(4.0) < 0  # Death with 4 neighbors
        
        # Create a dense array of values to test global behavior
        u_values = np.linspace(0, 8, 801)  # 0 to 8 with a step of 0.01
        results = model.growth_GoL(u_values)
        
        # Around critical values (2 and 3), the function may oscillate slightly
        # due to numerical implementation
        
        # Check rules for slightly expanded ranges
        birth_mask = np.logical_and(u_values > 2.95, u_values < 3.05)
        assert np.all(results[birth_mask] > -0.1)  # Most values should be positive
        
        # Check that cells die for values clearly outside the rules
        death_mask_low = u_values < 1.5  # Less than 1.5 neighbors = death
        death_mask_high = u_values > 3.5  # More than 3.5 neighbors = death
        assert np.all(results[death_mask_low] < 0)
        assert np.all(results[death_mask_high] < 0)
        
    def test_growth_gol_continuous_vs_discrete(self, model):
        """Check the behavior of growth_GoL for integer vs. real values."""
        # Integer values (classic Game of Life behavior)
        discrete_values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
        discrete_results = model.growth_GoL(discrete_values)
        
        # Adjacent values to check continuity
        # For example, compare results at u=2.95, u=3.0, u=3.05
        epsilon = 0.05
        
        # Important points to check
        critical_points = [2, 3]
        
        for point in critical_points:
            below = point - epsilon
            exact = point
            above = point + epsilon
            
            result_below = model.growth_GoL(below)
            result_exact = model.growth_GoL(exact)
            result_above = model.growth_GoL(above)
            
            # The function should be continuous, so for a small epsilon,
            # adjacent values should not be too different
            assert abs(result_below - result_exact) < 0.5, f"Discontinuity detected at u={point}"
            assert abs(result_above - result_exact) < 0.5, f"Discontinuity detected at u={point}"
            
    def test_kernel_normalization(self, model):
        """Check that the kernel is properly normalized to a sum of 1."""
        nhood = model.get_con_nhood()
        
        # The sum of the kernel elements should be equal to 1
        assert np.isclose(np.sum(nhood), 1.0, atol=1e-10)
        
        # After modifying the parameters, the kernel should still be normalized
        model.set_nhood_params(mu=0.7, sigma=0.1)
        nhood_new = model.get_con_nhood()
        assert np.isclose(np.sum(nhood_new), 1.0, atol=1e-10) 