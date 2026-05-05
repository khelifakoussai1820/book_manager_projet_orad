import tkinter as tk
from tkinter import messagebox

from logic.book import update_book


class EditForm:
    def __init__(self, parent, book, on_success=None):
        self.parent = parent
        self.book_id = book["id"]
        self.on_success = on_success

        parent.configure(bg="#f4efe6")

        tk.Label(parent, text="Titre *", bg="#f4efe6").grid(
            row=0, column=0, sticky="w", padx=8, pady=4
        )
        self.title = tk.Entry(parent, width=30)
        self.title.insert(0, book.get("title", ""))
        self.title.grid(row=0, column=1, padx=8, pady=4)

        tk.Label(parent, text="Auteur *", bg="#f4efe6").grid(
            row=1, column=0, sticky="w", padx=8, pady=4
        )
        self.author = tk.Entry(parent, width=30)
        self.author.insert(0, book.get("author", ""))
        self.author.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(parent, text="Annee", bg="#f4efe6").grid(
            row=2, column=0, sticky="w", padx=8, pady=4
        )
        self.year = tk.Entry(parent, width=30)
        self.year.insert(0, book.get("year", ""))
        self.year.grid(row=2, column=1, padx=8, pady=4)

        tk.Label(parent, text="ISBN", bg="#f4efe6").grid(
            row=3, column=0, sticky="w", padx=8, pady=4
        )
        self.isbn = tk.Entry(parent, width=30)
        self.isbn.insert(0, book.get("isbn", ""))
        self.isbn.grid(row=3, column=1, padx=8, pady=4)

        tk.Label(parent, text="Statut", bg="#f4efe6").grid(
            row=4, column=0, sticky="w", padx=8, pady=4
        )
        self.status = tk.StringVar(value=book.get("status", "available"))
        tk.OptionMenu(parent, self.status, "available", "borrowed", "not available").grid(
            row=4, column=1, sticky="w", padx=8, pady=4
        )

        tk.Button(
            parent,
            text="Modifier",
            command=self.submit,
            bg="#6b4226",
            fg="white",
            padx=12,
            pady=6,
        ).grid(row=5, column=1, sticky="e", padx=8, pady=10)

    def submit(self):
        title = self.title.get().strip()
        author = self.author.get().strip()

        if not title or not author:
            messagebox.showerror("Erreur", "Titre et auteur sont obligatoires !")
            return

        updated = update_book(
            self.book_id,
            title,
            author,
            self.year.get().strip(),
            self.isbn.get().strip(),
            self.status.get(),
        )

        if not updated:
            messagebox.showerror("Erreur", "Livre introuvable.")
            return

        messagebox.showinfo("Succes", "Livre modifie !")

        if self.on_success:
            self.on_success()