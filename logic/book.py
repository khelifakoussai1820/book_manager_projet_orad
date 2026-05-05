from logic.storage import load_books, save_books


def get_next_id(books):
    if not books:
        return 1

    ids = []
    for book in books:
        try:
            ids.append(int(book.get("id", 0)))
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
        "status": "available",
    }

    books.append(new_book)
    save_books(books)
    return new_book


def find_book(book_id):
    for book in load_books():
        if str(book.get("id", "")) == str(book_id):
            return book
    return None


def update_book(book_id, title, author, year, isbn, status):
    books = load_books()

    for book in books:
        if str(book.get("id", "")) == str(book_id):
            book["title"] = title
            book["author"] = author
            book["year"] = int(year) if year else 0
            book["isbn"] = isbn
            book["status"] = status
            save_books(books)
            return True

    return False


def delete_book(book_id):
    books = load_books()
    new_books = [
        book for book in books
        if str(book.get("id", "")) != str(book_id)
    ]

    if len(new_books) == len(books):
        return False

    save_books(new_books)
    return True