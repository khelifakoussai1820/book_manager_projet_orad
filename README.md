# Maktabati

Application desktop `Tkinter` de gestion de bibliotheque avec deux roles :

- `Admin` : gestion des livres, suivi des emprunts, validation des retours et consultation de la liste noire.
- `Etudiant` : consultation du catalogue, creation de compte, consultation du profil et emprunt de livres.

## Fonctionnalites

- ajout, modification et suppression de livres
- recherche et filtres sur le catalogue
- creation de comptes etudiants
- generation automatique des identifiants
- emprunt de livres avec duree configurable
- suivi des dates d'emprunt, de retour prevu et de retour effectif
- liste noire automatique pour les etudiants en retard
- persistance locale des donnees en JSON

## Architecture du projet

```text
book_manager_projet_orad/
|- main.py
|- data/
|  `- books.json
|- logic/
|  |- auth.py
|  |- book.py
|  |- borrow.py
|  |- find.py
|  |- storage.py
|  `- student.py
|- ui/
|  |- window.py
|  |- form.py
|  |- edit_form.py
|  `- search.py
`- tests
```

## UML - Diagramme de classes

```mermaid
classDiagram
    class MaktabatiApp {
        +run()
        +refresh_admin_views()
        +refresh_student_views()
        -_login()
        -_register_student()
        -_borrow_selected_book()
        -_return_selected_borrowing()
    }

    class BookForm {
        +submit()
    }

    class EditForm {
        +submit()
    }

    class SearchPanel {
        +refresh()
    }

    class AuthLogic {
        +authenticate_user(username, password, role)
        +register_student_account(username, password, first_name, last_name)
        +get_default_admin_credentials()
    }

    class BookLogic {
        +get_next_id(books)
        +add_book(title, author, year, isbn)
        +find_book(book_id)
        +update_book(book_id, title, author, year, isbn)
        +delete_book(book_id)
    }

    class BorrowLogic {
        +borrow_book(student_id, first_name, last_name, book_id, duration_days)
        +return_book(borrowing_id)
        +get_all_borrowings()
        +get_student_borrowings(student_id)
        +get_blacklisted_students()
    }

    class StudentLogic {
        +get_next_student_id(students)
        +create_student(first_name, last_name)
        +upsert_student(student_id, first_name, last_name)
        +find_student(student_id)
    }

    class FindLogic {
        +search_books(query, author_filter, year_filter, status_filter)
        +get_all_authors()
        +get_all_years()
    }

    class Storage {
        +load_state()
        +save_state(state)
        +load_books()
        +load_students()
        +load_borrowings()
        +load_users()
    }

    MaktabatiApp --> BookForm
    MaktabatiApp --> EditForm
    MaktabatiApp --> SearchPanel
    MaktabatiApp --> AuthLogic
    MaktabatiApp --> BookLogic
    MaktabatiApp --> BorrowLogic
    MaktabatiApp --> StudentLogic
    SearchPanel --> FindLogic
    AuthLogic --> StudentLogic
    AuthLogic --> Storage
    BookLogic --> Storage
    BorrowLogic --> StudentLogic
    BorrowLogic --> Storage
    FindLogic --> Storage
    StudentLogic --> Storage
```

## UML - Diagramme de cas d'utilisation

```mermaid
flowchart LR
    Admin[Admin]
    Etudiant[Etudiant]

    UC1((Se connecter))
    UC2((Ajouter un livre))
    UC3((Modifier un livre))
    UC4((Supprimer un livre))
    UC5((Rechercher des livres))
    UC6((Creer un compte etudiant))
    UC7((Emprunter un livre))
    UC8((Retourner un livre))
    UC9((Consulter les emprunts))
    UC10((Consulter la liste noire))

    Admin --> UC1
    Admin --> UC2
    Admin --> UC3
    Admin --> UC4
    Admin --> UC5
    Admin --> UC8
    Admin --> UC9
    Admin --> UC10

    Etudiant --> UC1
    Etudiant --> UC5
    Etudiant --> UC6
    Etudiant --> UC7
```

## Diagramme du pipeline de fonctionnement

```mermaid
flowchart TD
    A[Demarrage de l'application] --> B[main.py]
    B --> C[ui/window.py : MaktabatiApp]
    C --> D[Affichage de l'ecran de connexion]

    D --> E{Action utilisateur}
    E -->|Connexion| F[auth.py : authenticate_user]
    E -->|Inscription etudiant| G[auth.py : register_student_account]

    G --> H[student.py : create_student]
    H --> I[storage.py : save_state]
    G --> I

    F --> J{Role reconnu}
    J -->|Admin| K[Tableau de bord admin]
    J -->|Etudiant| L[Tableau de bord etudiant]

    K --> M[Gestion des livres]
    K --> N[Suivi des emprunts]
    K --> O[Retours]
    K --> P[Liste noire]

    M --> Q[book.py]
    N --> R[borrow.py]
    O --> R
    P --> R

    L --> S[Recherche dans le catalogue]
    L --> T[Emprunt d'un livre]
    S --> U[find.py]
    T --> R

    Q --> V[storage.py : load_state / save_state]
    R --> V
    U --> V
```

## Diagramme de sequence - Emprunt d'un livre

```mermaid
sequenceDiagram
    actor Etudiant
    participant UI as ui/window.py
    participant Borrow as logic/borrow.py
    participant Student as logic/student.py
    participant Storage as logic/storage.py

    Etudiant->>UI: Selectionne un livre et clique sur Emprunter
    UI->>Borrow: borrow_book(student_id, first_name, last_name, book_id, duree)
    Borrow->>Storage: load_state()
    Borrow->>Student: upsert_student(student_id, first_name, last_name)
    Student->>Storage: load_state()
    Student->>Storage: save_state(state)
    Borrow->>Storage: save_state(state)
    Borrow-->>UI: details de l'emprunt
    UI-->>Etudiant: affiche la date de retour prevue
```

## Structure JSON

Les donnees sont stockees dans [data/books.json](/c:/Users/kouss/coding/book_manager_projet_orad/data/books.json) avec cette structure :

```json
{
    "books": [],
    "students": [],
    "borrowings": [],
    "users": []
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
    "student_id": "1",
    "first_name": "Aya",
    "last_name": "Benali",
    "borrowed_book_ids": ["1", "4"]
}
```

### `borrowings`

```json
{
    "id": "1",
    "student_id": "1",
    "book_id": "4",
    "borrow_date": "2026-05-18",
    "due_date": "2026-06-01",
    "returned_date": "",
    "status": "borrowed"
}
```

### `users`

```json
{
    "username": "aya",
    "password": "1234",
    "role": "student",
    "student_id": "1",
    "first_name": "Aya",
    "last_name": "Benali"
}
```

## Lancer l'application

```bash
python main.py
```

## Version executable

Une version Windows executable est deja generee dans :

- [dist/main.exe](/c:/Users/kouss/coding/book_manager_projet_orad/dist/main.exe)

### Executer l'application

Depuis l'explorateur Windows :

- ouvrir le dossier `dist`
- double-cliquer sur `main.exe`

Depuis le terminal :

```powershell
.\dist\main.exe
```

### Regenerer le fichier `.exe`

Le projet contient deja le fichier de configuration [main.spec](/c:/Users/kouss/coding/book_manager_projet_orad/main.spec:1).

Si `PyInstaller` est installe, la commande de generation est :

```bash
pyinstaller main.spec
```

Le fichier genere sera ensuite disponible dans :

- `dist/main.exe`

### Donnees utilisees par l'executable

L'executable embarque aussi le fichier de donnees :

- [data/books.json](/c:/Users/kouss/coding/book_manager_projet_orad/data/books.json)

Le fichier `main.spec` inclut deja cette ressource :

```python
datas=[('data/books.json', 'data')]
```

## Tests

Fichiers de tests disponibles :

- [test_auth.py](/c:/Users/kouss/coding/book_manager_projet_orad/test_auth.py)
- [test_borrow.py](/c:/Users/kouss/coding/book_manager_projet_orad/test_borrow.py)
- [test_delete.py](/c:/Users/kouss/coding/book_manager_projet_orad/test_delete.py)
- [test_edit.py](/c:/Users/kouss/coding/book_manager_projet_orad/test_edit.py)
- [test_student.py](/c:/Users/kouss/coding/book_manager_projet_orad/test_student.py)

Compilation verifiee avec :

```bash
python -m py_compile main.py logic\storage.py logic\book.py logic\borrow.py logic\student.py logic\find.py logic\auth.py ui\window.py ui\form.py ui\edit_form.py ui\search.py test_auth.py test_borrow.py test_delete.py test_edit.py test_student.py
```

`pytest` n'etait pas installe dans l'environnement au moment de la verification.
