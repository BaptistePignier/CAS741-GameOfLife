# Influence Functions Module (fi)

Le module Influence Functions gère les règles qui déterminent l'évolution des cellules dans l'automate cellulaire. Il comprend deux composants principaux:

1. **Fonctions de voisinage**: Définissent comment les cellules interagissent avec leurs voisines
2. **Fonctions de croissance**: Déterminent comment l'état d'une cellule évolue en fonction de son voisinage

## Structure du Module

### Classes

#### FiModel

La classe `FiModel` gère tous les calculs liés aux voisinages et aux fonctions de croissance.

```python
class FiModel:
    def __init__(self, mu: float = 0.5, sigma: float = 0.15, 
                 growth_mu: float = 0.15, growth_sigma: float = 0.015) -> None:
        """Initialize the function influence model.
        
        Args:
            mu (float): Center of the kernel ring. Default is 0.5.
            sigma (float): Width of the kernel ring. Default is 0.15.
            growth_mu (float): Center parameter for growth function. Default is 0.15.
            growth_sigma (float): Width parameter for growth function. Default is 0.015.
        """
```

Méthodes principales:

- `_gauss(x: Union[float, np.ndarray], mu: float, sigma: float) -> Union[float, np.ndarray]`: Fonction gaussienne utilisée pour les voisinages continus
- `growth_lenia(u: Union[float, np.ndarray]) -> Union[float, np.ndarray]`: Fonction de croissance Lenia pour le mode continu
- `growth_GoL(u: Union[float, np.ndarray]) -> Union[float, np.ndarray]`: Fonction de croissance du Jeu de la Vie de Conway
- `_update_con_nhood() -> None`: Met à jour le noyau de voisinage continu
- `get_con_nhood() -> np.ndarray`: Renvoie le noyau de voisinage continu actuel
- `get_dis_nhood() -> np.ndarray`: Renvoie le noyau de voisinage discret actuel
- `set_nhood_params(mu: Optional[float] = None, sigma: Optional[float] = None) -> None`: Définit les paramètres pour la fonction de voisinage
- `set_growth_params(g_mu: Optional[float] = None, g_sigma: Optional[float] = None) -> None`: Définit les paramètres pour la fonction de croissance

#### FiController

La classe `FiController` gère les interactions de l'utilisateur avec les fonctions de croissance et de voisinage.

```python
class FiController:
    def __init__(self, view: Any, us_controller: Any) -> None:
        """Initialize the function influence controller.
        
        Sets up the model, connects to the view, and registers with the user simulation controller.
        
        Args:
            view: The FiView instance to control
            us_controller: The UsController instance to interact with
        """
```

Méthodes principales:

- `get_nhood() -> np.ndarray`: Obtient le noyau de voisinage approprié en fonction du mode actuel
- `get_growth_fct() -> Callable[[np.ndarray], np.ndarray]`: Obtient la fonction de croissance appropriée en fonction du mode actuel
- `get_step() -> float`: Obtient la valeur d'étape de simulation appropriée en fonction du mode actuel
- `update_nhood_params(mu: Optional[float] = None, sigma: Optional[float] = None) -> None`: Met à jour les paramètres de voisinage dans le modèle et rafraîchit l'affichage
- `update_growth_params(g_mu: Optional[float] = None, g_sigma: Optional[float] = None) -> None`: Met à jour les paramètres de la fonction de croissance dans le modèle et rafraîchit l'affichage
- `update_nhood_display() -> None`: Met à jour la visualisation du voisinage dans la vue
- `update_growth_display() -> None`: Met à jour la visualisation de la fonction de croissance dans la vue
- `update_displays() -> None`: Met à jour tous les éléments d'affichage dans la vue

#### FiView

La classe `FiView` affiche des visualisations des fonctions de voisinage et de croissance.

```python
class FiView:
    def __init__(self, master: Any) -> None:
        """Initialize the function influence view.
        
        Creates a frame with two visualization plots:
        - The top plot displays the neighborhood kernel
        - The bottom plot displays the growth function
        
        Args:
            master: The parent tkinter container widget
        """
```

Méthodes principales:

- `update_growth_plot(x_values: np.ndarray, y_values: np.ndarray) -> None`: Met à jour le graphique de la fonction de croissance avec de nouvelles données
- `update_growth_axes(xmin: float, xmax: float, ymin: float, ymax: float, continuous: bool = True) -> None`: Met à jour les limites et les graduations des axes du graphique de la fonction de croissance
- `update_nhood_plot(kernel: np.ndarray) -> None`: Met à jour la visualisation du voisinage avec un nouveau noyau
- `get_frame() -> ttk.Frame`: Obtient le cadre principal de la vue
- `get_canvas() -> Tuple[None, Any, Any]`: Obtient les widgets de canevas pour un accès externe

## Concepts Clés

### Fonction de Voisinage

La fonction de voisinage définit comment chaque cellule interagit avec les cellules environnantes. Dans notre implémentation:

- **Mode Continu**: Utilise une fonction gaussienne pour créer un noyau de voisinage lisse
- **Mode Discret**: Utilise un simple noyau binaire (vivant/mort)

### Fonction de Croissance

La fonction de croissance détermine comment l'état d'une cellule change en fonction de son voisinage:

- **Lenia**: Une fonction de croissance continue où:
  - u est la valeur actuelle du voisinage
  - growth_mu et growth_sigma déterminent la position et la largeur de la courbe de réponse
  
- **Jeu de la Vie**: Une fonction de croissance discrète où:
  - Une cellule vivante survit si elle a entre 2 et 3 voisines vivantes
  - Une cellule morte devient vivante si elle a exactement 3 voisines vivantes

## Exemples d'Utilisation

### Configuration du mode Lenia (continu)

```python
# Obtenir la fonction de croissance et le noyau de voisinage pour Lenia
growth_function = fi_controller.get_growth_fct()  # Renvoie la fonction growth_lenia
nhood = fi_controller.get_nhood()  # Renvoie le noyau continu
step = fi_controller.get_step()  # Renvoie 0.1 pour le mode continu
```

### Configuration du mode Game of Life (discret)

```python
# Obtenir la fonction de croissance et le noyau de voisinage pour Game of Life
growth_function = fi_controller.get_growth_fct()  # Renvoie la fonction growth_GoL
nhood = fi_controller.get_nhood()  # Renvoie le noyau discret
step = fi_controller.get_step()  # Renvoie 1 pour le mode discret
```

## Intégration avec les Autres Modules

Le module Influence Functions interagit principalement avec:

- **Module User Simulation**: Reçoit les paramètres de configuration des entrées utilisateur
- **Module Simulation**: Fournit les fonctions de croissance et de voisinage pour les mises à jour de la grille 