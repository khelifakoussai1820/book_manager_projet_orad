from logic import book as book_logic


def test_update_book_changes_matching_book(monkeypatch):
    saved = {}
    state = {
        "books": [
            {
                "id": "1",
                "title": "Old title",
                "author": "Old author",
                "year": 2000,
                "isbn": "old",
                "status": "available",
            }
        ],
        "students": [],
        "borrowings": [],
    }

    monkeypatch.setattr(book_logic, "load_state", lambda: state)
    monkeypatch.setattr(book_logic, "save_state", lambda data: saved.update({"state": data}))

    result = book_logic.update_book("1", "New title", "New author", "2026", "new-isbn")

    assert result is True
    assert saved["state"]["books"][0] == {
        "id": "1",
        "title": "New title",
        "author": "New author",
        "year": 2026,
        "isbn": "new-isbn",
        "status": "available",
    }


def test_update_book_returns_false_when_id_is_missing(monkeypatch):
    state = {"books": [{"id": "1", "title": "Old title"}], "students": [], "borrowings": []}

    monkeypatch.setattr(book_logic, "load_state", lambda: state)
    monkeypatch.setattr(
        book_logic,
        "save_state",
        lambda data: (_ for _ in ()).throw(AssertionError("save_state should not run")),
    )

    assert book_logic.update_book("99", "Title", "Author", "2026", "isbn") is False
