#=====importing libraries===========
'''This is the section where you will import libraries'''

# After research I found out about the datetime module, it's type and 
# attributes. Also the strftime function that returns a string, 
# representing date and time and strptime function for parsing date and 
# time strings. 
# 
# I also learnt about the re module and the fullmatch function that 
# returns a match

import re
from datetime import datetime

#====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and 
    passwords from the file
    - Use a while loop to validate your user name and password
'''

with open("10-020 Capstone Project - Files/user.txt", 'r') as file:
    users = {}
    for line in file:
        line = line.strip('\n').split(', ')
        users[line[0]] = line[1]

while True:
    username = input("Enter a username: ")
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

    if username == 'admin':
        menu = input('''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
ds - display statistics
e - exit
: ''').lower()
    else:
        menu = input('''Select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: ''').lower()
        
    print()

    if menu == 'r':
        pass
        '''This code block will add a new user to the user.txt file
        - You can use the following steps:
            - Request input of a new username
            - Request input of a new password
            - Request input of password confirmation.
            - Check if the new password and confirmed password are the 
            same
            - If they are the same, add them to the user.txt file,
              otherwise present a relevant message
        '''
        
        # Check if the username already exists with the built dictionary
        with open("10-020 Capstone Project - Files/user.txt", 'r') as file:
            users = {}
            for line in file:
                line = line.strip('\n').split(', ')
                users[line[0]] = line[1]

        username = input("Enter a new username: ")
        while username in users:
            print("Username already exists")
            username = input("Enter a new username: ")
        password = input("Enter password: ")
        password_confirmation = input("Enter password again to confirm: ")
        while password != password_confirmation:
            print("Passwords don't match")
            password = input("Enter password: ")
            password_confirmation = input("Enter password again to confirm: ")
        
        with open("10-020 Capstone Project - Files/user.txt", 'a') as file:
            file.write(f"\n{username}, {password}")

    elif menu == 'a':
        pass
        '''This code block will allow a user to add a new task to 
        task.txt file
        - You can use these steps:
            - Prompt a user for the following: 
                - the username of the person whom the task is assigned 
                to,
                - the title of the task,
                - the description of the task, and 
                - the due date of the task.
            - Then, get the current date.
            - Add the data to the file task.txt
            - Remember to include 'No' to indicate that the task is not 
            complete.
        '''

        # Sanitise the user input. Ensure no unecessary spaces in the 
        # string. Check if the date format is valid, then parse it and 
        # finally format it to our use case
        #
        # Append the task to the tasks.txt file if not already in the 
        # file, Go the beginning of the file and read all the lines
        # into a list. Then go back to the end of the file and add the 
        # task if it's not already in the list
    
        username = input("Enter the username of the person whom this task is \
assigned to: ")
        title = input("Enter the title of the task: ").strip()
        title = re.sub(r' +', ' ', title)
        description = input("Enter the description of the task: ").strip()
        description = re.sub(r' +', ' ', description)
        due_date = input("Enter the due_date of the task in this format \
'dd-mm-yyyy' e.g 20-10-2019: ").strip()
        due_date = re.sub(r' +', '', due_date)
        while not re.fullmatch(r'\d{1,2}-\d{1,2}-\d{4}', due_date):
            print("Date you entered is invalid")
            due_date = input("Enter the due_date of the task in this format \
'dd-mm-yyyy' e.g 20-10-2019: ").strip()
            due_date = re.sub(r' +', '', due_date)
        due_date = datetime.strptime(due_date,'%d-%m-%Y').strftime("%d %b %Y")
        today = datetime.now().strftime("%d %b %Y")

        with open("10-020 Capstone Project - Files/tasks.txt", "a+") as file:
            file.seek(0,0)
            tasks = file.readlines()
            file.seek(0,2)
            task = f"{username}, {title}, {description}, {today}, {due_date}, No"
            if task not in tasks:
                file.write('\n'+task)

    elif menu == 'va':
        pass
        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         You can do it in this way:
            - Read a line from the file.
            - Split that line where there is comma and space.
            - Then print the results in the format shown in the Output 2 in the PDF
            - It is much easier to read a file using a for loop.
        '''

        with open("10-020 Capstone Project - Files/tasks.txt", 'r') as file:
            
            task_found = False # Handle case of no task found

            for line in file:
                task_found = True
                print('—'*79, '\n')
                line = line.split(', ')
                print(f"Task:\t\t\t{line[1]}")
                print(f"Assigned to:\t\t{line[0]}")
                print(f"Date assigned:\t\t{line[3]}")
                print(f"Due date:\t\t{line[4]}")
                print("Task Complete?:\t\tNo")
                print(f"Task Description:\n {line[2]}\n")
            
            if task_found:
                print('—'*79)
            else:
                print("No tasks found")

    elif menu == 'vm':
        pass
        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         You can do it in this way:
            - Read a line from the file
            - Split the line where there is comma and space.
            - Check if the username of the person logged in is the same as the 
              username you have read from the file.
            - If they are the same you print the task in the format of Output 2
              shown in the PDF 
        '''

        with open("10-020 Capstone Project - Files/tasks.txt", 'r') as file:
    
            username_found = False # Handle if no task assigned to user 
            
            for line in file:
                line = line.split(', ')
                if line[0] == username:
                    username_found = True
                    print('—'*79, '\n')
                    print(f"Task:\t\t\t{line[1]}")
                    print(f"Assigned to:\t\t{line[0]}")
                    print(f"Date assigned:\t\t{line[3]}")
                    print(f"Due date:\t\t{line[4]}")
                    print("Task Complete?:\t\tNo")
                    print(f"Task Description:\n {line[2]}\n")
            
            if username_found:
                print('—'*79)
            else:
                print("No tasks assigned to you")

    elif menu == 'ds':
        pass
        """The admin user is provided with a new menu option that allows
        them to display statistics. When this menu option is selected, 
        the total number of tasks and the total number of users should 
        be displayed in a user-friendly manner.
        """
        with open("10-020 Capstone Project - Files/tasks.txt", 'r') as file:
            lines = file.readlines()
            print('—'*79, '\n')
            print(f"Total number of tasks:\t\t{len(lines)}")

        with open("10-020 Capstone Project - Files/user.txt", 'r') as file:
            lines = file.readlines()
            print(f"Total number of users:\t\t{len(lines)}\n")
            print('—'*79)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")
