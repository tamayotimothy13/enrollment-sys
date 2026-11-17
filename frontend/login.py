
import tkinter as tk
from tkinter import messagebox

from backend.auth import login, create_users_table
from frontend.dashboard import show_dashboard
from frontend.window import setup_window
from frontend.create_account import show_create_account


# COLORS
BG_COLOR = "#F3F6FC"
SIDEBAR_COLOR = "#172554"
PRIMARY_COLOR = "#2563EB"
WHITE = "#FFFFFF"
TEXT_COLOR = "#1E293B"
MUTED_COLOR = "#64748B"


def show_login():

    window = tk.Tk()
    setup_window(window, "Enrollment System")
    window.configure(bg=BG_COLOR)

    # ==============================
    # DATABASE INITIALIZATION
    # ==============================
    create_users_table()

    # ==============================
    # MAIN CONTENT
    # ==============================
    main = tk.Frame(
        window,
        bg=BG_COLOR
    )
    main.pack(fill="both", expand=True)

    # ==============================
    # LOGIN CONTAINER
    # ==============================
    login_frame = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )

    login_frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    # ==============================
    # HEADER
    # ==============================
    header = tk.Frame(
        login_frame,
        bg=SIDEBAR_COLOR,
        padx=35,
        pady=25
    )
    header.pack(fill="x")

    # Logo
    logo = tk.Label(
        header,
        text="ES",
        font=("Arial", 20, "bold"),
        bg=PRIMARY_COLOR,
        fg=WHITE,
        width=3,
        height=1
    )
    logo.pack(pady=(0, 12))

    # System name
    tk.Label(
        header,
        text="ENROLLMENT SYSTEM",
        font=("Arial", 16, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE
    ).pack()

    # Subtitle
    tk.Label(
        header,
        text="REGISTRAR PORTAL",
        font=("Arial", 8),
        bg=SIDEBAR_COLOR,
        fg="#BFDBFE"
    ).pack(pady=(5, 0))

    # ==============================
    # LOGIN FORM
    # ==============================
    form = tk.Frame(
        login_frame,
        bg=WHITE,
        padx=30,
        pady=25
    )
    form.pack(fill="x")

    # Welcome message
    tk.Label(
        form,
        text="Welcome Back!",
        font=("Arial", 17, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    tk.Label(
        form,
        text="Enter your username and password to continue.",
        font=("Arial", 9),
        bg=WHITE,
        fg=MUTED_COLOR
    ).pack(anchor="w", pady=(5, 20))

    # ==============================
    # USERNAME
    # ==============================
    tk.Label(
        form,
        text="Username",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    username_textbox = tk.Entry(
        form,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    username_textbox.pack(
        fill="x",
        pady=(6, 15),
        ipady=7
    )

    # ==============================
    # PASSWORD
    # ==============================
    tk.Label(
        form,
        text="Password",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    # Password container
    password_frame = tk.Frame(
        form,
        bg=WHITE,
        highlightbackground="BLACK",
        highlightthickness=1
    )

    password_frame.pack(
        fill="x",
        pady=(6, 20)
    )

    # Password textbox
    password_textbox = tk.Entry(
        password_frame,
        font=("Arial", 10),
        show="*",
        relief="flat",
        bd=0
    )

    password_textbox.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(8, 0),
        ipady=7
    )

    # ==============================
    # SHOW / HIDE PASSWORD
    # ==============================
    def toggle_password():

        if password_textbox.cget("show") == "*":

            password_textbox.config(show="")
            eye_button.config(text="◉")

        else:

            password_textbox.config(show="*")
            eye_button.config(text="⊘")

    # Eye button
    eye_button = tk.Button(
        password_frame,
        text="⊘",
        font=("Arial", 13),
        bg=WHITE,
        fg=MUTED_COLOR,
        activebackground=WHITE,
        activeforeground=PRIMARY_COLOR,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=toggle_password
    )

    eye_button.pack(
        side="right",
        padx=8
    )

    # ==============================
    # LOGIN FUNCTION
    # ==============================
    def attempt_login():

        username = username_textbox.get().strip()
        password = password_textbox.get()

        if not username or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter your username and password.",
                parent=window
            )
            return

        if login(username, password):

            window.destroy()
            show_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password.",
                parent=window
            )

    # ==============================
    # LOGIN BUTTON
    # ==============================
    login_button = tk.Button(
        form,
        text="Login",
        font=("Arial", 10, "bold"),
        bg=PRIMARY_COLOR,
        fg=WHITE,
        activebackground="#1D4ED8",
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=attempt_login
    )

    login_button.pack(
        fill="x",
        ipady=8
    )

    # ==============================
    # CREATE ACCOUNT BUTTON
    # ==============================
    create_account_button = tk.Button(
        form,
        text="Create Account",
        font=("Arial", 9, "bold"),
        bg=WHITE,
        fg=PRIMARY_COLOR,
        activebackground=WHITE,
        activeforeground="#1D4ED8",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda: show_create_account(window)
    )

    create_account_button.pack(
        fill="x",
        pady=(10, 0)
    )

    # ==============================
    # FOOTER
    # ==============================
    tk.Label(
        form,
        text="Registrar users only",
        font=("Arial", 8),
        bg=WHITE,
        fg=MUTED_COLOR
    ).pack(pady=(18, 0))

    # ==============================
    # KEYBOARD SHORTCUT
    # ==============================
    window.bind(
        "<Return>",
        lambda event: attempt_login()
    )

    username_textbox.focus_set()

    window.mainloop()


if __name__ == "__main__":
    show_login()
