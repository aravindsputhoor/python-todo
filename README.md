# To-Do App (Python + MySQL)

A console-based To-Do list manager backed by a MySQL database, with full CRUD
support: add, view, search, update, complete/uncomplete, and delete tasks.

## Project structure

```
todo_app/
├── schema.sql            # creates the database and tasks table
├── db.py                 # MySQL connection pool / config
├── task_repository.py    # data access layer (all SQL lives here)
├── todo.py                # CLI application (run this)
├── requirements.txt
└── README.md
```

## 1. Prerequisites

- Python 3.8+
- A running MySQL server (local or remote)

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Create the database

Run the schema script against your MySQL server. You'll be prompted for your
MySQL root/user password:

```bash
mysql -u root -p < schema.sql
```

This creates a `todo_db` database with a `tasks` table.

## 4. Configure credentials

The app reads connection settings from environment variables (recommended),
falling back to defaults in `db.py`:

| Variable            | Default     |
|---------------------|-------------|
| `TODO_DB_HOST`       | `localhost` |
| `TODO_DB_USER`       | `root`      |
| `TODO_DB_PASSWORD`   | *(empty)*   |
| `TODO_DB_NAME`       | `todo_db`   |
| `TODO_DB_PORT`       | `3306`      |

Example (Linux/macOS):

```bash
export TODO_DB_USER=root
export TODO_DB_PASSWORD=your_password
export TODO_DB_NAME=todo_db
```

Example (Windows PowerShell):

```powershell
$env:TODO_DB_USER="root"
$env:TODO_DB_PASSWORD="your_password"
```

Alternatively, just edit the `DEFAULT_CONFIG` dictionary directly in `db.py`.

## 5. Run the app

```bash
python todo.py
```

You'll see a menu:

```
==================================================
                    TO-DO APP
==================================================

 1. Add a task
 2. View all tasks
 3. View pending tasks only
 4. Search tasks
 5. Update a task
 6. Mark task complete / incomplete
 7. Delete a task
 8. Exit
```

## Database schema

```sql
CREATE TABLE tasks (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(255)      NOT NULL,
    description   TEXT,
    priority      ENUM('Low','Medium','High') NOT NULL DEFAULT 'Medium',
    due_date      DATE              NULL,
    is_completed  BOOLEAN           NOT NULL DEFAULT FALSE,
    created_at    TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP
                                    ON UPDATE CURRENT_TIMESTAMP
);
```

## Notes / possible extensions

- Swap the CLI in `todo.py` for a Flask/FastAPI web layer — `task_repository.py`
  already separates data access from the interface, so this is a drop-in change.
- Add user accounts by adding a `user_id` column and filtering queries by user.
- Add recurring tasks, tags/categories, or reminders as new columns/tables.
