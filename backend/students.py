import sqlite3


def add_student(
    student_id,
    first_name,
    middle_name,
    last_name,
    prefix,
    address,
    birthday,
    contact_number,
    email,
    admission_type,
    year_level,
    course
):
    connection = sqlite3.connect("database/database.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (
                student_id,
                first_name,
                middle_name,
                last_name,
                prefix,
                address,
                birthday,
                contact_number,
                email,
                admission_type,
                year_level,
                course
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_id,
            first_name,
            middle_name,
            last_name,
            prefix,
            address,
            birthday,
            contact_number,
            email,
            admission_type,
            year_level,
            course
        ))
        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()