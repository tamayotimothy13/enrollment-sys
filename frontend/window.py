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


def create_search_bar(parent, placeholder="Search..."):
    search_frame = tk.Frame(parent)

    search_var = tk.StringVar()

    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        width=30
    )
    search_entry.pack(side="right")

    search_label = tk.Label(
        search_frame,
        text="Search:"
    )
    search_label.pack(side="right", padx=(0, 5))

    return search_frame, search_var, search_entry