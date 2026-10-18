import sqlite3

from backend.enrollments import save_enrollment

DATABASE_PATH = "database/database.db"


def test_invalid_student_id():
    print("\n--- Test 1: Invalid student ID ---")

    result = save_enrollment(
        "INVALID-STUDENT-ID",
        "2099-2100",
        "1st Semester",
        [1]
    )

    if result is None:
        print("PASS: Invalid student ID was rejected.")
    else:
        print("FAIL: Enrollment was created unexpectedly.")


def test_invalid_subject_id():
    print("\n--- Test 2: Invalid subject ID ---")

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.cursor()
        cursor.execute("""
            SELECT student_id
            FROM students
            LIMIT 1
        """)
        student = cursor.fetchone()

        if student is None:
            print("SKIP: Add a student before running this test.")
            return

        student_id = student[0]

    finally:
        connection.close()

    result = save_enrollment(
        student_id,
        "2099-2100",
        "1st Semester",
        [-999999]
    )

    if result is None:
        print("PASS: Invalid subject ID was rejected.")
    else:
        print("FAIL: Enrollment was created unexpectedly.")


if __name__ == "__main__":
    test_invalid_student_id()
    test_invalid_subject_id()
