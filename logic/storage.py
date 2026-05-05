import json
from pathlib import Path


BOOKS_FILE = Path(__file__).resolve().parent.parent / "data" / "books.json"


def load_books():
    """Load books from data/books.json."""
    if not BOOKS_FILE.exists():
        return []

    content = BOOKS_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return []

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return []

    if isinstance(data, dict) and isinstance(data.get("book"), list):
        return data["book"]

    return data if isinstance(data, list) else []


def save_books(books):
    """Save books to data/books.json."""
    BOOKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {"book": books}
    BOOKS_FILE.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )