import argparse
import sqlite3
import sys

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()

# Add a new task
def add_task(task_description):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task_description, 0))
    conn.commit()
    conn.close()
    print(f"Task added: '{task_description}'")

# List all tasks
def list_tasks():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print("No tasks found.")
    else:
        for task_id, task, completed in tasks:
            status = "✅" if completed else "❌"
            print(f"{task_id}. {task} [{status}]")

# Mark a task as completed
def complete_task(task_id):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    if cursor.rowcount:
        print(f"Task {task_id} marked as completed.")
    else:
        print(f"Task {task_id} not found.")
    conn.close()

# Remove a task
def remove_task(task_id):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    if cursor.rowcount:
        print(f"Task {task_id} removed.")
    else:
        print(f"Task {task_id} not found.")
    conn.close()

# Display help
def display_help():
    print("""
Todo List Manager

Usage:
    python todo_manager.py add <task_description>      Add a new task
    python todo_manager.py list                        List all tasks
    python todo_manager.py complete <task_id>          Mark a task as completed
    python todo_manager.py remove <task_id>            Remove a task
    python todo_manager.py -h                         Display this help message
""")

def main():
    # Initialize the database
    init_db()

    parser = argparse.ArgumentParser(description="Todo List Manager with SQLite")
    parser.add_argument("command", choices=["add", "list", "complete", "remove"], help="Command to execute")
    parser.add_argument("args", nargs="*", help="Arguments for the command")
    args = parser.parse_args()

    if args.command == "add":
        if args.args:
            add_task(" ".join(args.args))
        else:
            print("Error: Task description is required for 'add' command.")
            sys.exit(1)

    elif args.command == "list":
        list_tasks()

    elif args.command == "complete":
        if args.args and args.args[0].isdigit():
            complete_task(int(args.args[0]))
        else:
            print("Error: Task ID (number) is required for 'complete' command.")
            sys.exit(1)

    elif args.command == "remove":
        if args.args and args.args[0].isdigit():
            remove_task(int(args.args[0]))
        else:
            print("Error: Task ID (number) is required for 'remove' command.")
            sys.exit(1)

    else:
        display_help()

if __name__ == "__main__":
    main()

