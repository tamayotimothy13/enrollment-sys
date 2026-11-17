
import tkinter as tk
from tkinter import messagebox

from backend.auth import register


# COLORS
BG_COLOR = "#F3F6FC"
SIDEBAR_COLOR = "#172554"
PRIMARY_COLOR = "#2563EB"
WHITE = "#FFFFFF"
TEXT_COLOR = "#1E293B"
MUTED_COLOR = "#64748B"


def show_create_account(parent):

    # ==============================
    # CREATE ACCOUNT WINDOW
    # ==============================
    window = tk.Toplevel(parent)
    window.title("Create Account")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)

    # CENTER WINDOW
    width = 450
    height = 650

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

    window.transient(parent)
    window.grab_set()

    # ==============================
    # MAIN CONTENT
    # ==============================
    main = tk.Frame(
        window,
        bg=BG_COLOR
    )
    main.pack(fill="both", expand=True)

    # ==============================
    # CREATE ACCOUNT CONTAINER
    # ==============================
    account_frame = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )

    account_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # ==============================
    # HEADER
    # ==============================
    header = tk.Frame(
        account_frame,
        bg=SIDEBAR_COLOR,
        padx=25,
        pady=20
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
    logo.pack(pady=(0, 10))

    # System name
    tk.Label(
        header,
        text="CREATE ACCOUNT",
        font=("Arial", 15, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE
    ).pack()

    # Subtitle
    tk.Label(
        header,
        text="REGISTER A NEW REGISTRAR ACCOUNT",
        font=("Arial", 8),
        bg=SIDEBAR_COLOR,
        fg="#BFDBFE"
    ).pack(pady=(5, 0))

    # ==============================
    # REGISTRATION FORM
    # ==============================
    form = tk.Frame(
        account_frame,
        bg=WHITE,
        padx=25,
        pady=20
    )
    form.pack(fill="both", expand=True)

    # Welcome message
    tk.Label(
        form,
        text="Get Started!",
        font=("Arial", 17, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    tk.Label(
        form,
        text="Create your registrar account below.",
        font=("Arial", 9),
        bg=WHITE,
        fg=MUTED_COLOR
    ).pack(anchor="w", pady=(5, 15))

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

    username_entry = tk.Entry(
        form,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    username_entry.pack(
        fill="x",
        pady=(6, 12),
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

    password_entry = tk.Entry(
        form,
        font=("Arial", 10),
        show="*",
        relief="solid",
        bd=1
    )

    password_entry.pack(
        fill="x",
        pady=(6, 12),
        ipady=7
    )

    # ==============================
    # CONFIRM PASSWORD
    # ==============================
    tk.Label(
        form,
        text="Confirm Password",
        font=("Arial", 10, "bold"),
        bg=WHITE,
        fg=TEXT_COLOR
    ).pack(anchor="w")

    confirm_password_entry = tk.Entry(
        form,
        font=("Arial", 10),
        show="*",
        relief="solid",
        bd=1
    )

    confirm_password_entry.pack(
        fill="x",
        pady=(6, 18),
        ipady=7
    )

    # ==============================
    # SHOW / HIDE PASSWORD
    # ==============================
    def toggle_password():

        if password_entry.cget("show") == "*":

            password_entry.config(show="")
            confirm_password_entry.config(show="")

            show_password_button.config(text="Hide Password")

        else:

            password_entry.config(show="*")
            confirm_password_entry.config(show="*")

            show_password_button.config(text="Show Password")

    show_password_button = tk.Button(
        form,
        text="Show Password",
        font=("Arial", 8),
        bg=WHITE,
        fg=PRIMARY_COLOR,
        activebackground=WHITE,
        activeforeground="#1D4ED8",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=toggle_password
    )

    show_password_button.pack(
        anchor="e",
        pady=(0, 10)
    )

    # ==============================
    # REGISTER FUNCTION
    # ==============================
    def create_account():

        username = username_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # EMPTY FIELDS
        if not username or not password or not confirm_password:

            messagebox.showwarning(
                "Missing Information",
                "Please complete all fields.",
                parent=window
            )
            return

        # USERNAME VALIDATION
        if len(username) < 4:

            messagebox.showwarning(
                "Invalid Username",
                "Username must contain at least 4 characters.",
                parent=window
            )
            return

        # PASSWORD VALIDATION
        if len(password) < 8:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 8 characters.",
                parent=window
            )
            return

        # CONFIRM PASSWORD VALIDATION
        if password != confirm_password:

            messagebox.showerror(
                "Password Mismatch",
                "Passwords do not match.",
                parent=window
            )
            return

        # SAVE ACCOUNT
        try:

            if register(username, password):

                messagebox.showinfo(
                    "Account Created",
                    "Your account has been created successfully!",
                    parent=window
                )

                window.destroy()

            else:

                messagebox.showerror(
                    "Registration Failed",
                    "Username already exists. Please choose another username.",
                    parent=window
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to create account:\n{error}",
                parent=window
            )

    # ==============================
    # CREATE ACCOUNT BUTTON
    # ==============================
    create_button = tk.Button(
        form,
        text="Create Account",
        font=("Arial", 10, "bold"),
        bg=PRIMARY_COLOR,
        fg=WHITE,
        activebackground="#1D4ED8",
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=create_account
    )

    create_button.pack(
        fill="x",
        ipady=8
    )

    # ==============================
    # FOOTER
    # ==============================
    tk.Label(
        form,
        text="Registrar Account Registration",
        font=("Arial", 8),
        bg=WHITE,
        fg=MUTED_COLOR
    ).pack(pady=(12, 0))

    # ==============================
    # KEYBOARD SHORTCUT
    # ==============================
    window.bind(
        "<Return>",
        lambda event: create_account()
    )

    username_entry.focus_set()
