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