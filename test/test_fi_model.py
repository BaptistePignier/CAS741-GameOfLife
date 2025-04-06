import pytest
import numpy as np
from src.fi.fi_model import FiModel

class TestFiModel:
    @pytest.fixture
    def model(self):
        """Create an instance of FiModel for testing."""
        return FiModel(mu=0.5, sigma=0.15, growth_mu=0.15, growth_sigma=0.015)
    
    def test_gauss(self, model):
        """Test the Gaussian function _gauss."""
        # Test with mu=0, sigma=1 (standard Gaussian)
        x = 0.0
        mu = 0.0
        sigma = 1.0
        result = model._gauss(x, mu, sigma)
        expected = 1.0  # The maximum value of a Gaussian is 1.0 when x = mu
        assert np.isclose(result, expected)
        
        # Test with a value at x=mu+sigma
        x = mu + sigma
        result = model._gauss(x, mu, sigma)
        expected = np.exp(-0.5)  # e^(-0.5) ≈ 0.607
        assert np.isclose(result, expected)
        
        # Test with a numpy array
        x_array = np.array([-1.0, 0.0, 1.0])
        result = model._gauss(x_array, mu, sigma)
        expected = np.array([np.exp(-0.5), 1.0, np.exp(-0.5)])
        assert np.allclose(result, expected)
    
    def test_growth_lenia(self, model):
        """Test the growth_lenia function."""
        # Test with different input values
        
        # At u = growth_mu, the function should reach its peak at +1
        u = model.growth_mu
        result = model.growth_lenia(u)
        assert np.isclose(result, 1.0)
        
        # At u = 0, the function should be negative
        u = 0.0
        result = model.growth_lenia(u)
        assert result < 0
        
        # Test with a numpy array
        u_array = np.array([0.0, model.growth_mu, model.growth_mu * 2])
        result = model.growth_lenia(u_array)
        
        # Verify that the function is symmetric around growth_mu
        # The difference between these two points should be close to zero
        diff = abs(model.growth_lenia(model.growth_mu - 0.01) - model.growth_lenia(model.growth_mu + 0.01))
        assert diff < 1e-10
    
    def test_growth_GoL(self, model):
        """Test the growth_GoL function which implements Game of Life rules."""
        # Test for survival and birth rules
        
        # Test values for u (number of neighbors)
        test_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        results = [model.growth_GoL(u) for u in test_values]
        
        # Game of Life rules:
        # - A dead cell (0) with exactly 3 neighbors is born (+1)
        # - A living cell (1) with 2 or 3 neighbors survives (0)
        # - In all other cases, death or remains dead (-1)
        
        # Verify that the function returns -1 for 0 neighbors (death)
        assert np.isclose(results[0], -1)
        
        # Verify that the function returns a positive value for 3 neighbors (birth)
        # According to the current implementation, it's 1.0 not 0
        assert results[3] > 0
        
        # Verify that the function returns appropriate values for other cases
        # 1 neighbor: death (-1+0=-1)
        assert results[1] < 0
        
        # 2 neighbors: survival for a living cell
        assert results[2] >= 0
        
        # 4 or more neighbors: death
        for i in range(4, 9):
            assert results[i] <= 0
    
    def test_con_nhood_normalization(self, model):
        """Test that the connectivity kernel is properly normalized."""
        # The con_nhood kernel should have a sum of 1
        nhood = model.get_con_nhood()
        assert np.isclose(np.sum(nhood), 1.0)
    
    def test_set_nhood_params(self, model):
        """Test that the kernel parameters update works."""
        # Save the initial kernel
        initial_nhood = model.get_con_nhood().copy()
        
        # Modify the parameters
        new_mu = 0.7
        new_sigma = 0.1
        model.set_nhood_params(mu=new_mu, sigma=new_sigma)
        
        # Verify that the kernel has changed
        assert not np.array_equal(initial_nhood, model.get_con_nhood())
        
        # Verify that the attributes have been updated
        assert model.mu == new_mu
        assert model.sigma == new_sigma
    
    def test_set_growth_params(self, model):
        """Test that the growth parameters update works."""
        # Save the initial values
        initial_g_mu = model.growth_mu
        initial_g_sigma = model.growth_sigma
        
        # Modify the parameters
        new_g_mu = 0.2
        new_g_sigma = 0.02
        model.set_growth_params(g_mu=new_g_mu, g_sigma=new_g_sigma)
        
        # Verify that the attributes have been updated
        assert model.growth_mu == new_g_mu
        assert model.growth_sigma == new_g_sigma
        
        # Verify that the growth function uses the new parameters
        result = model.growth_lenia(new_g_mu)
        assert np.isclose(result, 1.0) 