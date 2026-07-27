"""
student.py
----------
Defines the Student class: a simple data model (OOP) representing
one row of the `student` table.

OOP concepts used:
- Encapsulation: all student attributes are bundled inside one object
  instead of being passed around as loose variables.
- Constructor (__init__): initializes a Student instance with its data.
- Method (display): behavior attached to the object, responsible for
  presenting itself instead of making other code know its internal layout.
- __repr__: a developer-friendly representation, useful for debugging/logging.
"""


class Student:
    def __init__(self, first_name, last_name, gender, age, department,
                 course, email, phone, address, admission_date=None,
                 student_id=None):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.age = age
        self.department = department
        self.course = course
        self.email = email
        self.phone = phone
        self.address = address
        self.admission_date = admission_date

    def display(self):
        """Prints a nicely formatted view of this student's details."""
        print("-" * 50)
        print(f"Student ID     : {self.student_id}")
        print(f"Name           : {self.first_name} {self.last_name}")
        print(f"Gender         : {self.gender}")
        print(f"Age            : {self.age}")
        print(f"Department     : {self.department}")
        print(f"Course         : {self.course}")
        print(f"Email          : {self.email}")
        print(f"Phone          : {self.phone}")
        print(f"Address        : {self.address}")
        print(f"Admission Date : {self.admission_date}")
        print("-" * 50)

    @classmethod
    def from_row(cls, row: dict):
        """Build a Student instance from a dictionary row returned by MySQL."""
        return cls(
            student_id=row.get("student_id"),
            first_name=row.get("first_name"),
            last_name=row.get("last_name"),
            gender=row.get("gender"),
            age=row.get("age"),
            department=row.get("department"),
            course=row.get("course"),
            email=row.get("email"),
            phone=row.get("phone"),
            address=row.get("address"),
            admission_date=row.get("admission_date"),
        )

    def __repr__(self):
        return f"<Student id={self.student_id} name={self.first_name} {self.last_name}>"
