from datetime import datetime
import math
import ast
import os.path

setup = ["Unnamed Project", 24, False]
tasks = []
daysPlaceholder = 100
multiplier = 1

# A task can be [Name of task, deadline, priority]
def inputDate():
    year = input("Enter deadline year (yy): ")
    try:
        inputLength = len(year)
        year = int(year)
        success = inputLength == 2
    except:
        success = False

    if (not success):
        while (not success):
            year = input("Please enter a number for the year in (yy) format: ")
            try:
                inputLength = len(year)
                year = int(year)
                success = inputLength == 2
            except:
                success = False

    month = input("Enter deadline month (mm): ")
    try:
        inputLength = len(month)
        month = int(month)
        success = 0 < month < 13 and inputLength == 2
    except:
        success = False

    if (not success):
        while (not success):
            month = input("Please enter a number from 01–12 for the month in (mm) format: ")
            try:
                inputLength = len(month)
                month = int(month)
                success = 0 < month < 13 and inputLength == 2
            except:
                success = False

    day = input("Enter deadline day (dd): ")
    try:
        inputLength = len(day)
        day = int(day)
        if(month == 4 or month == 6 or month == 9 or month == 11):
            success = 0 < day < 31 and inputLength == 2
        elif(month == 2):
            success = 0 < day <  29 and inputLength == 2
        else:
            success = 0 < day < 32 and inputLength == 2
    except:
        success = False

    if (not success):
        while (not success):
            day = input("Please enter a number from for the day in (dd) format: ")
            try:
                inputLength = len(day)
                day = int(day)
                if(month == 4 or month == 6 or month == 9 or month == 11):
                    success = 0 < day < 31 and inputLength == 2
                elif(month == 2):
                    success = 0 < day <  29 and inputLength == 2
                else:
                    success = 0 < day < 32 and inputLength == 2
            except:
                success = False
    return([year,month,day])


def newTask():
    name = input("Enter name of task: ")
    dateCollected = inputDate()
    dateCheck = numberOfDays(getCurrentDate(), dateCollected)
    if (dateCheck == -1):
        inputCheck = input("Warning: this is due in the past! Does this mean someone has not been doing their work on time?")
    priority = input("Please enter a number from 1–10 for the priority of the task: ")
    try:
        priority = int(priority)
        success = 0 < int(priority) < 11
    except:
        success = False

    if (not success):
        while (not success):
            priority = input("Please enter a number from 1–10 for the priority of the task: ")
            try:
                priority = int(priority)
                success = 0 < int(priority) < 11
            except:
                success = False

    effort = input("Please enter a number from 1–10 for the expected amount of effort the task will require: ")
    try:
        effort = int(effort)
        effort = 0 < int(effort) < 11
    except:
        success = False

    if (not success):
        while (not success):
            effort = input("Please enter a number from 1–10 for the expected amount of effort the task will require: ")
            try:
                effort = int(effort)
                success = 0 < int(effort) < 11
            except:
                success = False

    return([name, dateCollected, priority, effort])

def getCurrentDate():
    year = int(str(datetime.now())[2:4])
    month = int(str(datetime.now())[5:7])
    day = int(str(datetime.now())[8:10])
    return([year,month,day])

def isLeapYear(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
            else: return False
        else: return True
    return False

def numberOfDays(date1, date2):
    months = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    if date1 == date2:
        return 0
    if date1[0] > date2[0]:
        return -1
    if date1[0] == date2[0] & date1[1] > date2[1]:
        return -1
    if (date1[0] == date2[0]) & (date1[1] == date2[1]) & (date1[2] > date2[2]):
        return -1
    if (date1[0] == date2[0]) & (date1[1] == date2[1]) & (date1[2] < date2[2]):
        return date2[2] - date1[2]
    if date1[2] == 1:
        offset = 0
    else:
        offset = date1[2] - 1
    if date1[1] == 12:
        return 31 + numberOfDays([date1[0]+1,1,1],date2) - offset
    if date1[1] == 2:
        if isLeapYear(date1[0]):
            return 29 + numberOfDays([date1[0],3,1],date2) - offset
        else:
            return 28 + numberOfDays([date1[0],3,1],date2) - offset
    return months[date1[1]] + numberOfDays([date1[0],date1[1] + 1,1],date2) - offset

def printTasks(tasks):
    if len(tasks) > 0:
        print("\nTasks: ")
        for task in tasks:
            print(task[0])
            print("Deadline: " + str(task[1][0]) + "-" + str(task[1][1]) + "-" + str(task[1][2]))
            print("Priority: " + str(task[2]) + "\n")

def taskCalendar(inputTask):
    if tasks == None:
        print("There are no tasks!")
        return
    taskLength = len(tasks)

    days = numberOfDays(getCurrentDate(), inputTask[1])
    if days > 98:
        safety = days - 14 # maximum 14 safety days
    elif days < 7:
        safety = days # no safety days
    elif days < 1:
        print("The task is literally overdue, the only plan I can give is to finish the task ASAP!")
    else:
        safety = round(days - days/7) # 1/7 days are safety days
    weights = []
    for i in range(taskLength):
        weights.append(float(tasks[i][2]))
    weightTotal = sum(weights)

    taskWeight = inputTask[2]/weightTotal
    taskDays = []

    taskDays = safety*taskWeight
    if taskDays < 1:
        taskDays = 1
    tDfloor = math.floor(taskDays)

    calendar = []

    for i in range(tDfloor):
        calendar.append([i + 1, 100/taskDays, inputTask[0]])
    # print(calendar)
    return calendar

def taskPercentPerDay(inputTask):
    calendar = taskCalendar(inputTask)
    dayWanted = input("What day do you want to view? 0 is today, 1 is tomorrow, etc. ")
    try:
        dayWanted = int(dayWanted)
        success = dayWanted < len(calendar)
    except:
        success = False
    if (not success):
        while (not success):
            print(str(len(calendar)))
            print(calendar)
            dayWanted = input("That day doesn't exist. What day do you want to view? 0 is today, 1 is tomorrow, etc. ")
            try:
                dayWanted = int(dayWanted)
                success = dayWanted < len(calendar)
            except:
                success = False
    print("\nThe task for Day " + str(dayWanted) + " is Task " + str(calendar[dayWanted][0]) + ": " + calendar[dayWanted][2] + "\nThe percent of the task you need to do on the day is " + str(round(calendar[dayWanted][1], 2)) + "%")
    return calendar


def workPerDay():
    count = 0.0
    workCalendar = []
    for i in range (len(tasks)):
        calendar = taskCalendar(tasks[i])
        for j in range (len(calendar)):
            workCalendar.append([])
            #try:
            count += calendar[j][1]
            workCalendar[j].append([i, calendar[j][1], calendar[j][2]])
            #except:
                #print("my feeling when")

    dayWanted = input("What day do you want to view? 0 is today, 1 is tomorrow, etc.")
    try:
        dayWanted = int(dayWanted)
        success = dayWanted < len(calendar)
    except:
        success = False
    if (not success):
        while (not success):
            dayWanted = input("Invalid input. What day do you want to view? 0 is today, 1 is tomorrow, etc.")
            try:
                dayWanted = int(dayWanted)
                success = dayWanted < len(taskCalendar)
            except:
                success = False
    for i in workCalendar[dayWanted]:
        taskHours = setup[1]*i[1]/count
        print("\nTask number: " + str(i[0] + 1) + "\nTask Name: " + i[2] + "\nHours to work on it: " + str(round(taskHours, 2)) + "\n")

    # print(workCalendar)
    # print("- - - - -")
    # print(workCalendar[dayWanted])
    # print("- + - + -")

# # # # # # # #

while True:
    if (not setup[2]):
        setup[0] = input("Name of project: ")
        try:
            setup[1] = int(input("Number of hours you can spend on this project: "))
            success = True
        except:
            success = False
        while not success:
            try:
                setup[1] = int(input("Number of hours you can spend on this project: "))
                success = True
            except:
                success = False
        setup[2] = True
        print("Setup is complete! Type 'h' for help and to view the commands :)")

    userCommand = input("What do you want to do? ")
    match userCommand:
        case "h": #help 
            print("\n---HELP MENU!---\nPress 'a' to add a task\nPress 'v' to view all the tasks\nPress 's' to view the schedule for a day\nPress 'p' to log today's progress\nPress 'q' to quit\n---HHELP MENU!---\n")
        case "a": # add a task
            taskAdd = newTask()
            tasks.append(taskAdd)
            print("Added task! :)")
        case "v": # print tasklist
            printTasks(tasks)
        case "s": # finds out how much work you should do per day
            workPerDay()
        case "p":
            try:
                progress = int(input("How much progress have you gotten so far on your goals for today so far? Only enter a number: "))
                success = True
            except:
                success = False
            while not success:
                try:
                    progress = int(input("Invalid input. How much progress have you gotten so far on your goals for today so far? Only enter a number: "))
                    success = True
                except:
                    success = False

            if( progress < 25 ):
                print("Have you been slacking off? You better show improvement tomorrow!")
            elif( progress < 75 ):
                print("Do better next time")
            elif( progress < 99 ):
                print("Almost done! Tomorrow try to finish it all :)")
            else:
                print("Perfect! Here, have a cookie for your efforts! 🍪 :)")
        case "q": #exit
            break
        case default:
            print("Not a command; to view all the commands press 'h'")

