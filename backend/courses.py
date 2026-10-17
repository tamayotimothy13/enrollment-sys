import sqlite3

def create_courses_table():
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT NOT NULL UNIQUE,
                course_name TEXT NOT NULL
            )
        """)
        connection.commit()
        return True

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()


def add_course(course_code, course_name):
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO courses (course_code, course_name)
            VALUES (?, ?)
        """, (course_code.strip().upper(), course_name.strip()))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()


def get_all_courses():
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT course_id, course_code, course_name
            FROM courses
            ORDER BY course_code
        """)

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()


def create_course_subjects_table():
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course_subjects (
                course_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                year_level TEXT NOT NULL CHECK (
                    year_level IN (
                        '1st Year',
                        '2nd Year',
                        '3rd Year',
                        '4th Year'
                    )
                ),
                semester TEXT NOT NULL CHECK (
                    semester IN (
                        '1st Semester',
                        '2nd Semester'
                    )
                ),

                PRIMARY KEY (course_id, subject_id),

                FOREIGN KEY (course_id)
                    REFERENCES courses(course_id)
                    ON DELETE CASCADE,

                FOREIGN KEY (subject_id)
                    REFERENCES subjects(subject_id)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()
        return True

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()


def assign_subject_to_course(
    course_id, subject_id, year_level, semester
):
    connection = sqlite3.connect("database/database.db")

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO course_subjects (
                course_id,
                subject_id,
                year_level,
                semester
            )
            VALUES (?, ?, ?, ?)
        """, (
            course_id,
            subject_id,
            year_level,
            semester
        ))

        connection.commit()
        return True

    except sqlite3.IntegrityError as error:
        print("Could not assign subject:", error)
        return False

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()


def get_course_subjects(course_id):
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                subjects.subject_id,
                subjects.subject_code,
                subjects.subject_name,
                subjects.units,
                course_subjects.year_level,
                course_subjects.semester
            FROM course_subjects
            JOIN subjects
                ON course_subjects.subject_id = subjects.subject_id
            WHERE course_subjects.course_id = ?
            ORDER BY
                course_subjects.year_level,
                course_subjects.semester,
                subjects.subject_code
        """, (course_id,))

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()


def remove_subject_from_course(course_id, subject_id):
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM course_subjects
            WHERE course_id = ? AND subject_id = ?
        """, (course_id, subject_id))

        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.Error as error:
        print("Could not remove subject assignment:", error)
        return False

    finally:
        connection.close()