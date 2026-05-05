"""ui/search.py — search bar + author/year filters, embeds above the book list."""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from logic.find import search_books, get_all_authors, get_all_years


class SearchPanel(tk.Frame):
    _ALL = "Tous"

    def __init__(self, parent: tk.Widget, on_search, **kw) -> None:
        super().__init__(parent, bg="#fffaf3", **kw)
        self._on_search = on_search
        self._build()

    def _build(self) -> None:
        self._apply_combobox_style()

        row = tk.Frame(self, bg="#fffaf3")
        row.pack(fill="x")

        # ── keyword entry ──────────────────────────────────────────────────
        tk.Label(row, text="Titre :", font=("Calibri", 11),
                 fg="#4b2e1f", bg="#fffaf3").pack(side="left")

        self._query_var = tk.StringVar()
        entry = tk.Entry(row, textvariable=self._query_var,
                         font=("Calibri", 12), bg="#fffdf9", fg="#3e3128",
                         relief="solid", bd=1, width=28,
                         highlightthickness=1, highlightcolor="#6b4226",
                         insertbackground="#3e3128",
                         )
        entry.pack(side="left", padx=(4, 14), ipady=5)
        # live search on every keystroke + Enter
        entry.bind("<KeyRelease>", lambda _: self._search())
        entry.bind("<Return>", lambda _: self._search())

        # ── author dropdown ────────────────────────────────────────────────
        tk.Label(row, text="Auteur :", font=("Calibri", 11),
                 fg="#4b2e1f", bg="#fffaf3").pack(side="left")

        self._author_var = tk.StringVar(value=self._ALL)
        self._author_cb = ttk.Combobox(row, textvariable=self._author_var,
                                       font=("Calibri", 11), state="readonly", width=16,
                                       )
        self._author_cb.pack(side="left", padx=(4, 14), ipady=4)
        # live search when dropdown selection changes
        self._author_cb.bind("<<ComboboxSelected>>", lambda _: self._search())

        # ── year dropdown ──────────────────────────────────────────────────
        tk.Label(row, text="Année :", font=("Calibri", 11),
                 fg="#4b2e1f", bg="#fffaf3").pack(side="left")

        self._year_var = tk.StringVar(value=self._ALL)
        self._year_cb = ttk.Combobox(row, textvariable=self._year_var,
                                     font=("Calibri", 11), state="readonly", width=7,
                                     )
        self._year_cb.pack(side="left", padx=(4, 14), ipady=4)
        # live search when dropdown selection changes
        self._year_cb.bind("<<ComboboxSelected>>", lambda _: self._search())

        # ── buttons ────────────────────────────────────────────────────────
        tk.Button(row, text="🔍",
                  font=("Calibri", 12), bg="#6b4226", fg="white",
                  activebackground="#5e4432", bd=0,
                  padx=10, pady=4, cursor="hand2", command=self._search,
                  ).pack(side="left", padx=(0, 4))

        tk.Button(row, text="Réinitialiser",
                  font=("Calibri", 11), bg="#c9b99a", fg="#4b2e1f",
                  activebackground="#b5a488", bd=0,
                  padx=8, pady=4, cursor="hand2", command=self._reset,
                  ).pack(side="left")

        self.refresh()

    def _apply_combobox_style(self) -> None:
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TCombobox",
                    fieldbackground="#fffdf9", background="#fffdf9",
                    foreground="#3e3128", selectbackground="#d9c4a8",
                    selectforeground="#4b2e1f", bordercolor="#e0d4c3",
                    arrowcolor="#6b4226",
                    )

    def _search(self) -> None:
        author = self._author_var.get()
        year = self._year_var.get()
        self._on_search(search_books(
            query=self._query_var.get(),
            author_filter="" if author == self._ALL else author,
            year_filter="" if year == self._ALL else year,
        ))

    def _reset(self) -> None:
        self._query_var.set("")
        self._author_var.set(self._ALL)
        self._year_var.set(self._ALL)
        self._on_search(None)

    def refresh(self) -> None:
        self._author_cb["values"] = [self._ALL] + get_all_authors()
        self._year_cb["values"] = [self._ALL] + get_all_years()