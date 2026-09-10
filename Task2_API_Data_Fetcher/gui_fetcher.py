"""
Task 2: Professional Public API Explorer (GUI Version)
Built with Python Tkinter - Modern Asynchronous REST API Data Browser with Search, Filtering & Details Panel
"""

import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import urllib.error
import json
import threading
import time

# Theme Palette
BG_MAIN = "#0f172a"        # Slate 900
BG_CARD = "#1e293b"        # Slate 800
BG_INPUT = "#334155"       # Slate 700
ACCENT_BLUE = "#3b82f6"    # Blue 500
ACCENT_CYAN = "#06b6d4"    # Cyan 500
ACCENT_GREEN = "#10b981"   # Emerald 500
ACCENT_PURPLE = "#8b5cf6"  # Purple 500
TEXT_MAIN = "#f8fafc"      # Slate 50
TEXT_MUTED = "#94a3b8"     # Slate 400
TEXT_HIGHLIGHT = "#38bdf8" # Sky 400

API_PRODUCTS = "https://dummyjson.com/products"
API_USERS = "https://jsonplaceholder.typicode.com/users"


class APIExplorerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("REST API Data Explorer Pro | Saiket Internship")
        self.geometry("1080x720")
        self.minsize(980, 650)
        self.configure(bg=BG_MAIN)

        # Data State
        self.current_source = "products"  # 'products' or 'users'
        self.raw_data = []
        self.filtered_data = []

        self._setup_styles()
        self._build_ui()
        
        # Initial Async Fetch
        self.fetch_data_async()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Treeview',
                        background=BG_CARD,
                        foreground=TEXT_MAIN,
                        fieldbackground=BG_CARD,
                        rowheight=28,
                        font=("Segoe UI", 9))
        
        style.configure('Treeview.Heading',
                        background=BG_INPUT,
                        foreground=TEXT_MAIN,
                        font=("Segoe UI", 10, "bold"))
        
        style.map('Treeview', background=[('selected', ACCENT_BLUE)], foreground=[('selected', 'white')])

    def _build_ui(self):
        # 1. Header
        header_frame = tk.Frame(self, bg=BG_MAIN)
        header_frame.pack(fill=tk.X, padx=25, pady=(20, 10))

        title_lbl = tk.Label(
            header_frame, 
            text="🌐 REST API Data Explorer", 
            font=("Segoe UI", 20, "bold"), 
            bg=BG_MAIN, 
            fg=TEXT_MAIN
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            header_frame, 
            text="Live Public REST API Data Fetcher with multi-threading, searching, and detailed inspection", 
            font=("Segoe UI", 10), 
            bg=BG_MAIN, 
            fg=TEXT_MUTED
        )
        subtitle_lbl.pack(anchor="w", pady=(2, 0))

        # 2. Control Toolbar (API Source selector, Search Box, Refresh button)
        toolbar = tk.Frame(self, bg=BG_CARD, padx=15, pady=12, highlightbackground="#334155", highlightthickness=1)
        toolbar.pack(fill=tk.X, padx=25, pady=10)

        # API Source Toggle Buttons
        src_lbl = tk.Label(toolbar, text="Select API Source:", font=("Segoe UI", 10, "bold"), bg=BG_CARD, fg=TEXT_MUTED)
        src_lbl.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_products = tk.Button(
            toolbar, text="📦 Products Catalog", font=("Segoe UI", 9, "bold"),
            bg=ACCENT_BLUE, fg="white", bd=0, padx=12, pady=6, cursor="hand2",
            command=lambda: self.switch_source("products")
        )
        self.btn_products.pack(side=tk.LEFT, padx=3)

        self.btn_users = tk.Button(
            toolbar, text="👥 User Directory", font=("Segoe UI", 9),
            bg=BG_INPUT, fg=TEXT_MAIN, bd=0, padx=12, pady=6, cursor="hand2",
            command=lambda: self.switch_source("users")
        )
        self.btn_users.pack(side=tk.LEFT, padx=3)

        # Refresh Button
        self.refresh_btn = tk.Button(
            toolbar, text="🔄 Refresh Live API", font=("Segoe UI", 9, "bold"),
            bg=ACCENT_GREEN, fg="white", bd=0, padx=14, pady=6, cursor="hand2",
            command=self.fetch_data_async
        )
        self.refresh_btn.pack(side=tk.RIGHT, padx=(10, 0))

        # Search Bar
        search_box = tk.Frame(toolbar, bg=BG_INPUT, padx=8, pady=3)
        search_box.pack(side=tk.RIGHT, padx=5)

        tk.Label(search_box, text="🔍", bg=BG_INPUT, fg=TEXT_MUTED).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.apply_filter())
        search_entry = tk.Entry(
            search_box, textvariable=self.search_var, width=22, font=("Segoe UI", 10),
            bg=BG_INPUT, fg="white", insertbackground="white", bd=0
        )
        search_entry.pack(side=tk.LEFT, padx=5)

        # 3. Main Split View (Table on Left 65%, Details Card on Right 35%)
        split_frame = tk.Frame(self, bg=BG_MAIN)
        split_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)
        split_frame.columnconfigure(0, weight=3)
        split_frame.columnconfigure(1, weight=2)
        split_frame.rowconfigure(0, weight=1)

        # Left: Treeview Table
        table_container = tk.Frame(split_frame, bg=BG_CARD, highlightbackground="#334155", highlightthickness=1)
        table_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Scrollbar
        tree_scroll = ttk.Scrollbar(table_container)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(table_container, yscrollcommand=tree_scroll.set, selectmode="browse")
        tree_scroll.config(command=self.tree.yview)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

        # Right: Details Card
        self.details_card = tk.Frame(split_frame, bg=BG_CARD, padx=20, pady=18, highlightbackground="#334155", highlightthickness=1)
        self.details_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        tk.Label(self.details_card, text="📄 Item Inspector", font=("Segoe UI", 13, "bold"), bg=BG_CARD, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 10))

        # Details Text area (Scrollable)
        self.details_text = tk.Text(
            self.details_card, bg=BG_MAIN, fg=TEXT_MAIN, font=("Consolas", 10),
            wrap=tk.WORD, bd=0, padx=12, pady=12, highlightbackground="#334155", highlightthickness=1
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.insert(tk.END, "Select any row on the left to view detailed JSON attributes.")
        self.details_text.config(state=tk.DISABLED)

        # 4. Footer Status Bar
        self.status_bar = tk.Label(
            self, text="Ready | Saiket Systems Internship Task 2",
            font=("Segoe UI", 9), bg="#090d16", fg=TEXT_MUTED, anchor="w", padx=15, pady=6
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def switch_source(self, source: str):
        if self.current_source == source:
            return
        self.current_source = source
        self.search_var.set("")
        
        if source == "products":
            self.btn_products.config(bg=ACCENT_BLUE, fg="white", font=("Segoe UI", 9, "bold"))
            self.btn_users.config(bg=BG_INPUT, fg=TEXT_MAIN, font=("Segoe UI", 9))
        else:
            self.btn_products.config(bg=BG_INPUT, fg=TEXT_MAIN, font=("Segoe UI", 9))
            self.btn_users.config(bg=ACCENT_BLUE, fg="white", font=("Segoe UI", 9, "bold"))

        self.fetch_data_async()

    def fetch_data_async(self):
        """Spawns background thread so UI stays completely responsive during HTTP request."""
        self.status_bar.config(text="⏳ Fetching live data from REST API...", fg=TEXT_HIGHLIGHT)
        self.refresh_btn.config(state=tk.DISABLED)

        thread = threading.Thread(target=self._fetch_worker, daemon=True)
        thread.start()

    def _fetch_worker(self):
        url = API_PRODUCTS if self.current_source == "products" else API_USERS
        start_time = time.time()
        
        headers = {'User-Agent': 'Mozilla/5.0 SaiketInternship/1.0'}
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                raw = response.read().decode('utf-8')
                data = json.loads(raw)
                elapsed = (time.time() - start_time) * 1000

                if self.current_source == "products":
                    self.raw_data = data.get('products', [])
                else:
                    self.raw_data = data if isinstance(data, list) else []

                # Schedule UI update on main thread
                self.after(0, self._update_ui_with_data, elapsed)

        except Exception as e:
            self.after(0, self._handle_fetch_error, str(e))

    def _update_ui_with_data(self, elapsed_ms: float):
        self.refresh_btn.config(state=tk.NORMAL)
        self.status_bar.config(
            text=f"✅ Loaded {len(self.raw_data)} records successfully in {elapsed_ms:.1f}ms | Source: {self.current_source.capitalize()}",
            fg=ACCENT_GREEN
        )
        self._configure_columns()
        self.apply_filter()

    def _handle_fetch_error(self, err_msg: str):
        self.refresh_btn.config(state=tk.NORMAL)
        self.status_bar.config(text=f"❌ Error fetching data: {err_msg}", fg="#ef4444")
        messagebox.showerror("API Connection Error", f"Failed to fetch data from API:\n\n{err_msg}")

    def _configure_columns(self):
        # Clear existing
        self.tree.delete(*self.tree.get_children())

        if self.current_source == "products":
            self.tree['columns'] = ("ID", "Title", "Category", "Price", "Rating")
            self.tree.heading("#0", text="", anchor="w")
            self.tree.column("#0", width=0, stretch=tk.NO)

            self.tree.heading("ID", text="ID")
            self.tree.column("ID", width=45, anchor="center")

            self.tree.heading("Title", text="Product Title")
            self.tree.column("Title", width=220, anchor="w")

            self.tree.heading("Category", text="Category")
            self.tree.column("Category", width=120, anchor="w")

            self.tree.heading("Price", text="Price ($)")
            self.tree.column("Price", width=80, anchor="e")

            self.tree.heading("Rating", text="Rating")
            self.tree.column("Rating", width=70, anchor="center")

        else:
            self.tree['columns'] = ("ID", "Name", "Email", "City", "Company")
            self.tree.heading("#0", text="", anchor="w")
            self.tree.column("#0", width=0, stretch=tk.NO)

            self.tree.heading("ID", text="ID")
            self.tree.column("ID", width=45, anchor="center")

            self.tree.heading("Name", text="Full Name")
            self.tree.column("Name", width=160, anchor="w")

            self.tree.heading("Email", text="Email Address")
            self.tree.column("Email", width=180, anchor="w")

            self.tree.heading("City", text="City")
            self.tree.column("City", width=110, anchor="w")

            self.tree.heading("Company", text="Company")
            self.tree.column("Company", width=140, anchor="w")

    def apply_filter(self):
        query = self.search_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())

        if self.current_source == "products":
            for p in self.raw_data:
                title = p.get('title', '')
                category = p.get('category', '')
                if not query or query in title.lower() or query in category.lower():
                    self.tree.insert(
                        "", tk.END, iid=str(p.get('id')),
                        values=(p.get('id'), title, category, f"${p.get('price', 0):.2f}", f"★ {p.get('rating', 0)}")
                    )
        else:
            for u in self.raw_data:
                name = u.get('name', '')
                email = u.get('email', '')
                city = u.get('address', {}).get('city', '')
                company = u.get('company', {}).get('name', '')
                if not query or query in name.lower() or query in email.lower() or query in city.lower():
                    self.tree.insert(
                        "", tk.END, iid=str(u.get('id')),
                        values=(u.get('id'), name, email, city, company)
                    )

    def on_item_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        item_obj = None
        for item in self.raw_data:
            if str(item.get('id')) == str(item_id):
                item_obj = item
                break

        if item_obj:
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(tk.END, json.dumps(item_obj, indent=2))
            self.details_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = APIExplorerApp()
    app.mainloop()
