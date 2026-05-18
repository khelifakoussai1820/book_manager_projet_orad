from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from logic.find import get_all_authors, get_all_years, search_books


class SearchPanel(tk.Frame):
    _ALL = "Tous"

    def __init__(self, parent: tk.Widget, on_search, include_status=False, **kwargs):
        super().__init__(parent, bg="#fffaf3", **kwargs)
        self._on_search = on_search
        self._include_status = include_status
        self._build()

    def _build(self):
        self._apply_style()
        row = tk.Frame(self, bg="#fffaf3")
        row.pack(fill="x")

        tk.Label(row, text="Recherche", bg="#fffaf3", fg="#4b2e1f").pack(side="left")
        self._query_var = tk.StringVar()
        entry = tk.Entry(row, textvariable=self._query_var, width=24)
        entry.pack(side="left", padx=(6, 12), ipady=4)
        entry.bind("<KeyRelease>", lambda _: self._search())

        tk.Label(row, text="Auteur", bg="#fffaf3", fg="#4b2e1f").pack(side="left")
        self._author_var = tk.StringVar(value=self._ALL)
        self._author_cb = ttk.Combobox(row, textvariable=self._author_var, state="readonly", width=18)
        self._author_cb.pack(side="left", padx=(6, 12))
        self._author_cb.bind("<<ComboboxSelected>>", lambda _: self._search())

        tk.Label(row, text="Année", bg="#fffaf3", fg="#4b2e1f").pack(side="left")
        self._year_var = tk.StringVar(value=self._ALL)
        self._year_cb = ttk.Combobox(row, textvariable=self._year_var, state="readonly", width=8)
        self._year_cb.pack(side="left", padx=(6, 12))
        self._year_cb.bind("<<ComboboxSelected>>", lambda _: self._search())

        if self._include_status:
            tk.Label(row, text="Statut", bg="#fffaf3", fg="#4b2e1f").pack(side="left")
            self._status_var = tk.StringVar(value=self._ALL)
            self._status_cb = ttk.Combobox(
                row,
                textvariable=self._status_var,
                state="readonly",
                width=12,
                values=[self._ALL, "available", "borrowed"],
            )
            self._status_cb.pack(side="left", padx=(6, 12))
            self._status_cb.bind("<<ComboboxSelected>>", lambda _: self._search())

        tk.Button(row, text="Réinitialiser", command=self._reset, bg="#c9b99a", bd=0).pack(side="left")
        self.refresh()

    def _apply_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

    def _search(self):
        status = ""
        if self._include_status:
            value = self._status_var.get()
            status = "" if value == self._ALL else value

        author = self._author_var.get()
        year = self._year_var.get()
        self._on_search(
            search_books(
                query=self._query_var.get(),
                author_filter="" if author == self._ALL else author,
                year_filter="" if year == self._ALL else year,
                status_filter=status,
            )
        )

    def _reset(self):
        self._query_var.set("")
        self._author_var.set(self._ALL)
        self._year_var.set(self._ALL)
        if self._include_status:
            self._status_var.set(self._ALL)
        self._on_search(None)

    def refresh(self):
        self._author_cb["values"] = [self._ALL] + get_all_authors()
        self._year_cb["values"] = [self._ALL] + get_all_years()
