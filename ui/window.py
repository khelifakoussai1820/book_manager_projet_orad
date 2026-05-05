import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk


BOOKS_FILE = Path(__file__).resolve().parent.parent / "data" / "books.json"


class MaktabatiApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Maktabati")
        self.root.geometry("980x560")          # a bit wider for the table
        self.root.minsize(860, 480)
        self.root.configure(bg="#f4efe6")
        self.count_var = tk.StringVar(value="0 livre disponible")
        self.books_table: ttk.Treeview | None = None
        self._search_panel = None

        self._build_header()
        self._build_content()

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg="#6b4226", padx=24, pady=22)
        header.pack(fill="x")

        tk.Label(header, text="Maktabati", font=("Georgia", 26, "bold"),
                 fg="#fff8ef", bg="#6b4226").pack(anchor="w")

        tk.Label(header, text="Gestion simple et elegante de votre bibliotheque",
                 font=("Calibri", 12), fg="#f5dfc3", bg="#6b4226"
                 ).pack(anchor="w", pady=(6, 0))

    def _build_content(self) -> None:
        container = tk.Frame(self.root, bg="#f4efe6", padx=24, pady=24)
        container.pack(fill="both", expand=True)

        left_panel = tk.Frame(container, bg="#f4efe6", width=240)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)

        right_panel = tk.Frame(container, bg="#fffaf3", bd=1, relief="solid",
                               padx=18, pady=18)
        right_panel.pack(side="right", fill="both", expand=True, padx=(18, 0))

        tk.Label(left_panel, text="Actions principales",
                 font=("Georgia", 18, "bold"), fg="#4b2e1f", bg="#f4efe6"
                 ).pack(anchor="w", pady=(0, 14))

        tk.Button(left_panel, text="Quitter", font=("Calibri", 13, "bold"),
                  bg="#7a5c46", fg="white", activebackground="#5e4432",
                  activeforeground="white", bd=0, padx=18, pady=12,
                  cursor="hand2", command=self.root.destroy
                  ).pack(fill="x", pady=7)

        tk.Button(left_panel, text="Ajouter un livre",
                  font=("Calibri", 13, "bold"), bg="#6b4226", fg="white",
                  activebackground="#5e4432", activeforeground="white",
                  bd=0, padx=18, pady=12, cursor="hand2",
                  command=self._open_add_form
                  ).pack(fill="x", pady=7)

        count_card = tk.Frame(left_panel, bg="#fffaf3", bd=1, relief="solid",
                              padx=14, pady=14)
        count_card.pack(fill="x", pady=(22, 0))

        tk.Label(count_card, text="Livres disponibles",
                 font=("Georgia", 14, "bold"), fg="#4b2e1f", bg="#fffaf3"
                 ).pack(anchor="w")

        tk.Label(count_card, textvariable=self.count_var,
                 font=("Calibri", 12, "bold"), fg="#6b4226",
                 bg="#fffaf3", pady=8).pack(anchor="w")

        tk.Label(right_panel, text="Liste des livres",
                 font=("Georgia", 16, "bold"), fg="#4b2e1f", bg="#fffaf3"
                 ).pack(anchor="w")

        tk.Label(right_panel,
                 text="Les livres enregistres s'affichent automatiquement ici.",
                 font=("Calibri", 12), fg="#6c5a4c", bg="#fffaf3"
                 ).pack(anchor="w", pady=(6, 8))

        from ui.search import SearchPanel
        self._search_panel = SearchPanel(right_panel, on_search=self._on_search_result)
        self._search_panel.pack(fill="x", pady=(0, 8))

        # ── table area ────────────────────────────────────────────────
        table_frame = tk.Frame(right_panel, bg="#f8efe3", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        self._apply_table_style()

        columns = ("id", "title", "author", "year", "isbn", "status")
        self.books_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Maktabati.Treeview",
        )

        # Column headings
        headings = {
            "id":     "ID",
            "title":  "Titre",
            "author": "Auteur",
            "year":   "Année",
            "isbn":   "ISBN",
            "status": "Statut",
        }
        widths = {
            "id":     50,
            "title":  220,
            "author": 170,
            "year":   70,
            "isbn":   140,
            "status": 100,
        }
        anchors = {
            "id":     "center",
            "title":  "w",
            "author": "w",
            "year":   "center",
            "isbn":   "center",
            "status": "center",
        }
        for col in columns:
            self.books_table.heading(col, text=headings[col])
            self.books_table.column(col, width=widths[col],
                                    anchor=anchors[col], stretch=True)

        # Vertical scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical",
                            command=self.books_table.yview)
        self.books_table.configure(yscrollcommand=vsb.set)

        self.books_table.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Row tags for striping + status colors
        self.books_table.tag_configure("odd",  background="#fffdf9")
        self.books_table.tag_configure("even", background="#f8efe3")
        self.books_table.tag_configure("borrowed", foreground="#a14b3c")
        self.books_table.tag_configure("available", foreground="#3e7c47")

        self._show_books()

    def _apply_table_style(self) -> None:
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure(
            "Maktabati.Treeview",
            background="#fffdf9",
            fieldbackground="#fffdf9",
            foreground="#3e3128",
            rowheight=28,
            font=("Calibri", 11),
            bordercolor="#e0d4c3",
            borderwidth=0,
        )
        s.configure(
            "Maktabati.Treeview.Heading",
            background="#6b4226",
            foreground="white",
            font=("Calibri", 11, "bold"),
            padding=(6, 6),
            relief="flat",
        )
        s.map(
            "Maktabati.Treeview.Heading",
            background=[("active", "#5e4432")],
        )
        s.map(
            "Maktabati.Treeview",
            background=[("selected", "#d9c4a8")],
            foreground=[("selected", "#4b2e1f")],
        )

    def _load_books(self) -> list:
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

    def _show_books(self, books: list | None = None) -> None:
        if books is None:
            books = self._load_books()

        total = len(books)
        suffix = "livre disponible" if total == 1 else "livres disponibles"
        self.count_var.set(f"{total} {suffix}")

        if self.books_table is None:
            return

        # Clear current rows
        for row in self.books_table.get_children():
            self.books_table.delete(row)

        if not books:
            return

        for index, book in enumerate(books):
            if not isinstance(book, dict):
                continue

            bid    = book.get("id", "")
            title  = book.get("title")  or book.get("titre")  or ""
            author = book.get("author") or book.get("auteur") or ""
            year   = book.get("year")   or book.get("annee")  or ""
            isbn   = book.get("isbn", "")
            status = book.get("status", "")

            stripe = "even" if index % 2 == 0 else "odd"
            status_tag = "borrowed" if str(status).lower() == "borrowed" else "available"

            self.books_table.insert(
                "", "end",
                values=(bid, title, author, year, isbn, status),
                tags=(stripe, status_tag),
            )

    def _on_search_result(self, results: list | None) -> None:
        """Called by SearchPanel: None means reset, list means filtered results."""
        self._show_books(results)

    def _open_add_form(self) -> None:
        from ui.form import BookForm
        from tkinter import Toplevel
        win = Toplevel(self.root)
        win.title("Ajouter un livre")
        win.geometry("360x220")
        win.configure(bg="#f4efe6")

        def on_success():
            self._show_books()
            if self._search_panel:
                self._search_panel.refresh()
            win.destroy()

        BookForm(win, on_success=on_success)

    def run(self) -> None:
        self.root.mainloop()


def launch_app() -> None:
    app = MaktabatiApp()
    app.run()
