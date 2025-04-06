# Tests pour CAS741-GameOfLife

Ce dossier contient les tests unitaires pour le projet Game of Life. Ces tests utilisent le framework pytest.

## Structure des tests

Les tests sont organisés comme suit :

- `test_fi_model.py` : Tests pour les fonctions du modèle FiModel, notamment les fonctions mathématiques utilisées pour les calculs de voisinage et de croissance.
- `test_us_model.py` : Tests pour les fonctions du modèle UsModel, notamment la gestion de l'état de simulation et la valeur numérique.
- `test_math_functions.py` : Tests plus approfondis des propriétés mathématiques des fonctions utilisées dans le projet.

## Exécution des tests

Pour exécuter tous les tests, depuis la racine du projet :

```bash
python -m pytest src/test
```

Pour exécuter un fichier de test spécifique :

```bash
python -m pytest src/test/test_fi_model.py
```

Pour exécuter un test spécifique :

```bash
python -m pytest src/test/test_fi_model.py::TestFiModel::test_growth_lenia
```

## Couverture des tests

Les tests couvrent principalement :

1. **Fonctions gaussiennes** : Test des propriétés mathématiques de la fonction gaussienne utilisée pour le calcul du voisinage.
2. **Fonctions de croissance** : 
   - `growth_lenia` : La fonction de croissance pour le mode continu
   - `growth_GoL` : La fonction de croissance pour le mode discret (Jeu de la Vie de Conway)
3. **Gestion du modèle UsModel** :
   - Tests de la fonction `toggle_continuous_mode`
   - Tests de la fonction `toggle_running_state`
   - Tests de gestion de la valeur numérique

## Ajout de nouveaux tests

Pour ajouter de nouveaux tests :

1. Créez un nouveau fichier de test avec le préfixe `test_` (par exemple, `test_nouveau_module.py`)
2. Implémentez vos tests en utilisant les conventions pytest
3. Exécutez les tests pour vous assurer qu'ils fonctionnent correctement 