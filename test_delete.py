from logic import book as book_logic


def test_delete_book_removes_matching_id(monkeypatch):
    saved = {}
    books = [
        {"id": 1, "title": "Book 1"},
        {"id": 2, "title": "Book 2"},
    ]

    monkeypatch.setattr(book_logic, "load_books", lambda: books)
    monkeypatch.setattr(book_logic, "save_books", lambda data: saved.update({"books": data}))

    assert book_logic.delete_book(1) is True
    assert saved["books"] == [{"id": 2, "title": "Book 2"}]


def test_delete_book_returns_false_when_id_is_missing(monkeypatch):
    books = [{"id": 1, "title": "Book 1"}]

    monkeypatch.setattr(book_logic, "load_books", lambda: books)
    monkeypatch.setattr(
        book_logic,
        "save_books",
        lambda data: (_ for _ in ()).throw(AssertionError("save_books should not run")),
    )

    assert book_logic.delete_book(99) is False
