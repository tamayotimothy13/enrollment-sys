
import tkinter as tk

from frontend.window import setup_window
from frontend.student import show_students
from frontend.masterlist import show_masterlist
from frontend.course import show_courses
from frontend.subject import show_subjects
from frontend.enrollment import show_enrollment
from frontend.enrollment_list import show_enrollment_list

from backend.students import get_student_count
from backend.courses import get_course_count
from backend.subjects import get_subject_count


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

    # ==============================
    # DASHBOARD UPDATE FUNCTION
    # ==============================
    def update_dashboard():

        try:
            student_count = get_student_count()
            course_count = get_course_count()
            subject_count = get_subject_count()

            student_count_label.config(
                text=str(student_count)
            )

            course_label.config(
                text=str(course_count)
            )

            subject_label.config(
                text=str(subject_count)
            )

        except Exception as error:
            print("Dashboard update error:", error)

    # ==============================
    # NAVIGATION BUTTON
    # ==============================
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

    nav_button(
        "Add Student(s)",
        lambda: show_students(update_dashboard)
    )

    nav_button(
        "Enroll Student(s)",
        lambda: show_enrollment(window)
    )

    nav_button(
        "View Enrollments",
        lambda: show_enrollment_list(window)
    )

    # Masterlist
    nav_button(
        "View Masterlist",
        lambda: show_masterlist(window, update_dashboard)
    )

    # Courses
    nav_button(
        "Courses",
        lambda: show_courses(window, update_dashboard)
    )

    # Subjects
    nav_button(
        "Subjects",
        lambda: show_subjects(window, update_dashboard)
    )

    # ==============================
    # LOGOUT
    # ==============================
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
    header = tk.Frame(
        main,
        bg=BG_COLOR
    )
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
    cards_frame = tk.Frame(
        main,
        bg=BG_COLOR
    )
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
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 4)
        )

        number_label = tk.Label(
            card,
            text=number,
            font=("Arial", 21, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR
        )

        number_label.pack(
            anchor="w",
            padx=12,
            pady=(0, 12)
        )

        return card, number_label

    # Students
    student_card, student_count_label = create_card(
        cards_frame,
        "Students",
        "0",
        PRIMARY_COLOR
    )

    student_card.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 5)
    )

    # Enrollments
    enrollment_card, enrollment_label = create_card(
        cards_frame,
        "Enrollments",
        "0",
        "#0D9488"
    )

    enrollment_card.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=5
    )

    # Courses
    course_card, course_label = create_card(
        cards_frame,
        "Courses",
        "0",
        "#D97706"
    )

    course_card.grid(
        row=0,
        column=2,
        sticky="nsew",
        padx=5
    )

    # Subjects
    subject_card, subject_label = create_card(
        cards_frame,
        "Subjects",
        "0",
        "#7C3AED"
    )

    subject_card.grid(
        row=0,
        column=3,
        sticky="nsew",
        padx=(5, 0)
    )

    for i in range(4):
        cards_frame.columnconfigure(i, weight=1)

    # ==============================
    # QUICK ACTIONS
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
    ).pack(
        anchor="w",
        pady=(0, 4)
    )

    tk.Label(
        actions,
        text="Choose a task to get started.",
        font=("Arial", 9),
        bg=WHITE,
        fg=MUTED_COLOR
    ).pack(
        anchor="w",
        pady=(0, 10)
    )

    # ==============================
    # FOOTER
    # ==============================
    tk.Label(
        main,
        text="Enrollment System  |  Dashboard",
        font=("Arial", 8),
        bg=BG_COLOR,
        fg=MUTED_COLOR
    ).pack(
        side="bottom",
        anchor="w",
        pady=(12, 0)
    )

    # Initial dashboard counts
    update_dashboard()

    window.mainloop()


if __name__ == "__main__":
    show_dashboard()
