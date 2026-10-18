
import sqlite3

from backend.enrollments import save_enrollment

DATABASE_PATH = "database/database.db"


def test_enrollment_rollback():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_id
            FROM students
            LIMIT 1
        """)
        student = cursor.fetchone()

        cursor.execute("""
            SELECT subject_id
            FROM subjects
            LIMIT 1
        """)
        subject = cursor.fetchone()

        if student is None or subject is None:
            print("SKIP: A student and a subject are required.")
            return

        student_id = student[0]
        valid_subject_id = subject[0]

        # Count records before the test.
        cursor.execute("SELECT COUNT(*) FROM enrollments")
        enrollments_before = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM enrollment_subjects")
        subjects_before = cursor.fetchone()[0]

    finally:
        connection.close()

    # The valid subject is inserted first; the invalid one should fail.
    result = save_enrollment(
        student_id,
        "2099-2100",
        "1st Semester",
        [valid_subject_id, -999999]
    )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM enrollments")
        enrollments_after = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM enrollment_subjects")
        subjects_after = cursor.fetchone()[0]

    finally:
        connection.close()

    if (
        result is None
        and enrollments_after == enrollments_before
        and subjects_after == subjects_before
    ):
        print("PASS: Failed enrollment was rolled back completely.")
    else:
        print("FAIL: Database record counts changed unexpectedly.")
        print("Enrollment result:", result)
        print("Enrollments before/after:",
              enrollments_before, enrollments_after)
        print("Enrollment subjects before/after:",
              subjects_before, subjects_after)


if __name__ == "__main__":
    test_enrollment_rollback()