import tkinter as tk
from tkinter import ttk, messagebox
import json
import hashlib
from pathlib import Path
from datetime import date, timedelta

# ============================================================
# ANDY'S LIBRARY - Digital Library
# Single-file application: main.py
# ============================================================

APP_NAME = "Andy's Library"
DATA_FILE = Path(__file__).with_name("andys_library.json")

BG = "#f5f7fb"
SIDEBAR = "#172033"
SIDEBAR_2 = "#202b42"
CARD = "#ffffff"
TEXT = "#172033"
MUTED = "#718096"
PRIMARY = "#6c5ce7"
PRIMARY_DARK = "#5746c7"
GREEN = "#16a085"
RED = "#e74c3c"
ORANGE = "#f39c12"
BORDER = "#e6e9f0"

FONT = "Segoe UI"

DEFAULT_DATA = {
    "users": {},
    "books": [
        {"id": 1, "title": "Negeri 5 Menara", "author": "Ahmad Fuadi", "year": "2009", "stock": 4, "category": "Novel"},
        {"id": 2, "title": "Filosofi Teras", "author": "Henry Manampiring", "year": "2018", "stock": 5, "category": "Pengembangan Diri"},
        {"id": 3, "title": "The Psychology of Money", "author": "Morgan Housel", "year": "2020", "stock": 3, "category": "Keuangan"},
        {"id": 4, "title": "Bumi Manusia", "author": "Pramoedya Ananta Toer", "year": "1980", "stock": 2, "category": "Sastra"},
        {"id": 5, "title": "Atomic Habits", "author": "James Clear", "year": "2018", "stock": 6, "category": "Produktivitas"},
    ],
    "loans": []
}


def read_data():
    if not DATA_FILE.exists():
        write_data(DEFAULT_DATA)
        return json.loads(json.dumps(DEFAULT_DATA))
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError
        data.setdefault("users", {})
        data.setdefault("books", [])
        data.setdefault("loans", [])
        return data
    except (OSError, json.JSONDecodeError, ValueError):
        messagebox.showwarning(
            "Data dipulihkan",
            "File data tidak dapat dibaca. Andy's Library akan membuat data baru."
        )
        write_data(DEFAULT_DATA)
        return json.loads(json.dumps(DEFAULT_DATA))


def write_data(data):
    temp = DATA_FILE.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    temp.replace(DATA_FILE)


def password_hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def next_id(items):
    return max((int(x.get("id", 0)) for x in items), default=0) + 1


class RoundedButton(tk.Button):
    """Flat button with a simple hover effect."""
    def __init__(self, master, **kwargs):
        normal = kwargs.pop("bg", PRIMARY)
        hover = kwargs.pop("hover_bg", PRIMARY_DARK)
        super().__init__(
            master,
            bg=normal,
            activebackground=hover,
            activeforeground="white",
            fg="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(FONT, 10, "bold"),
            **kwargs
        )
        self.normal = normal
        self.hover = hover
        self.bind("<Enter>", lambda _: self.configure(bg=self.hover))
        self.bind("<Leave>", lambda _: self.configure(bg=self.normal))


class AndyLibrary(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1220x760")
        self.minsize(1050, 680)
        self.configure(bg=BG)

        self.data = read_data()
        self.current_user = None
        self.page_title = tk.StringVar(value="Dashboard")

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure(
            "Treeview",
            background=CARD,
            fieldbackground=CARD,
            foreground=TEXT,
            rowheight=34,
            font=(FONT, 10),
            borderwidth=0
        )
        self.style.configure(
            "Treeview.Heading",
            background="#eef0f7",
            foreground=TEXT,
            font=(FONT, 10, "bold"),
            padding=8
        )
        self.style.map("Treeview", background=[("selected", "#ded9ff")],
                       foreground=[("selected", TEXT)])

        self.login_screen()

    # ---------------------------- authentication ----------------------------

    def login_screen(self):
        self.login_frame = tk.Frame(self, bg=BG)
        self.login_frame.pack(fill="both", expand=True)

        left = tk.Frame(self.login_frame, bg=SIDEBAR, width=470)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(
            left, text="ANDY'S\nLIBRARY",
            bg=SIDEBAR, fg="white",
            font=(FONT, 34, "bold"), justify="left"
        ).pack(anchor="w", padx=55, pady=(130, 15))

        tk.Label(
            left,
            text="Ruang baca digital untuk\nmengelola koleksi dan peminjaman.",
            bg=SIDEBAR, fg="#cbd5e1",
            font=(FONT, 13), justify="left"
        ).pack(anchor="w", padx=55)

        tk.Label(
            left, text="BOOKS  •  PEOPLE  •  LOANS",
            bg=SIDEBAR, fg="#9fa9bd",
            font=(FONT, 9, "bold")
        ).pack(anchor="w", padx=55, pady=(35, 0))

        panel = tk.Frame(self.login_frame, bg=BG)
        panel.pack(side="right", fill="both", expand=True)

        card = tk.Frame(panel, bg=CARD, padx=46, pady=42,
                        highlightbackground=BORDER, highlightthickness=1)
        card.place(relx=.5, rely=.5, anchor="center")

        tk.Label(card, text="Selamat datang", bg=CARD, fg=TEXT,
                 font=(FONT, 25, "bold")).pack(anchor="w")
        tk.Label(card, text="Masuk untuk membuka dashboard Andy's Library.",
                 bg=CARD, fg=MUTED, font=(FONT, 10)).pack(anchor="w", pady=(5, 28))

        self.login_user = self.input_box(card, "Username")
        self.login_pass = self.input_box(card, "Password", secret=True)

        RoundedButton(card, text="Masuk ke Library", width=25,
                      command=self.do_login).pack(fill="x", pady=(8, 10), ipady=8)

        tk.Label(card, text="Belum memiliki akun?", bg=CARD, fg=MUTED,
                 font=(FONT, 9)).pack(pady=(10, 3))
        RoundedButton(card, text="Buat akun baru", width=25,
                      bg=SIDEBAR_2, hover_bg=SIDEBAR,
                      command=self.signup_dialog).pack(fill="x", ipady=6)

        self.login_pass.bind("<Return>", lambda _: self.do_login())

    def input_box(self, parent, label, secret=False):
        box = tk.Frame(parent, bg=CARD)
        box.pack(fill="x", pady=(0, 14))
        tk.Label(box, text=label, bg=CARD, fg=TEXT,
                 font=(FONT, 9, "bold")).pack(anchor="w", pady=(0, 5))
        entry = tk.Entry(
            box, width=34, font=(FONT, 11), relief="flat",
            bg="#f7f8fc", fg=TEXT, insertbackground=TEXT
        )
        entry.pack(fill="x", ipady=9)
        if secret:
            entry.configure(show="•")
        return entry

    def do_login(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get()
        record = self.data["users"].get(username)

        if not username or not password:
            messagebox.showwarning("Belum lengkap", "Username dan password wajib diisi.")
            return
        if not record or record.get("password") != password_hash(password):
            messagebox.showerror("Login gagal", "Username atau password tidak cocok.")
            return

        self.current_user = username
        self.open_app()

    def signup_dialog(self):
        win = tk.Toplevel(self)
        win.title("Daftar - Andy's Library")
        win.geometry("420x470")
        win.resizable(False, False)
        win.configure(bg=CARD)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Buat Akun", bg=CARD, fg=TEXT,
                 font=(FONT, 23, "bold")).pack(anchor="w", padx=35, pady=(30, 4))
        tk.Label(win, text="Daftarkan akun anggota baru.",
                 bg=CARD, fg=MUTED, font=(FONT, 10)).pack(anchor="w", padx=35, pady=(0, 22))

        username = self.dialog_entry(win, "Username")
        email = self.dialog_entry(win, "Email")
        password = self.dialog_entry(win, "Password", True)

        def submit():
            u, e, p = username.get().strip(), email.get().strip(), password.get()
            if not u or not e or not p:
                messagebox.showwarning("Belum lengkap", "Semua kolom harus diisi.", parent=win)
                return
            if len(p) < 6:
                messagebox.showwarning("Password", "Password minimal 6 karakter.", parent=win)
                return
            if u in self.data["users"]:
                messagebox.showerror("Gagal", "Username tersebut sudah digunakan.", parent=win)
                return
            if any(x.get("email", "").lower() == e.lower() for x in self.data["users"].values()):
                messagebox.showerror("Gagal", "Email tersebut sudah digunakan.", parent=win)
                return

            self.data["users"][u] = {"email": e, "password": password_hash(p)}
            write_data(self.data)
            messagebox.showinfo("Berhasil", "Akun berhasil dibuat.", parent=win)
            win.destroy()

        RoundedButton(win, text="Simpan akun", command=submit).pack(fill="x", padx=35, pady=24, ipady=7)

    def dialog_entry(self, parent, label, secret=False):
        wrap = tk.Frame(parent, bg=CARD)
        wrap.pack(fill="x", padx=35, pady=6)
        tk.Label(wrap, text=label, bg=CARD, fg=TEXT,
                 font=(FONT, 9, "bold")).pack(anchor="w")
        e = tk.Entry(wrap, font=(FONT, 10), relief="flat", bg="#f4f5fa")
        e.pack(fill="x", ipady=8, pady=(4, 0))
        if secret:
            e.configure(show="•")
        return e

    # ------------------------------- shell ---------------------------------

    def open_app(self):
        self.login_frame.destroy()
        self.shell = tk.Frame(self, bg=BG)
        self.shell.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.shell, bg=SIDEBAR, width=235)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR, height=92)
        brand.pack(fill="x")
        brand.pack_propagate(False)
        tk.Label(brand, text="A", bg=PRIMARY, fg="white",
                 font=(FONT, 20, "bold"), width=2, height=1).pack(
                     side="left", padx=(20, 10), pady=25)
        tk.Label(brand, text="Andy's Library", bg=SIDEBAR, fg="white",
                 font=(FONT, 14, "bold")).pack(side="left")

        tk.Label(self.sidebar, text="MENU", bg=SIDEBAR, fg="#8490a7",
                 font=(FONT, 8, "bold")).pack(anchor="w", padx=23, pady=(18, 8))

        self.nav_buttons = {}
        self.add_nav("dashboard", "▦  Dashboard", self.show_dashboard)
        self.add_nav("books", "▤  Koleksi Buku", self.show_books)
        self.add_nav("loans", "↗  Peminjaman", self.show_loans)
        self.add_nav("users", "♙  Anggota", self.show_users)

        tk.Frame(self.sidebar, bg=SIDEBAR).pack(fill="both", expand=True)

        profile = tk.Frame(self.sidebar, bg=SIDEBAR_2, padx=15, pady=14)
        profile.pack(fill="x")
        tk.Label(profile, text=self.current_user, bg=SIDEBAR_2, fg="white",
                 font=(FONT, 10, "bold")).pack(anchor="w")
        tk.Label(profile, text="Administrator / Member", bg=SIDEBAR_2,
                 fg="#9aa6bb", font=(FONT, 8)).pack(anchor="w", pady=(2, 9))
        RoundedButton(profile, text="Keluar", bg=RED, hover_bg="#c0392b",
                      command=self.logout).pack(fill="x", ipady=5)

        main = tk.Frame(self.shell, bg=BG)
        main.pack(side="right", fill="both", expand=True)

        header = tk.Frame(main, bg=CARD, height=72,
                          highlightbackground=BORDER, highlightthickness=1)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.header_title = tk.Label(header, textvariable=self.page_title,
                                     bg=CARD, fg=TEXT, font=(FONT, 20, "bold"))
        self.header_title.pack(side="left", padx=28, pady=18)

        self.header_hint = tk.Label(header, text="Andy's Library • 2026",
                                    bg=CARD, fg=MUTED, font=(FONT, 9))
        self.header_hint.pack(side="right", padx=28)

        self.workspace = tk.Frame(main, bg=BG)
        self.workspace.pack(fill="both", expand=True, padx=25, pady=24)

        self.show_dashboard()

    def add_nav(self, key, label, command):
        btn = tk.Button(
            self.sidebar, text=label, command=command,
            bg=SIDEBAR, fg="#d5dbea", activebackground=SIDEBAR_2,
            activeforeground="white", relief="flat", bd=0,
            anchor="w", padx=23, pady=13, cursor="hand2",
            font=(FONT, 10, "bold")
        )
        btn.pack(fill="x", pady=2)
        self.nav_buttons[key] = btn

    def set_active(self, key):
        for name, btn in self.nav_buttons.items():
            btn.configure(bg=SIDEBAR_2 if name == key else SIDEBAR,
                          fg="white" if name == key else "#d5dbea")

    def clear_workspace(self):
        for child in self.workspace.winfo_children():
            child.destroy()

    def logout(self):
        if messagebox.askyesno("Keluar", "Keluar dari akun sekarang?"):
            self.current_user = None
            self.shell.destroy()
            self.login_screen()

    # ------------------------------ dashboard -------------------------------

    def show_dashboard(self):
        self.clear_workspace()
        self.set_active("dashboard")
        self.page_title.set("Dashboard")

        books = self.data["books"]
        loans = self.data["loans"]
        members = self.data["users"]
        active = sum(1 for x in loans if x.get("status") == "Dipinjam")
        stock = sum(int(x.get("stock", 0)) for x in books)

        welcome = tk.Frame(self.workspace, bg=BG)
        welcome.pack(fill="x", pady=(0, 18))
        tk.Label(welcome, text=f"Halo, {self.current_user} 👋",
                 bg=BG, fg=TEXT, font=(FONT, 17, "bold")).pack(anchor="w")
        tk.Label(welcome, text="Berikut ringkasan aktivitas Andy's Library.",
                 bg=BG, fg=MUTED, font=(FONT, 10)).pack(anchor="w", pady=(3, 0))

        stats = tk.Frame(self.workspace, bg=BG)
        stats.pack(fill="x")
        self.stat_card(stats, "TOTAL BUKU", len(books), "Koleksi terdaftar", PRIMARY)
        self.stat_card(stats, "STOK TERSEDIA", stock, "Eksemplar siap dipinjam", GREEN)
        self.stat_card(stats, "SEDANG DIPINJAM", active, "Belum dikembalikan", ORANGE)
        self.stat_card(stats, "ANGGOTA", len(members), "Akun terdaftar", "#3498db")

        lower = tk.Frame(self.workspace, bg=BG)
        lower.pack(fill="both", expand=True, pady=(22, 0))

        recent_box = self.panel(lower, "Peminjaman terbaru")
        recent_box.pack(side="left", fill="both", expand=True, padx=(0, 10))

        rows = sorted(loans, key=lambda x: x.get("id", 0), reverse=True)[:6]
        if not rows:
            tk.Label(recent_box, text="Belum ada transaksi peminjaman.",
                     bg=CARD, fg=MUTED, font=(FONT, 10)).pack(pady=45)
        else:
            for loan in rows:
                row = tk.Frame(recent_box, bg=CARD)
                row.pack(fill="x", padx=18, pady=7)
                tk.Label(row, text=loan.get("title", "-"), bg=CARD, fg=TEXT,
                         font=(FONT, 10, "bold")).pack(side="left")
                tk.Label(row, text=f"{loan.get('user', '-')}  •  {loan.get('status', '-')}",
                         bg=CARD, fg=MUTED, font=(FONT, 9)).pack(side="right")

        tips = self.panel(lower, "Pusat informasi")
        tips.pack(side="right", fill="both", expand=True, padx=(10, 0))
        info = [
            ("01", "Cari buku", "Gunakan halaman Koleksi Buku untuk menemukan koleksi dengan cepat."),
            ("02", "Catat transaksi", "Tambahkan peminjaman dan stok akan disesuaikan otomatis."),
            ("03", "Kelola anggota", "Akun anggota dapat dibuat, diperbarui, atau dihapus dari menu Anggota.")
        ]
        for number, title, text in info:
            line = tk.Frame(tips, bg=CARD)
            line.pack(fill="x", padx=18, pady=8)
            tk.Label(line, text=number, bg="#ece9ff", fg=PRIMARY,
                     font=(FONT, 9, "bold"), width=4, pady=5).pack(side="left")
            body = tk.Frame(line, bg=CARD)
            body.pack(side="left", padx=10)
            tk.Label(body, text=title, bg=CARD, fg=TEXT,
                     font=(FONT, 9, "bold")).pack(anchor="w")
            tk.Label(body, text=text, bg=CARD, fg=MUTED,
                     font=(FONT, 8), wraplength=300, justify="left").pack(anchor="w", pady=(2, 0))

    def stat_card(self, parent, title, value, caption, accent):
        card = tk.Frame(parent, bg=CARD, padx=20, pady=18,
                        highlightbackground=BORDER, highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=6)
        tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y", padx=(0, 15))
        body = tk.Frame(card, bg=CARD)
        body.pack(side="left")
        tk.Label(body, text=title, bg=CARD, fg=MUTED,
                 font=(FONT, 8, "bold")).pack(anchor="w")
        tk.Label(body, text=str(value), bg=CARD, fg=TEXT,
                 font=(FONT, 25, "bold")).pack(anchor="w", pady=3)
        tk.Label(body, text=caption, bg=CARD, fg=MUTED,
                 font=(FONT, 8)).pack(anchor="w")

    def panel(self, parent, title):
        box = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        tk.Label(box, text=title, bg=CARD, fg=TEXT,
                 font=(FONT, 11, "bold")).pack(anchor="w", padx=18, pady=(16, 10))
        return box

    # -------------------------------- books --------------------------------

    def show_books(self):
        self.clear_workspace()
        self.set_active("books")
        self.page_title.set("Koleksi Buku")

        toolbar = tk.Frame(self.workspace, bg=BG)
        toolbar.pack(fill="x", pady=(0, 14))

        self.book_search = tk.StringVar()
        search = tk.Entry(toolbar, textvariable=self.book_search, width=34,
                          relief="flat", bg=CARD, fg=TEXT, font=(FONT, 10))
        search.pack(side="left", ipady=9, padx=(0, 8))
        tk.Label(toolbar, text="Cari judul, penulis, atau kategori",
                 bg=BG, fg=MUTED, font=(FONT, 9)).pack(side="left")
        RoundedButton(toolbar, text="+ Tambah Buku", command=self.book_form).pack(side="right", ipady=7)

        box = tk.Frame(self.workspace, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        box.pack(fill="both", expand=True)

        cols = ("id", "title", "author", "category", "year", "stock")
        tree = ttk.Treeview(box, columns=cols, show="headings")
        headings = {"id": "ID", "title": "Judul", "author": "Penulis",
                    "category": "Kategori", "year": "Tahun", "stock": "Stok"}
        widths = {"id": 55, "title": 280, "author": 190, "category": 160, "year": 80, "stock": 70}
        for c in cols:
            tree.heading(c, text=headings[c])
            tree.column(c, width=widths[c], anchor="center" if c in ("id", "year", "stock") else "w")

        tree.pack(fill="both", expand=True, padx=14, pady=14)
        self.book_tree = tree
        search.bind("<KeyRelease>", lambda _: self.refresh_books())
        tree.bind("<Double-1>", lambda _: self.edit_selected_book())

        actions = tk.Frame(self.workspace, bg=BG)
        actions.pack(fill="x", pady=(12, 0))
        RoundedButton(actions, text="Edit pilihan", command=self.edit_selected_book).pack(side="left", ipady=5)
        RoundedButton(actions, text="Hapus pilihan", bg=RED, hover_bg="#c0392b",
                      command=self.delete_selected_book).pack(side="left", padx=8, ipady=5)
        self.refresh_books()

    def refresh_books(self):
        if not hasattr(self, "book_tree"):
            return
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        query = getattr(self, "book_search", tk.StringVar()).get().lower().strip()
        for b in self.data["books"]:
            text = " ".join(str(b.get(k, "")) for k in ("title", "author", "category", "year")).lower()
            if query and query not in text:
                continue
            self.book_tree.insert("", "end", values=(
                b["id"], b["title"], b["author"], b["category"], b["year"], b["stock"]
            ))

    def selected_tree_id(self, tree):
        selected = tree.selection()
        if not selected:
            return None
        return int(tree.item(selected[0], "values")[0])

    def book_form(self, book=None):
        win = tk.Toplevel(self)
        win.title("Tambah Buku" if book is None else "Edit Buku")
        win.geometry("470x570")
        win.resizable(False, False)
        win.configure(bg=CARD)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Data Buku", bg=CARD, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(anchor="w", padx=35, pady=(28, 4))
        tk.Label(win, text="Lengkapi informasi koleksi.",
                 bg=CARD, fg=MUTED, font=(FONT, 9)).pack(anchor="w", padx=35, pady=(0, 18))

        fields = {}
        for key, label in [
            ("title", "Judul"), ("author", "Penulis"), ("category", "Kategori"),
            ("year", "Tahun"), ("stock", "Stok")
        ]:
            fields[key] = self.dialog_entry(win, label)
            if book:
                fields[key].insert(0, str(book.get(key, "")))

        def save():
            title = fields["title"].get().strip()
            author = fields["author"].get().strip()
            category = fields["category"].get().strip() or "Umum"
            year = fields["year"].get().strip()
            stock_text = fields["stock"].get().strip()
            if not title or not author or not year or not stock_text:
                messagebox.showwarning("Belum lengkap", "Judul, penulis, tahun, dan stok wajib diisi.", parent=win)
                return
            try:
                stock = int(stock_text)
                if stock < 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Stok", "Stok harus berupa angka 0 atau lebih.", parent=win)
                return

            if book:
                book.update(title=title, author=author, category=category, year=year, stock=stock)
            else:
                self.data["books"].append({
                    "id": next_id(self.data["books"]), "title": title,
                    "author": author, "category": category, "year": year, "stock": stock
                })
            write_data(self.data)
            self.refresh_books()
            win.destroy()

        RoundedButton(win, text="Simpan perubahan", command=save).pack(fill="x", padx=35, pady=25, ipady=7)

    def edit_selected_book(self):
        book_id = self.selected_tree_id(self.book_tree)
        if book_id is None:
            messagebox.showinfo("Pilih buku", "Pilih satu buku terlebih dahulu.")
            return
        book = next((x for x in self.data["books"] if x["id"] == book_id), None)
        if book:
            self.book_form(book)

    def delete_selected_book(self):
        book_id = self.selected_tree_id(self.book_tree)
        if book_id is None:
            messagebox.showinfo("Pilih buku", "Pilih satu buku terlebih dahulu.")
            return
        if any(x.get("book_id") == book_id and x.get("status") == "Dipinjam" for x in self.data["loans"]):
            messagebox.showwarning("Tidak dapat dihapus", "Buku masih memiliki transaksi aktif.")
            return
        if not messagebox.askyesno("Hapus buku", "Yakin ingin menghapus koleksi ini?"):
            return
        self.data["books"] = [x for x in self.data["books"] if x["id"] != book_id]
        write_data(self.data)
        self.refresh_books()

    # -------------------------------- loans ---------------------------------

    def show_loans(self):
        self.clear_workspace()
        self.set_active("loans")
        self.page_title.set("Peminjaman")

        top = tk.Frame(self.workspace, bg=BG)
        top.pack(fill="x", pady=(0, 14))
        tk.Label(top, text="Pantau semua transaksi peminjaman.",
                 bg=BG, fg=MUTED, font=(FONT, 10)).pack(side="left")
        RoundedButton(top, text="+ Transaksi Baru", command=self.loan_form).pack(side="right", ipady=7)

        box = tk.Frame(self.workspace, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        box.pack(fill="both", expand=True)

        cols = ("id", "user", "title", "borrowed", "return", "status")
        self.loan_tree = ttk.Treeview(box, columns=cols, show="headings")
        labels = ["ID", "Anggota", "Buku", "Pinjam", "Kembali", "Status"]
        widths = [55, 150, 280, 110, 110, 110]
        for c, label, width in zip(cols, labels, widths):
            self.loan_tree.heading(c, text=label)
            self.loan_tree.column(c, width=width, anchor="center" if c in ("id", "borrowed", "return", "status") else "w")
        self.loan_tree.pack(fill="both", expand=True, padx=14, pady=14)
        self.loan_tree.bind("<Double-1>", lambda _: self.edit_selected_loan())

        actions = tk.Frame(self.workspace, bg=BG)
        actions.pack(fill="x", pady=(12, 0))
        RoundedButton(actions, text="Edit transaksi", command=self.edit_selected_loan).pack(side="left", ipady=5)
        RoundedButton(actions, text="Hapus transaksi", bg=RED, hover_bg="#c0392b",
                      command=self.delete_selected_loan).pack(side="left", padx=8, ipady=5)
        self.refresh_loans()

    def refresh_loans(self):
        if not hasattr(self, "loan_tree"):
            return
        for item in self.loan_tree.get_children():
            self.loan_tree.delete(item)
        for loan in sorted(self.data["loans"], key=lambda x: x["id"], reverse=True):
            self.loan_tree.insert("", "end", values=(
                loan["id"], loan["user"], loan["title"],
                loan["borrowed"], loan["return"], loan["status"]
            ))

    def loan_form(self, loan=None):
        win = tk.Toplevel(self)
        win.title("Transaksi Peminjaman")
        win.geometry("500x580")
        win.resizable(False, False)
        win.configure(bg=CARD)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Transaksi", bg=CARD, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(anchor="w", padx=35, pady=(28, 4))
        tk.Label(win, text="Hubungkan anggota dengan koleksi buku.",
                 bg=CARD, fg=MUTED, font=(FONT, 9)).pack(anchor="w", padx=35, pady=(0, 18))

        user = self.dialog_entry(win, "Username anggota")
        if loan:
            user.insert(0, loan["user"])

        tk.Label(win, text="Buku", bg=CARD, fg=TEXT,
                 font=(FONT, 9, "bold")).pack(anchor="w", padx=35, pady=(9, 4))
        book_map = {f'{b["id"]} — {b["title"]}': b["id"] for b in self.data["books"]}
        book_combo = ttk.Combobox(win, values=list(book_map.keys()), state="readonly",
                                  font=(FONT, 10))
        book_combo.pack(fill="x", padx=35, ipady=7)
        if loan:
            for label, bid in book_map.items():
                if bid == loan["book_id"]:
                    book_combo.set(label)
                    break

        borrowed = self.dialog_entry(win, "Tanggal pinjam (YYYY-MM-DD)")
        returned = self.dialog_entry(win, "Tanggal kembali (YYYY-MM-DD)")
        status = ttk.Combobox(win, values=["Dipinjam", "Kembali"], state="readonly",
                              font=(FONT, 10))
        tk.Label(win, text="Status", bg=CARD, fg=TEXT,
                 font=(FONT, 9, "bold")).pack(anchor="w", padx=35, pady=(9, 4))
        status.pack(fill="x", padx=35, ipady=7)

        if loan:
            borrowed.insert(0, loan["borrowed"])
            returned.insert(0, loan["return"])
            status.set(loan["status"])
        else:
            today = date.today()
            borrowed.insert(0, today.isoformat())
            returned.insert(0, (today + timedelta(days=7)).isoformat())
            status.set("Dipinjam")

        def save():
            username = user.get().strip()
            selected = book_combo.get()
            if username not in self.data["users"]:
                messagebox.showwarning("Anggota", "Username belum terdaftar.", parent=win)
                return
            if not selected or not borrowed.get().strip() or not returned.get().strip():
                messagebox.showwarning("Belum lengkap", "Semua data transaksi harus diisi.", parent=win)
                return

            book_id = book_map[selected]
            book = next((b for b in self.data["books"] if b["id"] == book_id), None)
            if not book:
                return

            new_status = status.get() or "Dipinjam"

            if loan is None:
                if book["stock"] <= 0 and new_status == "Dipinjam":
                    messagebox.showwarning("Stok habis", "Tidak ada stok buku yang tersedia.", parent=win)
                    return
                item = {
                    "id": next_id(self.data["loans"]), "user": username,
                    "book_id": book_id, "title": book["title"],
                    "borrowed": borrowed.get().strip(), "return": returned.get().strip(),
                    "status": new_status
                }
                self.data["loans"].append(item)
                if new_status == "Dipinjam":
                    book["stock"] -= 1
            else:
                old_status = loan["status"]
                old_book_id = loan["book_id"]

                if old_status == "Dipinjam" and new_status == "Kembali":
                    old_book = next((b for b in self.data["books"] if b["id"] == old_book_id), None)
                    if old_book:
                        old_book["stock"] += 1
                elif old_status == "Kembali" and new_status == "Dipinjam":
                    if book["stock"] <= 0:
                        messagebox.showwarning("Stok habis", "Tidak ada stok buku yang tersedia.", parent=win)
                        return
                    book["stock"] -= 1
                elif old_status == "Dipinjam" and new_status == "Dipinjam" and old_book_id != book_id:
                    if book["stock"] <= 0:
                        messagebox.showwarning("Stok habis", "Buku baru tidak tersedia.", parent=win)
                        return
                    old_book = next((b for b in self.data["books"] if b["id"] == old_book_id), None)
                    if old_book:
                        old_book["stock"] += 1
                    book["stock"] -= 1

                loan.update({
                    "user": username,
                    "book_id": book_id,
                    "title": book["title"],
                    "borrowed": borrowed.get().strip(),
                    "return": returned.get().strip(),
                    "status": new_status
                })

            write_data(self.data)
            self.refresh_loans()
            win.destroy()

        RoundedButton(win, text="Simpan transaksi", command=save).pack(fill="x", padx=35, pady=25, ipady=7)

    def edit_selected_loan(self):
        selected = self.loan_tree.selection()
        if not selected:
            messagebox.showinfo("Pilih transaksi", "Pilih transaksi terlebih dahulu.")
            return
        loan_id = int(self.loan_tree.item(selected[0], "values")[0])
        loan = next((x for x in self.data["loans"] if x["id"] == loan_id), None)
        if loan:
            self.loan_form(loan)

    def delete_selected_loan(self):
        selected = self.loan_tree.selection()
        if not selected:
            messagebox.showinfo("Pilih transaksi", "Pilih transaksi terlebih dahulu.")
            return
        loan_id = int(self.loan_tree.item(selected[0], "values")[0])
        loan = next((x for x in self.data["loans"] if x["id"] == loan_id), None)
        if not loan:
            return
        if not messagebox.askyesno("Hapus transaksi", "Hapus transaksi ini?"):
            return
        if loan["status"] == "Dipinjam":
            book = next((b for b in self.data["books"] if b["id"] == loan["book_id"]), None)
            if book:
                book["stock"] += 1
        self.data["loans"] = [x for x in self.data["loans"] if x["id"] != loan_id]
        write_data(self.data)
        self.refresh_loans()

    # -------------------------------- users ---------------------------------

    def show_users(self):
        self.clear_workspace()
        self.set_active("users")
        self.page_title.set("Anggota Library")

        top = tk.Frame(self.workspace, bg=BG)
        top.pack(fill="x", pady=(0, 14))
        tk.Label(top, text="Daftar akun yang dapat menggunakan library.",
                 bg=BG, fg=MUTED, font=(FONT, 10)).pack(side="left")
        RoundedButton(top, text="+ Tambah Anggota", command=self.user_form).pack(side="right", ipady=7)

        box = tk.Frame(self.workspace, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        box.pack(fill="both", expand=True)

        self.user_tree = ttk.Treeview(box, columns=("username", "email"), show="headings")
        self.user_tree.heading("username", text="Username")
        self.user_tree.heading("email", text="Email")
        self.user_tree.column("username", width=240)
        self.user_tree.column("email", width=430)
        self.user_tree.pack(fill="both", expand=True, padx=14, pady=14)
        self.user_tree.bind("<Double-1>", lambda _: self.edit_selected_user())

        actions = tk.Frame(self.workspace, bg=BG)
        actions.pack(fill="x", pady=(12, 0))
        RoundedButton(actions, text="Edit anggota", command=self.edit_selected_user).pack(side="left", ipady=5)
        RoundedButton(actions, text="Hapus anggota", bg=RED, hover_bg="#c0392b",
                      command=self.delete_selected_user).pack(side="left", padx=8, ipady=5)
        self.refresh_users()

    def refresh_users(self):
        if not hasattr(self, "user_tree"):
            return
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        for username in sorted(self.data["users"]):
            self.user_tree.insert("", "end", values=(
                username, self.data["users"][username].get("email", "")
            ))

    def user_form(self, username=None):
        win = tk.Toplevel(self)
        win.title("Anggota")
        win.geometry("430x430")
        win.resizable(False, False)
        win.configure(bg=CARD)
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Profil Anggota", bg=CARD, fg=TEXT,
                 font=(FONT, 22, "bold")).pack(anchor="w", padx=35, pady=(30, 5))

        user = self.dialog_entry(win, "Username")
        email = self.dialog_entry(win, "Email")
        password = self.dialog_entry(win, "Password baru" if username else "Password", True)

        if username:
            user.insert(0, username)
            user.configure(state="disabled")
            email.insert(0, self.data["users"][username].get("email", ""))

        def save():
            u = user.get().strip()
            e = email.get().strip()
            p = password.get()
            if not u or not e:
                messagebox.showwarning("Data", "Username dan email wajib diisi.", parent=win)
                return
            if username is None:
                if not p:
                    messagebox.showwarning("Password", "Password wajib diisi.", parent=win)
                    return
                if u in self.data["users"]:
                    messagebox.showerror("Gagal", "Username sudah digunakan.", parent=win)
                    return
                self.data["users"][u] = {"email": e, "password": password_hash(p)}
            else:
                self.data["users"][username]["email"] = e
                if p:
                    self.data["users"][username]["password"] = password_hash(p)

            write_data(self.data)
            self.refresh_users()
            win.destroy()

        RoundedButton(win, text="Simpan", command=save).pack(fill="x", padx=35, pady=28, ipady=7)

    def edit_selected_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showinfo("Pilih anggota", "Pilih anggota terlebih dahulu.")
            return
        username = self.user_tree.item(selected[0], "values")[0]
        self.user_form(username)

    def delete_selected_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showinfo("Pilih anggota", "Pilih anggota terlebih dahulu.")
            return
        username = self.user_tree.item(selected[0], "values")[0]
        if username == self.current_user:
            messagebox.showwarning("Tidak diizinkan", "Akun yang sedang digunakan tidak dapat dihapus.")
            return
        if any(x.get("user") == username and x.get("status") == "Dipinjam" for x in self.data["loans"]):
            messagebox.showwarning("Tidak dapat dihapus", "Anggota masih memiliki peminjaman aktif.")
            return
        if messagebox.askyesno("Hapus anggota", f"Hapus akun '{username}'?"):
            del self.data["users"][username]
            write_data(self.data)
            self.refresh_users()


if __name__ == "__main__":
    app = AndyLibrary()
    app.mainloop()