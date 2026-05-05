"""logic/find.py — search and filter helpers for Maktabati."""

from __future__ import annotations
import json
from pathlib import Path

BOOKS_FILE = Path(__file__).resolve().parent.parent / "data" / "books.json"


def _load_books() -> list[dict]:
    if not BOOKS_FILE.exists():
        return []
    content = BOOKS_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return []
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return []
    books = data.get("book", data) if isinstance(data, dict) else data
    if not isinstance(books, list):
        return []
    return [
        {
            "title":  b.get("title")  or b.get("titre")  or "",
            "author": b.get("author") or b.get("auteur") or "",
            "year":   str(b.get("year") or b.get("annee") or b.get("date") or ""),
        }
        for b in books if isinstance(b, dict)
    ]


def search_books(query: str = "", author_filter: str = "", year_filter: str = "") -> list[dict]:
    q  = query.strip().lower()
    af = author_filter.strip().lower()
    yf = year_filter.strip()
    results = []
    for b in _load_books():
        if q  and q  not in b["title"].lower() and q not in b["author"].lower():
            continue
        if af and af not in b["author"].lower():
            continue
        if yf and yf != b["year"]:
            continue
        results.append(b)
    return results


def get_all_authors() -> list[str]:
    return sorted({b["author"] for b in _load_books() if b["author"]})


def get_all_years() -> list[str]:
    return sorted({b["year"] for b in _load_books() if b["year"]})