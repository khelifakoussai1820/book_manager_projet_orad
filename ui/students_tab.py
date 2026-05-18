import tkinter as tk
from tkinter import ttk, messagebox

from logic.student import (
    add_student, update_student, delete_student,
    search_students, find_student, set_blacklist,
)


CARD_BG = "#fffaf3"
BG = "#f4efe6"
BROWN = "#6b4226"


class StudentsTab(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()
        self.refresh()

    def _build(self):
        top = tk.Frame(self, bg=BG, padx=12, pady=12)
        top.pack(fill="x")

        tk.Label(top, text="Rechercher :", bg=BG, fg=BROWN, font=("Calibri", 11, "bold")).pack(side="left")
        self.search_var = tk.StringVar()
        entry = tk.Entry(top, textvariable=self.search_var, width=30)
        entry.pack(side="left", padx=8, ipady=4)
        entry.bind("<KeyRelease>", lambda _: self.refresh())

        tk.Button(top, text="➕ Ajouter un étudiant", command=self._open_add,
                  bg=BROWN, fg="white", bd=0, padx=14, pady=6, cursor="hand2").pack(side="right", padx=4)
        tk.Button(top, text="✏️ Modifier", command=self._open_edit,
                  bg=BROWN, fg="white", bd=0, padx=14, pady=6, cursor="hand2").pack(side="right", padx=4)
        tk.Button(top, text="🚫 Liste noire", command=self._toggle_blacklist,
                  bg="#7a5c1c", fg="white", bd=0, padx=14, pady=6, cursor="hand2").pack(side="right", padx=4)
        tk.Button(top, text="🗑️ Supprimer", command=self._delete,
                  bg="#a8432b", fg="white", bd=0, padx=14, pady=6, cursor="hand2").pack(side="right", padx=4)

        card = tk.Frame(self, bg=CARD_BG, padx=12, pady=12)
        card.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        tk.Label(card, text="Liste des étudiants", font=("Georgia", 14, "bold"),
                 bg=CARD_BG, fg=BROWN).pack(anchor="w", pady=(0, 8))

        columns = ("id", "first_name", "last_name", "blacklisted", "reason")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=18)
        headings = {
            "id": ("ID", 60, "center"),
            "first_name": ("Prénom", 180, "w"),
            "last_name": ("Nom", 180, "w"),
            "blacklisted": ("Liste noire", 110, "center"),
            "reason": ("Raison", 400, "w"),
        }
        for col, (text, width, anchor) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor)

        sb = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.tag_configure("blacklisted", background="#fbe2dc")

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for s in search_students(self.search_var.get()):
            blocked = "Oui" if s.get("blacklisted") else "Non"
            tags = ("blacklisted",) if s.get("blacklisted") else ()
            self.tree.insert("", "end", iid=str(s["id"]),
                             values=(s["id"], s["first_name"], s["last_name"],
                                     blocked, s.get("blacklist_reason", "")),
                             tags=tags)

    def _selected_id(self):
        sel = self.tree.selection()
        return sel[0] if sel else None

    def _open_add(self):
        StudentDialog(self, title="Ajouter un étudiant", on_success=self._after_change)

    def _open_edit(self):
        sid = self._selected_id()
        if not sid:
            messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant.")
            return
        student = find_student(sid)
        if not student:
            return
        StudentDialog(self, title="Modifier l'étudiant", student=student, on_success=self._after_change)

    def _delete(self):
        sid = self._selected_id()
        if not sid:
            messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant.")
            return
        student = find_student(sid)
        if not student:
            return
        if not messagebox.askyesno("Confirmation",
                                   f"Supprimer l'étudiant {student['first_name']} {student['last_name']} ?"):
            return
        try:
            delete_student(sid)
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc))
            return
        messagebox.showinfo("Succès", "Étudiant supprimé.")
        self._after_change()

    def _toggle_blacklist(self):
        sid = self._selected_id()
        if not sid:
            messagebox.showerror("Erreur", "Veuillez sélectionner un étudiant.")
            return
        student = find_student(sid)
        if not student:
            return
        if student.get("blacklisted"):
            if messagebox.askyesno("Retirer de la liste noire",
                                   f"Retirer {student['first_name']} {student['last_name']} de la liste noire ?"):
                set_blacklist(sid, False)
                self._after_change()
        else:
            BlacklistDialog(self, student, on_success=self._after_change)

    def _after_change(self):
        self.app.refresh_all()


class StudentDialog(tk.Toplevel):
    def __init__(self, parent, title, student=None, on_success=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("380x220")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.student = student
        self.on_success = on_success
        self._build()
        self.transient(parent)
        self.grab_set()

    def _build(self):
        frm = tk.Frame(self, bg=BG, padx=18, pady=18)
        frm.pack(fill="both", expand=True)

        tk.Label(frm, text="Prénom *", bg=BG, fg=BROWN).grid(row=0, column=0, sticky="w", pady=6)
        self.first = tk.Entry(frm, width=28)
        self.first.grid(row=0, column=1, padx=(10, 0))

        tk.Label(frm, text="Nom *", bg=BG, fg=BROWN).grid(row=1, column=0, sticky="w", pady=6)
        self.last = tk.Entry(frm, width=28)
        self.last.grid(row=1, column=1, padx=(10, 0))

        if self.student:
            self.first.insert(0, self.student["first_name"])
            self.last.insert(0, self.student["last_name"])

        tk.Button(frm, text="Enregistrer", command=self._submit,
                  bg=BROWN, fg="white", bd=0, padx=18, pady=8, cursor="hand2"
                  ).grid(row=2, column=1, sticky="e", pady=(18, 0))

    def _submit(self):
        try:
            if self.student:
                update_student(self.student["id"], self.first.get(), self.last.get())
            else:
                add_student(self.first.get(), self.last.get())
        except ValueError as exc:
            messagebox.showerror("Erreur", str(exc), parent=self)
            return
        messagebox.showinfo("Succès", "Opération réussie.", parent=self)
        if self.on_success:
            self.on_success()
        self.destroy()


class BlacklistDialog(tk.Toplevel):
    def __init__(self, parent, student, on_success=None):
        super().__init__(parent)
        self.title("Ajouter à la liste noire")
        self.geometry("420x260")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.student = student
        self.on_success = on_success
        self._build()
        self.transient(parent)
        self.grab_set()

    def _build(self):
        frm = tk.Frame(self, bg=BG, padx=18, pady=18)
        frm.pack(fill="both", expand=True)

        tk.Label(frm,
                 text=f"Étudiant : {self.student['first_name']} {self.student['last_name']}",
                 bg=BG, fg=BROWN, font=("Calibri", 11, "bold")).pack(anchor="w")
        tk.Label(frm, text="Raison de la mise en liste noire :",
                 bg=BG, fg=BROWN).pack(anchor="w", pady=(12, 4))

        self.reason = tk.Text(frm, height=5, width=40)
        self.reason.pack(fill="x")

        tk.Button(frm, text="Confirmer", command=self._submit,
                  bg="#7a5c1c", fg="white", bd=0, padx=18, pady=8, cursor="hand2"
                  ).pack(anchor="e", pady=(14, 0))

    def _submit(self):
        reason = self.reason.get("1.0", "end").strip()
        if not reason:
            messagebox.showerror("Erreur", "La raison est obligatoire.", parent=self)
            return
        set_blacklist(self.student["id"], True, reason)
        messagebox.showinfo("Succès", "Étudiant ajouté à la liste noire.", parent=self)
        if self.on_success:
            self.on_success()
        self.destroy()
