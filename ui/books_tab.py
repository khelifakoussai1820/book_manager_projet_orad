import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from logic.book import add_book, update_book, delete_book, search_books, find_book


CARD_BG = "#fffaf3"
BG = "#f4efe6"
BROWN = "#6b4226"


class BooksTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()
        self.refresh()

    def _build(self):
        # Top: search + actions
        top = tk.Frame(self, bg=BG, padx=12, pady=12)
        top.pack(fill="x")

        tk.Label(top, text="Rechercher :", bg=BG, fg=BROWN, font=("Calibri", 11, "bold")).pack(side="left")
        self.search_var = tk.StringVar()
        entry = tk.Entry(top, textvariable=self.search_var, width=30)
        entry.pack(side="left", padx=8, ipady=4)
        entry.bind("<KeyRelease>", lambda _: self.refresh())

        tk.Button(top, text="➕ Ajouter un livre", command=self._open_add,
                  bg=BROWN, fg="white", bd=0, padx=14, pady=6, cursor="hand2").pack(side="right", padx=4)
        tk.Button(top, text="✏️ Modifier", command=self._open_edit,
                  bg=BROWN, fg="white", bd=0, padx=14, pady=6, cursor="hand2").pack(side="right", padx=4)
        tk.Button(top, text="🗑️ Supprimer", command=self._delete,
                  bg="#a8432b", fg="white", bd=0, padx=14, pady=6, cursor="hand2").pack(side="right", padx=4)

        # Table
        card = tk.Frame(self, bg=CARD_BG, padx=12, pady=12)
        card.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        tk.Label(card, text="Liste des livres", font=("Georgia", 14, "bold"),
                 bg=CARD_BG, fg=BROWN).pack(anchor="w", pady=(0, 8))

        columns = ("id", "title", "author", "year", "isbn", "total", "available", "status")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=18)
        headings = {
            "id": ("ID", 50, "center"),
            "title": ("Titre", 260, "w"),
            "author": ("Auteur", 180, "w"),
            "year": ("Année", 70, "center"),
            "isbn": ("ISBN", 130, "center"),
            "total": ("Copies totales", 100, "center"),
            "available": ("Copies dispo.", 100, "center"),
            "status": ("Disponibilité", 120, "center"),
        }
        for col, (text, width, anchor) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor)

        sb = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        books = search_books(self.search_var.get())
        for book in books:
            status = "Disponible" if book["available_copies"] > 0 else "Indisponible"
            self.tree.insert("", "end", iid=str(book["id"]), values=(
                book["id"], book["title"], book["author"], book["year"] or "",
                book["isbn"], book["total_copies"], book["available_copies"], status,
            ))

    def _selected_id(self):
        sel = self.tree.selection()
        return sel[0] if sel else None

    def _open_add(self):
        BookDialog(self, title="Ajouter un livre", on_success=self._after_change)

    def _open_edit(self):
        book_id = self._selected_id()
        if not book_id:
            messagebox.showerror("Erreur", "Veuillez sélectionner un livre.")
            return
        book = find_book(book_id)
        if not book:
            messagebox.showerror("Erreur", "Livre introuvable.")
            return
        BookDialog(self, title="Modifier le livre", book=book, on_success=self._after_change)

    def _delete(self):
        book_id = self._selected_id()
        if not book_id:
            messagebox.showerror("Erreur", "Veuillez sélectionner un livre.")
            return
        book = find_book(book_id)
        if not book:
            return
        if not messagebox.askyesno("Confirmation", f"Supprimer le livre « {book['title']} » ?"):
            return
        try:
            delete_book(book_id)
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc))
            return
        messagebox.showinfo("Succès", "Livre supprimé.")
        self._after_change()

    def _after_change(self):
        self.app.refresh_all()


class BookDialog(tk.Toplevel):
    def __init__(self, parent, title, book=None, on_success=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x340")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.book = book
        self.on_success = on_success
        self._build()
        self.transient(parent)
        self.grab_set()

    def _build(self):
        frm = tk.Frame(self, bg=BG, padx=18, pady=18)
        frm.pack(fill="both", expand=True)

        fields = [
            ("Titre *", "title"),
            ("Auteur *", "author"),
            ("Année", "year"),
            ("ISBN", "isbn"),
            ("Nombre de copies *", "total_copies"),
        ]
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(frm, text=label, bg=BG, fg=BROWN, font=("Calibri", 11)).grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(frm, width=30)
            entry.grid(row=i, column=1, pady=5, padx=(10, 0))
            if self.book:
                if key == "total_copies":
                    entry.insert(0, str(self.book.get("total_copies", 1)))
                else:
                    entry.insert(0, str(self.book.get(key, "") or ""))
            elif key == "total_copies":
                entry.insert(0, "1")
            self.entries[key] = entry

        tk.Button(frm, text="Enregistrer", command=self._submit,
                  bg=BROWN, fg="white", bd=0, padx=18, pady=8, cursor="hand2"
                  ).grid(row=len(fields), column=1, sticky="e", pady=(16, 0))

    def _submit(self):
        values = {k: e.get().strip() for k, e in self.entries.items()}
        try:
            if self.book:
                update_book(self.book["id"], values["title"], values["author"],
                            values["year"], values["isbn"], values["total_copies"])
            else:
                add_book(values["title"], values["author"], values["year"],
                         values["isbn"], values["total_copies"])
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc), parent=self)
            return

        messagebox.showinfo("Succès", "Opération réussie.", parent=self)
        if self.on_success:
            self.on_success()
        self.destroy()
