# =====importing libraries===========
"""This is the section where you will import libraries"""

# After research I found out about the datetime module, it's type and
# attributes. Also the strftime function that returns a string,
# representing date and time and strptime function for parsing date and
# time strings.
#
# I also learnt about the re module and the fullmatch function that
# returns a match

import os
import re
from datetime import datetime

# ====Functions Section====
"""These function will be called to print the tasks in a user-friendly
manner
"""


def print_task(line, task_id=None):
    print("—" * 79, "\n")
    if task_id:  #  Print task ID if provided
        print(f"Task ID:\t\t{task_id}")
    print(f"Task:\t\t\t{line[1]}")
    print(f"Assigned to:\t\t{line[0]}")
    print(f"Date assigned:\t\t{line[3]}")
    print(f"Due date:\t\t{line[4]}")
    print("Task Complete?:\t\tNo")
    print(f"Task Description:\n {line[2]}\n")


"""This function contains the registration process. It allows users to 
be registered and stores their details in the user.txt file as follows:
    - Request input of a new username
    - Check if the username already exists
    - Request input of a new password
    - Request input of password confirmation.
    - Check if the new password and confirmed password are the 
    same
    - If they are the same, add them to the user.txt file,
        otherwise present a relevant message
"""


def reg_user(users):
    print("Welcome to the registration process!\n")
    new_username = input("Enter a new username: ").lower()
    while new_username in users:
        print("Username already exists")
        new_username = input("Enter a new username: ").lower()
    password = input("Enter password: ")
    password_confirmation = input("Enter password again to confirm: ")
    while password != password_confirmation:
        print("Passwords don't match")
        password = input("Enter password: ")
        password_confirmation = input("Enter password again to confirm: ")

    with open("user.txt", "a") as file:
        file.write(f"\n{new_username}, {password}")

    users[new_username] = password  #  Update users

    print("\nUser added successfully")


def add_task(users):
    """This function will allow a user to add a new task to task.txt
    file as follows:
        - Prompt a user for the following:
            - the username of the person whom the task is assigned
            to (check if the user exists),
            - the title of the task,
            - the description of the task, and
            - the due date of the task.
        - Then, get the current date.
        - Add the data to the file task.txt
        - Remember to include 'No' to indicate that the task is not
        complete.

    Sanitise the user input. Ensure no unecessary spaces in the
    string. Check if the date format is valid, then parse it and
    finally format it to our use case

    Append the task to the tasks.txt file if not already in the
    file, Go the beginning of the file and read all the lines
    into a list. Then go back to the end of the file and add the
    task if it's not already in the list
    """
    task_username = input(
        "Enter the username of the person whom this \
task is assigned to: "
    ).lower()
    if task_username in users:
        title = input("Enter the title of the task: ").strip()
        title = re.sub(r" +", " ", title)
        description = input("Enter the description of the task: ").strip()
        description = re.sub(r" +", " ", description)
        due_date = input(
            "Enter the due_date of the task in this format \
'dd-mm-yyyy' e.g 20-10-2019: "
        ).strip()
        due_date = re.sub(r" +", "", due_date)
        while not re.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}", due_date):
            print("Date you entered is invalid")
            due_date = input(
                "Enter the due_date of the task in this \
format 'dd-mm-yyyy' e.g 20-10-2019: "
            ).strip()
            due_date = re.sub(r" +", "", due_date)
        due_date = datetime.strptime(due_date, "%d-%m-%Y").strftime("%d %b %Y")
        today = datetime.now().strftime("%d %b %Y")

        with open("tasks.txt", "a+") as file:
            file.seek(0, 0)
            tasks = file.readlines()
            file.seek(0, 2)
            task = f"{task_username}, \
{title}, {description}, {today}, {due_date}, No"
            if task not in tasks:
                file.write("\n" + task)
                print("\nTask added successfully")
    else:
        print("\nUser does not exist")


def view_all():
    """This function will read the tasks from tasks.txt file and
    print to the console in a user-friendly manner.
    You can do it in this way:
        - Read a line from the file.
        - Split that line where there is comma and space.
        - Then print the results in a user-friendly manner.
    """
    with open("tasks.txt", "r") as file:
        task_found = False  # Handle case of no task found

        for line in file:
            task_found = True
            line = line.split(", ")
            print_task(line)  #  Print in a user-friendly manner

        if task_found:
            print("—" * 79)
        else:
            print("No tasks found")


def view_mine(username):
    """This function will read the task from task.txt file and
    print to the console in a user-friendly manner.
    You can do it in this way:
        - Read a line from the file
        - Split the line where there is comma and space.
        - Check if the username of the person logged in is the same
            as the username you have read from the file.
        - If they are the same you print the task

    Also it makes sure that each task is displayed with a
    corresponding number that can be used to identify the task.
    Allows the user to select either a specific task
    (by entering a number) or input "-1" to return to the main menu.
    If the user selects a specific task, they should be able to
    choose to either mark the task as complete or edit the task.
    If the user chooses to mark a task as complete, the "Yes"/"No"
    value that describes whether the task has been completed
    or not should be changed to "Yes".
    If the user chooses to edit a task, the username of the person
    to whom the task is assigned or the due date of the task can
    be edited. The task can only be edited if it has not yet been
    completed.
    """
    tasks = []  #  Task list

    with open("tasks.txt", "r") as file:
        username_found = False  # Handle if no task assigned to user

        for line in file:
            tasks.append(line)
            line = line.split(", ")
            if line[0] == username:
                username_found = True

                # Print in a user-friendly manner, with task ID
                print_task(line, len(tasks))

        if username_found:
            print("—" * 79)
        else:
            print("No tasks assigned to you")

    if username_found:  #  If tasks printed, allow user to select a task
        task_id = input(
            "\nPlease select a specific task by entering the task ID or -1 to \
return to the main menu: "
        )

        # Check if the user wants to return to the main menu
        # Also check if the task ID entered is valid
        if (
            task_id != "-1" 
            and task_id.isdigit() 
            and int(task_id) <= len(tasks)
        ):
            task = tasks[int(task_id) - 1] #  Task the user will edit
            task = task.strip("\n").split(", ")
            if task[5] == "Yes":  #  Check if the task is completed
                print("\nYou can't edit a completed task")
            else:
                action = input(
                    "\nDo you want to mark the task as complete or \
edit the task? Type 'complete' or 'edit': "
                ).lower()
                if action == "complete":
                    task[5] = "Yes"
                elif action == "edit":
                    change_username = input(
                        "\nDo you want to change the username? Type \
'yes' or 'no': "
                    ).lower()
                    if change_username == "yes":
                        new_username = input(
                            "\nEnter the new username: "
                        ).lower()

                        # Ask the user to enter new username that exists
                        while new_username not in users:
                            print("\nUsername doesn't exist")
                            new_username = input(
                                "\nEnter the new username: "
                            ).lower()
                        task[0] = new_username
                    elif change_username != "no":
                        print(
                            "You've entered an invalid input. Enter 'yes' or \
'no'"
                        )
                    change_due_date = input(
                        "\nDo you want to change the due date? Type \
'yes' or 'no': "
                    ).lower()
                    if change_due_date == "yes":
                        new_due_date = input(
                            "\nEnter the new due date of the \
task in this format 'dd-mm-yyyy' e.g 20-10-2019: "
                        ).strip()

                        # Remove extra spaces from the due date
                        new_due_date = re.sub(r" +", "", new_due_date)

                        # Ask user for a valid due date not in the past
                        while (
                            not re.fullmatch(
                                r"\d{1,2}-\d{1,2}-\d{4}", new_due_date
                            )
                            or datetime.strptime(
                                new_due_date, "%d-%m-%Y"
                            ) < datetime.now()
                        ):
                            print("\nDate you entered is invalid or in the \
past")
                            new_due_date = input("\nEnter the new due date of \
the task in this format 'dd-mm-yyyy' e.g 20-10-2019: "
                            ).strip()
                            new_due_date = re.sub(r" +", "", new_due_date)

                        # change due date to this format 'dd mmm yyyy'
                        task[4] = datetime.strptime(
                            new_due_date, "%d-%m-%Y"
                        ).strftime(
                            "%d %b %Y"
                        )
                    elif change_due_date != "no":
                        print(
                            "You've entered an invalid input. Enter 'yes' or \
'no'"
                        )
                else:
                    print(
                        "\nYou've entered an invalid input. Enter 'complete' \
or 'edit'"
                    )

                task = ", ".join(task)

                if int(task_id) != len(tasks):
                    # Add '\n' if task is not the last task in tasks.txt
                    task += "\n"

                # Write the updated task to tasks.txt
                if tasks[int(task_id) - 1]  != task: 
                    tasks[int(task_id) - 1] = task
                    with open("tasks.txt", "w") as file:
                        file.writelines(tasks)
                        print("\nTask updated successfully")
    

def generate_reports(users):
    """When the user chooses to generate reports, two text files, called
    task_overview.txt and user_overview.txt, should be generated. Both
    these text files should output data in a user-friendly, easy to read
    manner
    task_overview.txt should contain:
        - The total number of tasks that have been generated and
        tracked using the task_manager.py.
        - The total number of completed tasks.
        - The total number of uncompleted tasks.
        - The total number of tasks that haven’t been completed and
        that are overdue.
        - The percentage of tasks that are incomplete.
        - The percentage of tasks that are overdue.
    user_overview.txt should contain:
        - The total number of users registered with task_manager.py.
        - The total number of tasks that have been generated and
        tracked using task_manager.py.
        For each user also describe:
            - The total number of tasks assigned to that user.
            - The percentage of the total number of tasks that have
            been assigned to that user
            - The percentage of the tasks assigned to that user that
            have been completed
            - The percentage of the tasks assigned to that user that
            must still be completed
            - The percentage of the tasks assigned to that user that
            has not yet been completed and are overdue
    """
    # Notify the user that the reports are being generated
    print("Generating reports...", end="")

    users_stat = {}  #  Map username to a list of user stats
    for key in users.keys():
        # [Total tasks, Completed tasks, Uncompleted tasks, 
        # Overdue tasks]
        users_stat[key] = [0, 0, 0, 0] 
    total_tasks = 0  #  Total number of tasks that have been generated
    total_completed = 0  #  Total of tasks that have been completed
    total_uncompleted = 0  #  Total number of tasks uncompleted
    total_overdue = 0  #  Total number of tasks that are overdue
    percentage_uncompleted = 0  #  Percentage of tasks uncompleted
    percentage_overdue = 0  #  Percentage of tasks that are overdue

    with open("tasks.txt", "r") as file:
        for line in file:
            total_tasks += 1
            line = line.strip("\n").split(", ")
            users_stat[line[0]][0] += 1  #  Tasks assigned to user

            if line[-1] == "Yes":
                total_completed += 1
                users_stat[line[0]][1] += 1  # Tasks completed by user
            elif line[-1] == "No":
                total_uncompleted += 1
                users_stat[line[0]][2] += 1 #  Tasks uncompleted by user
            if (
                line[-1] == "No" 
                and line[-2] < datetime.now().strftime("%d %b %Y")
            ):
                total_overdue += 1
                users_stat[line[0]][3] += 1  #  Tasks overdue per user

    # Calculate the percentage of uncompleted and overdue tasks
    percentage_uncompleted = (total_uncompleted / total_tasks) * 100
    percentage_overdue = (total_overdue / total_tasks) * 100

    # Generate a report of the task overview
    with open("task_overview.txt", "w+") as file:
        file.write(f"{'—' * 79}\n")
        file.write(f"Total tasks:{' '*21}{total_tasks}\n")
        file.write(f"Total completed:{' '*17}{total_completed}\n")
        file.write(f"Total uncompleted:{' '*15}{total_uncompleted}\n")
        file.write(f"Total overdue:{' '*19}{total_overdue}\n")
        file.write(
            f"Percentage uncompleted:{' '*10}{percentage_uncompleted:.0f}%\n"
        ) #  To the nearest whole number
        file.write(
            f"Percentage overdue:{' '*14}{percentage_overdue:.0f}%\n"
        ) #  To the nearest whole number
        file.write("—" * 79)

    # Generate a report of user overview and write to user_overview.txt
    with open("user_overview.txt", "w+") as file:
        user_found = False  # Flag to check if tasks.txt is empty

        file.write(f"{'—' * 79}\n")
        file.write(f"Total users: {len(users)}\n")
        file.write(f"Total tasks: {total_tasks}\n")

        for key in users_stat.keys():
            user_found = True
            total_tasks_per_user = users_stat[key][0]
            percentage_of_tasks_per_user = (
                users_stat[key][0] / total_tasks
            ) * 100
            percentage_of_completed_tasks_per_user = (
                users_stat[key][1] / total_tasks_per_user
            ) * 100
            percentage_of_uncompleted_tasks_per_user = (
                users_stat[key][2] / total_tasks_per_user
            ) * 100
            percentage_of_overdue_tasks_per_user = (
                users_stat[key][3] / total_tasks_per_user
            ) * 100

            file.write(f"{'—' * 79}\n")
            file.write(f"User:{' '*28}{key}\n")
            file.write(f"Total tasks:{' '*21}{total_tasks_per_user}\n")
            file.write(
                f"Percentage of total tasks:{' '*7}\
{percentage_of_tasks_per_user:.0f}%\n"
            ) #  To the nearest whole number
            file.write(
                f"Percentage of completed tasks:{' '*3}\
{percentage_of_completed_tasks_per_user:.0f}%\n"
            ) #  To the nearest whole number
            file.write(
                f"Percentage of uncompleted tasks: \
{percentage_of_uncompleted_tasks_per_user:.0f}%\n"
            ) #  To the nearest whole number
            file.write(
                f"Percentage of overdue tasks:{' '*5}\
{percentage_of_overdue_tasks_per_user:.0f}%\n"
            ) #  To the nearest whole number

        if user_found:
            file.write("—" * 79)
        else:
            print("No tasks found for any user")

    print("Done") # Notify the user that the reports have been generated


def display_stats():

    '''The admin user is provided with a new menu option that allows
    them to display statistics. When this menu option is selected, 
    these statistics should be displayed in a user-friendly manner,
    from task_overview.txt and user_overview.txt. If these files do
    not exist, they should be generated before the statistics are
    displayed.  Prompt the user to press enter to return to the main 
    menu
    '''
    pass

    if not os.path.exists('task_overview.txt'):
        generate_reports(users)
        print()  # Make console output more readable
    
    with open('task_overview.txt', 'r') as file:
        for line in file:
            print(line, end="")

    print() # Make console output more readable
        
    with open('user_overview.txt', 'r') as file:
        for line in file:
            print(line, end="")


# ====Login Section====
"""Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and 
    passwords from the file
    - Use a while loop to validate your user name and password
"""
with open("user.txt", "r") as file:
    users = {}
    for line in file:
        line = line.strip("\n").split(", ")
        users[line[0]] = line[1]

while True:
    username = input("Enter a username: ").lower()
    if username in users:
        password = input("Enter password: ")
        while password != users[username]:
            print("You've entered an invalid password")
            password = input("Enter a valid password: ")
        break
    print("You've entered an invalid username")
print("\nYou've successfully logged in")

while True:
    # Present the menu to the user and
    # make sure that the user input is converted to lower case.
    # Only the user 'admin' is allowed to register users
    print()

    if username == "admin":
        menu = input("""Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - exit
: """).lower()
    else:
        menu = input("""Select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
e - exit
: """).lower()

    print()

    if menu == "r":
        pass
        reg_user(users)  #  Register a new user
        user_input = input("\nPress enter to return to the main menu: ")
        if user_input:
            pass

    elif menu == "a":
        pass
        add_task(users)  #  Add a new task
        user_input = input("\nPress enter to return to the main menu: ")
        if user_input:
            pass

    elif menu == "va":
        pass
        view_all()  #  View all the tasks listed in 'tasks.txt'
        user_input = input("\nPress enter to return to the main menu: ")
        if user_input:
            pass

    elif menu == "vm":
        pass
        view_mine(username) #  View tasks assigned to the logged in user
        user_input = input("\nPress enter to return to the main menu: ")
        if user_input:
            pass

    elif menu == "gr":
        pass
        generate_reports(users) #  Generate reports
        user_input = input("\nPress enter to return to the main menu: ")
        if user_input:
            pass

    elif menu == "ds":
        pass
        display_stats()
        user_input = input("\nPress enter to return to the main menu: ")
        if user_input:
            pass

    elif menu == "e":
        print("Goodbye!!!")
        exit()

    else:
        print("You have entered an invalid input. Please try again")

# ====End of Code====
