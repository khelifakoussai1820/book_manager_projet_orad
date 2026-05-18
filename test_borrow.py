from logic import borrow as borrow_logic


def test_return_book_marks_borrowing_as_returned(monkeypatch):
    saved = {}
    state = {
        "books": [{"id": "1", "title": "Book 1", "status": "borrowed"}],
        "students": [{"student_id": "E1", "first_name": "Ada", "last_name": "Lovelace", "borrowed_book_ids": ["1"]}],
        "borrowings": [
            {
                "id": "1",
                "student_id": "E1",
                "book_id": "1",
                "borrow_date": "2026-05-01",
                "due_date": "2026-05-15",
                "returned_date": "",
                "status": "borrowed",
            }
        ],
    }

    monkeypatch.setattr(borrow_logic, "load_state", lambda: state)
    monkeypatch.setattr(borrow_logic, "save_state", lambda data: saved.update({"state": data}))

    assert borrow_logic.return_book("1") is True
    assert saved["state"]["borrowings"][0]["status"] == "returned"
    assert saved["state"]["borrowings"][0]["returned_date"]


def test_get_blacklisted_students_returns_only_late_students(monkeypatch):
    monkeypatch.setattr(
        borrow_logic,
        "get_all_borrowings",
        lambda: [
            {
                "id": "1",
                "student_id": "E1",
                "student_name": "Ada Lovelace",
                "book_title": "Python",
                "borrow_date": "2026-05-01",
                "due_date": "2026-05-10",
                "status": "borrowed",
                "is_late": True,
            },
            {
                "id": "2",
                "student_id": "E2",
                "student_name": "Alan Turing",
                "book_title": "Math",
                "borrow_date": "2026-05-01",
                "due_date": "2026-05-30",
                "status": "borrowed",
                "is_late": False,
            },
        ],
    )

    result = borrow_logic.get_blacklisted_students()

    assert result == [
        {
            "student_id": "E1",
            "student_name": "Ada Lovelace",
            "late_books": [{"book_title": "Python", "due_date": "2026-05-10"}],
        }
    ]
