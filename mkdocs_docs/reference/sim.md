# Module Simulation (sim)

Le module Simulation gère l'automate cellulaire lui-même, y compris la grille, les règles d'évolution et la boucle de mise à jour. Il prend en charge à la fois le Jeu de la Vie traditionnel (mode discret) et Lenia (mode continu).

## Structure du Module

### Classes

#### SimModel

La classe `SimModel` est responsable de la grille et de la logique de l'automate cellulaire.

```python
class SimModel:
    def __init__(self, width: int = 500, height: int = 500, initial_alive_prob: float = 0.2) -> None:
        """Initialize the simulation model.
        
        Args:
            width (int): Grid width in cells
            height (int): Grid height in cells
            initial_alive_prob (float): Initial probability for a cell to be alive
        """
```

Méthodes principales:

- `update(fct: Callable[[np.ndarray], np.ndarray], nhood: np.ndarray, dt: float) -> None`: Met à jour l'état de la grille pour une génération
- `get_grid() -> np.ndarray`: Renvoie la grille actuelle
- `reset_discrete(prob: Optional[float] = None) -> None`: Réinitialise la grille avec une nouvelle configuration aléatoire
- `reset_continuous(num: int) -> None`: Réinitialise la grille avec un modèle continu basé sur la valeur numérique
- `stain() -> None`: Crée un motif de tache gaussienne centrée
- `orbium() -> None`: Crée un motif d'Orbium (vaisseau spatial Lenia)

#### SimController

La classe `SimController` coordonne le modèle et la vue, gérant la boucle d'animation.

```python
class SimController:
    def __init__(self, view: Any, root: Any, us_controller: Any, fi_controller: Any) -> None:
        """Initialize the simulation controller.
        
        Args:
            view: SimView instance
            root: Main Tkinter window
            us_controller: UsController instance
            fi_controller: FiController instance
        """
```

Méthodes principales:

- `run() -> None`: Démarre la simulation
- `update() -> None`: Met à jour le modèle et la vue si la simulation est en cours
- `stop() -> None`: Arrête le minuteur de mise à jour
- `reset() -> None`: Réinitialise la grille de simulation

#### SimView

La classe `SimView` gère la visualisation de la grille de l'automate cellulaire.

```python
class SimView:
    def __init__(self, master: Any, width: int, height: int) -> None:
        """Initialize the simulation view.
        
        Args:
            master: Parent Tkinter widget
            width (int): Grid width in cells
            height (int): Grid height in cells
        """
```

Méthodes principales:

- `update_display(grid: np.ndarray) -> None`: Met à jour l'affichage de la grille
- `get_canvas() -> Any`: Renvoie le widget de canevas
- `__del__() -> None`: Nettoie les ressources matplotlib

## Flux de Simulation

1. Initialisation:
   - `SimController` initialise le modèle et la vue
   - La grille est configurée en fonction du mode actuel (continu ou discret)

2. Boucle de mise à jour:
   - `SimController.update()` est appelé périodiquement
   - Si la simulation est en cours d'exécution, le modèle est mis à jour
   - La vue est rafraîchie avec le nouvel état de la grille

3. Réinitialisation:
   - Lorsque l'utilisateur déclenche une réinitialisation, `SimController.reset()` est appelé
   - Une nouvelle grille est générée en fonction du mode actuel

## Algorithme d'Automate Cellulaire

### Mode Discret (Jeu de la Vie)

1. Pour chaque cellule, compter le nombre de voisines vivantes
2. Appliquer la fonction de croissance du Game of Life:
   - Une cellule vivante survit si elle a 2 ou 3 voisines vivantes
   - Une cellule morte devient vivante si elle a exactement 3 voisines vivantes

### Mode Continu (Lenia)

1. Convoluer la grille avec le noyau de voisinage
2. Appliquer la fonction de croissance Lenia qui dépend des paramètres mu et sigma
3. Mettre à jour la grille avec un petit pas temporel (dt) pour une transition fluide

## Schémas d'Initialisation

### Mode Discret

- Initialisation aléatoire avec une probabilité configurable pour les cellules vivantes

### Mode Continu

Deux modèles prédéfinis:

1. **Stain**: Une tache gaussienne centrée qui se développe de manière organique
2. **Orbium**: Un "glisseur" Lenia qui se déplace à travers la grille

## Exemples d'Utilisation

### Mise à jour de la grille de simulation

```python
# Obtenir la fonction de croissance et le noyau de voisinage
growth_function = fi_controller.get_growth_fct()
neighborhood = fi_controller.get_nhood()
step = fi_controller.get_step()

# Mettre à jour la grille
sim_model.update(growth_function, neighborhood, step)
```

### Réinitialisation de la simulation

```python
# Réinitialisation en mode discret
sim_model.reset_discrete(prob=0.2)  # 20% de probabilité pour les cellules vivantes

# Réinitialisation en mode continu avec un motif spécifique
sim_model.reset_continuous(num=1)  # Utiliser le motif Orbium
```

## Intégration avec les Autres Modules

Le module Simulation interagit avec:

- **Module Function Influence**: Obtient les fonctions de voisinage et de croissance
- **Module User Simulation**: Reçoit les commandes de contrôle de la simulation (démarrer/arrêter/réinitialiser)
- **Module Window Manager**: S'intègre dans l'interface utilisateur globale de l'application 