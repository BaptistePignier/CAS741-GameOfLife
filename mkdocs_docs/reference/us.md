# Module User Simulation (us)

Le module User Simulation gère l'interface utilisateur pour le contrôle de la simulation. Il permet à l'utilisateur de:

1. Démarrer, arrêter et réinitialiser la simulation
2. Ajuster la vitesse de simulation
3. Basculer entre les modes continu (Lenia) et discret (Jeu de la Vie)
4. Configurer les paramètres des fonctions de voisinage et de croissance

## Structure du Module

### Classes

#### UsModel

La classe `UsModel` stocke l'état de la simulation et les paramètres utilisateur.

```python
class UsModel:
    def __init__(self) -> None:
        """Initialize the user simulation model.
        
        Sets up the default state for simulation control:
        - Default speed of 60 generations per second
        - Simulation initially stopped
        - No reset pending
        - Discrete mode (not continuous) by default
        - Initial numeric value of 0
        """
```

Méthodes principales:

- `set_widgets(toggle_button: Any, continuous_switch: Any) -> None`: Stocke les références aux widgets qui doivent être mis à jour
- `toggle_running_state() -> bool`: Bascule l'état de la simulation et renvoie le nouvel état
- `reset_state() -> None`: Réinitialise l'état de la simulation
- `acknowledge_reset() -> bool`: Confirme la demande de réinitialisation et renvoie l'état précédent
- `toggle_continuous_mode() -> bool`: Bascule le mode continu et renvoie le nouvel état
- `is_mode_continuous() -> bool`: Renvoie l'état du mode continu
- `set_numeric_value(value: Union[int, str, None]) -> None`: Définit la valeur numérique
- `get_numeric_value() -> int`: Renvoie la valeur numérique actuelle

#### UsController

La classe `UsController` coordonne les interactions entre le modèle et la vue.

```python
class UsController:
    def __init__(self, view: Any) -> None:
        """Initialize the user simulation controller.
        
        Sets up the model, connects to the view, and configures the event handlers
        for all user interface elements.
        
        Args:
            view: The UsView instance to control
        """
```

Méthodes principales:

- `update_numeric_value(value: str) -> None`: Met à jour la valeur numérique dans le modèle
- `set_interface_commands(mu_command: Callable[[float], None], sigma_command: Callable[[float], None], growth_mu_command: Callable[[float], None], growth_sigma_command: Callable[[float], None], continuous_button_command: Callable[[], None]) -> None`: Configure les commandes pour les éléments d'interface
- `get_speed() -> float`: Renvoie la vitesse de simulation actuelle
- `is_running() -> bool`: Renvoie l'état actuel de la simulation
- `is_mode_continuous() -> bool`: Renvoie l'état du mode continu
- `get_numeric_value() -> int`: Renvoie la valeur numérique actuelle

#### UsView

La classe `UsView` gère l'interface utilisateur pour les contrôles de simulation.

```python
class UsView:
    def __init__(self, control_frame: Any) -> None:
        """Initialize the user simulation view.
        
        Creates the UI frame and adds all control elements including:
        - Start/Stop toggle button
        - Reset button
        - Continuous mode checkbox
        - Numeric entry field
        - Speed control slider
        - Gaussian function parameter sliders
        - Growth function parameter sliders
        
        Args:
            control_frame: The parent tkinter container widget
        """
```

Méthodes principales:

- `_create_control_buttons() -> None`: Crée les boutons de contrôle
- `_create_speed_frame() -> None`: Crée le cadre de contrôle de la vitesse
- `_create_gaussian_frame() -> None`: Crée le cadre des paramètres gaussiens
- `get_frame() -> ttk.Frame`: Obtient le cadre principal de la vue
- `set_numeric_entry_command(command: Callable[[str], None]) -> None`: Configure la commande pour le champ de texte numérique

## Flux d'Interaction

1. L'utilisateur interagit avec les contrôles dans `UsView`
2. `UsController` reçoit ces interactions et met à jour `UsModel`
3. `UsController` notifie également les autres contrôleurs de l'application des changements pertinents

## Événements Principaux

### Contrôle de l'Exécution

- **Démarrer/Arrêter**: Démarre ou arrête le déroulement de la simulation
- **Réinitialiser**: Efface la grille actuelle et configure une nouvelle grille initiale
- **Vitesse**: Ajuste le nombre de générations par seconde

### Configuration du Mode

- **Mode Continu**: Bascule entre:
  - Mode discret (Jeu de la Vie traditionnel avec cellules vivantes/mortes)
  - Mode continu (Lenia avec valeurs d'état entre 0 et 1)

### Paramètres des Fonctions

- **Paramètres de Voisinage**:
  - μ (mu): Centre de l'anneau du noyau (de 0 à 1)
  - σ (sigma): Largeur de l'anneau du noyau (de 0.05 à 0.5)

- **Paramètres de Croissance**:
  - μ (mu): Centre de la fonction de croissance (de 0 à 0.30)
  - σ (sigma): Largeur de la fonction de croissance (de 0 à 0.1)

## Exemples d'Utilisation

### Démarrer et arrêter la simulation

```python
# Vérifier si la simulation est en cours d'exécution
is_running = us_controller.is_running()

# La simulation démarrera ou s'arrêtera lorsque l'utilisateur appuie sur le bouton toggle
# le contrôleur appelle alors:
us_model.toggle_running_state()
```

### Basculer entre les modes continu et discret

```python
# Vérifier le mode actuel
is_continuous = us_controller.is_mode_continuous()

# Basculer le mode lorsque l'utilisateur appuie sur le switch
# le contrôleur appelle alors:
us_model.toggle_continuous_mode()
```

### Obtenir la valeur numérique entrée par l'utilisateur

```python
# Obtenir la valeur numérique actuelle
num_value = us_controller.get_numeric_value()
```

## Intégration avec les Autres Modules

Le module User Simulation interagit avec:

- **Module Function Influence**: Fournit les paramètres utilisateur pour les fonctions de voisinage et de croissance
- **Module Simulation**: Contrôle l'exécution de la simulation et fournit les paramètres de vitesse et de mode