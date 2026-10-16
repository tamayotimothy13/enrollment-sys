import sqlite3
import random
import string
from datetime import datetime

def generate_student_id():
    year = datetime.now().strftime("%y")
    letter = random.choice(string.ascii_uppercase)
    number = random.randint(0, 9999)

    return f"{year}{letter}-{number:04d}"

def add_student(
    first_name,
    middle_name,
    last_name,
    prefix,
    address,
    birthday,
    birth_place,
    contact_number,
    emergency_contact_number,
    email,
    admission_type,
    year_level,
    course
):
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()
        student_id = generate_student_id()

        cursor.execute("""
            INSERT INTO students (
                student_id,
                first_name,
                middle_name,
                last_name,
                prefix,
                address,
                birthday,
                birth_place,
                contact_number,
                emergency_contact_number,
                email,
                admission_type,
                year_level,
                course
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            first_name,
            middle_name,
            last_name,
            prefix,
            address,
            birthday,
            birth_place,
            contact_number,
            emergency_contact_number,
            email,
            admission_type,
            int(year_level[0]),
            course
        ))

        connection.commit()
        return True

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()


def get_all_students():
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                student_id,
                first_name,
                last_name,
                course,
                year_level,
                email
            FROM students
            ORDER BY last_name ASC
        """)

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return []

    finally:
        connection.close()


def delete_student(student_id):
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )

        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()

    
def get_student_by_id(student_id):
    connection = sqlite3.connect("database/database.db")
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if student:
            return dict(student)

        return None

    except sqlite3.Error as error:
        print("Database error:", error)
        return None

    finally:
        connection.close()


def update_student(
    student_id,
    first_name,
    middle_name,
    last_name,
    prefix,
    address,
    birthday,
    birth_place,
    contact_number,
    emergency_contact_number,
    email,
    admission_type,
    year_level,
    course
):
    connection = sqlite3.connect("database/database.db")

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE students
            SET first_name = ?,
                middle_name = ?,
                last_name = ?,
                prefix = ?,
                address = ?,
                birthday = ?,
                birth_place = ?,
                contact_number = ?,
                emergency_contact_number = ?,
                email = ?,
                admission_type = ?,
                year_level = ?,
                course = ?
            WHERE student_id = ?
        """, (
            first_name,
            middle_name,
            last_name,
            prefix,
            address,
            birthday,
            birth_place,
            contact_number,
            emergency_contact_number,
            email,
            admission_type,
            int(year_level[0]),
            course,
            student_id
        ))

        connection.commit()
        return cursor.rowcount > 0

    except sqlite3.Error as error:
        print("Database error:", error)
        return False

    finally:
        connection.close()