import tkinter as tk
from backend.auth import login


def show_login():
    window = tk.Tk()
    window.title("Enrollment System")
    window.geometry("400x300")

    # Username
    username_label = tk.Label(window, text="Username")
    username_label.pack()

    username_textbox = tk.Entry(window)
    username_textbox.pack()

    # Password
    password_label = tk.Label(window, text="Password")
    password_label.pack()

    password_textbox = tk.Entry(window, show="*")
    password_textbox.pack()

    # Login function for the button
    def attempt_login():
        username = username_textbox.get()
        password = password_textbox.get()

        if login(username, password):
            print("Login successful!")
        else:
            print("Invalid username or password.")

    # Login button
    login_button = tk.Button(
        window,
        text="Login",
        command=attempt_login
    )
    login_button.pack()

    window.mainloop()