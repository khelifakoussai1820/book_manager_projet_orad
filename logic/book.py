from logic.storage import load_state, save_state


def get_next_id(books):
    if not books:
        return "1"

    ids = []
    for book in books:
        try:
            ids.append(int(book.get("id", 0)))
        except (TypeError, ValueError):
            ids.append(0)
    return str(max(ids) + 1)


def add_book(title, author, year, isbn):
    state = load_state()
    books = state["books"]

    new_book = {
        "id": get_next_id(books),
        "title": title.strip(),
        "author": author.strip(),
        "year": int(year) if str(year).strip() else 0,
        "isbn": isbn.strip(),
        "status": "available",
    }
    books.append(new_book)
    save_state(state)
    return new_book


def find_book(book_id):
    for book in load_state()["books"]:
        if str(book.get("id", "")) == str(book_id):
            return book
    return None


def update_book(book_id, title, author, year, isbn):
    state = load_state()

    for book in state["books"]:
        if str(book.get("id", "")) == str(book_id):
            book["title"] = title.strip()
            book["author"] = author.strip()
            book["year"] = int(year) if str(year).strip() else 0
            book["isbn"] = isbn.strip()
            save_state(state)
            return True
    return False


def delete_book(book_id):
    state = load_state()
    book_id = str(book_id)

    if any(
        borrowing["book_id"] == book_id and borrowing["status"] != "returned"
        for borrowing in state["borrowings"]
    ):
        raise ValueError("Impossible de supprimer un livre en cours d'emprunt.")

    new_books = [book for book in state["books"] if str(book.get("id", "")) != book_id]
    if len(new_books) == len(state["books"]):
        return False

    state["books"] = new_books
    state["borrowings"] = [
        borrowing for borrowing in state["borrowings"] if borrowing["book_id"] != book_id
    ]
    save_state(state)
    return True
