# Maktabati

Application desktop de gestion de bibliothèque personnelle développée en Python avec `Tkinter`.

Maktabati permet d'ajouter, modifier, rechercher et supprimer des livres à travers une interface graphique simple, claire et agréable, avec persistance des données dans un fichier JSON local.

## Aperçu

Ce projet a pour objectif de proposer un mini gestionnaire de livres facile à prendre en main, sans base de données ni dépendances lourdes. L'application convient bien pour :

- un projet pédagogique Python
- une démonstration d'interface graphique avec `Tkinter`
- un petit outil local de gestion de livres

## Fonctionnalités

- ajout d'un nouveau livre
- modification d'un livre existant
- suppression d'un livre avec confirmation
- affichage de la liste complète des livres
- recherche en direct par titre ou auteur
- filtrage par auteur
- filtrage par année
- gestion du statut d'un livre : `available`, `borrowed`, `not available`
- sauvegarde automatique dans `data/books.json`

## Interface

L'interface principale contient :

- un panneau d'actions pour ajouter un livre ou quitter l'application
- un compteur du nombre de livres visibles
- un tableau listant les ouvrages avec leurs informations principales
- une zone de recherche avec filtres
- des actions rapides `Modifier | Supprimer` directement dans la liste

## Structure Du Projet

```text
book_manager_projet_orad/
├── main.py
├── README.md
├── data/
│   └── books.json
├── logic/
│   ├── book.py
│   ├── find.py
│   └── storage.py
├── ui/
│   ├── window.py
│   ├── form.py
│   ├── edit_form.py
│   └── search.py
├── test_delete.py
└── test_edit.py
```

## Architecture

Le projet est organisé en deux grandes couches :

- `ui/` : interface graphique, fenêtres, formulaires, tableau et barre de recherche
- `logic/` : logique métier, recherche, lecture/écriture des données et opérations CRUD

### Rôle des fichiers principaux

- `main.py` : point d'entrée de l'application
- `ui/window.py` : fenêtre principale et orchestration de l'interface
- `ui/form.py` : formulaire d'ajout d'un livre
- `ui/edit_form.py` : formulaire de modification
- `ui/search.py` : recherche et filtres
- `logic/book.py` : ajout, mise à jour, suppression et recherche d'un livre
- `logic/find.py` : recherche textuelle et filtres par auteur/année
- `logic/storage.py` : chargement et sauvegarde du fichier JSON
- `data/books.json` : stockage local des livres

## Prérequis

- Python 3.11 ou plus récent recommandé
- système compatible avec `Tkinter`

Vérifier la version de Python :

```bash
python --version
```

## Lancement Rapide

1. Cloner le projet :

```bash
git clone <url-du-repo>
cd book_manager_projet_orad
```

2. Lancer l'application :

```bash
python main.py
```

L'application ouvrira une fenêtre desktop nommée **Maktabati**.

## Données

Les données sont enregistrées dans le fichier suivant :

```text
data/books.json
```

Le format utilisé est un objet JSON contenant une clé `book` :

```json
{
  "book": [
    {
      "id": 1,
      "title": "Example Book",
      "author": "Author Name",
      "year": 2024,
      "isbn": "978-0000000000",
      "status": "available"
    }
  ]
}
```

## Tests

Le dépôt contient actuellement des tests unitaires ciblés sur :

- la suppression d'un livre
- la modification d'un livre

Fichiers concernés :

- `test_delete.py`
- `test_edit.py`

Pour les exécuter avec `pytest` :

```bash
pip install pytest
pytest -q
```

## Choix Techniques

- `Tkinter` pour une interface graphique native et légère
- `JSON` pour une persistance simple sans base de données
- séparation `ui` / `logic` pour garder un code plus lisible et plus facile à faire évoluer

## Cas D'Usage

Maktabati peut servir de base pour :

- un projet étudiant en Python
- une introduction aux interfaces graphiques
- un mini logiciel de gestion locale
- une base à enrichir avec une base de données, des emprunts, ou une authentification

## Améliorations Possibles

- ajouter un fichier `requirements.txt`
- ajouter plus de tests unitaires
- normaliser totalement les textes de l'interface en UTF-8
- ajouter l'export CSV ou Excel
- permettre le tri des colonnes
- ajouter une fiche détaillée par livre
- remplacer le stockage JSON par SQLite

## Points Forts Du Projet

- interface simple et directe
- prise en main rapide
- code découpé en modules
- aucune dépendance lourde pour démarrer
- stockage local facile à comprendre

## Auteur

Projet Python de gestion de bibliothèque locale.

Vous pouvez personnaliser cette section avec :

- votre nom
- votre promotion ou établissement
- un lien GitHub

## Licence

Licence non précisée pour le moment.

Si vous souhaitez ouvrir le projet publiquement, vous pouvez ajouter une licence comme `MIT`.
