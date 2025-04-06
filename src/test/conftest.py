import pytest
import sys
import os

# Ajouter le dossier parent au PYTHONPATH pour permettre l'importation des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def app_path():
    """Retourne le chemin de base de l'application."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(scope="session")
def test_data_path():
    """Retourne le chemin des données de test."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

# Configure pytest pour éviter les avertissements de ressources Tkinter
@pytest.fixture(autouse=True)
def suppress_tk_warnings():
    """Supprime les avertissements liés à Tkinter pendant les tests."""
    import warnings
    warnings.filterwarnings("ignore", category=ResourceWarning) 