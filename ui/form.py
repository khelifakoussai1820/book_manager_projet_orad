import tkinter as tk
from tkinter import messagebox
from logic.book import add_book

class BookForm:
    def __init__(self, parent, on_success=None):
        self.on_success = on_success

        tk.Label(parent, text="Titre *").grid(row=0, column=0, sticky="w", padx=8, pady=4)
        self.title = tk.Entry(parent, width=30)
        self.title.grid(row=0, column=1, padx=8, pady=4)

        tk.Label(parent, text="Auteur *").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        self.author = tk.Entry(parent, width=30)
        self.author.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(parent, text="Année").grid(row=2, column=0, sticky="w", padx=8, pady=4)
        self.year = tk.Entry(parent, width=30)
        self.year.grid(row=2, column=1, padx=8, pady=4)

        tk.Label(parent, text="ISBN").grid(row=3, column=0, sticky="w", padx=8, pady=4)
        self.isbn = tk.Entry(parent, width=30)
        self.isbn.grid(row=3, column=1, padx=8, pady=4)

        tk.Button(parent, text="Ajouter", command=self.submit, bg="#6b4226", fg="white",
                  padx=12, pady=6).grid(row=4, column=1, sticky="e", padx=8, pady=10)

    def submit(self):
        title  = self.title.get().strip()
        author = self.author.get().strip()
        year   = self.year.get().strip()
        isbn   = self.isbn.get().strip()

        if not title or not author:
            messagebox.showerror("Erreur", "Le titre et l'auteur sont obligatoires.")
            return

        if year and not year.isdigit():
            messagebox.showerror("Erreur", "L'année doit être un nombre (ex: 2024) !")
            return

        try:
            add_book(title, author, year, isbn)
            self.clear_form()
            if self.on_success:
                self.on_success()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")

    def clear_form(self):  # ✅ DANS la classe, bien indenté
        self.title.delete(0, tk.END)
        self.author.delete(0, tk.END)
        self.year.delete(0, tk.END)
        self.isbn.delete(0, tk.END)