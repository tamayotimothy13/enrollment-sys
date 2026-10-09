import tkinter as tk
from frontend.student import show_students
from frontend.window import setup_window

def show_dashboard():

    window = tk.Tk()
    setup_window(window, "Enrollment System")

    title = tk.Label(
        window,
        text="Enrollment System",
        font=("Arial", 20)
    )
    title.pack(pady=30)

    students_button = tk.Button(
        window,
        text="Students",
        width=20,
        command=show_students
    )
    students_button.pack(pady=5)

    subjects_button = tk.Button(
        window,
        text="Subjects",
        width=20
    )
    subjects_button.pack(pady=5)

    enrollment_button = tk.Button(
        window,
        text="Enrollment",
        width=20
    )
    enrollment_button.pack(pady=5)

    logout_button = tk.Button(
        window,
        text="Logout",
        width=20
    )
    logout_button.pack(pady=20)

    window.mainloop()