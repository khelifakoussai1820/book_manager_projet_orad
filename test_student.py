from logic import student as student_logic


def test_create_student_generates_next_numeric_id(monkeypatch):
    saved = {}
    state = {
        "books": [],
        "students": [
            {"student_id": "2", "first_name": "Aya", "last_name": "A", "borrowed_book_ids": []},
            {"student_id": "9", "first_name": "Yacine", "last_name": "B", "borrowed_book_ids": []},
        ],
        "borrowings": [],
        "users": [],
    }

    monkeypatch.setattr(student_logic, "load_state", lambda: state)
    monkeypatch.setattr(student_logic, "save_state", lambda data: saved.update({"state": data}))

    student = student_logic.create_student("Nora", "Benali")

    assert student["student_id"] == "10"
    assert saved["state"]["students"][-1]["student_id"] == "10"
    assert saved["state"]["students"][-1]["first_name"] == "Nora"
    assert saved["state"]["students"][-1]["last_name"] == "Benali"
