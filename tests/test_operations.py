"""
tests/test_operations.py
-------------------------
Unit tests for the Student Management System.

Two groups of tests:
1. Pure validation logic (utils.py) - no database required, run anywhere.
2. CRUD operations (operations.py) - use unittest.mock to fake the
   database layer so tests don't need a real MySQL server.

Run with:
    python -m unittest tests/test_operations.py -v
"""

import sys
import os
import unittest
from unittest.mock import patch

# Allow running this file directly (adds project root to path)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import (
    validate_name, validate_age, validate_email,
    validate_phone, validate_gender,
)
import operations


class TestValidation(unittest.TestCase):
    """Tests for the pure validation helpers - fast, no mocking needed."""

    def test_validate_name_accepts_letters(self):
        self.assertTrue(validate_name("Rahul"))
        self.assertTrue(validate_name("Rahul Kumar"))

    def test_validate_name_rejects_numbers(self):
        self.assertFalse(validate_name("Rahul123"))
        self.assertFalse(validate_name(""))

    def test_validate_age_within_range(self):
        ok, age = validate_age("21")
        self.assertTrue(ok)
        self.assertEqual(age, 21)

    def test_validate_age_out_of_range(self):
        ok, age = validate_age("5")
        self.assertFalse(ok)
        self.assertIsNone(age)

    def test_validate_age_non_numeric(self):
        ok, age = validate_age("abc")
        self.assertFalse(ok)

    def test_validate_email_valid(self):
        self.assertTrue(validate_email("student@example.com"))

    def test_validate_email_invalid(self):
        self.assertFalse(validate_email("not-an-email"))
        self.assertFalse(validate_email("missing@domain"))

    def test_validate_phone_valid(self):
        self.assertTrue(validate_phone("9876543210"))

    def test_validate_phone_invalid(self):
        self.assertFalse(validate_phone("12345"))
        self.assertFalse(validate_phone("abcdefghij"))

    def test_validate_gender_normalizes_case(self):
        self.assertEqual(validate_gender("male"), "Male")
        self.assertEqual(validate_gender("FEMALE"), "Female")

    def test_validate_gender_rejects_invalid(self):
        self.assertIsNone(validate_gender("unknown"))


class TestCRUDOperations(unittest.TestCase):
    """
    Tests for CRUD functions using mocked database calls.
    We patch operations.execute_query so no real MySQL connection
    is ever needed to run these tests.
    """

    @patch("operations.execute_query")
    def test_count_students(self, mock_execute):
        mock_execute.return_value = {"total": 4}
        with patch("builtins.print") as mock_print:
            operations.count_students()
            mock_execute.assert_called_once()
            mock_print.assert_any_call("Total Students: 4")

    @patch("operations.execute_query")
    def test_view_students_empty(self, mock_execute):
        mock_execute.return_value = []
        with patch("builtins.print") as mock_print:
            operations.view_students()
            mock_print.assert_any_call("No students found.")

    @patch("operations.execute_query")
    @patch("builtins.input", side_effect=["1", "1"])
    def test_search_by_id(self, mock_input, mock_execute):
        mock_execute.return_value = [{
            "student_id": 1, "first_name": "Rahul", "last_name": "Sharma",
            "gender": "Male", "age": 20, "department": "CS", "course": "B.Tech",
            "email": "rahul@example.com", "phone": "9876543210",
        }]
        operations.search_student()
        args, kwargs = mock_execute.call_args
        self.assertIn("WHERE student_id", args[0])

    @patch("operations.execute_query")
    @patch("builtins.input", side_effect=["y"])
    def test_delete_student_confirmed(self, mock_input, mock_execute):
        # First call: lookup (fetchone). Second call: DELETE.
        mock_execute.side_effect = [
            {"student_id": 1, "first_name": "Rahul", "last_name": "Sharma",
             "gender": "Male", "age": 20, "department": "CS", "course": "B.Tech",
             "email": "rahul@example.com", "phone": "9876543210",
             "address": "Hyderabad", "admission_date": "2023-08-01"},
            1,
        ]
        with patch("builtins.input", side_effect=["1", "y"]):
            operations.delete_student()
        self.assertEqual(mock_execute.call_count, 2)

    @patch("operations.execute_query")
    @patch("builtins.input", side_effect=["999", "n"])
    def test_delete_student_cancelled(self, mock_input, mock_execute):
        mock_execute.return_value = {
            "student_id": 999, "first_name": "Test", "last_name": "User",
            "gender": "Male", "age": 20, "department": "CS", "course": "B.Tech",
            "email": "test@example.com", "phone": "9876543210",
            "address": "N/A", "admission_date": "2023-08-01",
        }
        operations.delete_student()
        # Only the lookup call should happen, no DELETE call
        self.assertEqual(mock_execute.call_count, 1)


if __name__ == "__main__":
    unittest.main()
