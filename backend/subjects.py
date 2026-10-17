
import sqlite3


DATABASE_PATH = "database/database.db"


def create_subjects_table():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_code TEXT NOT NULL UNIQUE,
                subject_name TEXT NOT NULL,
                units INTEGER NOT NULL CHECK (units > 0),
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
                )
            )
        """)

        connection.commit()
        return True

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()


def add_subject(subject_code, subject_name, units, year_level,
                semester="1st Semester"):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO subjects (
                subject_code,
                subject_name,
                units,
                year_level,
                semester
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            subject_code.strip().upper(),
            subject_name.strip(),
            units,
            year_level,
            semester
        ))

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


def get_all_subjects():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                subject_id,
                subject_code,
                subject_name,
                units,
                year_level,
                semester
            FROM subjects
            ORDER BY year_level, semester, subject_code
        """)

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()


def update_subject(subject_id, subject_code, subject_name, units,
                   year_level, semester):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE subjects
            SET subject_code = ?,
                subject_name = ?,
                units = ?,
                year_level = ?,
                semester = ?
            WHERE subject_id = ?
        """, (
            subject_code.strip().upper(),
            subject_name.strip(),
            units,
            year_level,
            semester,
            subject_id
        ))

        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.Error as error:
        print("Could not update subject:", error)
        return False

    finally:
        connection.close()


def delete_subject(subject_id):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM subjects
            WHERE subject_id = ?
        """, (subject_id,))

        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.Error as error:
        print("Could not delete subject:", error)
        return False

    finally:
        connection.close()