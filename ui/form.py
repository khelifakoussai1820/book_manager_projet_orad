import tkinter as tk
from tkinter import messagebox

from logic.book import add_book


class BookForm:
    def __init__(self, parent, on_success=None):
        self.parent = parent
        self.on_success = on_success
        self._build()

    def _build(self):
        self.parent.configure(bg="#f4efe6", padx=12, pady=12)

        tk.Label(self.parent, text="Titre *", bg="#f4efe6").grid(row=0, column=0, sticky="w", pady=4)
        self.title = tk.Entry(self.parent, width=34)
        self.title.grid(row=0, column=1, pady=4)

        tk.Label(self.parent, text="Auteur *", bg="#f4efe6").grid(row=1, column=0, sticky="w", pady=4)
        self.author = tk.Entry(self.parent, width=34)
        self.author.grid(row=1, column=1, pady=4)

        tk.Label(self.parent, text="Année", bg="#f4efe6").grid(row=2, column=0, sticky="w", pady=4)
        self.year = tk.Entry(self.parent, width=34)
        self.year.grid(row=2, column=1, pady=4)

        tk.Label(self.parent, text="ISBN", bg="#f4efe6").grid(row=3, column=0, sticky="w", pady=4)
        self.isbn = tk.Entry(self.parent, width=34)
        self.isbn.grid(row=3, column=1, pady=4)

        tk.Button(
            self.parent,
            text="Ajouter",
            command=self.submit,
            bg="#6b4226",
            fg="white",
            bd=0,
            padx=16,
            pady=8,
        ).grid(row=4, column=1, sticky="e", pady=(12, 0))

    def submit(self):
        title = self.title.get().strip()
        author = self.author.get().strip()
        year = self.year.get().strip()
        isbn = self.isbn.get().strip()

        if not title or not author:
            messagebox.showerror("Erreur", "Le titre et l'auteur sont obligatoires.")
            return
        if year and not year.isdigit():
            messagebox.showerror("Erreur", "L'année doit être un nombre.")
            return

        add_book(title, author, year, isbn)
        messagebox.showinfo("Succès", "Livre ajouté.")
        if self.on_success:
            self.on_success()
