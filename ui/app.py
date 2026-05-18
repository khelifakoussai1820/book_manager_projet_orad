import tkinter as tk
from tkinter import ttk

from ui.books_tab import BooksTab
from ui.students_tab import StudentsTab
from ui.borrows_tab import BorrowsTab


class MaktabatiApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Maktabati — Gestion de Bibliothèque")
        self.root.geometry("1280x760")
        self.root.minsize(1100, 680)
        self.root.configure(bg="#f4efe6")

        self._apply_style()
        self._build_header()
        self._build_body()

    def _apply_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=26, font=("Calibri", 11))
        style.configure("Treeview.Heading", font=("Calibri", 11, "bold"))
        style.configure("TNotebook", background="#f4efe6")
        style.configure("TNotebook.Tab", padding=[18, 8], font=("Calibri", 11, "bold"))

    def _build_header(self):
        header = tk.Frame(self.root, bg="#6b4226", padx=24, pady=16)
        header.pack(fill="x")
        tk.Label(
            header, text="Maktabati",
            font=("Georgia", 22, "bold"),
            fg="#fff8ef", bg="#6b4226",
        ).pack(anchor="w")
        tk.Label(
            header, text="Espace d'administration — Gestion des livres, étudiants et emprunts",
            font=("Calibri", 12), fg="#f4dfc8", bg="#6b4226",
        ).pack(anchor="w", pady=(4, 0))

    def _build_body(self):
        container = tk.Frame(self.root, bg="#f4efe6", padx=16, pady=16)
        container.pack(fill="both", expand=True)

        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)

        # Cross-refresh: each tab can refresh the others
        self.books_tab = BooksTab(notebook, app=self)
        self.students_tab = StudentsTab(notebook, app=self)
        self.borrows_tab = BorrowsTab(notebook, app=self)

        notebook.add(self.books_tab, text="📚  Gestion des livres")
        notebook.add(self.students_tab, text="👥  Gestion des étudiants")
        notebook.add(self.borrows_tab, text="🔄  Gestion des emprunts")

    def refresh_all(self):
        self.books_tab.refresh()
        self.students_tab.refresh()
        self.borrows_tab.refresh()

    def run(self):
        self.root.mainloop()
