import json
import os

FICHIER = "data/books.json"

# Charger les livres depuis le fichier
def load_books():
    if not os.path.exists(FICHIER):
        return []
    with open(FICHIER, "r") as f:
        data = json.load(f)

    if isinstance(data, dict) and isinstance(data.get("book"), list):
        return data["book"]

    return data if isinstance(data, list) else []

# Sauvegarder les livres dans le fichier
def save_books(books):
    with open(FICHIER, "w") as f:

        json.dump({"book": books}, f, indent=4)