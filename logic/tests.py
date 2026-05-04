"""
Tests automatiques — pas besoin de Tkinter.
Teste: storage, get_next_id, add_book.
"""
import sys, os, json, shutil, tempfile, unittest

# Make imports work from project root
sys.path.insert(0, os.path.dirname(__file__))

# ── Patch FICHIER to use a temp file so tests don't touch real data ──
import logic.storage as storage_mod
_tmp_dir = tempfile.mkdtemp()
_tmp_file = os.path.join(_tmp_dir, "books.json")
storage_mod.FICHIER = _tmp_file   # redirect all reads/writes

from logic.storage import load_books, save_books, get_next_id
from logic.book import add_book


class TestGetNextId(unittest.TestCase):
    def test_empty_list_returns_1(self):
        self.assertEqual(get_next_id([]), 1)

    def test_next_after_existing(self):
        books = [{"id": 1}, {"id": 2}, {"id": 5}]
        self.assertEqual(get_next_id(books), 6)

    def test_handles_string_ids(self):
        books = [{"id": "3"}, {"id": "7"}]
        self.assertEqual(get_next_id(books), 8)

    def test_handles_missing_id(self):
        books = [{"title": "no id here"}]
        self.assertEqual(get_next_id(books), 1)


class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        # Start with empty file
        if os.path.exists(_tmp_file):
            os.remove(_tmp_file)

    def test_save_and_reload(self):
        books = [{"id": 1, "title": "Test", "author": "A"}]
        save_books(books)
        loaded = load_books()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["title"], "Test")

    def test_load_missing_file_returns_empty(self):
        if os.path.exists(_tmp_file):
            os.remove(_tmp_file)
        self.assertEqual(load_books(), [])

    def test_json_structure_is_dict_with_book_key(self):
        save_books([{"id": 1, "title": "A"}])
        with open(_tmp_file) as f:
            raw = json.load(f)
        self.assertIn("book", raw)
        self.assertIsInstance(raw["book"], list)


class TestAddBook(unittest.TestCase):
    def setUp(self):
        if os.path.exists(_tmp_file):
            os.remove(_tmp_file)

    def test_add_single_book(self):
        book = add_book("Dune", "Frank Herbert", "1965", "978-0441013593")
        self.assertEqual(book["title"], "Dune")
        self.assertEqual(book["author"], "Frank Herbert")
        self.assertEqual(book["year"], 1965)
        self.assertEqual(book["status"], "available")
        self.assertEqual(book["id"], 1)   # first book gets id=1

    def test_id_increments(self):
        b1 = add_book("Book One", "Author A", "2000", "000")
        b2 = add_book("Book Two", "Author B", "2001", "001")
        self.assertEqual(b2["id"], b1["id"] + 1)

    def test_books_persist_after_add(self):
        add_book("Persisted", "Someone", "1999", "123")
        loaded = load_books()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["title"], "Persisted")

    def test_year_stored_as_int(self):
        book = add_book("Year Test", "Author", "2024", "")
        self.assertIsInstance(book["year"], int)

    def test_empty_year_defaults_to_zero(self):
        book = add_book("No Year", "Author", "", "")
        self.assertEqual(book["year"], 0)


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False)
    # cleanup
    shutil.rmtree(_tmp_dir, ignore_errors=True)
    sys.exit(0 if result.result.wasSuccessful() else 1)
