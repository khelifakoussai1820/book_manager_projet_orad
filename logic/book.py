from logic.storage import load_state, save_state


def _next_id(items):
    if not items:
        return "1"
    ids = []
    for item in items:
        try:
            ids.append(int(item.get("id", 0)))
        except (TypeError, ValueError):
            ids.append(0)
    return str(max(ids) + 1)


def get_all_books():
    return load_state()["books"]


def find_book(book_id):
    book_id = str(book_id)
    for book in load_state()["books"]:
        if str(book.get("id")) == book_id:
            return book
    return None


def add_book(title, author, year, isbn, total_copies):
    title = title.strip()
    author = author.strip()
    if not title or not author:
        raise ValueError("Le titre et l'auteur sont obligatoires.")
    try:
        total = int(total_copies)
        if total <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("Le nombre de copies doit être un entier positif.")

    year_int = 0
    if str(year).strip():
        if not str(year).strip().isdigit():
            raise ValueError("L'année doit être un nombre.")
        year_int = int(year)

    state = load_state()
    book = {
        "id": _next_id(state["books"]),
        "title": title,
        "author": author.strip(),
        "year": year_int,
        "isbn": str(isbn).strip(),
        "total_copies": total,
        "available_copies": total,
    }
    state["books"].append(book)
    save_state(state)
    return book


def update_book(book_id, title, author, year, isbn, total_copies):
    title = title.strip()
    author = author.strip()
    if not title or not author:
        raise ValueError("Le titre et l'auteur sont obligatoires.")
    try:
        total = int(total_copies)
        if total <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("Le nombre de copies doit être un entier positif.")

    year_int = 0
    if str(year).strip():
        if not str(year).strip().isdigit():
            raise ValueError("L'année doit être un nombre.")
        year_int = int(year)

    state = load_state()
    for book in state["books"]:
        if str(book["id"]) == str(book_id):
            borrowed = book["total_copies"] - book["available_copies"]
            if total < borrowed:
                raise ValueError(
                    f"Impossible : {borrowed} copie(s) actuellement empruntée(s)."
                )
            book["title"] = title
            book["author"] = author
            book["year"] = year_int
            book["isbn"] = str(isbn).strip()
            book["total_copies"] = total
            book["available_copies"] = total - borrowed
            save_state(state)
            return True
    return False


def delete_book(book_id):
    state = load_state()
    book_id = str(book_id)

    active = any(
        b["book_id"] == book_id and not b.get("returned_date")
        for b in state["borrowings"]
    )
    if active:
        raise ValueError("Impossible de supprimer un livre en cours d'emprunt.")

    new_books = [b for b in state["books"] if str(b["id"]) != book_id]
    if len(new_books) == len(state["books"]):
        return False
    state["books"] = new_books
    # Remove historical borrowings for this book
    state["borrowings"] = [b for b in state["borrowings"] if b["book_id"] != book_id]
    save_state(state)
    return True


def search_books(query=""):
    query = (query or "").strip().lower()
    books = get_all_books()
    if not query:
        return books
    return [
        b for b in books
        if query in b["title"].lower()
        or query in b["author"].lower()
        or query in str(b.get("isbn", "")).lower()
        or query in str(b["id"])
    ]
