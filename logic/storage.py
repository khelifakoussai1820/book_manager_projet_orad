import json
import os

# Path is always relative to this file, not the working directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHIER = os.path.join(BASE_DIR, "data", "books.json")

def load_books():
    if not os.path.exists(FICHIER):
        return []
    with open(FICHIER, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get("book"), list):
        return data["book"]
    return data if isinstance(data, list) else []

def save_books(books):
    os.makedirs(os.path.dirname(FICHIER), exist_ok=True)
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump({"book": books}, f, indent=4, ensure_ascii=False)

def get_next_id(books):
    """Return max existing id + 1 (works with int or str ids)."""
    if not books:
        return 1
    ids = []
    for b in books:
        try:
            ids.append(int(b.get("id", 0)))
        except (ValueError, TypeError):
            ids.append(0)
    return max(ids) + 1
