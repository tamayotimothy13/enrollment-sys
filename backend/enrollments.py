
import sqlite3
import re

DATABASE_PATH = "database/database.db"

YEAR_NAMES = {
    1: "1st Year",
    2: "2nd Year",
    3: "3rd Year",
    4: "4th Year"
}


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_year_number(year_level):

    if year_level is None:
        return None

    value = str(year_level).strip().lower()

    word_numbers = {
        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4
    }

    for word, number in word_numbers.items():
        if word in value:
            return number

    match = re.search(r"\d+", value)

    if match:
        return int(match.group())

    return None


def get_student_info(cursor, student_id):

    cursor.execute("""
        SELECT admission_type, course, year_level
        FROM students
        WHERE student_id = ?
    """, (student_id,))

    return cursor.fetchone()


def get_allowed_subjects(cursor, student_id, semester):

    student = get_student_info(cursor, student_id)

    if student is None:
        return []

    admission_type, student_course, year_level = student

    year_number = get_year_number(year_level)

    if year_number not in YEAR_NAMES:
        return []

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

    if str(admission_type).strip().lower() == "transferee":

        query += """
            AND CAST(
                SUBSTR(course_subjects.year_level, 1, 1)
                AS INTEGER
            ) <= ?
        """

        parameters.append(year_number)

    else:

        query += """
            AND course_subjects.year_level = ?
        """

        parameters.append(YEAR_NAMES[year_number])

    query += " ORDER BY subjects.subject_code"

    cursor.execute(query, parameters)

    return cursor.fetchall()


def validate_subject_ids(
    cursor,
    student_id,
    semester,
    subject_ids
):

    allowed_subjects = get_allowed_subjects(
        cursor,
        student_id,
        semester
    )

    allowed_ids = {
        int(subject[0])
        for subject in allowed_subjects
    }

    try:
        selected_ids = [int(value) for value in subject_ids]
    except (TypeError, ValueError):
        return False

    if len(selected_ids) != len(set(selected_ids)):
        return False

    if not selected_ids:
        return False

    return all(
        subject_id in allowed_ids
        for subject_id in selected_ids
    )


# ==========================================
# CREATE ENROLLMENT TABLES
# ==========================================

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


# ==========================================
# CREATE ENROLLMENT
# ==========================================

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


# ==========================================
# ADD SUBJECT TO ENROLLMENT
# ==========================================

def add_subject_to_enrollment(enrollment_id, subject_id):

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_id, semester
            FROM enrollments
            WHERE enrollment_id = ?
        """, (enrollment_id,))

        enrollment = cursor.fetchone()

        if enrollment is None:
            return False

        student_id, semester = enrollment

        if not validate_subject_ids(
            cursor,
            student_id,
            semester,
            [subject_id]
        ):
            print("Subject does not match the student's year level.")
            return False

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


# ==========================================
# GET AVAILABLE SUBJECTS
# ==========================================

def get_available_subjects(student_id, semester):

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.cursor()

        student = get_student_info(cursor, student_id)

        if student is None:
            print("Student not found.")
            return []

        admission_type, student_course, year_level = student

        if get_year_number(year_level) not in YEAR_NAMES:
            print("Invalid student year level.")
            return []

        if semester not in ("1st Semester", "2nd Semester"):
            print("Invalid semester.")
            return []

        return get_allowed_subjects(
            cursor,
            student_id,
            semester
        )

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()


# ==========================================
# GET UNENROLLED STUDENTS
# ==========================================

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
        return []

    finally:
        connection.close()


# ==========================================
# SAVE ENROLLMENT WITH VALIDATION
# ==========================================

def save_enrollment(
    student_id,
    academic_year,
    semester,
    subject_ids
):

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        if semester not in ("1st Semester", "2nd Semester"):
            print("Invalid semester.")
            return None

        if not academic_year or not academic_year.strip():
            print("Academic year is required.")
            return None

        if not validate_subject_ids(
            cursor,
            student_id,
            semester,
            subject_ids
        ):
            print("Enrollment rejected: invalid subjects.")
            return None

        cursor.execute("""
            INSERT INTO enrollments (
                student_id,
                academic_year,
                semester
            )
            VALUES (?, ?, ?)
        """, (student_id, academic_year.strip(), semester))

        enrollment_id = cursor.lastrowid

        for subject_id in subject_ids:

            cursor.execute("""
                INSERT INTO enrollment_subjects (
                    enrollment_id,
                    subject_id
                )
                VALUES (?, ?)
            """, (enrollment_id, int(subject_id)))

        connection.commit()
        return enrollment_id

    except sqlite3.Error as error:
        connection.rollback()
        print("Could not save enrollment:", error)
        return None

    finally:
        connection.close()


# ==========================================
# GET ENROLLMENT DETAILS
# ==========================================

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
                subjects.units,

                (
                    SELECT course_subjects.year_level
                    FROM course_subjects
                    JOIN courses
                        ON courses.course_id =
                           course_subjects.course_id
                    JOIN students
                        ON students.student_id =
                           enrollments.student_id
                    WHERE course_subjects.subject_id =
                          subjects.subject_id
                      AND course_subjects.semester =
                          enrollments.semester
                      AND (
                          UPPER(courses.course_code) =
                          UPPER(students.course)

                          OR

                          UPPER(courses.course_name) =
                          UPPER(students.course)
                      )
                    LIMIT 1
                ) AS subject_year_level

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


# ==========================================
# GET ALL ENROLLMENTS
# ==========================================

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


# ==========================================
# UPDATE ENROLLMENT SUBJECTS
# ==========================================

def update_enrollment_subjects(enrollment_id, subject_ids):

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_id, semester
            FROM enrollments
            WHERE enrollment_id = ?
        """, (enrollment_id,))

        enrollment = cursor.fetchone()

        if enrollment is None:
            return False

        student_id, semester = enrollment

        if not validate_subject_ids(
            cursor,
            student_id,
            semester,
            subject_ids
        ):
            print("Update rejected: invalid subjects.")
            return False

        cursor.execute("""
            DELETE FROM enrollment_subjects
            WHERE enrollment_id = ?
        """, (enrollment_id,))

        for subject_id in set(int(value) for value in subject_ids):

            cursor.execute("""
                INSERT INTO enrollment_subjects (
                    enrollment_id,
                    subject_id
                )
                VALUES (?, ?)
            """, (enrollment_id, subject_id))

        connection.commit()
        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("Could not update enrollment subjects:", error)
        return False

    finally:
        connection.close()


# ==========================================
# SYNCHRONIZE ENROLLED SUBJECTS WITH YEAR
# ==========================================

def sync_enrollment_subjects_to_year(student_id):

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        # Get updated student information.
        cursor.execute("""
            SELECT course, year_level
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
            return False

        student_course, year_level = student

        year_number = get_year_number(year_level)

        if year_number not in YEAR_NAMES:
            print("Invalid year level.")
            return False

        current_year = YEAR_NAMES[year_number]

        # Get latest academic year enrollments.
        cursor.execute("""
            SELECT enrollment_id, semester
            FROM enrollments
            WHERE student_id = ?
              AND academic_year = (
                  SELECT MAX(academic_year)
                  FROM enrollments
                  WHERE student_id = ?
              )
        """, (student_id, student_id))

        enrollments = cursor.fetchall()

        if not enrollments:
            connection.commit()
            return True

        for enrollment_id, semester in enrollments:

            # Get valid subject IDs from the subjects table.
            cursor.execute("""
                SELECT DISTINCT subjects.subject_id
                FROM courses
                INNER JOIN course_subjects
                    ON courses.course_id = course_subjects.course_id
                INNER JOIN subjects
                    ON course_subjects.subject_id = subjects.subject_id
                WHERE (
                    UPPER(courses.course_code) = UPPER(?)
                    OR UPPER(courses.course_name) = UPPER(?)
                )
                AND course_subjects.semester = ?
                AND course_subjects.year_level = ?
                AND subjects.year_level = ?
                AND subjects.semester = ?
                ORDER BY subjects.subject_code
            """, (
                student_course,
                student_course,
                semester,
                current_year,
                current_year,
                semester
            ))

            subject_ids = [
                row[0] for row in cursor.fetchall()
            ]

            if not subject_ids:
                print(
                    f"No assigned subjects found for "
                    f"{student_course}, {current_year}, {semester}."
                )

                connection.rollback()
                return False

            # Replace existing subjects.
            cursor.execute("""
                DELETE FROM enrollment_subjects
                WHERE enrollment_id = ?
            """, (enrollment_id,))

            # Insert updated subjects.
            for subject_id in subject_ids:

                cursor.execute("""
                    INSERT INTO enrollment_subjects (
                        enrollment_id,
                        subject_id
                    )
                    SELECT ?, subject_id
                    FROM subjects
                    WHERE subject_id = ?
                """, (enrollment_id, subject_id))

        connection.commit()

        print("Enrolled subjects synchronized successfully.")
        return True

    except sqlite3.Error as error:
        connection.rollback()
        print("Could not synchronize enrolled subjects:", error)
        return False

    finally:
        connection.close()


# ==========================================
# DELETE ENROLLMENT
# ==========================================

def delete_enrollment(enrollment_id):

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

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


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("\n--- ALL ENROLLMENTS ---")

    for enrollment in get_all_enrollments():
        print(enrollment)
