import json
from pathlib import Path
import tkinter as tk


BOOKS_FILE = Path(__file__).resolve().parent.parent / "data" / "books.json"


class MaktabatiApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Maktabati")
        self.root.geometry("760x500")
        self.root.minsize(680, 440)
        self.root.configure(bg="#f4efe6")
        self.count_var = tk.StringVar(value="0 livre disponible")
        self.books_listbox: tk.Listbox | None = None

        self._build_header()
        self._build_content()

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg="#6b4226", padx=24, pady=22)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Maktabati",
            font=("Georgia", 26, "bold"),
            fg="#fff8ef",
            bg="#6b4226",
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Gestion simple et elegante de votre bibliotheque",
            font=("Calibri", 12),
            fg="#f5dfc3",
            bg="#6b4226",
        )
        subtitle.pack(anchor="w", pady=(6, 0))

    def _build_content(self) -> None:
        container = tk.Frame(self.root, bg="#f4efe6", padx=24, pady=24)
        container.pack(fill="both", expand=True)

        left_panel = tk.Frame(container, bg="#f4efe6", width=240)
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)

        right_panel = tk.Frame(
            container,
            bg="#fffaf3",
            bd=1,
            relief="solid",
            padx=18,
            pady=18,
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=(18, 0))

        section_title = tk.Label(
            left_panel,
            text="Actions principales",
            font=("Georgia", 18, "bold"),
            fg="#4b2e1f",
            bg="#f4efe6",
        )
        section_title.pack(anchor="w", pady=(0, 14))

        quit_button = tk.Button(
            left_panel,
            text="Quitter",
            font=("Calibri", 13, "bold"),
            bg="#7a5c46",
            fg="white",
            activebackground="#5e4432",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=12,
            cursor="hand2",
            command=self.root.destroy,
        )
        quit_button.pack(fill="x", pady=7)

        count_card = tk.Frame(left_panel, bg="#fffaf3", bd=1, relief="solid", padx=14, pady=14)
        count_card.pack(fill="x", pady=(22, 0))

        count_title = tk.Label(
            count_card,
            text="Livres disponibles",
            font=("Georgia", 14, "bold"),
            fg="#4b2e1f",
            bg="#fffaf3",
        )
        count_title.pack(anchor="w")

        count_value = tk.Label(
            count_card,
            textvariable=self.count_var,
            font=("Calibri", 12, "bold"),
            fg="#6b4226",
            bg="#fffaf3",
            pady=8,
        )
        count_value.pack(anchor="w")

        list_title = tk.Label(
            right_panel,
            text="Liste des livres",
            font=("Georgia", 16, "bold"),
            fg="#4b2e1f",
            bg="#fffaf3",
        )
        list_title.pack(anchor="w")

        list_subtitle = tk.Label(
            right_panel,
            text="Les livres enregistres s'affichent automatiquement ici.",
            font=("Calibri", 12),
            fg="#6c5a4c",
            bg="#fffaf3",
        )
        list_subtitle.pack(anchor="w", pady=(6, 12))

        list_frame = tk.Frame(right_panel, bg="#f8efe3", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True)

        self.books_listbox = tk.Listbox(
            list_frame,
            font=("Calibri", 12),
            bg="#fffdf9",
            fg="#3e3128",
            bd=0,
            highlightthickness=0,
        )
        self.books_listbox.pack(fill="both", expand=True)

        self._show_books()

    def _load_books(self) -> list:
        if not BOOKS_FILE.exists():
            return []

        content = BOOKS_FILE.read_text(encoding="utf-8").strip()
        if not content:
            return []

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return []

        return data if isinstance(data, list) else []

    def _show_books(self) -> None:
        books = self._load_books()
        total = len(books)
        suffix = "livre disponible" if total == 1 else "livres disponibles"
        self.count_var.set(f"{total} {suffix}")

        if self.books_listbox is None:
            return

        self.books_listbox.delete(0, tk.END)

        if not books:
            self.books_listbox.insert(tk.END, "Aucun livre enregistre pour le moment.")
            return

        for index, book in enumerate(books, start=1):
            if isinstance(book, dict):
                title = book.get("title") or book.get("titre") or f"Livre {index}"
                author = book.get("author") or book.get("auteur")
                line = f"{index}. {title}"
                if author:
                    line += f" - {author}"
            else:
                line = f"{index}. {book}"

            self.books_listbox.insert(tk.END, line)

    def run(self) -> None:
        self.root.mainloop()


def launch_app() -> None:
    app = MaktabatiApp()
    app.run()
