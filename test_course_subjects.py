from backend.courses import (
    create_course_subjects_table,
    get_all_courses,
    get_course_subjects,
    assign_subject_to_course,
    remove_subject_from_course
)

from backend.subjects import get_all_subjects

create_course_subjects_table()

courses = get_all_courses()
subjects = get_all_subjects()

print("Courses:", courses)
print("Subjects:", subjects)

if courses and subjects:
    course_id = courses[0][0]
    subject_id = subjects[0][0]

    print(
        "Assignment result:",
        assign_subject_to_course(
            course_id,
            subject_id,
            "1st Year",
            "1st Semester"
        )
    )

    print("Assigned subjects:", get_course_subjects(course_id))

    print(
        "Removal result:",
        remove_subject_from_course(course_id, subject_id)
    )
else:
    print("Add at least one course and one subject before testing.")