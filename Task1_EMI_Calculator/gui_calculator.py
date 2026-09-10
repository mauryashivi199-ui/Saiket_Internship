"""
Task 1: Professional Loan EMI Calculator (GUI Version)
Built with Python Tkinter - Modern Fintech Theme with Sliders, Real-time Canvas Donut Chart & Breakdown
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

# Theme Palette (Modern Fintech Dark / Indigo)
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


class EMICalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Loan EMI Calculator Pro | Saiket Internship")
        self.geometry("960x700")
        self.minsize(900, 650)
        self.configure(bg=BG_MAIN)

        # State Variables
        self.principal_var = tk.DoubleVar(value=500000.0)
        self.rate_var = tk.DoubleVar(value=1.0)
        self.tenure_var = tk.IntVar(value=60)

        self._setup_styles()
        self._build_ui()
        self.calculate_and_render()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style general ttk widgets
        style.configure('TFrame', background=BG_MAIN)
        style.configure('Card.TFrame', background=BG_CARD)
        
        style.configure('Horizontal.TScale', 
                        background=BG_CARD,
                        troughcolor=BG_INPUT,
                        sliderthickness=16)

    def _build_ui(self):
        # Header
        header_frame = tk.Frame(self, bg=BG_MAIN)
        header_frame.pack(fill=tk.X, padx=30, pady=(20, 10))

        title_lbl = tk.Label(
            header_frame, 
            text="💳 Loan EMI Calculator Pro", 
            font=("Segoe UI", 22, "bold"), 
            bg=BG_MAIN, 
            fg=TEXT_MAIN
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            header_frame, 
            text="Accurate monthly EMI calculation with real-time interest & principal breakdown", 
            font=("Segoe UI", 10), 
            bg=BG_MAIN, 
            fg=TEXT_MUTED
        )
        subtitle_lbl.pack(anchor="w", pady=(2, 0))

        # Main Layout (2 Columns: Left Inputs, Right Results & Chart)
        main_content = tk.Frame(self, bg=BG_MAIN)
        main_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=15)
        main_content.columnconfigure(0, weight=1, uniform="cols")
        main_content.columnconfigure(1, weight=1, uniform="cols")
        main_content.rowconfigure(0, weight=1)

        # ------------------ LEFT PANEL (Inputs & Presets) ------------------
        left_card = tk.Frame(main_content, bg=BG_CARD, padx=25, pady=20, highlightbackground="#334155", highlightthickness=1)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        left_title = tk.Label(left_card, text="Loan Parameters", font=("Segoe UI", 14, "bold"), bg=BG_CARD, fg=TEXT_MAIN)
        left_title.pack(anchor="w", pady=(0, 15))

        # 1. Principal Amount
        self._create_input_group(
            parent=left_card,
            title="Loan Amount (Principal ₹)",
            var=self.principal_var,
            min_val=10000,
            max_val=10000000,
            is_int=False,
            prefix="₹ "
        )

        # 2. Monthly Interest Rate
        self._create_input_group(
            parent=left_card,
            title="Monthly Interest Rate (%)",
            var=self.rate_var,
            min_val=0.1,
            max_val=5.0,
            is_int=False,
            suffix=" % / mo"
        )

        # 3. Tenure in Months
        self._create_input_group(
            parent=left_card,
            title="Tenure (Months)",
            var=self.tenure_var,
            min_val=1,
            max_val=360,
            is_int=True,
            suffix=" Months"
        )

        # Presets Bar
        preset_lbl = tk.Label(left_card, text="Quick Presets:", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=TEXT_MUTED)
        preset_lbl.pack(anchor="w", pady=(15, 6))

        preset_box = tk.Frame(left_card, bg=BG_CARD)
        preset_box.pack(fill=tk.X)

        presets = [
            ("Personal Loan (₹5L, 1%, 5Y)", 500000, 1.0, 60),
            ("Car Loan (₹10L, 0.75%, 4Y)", 1000000, 0.75, 48),
            ("Home Loan (₹40L, 0.7%, 15Y)", 4000000, 0.7, 180),
        ]
        for name, p, r, t in presets:
            btn = tk.Button(
                preset_box,
                text=name,
                font=("Segoe UI", 8),
                bg=BG_INPUT,
                fg=TEXT_MAIN,
                activebackground=ACCENT_BLUE,
                activeforeground="white",
                bd=0,
                padx=8,
                pady=4,
                cursor="hand2",
                command=lambda p=p, r=r, t=t: self.set_preset(p, r, t)
            )
            btn.pack(fill=tk.X, pady=3)

        # ------------------ RIGHT PANEL (Summary Cards & Visual Chart) ------------------
        right_card = tk.Frame(main_content, bg=BG_CARD, padx=25, pady=20, highlightbackground="#334155", highlightthickness=1)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        right_title = tk.Label(right_card, text="Payment Breakdown", font=("Segoe UI", 14, "bold"), bg=BG_CARD, fg=TEXT_MAIN)
        right_title.pack(anchor="w", pady=(0, 15))

        # Big Highlight Card for Monthly EMI
        emi_card = tk.Frame(right_card, bg="#1e3a8a", padx=20, pady=15, highlightbackground=ACCENT_BLUE, highlightthickness=1)
        emi_card.pack(fill=tk.X, pady=(0, 15))

        emi_caption = tk.Label(emi_card, text="MONTHLY EMI", font=("Segoe UI", 10, "bold"), bg="#1e3a8a", fg=TEXT_HIGHLIGHT)
        emi_caption.pack(anchor="w")

        self.emi_display_lbl = tk.Label(emi_card, text="₹ 11,122.22", font=("Segoe UI", 24, "bold"), bg="#1e3a8a", fg="#ffffff")
        self.emi_display_lbl.pack(anchor="w", pady=(2, 0))

        # Secondary Summary Cards (2 Grid Columns)
        stats_frame = tk.Frame(right_card, bg=BG_CARD)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

        # Total Interest Card
        int_card = tk.Frame(stats_frame, bg=BG_INPUT, padx=12, pady=10)
        int_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        tk.Label(int_card, text="Total Interest", font=("Segoe UI", 9), bg=BG_INPUT, fg=TEXT_MUTED).pack(anchor="w")
        self.interest_display_lbl = tk.Label(int_card, text="₹ 1,67,333.43", font=("Segoe UI", 12, "bold"), bg=BG_INPUT, fg=ACCENT_CYAN)
        self.interest_display_lbl.pack(anchor="w")

        # Total Amount Card
        tot_card = tk.Frame(stats_frame, bg=BG_INPUT, padx=12, pady=10)
        tot_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        tk.Label(tot_card, text="Total Payable", font=("Segoe UI", 9), bg=BG_INPUT, fg=TEXT_MUTED).pack(anchor="w")
        self.total_display_lbl = tk.Label(tot_card, text="₹ 6,67,333.43", font=("Segoe UI", 12, "bold"), bg=BG_INPUT, fg=ACCENT_GREEN)
        self.total_display_lbl.pack(anchor="w")

        # Canvas Donut Chart for Breakdown
        self.chart_canvas = tk.Canvas(right_card, width=220, height=180, bg=BG_CARD, highlightthickness=0)
        self.chart_canvas.pack(pady=(5, 5))

        # Legend
        legend_frame = tk.Frame(right_card, bg=BG_CARD)
        legend_frame.pack()

        self._create_legend_item(legend_frame, color=ACCENT_BLUE, text="Principal Loan")
        self._create_legend_item(legend_frame, color=ACCENT_CYAN, text="Total Interest")

    def _create_legend_item(self, parent, color, text):
        box = tk.Frame(parent, bg=BG_CARD)
        box.pack(side=tk.LEFT, padx=10)
        dot = tk.Canvas(box, width=12, height=12, bg=BG_CARD, highlightthickness=0)
        dot.pack(side=tk.LEFT, padx=(0, 5))
        dot.create_oval(1, 1, 11, 11, fill=color, outline="")
        tk.Label(box, text=text, font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_MUTED).pack(side=tk.LEFT)

    def _create_input_group(self, parent, title, var, min_val, max_val, is_int=False, prefix="", suffix=""):
        group = tk.Frame(parent, bg=BG_CARD)
        group.pack(fill=tk.X, pady=(0, 12))

        top_row = tk.Frame(group, bg=BG_CARD)
        top_row.pack(fill=tk.X)

        lbl = tk.Label(top_row, text=title, font=("Segoe UI", 10), bg=BG_CARD, fg=TEXT_MAIN)
        lbl.pack(side=tk.LEFT)

        val_entry = tk.Entry(top_row, width=12, font=("Segoe UI", 10, "bold"), bg=BG_INPUT, fg=TEXT_HIGHLIGHT, insertbackground="white", bd=0, justify="right")
        val_entry.pack(side=tk.RIGHT)

        def sync_entry_from_var(*args):
            val = var.get()
            val_entry.delete(0, tk.END)
            if is_int:
                val_entry.insert(0, f"{int(val)}")
            else:
                val_entry.insert(0, f"{val:g}")

        def sync_var_from_entry(event=None):
            try:
                v = float(val_entry.get().replace(",", "").strip())
                if v >= 0:
                    var.set(int(v) if is_int else v)
                    self.calculate_and_render()
            except ValueError:
                pass

        val_entry.bind("<Return>", sync_var_from_entry)
        val_entry.bind("<FocusOut>", sync_var_from_entry)
        sync_entry_from_var()

        # Slider
        slider = ttk.Scale(
            group,
            from_=min_val,
            to=max_val,
            variable=var,
            orient=tk.HORIZONTAL,
            command=lambda v: (sync_entry_from_var(), self.calculate_and_render())
        )
        slider.pack(fill=tk.X, pady=(6, 0))

    def set_preset(self, p, r, t):
        self.principal_var.set(p)
        self.rate_var.set(r)
        self.tenure_var.set(t)
        self._build_ui_sync_refresh()
        self.calculate_and_render()

    def _build_ui_sync_refresh(self):
        # Re-trigger UI redraw
        pass

    def calculate_and_render(self):
        try:
            P = float(self.principal_var.get())
            rate_percent = float(self.rate_var.get())
            N = int(self.tenure_var.get())

            if P <= 0 or N <= 0:
                return

            r = rate_percent / 100.0

            if r == 0:
                emi = P / N
                total_payment = P
                total_interest = 0.0
            else:
                power_term = math.pow(1 + r, N)
                emi = (P * r * power_term) / (power_term - 1)
                total_payment = emi * N
                total_interest = total_payment - P

            # Update Labels
            self.emi_display_lbl.config(text=f"₹ {emi:,.2f}")
            self.interest_display_lbl.config(text=f"₹ {total_interest:,.2f}")
            self.total_display_lbl.config(text=f"₹ {total_payment:,.2f}")

            # Draw Donut Chart
            self._draw_donut_chart(P, total_interest)

        except Exception as e:
            pass

    def _draw_donut_chart(self, principal, interest):
        self.chart_canvas.delete("all")
        total = principal + interest
        if total <= 0:
            return

        principal_ratio = principal / total
        interest_ratio = interest / total

        # Angles in degrees (0 is at 3 o'clock, Tkinter measures counter-clockwise)
        principal_extent = principal_ratio * 360
        interest_extent = interest_ratio * 360

        cx, cy, r_outer, r_inner = 110, 90, 75, 45

        # Draw Outer Arcs
        # Arc 1: Principal
        self.chart_canvas.create_arc(
            cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer,
            start=90, extent=-principal_extent, fill=ACCENT_BLUE, outline=""
        )
        # Arc 2: Interest
        self.chart_canvas.create_arc(
            cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer,
            start=90 - principal_extent, extent=-interest_extent, fill=ACCENT_CYAN, outline=""
        )

        # Center Hole for Donut effect
        self.chart_canvas.create_oval(
            cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner,
            fill=BG_CARD, outline=""
        )

        # Center text (% Interest)
        int_pct = (interest / total) * 100
        self.chart_canvas.create_text(
            cx, cy - 6,
            text=f"{int_pct:.1f}%",
            fill=TEXT_MAIN,
            font=("Segoe UI", 12, "bold")
        )
        self.chart_canvas.create_text(
            cx, cy + 10,
            text="Interest",
            fill=TEXT_MUTED,
            font=("Segoe UI", 8)
        )


if __name__ == "__main__":
    app = EMICalculatorApp()
    app.mainloop()
