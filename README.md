# Student Management System (CLI-Based)

A command-line Student Management System built with **Python 3** and **MySQL**.
Supports full CRUD operations, search, sorting, filtering, reporting, CSV
import/export, logging, input validation, and unit tests.

## Features

- Add Student
- View All Students
- Search Student (by ID or partial name using SQL `LIKE`)
- Update Student
- Delete Student (with confirmation)
- Count Students
- Sort Students (by name, department, or admission date)
- Filter Students (by department, gender, or course)
- Student Report (totals, department-wise & gender-wise counts, average age)
- Export students to CSV
- Import students from CSV (skips duplicates gracefully)
- Centralized logging to `logs/app.log`
- Input validation (name, age, email, phone, gender)
- Unit tests for validation and CRUD logic

## Technology Stack

| Component        | Technology              |
|-------------------|--------------------------|
| Language          | Python 3                |
| Database          | MySQL                   |
| DB Driver         | mysql-connector-python  |
| IDE               | VS Code                 |
| DB Tool           | MySQL Workbench         |

## Project Structure

```
StudentManagementSystem/
│
├── main.py                  # CLI entry point / menu loop
├── database.py               # Connection handling + generic query executor
├── student.py                 # Student class (OOP data model)
├── operations.py              # All CRUD + reporting logic
├── config.py                   # DB credentials & file path configuration
├── utils.py                     # Validation helpers + logging setup
├── requirements.txt
├── README.md
├── student_management.sql     # Schema + sample data
├── logs/
│   └── app.log
├── exports/
│   └── students.csv
└── tests/
    └── test_operations.py
```

## Installation

1. **Clone or copy the project folder.**

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. Open **MySQL Workbench** (or the `mysql` CLI) and run the schema script:
   ```bash
   mysql -u root -p < student_management.sql
   ```
   This creates the `student_management` database, the `student` table,
   indexes, and a few sample rows.

2. Set your database credentials as environment variables (recommended),
   or edit the defaults directly in `config.py`:
   ```bash
   export SMS_DB_HOST=localhost
   export SMS_DB_USER=root
   export SMS_DB_PASSWORD=your_password_here
   export SMS_DB_NAME=student_management
   ```

## Running the Project

```bash
python main.py
```

You'll see a menu like this:

```
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
```

## Running Tests

```bash
python -m unittest tests/test_operations.py -v
```

## Screenshots

## Screenshots

### Main Menu
![Main Menu](images/main-menu.png)

### View Students Table
![View Students Table](images/view-students.png)

### Student Report
![Student Report](images/student-report.png)

## License

This project is provided as-is for educational purposes.
