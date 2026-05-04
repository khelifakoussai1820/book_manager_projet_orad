import tkinter as tk
from tkinter import messagebox
from logic.book import add_book

class BookForm:
    def __init__(self, parent, on_success=None):
        self.on_success = on_success  # optional callback to refresh list

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

        # FIX: button moved to row=4 (was overlapping ISBN at row=4, col=1)
        tk.Button(parent, text="Ajouter", command=self.submit, bg="#6b4226", fg="white",
                  padx=12, pady=6).grid(row=4, column=1, sticky="e", padx=8, pady=10)

    def submit(self):
        title  = self.title.get().strip()
        author = self.author.get().strip()
        year   = self.year.get().strip()
        isbn   = self.isbn.get().strip()

        if not title or not author:
            messagebox.showerror("Erreur", "Titre et Auteur sont obligatoires !")
            return

        book = add_book(title, author, year, isbn)
        messagebox.showinfo("Succès", f"Livre '{title}' ajouté (ID: {book['id']}) !")

        # Clear fields after success
        self.title.delete(0, tk.END)
        self.author.delete(0, tk.END)
        self.year.delete(0, tk.END)
        self.isbn.delete(0, tk.END)

        if self.on_success:
            self.on_success()
