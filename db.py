"""
db.py
Handles the MySQL database connection for the To-Do app.

Configure your credentials either by:
  1. Setting environment variables (recommended), or
  2. Editing the DEFAULT_CONFIG values below.

Environment variables used:
  TODO_DB_HOST      (default: localhost)
  TODO_DB_USER      (default: root)
  TODO_DB_PASSWORD  (default: "")
  TODO_DB_NAME      (default: todo_db)
  TODO_DB_PORT      (default: 3306)
"""

import os
import sys
import mysql.connector
from mysql.connector import Error, pooling

DEFAULT_CONFIG = {
    "host": os.getenv("TODO_DB_HOST", "localhost"),
    "user": os.getenv("TODO_DB_USER", "root"),
    "password": os.getenv("TODO_DB_PASSWORD", ""),
    "database": os.getenv("TODO_DB_NAME", "todo_db"),
    "port": int(os.getenv("TODO_DB_PORT", "3306")),
}

_pool = None


def get_pool():
    """Create (once) and return a connection pool."""
    global _pool
    if _pool is None:
        try:
            _pool = pooling.MySQLConnectionPool(
                pool_name="todo_pool",
                pool_size=5,
                **DEFAULT_CONFIG
            )
        except Error as e:
            print(f"[FATAL] Could not connect to MySQL: {e}")
            print("Check that MySQL is running and your credentials/env vars are correct.")
            sys.exit(1)
    return _pool


def get_connection():
    """Get a single connection from the pool."""
    return get_pool().get_connection()
