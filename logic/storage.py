import json
from copy import deepcopy
from datetime import date
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "books.json"

DEFAULT_STATE = {
    "books": [],
    "students": [],
    "borrowings": [],
}


def _coerce_book(raw_book):
    if not isinstance(raw_book, dict):
        return None

    return {
        "id": str(raw_book.get("id", "")).strip(),
        "title": (raw_book.get("title") or raw_book.get("titre") or "").strip(),
        "author": (raw_book.get("author") or raw_book.get("auteur") or "").strip(),
        "year": int(raw_book.get("year") or raw_book.get("annee") or 0),
        "isbn": str(raw_book.get("isbn", "")).strip(),
        "status": str(raw_book.get("status") or "available").strip() or "available",
    }


def _normalize_state(raw_data):
    if isinstance(raw_data, list):
        raw_data = {"books": raw_data}

    if isinstance(raw_data, dict) and "book" in raw_data and "books" not in raw_data:
        raw_data = {
            "books": raw_data.get("book", []),
            "students": raw_data.get("students", []),
            "borrowings": raw_data.get("borrowings", []),
        }

    if not isinstance(raw_data, dict):
        return deepcopy(DEFAULT_STATE)

    books = []
    for raw_book in raw_data.get("books", []):
        book = _coerce_book(raw_book)
        if book and book["id"]:
            books.append(book)

    students = []
    for raw_student in raw_data.get("students", []):
        if not isinstance(raw_student, dict):
            continue
        student_id = str(raw_student.get("student_id") or raw_student.get("id") or "").strip()
        if not student_id:
            continue
        students.append(
            {
                "student_id": student_id,
                "first_name": str(raw_student.get("first_name") or raw_student.get("prenom") or "").strip(),
                "last_name": str(raw_student.get("last_name") or raw_student.get("nom") or "").strip(),
                "borrowed_book_ids": [
                    str(book_id).strip()
                    for book_id in raw_student.get("borrowed_book_ids", [])
                    if str(book_id).strip()
                ],
            }
        )

    borrowings = []
    for raw_borrowing in raw_data.get("borrowings", []):
        if not isinstance(raw_borrowing, dict):
            continue
        borrowing_id = str(raw_borrowing.get("id", "")).strip()
        student_id = str(raw_borrowing.get("student_id", "")).strip()
        book_id = str(raw_borrowing.get("book_id", "")).strip()
        if not borrowing_id or not student_id or not book_id:
            continue
        borrowings.append(
            {
                "id": borrowing_id,
                "student_id": student_id,
                "book_id": book_id,
                "borrow_date": str(raw_borrowing.get("borrow_date") or date.today().isoformat()),
                "due_date": str(raw_borrowing.get("due_date") or date.today().isoformat()),
                "returned_date": str(raw_borrowing.get("returned_date") or "").strip(),
                "status": str(raw_borrowing.get("status") or "borrowed").strip() or "borrowed",
            }
        )

    state = {
        "books": books,
        "students": students,
        "borrowings": borrowings,
    }
    _sync_computed_fields(state)
    return state


def _sync_computed_fields(state):
    active_by_student = {}
    active_book_ids = set()

    for borrowing in state["borrowings"]:
        if borrowing.get("status") != "returned":
            student_id = borrowing["student_id"]
            active_by_student.setdefault(student_id, []).append(borrowing["book_id"])
            active_book_ids.add(borrowing["book_id"])

    for student in state["students"]:
        student["borrowed_book_ids"] = active_by_student.get(student["student_id"], [])

    for book in state["books"]:
        book["status"] = "borrowed" if book["id"] in active_book_ids else "available"


def load_state():
    if not DATA_FILE.exists():
        return deepcopy(DEFAULT_STATE)

    content = DATA_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return deepcopy(DEFAULT_STATE)

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return deepcopy(DEFAULT_STATE)

    return _normalize_state(data)


def save_state(state):
    normalized = _normalize_state(state)
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(normalized, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )


def load_books():
    return load_state()["books"]


def save_books(books):
    state = load_state()
    state["books"] = books
    save_state(state)


def load_students():
    return load_state()["students"]


def load_borrowings():
    return load_state()["borrowings"]
