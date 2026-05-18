from logic.storage import load_state, save_state


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


def get_all_students():
    return load_state()["students"]


def find_student(student_id):
    student_id = str(student_id)
    for student in load_state()["students"]:
        if str(student.get("id")) == student_id:
            return student
    return None


def add_student(first_name, last_name):
    first_name = first_name.strip()
    last_name = last_name.strip()
    if not first_name or not last_name:
        raise ValueError("Le prénom et le nom sont obligatoires.")

    state = load_state()
    student = {
        "id": _next_id(state["students"]),
        "first_name": first_name,
        "last_name": last_name,
        "blacklisted": False,
        "blacklist_reason": "",
    }
    state["students"].append(student)
    save_state(state)
    return student


def update_student(student_id, first_name, last_name):
    first_name = first_name.strip()
    last_name = last_name.strip()
    if not first_name or not last_name:
        raise ValueError("Le prénom et le nom sont obligatoires.")

    state = load_state()
    for student in state["students"]:
        if str(student["id"]) == str(student_id):
            student["first_name"] = first_name
            student["last_name"] = last_name
            save_state(state)
            return True
    return False


def delete_student(student_id):
    state = load_state()
    student_id = str(student_id)

    active = any(
        b["student_id"] == student_id and not b.get("returned_date")
        for b in state["borrowings"]
    )
    if active:
        raise ValueError("Impossible de supprimer un étudiant ayant des emprunts en cours.")

    new_students = [s for s in state["students"] if str(s["id"]) != student_id]
    if len(new_students) == len(state["students"]):
        return False
    state["students"] = new_students
    state["borrowings"] = [b for b in state["borrowings"] if b["student_id"] != student_id]
    save_state(state)
    return True


def set_blacklist(student_id, blacklisted, reason=""):
    state = load_state()
    for student in state["students"]:
        if str(student["id"]) == str(student_id):
            student["blacklisted"] = bool(blacklisted)
            student["blacklist_reason"] = reason.strip() if blacklisted else ""
            save_state(state)
            return True
    return False


def search_students(query=""):
    query = (query or "").strip().lower()
    students = get_all_students()
    if not query:
        return students
    return [
        s for s in students
        if query in s["first_name"].lower()
        or query in s["last_name"].lower()
        or query in str(s["id"])
    ]
