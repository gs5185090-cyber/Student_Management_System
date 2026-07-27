# Interview Preparation — Student Management System

## Python Basics

**Q: Why use a virtual environment for this project?**
A: It isolates the project's dependencies (like `mysql-connector-python`)
from other Python projects on the same machine, avoiding version conflicts.

**Q: What does `if __name__ == "__main__":` do in `main.py`?**
A: It ensures `main()` only runs when the file is executed directly, not
when it's imported as a module elsewhere (e.g., in tests).

## OOP Concepts

**Q: Where is OOP used in this project, and why?**
A: The `Student` class in `student.py` encapsulates a student's data and
behavior (like `display()`) into one object, instead of passing around
individual variables. This keeps related data together and makes the code
easier to extend (e.g., adding a new field only touches one class).

**Q: What OOP principle does `Student.from_row()` demonstrate?**
A: It's a factory method pattern (via `@classmethod`) — it builds a
`Student` object from raw dictionary data returned by the database,
keeping the conversion logic in one place.

**Q: What's the difference between encapsulation and abstraction here?**
A: Encapsulation bundles the student's attributes and `display()` method
together in one class. Abstraction is seen in `database.py`, where
`execute_query()` hides the low-level connection/cursor details from the
rest of the app.

## Functions & Modular Programming

**Q: Why split the project into `main.py`, `operations.py`, `database.py`, etc.?**
A: Each module has a single responsibility: `main.py` handles the CLI loop,
`operations.py` handles business logic, `database.py` handles persistence,
and `utils.py` handles validation/logging. This makes the code easier to
test, maintain, and reuse.

**Q: What's the benefit of `execute_query()` being a single shared function?**
A: It avoids duplicating connection-open/close and error-handling code in
every CRUD function, and guarantees connections are always closed properly
via `finally`.

## Exception Handling

**Q: How does the project handle database connection failures?**
A: `database.py` catches `mysql.connector.Error` and re-raises it as a
custom `DatabaseError`, so callers only need to catch one exception type
regardless of the underlying driver's error hierarchy.

**Q: How are duplicate student records handled?**
A: The `email` and `phone` columns have `UNIQUE` constraints in MySQL.
Attempting to insert a duplicate raises an error, which `add_student()`
catches and reports to the user instead of crashing.

**Q: What happens if a menu action raises an unexpected error?**
A: `main.py`'s loop wraps each action call in a `try/except`, logs the
error, and shows a message — so one bad interaction never crashes the
whole CLI session.

## MySQL & Database Connectivity

**Q: Why use parameterized queries (`%s`) instead of string formatting?**
A: To prevent SQL injection. User input is passed separately from the SQL
text, so it's always treated as data, never as executable SQL.

**Q: How does partial name search work?**
A: Using SQL's `LIKE` operator with `%` wildcards, e.g.
`WHERE first_name LIKE %s` with a bound value of `%Rah%`, which matches
"Rahul", "Rahul Kumar", "Rahman", etc.

**Q: How would you get department-wise counts in SQL?**
A: `SELECT department, COUNT(*) FROM student GROUP BY department;`

## CRUD Operations

**Q: Walk through what happens when a user adds a student.**
A: `add_student()` prompts for each field, validates it (name, age, email,
phone, gender), then runs a parameterized `INSERT` via `execute_query()`.
On success it logs the event and confirms to the user; on failure (e.g. a
duplicate email) it catches `DatabaseError` and reports it.

**Q: How does delete confirm before removing a record?**
A: `delete_student()` first looks up and displays the record, then asks
the user to type `y` to confirm before running the `DELETE` query.

## Project Design

**Q: How would you extend this project to a web application?**
A: Keep `database.py`, `student.py`, and most of `operations.py` as-is,
then replace `main.py`'s CLI loop with a web framework (e.g., Flask or
FastAPI) that calls the same operation functions from HTTP route handlers.

**Q: What would you add next to make this production-ready?**
A: Connection pooling, hashed/role-based authentication for admin access,
pagination for large student lists, a proper migrations tool instead of a
single `.sql` file, and moving secrets into a `.env` file excluded from
version control.
