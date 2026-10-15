import tkinter as tk
from tkinter import ttk
from frontend.window import setup_window


def show_masterlist():

    window = tk.Tk()
    setup_window(window, "Student Masterlist")

    # Colors
    BG_COLOR = "#F3F6FC"
    PRIMARY_COLOR = "#2563EB"
    WHITE = "#FFFFFF"
    TEXT_COLOR = "#1E293B"
    MUTED_COLOR = "#64748B"
    RED_COLOR = "#DC2626"

    window.configure(bg=BG_COLOR)

    # =========================
    # HEADER
    # =========================
    header = tk.Frame(window, bg=WHITE, height=90)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Student Masterlist",
        font=("Arial", 22, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=25, pady=(15, 0))

    tk.Label(
        header,
        text="View and manage student records",
        font=("Arial", 10),
        bg=WHITE,
        fg=MUTED_COLOR
    ).pack(anchor="w", padx=27, pady=3)

    # =========================
    # MAIN CONTENT
    # =========================
    content = tk.Frame(window, bg=BG_COLOR)
    content.pack(fill="both", expand=True, padx=25, pady=20)

    # Search section
    search_frame = tk.Frame(content, bg=BG_COLOR)
    search_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        search_frame,
        text="Students",
        font=("Arial", 15, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(side="left")

    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 10),
        width=25,
        relief="solid",
        bd=1
    )
    search_entry.pack(side="right", ipady=6)

    search_button = tk.Button(
        search_frame,
        text="Search",
        font=("Arial", 10, "bold"),
        bg=PRIMARY_COLOR,
        fg=WHITE,
        activebackground=PRIMARY_COLOR,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        padx=15
    )
    search_button.pack(side="right", padx=8, ipady=4)

    # =========================
    # TABLE CARD
    # =========================
    table_card = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    table_card.pack(fill="both", expand=True)

    columns = (
        "student_id",
        "first_name",
        "last_name",
        "course",
        "year_level",
        "email"
    )

    tree = ttk.Treeview(
        table_card,
        columns=columns,
        show="headings",
        height=10
    )

    tree.heading("student_id", text="Student ID")
    tree.heading("first_name", text="First Name")
    tree.heading("last_name", text="Last Name")
    tree.heading("course", text="Course")
    tree.heading("year_level", text="Year Level")
    tree.heading("email", text="Email")

    tree.column("student_id", width=100, anchor="center")
    tree.column("first_name", width=120)
    tree.column("last_name", width=120)
    tree.column("course", width=130)
    tree.column("year_level", width=90, anchor="center")
    tree.column("email", width=180)

    scrollbar = ttk.Scrollbar(
        table_card,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=10
    )
    scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

    # =========================
    # EMPTY STATE
    # =========================
    # No student records are loaded yet.
    # The message is shown while the table is empty.
    empty_label = tk.Label(
        table_card,
        text="No students found.",
        font=("Arial", 14, "bold"),
        bg=WHITE,
        fg=MUTED_COLOR
    )
    empty_label.place(relx=0.5, rely=0.5, anchor="center")

    # =========================
    # ACTION BUTTONS
    # =========================
    actions = tk.Frame(content, bg=BG_COLOR)
    actions.pack(fill="x", pady=(15, 0))

    tk.Button(
        actions,
        text="View Details",
        width=14,
        font=("Arial", 10, "bold"),
        bg="#0F766E",
        fg=WHITE,
        relief="flat",
        cursor="hand2"
    ).pack(side="left", padx=(0, 8), ipady=5)

    tk.Button(
        actions,
        text="Edit Student",
        width=14,
        font=("Arial", 10, "bold"),
        bg=PRIMARY_COLOR,
        fg=WHITE,
        relief="flat",
        cursor="hand2"
    ).pack(side="left", padx=8, ipady=5)

    tk.Button(
        actions,
        text="Delete Student",
        width=14,
        font=("Arial", 10, "bold"),
        bg=RED_COLOR,
        fg=WHITE,
        relief="flat",
        cursor="hand2"
    ).pack(side="left", padx=8, ipady=5)

    tk.Button(
        actions,
        text="Back",
        width=12,
        font=("Arial", 10, "bold"),
        bg="#E2E8F0",
        fg=TEXT_COLOR,
        relief="flat",
        cursor="hand2",
        command=window.destroy
    ).pack(side="right", ipady=5)

    window.mainloop()


if __name__ == "__main__":
    show_masterlist()