import tkinter as tk

def setup_window(window, title):
    window.title(title)

    width = 900
    height = 600

    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate center position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set size and position
    window.geometry(f"{width}x{height}+{x}+{y}")

    # Prevent resizing
    window.resizable(False, False)


def create_search_box(parent, search_command=None, clear_command=None):
    search_box = tk.Frame(
        parent,
        relief="solid",
        bd=1
    )

    search_entry = tk.Entry(
        search_box,
        font=("Arial", 10),
        width=25,
        relief="flat",
        bd=0
    )
    search_entry.pack(side="left", ipady=6, padx=(5, 0))

    clear_button = tk.Button(
        search_box,
        text="×",
        font=("Arial", 12),
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda: clear_command() if clear_command else search_entry.delete(0, tk.END)
    )
    clear_button.pack(side="right", padx=(0, 4))

    if search_command:
        search_entry.bind(
            "<Return>",
            lambda event: search_command()
        )

    return search_box, search_entry