
import sqlite3


DATABASE_PATH = "database/database.db"


def create_enrollment_tables():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                academic_year TEXT NOT NULL,
                semester TEXT NOT NULL CHECK (
                    semester IN ('1st Semester', '2nd Semester')
                ),
                enrollment_date TEXT DEFAULT CURRENT_TIMESTAMP,

                UNIQUE (student_id, academic_year, semester),

                FOREIGN KEY (student_id)
                    REFERENCES students(student_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollment_subjects (
                enrollment_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,

                PRIMARY KEY (enrollment_id, subject_id),

                FOREIGN KEY (enrollment_id)
                    REFERENCES enrollments(enrollment_id)
                    ON DELETE CASCADE,

                FOREIGN KEY (subject_id)
                    REFERENCES subjects(subject_id)
            )
        """)

        connection.commit()
        return True

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()


def create_enrollment(student_id, academic_year, semester):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO enrollments (
                student_id,
                academic_year,
                semester
            )
            VALUES (?, ?, ?)
        """, (student_id, academic_year, semester))

        connection.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError as error:
        print("Could not create enrollment:", error)
        return None

    except sqlite3.Error as error:
        print("Database error:", error)
        return None

    finally:
        connection.close()


def add_subject_to_enrollment(enrollment_id, subject_id):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO enrollment_subjects (
                enrollment_id,
                subject_id
            )
            VALUES (?, ?)
        """, (enrollment_id, subject_id))

        connection.commit()
        return True

    except sqlite3.IntegrityError as error:
        print("Could not add subject:", error)
        return False

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()


def get_available_subjects(student_id, semester):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        # Get the student's course and year level.
        cursor.execute("""
            SELECT course, year_level
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
            return []

        student_course, year_level = student

        # Convert 1 to "1st Year", 2 to "2nd Year", etc.
        year_names = {
            1: "1st Year",
            2: "2nd Year",
            3: "3rd Year",
            4: "4th Year"
        }

        year_name = year_names.get(year_level)

        if year_name is None:
            print("Invalid student year level.")
            return []

        # Match the student's course and retrieve its subjects.
        cursor.execute("""
            SELECT
                subjects.subject_id,
                subjects.subject_code,
                subjects.subject_name,
                subjects.units
            FROM courses
            JOIN course_subjects
                ON courses.course_id = course_subjects.course_id
            JOIN subjects
                ON course_subjects.subject_id = subjects.subject_id
            WHERE (
                UPPER(courses.course_code) = UPPER(?)
                OR UPPER(courses.course_name) = UPPER(?)
            )
            AND course_subjects.year_level = ?
            AND course_subjects.semester = ?
            ORDER BY subjects.subject_code
        """, (
            student_course,
            student_course,
            year_name,
            semester
        ))

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()