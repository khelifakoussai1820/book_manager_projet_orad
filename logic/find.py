from logic.storage import load_state


def _load_books():
    return load_state()["books"]


def search_books(query="", author_filter="", year_filter="", status_filter=""):
    query = query.strip().lower()
    author_filter = author_filter.strip().lower()
    year_filter = str(year_filter).strip()
    status_filter = status_filter.strip().lower()

    results = []
    for book in _load_books():
        if query and query not in book["title"].lower() and query not in book["author"].lower():
            continue
        if author_filter and author_filter not in book["author"].lower():
            continue
        if year_filter and year_filter != str(book["year"]):
            continue
        if status_filter and status_filter != str(book["status"]).lower():
            continue
        results.append(book)
    return results


def get_all_authors():
    return sorted({book["author"] for book in _load_books() if book["author"]})


def get_all_years():
    return sorted({str(book["year"]) for book in _load_books() if book["year"]})
