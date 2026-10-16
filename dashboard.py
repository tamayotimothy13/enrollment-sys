import tkinter as tk
from frontend.window import setup_window
from frontend.student import show_students
from frontend.masterlist import show_masterlist

# COLORS
BG_COLOR = "#F3F6FC"
SIDEBAR_COLOR = "#172554"
PRIMARY_COLOR = "#2563EB"
WHITE = "#FFFFFF"
TEXT_COLOR = "#1E293B"
MUTED_COLOR = "#64748B"
RED_COLOR = "#DC2626"


def show_dashboard():
    window = tk.Tk()
    setup_window(window, "Enrollment System")

    # ==============================
    # SIDEBAR
    # ==============================
    sidebar = tk.Frame(
        window,
        bg=SIDEBAR_COLOR,
        width=190
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Logo
    logo = tk.Label(
        sidebar,
        text="ES",
        font=("Arial", 19, "bold"),
        bg=PRIMARY_COLOR,
        fg=WHITE,
        width=3,
        height=1
    )
    logo.pack(pady=(24, 8))

    system_name = tk.Label(
        sidebar,
        text="ENROLLMENT\nSYSTEM",
        font=("Arial", 11, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE,
        justify="center"
    )
    system_name.pack(pady=(0, 28))

    # Navigation design only
    def nav_button(text, command=None, active=False):
        button = tk.Button(
            sidebar,
            text=text,
            font=("Arial", 10),
            bg=PRIMARY_COLOR if active else SIDEBAR_COLOR,
            fg=WHITE,
            activebackground=PRIMARY_COLOR,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            anchor="w",
            padx=18,
            cursor="arrow",
            takefocus=False,
            command=command
        )
        button.pack(
            fill="x",
            padx=10,
            pady=4,
            ipady=7
        )

    nav_button("Dashboard", active=True)
    nav_button("Add Student(s)", show_students)
    nav_button("Enroll Student(s)")
    nav_button("View Masterlist", show_masterlist)
    nav_button("Courses")

    # Logout is the only functional button
    logout_button = tk.Button(
        sidebar,
        text="Logout",
        font=("Arial", 10),
        bg=SIDEBAR_COLOR,
        fg="#FCA5A5",
        activebackground=RED_COLOR,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        anchor="w",
        padx=18,
        cursor="hand2",
        command=window.destroy
    )
    logout_button.pack(
        side="bottom",
        fill="x",
        padx=10,
        pady=20,
        ipady=7
    )

    # ==============================
    # MAIN CONTENT
    # ==============================
    main = tk.Frame(
        window,
        bg=BG_COLOR,
        padx=24,
        pady=20
    )
    main.pack(side="left", fill="both", expand=True)

    # Header
    header = tk.Frame(main, bg=BG_COLOR)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Dashboard",
        font=("Arial", 21, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Welcome to your enrollment management system.",
        font=("Arial", 9),
        bg=BG_COLOR,
        fg=MUTED_COLOR
    ).pack(anchor="w", pady=(5, 18))

    # ==============================
    # SUMMARY CARDS
    # ==============================
    cards_frame = tk.Frame(main, bg=BG_COLOR)
    cards_frame.pack(fill="x", pady=(0, 20))

    def create_card(parent, label, number, accent):
        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        tk.Frame(
            card,
            bg=accent,
            height=4
        ).pack(fill="x")

        tk.Label(
            card,
            text=label,
            font=("Arial", 9),
            bg=WHITE,
            fg=MUTED_COLOR
        ).pack(anchor="w", padx=12, pady=(12, 4))

        tk.Label(
            card,
            text=number,
            font=("Arial", 21, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR
        ).pack(anchor="w", padx=12, pady=(0, 12))

        return card

    cards = [
        ("Students", "0", PRIMARY_COLOR),
        ("Enrollments", "0", "#0D9488"),
        ("Courses", "0", "#D97706")
    ]

    for i, (label, number, accent) in enumerate(cards):
        card = create_card(
            cards_frame,
            label,
            number,
            accent
        )

        card.grid(
            row=0,
            column=i,
            sticky="nsew",
            padx=(0 if i == 0 else 7,
                  0 if i == 2 else 7)
        )

    for i in range(3):
        cards_frame.columnconfigure(i, weight=1)

    # ==============================
    # QUICK ACTIONS - DESIGN ONLY
    # ==============================
    actions = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground="#E2E8F0",
        highlightthickness=1,
        padx=15,
        pady=12
    )
    actions.pack(fill="x")

    tk.Label(
        actions,
        text="Quick Actions",
        font=("Arial", 12, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack(anchor="w", pady=(0, 4))

    tk.Label(
        actions,
        text="Choose a task to get started.",
        font=("Arial", 9),
        bg=WHITE,
        fg=MUTED_COLOR
    ).pack(anchor="w", pady=(0, 10))

    def action_button(text, color):
        button = tk.Button(
            actions,
            text=text,
            font=("Arial", 9, "bold"),
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="arrow",
            takefocus=False
        )
        button.pack(
            fill="x",
            pady=3,
            ipady=5
        )

    action_button("Add Student(s)", PRIMARY_COLOR)
    action_button("Enroll Student(s)", "#0D9488")
    action_button("View Masterlist", "#475569")

    # Footer
    tk.Label(
        main,
        text="Enrollment System  |  Dashboard",
        font=("Arial", 8),
        bg=BG_COLOR,
        fg=MUTED_COLOR
    ).pack(side="bottom", anchor="w", pady=(12, 0))

    window.mainloop()


if __name__ == "__main__":
    show_dashboard()

show_dashboard()