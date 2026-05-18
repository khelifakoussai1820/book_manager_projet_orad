from datetime import date, timedelta

from logic.storage import load_state, save_state


DEFAULT_BORROW_DAYS = 14


def _next_id(items):
    if not items:
        return "1"
    ids = []
    for item in items:
        try:
            ids.append(int(item.get("id", 0)))
        except (TypeError, ValueError):
            ids.append(0)
    return str(max(ids) + 1)


def borrow_book(student_id, book_id, duration_days=DEFAULT_BORROW_DAYS):
    state = load_state()
    student_id = str(student_id)
    book_id = str(book_id)

    student = next((s for s in state["students"] if str(s["id"]) == student_id), None)
    if student is None:
        raise ValueError("Étudiant introuvable.")
    if student.get("blacklisted"):
        reason = student.get("blacklist_reason", "")
        raise ValueError(
            f"Cet étudiant est sur liste noire. Emprunt refusé.\nRaison : {reason or 'non précisée'}"
        )

    book = next((b for b in state["books"] if str(b["id"]) == book_id), None)
    if book is None:
        raise ValueError("Livre introuvable.")
    if book["available_copies"] <= 0:
        raise ValueError("Aucune copie disponible pour ce livre.")

    try:
        duration = int(duration_days)
        if duration <= 0:
            raise ValueError
    except (TypeError, ValueError):
        raise ValueError("La durée d'emprunt doit être un entier positif.")

    today = date.today()
    borrowing = {
        "id": _next_id(state["borrowings"]),
        "student_id": student_id,
        "book_id": book_id,
        "borrow_date": today.isoformat(),
        "due_date": (today + timedelta(days=duration)).isoformat(),
        "returned_date": "",
    }
    book["available_copies"] -= 1
    state["borrowings"].append(borrowing)
    save_state(state)
    return borrowing


def return_borrowing(borrowing_id):
    state = load_state()
    borrowing_id = str(borrowing_id)

    for borrowing in state["borrowings"]:
        if str(borrowing["id"]) == borrowing_id and not borrowing.get("returned_date"):
            borrowing["returned_date"] = date.today().isoformat()
            for book in state["books"]:
                if str(book["id"]) == borrowing["book_id"]:
                    if book["available_copies"] < book["total_copies"]:
                        book["available_copies"] += 1
                    break
            save_state(state)
            return True
    return False


def get_all_borrowings():
    state = load_state()
    students = {str(s["id"]): s for s in state["students"]}
    books = {str(b["id"]): b for b in state["books"]}

    result = []
    for borrowing in state["borrowings"]:
        student = students.get(borrowing["student_id"], {})
        book = books.get(borrowing["book_id"], {})
        result.append({
            **borrowing,
            "student_name": f"{student.get('first_name', '')} {student.get('last_name', '')}".strip() or "Étudiant supprimé",
            "book_title": book.get("title", "Livre supprimé"),
        })
    # Active first, then by date desc
    result.sort(key=lambda x: (bool(x["returned_date"]), x["borrow_date"]), reverse=False)
    return result
