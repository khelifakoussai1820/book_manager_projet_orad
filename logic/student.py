from logic.storage import load_state, save_state


def upsert_student(student_id, first_name, last_name):
    state = load_state()
    student_id = str(student_id).strip()

    if not student_id:
        raise ValueError("L'identifiant étudiant est obligatoire.")

    first_name = first_name.strip()
    last_name = last_name.strip()
    if not first_name or not last_name:
        raise ValueError("Le prénom et le nom sont obligatoires.")

    for student in state["students"]:
        if student["student_id"] == student_id:
            student["first_name"] = first_name
            student["last_name"] = last_name
            save_state(state)
            return student

    student = {
        "student_id": student_id,
        "first_name": first_name,
        "last_name": last_name,
        "borrowed_book_ids": [],
    }
    state["students"].append(student)
    save_state(state)
    return student


def find_student(student_id):
    student_id = str(student_id).strip()
    for student in load_state()["students"]:
        if student["student_id"] == student_id:
            return student
    return None


def get_all_students():
    return sorted(
        load_state()["students"],
        key=lambda student: (
            student.get("last_name", "").lower(),
            student.get("first_name", "").lower(),
            student.get("student_id", ""),
        ),
    )
