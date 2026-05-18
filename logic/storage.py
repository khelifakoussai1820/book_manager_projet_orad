import json
from copy import deepcopy
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "library.json"

DEFAULT_STATE = {
    "books": [],       # {id, title, author, year, isbn, total_copies, available_copies}
    "students": [],    # {id, first_name, last_name, blacklisted, blacklist_reason}
    "borrowings": [],  # {id, student_id, book_id, borrow_date, due_date, returned_date}
}


def load_state():
    if not DATA_FILE.exists():
        return deepcopy(DEFAULT_STATE)
    try:
        content = DATA_FILE.read_text(encoding="utf-8").strip()
        if not content:
            return deepcopy(DEFAULT_STATE)
        data = json.loads(content)
    except (json.JSONDecodeError, OSError):
        return deepcopy(DEFAULT_STATE)

    # Ensure all keys exist
    for key in DEFAULT_STATE:
        data.setdefault(key, [])
    return data


def save_state(state):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(state, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
