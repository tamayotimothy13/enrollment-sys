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

        # Get the student's admission type, course, and year level.
        cursor.execute("""
            SELECT admission_type, course, year_level
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
            return []

        admission_type, student_course, year_level = student

        # Convert the numeric year level to its name.
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

        # Common query: retrieve subjects assigned to the student's course.
        query = """
            SELECT
                subjects.subject_id,
                subjects.subject_code,
                subjects.subject_name,
                course_subjects.year_level,
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
            AND course_subjects.semester = ?
        """

        parameters = [
            student_course,
            student_course,
            semester
        ]

        # Regular students: restrict subjects to their year level.
        # Transferees: allow subjects from any year level.
        
        if admission_type == "Transferee":
            # Transferees can take subjects from their year
            # level and any earlier year level.
            query += """
                AND CAST(
                    SUBSTR(course_subjects.year_level, 1, 1)
                    AS INTEGER
                ) <= ?
            """
            parameters.append(year_level)

        else:
            # Regular students can take subjects from their
            # assigned year level only.
            query += """
                AND course_subjects.year_level = ?
            """
            parameters.append(year_name)

        cursor.execute(query, parameters)
        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()


def get_unenrolled_students(academic_year, semester):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                students.student_id,
                students.first_name,
                students.last_name,
                students.course,
                students.year_level,
                students.admission_type
            FROM students
            WHERE NOT EXISTS (
                SELECT 1
                FROM enrollments
                WHERE enrollments.student_id = students.student_id
                  AND enrollments.academic_year = ?
                  AND enrollments.semester = ?
            )
            ORDER BY students.last_name ASC
        """, (academic_year, semester))

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return None

    finally:
        connection.close()


def save_enrollment(student_id, academic_year, semester, subject_ids):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        # Create the enrollment record.
        cursor.execute("""
            INSERT INTO enrollments (
                student_id,
                academic_year,
                semester
            )
            VALUES (?, ?, ?)
        """, (student_id, academic_year, semester))

        enrollment_id = cursor.lastrowid

        # Add all selected subjects to this enrollment.
        for subject_id in subject_ids:
            cursor.execute("""
                INSERT INTO enrollment_subjects (
                    enrollment_id,
                    subject_id
                )
                VALUES (?, ?)
            """, (enrollment_id, subject_id))

        # Save everything together.
        connection.commit()
        return enrollment_id

    except sqlite3.Error as error:
        connection.rollback()
        print("Could not save enrollment:", error)
        return None

    finally:
        connection.close()


def get_enrollment_details(enrollment_id):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                enrollments.enrollment_id,
                enrollments.student_id,
                enrollments.academic_year,
                enrollments.semester,
                enrollments.enrollment_date,
                subjects.subject_id,
                subjects.subject_code,
                subjects.subject_name,
                subjects.units
            FROM enrollments
            LEFT JOIN enrollment_subjects
                ON enrollments.enrollment_id =
                   enrollment_subjects.enrollment_id
            LEFT JOIN subjects
                ON enrollment_subjects.subject_id =
                   subjects.subject_id
            WHERE enrollments.enrollment_id = ?
            ORDER BY subjects.subject_code
        """, (enrollment_id,))

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()


def get_all_enrollments():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                enrollments.enrollment_id,
                enrollments.student_id,
                students.first_name,
                students.last_name,
                students.course,
                students.year_level,
                enrollments.academic_year,
                enrollments.semester,
                enrollments.enrollment_date
            FROM enrollments
            JOIN students
                ON enrollments.student_id = students.student_id
            ORDER BY enrollments.enrollment_id DESC
        """)

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()


def delete_enrollment(enrollment_id):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        # Enable foreign-key enforcement for this connection.
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        # Delete the selected enrollment.
        # Its linked enrollment_subjects rows are deleted automatically.
        cursor.execute("""
            DELETE FROM enrollments
            WHERE enrollment_id = ?
        """, (enrollment_id,))

        if cursor.rowcount == 0:
            connection.rollback()
            return False

        connection.commit()
        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("Could not delete enrollment:", error)
        return False

    finally:
        connection.close()

if __name__ == "__main__":
    print("\n--- ALL ENROLLMENTS ---")

    for enrollment in get_all_enrollments():
        print(enrollment)