from datetime import datetime
import json
import os

tasks = []
# constant, don't edit, use .copy()
TASK_TEMPLATE = {
    "name":"",
    "due": None, # datetime
    "lastActivity": None, # datetime
    "description": "",
    "done": False # False if not done, datetime otherise
}

# don't edit, intentionaly left an unhandled exception possibility
def str_to_datetime(datetime_str):
    """ attempts to convert a string in one of two formats to a datetime
    Valid formats (visual representation): mm/dd/yy hh:mm:ss or yyyy-mm-dd hh:mm:ss """
    try:
        return datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    except:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

# diff_in_secs takes in two timestamps and calculate the time difference in seconds
def diff_in_secs(dt2, dt1):
    timedelta = dt2 - dt1
    return timedelta.days * 24 * 3600 + timedelta.seconds

# format_time_diff takes in seconds and converts them into days, hours, minutes, seconds
def format_time_diff(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return (abs(days), abs(hours), abs(minutes), abs(seconds))

def save():
    """ writes the tasks list to a json file to persist changes """
    f = open("tracker.json", "w")
    f.write(json.dumps(tasks, indent=4, default=str))
    f.close()

def load():
    """ loads the task list from a json file """
    if not os.path.isfile("tracker.json"):
        return
    f = open("tracker.json", "r")
    
    data = json.load(f)
    # Note about global keyword: https://stackoverflow.com/a/11867510
    global tasks
    tasks = data
    f.close()
    print(f"data {data}")    

def list_tasks(_tasks):
    """ List a summary view of all tasks """
    i = 0
    for t in _tasks:
        print(f"{i+1}) [{'x' if t['done'] else ' '}] Task: {t['name']} (Due: {t['due']})")
        i += 1
    if len(_tasks) == 0:
        print("No tasks to show")

# edits should happen below this line

def add_task(name: str, description: str, due: str):
    """ Copies the TASK_TEMPLATE and fills in the passed in data then adds the task to the tasks list """
    task = TASK_TEMPLATE.copy() # don't delete this
    # update lastActivity with the current datetime value
    lastActivity = datetime.now()
    try:
        if len(name) == 0:
            raise Exception("Task name is missing")
        if len(description) == 0:
            raise Exception("Task description is missing")
        if len(due) == 0:
            raise Exception("Task due date is missing")
        # set the name, description, and due date (all must be provided)
        task = {
            "name": name,
            "description": description,
            # due date must match one of the formats mentioned in str_to_datetime()
            "due": str_to_datetime(due),
            "lastActivity": lastActivity,
            "done": False
        }
        task_copy = task.copy()
        tasks.append(task_copy)  # add the new task to the tasks list
        # output a message confirming the new task was added or if the addition was rejected due to missing data
        print(f'''Task: {task["name"]} is added to the list''')
        # make sure save() is still called last in this function
        save()
    except Exception as e:
        print("Something else went wrong:", e)
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # UCID - vg473; date :02/20/23;
    # add_task() takes in name, description, due as arguments. When any of these argument has an empty string or due is in incorrect format
    # I'm raising an exception with approriate message that is caught and error message is shown to the user. When the data is entered correctly, 
    # the add_task() will convert due string to datetime format and update template task with provided arguments, 
    # and then add it to the list and save it to tracker.json file

def process_update(index):
    """ extracted the user input prompts to get task data then passes it to update_task() """

    if index in range(len(tasks)):  # get the task by index
        task = tasks[index]
        # show the existing value of each property where the TODOs are marked in the text of the inputs (replace the TODO related text)
        name = input(f"What's the name of this task? (TODO name) \n").strip()
        desc = input(
            f"What's a brief descriptions of this task? (TODO description) \n").strip()
        due = input(
            f"When is this task due (format: m/d/y H:M:S) (TODO due) \n").strip()
        print(f"updated name:", name)
        print(f"updated description:", desc)
        print(f"updated due date:", due)
        update_task(index, name=name, description=desc, due=due)
    else:
        # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print("Invalid Index Number")
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # UCID - vg473; date :02/20/23;
    # process_update() checks whether the given is in tasks or not. 
    # if it is in tasks range, it reads update_task() function variables; else printing an error message

def update_task(index: int, name: str, description:str, due: str):
    """ Updates the name, description , due date of a task found by index if an update to the property was provided """
    # find the task by index
    if index < 0 or index >= len(tasks):
        # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print("Invalid Index")
        return

    task = tasks[index].copy()
    # update incoming task data if it's provided (if it's not provided use the original task property value)
    if name:
        task['name'] = name
    if description:
        task['description'] = description
    if due:
        task['due'] = due
    # update lastActivity with the current datetime value
    task['lastActivity'] = datetime.now()

    if name != tasks[index]['name'] or description != tasks[index]['description'] or due != tasks[index]['due']:
        tasks[index] = task
        # output that the task was updated if any items were changed, otherwise mention task was not updated
        print("task updated")
        # make sure save() is still called last in this function
        save()
    else:
        print("Task not updated - Input values already match existing task details")
   # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
   # UCID - vg473; date :02/20/23;
   # update_task() get the value for the process_update(),
   #  - if index value is less than zero or greater than or equal to len(tasks) it prints invalid index
   #  - if index value is valid, it checks given name,description,due are valid and compare them with the old values, 
   #    if new values aren't matching old values, prints a message that the task is updated and saves updated task to tasks
   #    if new values are same as old, it prints a message task not updated.

def mark_done(index):
    """ Updates a single task, via index, to a done datetime"""
    # find task from list by index
    if index in range(len(tasks)):
        task = tasks[index]
        if task['done'] == False:  # if it's not done, record the current datetime as the value
            task['done'] = datetime.now()
            task['lastActivity'] = datetime.now()
            print("task completed")
        else:
            # if it is done, print a message saying it's already completed
            print("task completed already")
    else:
        # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print("invalid index")

    # make sure save() is still called last in this function
    save()
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # UCID - vg473; date :02/20/23;
    # mark_done() does following things,
    #   - if index is out of range, then a message invalid index is shown
    #   - if index is valid and task is not done, done and lastActivity are updated with current timestamp and task completed message is printed
    #   - if index is valid and task done value is not False, task completed message is printed

def view_task(index):
    """ View more info about a specific task fetch by index """
    # find task from list by index
    if index in range(len(tasks)):
        task = tasks[index]
        # utilize the given print statement when a task is found
        print(f"""
        [{'x' if task['done'] else ' '}] Task: {task['name']}\n 
        Description: {task['description']} \n 
        Last Activity: {task['lastActivity']} \n
        Due: {task['due']}\n
        Completed: {task['done'] if task['done'] else '-'} \n
        """.replace('  ', ' '))
    else:
        # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print("Index is out of range,please enter valid number")
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # UCID - vg473; date :02/20/23;
    # view_task() picks and displays the task based on index value if the index is valid else an error message is printed 


def delete_task(index):
    """ deletes a task from the tasks list by index """
    if index in range(len(tasks)):
        del tasks[index]  # delete/remove task from list by index
        # message should show if it was successful or not
        print(f'''Task #{index+1} Deleted successful''')
    else:
        # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print("Index is out of range,please enter valid number")
    # make sure save() is still called last in this function

    save()
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # UCID - vg473; date :02/20/23;
    # delete_task() delete the task from tasks based index values if valid else it will print an error message

def get_incomplete_tasks():
    """ prints a list of tasks that are not done """
    # generate a list of tasks where the task is not done
    _tasks = []
    for index in range(len(tasks)):
        task = tasks[index]
        if task['done'] == False:
            _tasks.append(task)
    # pass that list into list_tasks()
    if len(_tasks):
        list_tasks(_tasks)
    else:
        print("There are no incomplete tasks in the list")
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # UCID - vg473; date :02/20/23;
    # get_incomplete_tasks() loops over all the tasks and find incomplete task and adds them to _tasks list. 
    # Once the loop is done, list_tasks() is called to print all incomplete tasks if _tasks has any tasks if not it prints no incomplete tasks message

def get_overdue_tasks():
    """ prints a list of tasks that are over due completion (not done and expired) """
    # generate a list of tasks where the due date is older than now and that are not complete
    _tasks = []
    for index in range(len(tasks)):
        task = tasks[index]
        if str_to_datetime(task['due']) < datetime.now():
            _tasks.append(task)
    # pass that list into list_tasks()
    if len(_tasks):
        list_tasks(_tasks)
    else:
        print("There are no overdue tasks")
   # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
   # UCID - vg473; date :02/20/23;
   # get_overdue_tasks() loops over all tasks to see if any task due timestamps are in past and add them to _tasks. 
   # If _tasks has more than one task in it, we call list_tasks() or else print no overdue tasks message

def get_time_remaining(index):
    """ outputs the number of days, hours, minutes, seconds a task has before it's overdue otherwise shows similar info for how far past due it is """
    # get the task by index

    # display the remaining time via print in a clear format showing days, hours, minutes, seconds
    # if the due date is in the past print out how many days, hours, minutes, seconds the task is over due (clearly note that it's over due, values should be positive)
    if index < 0 or index > len(tasks):
        # consider index out of bounds scenarios and include appropriate message(s) for invalid index
        print("Index is out of range or invalid. Please try again")
    else:
        # get the days, hours, minutes, seconds between the due date and now
        task = tasks[index]
        task_due_datetime = str_to_datetime(task['due'])
        days, hours, minutes, seconds = format_time_diff(diff_in_secs(
            task_due_datetime, datetime.now()))

        if (task_due_datetime > datetime.now()):
            print(
                f'''\nRemaining time: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds''')
        else:
            print(
                f'''\nOver due by: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds''')
    # include your ucid and date as a comment of when you implemented this, briefly summarize the solution
    # UCID - vg473; date :02/20/23;
    # get_time_remaining() does following things,
    #   - if index is invalid, prints an error message
    #   - if index is valid, we find the task and change the due string to datetime format - task_due_datetime. 
    #       task_due_datetime is then compared with current timestamp to get the difference 
    #       I have used two functions, diff_in_secs() which gives me the seconds difference between two datetimes and
    #       format_time_diff() which converts those seconds into days, hours, minutes, seconds with abs().
    #   - at the end, if due is before current time, we print it as remaining time and if due is after current time we print it as over due by

# no changes needed below this line

command_list = ["add", "view", "update", "list", "incomplete", "overdue", "delete", "remaining", "help", "quit", "exit", "done"]
def print_options():
    """ prints a readable list of commands that can be typed when prompted """
    print("Choices")
    print("add - Creates a task")
    print("update - updates a specific task")
    print("view - see more info about a task by number")
    print("list - lists tasks")
    print("incomplete - lists incomplete tasks")
    print("overdue - lists overdue tasks")
    print("delete - deletes a task by number")
    print("remaining - gets the remaining time of a task by number")
    print("done - marks a task complete by number")
    print("quit or exit - terminates the program")
    print("help - shows this list again")

def run():
    """ runs the program until terminated or a quit/exit command is used """
    print("Welcome to Task Tracker!")
    load()
    print_options()
    while(True):
        opt = input("What would you like to do?\n").strip() # strip removes whitespace from beginning/end
        if opt not in command_list:
            print("That's not a valid option")
        elif opt == "add":
            name = input("What's the name of this task?\n").strip()
            desc = input("What's a brief descriptions of this task?\n").strip()
            due = input("When is this task due (visual format: mm/dd/yy hh:mm:ss)\n").strip()
            add_task(name, desc, due)
        elif opt == "view":
            num = int(input("Which task do you want to view? (hint: number from 'list') ").strip())
            index = num-1
            view_task(index)
        elif opt == "update":
            num = int(input("Which task do you want to update? (hint: number from 'list') ").strip())
            index = num-1
            process_update(index)
        elif opt == "done":
            num = int(input("Which task do you want to complete? (hint: number from 'list') ").strip())
            index = num-1
            mark_done(index)
        elif opt == "list":
            list_tasks(tasks)
        elif opt == "incomplete":
            get_incomplete_tasks()
        elif opt == "overdue":
            get_overdue_tasks()
        elif opt == "delete":
            num = int(input("Which task do you want to delete? (hint: number from 'list') ").strip())
            index = num-1
            delete_task(index)
        elif opt == "remaining":
            num = int(input("Which task do you like to get the duration for? (hint: number from 'list') ").strip())
            index = num-1
            get_time_remaining(index)
        elif opt in ["quit", "exit"]:
            print("Good bye.")
            quit()
        elif opt == "help":
            print_options()
        
if __name__ == "__main__":
    run()