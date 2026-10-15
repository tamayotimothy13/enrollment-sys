import tkinter as tk
def show_dashboard():

    window = tk.Tk()
    width = 800
    height = 450
    
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

    title = tk.Label(
        window,
        text="Enrollment System",
        font=("Arial", 20)
    )
    title.pack(pady=30)

    students_button = tk.Button(
        window,
        text="Add Student(s)",
        width=20
    )
    students_button.pack(pady=5)

    subjects_button = tk.Button(
        window,
        text="Enroll Student(s)",
        width=20
    )
    subjects_button.pack(pady=5)

    masterlist_button = tk.Button(
        window,
        text="View Masterlist",
        width=20
    )
    masterlist_button.pack(pady=5)

    courses_button = tk.Button(
            window,
            text="Courses",
            width=20
    )
    courses_button.pack(pady=5)

    logout_button = tk.Button(
        window,
        text="Logout",
        width=20,
        command=window.destroy
    )
    logout_button.pack(pady=20)

    window.mainloop()