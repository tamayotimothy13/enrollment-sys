import sqlite3

connection = sqlite3.connect("database/database.db")

cursor = connection.cursor()
cursor.execute("SELECT student_id FROM students LIMIT 1")

result = cursor.fetchone()

print("Existing student ID:", result[0] if result else "No students found")

connection.close()