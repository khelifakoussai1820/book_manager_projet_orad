# Maktabati

Application desktop `Tkinter` de gestion de bibliothèque avec deux rôles :

- `Admin` : gestion complète des livres, suivi des emprunts, retours, et liste noire des étudiants en retard.
- `Étudiant` : consultation des livres, enregistrement du profil étudiant, et emprunt de livres.

## Fonctionnalités

- ajout, modification et suppression de livres
- recherche et filtres sur le catalogue
- enregistrement des étudiants avec `id`, `prénom`, `nom`
- emprunt d'un livre par un étudiant avec durée configurable
- suivi des dates d'emprunt et de retour prévu
- retour d'un livre depuis l'espace admin
- liste noire automatique pour les étudiants en retard
- persistance locale en JSON

## Structure JSON

Les données sont stockées dans [data/books.json](/c:/Users/kouss/coding/book_manager_projet_orad/data/books.json) avec cette structure :

```json
{
    "books": [],
    "students": [],
    "borrowings": []
}
```

### `books`

```json
{
    "id": "1",
    "title": "Python 101",
    "author": "John Doe",
    "year": 2024,
    "isbn": "978-0000000000",
    "status": "available"
}
```

### `students`

```json
{
    "student_id": "E001",
    "first_name": "Aya",
    "last_name": "Benali",
    "borrowed_book_ids": ["1", "4"]
}
```

### `borrowings`

```json
{
    "id": "1",
    "student_id": "E001",
    "book_id": "4",
    "borrow_date": "2026-05-18",
    "due_date": "2026-06-01",
    "returned_date": "",
    "status": "borrowed"
}
```

## Lancer l'application

```bash
python main.py
```

## Tests

Les fichiers de tests sont présents :

- [test_delete.py](/c:/Users/kouss/coding/book_manager_projet_orad/test_delete.py)
- [test_edit.py](/c:/Users/kouss/coding/book_manager_projet_orad/test_edit.py)
- [test_borrow.py](/c:/Users/kouss/coding/book_manager_projet_orad/test_borrow.py)

Compilation vérifiée avec :

```bash
python -m py_compile main.py logic\storage.py logic\book.py logic\borrow.py logic\student.py logic\find.py ui\window.py ui\form.py ui\edit_form.py ui\search.py
```

`pytest` n'était pas installé dans l'environnement au moment de la vérification.
