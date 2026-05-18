import tkinter as tk
from tkinter import ttk, messagebox

from logic.book import search_books, find_book
from logic.student import search_students, find_student
from logic.borrow import borrow_book, return_borrowing, get_all_borrowings


CARD_BG = "#fffaf3"
BG = "#f4efe6"
BROWN = "#6b4226"


class BorrowsTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.selected_student_id = None
        self.selected_book_id = None
        self._build()
        self.refresh()

    def _build(self):
        # Top: two search panels side by side
        top = tk.Frame(self, bg=BG, padx=12, pady=12)
        top.pack(fill="x")

        # ---- Student picker ----
        sframe = tk.LabelFrame(top, text="  Rechercher un étudiant  ",
                               bg=CARD_BG, fg=BROWN, font=("Calibri", 11, "bold"),
                               padx=10, pady=10)
        sframe.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.s_search_var = tk.StringVar()
        s_entry = tk.Entry(sframe, textvariable=self.s_search_var)
        s_entry.pack(fill="x", ipady=4)
        s_entry.bind("<KeyRelease>", lambda _: self._refresh_students())

        self.students_list = ttk.Treeview(
            sframe, columns=("id", "name", "blk"), show="headings", height=5
        )
        self.students_list.heading("id", text="ID")
        self.students_list.heading("name", text="Nom complet")
        self.students_list.heading("blk", text="Liste noire")
        self.students_list.column("id", width=50, anchor="center")
        self.students_list.column("name", width=240, anchor="w")
        self.students_list.column("blk", width=90, anchor="center")
        self.students_list.pack(fill="both", expand=True, pady=(8, 0))
        self.students_list.tag_configure("blacklisted", background="#fbe2dc")
        self.students_list.bind("<<TreeviewSelect>>", self._on_student_select)

        # ---- Book picker ----
        bframe = tk.LabelFrame(top, text="  Rechercher un livre  ",
                               bg=CARD_BG, fg=BROWN, font=("Calibri", 11, "bold"),
                               padx=10, pady=10)
        bframe.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.b_search_var = tk.StringVar()
        b_entry = tk.Entry(bframe, textvariable=self.b_search_var)
        b_entry.pack(fill="x", ipady=4)
        b_entry.bind("<KeyRelease>", lambda _: self._refresh_books())

        self.books_list = ttk.Treeview(
            bframe, columns=("id", "title", "available"), show="headings", height=5
        )
        self.books_list.heading("id", text="ID")
        self.books_list.heading("title", text="Titre")
        self.books_list.heading("available", text="Dispo.")
        self.books_list.column("id", width=50, anchor="center")
        self.books_list.column("title", width=260, anchor="w")
        self.books_list.column("available", width=70, anchor="center")
        self.books_list.pack(fill="both", expand=True, pady=(8, 0))
        self.books_list.bind("<<TreeviewSelect>>", self._on_book_select)

        # ---- Borrow action bar ----
        action = tk.Frame(self, bg=BG, padx=12, pady=4)
        action.pack(fill="x")

        self.summary_var = tk.StringVar(value="Sélectionnez un étudiant et un livre.")
        tk.Label(action, textvariable=self.summary_var,
                 bg=BG, fg=BROWN, font=("Calibri", 11, "italic")
                 ).pack(side="left")

        tk.Label(action, text="Durée (jours) :", bg=BG, fg=BROWN).pack(side="left", padx=(20, 4))
        self.duration_var = tk.StringVar(value="14")
        tk.Entry(action, textvariable=self.duration_var, width=6).pack(side="left")

        tk.Button(action, text="📖 Emprunter", command=self._do_borrow,
                  bg=BROWN, fg="white", bd=0, padx=16, pady=6, cursor="hand2"
                  ).pack(side="right", padx=4)
        tk.Button(action, text="↩️ Marquer retourné", command=self._do_return,
                  bg="#3d6b3a", fg="white", bd=0, padx=16, pady=6, cursor="hand2"
                  ).pack(side="right", padx=4)

        # ---- Borrowings list ----
        card = tk.Frame(self, bg=CARD_BG, padx=12, pady=12)
        card.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(card, text="Liste des emprunts", font=("Georgia", 14, "bold"),
                 bg=CARD_BG, fg=BROWN).pack(anchor="w", pady=(0, 8))

        columns = ("id", "student", "book", "borrow_date", "due_date", "returned_date", "status")
        self.borrows_tree = ttk.Treeview(card, columns=columns, show="headings", height=12)
        headings = {
            "id": ("ID", 50, "center"),
            "student": ("Étudiant", 180, "w"),
            "book": ("Livre", 240, "w"),
            "borrow_date": ("Date d'emprunt", 120, "center"),
            "due_date": ("Date prévue", 120, "center"),
            "returned_date": ("Date de retour", 160, "center"),
            "status": ("Statut", 110, "center"),
        }
        for col, (text, width, anchor) in headings.items():
            self.borrows_tree.heading(col, text=text)
            self.borrows_tree.column(col, width=width, anchor=anchor)

        sb = ttk.Scrollbar(card, orient="vertical", command=self.borrows_tree.yview)
        self.borrows_tree.configure(yscrollcommand=sb.set)
        self.borrows_tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.borrows_tree.tag_configure("active", background="#fff7e2")
        self.borrows_tree.tag_configure("returned", background="#e7f1e3")

    def refresh(self):
        self._refresh_students()
        self._refresh_books()
        self._refresh_borrowings()

    def _refresh_students(self):
        for row in self.students_list.get_children():
            self.students_list.delete(row)
        for s in search_students(self.s_search_var.get()):
            tags = ("blacklisted",) if s.get("blacklisted") else ()
            name = f"{s['first_name']} {s['last_name']}"
            blk = "Oui" if s.get("blacklisted") else "Non"
            self.students_list.insert("", "end", iid=str(s["id"]),
                                      values=(s["id"], name, blk), tags=tags)

    def _refresh_books(self):
        for row in self.books_list.get_children():
            self.books_list.delete(row)
        for b in search_books(self.b_search_var.get()):
            self.books_list.insert("", "end", iid=str(b["id"]),
                                   values=(b["id"], b["title"], b["available_copies"]))

    def _refresh_borrowings(self):
        for row in self.borrows_tree.get_children():
            self.borrows_tree.delete(row)
        for br in get_all_borrowings():
            returned = br.get("returned_date") or ""
            if returned:
                status = "Retourné"
                returned_display = returned
                tag = "returned"
            else:
                status = "En cours"
                returned_display = "Pas encore retourné"
                tag = "active"
            self.borrows_tree.insert("", "end", iid=str(br["id"]), values=(
                br["id"], br["student_name"], br["book_title"],
                br["borrow_date"], br["due_date"], returned_display, status,
            ), tags=(tag,))

    def _on_student_select(self, _):
        sel = self.students_list.selection()
        self.selected_student_id = sel[0] if sel else None
        self._update_summary()

    def _on_book_select(self, _):
        sel = self.books_list.selection()
        self.selected_book_id = sel[0] if sel else None
        self._update_summary()

    def _update_summary(self):
        parts = []
        if self.selected_student_id:
            s = find_student(self.selected_student_id)
            if s:
                tag = " — 🚫 LISTE NOIRE" if s.get("blacklisted") else ""
                parts.append(f"Étudiant : {s['first_name']} {s['last_name']}{tag}")
        if self.selected_book_id:
            b = find_book(self.selected_book_id)
            if b:
                parts.append(f"Livre : {b['title']} (dispo : {b['available_copies']})")
        self.summary_var.set("   |   ".join(parts) if parts else "Sélectionnez un étudiant et un livre.")

    def _do_borrow(self):
        if not self.selected_student_id or not self.selected_book_id:
            messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant ET un livre.")
            return
        try:
            duration = int(self.duration_var.get().strip() or "14")
        except ValueError:
            messagebox.showerror("Erreur", "La durée doit être un entier positif.")
            return
        try:
            borrowing = borrow_book(self.selected_student_id, self.selected_book_id, duration)
        except ValueError as exc:
            messagebox.showerror("Emprunt refusé", str(exc))
            return
        messagebox.showinfo("Succès",
                            f"Emprunt enregistré.\nRetour prévu le {borrowing['due_date']}.")
        self.app.refresh_all()

    def _do_return(self):
        sel = self.borrows_tree.selection()
        if not sel:
            messagebox.showerror("Erreur", "Veuillez sélectionner un emprunt dans la liste.")
            return
        if not return_borrowing(sel[0]):
            messagebox.showerror("Erreur", "Emprunt introuvable ou déjà retourné.")
            return
        messagebox.showinfo("Succès", "Retour enregistré.")
        self.app.refresh_all()
