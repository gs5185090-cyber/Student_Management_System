"""
utils.py
--------
Shared helper functions: input validation and logging setup.
Keeping these separate from operations.py keeps CRUD logic focused
on "what to do with the database" rather than "how to validate input".
"""

import re
import logging
import os

from config import LOG_FILE


def setup_logging():
    """
    Configure the 'sms' logger to write to logs/app.log.
    Called once, at program startup (see main.py).
    """
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logger = logging.getLogger("sms")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if setup_logging() runs more than once
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# ------------------------------------------------------------------
# Validation helpers
# ------------------------------------------------------------------

EMAIL_PATTERN = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")
PHONE_PATTERN = re.compile(r"^\d{10}$")
VALID_GENDERS = {"male", "female", "other"}


def validate_name(name: str) -> bool:
    return bool(name) and name.replace(" ", "").isalpha()


def validate_age(age_str: str):
    """Returns (True, int_age) or (False, None)."""
    if not age_str.isdigit():
        return False, None
    age = int(age_str)
    if 15 <= age <= 100:
        return True, age
    return False, None


def validate_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email or ""))


def validate_phone(phone: str) -> bool:
    return bool(PHONE_PATTERN.match(phone or ""))


def validate_gender(gender: str):
    """Returns normalized gender string (Title case) if valid, else None."""
    if gender and gender.strip().lower() in VALID_GENDERS:
        return gender.strip().capitalize()
    return None


def prompt_non_empty(prompt_text: str) -> str:
    """Keep asking until the user enters a non-empty value."""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")
