"""
config.py
----------
Centralized configuration for the Student Management System.

Keeping credentials here (instead of hardcoding them inside database.py)
makes it easy to:
  - change environments (dev / test / production) without touching logic code
  - avoid committing secrets directly inside business-logic files
  - override values using environment variables when deploying

For a real production project, replace the hardcoded defaults below with
environment variables (see the os.getenv usage) and never commit a .env
file containing real passwords to Git.
"""

import os

DB_CONFIG = {
    "host": os.getenv("SMS_DB_HOST", "localhost"),
    "user": os.getenv("SMS_DB_USER", "root"),
    "password": os.getenv("SMS_DB_PASSWORD", "GOWRI123"),
    "database": os.getenv("SMS_DB_NAME", "student_management"),
}

# Logging configuration
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "app.log")

# Export/Import configuration
EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
DEFAULT_EXPORT_FILE = os.path.join(EXPORT_DIR, "students.csv")
