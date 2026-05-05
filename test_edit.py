from logic import book as book_logic


def test_update_book_changes_matching_book(monkeypatch):
    saved = {}
    books = [
        {
            "id": 1,
            "title": "Old title",
            "author": "Old author",
            "year": 2000,
            "isbn": "old",
            "status": "available",
        }
    ]

    monkeypatch.setattr(book_logic, "load_books", lambda: books)
    monkeypatch.setattr(book_logic, "save_books", lambda data: saved.update({"books": data}))

    result = book_logic.update_book(
        1,
        "New title",
        "New author",
        "2026",
        "new-isbn",
        "borrowed",
    )

    assert result is True
    assert saved["books"][0] == {
        "id": 1,
        "title": "New title",
        "author": "New author",
        "year": 2026,
        "isbn": "new-isbn",
        "status": "borrowed",
    }


def test_update_book_returns_false_when_id_is_missing(monkeypatch):
    books = [{"id": 1, "title": "Old title"}]

    monkeypatch.setattr(book_logic, "load_books", lambda: books)
    monkeypatch.setattr(
        book_logic,
        "save_books",
        lambda data: (_ for _ in ()).throw(AssertionError("save_books should not run")),
    )

    assert book_logic.update_book(99, "Title", "Author", "2026", "isbn", "available") is False