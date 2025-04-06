import pytest
import numpy as np
from src.fi.fi_model import FiModel

class TestFiModel:
    @pytest.fixture
    def model(self):
        """Créer une instance de FiModel pour les tests."""
        return FiModel(mu=0.5, sigma=0.15, growth_mu=0.15, growth_sigma=0.015)
    
    def test_gauss(self, model):
        """Tester la fonction gaussienne _gauss."""
        # Test avec mu=0, sigma=1 (gaussienne standard)
        x = 0.0
        mu = 0.0
        sigma = 1.0
        result = model._gauss(x, mu, sigma)
        expected = 1.0  # La valeur maximale d'une gaussienne est 1.0 lorsque x = mu
        assert np.isclose(result, expected)
        
        # Test avec une valeur à x=mu+sigma
        x = mu + sigma
        result = model._gauss(x, mu, sigma)
        expected = np.exp(-0.5)  # e^(-0.5) ≈ 0.607
        assert np.isclose(result, expected)
        
        # Test avec un tableau numpy
        x_array = np.array([-1.0, 0.0, 1.0])
        result = model._gauss(x_array, mu, sigma)
        expected = np.array([np.exp(-0.5), 1.0, np.exp(-0.5)])
        assert np.allclose(result, expected)
    
    def test_growth_lenia(self, model):
        """Tester la fonction growth_lenia."""
        # Test avec différentes valeurs d'entrée
        
        # À u = growth_mu, la fonction devrait atteindre son pic à +1
        u = model.growth_mu
        result = model.growth_lenia(u)
        assert np.isclose(result, 1.0)
        
        # À u = 0, la fonction devrait être négative
        u = 0.0
        result = model.growth_lenia(u)
        assert result < 0
        
        # Test avec un tableau numpy
        u_array = np.array([0.0, model.growth_mu, model.growth_mu * 2])
        result = model.growth_lenia(u_array)
        
        # Vérifier que la fonction est symétrique par rapport à growth_mu
        # La différence entre ces deux points devrait être proche de zéro
        diff = abs(model.growth_lenia(model.growth_mu - 0.01) - model.growth_lenia(model.growth_mu + 0.01))
        assert diff < 1e-10
    
    def test_growth_GoL(self, model):
        """Tester la fonction growth_GoL qui implémente les règles du Jeu de la Vie."""
        # Test pour les règles de survie et de naissance
        
        # Valeurs de test pour u (nombre de voisins)
        test_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        results = [model.growth_GoL(u) for u in test_values]
        
        # Règles du jeu de la vie:
        # - Une cellule morte (0) avec exactement 3 voisins naît (+1)
        # - Une cellule vivante (1) avec 2 ou 3 voisins survit (0)
        # - Dans tous les autres cas, mort ou reste morte (-1)
        
        # Vérifier que la fonction retourne -1 pour 0 voisins (mort)
        assert np.isclose(results[0], -1)
        
        # Vérifier que la fonction retourne une valeur positive pour 3 voisins (naissance)
        # D'après l'implémentation actuelle, c'est 1.0 et non 0
        assert results[3] > 0
        
        # Vérifier que la fonction retourne des valeurs appropriées pour les autres cas
        # 1 voisin: mort (-1+0=-1)
        assert results[1] < 0
        
        # 2 voisins: survie pour cellule vivante
        assert results[2] >= 0
        
        # 4 voisins ou plus: mort
        for i in range(4, 9):
            assert results[i] <= 0
    
    def test_con_nhood_normalization(self, model):
        """Tester que le noyau de connectivité est correctement normalisé."""
        # Le kernel con_nhood devrait avoir une somme de 1
        nhood = model.get_con_nhood()
        assert np.isclose(np.sum(nhood), 1.0)
    
    def test_set_nhood_params(self, model):
        """Tester que la mise à jour des paramètres du noyau fonctionne."""
        # Sauvegarder le noyau initial
        initial_nhood = model.get_con_nhood().copy()
        
        # Modifier les paramètres
        new_mu = 0.7
        new_sigma = 0.1
        model.set_nhood_params(mu=new_mu, sigma=new_sigma)
        
        # Vérifier que le noyau a changé
        assert not np.array_equal(initial_nhood, model.get_con_nhood())
        
        # Vérifier que les attributs ont été mis à jour
        assert model.mu == new_mu
        assert model.sigma == new_sigma
    
    def test_set_growth_params(self, model):
        """Tester que la mise à jour des paramètres de croissance fonctionne."""
        # Sauvegarder les valeurs initiales
        initial_g_mu = model.growth_mu
        initial_g_sigma = model.growth_sigma
        
        # Modifier les paramètres
        new_g_mu = 0.2
        new_g_sigma = 0.02
        model.set_growth_params(g_mu=new_g_mu, g_sigma=new_g_sigma)
        
        # Vérifier que les attributs ont été mis à jour
        assert model.growth_mu == new_g_mu
        assert model.growth_sigma == new_g_sigma
        
        # Vérifier que la fonction de croissance utilise les nouveaux paramètres
        result = model.growth_lenia(new_g_mu)
        assert np.isclose(result, 1.0) 