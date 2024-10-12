import json
from datetime import datetime, timedelta

# Define the Task class
class Task:
    def __init__(self, title, description, category, priority='Medium', due_date=None, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.due_date = due_date  # Expected format: 'YYYY-MM-DD'
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def edit_task(self, title=None, description=None, category=None, priority=None, due_date=None):
        if title:
            self.title = title
        if description:
            self.description = description
        if category:
            self.category = category
        if priority:
            self.priority = priority
        if due_date:
            self.due_date = due_date

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            priority=data.get('priority', 'Medium'),
            due_date=data.get('due_date'),
            completed=data.get('completed', False)
        )

    def __repr__(self):
        status = "✅" if self.completed else "❌"
        due = f", Due: {self.due_date}" if self.due_date else ""
        return f"[{status}] {self.title} - {self.description} (Category: {self.category}, Priority: {self.priority}{due})"

# File handling functions
def save_tasks(tasks, file_name='tasks.json'):
    with open(file_name, 'w') as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)

def load_tasks(file_name='tasks.json'):
    try:
        with open(file_name, 'r') as f:
            tasks_data = json.load(f)
            return [Task.from_dict(task) for task in tasks_data]
    except FileNotFoundError:
        return []

# Task management functions
def display_tasks(tasks, filter_option=None):
    if not tasks:
        print("No tasks available.")
        return

    filtered_tasks = tasks
    if filter_option == 'completed':
        filtered_tasks = [task for task in tasks if task.completed]
    elif filter_option == 'pending':
        filtered_tasks = [task for task in tasks if not task.completed]
    elif filter_option == 'due_soon':
        today = datetime.now().date()
        soon = today + timedelta(days=3)
        filtered_tasks = [
            task for task in tasks
            if task.due_date and today <= datetime.strptime(task.due_date, '%Y-%m-%d').date() <= soon
        ]

    if not filtered_tasks:
        print(f"No tasks found for the filter: {filter_option}")
        return

    for idx, task in enumerate(filtered_tasks, 1):
        print(f"{idx}. {task}")

def add_task(tasks):
    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    category = input("Enter task category (e.g., Work, Personal, Urgent): ").strip()
    priority = input("Enter task priority (Low, Medium, High) [Default: Medium]: ").strip().capitalize() or 'Medium'
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip()
    if due_date:
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Due date will be set to None.")
            due_date = None
    else:
        due_date = None

    new_task = Task(title, description, category, priority, due_date)
    tasks.append(new_task)
    print("Task added successfully!")

def mark_task_completed(tasks):
    pending_tasks = [task for task in tasks if not task.completed]
    if not pending_tasks:
        print("No pending tasks to mark as completed.")
        return

    display_tasks(pending_tasks)
    try:
        task_num = int(input("Enter the task number to mark as completed: "))
        if 1 <= task_num <= len(pending_tasks):
            pending_tasks[task_num - 1].mark_completed()
            print("Task marked as completed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def edit_task(tasks):
    if not tasks:
        print("No tasks available to edit.")
        return

    display_tasks(tasks)
    try:
        task_num = int(input("Enter the task number to edit: "))
        if 1 <= task_num <= len(tasks):
            task = tasks[task_num - 1]
            print("Leave a field blank to keep it unchanged.")
            new_title = input(f"Enter new title [{task.title}]: ").strip()
            new_description = input(f"Enter new description [{task.description}]: ").strip()
            new_category = input(f"Enter new category [{task.category}]: ").strip()
            new_priority = input(f"Enter new priority (Low, Medium, High) [{task.priority}]: ").strip().capitalize()
            new_due_date = input(f"Enter new due date (YYYY-MM-DD) [{task.due_date}]: ").strip()

            if new_due_date:
                try:
                    datetime.strptime(new_due_date, '%Y-%m-%d')
                except ValueError:
                    print("Invalid date format. Due date will not be changed.")
                    new_due_date = None
            else:
                new_due_date = None

            task.edit_task(
                title=new_title or None,
                description=new_description or None,
                category=new_category or None,
                priority=new_priority or None,
                due_date=new_due_date or None
            )
            print("Task updated successfully.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def delete_task(tasks):
    if not tasks:
        print("No tasks available to delete.")
        return

    display_tasks(tasks)
    try:
        task_num = int(input("Enter the task number to delete: "))
        if 1 <= task_num <= len(tasks):
            deleted_task = tasks.pop(task_num - 1)
            print(f"Task '{deleted_task.title}' deleted successfully.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# Main menu function
def main():
    tasks = load_tasks()

    while True:
        print("\n=== Personal To-Do List Manager ===")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Completed Tasks")
        print("4. View Pending Tasks")
        print("5. View Tasks Due Soon")
        print("6. Mark Task as Completed")
        print("7. Edit Task")
        print("8. Delete Task")
        print("9. Exit")

        choice = input("Choose an option (1-9): ").strip()

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            print("\n--- All Tasks ---")
            display_tasks(tasks)
        elif choice == '3':
            print("\n--- Completed Tasks ---")
            display_tasks(tasks, filter_option='completed')
        elif choice == '4':
            print("\n--- Pending Tasks ---")
            display_tasks(tasks, filter_option='pending')
        elif choice == '5':
            print("\n--- Tasks Due Soon (within 3 days) ---")
            display_tasks(tasks, filter_option='due_soon')
        elif choice == '6':
            mark_task_completed(tasks)
        elif choice == '7':
            edit_task(tasks)
        elif choice == '8':
            delete_task(tasks)
        elif choice == '9':
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 9.")

# Run the application
if __name__ == "__main__":
    main()
