from datetime import date, datetime, timedelta

from logic.storage import load_state, save_state
from logic.student import upsert_student


DEFAULT_BORROW_DAYS = 14


def _next_borrowing_id(borrowings):
    if not borrowings:
        return "1"

    ids = []
    for borrowing in borrowings:
        try:
            ids.append(int(borrowing.get("id", 0)))
        except (TypeError, ValueError):
            ids.append(0)
    return str(max(ids) + 1)


def _parse_iso_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def borrow_book(student_id, first_name, last_name, book_id, duration_days=DEFAULT_BORROW_DAYS):
    state = load_state()
    book_id = str(book_id).strip()
    student_id = str(student_id).strip()

    book = next((item for item in state["books"] if item["id"] == book_id), None)
    if book is None:
        raise ValueError("Livre introuvable.")
    if book["status"] != "available":
        raise ValueError("Ce livre n'est pas disponible.")

    upsert_student(student_id, first_name, last_name)
    state = load_state()

    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=int(duration_days))

    borrowing = {
        "id": _next_borrowing_id(state["borrowings"]),
        "student_id": student_id,
        "book_id": book_id,
        "borrow_date": borrow_date.isoformat(),
        "due_date": due_date.isoformat(),
        "returned_date": "",
        "status": "borrowed",
    }
    state["borrowings"].append(borrowing)
    save_state(state)
    return borrowing


def return_book(borrowing_id):
    state = load_state()
    borrowing_id = str(borrowing_id).strip()

    for borrowing in state["borrowings"]:
        if borrowing["id"] == borrowing_id and borrowing["status"] != "returned":
            borrowing["status"] = "returned"
            borrowing["returned_date"] = date.today().isoformat()
            save_state(state)
            return True
    return False


def get_all_borrowings():
    state = load_state()
    students = {student["student_id"]: student for student in state["students"]}
    books = {book["id"]: book for book in state["books"]}

    enriched = []
    for borrowing in state["borrowings"]:
        student = students.get(borrowing["student_id"], {})
        book = books.get(borrowing["book_id"], {})
        due_date = borrowing.get("due_date", "")
        is_late = False
        if borrowing.get("status") != "returned" and due_date:
            try:
                is_late = _parse_iso_date(due_date) < date.today()
            except ValueError:
                is_late = False

        enriched.append(
            {
                **borrowing,
                "student_name": f'{student.get("first_name", "")} {student.get("last_name", "")}'.strip(),
                "book_title": book.get("title", ""),
                "is_late": is_late,
            }
        )

    return sorted(enriched, key=lambda item: (item["status"], item["due_date"], item["id"]))


def get_student_borrowings(student_id):
    student_id = str(student_id).strip()
    return [borrowing for borrowing in get_all_borrowings() if borrowing["student_id"] == student_id]


def get_blacklisted_students():
    late_borrowings = [
        borrowing
        for borrowing in get_all_borrowings()
        if borrowing["status"] != "returned" and borrowing["is_late"]
    ]

    grouped = {}
    for borrowing in late_borrowings:
        key = borrowing["student_id"]
        grouped.setdefault(
            key,
            {
                "student_id": borrowing["student_id"],
                "student_name": borrowing["student_name"],
                "late_books": [],
            },
        )
        grouped[key]["late_books"].append(
            {
                "book_title": borrowing["book_title"],
                "due_date": borrowing["due_date"],
            }
        )

    return sorted(grouped.values(), key=lambda item: (item["student_name"].lower(), item["student_id"]))
