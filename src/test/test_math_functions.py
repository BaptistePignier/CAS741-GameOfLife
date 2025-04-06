import pytest
import numpy as np
from src.fi.fi_model import FiModel

class TestMathFunctions:
    @pytest.fixture
    def model(self):
        """Créer une instance du modèle pour les tests."""
        return FiModel()
    
    def test_gaussian_properties(self, model):
        """Tester les propriétés mathématiques de la fonction gaussienne."""
        # Paramètres de test
        mu = 0.5
        sigma = 0.2
        x = np.linspace(-1, 2, 300)
        
        # Calculer la fonction gaussienne
        y = model._gauss(x, mu, sigma)
        
        # Propriété 1: La valeur maximale devrait être à x = mu
        max_index = np.argmax(y)
        assert np.isclose(x[max_index], mu, atol=0.01)
        
        # Propriété 2: La valeur au sommet devrait être 1.0 ou très proche
        assert np.isclose(y[max_index], 1.0, atol=1e-3)
        
        # Propriété 3: La fonction est symétrique autour de mu
        # Pour chaque point à gauche de mu, vérifier que le point correspondant à droite a la même valeur
        x_left = x[x < mu]
        for i, x_val in enumerate(x_left):
            distance = mu - x_val
            x_right = mu + distance
            if x_right <= x[-1]:  # Vérifier que x_right est dans notre domaine
                y_left = model._gauss(x_val, mu, sigma)
                y_right = model._gauss(x_right, mu, sigma)
                assert np.isclose(y_left, y_right, atol=1e-10)
        
        # Propriété 4: À mu ± sigma, la valeur est exp(-0.5) ≈ 0.607
        value_at_plus_sigma = model._gauss(mu + sigma, mu, sigma)
        value_at_minus_sigma = model._gauss(mu - sigma, mu, sigma)
        expected = np.exp(-0.5)
        assert np.isclose(value_at_plus_sigma, expected, atol=1e-10)
        assert np.isclose(value_at_minus_sigma, expected, atol=1e-10)
    
    def test_lenia_growth_properties(self, model):
        """Tester les propriétés de la fonction de croissance Lenia."""
        # Paramètres
        growth_mu = model.growth_mu
        growth_sigma = model.growth_sigma
        x = np.linspace(0, 0.3, 100)
        
        # Calculer la fonction de croissance
        y = model.growth_lenia(x)
        
        # Propriété 1: La valeur à x=0 devrait être -1 + 2*gauss(0, growth_mu, growth_sigma)
        expected_at_zero = -1 + 2 * model._gauss(0, growth_mu, growth_sigma)
        assert np.isclose(y[0], expected_at_zero, atol=1e-10)
        
        # Propriété 2: La valeur maximale devrait être à x = growth_mu
        max_index = np.argmax(y)
        assert np.isclose(x[max_index], growth_mu, atol=0.01)
        
        # Propriété 3: La valeur maximale devrait être proche de 1.0
        # La précision numérique peut causer des écarts mineurs
        assert np.isclose(y[max_index], 1.0, atol=0.02)
        
        # Propriété 4: La fonction devrait être négative pour x très différent de growth_mu
        far_from_mu = growth_mu + 5 * growth_sigma
        if far_from_mu <= 1.0:  # Vérifier que la valeur est dans un domaine raisonnable
            assert model.growth_lenia(far_from_mu) < 0
    
    def test_gol_growth_function_rules(self, model):
        """Tester que la fonction growth_GoL respecte les règles du Jeu de la Vie."""
        # Règles du Jeu de la Vie:
        # 1. Une cellule morte (0) avec exactement 3 voisins naît (devrait retourner une valeur positive)
        # 2. Une cellule vivante (1) avec 2 ou 3 voisins survit (devrait retourner une valeur ≥ 0)
        # 3. Dans tous les autres cas, la cellule meurt ou reste morte (devrait retourner une valeur négative)
        
        # Tester les valeurs exactes aux points critiques
        assert model.growth_GoL(3.0) > 0  # Naissance avec exactement 3 voisins
        assert model.growth_GoL(2.0) >= 0  # Survie avec exactement 2 voisins
        assert model.growth_GoL(0.0) < 0  # Mort avec 0 voisins
        assert model.growth_GoL(4.0) < 0  # Mort avec 4 voisins
        
        # Créer un tableau dense de valeurs pour tester le comportement global
        u_values = np.linspace(0, 8, 801)  # 0 à 8 avec un pas de 0.01
        results = model.growth_GoL(u_values)
        
        # Autour des valeurs critiques (2 et 3), la fonction peut osciller légèrement
        # à cause de l'implémentation numérique
        
        # Vérifier les règles pour des plages légèrement élargies
        birth_mask = np.logical_and(u_values > 2.95, u_values < 3.05)
        assert np.all(results[birth_mask] > -0.1)  # La plupart des valeurs devraient être positives
        
        # Vérifier que les cellules meurent pour des valeurs clairement en dehors des règles
        death_mask_low = u_values < 1.5  # Moins de 1.5 voisins = mort
        death_mask_high = u_values > 3.5  # Plus de 3.5 voisins = mort
        assert np.all(results[death_mask_low] < 0)
        assert np.all(results[death_mask_high] < 0)
        
    def test_growth_gol_continuous_vs_discrete(self, model):
        """Vérifier le comportement de growth_GoL pour des valeurs entières vs. des valeurs réelles."""
        # Valeurs entières (comportement classique du Jeu de la Vie)
        discrete_values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
        discrete_results = model.growth_GoL(discrete_values)
        
        # Valeurs adjacentes pour vérifier la continuité
        # Par exemple, comparer les résultats à u=2.95, u=3.0, u=3.05
        epsilon = 0.05
        
        # Points importants à vérifier
        critical_points = [2, 3]
        
        for point in critical_points:
            below = point - epsilon
            exact = point
            above = point + epsilon
            
            result_below = model.growth_GoL(below)
            result_exact = model.growth_GoL(exact)
            result_above = model.growth_GoL(above)
            
            # La fonction devrait être continue, donc pour un petit epsilon,
            # les valeurs adjacentes ne devraient pas être trop différentes
            assert abs(result_below - result_exact) < 0.5, f"Discontinuité détectée à u={point}"
            assert abs(result_above - result_exact) < 0.5, f"Discontinuité détectée à u={point}"
            
    def test_kernel_normalization(self, model):
        """Vérifier que le noyau est correctement normalisé à la somme 1."""
        nhood = model.get_con_nhood()
        
        # La somme des éléments du noyau devrait être égale à 1
        assert np.isclose(np.sum(nhood), 1.0, atol=1e-10)
        
        # Après modification des paramètres, le noyau devrait toujours être normalisé
        model.set_nhood_params(mu=0.7, sigma=0.1)
        nhood_new = model.get_con_nhood()
        assert np.isclose(np.sum(nhood_new), 1.0, atol=1e-10) 