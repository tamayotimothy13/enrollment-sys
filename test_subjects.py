from backend.subjects import (
    create_subjects_table,
    add_subject,
    get_all_subjects
)

if create_subjects_table():
    print("Subjects table is ready.")

    success = add_subject(
        "CS101",
        "Introduction to Computing",
        3,
        "1st Year"
    )

    print("Subject added:", success)
    print("Subjects:", get_all_subjects())