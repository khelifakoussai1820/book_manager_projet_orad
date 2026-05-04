from logic.storage import load_books, save_books

def get_next_id(books):
    if not books:
        return 1
    ids = []
    for b in books:
        try:
            ids.append(int(b.get("id", 0)))
        except (ValueError, TypeError):
            ids.append(0)
    return max(ids) + 1

def add_book(title, author, year, isbn):
    books = load_books()

    new_book = {
        "id": get_next_id(books),
        "title": title,
        "author": author,
        "year": int(year) if year else 0,
        "isbn": isbn,
        "status": "available"
    }

    books.append(new_book)
    save_books(books)
    return new_book