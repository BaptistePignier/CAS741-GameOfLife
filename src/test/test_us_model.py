import pytest
from src.us.us_model import UsModel

class TestUsModel:
    @pytest.fixture
    def model(self):
        """Créer une instance du modèle pour les tests."""
        return UsModel()
    
    def test_numeric_value_initialization(self, model):
        """Tester que la valeur numérique est correctement initialisée."""
        assert model.numeric_value == 0
    
    def test_set_numeric_value_valid_input(self, model):
        """Tester que la méthode set_numeric_value fonctionne avec des entrées valides."""
        # Test avec un entier
        model.set_numeric_value(42)
        assert model.numeric_value == 42
        
        # Test avec un entier négatif
        model.set_numeric_value(-10)
        assert model.numeric_value == -10
        
        # Test avec zéro
        model.set_numeric_value(0)
        assert model.numeric_value == 0
    
    def test_set_numeric_value_invalid_input(self, model):
        """Tester que la méthode set_numeric_value conserve la valeur actuelle si l'entrée est invalide."""
        # Définir une valeur initiale
        model.set_numeric_value(42)
        assert model.numeric_value == 42
        
        # Test avec None (la valeur None doit être gérée par la méthode)
        try:
            model.set_numeric_value(None)
            # Si aucune exception n'est levée, la valeur ne devrait pas changer
            assert model.numeric_value == 42
        except TypeError:
            # Si une exception est levée, nous testons simplement que la valeur n'a pas changé
            assert model.numeric_value == 42
        
        # Test avec une chaîne vide
        model.set_numeric_value("")
        assert model.numeric_value == 42  # La valeur ne doit pas changer
        
        # Test avec un nombre à virgule (devrait être tronqué à un entier)
        model.set_numeric_value("3.14")
        assert model.numeric_value == 42

        model.set_numeric_value("a")
        assert model.numeric_value == 42
    
    def test_toggle_continuous_mode(self, model):
        """Tester la fonction toggle_continuous_mode."""
        # L'état initial est False
        assert model.is_continuous == False
        
        # Premier appel: passe à True
        result = model.toggle_continuous_mode()
        assert model.is_continuous == True
        assert result == True
        
        # Deuxième appel: revient à False
        result = model.toggle_continuous_mode()
        assert model.is_continuous == False
        assert result == False
    
    def test_toggle_running_state(self, model):
        """Tester la fonction toggle_running_state."""
        # Créer un mock pour le bouton toggle
        class MockButton:
            def __init__(self):
                self.text = "Start"
                
            def config(self, **kwargs):
                if "text" in kwargs:
                    self.text = kwargs["text"]
        
        # Configurer le modèle avec le mock
        mock_button = MockButton()
        model.toggle_button = mock_button
        
        # L'état initial est False
        assert model.is_running == False
        
        # Premier appel: passe à True
        result = model.toggle_running_state()
        assert model.is_running == True
        assert result == True
        assert mock_button.text == "Stop"
        
        # Deuxième appel: revient à False
        result = model.toggle_running_state()
        assert model.is_running == False
        assert result == False
        assert mock_button.text == "Start"
    
    def test_reset_state(self, model):
        """Tester la fonction reset_state."""
        # Créer un mock pour le bouton toggle
        class MockButton:
            def __init__(self):
                self.text = "Stop"
                
            def config(self, **kwargs):
                if "text" in kwargs:
                    self.text = kwargs["text"]
        
        # Configurer le modèle avec le mock
        mock_button = MockButton()
        model.toggle_button = mock_button
        
        # Modifier l'état pour simuler une simulation en cours
        model.is_running = True
        
        # Appeler reset_state
        model.reset_state()
        
        # Vérifier que l'état a été réinitialisé
        assert model.is_running == False
        assert model.needs_reset == True
        assert mock_button.text == "Start"
    
    def test_acknowledge_reset(self, model):
        """Tester la fonction acknowledge_reset."""
        # L'état initial est False
        assert model.needs_reset == False
        assert model.acknowledge_reset() == False
        
        # Marquer que reset est nécessaire
        model.needs_reset = True
        
        # Vérifier que acknowledge_reset retourne True et réinitialise needs_reset à False
        assert model.acknowledge_reset() == True
        assert model.needs_reset == False
        
        # Un second appel devrait retourner False
        assert model.acknowledge_reset() == False 