# Project Documentation — Student Management System

## 1. Overview

The Student Management System is a command-line application that lets an
administrator manage student records stored in a MySQL database. It covers
the full lifecycle of a student record — creation, retrieval, updating, and
deletion — along with reporting, data export/import, and logging.

## 2. Objectives

- Provide a simple, reliable CLI tool to manage student data without
  requiring a GUI or web server.
- Demonstrate clean separation of concerns using modular Python design.
- Apply core object-oriented programming principles.
- Practice safe, parameterized SQL to prevent injection vulnerabilities.
- Build in validation, logging, and exception handling suitable for a
  small production-style tool.

## 3. Technology Stack

- **Language:** Python 3
- **Database:** MySQL
- **Driver:** mysql-connector-python
- **Testing:** unittest + unittest.mock
- **Tools:** VS Code, MySQL Workbench, Git

## 4. Modules

| Module | Responsibility |
|---|---|
| `main.py` | CLI menu loop; dispatches user choices to operations |
| `database.py` | Opens MySQL connections; generic `execute_query()` helper; wraps driver errors in `DatabaseError` |
| `student.py` | `Student` class — OOP data model with a `display()` method |
| `operations.py` | All CRUD, search, sort, filter, report, export/import logic |
| `utils.py` | Input validation functions; logging configuration |
| `config.py` | Centralized DB credentials and file paths (overridable via environment variables) |
| `tests/test_operations.py` | Unit tests for validation and CRUD logic (mocked database) |

## 5. Database Design

**Table: `student`**

| Column | Type | Constraints |
|---|---|---|
| student_id | INT | PRIMARY KEY, AUTO_INCREMENT |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| gender | ENUM('Male','Female','Other') | NOT NULL |
| age | INT | NOT NULL, CHECK (15–100) |
| department | VARCHAR(50) | NOT NULL |
| course | VARCHAR(50) | NOT NULL |
| email | VARCHAR(100) | NOT NULL, UNIQUE |
| phone | VARCHAR(15) | NOT NULL, UNIQUE |
| address | VARCHAR(255) | nullable |
| admission_date | DATE | NOT NULL, default current date |

Indexes are added on `last_name` and `department` to speed up common
search/filter/sort queries.

## 6. Design Decisions

- **Parameterized queries everywhere** (`%s` placeholders) to prevent SQL
  injection — no string-formatted SQL is ever executed.
- **`execute_query()` centralizes connection lifecycle** (open → execute →
  commit/fetch → close) so every operation function stays short and never
  has to remember to close a cursor/connection.
- **Custom `DatabaseError`** decouples the rest of the app from
  `mysql.connector`'s specific exception types, making it easier to swap
  drivers later if needed.
- **Validation lives in `utils.py`**, separate from I/O, so the rules
  (e.g. what counts as a valid phone number) can be unit tested without a
  database.
- **Logging** captures every add/update/delete and every error to
  `logs/app.log` with timestamps, useful for auditing and debugging.

## 7. Conclusion

This project demonstrates a complete, modular CLI application backed by a
relational database, following good practices around validation, error
handling, logging, and testing — while remaining small enough to read and
extend easily.
