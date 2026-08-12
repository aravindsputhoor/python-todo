"""
todo.py
Console-based To-Do application backed by MySQL.

Run with:  python todo.py
"""

from datetime import datetime
from task_repository import TaskRepository

PRIORITIES = ("Low", "Medium", "High")


def print_header(text):
    print("\n" + "=" * 50)
    print(text.center(50))
    print("=" * 50)


def print_menu():
    print_header("TO-DO APP")
    print("""
 1. Add a task
 2. View all tasks
 3. View pending tasks only
 4. Search tasks
 5. Update a task
 6. Mark task complete / incomplete
 7. Delete a task
 8. Exit
""")


def prompt_priority(default="Medium"):
    raw = input(f"Priority (Low/Medium/High) [{default}]: ").strip().title()
    return raw if raw in PRIORITIES else default


def prompt_date(label="Due date"):
    raw = input(f"{label} (YYYY-MM-DD, leave blank for none): ").strip()
    if not raw:
        return None
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        print("  Invalid date format, ignoring due date.")
        return None


def format_task(t):
    status = "✔ Done" if t["is_completed"] else "◻ Pending"
    due = t["due_date"] if t["due_date"] else "—"
    return (
        f"[{t['id']:>3}] {status:<10} | {t['priority']:<6} | "
        f"Due: {due:<10} | {t['title']}"
    )


def print_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.\n")
        return
    print()
    for t in tasks:
        print(format_task(t))
        if t.get("description"):
            print(f"        -> {t['description']}")
    print()


def add_task():
    print_header("ADD TASK")
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty. Cancelled.")
        return
    description = input("Description (optional): ").strip()
    priority = prompt_priority()
    due_date = prompt_date()

    task_id = TaskRepository.add_task(title, description, priority, due_date)
    print(f"\nTask added with ID {task_id}.")


def view_all_tasks():
    print_header("ALL TASKS")
    tasks = TaskRepository.get_all_tasks(include_completed=True)
    print_tasks(tasks)


def view_pending_tasks():
    print_header("PENDING TASKS")
    tasks = TaskRepository.get_all_tasks(include_completed=False)
    print_tasks(tasks)


def search_tasks():
    print_header("SEARCH TASKS")
    keyword = input("Enter keyword: ").strip()
    if not keyword:
        print("Empty search, cancelled.")
        return
    tasks = TaskRepository.search_tasks(keyword)
    print_tasks(tasks)


def update_task():
    print_header("UPDATE TASK")
    try:
        task_id = int(input("Task ID to update: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    task = TaskRepository.get_task_by_id(task_id)
    if not task:
        print("Task not found.")
        return

    print(f"Editing: {task['title']}  (leave a field blank to keep it unchanged)")
    title = input(f"New title [{task['title']}]: ").strip() or None
    description = input(f"New description [{task['description'] or ''}]: ").strip() or None
    priority_raw = input(f"New priority (Low/Medium/High) [{task['priority']}]: ").strip().title()
    priority = priority_raw if priority_raw in PRIORITIES else None
    due_date = prompt_date("New due date") or None

    updated = TaskRepository.update_task(
        task_id, title=title, description=description,
        priority=priority, due_date=due_date
    )
    print("Task updated." if updated else "No changes made.")


def toggle_complete():
    print_header("MARK COMPLETE / INCOMPLETE")
    try:
        task_id = int(input("Task ID: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    task = TaskRepository.get_task_by_id(task_id)
    if not task:
        print("Task not found.")
        return

    new_status = not task["is_completed"]
    TaskRepository.mark_complete(task_id, new_status)
    print(f"Task '{task['title']}' marked as {'complete' if new_status else 'incomplete'}.")


def delete_task():
    print_header("DELETE TASK")
    try:
        task_id = int(input("Task ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    task = TaskRepository.get_task_by_id(task_id)
    if not task:
        print("Task not found.")
        return

    confirm = input(f"Delete '{task['title']}'? (y/N): ").strip().lower()
    if confirm == "y":
        TaskRepository.delete_task(task_id)
        print("Task deleted.")
    else:
        print("Cancelled.")


def main():
    actions = {
        "1": add_task,
        "2": view_all_tasks,
        "3": view_pending_tasks,
        "4": search_tasks,
        "5": update_task,
        "6": toggle_complete,
        "7": delete_task,
    }

    while True:
        print_menu()
        choice = input("Choose an option (1-8): ").strip()
        if choice == "8":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except RuntimeError as e:
                print(f"Error: {e}")
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
