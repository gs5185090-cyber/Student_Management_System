"""
database.py
------------
Handles all direct communication with MySQL.

Design notes:
- get_connection() is the single place that knows how to open a
  connection to MySQL. Every other module asks this module for a
  connection instead of calling mysql.connector directly, so if the
  connection strategy ever changes (pooling, different driver, etc.)
  only this file needs to change.
- Errors are caught here and re-raised as a custom DatabaseError so
  the rest of the app doesn't need to know about mysql.connector's
  specific exception types.
"""

import logging
import mysql.connector
from mysql.connector import Error as MySQLError

from config import DB_CONFIG

logger = logging.getLogger("sms")


class DatabaseError(Exception):
    """Raised whenever a database operation fails."""
    pass


def get_connection():
    """
    Create and return a new MySQL connection using the credentials
    defined in config.py.

    Returns:
        mysql.connector.connection.MySQLConnection

    Raises:
        DatabaseError: if the connection cannot be established
                        (wrong credentials, MySQL server down, etc.)
    """
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
        )
        if connection.is_connected():
            return connection
        raise DatabaseError("Failed to connect to MySQL: connection not established.")
    except MySQLError as err:
        logger.error(f"Database connection error: {err}")
        raise DatabaseError(f"Could not connect to database: {err}") from err


def execute_query(query, params=None, fetch=False, fetchone=False):
    """
    Generic helper to run a query with proper connection/cursor cleanup.

    Args:
        query (str): SQL query with %s placeholders.
        params (tuple): values to bind to the placeholders.
        fetch (bool): if True, returns all rows (SELECT statements).
        fetchone (bool): if True, returns a single row.

    Returns:
        - list of rows (fetch=True)
        - single row / None (fetchone=True)
        - number of affected rows (INSERT/UPDATE/DELETE)
    """
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if fetch:
            result = cursor.fetchall()
        elif fetchone:
            result = cursor.fetchone()
        else:
            connection.commit()
            result = cursor.rowcount

        return result

    except MySQLError as err:
        logger.error(f"Query failed: {query} | params={params} | error={err}")
        raise DatabaseError(f"Query execution failed: {err}") from err
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
