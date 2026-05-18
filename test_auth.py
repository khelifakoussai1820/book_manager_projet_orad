from logic import auth as auth_logic


def test_authenticate_user_returns_matching_user(monkeypatch):
    monkeypatch.setattr(
        auth_logic,
        "load_state",
        lambda: {
            "books": [],
            "students": [],
            "borrowings": [],
            "users": [
                {
                    "username": "admin",
                    "password": "admin123",
                    "role": "admin",
                    "student_id": "",
                    "first_name": "Admin",
                    "last_name": "Principal",
                }
            ],
        },
    )

    user = auth_logic.authenticate_user("admin", "admin123", "admin")

    assert user["username"] == "admin"
    assert user["role"] == "admin"


def test_register_student_account_adds_user(monkeypatch):
    saved = {}
    state = {
        "books": [],
        "students": [],
        "borrowings": [],
        "users": [],
    }

    monkeypatch.setattr(auth_logic, "load_state", lambda: state)
    monkeypatch.setattr(auth_logic, "save_state", lambda data: saved.update({"state": data}))
    monkeypatch.setattr(
        auth_logic,
        "create_student",
        lambda first_name, last_name: {
            "student_id": "10",
            "first_name": first_name,
            "last_name": last_name,
        },
    )

    user = auth_logic.register_student_account("aya", "1234", "Aya", "Benali")

    assert user["role"] == "student"
    assert saved["state"]["users"][0]["student_id"] == "10"
