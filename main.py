"""
main.py
-------
Entry point for the Student Management System CLI.
Keeps the loop thin: it only handles menu display and dispatching
to functions defined in operations.py.
"""

from utils import setup_logging
from operations import (
    add_student, view_students, search_student, update_student,
    delete_student, count_students, sort_students, filter_students,
    student_report, export_students, import_students,
)

MENU = """
==============================
 STUDENT MANAGEMENT SYSTEM
==============================
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. Count Students
7. Sort Students
8. Filter Students
9. Student Report
10. Export Students to CSV
11. Import Students from CSV
12. Exit
==============================
"""


def main():
    logger = setup_logging()
    logger.info("Application started.")

    actions = {
        "1": add_student,
        "2": view_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "6": count_students,
        "7": sort_students,
        "8": filter_students,
        "9": student_report,
        "10": export_students,
        "11": import_students,
    }

    while True:
        print(MENU)
        choice = input("Enter your choice (1-12): ").strip()

        if choice == "12":
            print("Exiting Student Management System. Goodbye!")
            logger.info("Application exited.")
            break

        action = actions.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                # Last-resort safety net so a single bad interaction
                # never crashes the whole CLI session.
                logger.error(f"Unexpected error in menu action '{choice}': {e}")
                print(f"An unexpected error occurred: {e}")
        else:
            print("Invalid choice. Please select a number between 1 and 12.")


if __name__ == "__main__":
    main()
