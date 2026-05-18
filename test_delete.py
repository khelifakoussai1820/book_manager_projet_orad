import pytest

from logic import book as book_logic


def test_delete_book_removes_matching_id(monkeypatch):
    saved = {}
    state = {
        "books": [
            {"id": "1", "title": "Book 1", "status": "available"},
            {"id": "2", "title": "Book 2", "status": "available"},
        ],
        "students": [],
        "borrowings": [],
    }

    monkeypatch.setattr(book_logic, "load_state", lambda: state)
    monkeypatch.setattr(book_logic, "save_state", lambda data: saved.update({"state": data}))

    assert book_logic.delete_book("1") is True
    assert saved["state"]["books"] == [{"id": "2", "title": "Book 2", "status": "available"}]


def test_delete_book_returns_false_when_id_is_missing(monkeypatch):
    state = {"books": [{"id": "1", "title": "Book 1"}], "students": [], "borrowings": []}

    monkeypatch.setattr(book_logic, "load_state", lambda: state)
    monkeypatch.setattr(
        book_logic,
        "save_state",
        lambda data: (_ for _ in ()).throw(AssertionError("save_state should not run")),
    )

    assert book_logic.delete_book("99") is False


def test_delete_book_rejects_active_borrowing(monkeypatch):
    state = {
        "books": [{"id": "1", "title": "Book 1", "status": "borrowed"}],
        "students": [],
        "borrowings": [{"id": "1", "student_id": "E1", "book_id": "1", "status": "borrowed"}],
    }

    monkeypatch.setattr(book_logic, "load_state", lambda: state)

    with pytest.raises(ValueError):
        book_logic.delete_book("1")
