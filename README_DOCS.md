# Documentation Game of Life

Ce projet utilise MkDocs pour générer sa documentation. Voici comment vous pouvez l'utiliser et la mettre à jour.

## Prérequis

Avant d'utiliser la documentation, vous devez installer les dépendances nécessaires :

```bash
pip install mkdocs mkdocs-material
```

## Visualiser la documentation

Pour visualiser la documentation localement, exécutez :

```bash
mkdocs serve
```

Puis ouvrez votre navigateur à l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Générer la documentation

Pour générer une version statique de la documentation, exécutez :

```bash
mkdocs build
```

La documentation sera générée dans le répertoire `site/`.

## Structure de la documentation

La documentation est organisée comme suit :

```
mkdocs_docs/
├── architecture/     # Documentation sur l'architecture du projet
├── img/              # Images utilisées dans la documentation
├── reference/        # Documentation de référence des modules
├── index.md          # Page d'accueil
└── user_guide.md     # Guide d'utilisation
```

## Mettre à jour la documentation

Pour mettre à jour la documentation, modifiez simplement les fichiers Markdown dans le répertoire `mkdocs_docs/`. La documentation sera automatiquement mise à jour si vous utilisez `mkdocs serve` pour la prévisualiser.

## Conventions de documentation

Veuillez suivre ces conventions lorsque vous mettez à jour la documentation :

1. Utilisez des titres clairs et descriptifs
2. Incluez des exemples de code lorsque c'est pertinent
3. Utilisez des listes et des tableaux pour organiser l'information
4. Ajoutez des illustrations si nécessaire pour clarifier les concepts

## Déployer la documentation

Pour déployer la documentation sur GitHub Pages, exécutez :

```bash
mkdocs gh-deploy
```

La documentation sera alors accessible à l'adresse suivante : https://votre-username.github.io/CAS741-GameOfLife/ 