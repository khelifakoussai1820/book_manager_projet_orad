import tkinter as tk
from tkinter import messagebox, ttk

from logic.book import delete_book, find_book
from logic.borrow import borrow_book, get_all_borrowings, get_blacklisted_students, get_student_borrowings, return_book
from logic.storage import load_books
from logic.student import find_student, upsert_student
from ui.edit_form import EditForm
from ui.form import BookForm
from ui.search import SearchPanel


class MaktabatiApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Maktabati")
        self.root.geometry("1280x760")
        self.root.minsize(1100, 680)
        self.root.configure(bg="#f4efe6")

        self.admin_books = []
        self.student_books = []
        self.current_student = None

        self.student_id_var = tk.StringVar()
        self.student_first_name_var = tk.StringVar()
        self.student_last_name_var = tk.StringVar()
        self.borrow_duration_var = tk.StringVar(value="14")
        self.student_info_var = tk.StringVar(value="Aucun étudiant chargé.")

        self._build_header()
        self._build_body()
        self.refresh_all_views()

    def _build_header(self):
        header = tk.Frame(self.root, bg="#6b4226", padx=24, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Maktabati",
            font=("Georgia", 24, "bold"),
            fg="#fff8ef",
            bg="#6b4226",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Bibliothèque desktop avec rôles Admin et Étudiant",
            font=("Calibri", 12),
            fg="#f4dfc8",
            bg="#6b4226",
        ).pack(anchor="w", pady=(4, 0))

    def _build_body(self):
        self._apply_tree_style()

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=16, pady=16)

        self.admin_tab = tk.Frame(notebook, bg="#f4efe6")
        self.student_tab = tk.Frame(notebook, bg="#f4efe6")
        notebook.add(self.admin_tab, text="Admin")
        notebook.add(self.student_tab, text="Étudiant")

        self._build_admin_tab()
        self._build_student_tab()

    def _apply_tree_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=28, font=("Calibri", 11))
        style.configure("Treeview.Heading", font=("Calibri", 11, "bold"))

    def _build_admin_tab(self):
        left = tk.Frame(self.admin_tab, bg="#f4efe6", padx=10, pady=10)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(self.admin_tab, bg="#f4efe6", padx=10, pady=10, width=360)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        books_card = self._create_card(left, "Catalogue des livres")
        self.admin_search = SearchPanel(books_card, on_search=self._show_admin_books, include_status=True)
        self.admin_search.pack(fill="x", pady=(0, 10))

        self.admin_books_tree = self._create_tree(
            books_card,
            ("id", "title", "author", "year", "isbn", "status"),
            {
                "id": ("ID", 55, "center"),
                "title": ("Titre", 260, "w"),
                "author": ("Auteur", 180, "w"),
                "year": ("Année", 80, "center"),
                "isbn": ("ISBN", 150, "center"),
                "status": ("Statut", 100, "center"),
            },
            height=12,
        )
        self.admin_books_tree.pack(fill="both", expand=True)

        books_actions = tk.Frame(books_card, bg="#fffaf3")
        books_actions.pack(fill="x", pady=(10, 0))
        self._action_button(books_actions, "Ajouter", self._open_add_form).pack(side="left", padx=(0, 8))
        self._action_button(books_actions, "Modifier", self._open_selected_book).pack(side="left", padx=8)
        self._action_button(books_actions, "Supprimer", self._delete_selected_book).pack(side="left", padx=8)

        borrowings_card = self._create_card(left, "Suivi des emprunts")
        self.borrowings_tree = self._create_tree(
            borrowings_card,
            ("id", "student_id", "student_name", "book_title", "borrow_date", "due_date", "status"),
            {
                "id": ("ID", 50, "center"),
                "student_id": ("ID étudiant", 100, "center"),
                "student_name": ("Nom étudiant", 180, "w"),
                "book_title": ("Livre", 220, "w"),
                "borrow_date": ("Emprunt", 100, "center"),
                "due_date": ("Retour prévu", 110, "center"),
                "status": ("Statut", 90, "center"),
            },
            height=10,
        )
        self.borrowings_tree.pack(fill="both", expand=True)

        borrowing_actions = tk.Frame(borrowings_card, bg="#fffaf3")
        borrowing_actions.pack(fill="x", pady=(10, 0))
        self._action_button(borrowing_actions, "Marquer comme retourné", self._return_selected_borrowing).pack(side="left")

        summary_card = self._create_card(right, "Administration")
        self.admin_counts_var = tk.StringVar(value="")
        tk.Label(
            summary_card,
            textvariable=self.admin_counts_var,
            justify="left",
            anchor="w",
            bg="#fffaf3",
            fg="#4b2e1f",
            font=("Calibri", 12),
        ).pack(fill="x")

        blacklist_card = self._create_card(right, "Liste noire")
        self.blacklist_tree = self._create_tree(
            blacklist_card,
            ("student_id", "student_name", "late_books"),
            {
                "student_id": ("ID", 90, "center"),
                "student_name": ("Étudiant", 150, "w"),
                "late_books": ("Livres en retard", 320, "w"),
            },
            height=18,
        )
        self.blacklist_tree.pack(fill="both", expand=True)

    def _build_student_tab(self):
        left = tk.Frame(self.student_tab, bg="#f4efe6", padx=10, pady=10, width=320)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        right = tk.Frame(self.student_tab, bg="#f4efe6", padx=10, pady=10)
        right.pack(side="right", fill="both", expand=True)

        profile_card = self._create_card(left, "Profil étudiant")
        self._labeled_entry(profile_card, "ID étudiant", self.student_id_var)
        self._labeled_entry(profile_card, "Prénom", self.student_first_name_var)
        self._labeled_entry(profile_card, "Nom", self.student_last_name_var)
        self._labeled_entry(profile_card, "Durée (jours)", self.borrow_duration_var)

        actions = tk.Frame(profile_card, bg="#fffaf3")
        actions.pack(fill="x", pady=(10, 0))
        self._action_button(actions, "Charger / enregistrer", self._load_or_create_student).pack(side="left")

        tk.Label(
            profile_card,
            textvariable=self.student_info_var,
            bg="#fffaf3",
            fg="#4b2e1f",
            justify="left",
            wraplength=250,
        ).pack(fill="x", pady=(12, 0))

        books_card = self._create_card(right, "Livres disponibles pour l'étudiant")
        self.student_search = SearchPanel(books_card, on_search=self._show_student_books, include_status=True)
        self.student_search.pack(fill="x", pady=(0, 10))

        self.student_books_tree = self._create_tree(
            books_card,
            ("id", "title", "author", "year", "isbn", "status"),
            {
                "id": ("ID", 55, "center"),
                "title": ("Titre", 250, "w"),
                "author": ("Auteur", 180, "w"),
                "year": ("Année", 80, "center"),
                "isbn": ("ISBN", 150, "center"),
                "status": ("Statut", 100, "center"),
            },
            height=10,
        )
        self.student_books_tree.pack(fill="both", expand=True)

        student_actions = tk.Frame(books_card, bg="#fffaf3")
        student_actions.pack(fill="x", pady=(10, 0))
        self._action_button(student_actions, "Emprunter le livre sélectionné", self._borrow_selected_book).pack(side="left")

        my_borrowings_card = self._create_card(right, "Mes emprunts")
        self.student_borrowings_tree = self._create_tree(
            my_borrowings_card,
            ("id", "book_title", "borrow_date", "due_date", "status"),
            {
                "id": ("ID", 50, "center"),
                "book_title": ("Livre", 320, "w"),
                "borrow_date": ("Emprunt", 110, "center"),
                "due_date": ("Retour prévu", 120, "center"),
                "status": ("Statut", 90, "center"),
            },
            height=8,
        )
        self.student_borrowings_tree.pack(fill="both", expand=True)

    def _create_card(self, parent, title):
        card = tk.Frame(parent, bg="#fffaf3", bd=1, relief="solid", padx=12, pady=12)
        card.pack(fill="both", expand=True, pady=(0, 12))
        tk.Label(card, text=title, font=("Georgia", 14, "bold"), bg="#fffaf3", fg="#4b2e1f").pack(anchor="w", pady=(0, 8))
        return card

    def _create_tree(self, parent, columns, column_config, height=10):
        frame = tk.Frame(parent, bg="#fffaf3")
        frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(frame, columns=columns, show="headings", height=height)
        for column in columns:
            heading, width, anchor = column_config[column]
            tree.heading(column, text=heading)
            tree.column(column, width=width, anchor=anchor, stretch=anchor == "w")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return tree

    def _action_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#6b4226",
            fg="white",
            activebackground="#5e4432",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
        )

    def _labeled_entry(self, parent, label, variable):
        tk.Label(parent, text=label, bg="#fffaf3", fg="#4b2e1f").pack(anchor="w", pady=(6, 2))
        tk.Entry(parent, textvariable=variable).pack(fill="x")

    def refresh_all_views(self):
        self._show_admin_books()
        self._show_student_books()
        self._refresh_borrowings()
        self._refresh_blacklist()
        self._refresh_student_borrowings()

        books = load_books()
        borrowings = get_all_borrowings()
        blacklisted = get_blacklisted_students()
        self.admin_counts_var.set(
            f"Livres: {len(books)}\n"
            f"Emprunts actifs: {len([item for item in borrowings if item['status'] != 'returned'])}\n"
            f"Étudiants en liste noire: {len(blacklisted)}"
        )

        self.admin_search.refresh()
        self.student_search.refresh()

    def _fill_books_tree(self, tree, books):
        for row in tree.get_children():
            tree.delete(row)
        for book in books:
            tree.insert(
                "",
                "end",
                iid=str(book["id"]),
                values=(
                    book["id"],
                    book["title"],
                    book["author"],
                    book["year"],
                    book["isbn"],
                    book["status"],
                ),
            )

    def _show_admin_books(self, books=None):
        if books is None:
            books = load_books()
        self.admin_books = books
        self._fill_books_tree(self.admin_books_tree, books)

    def _show_student_books(self, books=None):
        if books is None:
            books = load_books()
        self.student_books = books
        self._fill_books_tree(self.student_books_tree, books)

    def _refresh_borrowings(self):
        for row in self.borrowings_tree.get_children():
            self.borrowings_tree.delete(row)
        for borrowing in get_all_borrowings():
            status = borrowing["status"]
            if borrowing["is_late"] and status != "returned":
                status = "late"
            self.borrowings_tree.insert(
                "",
                "end",
                iid=borrowing["id"],
                values=(
                    borrowing["id"],
                    borrowing["student_id"],
                    borrowing["student_name"],
                    borrowing["book_title"],
                    borrowing["borrow_date"],
                    borrowing["due_date"],
                    status,
                ),
            )

    def _refresh_blacklist(self):
        for row in self.blacklist_tree.get_children():
            self.blacklist_tree.delete(row)
        for student in get_blacklisted_students():
            books_text = ", ".join(
                f"{item['book_title']} ({item['due_date']})" for item in student["late_books"]
            )
            self.blacklist_tree.insert(
                "",
                "end",
                iid=student["student_id"],
                values=(student["student_id"], student["student_name"], books_text),
            )

    def _refresh_student_borrowings(self):
        for row in self.student_borrowings_tree.get_children():
            self.student_borrowings_tree.delete(row)

        if not self.current_student:
            return

        for borrowing in get_student_borrowings(self.current_student["student_id"]):
            status = borrowing["status"]
            if borrowing["is_late"] and status != "returned":
                status = "late"
            self.student_borrowings_tree.insert(
                "",
                "end",
                iid=borrowing["id"],
                values=(
                    borrowing["id"],
                    borrowing["book_title"],
                    borrowing["borrow_date"],
                    borrowing["due_date"],
                    status,
                ),
            )

    def _open_add_form(self):
        win = tk.Toplevel(self.root)
        win.title("Ajouter un livre")
        win.geometry("420x240")

        def on_success():
            win.destroy()
            self.refresh_all_views()

        BookForm(win, on_success=on_success)

    def _open_selected_book(self):
        selected = self.admin_books_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un livre à modifier.")
            return

        book = find_book(selected[0])
        if not book:
            messagebox.showerror("Erreur", "Livre introuvable.")
            return

        win = tk.Toplevel(self.root)
        win.title("Modifier un livre")
        win.geometry("420x240")

        def on_success():
            win.destroy()
            self.refresh_all_views()

        EditForm(win, book, on_success=on_success)

    def _delete_selected_book(self):
        selected = self.admin_books_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un livre à supprimer.")
            return

        book = find_book(selected[0])
        if not book:
            messagebox.showerror("Erreur", "Livre introuvable.")
            return

        if not messagebox.askyesno("Confirmation", f"Supprimer '{book['title']}' ?"):
            return

        try:
            deleted = delete_book(book["id"])
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc))
            return

        if deleted:
            messagebox.showinfo("Succès", "Livre supprimé.")
            self.refresh_all_views()

    def _return_selected_borrowing(self):
        selected = self.borrowings_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un emprunt.")
            return

        if not return_book(selected[0]):
            messagebox.showerror("Erreur", "Emprunt introuvable ou déjà retourné.")
            return

        messagebox.showinfo("Succès", "Retour enregistré.")
        self.refresh_all_views()

    def _load_or_create_student(self):
        student_id = self.student_id_var.get().strip()
        first_name = self.student_first_name_var.get().strip()
        last_name = self.student_last_name_var.get().strip()

        try:
            student = upsert_student(student_id, first_name, last_name)
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc))
            return

        self.current_student = student
        fresh_student = find_student(student["student_id"]) or student
        self.current_student = fresh_student
        self.student_info_var.set(
            f"Étudiant chargé : {fresh_student['first_name']} {fresh_student['last_name']}\n"
            f"ID : {fresh_student['student_id']}\n"
            f"Livres empruntés : {len(fresh_student.get('borrowed_book_ids', []))}"
        )
        self._refresh_student_borrowings()
        self.refresh_all_views()

    def _borrow_selected_book(self):
        selected = self.student_books_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Sélectionnez un livre à emprunter.")
            return

        student_id = self.student_id_var.get().strip()
        first_name = self.student_first_name_var.get().strip()
        last_name = self.student_last_name_var.get().strip()
        duration = self.borrow_duration_var.get().strip() or "14"

        if not duration.isdigit() or int(duration) <= 0:
            messagebox.showerror("Erreur", "La durée d'emprunt doit être un nombre positif.")
            return

        try:
            borrowing = borrow_book(student_id, first_name, last_name, selected[0], int(duration))
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc))
            return

        self.current_student = find_student(student_id)
        messagebox.showinfo(
            "Succès",
            f"Emprunt enregistré.\nRetour prévu le {borrowing['due_date']}.",
        )
        self.refresh_all_views()

    def run(self):
        self.root.mainloop()


def launch_app():
    app = MaktabatiApp()
    app.run()
