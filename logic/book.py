from logic.storage import load_books, save_books, get_next_id

def add_book(title, author, year, isbn):
    books = load_books()

    new_book = {
        "id": get_next_id(books),   # FIX: was "id": int (the type, not a value)
        "title": title,
        "author": author,
        "year": int(year) if year else 0,
        "isbn": isbn,
        "status": "available"
    }

    books.append(new_book)
    save_books(books)
    return new_book
