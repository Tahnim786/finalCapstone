import os
from datetime import datetime

# Constants
DATETIME_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"

# Function to register a user
def reg_user():
    """
    Registers a new user by prompting for username and password.
    Checks if the username already exists in the user.txt file and displays an error message if it does.
    """
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Check if username already exists
    if username in username_password:
        print("Username already exists. Please try again with a different username.")
        return

    # Add the new user to the user.txt file and the username_password dictionary
    with open("user.txt", "a") as user_file:
        user_file.write(f"{username},{password}\n")
    username_password[username] = password
    print("User registered successfully.")

# Function to add a new task
def add_task():
    """
    Adds a new task by prompting for task details.
    Saves the task to the tasks.txt file.
    """
    username = input("Enter the username of the person the task is assigned to: ")
    title = input("Enter the title of the task: ")
    description = input("Enter the description of the task: ")
    due_date = input("Enter the due date of the task (YYYY-MM-DD HH:MM:SS): ")

    # Validate the due date format
    try:
        due_date = datetime.strptime(due_date, DATETIME_STRING_FORMAT)
    except ValueError:
        print("Invalid date format. Task not added.")
        return

    # Add the task to the tasks.txt file and the task_list
    with open("tasks.txt", "a") as tasks_file:
        tasks_file.write(f"{username},{title},{description},no,{due_date.strftime(DATETIME_STRING_FORMAT)}\n")
    task_list.append({
        'username': username,
        'title': title,
        'description': description,
        'completed': 'no',
        'due_date': due_date
    })
    print("Task added successfully.")

# Function to view all tasks
def view_all():
    """
    Displays all tasks listed in the tasks.txt file.
    """
    if not task_list:
        print("No tasks found.")
        return

    print("All Tasks:")
    for i, task in enumerate(task_list):
        print(f"Task {i+1}:")
        print(f"Username: {task['username']}")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Completed: {task['completed']}")
        print(f"Due Date: {task['due_date']}")
        print()

# Function to view tasks assigned to the current user
def view_mine():
    """
    Displays tasks that have been assigned to the current user.
    """
    if not curr_user:
        print("Please log in to view your tasks.")
        return

    user_tasks = [task for task in task_list if task['username'] == curr_user]

    if not user_tasks:
        print("No tasks found.")
        return

    print("Your Tasks:")
    for i, task in enumerate(user_tasks):
        print(f"Task {i+1}:")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Completed: {task['completed']}")
        print(f"Due Date: {task['due_date']}")
        print()

# Function to generate reports
def generate_reports():
    """
    Generates two text files: task_overview.txt and user_overview.txt.
    task_overview.txt contains overall statistics about the tasks.
    user_overview.txt contains statistics about each user and their assigned tasks.
    """
    total_tasks = len(task_list)
    tasks_completed = sum(1 for task in task_list if task['completed'] == 'yes')
    tasks_incomplete = total_tasks - tasks_completed
    tasks_overdue = sum(1 for task in task_list if task['completed'] == 'no' and task['due_date'] < datetime.now())
    tasks_completed_percentage = (tasks_completed / total_tasks) * 100 if total_tasks > 0 else 0
    tasks_incomplete_percentage = (tasks_incomplete / total_tasks) * 100 if total_tasks > 0 else 0
    tasks_overdue_percentage = (tasks_overdue / total_tasks) * 100 if total_tasks > 0 else 0

    task_overview = f"Total tasks: {total_tasks}\n"
    task_overview += f"Tasks completed: {tasks_completed}\n"
    task_overview += f"Tasks incomplete: {tasks_incomplete}\n"
    task_overview += f"Tasks overdue: {tasks_overdue}\n"
    task_overview += f"Percentage of tasks incomplete: {tasks_incomplete_percentage:.2f}%\n"
    task_overview += f"Percentage of tasks overdue: {tasks_overdue_percentage:.2f}%\n"

    user_overview = {}
    total_users = len(username_password)
    for username in username_password:
        user_tasks = [task for task in task_list if task['username'] == username]
        tasks_assigned = len(user_tasks)
        tasks_assigned_percentage = (tasks_assigned / total_tasks) * 100 if total_tasks > 0 else 0
        tasks_completed = sum(1 for task in user_tasks if task['completed'] == 'yes')
        tasks_completed_percentage = (tasks_completed / tasks_assigned) * 100 if tasks_assigned > 0 else 0
        tasks_incomplete = tasks_assigned - tasks_completed
        tasks_overdue = sum(1 for task in user_tasks if task['completed'] == 'no' and task['due_date'] < datetime.now())
        tasks_overdue_percentage = (tasks_overdue / tasks_assigned) * 100 if tasks_assigned > 0 else 0

        user_overview[username] = {
            'tasks_assigned': tasks_assigned,
            'tasks_assigned_percentage': tasks_assigned_percentage,
            'tasks_completed_percentage': tasks_completed_percentage,
            'tasks_incomplete_percentage': tasks_incomplete_percentage,
            'tasks_overdue_percentage': tasks_overdue_percentage
        }

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(task_overview)

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Total users: {total_users}\n")
        user_overview_file.write(f"Total tasks: {total_tasks}\n")
        for username, overview in user_overview.items():
            user_overview_file.write(f"Username: {username}\n")
            user_overview_file.write(f"Tasks assigned: {overview['tasks_assigned']}\n")
            user_overview_file.write(f"Percentage of tasks assigned: {overview['tasks_assigned_percentage']:.2f}%\n")
            user_overview_file.write(f"Percentage of tasks completed: {overview['tasks_completed_percentage']:.2f}%\n")
            user_overview_file.write(f"Percentage of tasks incomplete: {overview['tasks_incomplete_percentage']:.2f}%\n")
            user_overview_file.write(f"Percentage of tasks overdue: {overview['tasks_overdue_percentage']:.2f}%\n")
            user_overview_file.write("\n")

    print("Reports generated successfully.")

# Function to display statistics
def display_statistics():
    """
    Displays statistics read from task_overview.txt and user_overview.txt.
    If the text files don't exist, generates the reports first.
    """
    if not os.path.isfile("task_overview.txt") or not os.path.isfile("user_overview.txt"):
        generate_reports()

    with open("task_overview.txt", "r") as task_overview_file:
        task_overview = task_overview_file.read()
        print("Task Overview:")
        print(task_overview)

    with open("user_overview.txt", "r") as user_overview_file:
        user_overview = user_overview_file.read()
        print("User Overview:")
        print(user_overview)

# Function to exit the program
def exit_program():
    """
    Exits the program and writes the updated user and task information to files.
    """
    with open("users.txt", "w") as user_file:
        for username, password in username_password.items():
            user_file.write(f"{username},{password}\n")

    with open("tasks.txt", "w") as tasks_file:
        for task in task_list:
            tasks_file.write(f"{task['username']},{task['title']},{task['description']},{task['completed']},{task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n")

    print("Program exited successfully.")

# Initialize the user credentials dictionary
username_password = {}

# Read user credentials from user.txt file
with open("user.txt", "r") as user_file:
    for line in user_file:
        username, password = line.strip().split(",")
        username_password[username] = password

# Initialize the task list
task_list = []

# Read tasks from tasks.txt file
with open("tasks.txt", "r") as tasks_file:
    for line in tasks_file:
        task_data = line.strip().split(",")
        username, title, description, completed, due_date_str = task_data
        due_date = datetime.strptime(due_date_str, DATETIME_STRING_FORMAT)
        task_list.append({
            'username': username,
            'title': title,
            'description': description,
            'completed': completed,
            'due_date': due_date
        })

# Main program loop
curr_user = None
while True:
    print("Please select one of the following options:")
    print("r - Register user")
    print("a - Add task")
    print("va - View all tasks")
    print("vm - View my tasks")
    print("gr - Generate reports")
    print("ds - Display statistics")
    print("e - Exit")

    choice = input("Enter your choice: ")

    if choice == "r":
        reg_user()
    elif choice == "a":
        add_task()
    elif choice == "va":
        view_all()
    elif choice == "vm":
        view_mine()
    elif choice == "gr":
        generate_reports()
    elif choice == "ds":
        display_statistics()
    elif choice == "e":
        exit_program()
        break
    else:
        print("Invalid choice. Please try again.")
