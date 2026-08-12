"""
task_repository.py
All SQL queries live here (data access layer), separate from CLI/UI logic.
"""

from mysql.connector import Error
from db import get_connection


class TaskRepository:

    @staticmethod
    def add_task(title, description, priority, due_date):
        query = """
            INSERT INTO tasks (title, description, priority, due_date)
            VALUES (%s, %s, %s, %s)
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (title, description, priority, due_date))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Failed to add task: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_all_tasks(include_completed=True):
        query = "SELECT * FROM tasks"
        if not include_completed:
            query += " WHERE is_completed = FALSE"
        query += " ORDER BY is_completed ASC, due_date IS NULL, due_date ASC, priority DESC"

        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_task_by_id(task_id):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update_task(task_id, title=None, description=None, priority=None, due_date=None):
        fields = []
        values = []
        if title is not None:
            fields.append("title = %s")
            values.append(title)
        if description is not None:
            fields.append("description = %s")
            values.append(description)
        if priority is not None:
            fields.append("priority = %s")
            values.append(priority)
        if due_date is not None:
            fields.append("due_date = %s")
            values.append(due_date)

        if not fields:
            return False

        values.append(task_id)
        query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = %s"

        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Failed to update task: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def mark_complete(task_id, completed=True):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET is_completed = %s WHERE id = %s",
                (completed, task_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Failed to update task status: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete_task(task_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Failed to delete task: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search_tasks(keyword):
        query = """
            SELECT * FROM tasks
            WHERE title LIKE %s OR description LIKE %s
            ORDER BY is_completed ASC, due_date IS NULL, due_date ASC
        """
        like_pattern = f"%{keyword}%"
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (like_pattern, like_pattern))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
