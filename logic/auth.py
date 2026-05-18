from logic.storage import load_state, save_state
from logic.student import create_student


def authenticate_user(username, password, role):
    username = username.strip()
    password = password.strip()
    role = role.strip().lower()

    for user in load_state()["users"]:
        if user["username"] == username and user["password"] == password and user["role"] == role:
            return user
    return None


def register_student_account(username, password, first_name, last_name):
    username = username.strip()
    password = password.strip()
    first_name = first_name.strip()
    last_name = last_name.strip()

    if not username or not password:
        raise ValueError("Le nom d'utilisateur et le mot de passe sont obligatoires.")
    if not first_name or not last_name:
        raise ValueError("Les informations étudiant sont obligatoires.")

    state = load_state()
    if any(user["username"].lower() == username.lower() for user in state["users"]):
        raise ValueError("Ce nom d'utilisateur existe déjà.")

    student = create_student(first_name, last_name)
    student_id = student["student_id"]

    state = load_state()
    user = {
        "username": username,
        "password": password,
        "role": "student",
        "student_id": student_id,
        "first_name": first_name,
        "last_name": last_name,
    }
    state["users"].append(user)
    save_state(state)
    return user


def get_default_admin_credentials():
    return {"username": "admin", "password": "admin123"}
