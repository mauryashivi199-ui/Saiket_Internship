"""
Task 3: Professional Blog Application (Desktop GUI)
Built with Python Tkinter - Modern Editorial / Medium Theme with Persistent Local JSON Storage & Full CRUD
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

BG_MAIN = "#0f172a"        # Slate 900
BG_CARD = "#1e293b"        # Slate 800
BG_INPUT = "#334155"       # Slate 700
ACCENT_BLUE = "#3b82f6"    # Blue 500
ACCENT_CYAN = "#06b6d4"    # Cyan 500
ACCENT_GREEN = "#10b981"   # Emerald 500
ACCENT_RED = "#ef4444"     # Red 500
TEXT_MAIN = "#f8fafc"      # Slate 50
TEXT_MUTED = "#94a3b8"     # Slate 400
TEXT_HIGHLIGHT = "#38bdf8" # Sky 400

DATA_FILE = os.path.join(os.path.dirname(__file__), "blog_data.json")

INITIAL_SAMPLE_POSTS = [
    {
        "id": 1,
        "title": "Mastering Python & Modern Backend Architecture",
        "author": "Shivangi Maurya",
        "category": "Technology",
        "content": "Python is a powerhouse for modern backend systems, automation, and AI integrations. With clean syntax and massive library ecosystems, building scalable applications has never been easier.",
        "date": "2026-09-15 10:30",
        "likes": 15
    },
    {
        "id": 2,
        "title": "Why Local Storage & Offline-First Apps Matter",
        "author": "Tech Insights",
        "category": "Web Dev",
        "content": "Local Storage allows applications to save user state and documents directly on the device. Even without an active internet connection, users can read, edit, and create content seamlessly.",
        "date": "2026-09-18 14:20",
        "likes": 9
    },
    {
        "id": 3,
        "title": "5 Tips for Cracking Internship Coding Interviews",
        "author": "Career Hub",
        "category": "Career",
        "content": "Focus on fundamentals: understand the underlying data structures, explain time complexity clearly, build real working projects, and always follow clean code practices.",
        "date": "2026-09-19 08:00",
        "likes": 24
    }
]


class BlogAppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DevBlog Pro | Saiket Internship Task 3")
        self.geometry("1080x720")
        self.minsize(960, 640)
        self.configure(bg=BG_MAIN)

        self.posts = self.load_data()
        self.selected_post_id = None

        self._setup_styles()
        self._build_ui()
        self.refresh_posts_list()

        # Select first post if available
        if self.posts:
            self.select_post(self.posts[0]["id"])

    def load_data(self) -> list[dict]:
        if not os.path.exists(DATA_FILE):
            self.save_data(INITIAL_SAMPLE_POSTS)
            return INITIAL_SAMPLE_POSTS.copy()
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return INITIAL_SAMPLE_POSTS.copy()

    def save_data(self, posts_to_save: list[dict]):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(posts_to_save, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save to local storage: {e}")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=BG_MAIN)

    def _build_ui(self):
        # 1. Header
        header = tk.Frame(self, bg=BG_MAIN, padx=25, pady=15)
        header.pack(fill=tk.X)

        h_left = tk.Frame(header, bg=BG_MAIN)
        h_left.pack(side=tk.LEFT)

        tk.Label(h_left, text="📝 DevBlog Studio", font=("Segoe UI", 20, "bold"), bg=BG_MAIN, fg=TEXT_MAIN).pack(anchor="w")
        tk.Label(h_left, text="Simple Blog App with Local Storage (CRUD) • Task 3", font=("Segoe UI", 9), bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")

        # Action Buttons Header
        h_right = tk.Frame(header, bg=BG_MAIN)
        h_right.pack(side=tk.RIGHT)

        tk.Button(
            h_right, text="✍️ New Post", font=("Segoe UI", 10, "bold"),
            bg=ACCENT_BLUE, fg="white", bd=0, padx=14, pady=6, cursor="hand2",
            command=self.open_new_post_dialog
        ).pack(side=tk.LEFT, padx=5)

        # 2. Main Layout (Left Feed 40%, Right Reader/Editor 60%)
        main_box = tk.Frame(self, bg=BG_MAIN, padx=25, pady=5)
        main_box.pack(fill=tk.BOTH, expand=True)
        main_box.columnconfigure(0, weight=4)
        main_box.columnconfigure(1, weight=6)
        main_box.rowconfigure(0, weight=1)

        # Left Column: Post Feed & Search
        left_panel = tk.Frame(main_box, bg=BG_CARD, padx=15, pady=15, highlightbackground="#334155", highlightthickness=1)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Search Bar
        search_box = tk.Frame(left_panel, bg=BG_INPUT, padx=8, pady=4)
        search_box.pack(fill=tk.X, pady=(0, 10))

        tk.Label(search_box, text="🔍", bg=BG_INPUT, fg=TEXT_MUTED).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_posts_list())
        search_entry = tk.Entry(search_box, textvariable=self.search_var, bg=BG_INPUT, fg="white", bd=0, font=("Segoe UI", 10))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Posts Listbox
        list_frame = tk.Frame(left_panel, bg=BG_CARD)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.posts_listbox = tk.Listbox(
            list_frame, bg=BG_CARD, fg=TEXT_MAIN, selectbackground=ACCENT_BLUE,
            selectforeground="white", bd=0, font=("Segoe UI", 10),
            yscrollcommand=scrollbar.set, activestyle="none", highlightthickness=0
        )
        self.posts_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.posts_listbox.yview)
        self.posts_listbox.bind("<<ListboxSelect>>", self.on_post_selected)

        # Left Footer: Stats
        self.stats_lbl = tk.Label(left_panel, text="3 Posts saved locally", font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_MUTED)
        self.stats_lbl.pack(anchor="w", pady=(8, 0))

        # Right Column: Post Reader / Inspector
        self.right_panel = tk.Frame(main_box, bg=BG_CARD, padx=25, pady=20, highlightbackground="#334155", highlightthickness=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Article Header (Category, Title, Metadata, Actions)
        self.article_category_lbl = tk.Label(self.right_panel, text="TECHNOLOGY", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=ACCENT_CYAN)
        self.article_category_lbl.pack(anchor="w")

        self.article_title_lbl = tk.Label(self.right_panel, text="Select an article to read", font=("Segoe UI", 16, "bold"), bg=BG_CARD, fg=TEXT_MAIN, wraplength=520, justify="left")
        self.article_title_lbl.pack(anchor="w", pady=(4, 6))

        # Meta Bar (Author, Date, Likes, Edit/Delete buttons)
        meta_bar = tk.Frame(self.right_panel, bg=BG_CARD)
        meta_bar.pack(fill=tk.X, pady=(0, 15))

        self.article_meta_lbl = tk.Label(meta_bar, text="By Shivangi Maurya • 2026-09-15", font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_MUTED)
        self.article_meta_lbl.pack(side=tk.LEFT)

        # Action Buttons
        self.btn_like = tk.Button(
            meta_bar, text="❤️ Like (15)", font=("Segoe UI", 8, "bold"),
            bg=BG_INPUT, fg="#f43f5e", bd=0, padx=10, pady=3, cursor="hand2",
            command=self.like_current_post
        )
        self.btn_like.pack(side=tk.RIGHT, padx=3)

        self.btn_delete = tk.Button(
            meta_bar, text="🗑️ Delete", font=("Segoe UI", 8),
            bg=BG_INPUT, fg=ACCENT_RED, bd=0, padx=8, pady=3, cursor="hand2",
            command=self.delete_current_post
        )
        self.btn_delete.pack(side=tk.RIGHT, padx=3)

        self.btn_edit = tk.Button(
            meta_bar, text="✏️ Edit", font=("Segoe UI", 8),
            bg=BG_INPUT, fg=TEXT_MAIN, bd=0, padx=8, pady=3, cursor="hand2",
            command=self.edit_current_post
        )
        self.btn_edit.pack(side=tk.RIGHT, padx=3)

        # Content Reader Area
        self.content_text = tk.Text(
            self.right_panel, bg=BG_MAIN, fg=TEXT_MAIN, font=("Segoe UI", 11),
            wrap=tk.WORD, bd=0, padx=15, pady=15, highlightbackground="#334155", highlightthickness=1
        )
        self.content_text.pack(fill=tk.BOTH, expand=True)

        # 3. Status Bar
        self.status_bar = tk.Label(
            self, text="Local Storage Synced (blog_data.json) | Saiket Internship Task 3",
            font=("Segoe UI", 9), bg="#090d16", fg=TEXT_MUTED, anchor="w", padx=20, pady=5
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def refresh_posts_list(self):
        query = self.search_var.get().strip().lower()
        self.posts_listbox.delete(0, tk.END)
        
        self.filtered_ids = []
        for p in self.posts:
            title = p.get("title", "")
            category = p.get("category", "")
            if not query or query in title.lower() or query in category.lower():
                self.filtered_ids.append(p["id"])
                self.posts_listbox.insert(tk.END, f"  [{category.upper()}]  {title}")

        total_likes = sum(p.get("likes", 0) for p in self.posts)
        self.stats_lbl.config(text=f"{len(self.posts)} Posts • {total_likes} Total Likes (Local Storage)")

    def on_post_selected(self, event):
        selection = self.posts_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        if idx < len(self.filtered_ids):
            post_id = self.filtered_ids[idx]
            self.select_post(post_id)

    def select_post(self, post_id: int):
        post = next((p for p in self.posts if p["id"] == post_id), None)
        if not post:
            return
        self.selected_post_id = post_id

        self.article_category_lbl.config(text=post.get("category", "GENERAL").upper())
        self.article_title_lbl.config(text=post.get("title", "Untitled"))
        self.article_meta_lbl.config(text=f"By {post.get('author', 'Anonymous')} • 📅 {post.get('date', 'Recent')}")
        self.btn_like.config(text=f"❤️ Like ({post.get('likes', 0)})")

        self.content_text.delete("1.0", tk.END)
        self.content_text.insert(tk.END, post.get("content", ""))

    def like_current_post(self):
        if not self.selected_post_id:
            return
        post = next((p for p in self.posts if p["id"] == self.selected_post_id), None)
        if post:
            post["likes"] = post.get("likes", 0) + 1
            self.save_data(self.posts)
            self.btn_like.config(text=f"❤️ Like ({post['likes']})")
            self.refresh_posts_list()

    def delete_current_post(self):
        if not self.selected_post_id:
            return
        post = next((p for p in self.posts if p["id"] == self.selected_post_id), None)
        if not post:
            return

        if messagebox.askyesno("Delete Post", f"Are you sure you want to delete:\n'{post['title']}'?"):
            self.posts = [p for p in self.posts if p["id"] != self.selected_post_id]
            self.save_data(self.posts)
            self.selected_post_id = None
            self.refresh_posts_list()
            if self.posts:
                self.select_post(self.posts[0]["id"])
            else:
                self.article_title_lbl.config(text="No blog posts available")
                self.content_text.delete("1.0", tk.END)

    def open_new_post_dialog(self):
        self._post_form_modal("Create New Post", on_submit=self._create_post_callback)

    def edit_current_post(self):
        if not self.selected_post_id:
            return
        post = next((p for p in self.posts if p["id"] == self.selected_post_id), None)
        if not post:
            return
        self._post_form_modal("Edit Post", initial=post, on_submit=self._edit_post_callback)

    def _post_form_modal(self, modal_title, initial=None, on_submit=None):
        win = tk.Toplevel(self)
        win.title(modal_title)
        win.geometry("540x580")
        win.configure(bg=BG_MAIN)
        win.transient(self)
        win.grab_set()

        pad = 15
        f = tk.Frame(win, bg=BG_MAIN, padx=pad, pady=pad)
        f.pack(fill=tk.BOTH, expand=True)

        tk.Label(f, text=modal_title, font=("Segoe UI", 14, "bold"), bg=BG_MAIN, fg=TEXT_MAIN).pack(anchor="w", pady=(0, 10))

        # Title
        tk.Label(f, text="Title", font=("Segoe UI", 9, "bold"), bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")
        t_entry = tk.Entry(f, bg=BG_INPUT, fg="white", font=("Segoe UI", 10), insertbackground="white", bd=0)
        t_entry.pack(fill=tk.X, pady=(2, 10), ipady=4)
        if initial:
            t_entry.insert(0, initial.get("title", ""))

        # Category & Author in 2 columns
        grid_f = tk.Frame(f, bg=BG_MAIN)
        grid_f.pack(fill=tk.X, pady=(0, 10))
        grid_f.columnconfigure(0, weight=1)
        grid_f.columnconfigure(1, weight=1)

        c_box = tk.Frame(grid_f, bg=BG_MAIN)
        c_box.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        tk.Label(c_box, text="Category", font=("Segoe UI", 9, "bold"), bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")
        c_entry = tk.Entry(c_box, bg=BG_INPUT, fg="white", font=("Segoe UI", 10), bd=0)
        c_entry.pack(fill=tk.X, ipady=4)
        c_entry.insert(0, initial.get("category", "Tech") if initial else "Technology")

        a_box = tk.Frame(grid_f, bg=BG_MAIN)
        a_box.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        tk.Label(a_box, text="Author", font=("Segoe UI", 9, "bold"), bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")
        a_entry = tk.Entry(a_box, bg=BG_INPUT, fg="white", font=("Segoe UI", 10), bd=0)
        a_entry.pack(fill=tk.X, ipady=4)
        a_entry.insert(0, initial.get("author", "Shivangi Maurya") if initial else "Shivangi Maurya")

        # Content
        tk.Label(f, text="Post Content", font=("Segoe UI", 9, "bold"), bg=BG_MAIN, fg=TEXT_MUTED).pack(anchor="w")
        c_text = tk.Text(f, bg=BG_INPUT, fg="white", font=("Segoe UI", 10), bd=0, height=10, insertbackground="white")
        c_text.pack(fill=tk.BOTH, expand=True, pady=(2, 12))
        if initial:
            c_text.insert("1.0", initial.get("content", ""))

        def submit():
            t = t_entry.get().strip()
            cat = c_entry.get().strip()
            auth = a_entry.get().strip()
            body = c_text.get("1.0", tk.END).strip()
            if not t or not body:
                messagebox.showwarning("Validation", "Title and content cannot be empty.")
                return
            if on_submit:
                on_submit(t, cat, auth, body, win)

        tk.Button(
            f, text="💾 Save to Local Storage", font=("Segoe UI", 10, "bold"),
            bg=ACCENT_GREEN, fg="white", bd=0, pady=8, cursor="hand2",
            command=submit
        ).pack(fill=tk.X)

    def _create_post_callback(self, title, category, author, content, modal):
        next_id = max([p["id"] for p in self.posts], default=0) + 1
        new_item = {
            "id": next_id,
            "title": title,
            "author": author or "Shivangi Maurya",
            "category": category or "General",
            "content": content,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "likes": 0
        }
        self.posts.insert(0, new_item)
        self.save_data(self.posts)
        self.refresh_posts_list()
        self.select_post(next_id)
        modal.destroy()
        messagebox.showinfo("Success", "New Blog Post saved to Local Storage!")

    def _edit_post_callback(self, title, category, author, content, modal):
        post = next((p for p in self.posts if p["id"] == self.selected_post_id), None)
        if post:
            post["title"] = title
            post["category"] = category
            post["author"] = author
            post["content"] = content
            self.save_data(self.posts)
            self.refresh_posts_list()
            self.select_post(post["id"])
            modal.destroy()
            messagebox.showinfo("Updated", "Post updated in Local Storage!")


if __name__ == "__main__":
    app = BlogAppGUI()
    app.mainloop()
