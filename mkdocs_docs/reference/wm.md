# Module Window Manager (wm)

Le module Window Manager gère la fenêtre principale de l'application, gérant la disposition, l'état de la fenêtre (plein écran, maximisé) et le placement des différentes vues. Il sert de conteneur pour tous les composants visuels de l'application.

## Structure du Module

### Classes

#### WindowManager

La classe `WindowManager` gère la fenêtre principale et organise les différentes vues.

```python
class WindowManager:
    def __init__(self, root: tk.Tk, sim_size: int, panel_width: int) -> None:
        """Initialize the window manager.
        
        Args:
            root: Main Tkinter window
            sim_size (int): Size of simulation area in pixels
            panel_width (int): Width of control panel in pixels
        """
```

Méthodes principales:

- `toggle_fullscreen() -> None`: Bascule le mode plein écran
- `exit_fullscreen() -> None`: Quitte le mode plein écran
- `maximize_window() -> None`: Maximise la fenêtre sans mode plein écran
- `setup_main_layout() -> None`: Configure la disposition principale de la fenêtre
- `setup_control_panel() -> None`: Configure le panneau de contrôle
- `place_views(sim_view: Any, us_view: Any, fi_view: Any) -> None`: Place toutes les vues dans l'interface
- `get_control_frame() -> ttk.Frame`: Renvoie le cadre de contrôle

## Disposition de la Fenêtre

La fenêtre est organisée en deux sections principales:

1. **Zone de Simulation**: Une zone extensible qui occupe la majorité de l'espace de la fenêtre, contenant la grille de l'automate cellulaire
2. **Panneau de Contrôle**: Un panneau de largeur fixe sur le côté droit, contenant tous les contrôles utilisateur

```
+----------------------------------+-------------+
|                                  |             |
|                                  |   Contrôle  |
|                                  |   de la     |
|        Zone de Simulation        |   Simulation|
|                                  |             |
|                                  |-------------|
|                                  |   Fonctions |
|                                  |   d'Influence|
|                                  |             |
+----------------------------------+-------------+
```

## Gestion de l'État de la Fenêtre

Le gestionnaire de fenêtre fournit trois modes d'affichage:

1. **Normal**: Taille de fenêtre par défaut
2. **Maximisé**: La fenêtre occupe tout l'espace disponible, mais conserve la barre de titre et les bordures
3. **Plein écran**: La fenêtre occupe tout l'écran, sans barre de titre ni bordures

Les raccourcis clavier suivants sont configurés:

- **F11**: Bascule le mode plein écran
- **Échap**: Quitte le mode plein écran

## Intégration des Vues

Le gestionnaire de fenêtre est responsable de l'intégration des différentes vues des autres modules:

1. **SimView**: Placée dans la zone de simulation principale
2. **UsView**: Placée dans la partie supérieure du panneau de contrôle
3. **FiView**: Placée dans la partie inférieure du panneau de contrôle

## Contraintes de Redimensionnement

Pour garantir une expérience utilisateur cohérente, le gestionnaire de fenêtre impose des contraintes de redimensionnement:

- **Taille minimale**: La fenêtre ne peut pas être redimensionnée en dessous d'une taille minimale (300px pour la simulation + largeur du panneau de contrôle × 400px de hauteur)
- **Panneau de contrôle**: Maintient une largeur fixe même lorsque la fenêtre est redimensionnée
- **Zone de simulation**: S'étend pour occuper l'espace supplémentaire lorsque la fenêtre est agrandie

## Exemples d'Utilisation

### Création de l'interface principale

```python
# Création de la fenêtre principale
root = tk.Tk()
window_manager = WindowManager(root, sim_size=500, panel_width=300)

# Initialisation des vues
sim_view = SimView(root, 500, 500)
us_view = UsView(window_manager.get_control_frame())
fi_view = FiView(window_manager.get_control_frame())

# Placement des vues
window_manager.place_views(sim_view, us_view, fi_view)

# Démarrage en fenêtre maximisée
window_manager.maximize_window()
```

### Gestion du mode plein écran

```python
# Bascule du mode plein écran
window_manager.toggle_fullscreen()

# Sortie du mode plein écran
window_manager.exit_fullscreen()
```

## Adaptation à Différentes Plateformes

Le module Window Manager est conçu pour s'adapter à différentes plateformes (Windows, Linux, macOS) en utilisant des méthodes spécifiques à la plateforme pour les opérations comme la maximisation de la fenêtre. Cela garantit une expérience utilisateur cohérente sur tous les systèmes d'exploitation. 