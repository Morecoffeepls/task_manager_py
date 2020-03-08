############################################
### Program name: task_manager.py
### Written by: Y Taylor
### Date written: 13/02/2020
### This program helps a team manage tasks by, adding users to a list (admin only), assigning tasks to each user, viewing all tasks or just those of the current user. Generate reports of - the number of users, whether any tasks are overdue, what percentages of the tasks are overdue. as well as statistics of all the tasks and users(admin only).
#############################################

user = ''  # store the currently logged in username for later use in the program

# This function generates reports about number of users, tasks, due dates, completed tasks, overdue tasks as well as the various percentages of the above.

def generate_report():
    total_tasks = 0
    f_tasks = open('task_overview.txt','w+')
    with open('tasks.txt') as all_tasks:
        tasks = all_tasks.readlines()
        from datetime import date
        today = str(date.today())
        total_tasks = 0
        total_tasks_com = 0
        total_tasks_not = 0
        overdue = 0
        incompelte = 0
        
        for line in tasks:  # loop through all the lines in task and calculate the total number of tasks, completed tasks, incomplete tasks and overdue tasks
            current_line = line.split(",")
            #print(current_line)
            total_tasks += 1 
            if current_line[5] == " yes":
                total_tasks_com +=1
            elif current_line[5] == " no":
                total_tasks_not += 1
            elif str(current_line[4]) > today:
                incompelte += 1
            elif str(current_line[4]) < today:
                overdue += 1   
        per_inc = 100 * float(total_tasks_not/total_tasks)  # percentage calculations for incomplete and overdue tasks
        per_overdue = 100 * float(overdue/total_tasks)   
        #total_tasks += total_tasks             
    write_to_file = ("The total number of tasks tracked using this system is: " + str(total_tasks) + "\nCompleted tasks : " + str(total_tasks_com) + "\nIncomplete tasks: " + str(total_tasks_not) + "\nOverdue tasks: " + str(overdue) + "\nPercent incomplete: " + str(f"{per_inc:.2f}") + "\nPercent overdue: " + str(per_overdue))            
    print(f"\n{write_to_file}\n")
    f_tasks.write(write_to_file)   # format the above numberes and adds them to the new text file
    f_tasks.close()

    f_user_overview = open('user_overview.txt','w+') # open new user overview files so that the following calculations and respective sentences can be written to the file
    
    users = open('user.txt','r+')
    
    all_tasks = open('tasks.txt','r+') 
    tasks = all_tasks.readlines()

    num_users = sum(1 for line in open('user.txt'))  # calculate the number of users in the file, by counting the lines in the file
    f_user_overview.write(f"The total number of users registered is: {num_users}\nThe total number of tasks generated and tracked is: {total_tasks}\n")
 
### the following calculates the number of tasks assigned to each user ##############

    for line in users:             
        current_line_u = line.split(",")
        tasks_per_user = 1
        tasks_completed = 0
        tasks_not_completed = 0
        tasks_overdue = 0
        for line in tasks:
            current_line = line.split(",")
            if current_line_u[0] == current_line[0]: # find the lines that match the current username 
                
                tasks_per_user += 1    # keep track of the number of tasks they have completed and if they are overdue

                if current_line[5] == " yes":
                    tasks_completed += 1
                if current_line[5] == " no":
                    tasks_not_completed += 1
                if (current_line[5] == "no") and (current_line[4] < today):
                    tasks_overdue +=1

        # calculate the respective percentages for each user

        percent_per_user = 100 * float((tasks_per_user-1)/total_tasks)
        percent_of_user_com = 100 * float(tasks_completed/(tasks_per_user-1)) 
        percent_of_user_not = 100 * float(tasks_not_completed/(tasks_per_user-1)) 
        per_user_over = 100 * float(tasks_overdue/(tasks_per_user-1))
        # add this all to a variable with the correct formatting

        new_line = "Number of tasks assigned to - " +current_line_u[0] +" is " + str(tasks_per_user-1) +  "\nPercentage of total that have been assigned to the user: " + str(f"{percent_per_user:.2f}") + "\nPercentage of tasks that user has completed: " + str(f"{percent_of_user_com:.2f}") + "\nPercentage of tasks the user still needs to complete: " + str(f"{percent_of_user_not:.2f}") + "\nThe percentage of overdue tasks for this user: " + str(f"{per_user_over:.2f}")  
        print(f"\n{new_line}")
        f_user_overview.seek(0,2)               
        f_user_overview.write(f"\n{new_line}\n") # find the end of the file and write the above to it
        menu()
          

def display_statistics(): # display the innformation gathered in the generate report function
    generate_report()
    menu()


def view_mine():  # display the information relating to the currently logged in user
    empty_list = []  
    with open('tasks.txt') as all_tasks:
        for line in all_tasks:
            current_line = line.split(",")
              
            if current_line[0] == user :  
                empty_list.append(current_line)  # when the line name value matches the that of the currently user - display the following
                view = ("\n") + ("Task:") + current_line[1]+ ("\nAssigned to: ")+current_line[0] + ("\nTask description: ") + current_line[2] + ("\nDate assigned: ") + current_line[3] + ("\nDue date:      ") + current_line[4] + ("\nTask complete: ") + current_line[5] + ("\nTask number: ") + current_line[6]
                print(view)

    # allow the user to choose between editing one of the tasks or returning to the main menu

    select = input("To edit a task - please select the task (by entering the number at the end of the respective task) or enter (-1) to return to the main menu: ")
    select2 = " " + select
    if select == "-1":
        menu()

    elif select != "-1":   # if the user chooses to edit the task, the can either choose to mark the tasks as complete or edit who it is assigned to 
        with open('tasks.txt','r+') as all_tasks:
            lines = all_tasks.read()
            clean = lines.split("\n")
            all_tasks.truncate(0)
            for line in clean:
                current_line = line.split(",")     # copy all of the lines in the text file , and delete all the lines in the file. (so that the edit line can be added with the copied lines to avoid a conflicting newly edited and old lines)
                if not ((current_line[0] == user) and (current_line[6] == select2)):

                    org_lines = str(current_line).replace("'","").replace("  "," ").strip("[]")
                    all_tasks.seek(0,2)
                    all_tasks.write("\n")                    
                    all_tasks.write(str(org_lines)) # write all the copied lines besides for the selected task to be edited

                elif (current_line[0] == user) and (current_line[6] == select2): 
                    entry = input("would you like to mark this task as complete (y) or would you like to edit this task (e) ?\n enter (-1) to return to main menu: ")
                    if entry == "-1":
                        menu()
                    elif entry == "y":   # if they choose to mark the task as complete then edit the line of the task and remove the no, by its position in the list and replace it with "yes"
                        current_line.pop(5)
                        current_line.insert(5," yes")
                        #c = current_line[0] + current_line[1] +"ggg"
                        c = current_line[0]+ "," +current_line[1] +"," + current_line[2] + "," + current_line[3] + "," + current_line[4]+ "," + current_line[5] + "," + current_line[6] 
                        
                        all_tasks.seek(0,2)
                        all_tasks.write(f"\n{c}")
                        all_tasks.close()  # write the edited line to the text file
                        menu()
                    elif entry == "e" and current_line[5] == " no": # if the user chooses to edit who the task is assigned to prompt for the following
                        print(current_line[5])
                        new_username = input("Please enter the username for which this task will be assigned to: ")
                        new_due_date = input("Please enter the new due date (year/month/day): ")
                        current_line.pop(0)
                        current_line.insert(0,new_username)
                        current_line.pop(4)
                        current_line.insert(4,new_due_date) # replace the old information by deleting the item by position and replace it with the new data 
                        n = current_line[0]+ "," +current_line[1] +"," + current_line[2] + "," + current_line[3] + "," + current_line[4]+ "," + current_line[5] + "," + current_line[6]
                        all_users.seek(0,2)
                        all_tasks.write(f"\n{n}") # find the end of the file and write the new lines to it
                        all_tasks.close()
                        menu() # return to the main menu


###### function to add a new user ######

def reg_user(): 
        all_users = open('user.txt','r+') # open user and password file
        user_list = all_users.read()
        new_user = input("please enter username: ")  # request new username and password
        if new_user in user_list:
            print("Username already exists! ")
            reg_user()

        else:
            password = input("Please enter a password: ")
            con_paswd = input("Please confirm password: ")
            full = new_user + ", " + password 
            if password == con_paswd:    # confirm password is correct
                all_users.seek(0,2)      # find the end of the file and write the new username and password to the file
                all_users.write(f"\n{full}")
                all_users.close()
                print("Please assign a task to this user! \n")
                add_task()

#### function to calculate the total number of tasks ####    
 
def total():
    tasks = open('tasks.txt','r+')
    total = 0
    for line in tasks:
        total += 1
    return total

### function to add new tasks to users ####

def add_task():
    from datetime import date
    today = str(date.today())         # import the datetime module to add due dates to  tasks
    tasks = open('tasks.txt','r+')    # open the tasks file so that the new task can be written to it
    
    username = input("Please enter the user that this task will be assigned to: ")  # select user to add task to
    title = input("please enter the task title: ")   # enter the task title, description, due date
    description = input("Please enter the task description: ")
    due_date = input("Please enter the due date of the task: ")
    full_task = username + ", " + title + ", " + description + ", " + today + ", " + due_date + ", no, " + str(total())
    tasks.seek(0,2)
    tasks.write(f"\n{full_task}") # write all the data in the above format to the file, close it and return to the main menu
    tasks.close()  
    menu() 
 
### function which displayes all the tasks in the file ###

def view_all():
    with open('tasks.txt') as all_tasks: # open the file
        for line in all_tasks:            # loop through all the lines
            current_line = line.split(",")
            #print(current_line[3])
            total = ("Task:") + current_line[1]+ ("\nAssigned to: ")+current_line[0] + ("\nTask description: ") + current_line[2] + ("\nDate    assigned: ")     + current_line[3] + ("\nDue date:      ") + current_line[4] + ("\nTask complete: ") + current_line[5] + ("\nTask id number: ") + current_line[6]
            print(total)   # print each line in the above format 
    print("-"*50 + "\n" +"-"*50)
    menu()

##### menu function #####
## this function calls all the other functions

def menu():

    entry = input("\nPlease select one of the following options: \nr - register user\na - add task\nva- view all tasks\nvm - view my tasks\ngr - generate reports (admin only)\nds - display statistics (admin only)\ne- exit\n:").lower()
    if entry == "r" :
        reg_user()    
    elif entry == "a":
        add_task()
    elif entry == "va":
        view_all()
    elif entry == "vm":
        view_mine()
    elif entry == "gr" and user == "admin": # some functions can only be accessed by admin
        generate_report()
    elif entry == "ds" and user == "admin":
        display_statistics()        
    elif entry == "e":
        quit()        

##### login #######

all_users = open('user.txt','r+')  # open the username and password file
user_list = all_users.read()
psw = 0
while psw == 0:  # loop until correct username and password is given
    username = input("please enter your username: ")
    password = input("please enter your password: ")

    clean = user_list.split("\n")
    for line in range(len(clean)):    # loop through all the lines in the text file to find the username and password
        current_line = clean[line].split(", ") 

        if (current_line[0] == username) and (current_line[-1] == password):   # look for a username and password that matches the current inputted values
            user += username   # if login is correct - keep track of user
            menu()
            psw =1  # break out of the loop
    if psw == 0:    
        print("Please enter the correct username and password!! ") # display error message if incorrect info is entered
        