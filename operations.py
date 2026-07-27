"""
operations.py
-------------
All business logic / CRUD operations for the Student Management System.
This module is the "controller" layer: it talks to database.py for
persistence and to student.py for the data model, and exposes one
function per menu action so main.py can stay a thin CLI loop.
"""

import csv
import logging

from database import execute_query, DatabaseError
from student import Student
from utils import (
    validate_name, validate_age, validate_email,
    validate_phone, validate_gender, prompt_non_empty,
)
from config import DEFAULT_EXPORT_FILE

logger = logging.getLogger("sms")


# ------------------------------------------------------------------
# CREATE
# ------------------------------------------------------------------
def add_student():
    """Prompt the user for student details, validate them, and insert them."""
    print("\n--- Add New Student ---")

    while True:
        first_name = prompt_non_empty("First Name: ")
        if validate_name(first_name):
            break
        print("Invalid first name. Letters only, please.")

    while True:
        last_name = prompt_non_empty("Last Name: ")
        if validate_name(last_name):
            break
        print("Invalid last name. Letters only, please.")

    while True:
        gender_input = prompt_non_empty("Gender (Male/Female/Other): ")
        gender = validate_gender(gender_input)
        if gender:
            break
        print("Invalid gender. Enter Male, Female, or Other.")

    while True:
        age_input = prompt_non_empty("Age: ")
        ok, age = validate_age(age_input)
        if ok:
            break
        print("Invalid age. Enter a number between 15 and 100.")

    department = prompt_non_empty("Department: ")
    course = prompt_non_empty("Course: ")

    while True:
        email = prompt_non_empty("Email: ")
        if validate_email(email):
            break
        print("Invalid email format.")

    while True:
        phone = prompt_non_empty("Phone (10 digits): ")
        if validate_phone(phone):
            break
        print("Invalid phone number. Must be exactly 10 digits.")

    address = input("Address: ").strip()

    query = """
        INSERT INTO student
            (first_name, last_name, gender, age, department, course, email, phone, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (first_name, last_name, gender, age, department, course, email, phone, address)

    try:
        execute_query(query, params)
        logger.info(f"Student Added: {first_name} {last_name} ({email})")
        print("Student added successfully!")
    except DatabaseError as e:
        # Duplicate email/phone will raise here due to UNIQUE constraints
        logger.error(f"Error adding student: {e}")
        print(f"Failed to add student: {e}")


# ------------------------------------------------------------------
# READ
# ------------------------------------------------------------------
def _print_students_table(rows):
    if not rows:
        print("No students found.")
        return

    header = f"{'ID':<5}{'Name':<25}{'Gender':<8}{'Age':<5}{'Department':<18}{'Course':<12}{'Email':<28}{'Phone':<14}"
    print(header)
    print("-" * len(header))
    for row in rows:
        full_name = f"{row['first_name']} {row['last_name']}"
        print(f"{row['student_id']:<5}{full_name:<25}{row['gender']:<8}{row['age']:<5}"
              f"{row['department']:<18}{row['course']:<12}{row['email']:<28}{row['phone']:<14}")


def view_students():
    print("\n--- All Students ---")
    try:
        rows = execute_query("SELECT * FROM student ORDER BY student_id", fetch=True)
        _print_students_table(rows)
    except DatabaseError as e:
        print(f"Failed to fetch students: {e}")


def search_student():
    print("\n--- Search Student ---")
    print("1. Search by ID")
    print("2. Search by Name (partial match)")
    choice = input("Choose an option: ").strip()

    try:
        if choice == "1":
            sid = prompt_non_empty("Enter Student ID: ")
            rows = execute_query(
                "SELECT * FROM student WHERE student_id = %s", (sid,), fetch=True
            )
        elif choice == "2":
            name = prompt_non_empty("Enter name (or part of it): ")
            like_pattern = f"%{name}%"
            rows = execute_query(
                """SELECT * FROM student
                   WHERE first_name LIKE %s OR last_name LIKE %s""",
                (like_pattern, like_pattern),
                fetch=True,
            )
        else:
            print("Invalid option.")
            return

        _print_students_table(rows)
    except DatabaseError as e:
        print(f"Search failed: {e}")


def sort_students():
    print("\n--- Sort Students ---")
    print("1. By Name")
    print("2. By Department")
    print("3. By Admission Date")
    choice = input("Choose an option: ").strip()

    columns = {
        "1": "first_name, last_name",
        "2": "department",
        "3": "admission_date",
    }
    column = columns.get(choice)
    if not column:
        print("Invalid option.")
        return

    try:
        rows = execute_query(f"SELECT * FROM student ORDER BY {column}", fetch=True)
        _print_students_table(rows)
    except DatabaseError as e:
        print(f"Failed to sort students: {e}")


def filter_students():
    print("\n--- Filter Students ---")
    print("1. By Department")
    print("2. By Gender")
    print("3. By Course")
    choice = input("Choose an option: ").strip()

    columns = {"1": "department", "2": "gender", "3": "course"}
    column = columns.get(choice)
    if not column:
        print("Invalid option.")
        return

    value = prompt_non_empty(f"Enter {column}: ")
    try:
        rows = execute_query(
            f"SELECT * FROM student WHERE {column} = %s", (value,), fetch=True
        )
        _print_students_table(rows)
    except DatabaseError as e:
        print(f"Failed to filter students: {e}")


def count_students():
    print("\n--- Student Count ---")
    try:
        row = execute_query("SELECT COUNT(*) AS total FROM student", fetchone=True)
        print(f"Total Students: {row['total']}")
    except DatabaseError as e:
        print(f"Failed to count students: {e}")


def student_report():
    print("\n--- Student Report ---")
    try:
        total = execute_query("SELECT COUNT(*) AS total FROM student", fetchone=True)["total"]

        dept_rows = execute_query(
            "SELECT department, COUNT(*) AS count FROM student GROUP BY department",
            fetch=True,
        )
        gender_rows = execute_query(
            "SELECT gender, COUNT(*) AS count FROM student GROUP BY gender",
            fetch=True,
        )
        avg_row = execute_query(
            "SELECT AVG(age) AS avg_age FROM student", fetchone=True
        )

        print(f"Total Students   : {total}")
        print("Department-wise Count:")
        for row in dept_rows:
            print(f"  {row['department']:<20}: {row['count']}")
        print("Gender-wise Count:")
        for row in gender_rows:
            print(f"  {row['gender']:<20}: {row['count']}")
        avg_age = avg_row["avg_age"]
        print(f"Average Age      : {round(avg_age, 2) if avg_age is not None else 'N/A'}")
    except DatabaseError as e:
        print(f"Failed to generate report: {e}")


# ------------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------------
def update_student():
    print("\n--- Update Student ---")
    sid = prompt_non_empty("Enter Student ID to update: ")

    try:
        existing = execute_query(
            "SELECT * FROM student WHERE student_id = %s", (sid,), fetchone=True
        )
    except DatabaseError as e:
        print(f"Lookup failed: {e}")
        return

    if not existing:
        print("No student found with that ID.")
        return

    print("Leave a field blank to keep its current value.")
    print(f"Current first name: {existing['first_name']}")
    first_name = input("New First Name: ").strip() or existing["first_name"]

    print(f"Current last name: {existing['last_name']}")
    last_name = input("New Last Name: ").strip() or existing["last_name"]

    print(f"Current department: {existing['department']}")
    department = input("New Department: ").strip() or existing["department"]

    print(f"Current course: {existing['course']}")
    course = input("New Course: ").strip() or existing["course"]

    print(f"Current phone: {existing['phone']}")
    while True:
        phone_input = input("New Phone: ").strip()
        if not phone_input:
            phone = existing["phone"]
            break
        if validate_phone(phone_input):
            phone = phone_input
            break
        print("Invalid phone number. Must be exactly 10 digits.")

    print(f"Current email: {existing['email']}")
    while True:
        email_input = input("New Email: ").strip()
        if not email_input:
            email = existing["email"]
            break
        if validate_email(email_input):
            email = email_input
            break
        print("Invalid email format.")

    query = """
        UPDATE student
        SET first_name = %s, last_name = %s, department = %s,
            course = %s, phone = %s, email = %s
        WHERE student_id = %s
    """
    params = (first_name, last_name, department, course, phone, email, sid)

    try:
        affected = execute_query(query, params)
        if affected:
            logger.info(f"Student Updated: ID={sid}")
            print("Student updated successfully!")
        else:
            print("No changes were made.")
    except DatabaseError as e:
        logger.error(f"Error updating student {sid}: {e}")
        print(f"Failed to update student: {e}")


# ------------------------------------------------------------------
# DELETE
# ------------------------------------------------------------------
def delete_student():
    print("\n--- Delete Student ---")
    sid = prompt_non_empty("Enter Student ID to delete: ")

    try:
        existing = execute_query(
            "SELECT * FROM student WHERE student_id = %s", (sid,), fetchone=True
        )
    except DatabaseError as e:
        print(f"Lookup failed: {e}")
        return

    if not existing:
        print("No student found with that ID.")
        return

    Student.from_row(existing).display()
    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    try:
        execute_query("DELETE FROM student WHERE student_id = %s", (sid,))
        logger.info(f"Student Deleted: ID={sid}")
        print("Student deleted successfully!")
    except DatabaseError as e:
        logger.error(f"Error deleting student {sid}: {e}")
        print(f"Failed to delete student: {e}")


# ------------------------------------------------------------------
# EXPORT / IMPORT
# ------------------------------------------------------------------
FIELDNAMES = [
    "student_id", "first_name", "last_name", "gender", "age",
    "department", "course", "email", "phone", "address", "admission_date",
]


def export_students(filepath: str = None):
    filepath = filepath or DEFAULT_EXPORT_FILE
    print("\n--- Export Students to CSV ---")
    try:
        rows = execute_query("SELECT * FROM student ORDER BY student_id", fetch=True)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f"Exported {len(rows)} records to {filepath}")
        logger.info(f"Exported {len(rows)} students to {filepath}")
    except (DatabaseError, OSError) as e:
        logger.error(f"Export failed: {e}")
        print(f"Export failed: {e}")


def import_students(filepath: str = None):
    filepath = filepath or DEFAULT_EXPORT_FILE
    print("\n--- Import Students from CSV ---")
    imported, skipped = 0, 0
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get("email")
                # Skip duplicates gracefully instead of crashing the whole import
                existing = execute_query(
                    "SELECT student_id FROM student WHERE email = %s OR phone = %s",
                    (email, row.get("phone")),
                    fetchone=True,
                )
                if existing:
                    skipped += 1
                    continue

                query = """
                    INSERT INTO student
                        (first_name, last_name, gender, age, department, course, email, phone, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (
                    row.get("first_name"), row.get("last_name"), row.get("gender"),
                    int(row.get("age")), row.get("department"), row.get("course"),
                    row.get("email"), row.get("phone"), row.get("address"),
                )
                execute_query(query, params)
                imported += 1

        print(f"Import complete. Imported: {imported}, Skipped duplicates: {skipped}")
        logger.info(f"Import complete. Imported={imported} Skipped={skipped}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except (DatabaseError, ValueError, OSError) as e:
        logger.error(f"Import failed: {e}")
        print(f"Import failed: {e}")
