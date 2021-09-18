import os.path
import random
from chore import Chore
import datetime

DEBUG_INFO = 1  # 0 - none. 1 - method calls. 2 - details. 3 - variable values
ACTIVE_DAYS = []
NUM_DAYS = -1
WEEKS = 12
CHORES_PER_WEEK = 1

chores = []
locked_day = []
total_chores = 0
total_people = 0


def parse_people_data():
    if DEBUG_INFO >= 1:
        print("Attempting to parse people data...")
    global total_people
    global ACTIVE_DAYS
    global NUM_DAYS
    people = {}

    # Define a filename.
    filename = "people_data.tsv"

    if not os.path.isfile(filename):
        print('File does not exist.')
        raise IOError

    # Open the file as f.
    # The function readlines() reads the file.
    reading_header = True
    with open(filename) as f:
        if reading_header:
            head = f.readline()
            head = head.split("\n")
            ACTIVE_DAYS = head[0].split("\t")  # jank array access, but trust me, it works.
            NUM_DAYS = len(ACTIVE_DAYS)

            if DEBUG_INFO >= 2:
                print("    Active days: " + str(ACTIVE_DAYS))
                print("    Num days; " + str(NUM_DAYS))
            reading_header = False

        content = f.read().splitlines()
    f.close()

    for day in ACTIVE_DAYS:
        people[day] = []

    if DEBUG_INFO >= 2:
        print("-------------------------------")
        print("    people data:")
    for line in content:
        if DEBUG_INFO >= 3:
            print("        " + line)

        day_data = line.split("\t")
        index = 0
        for name in day_data:
            if name != "":
                people[ACTIVE_DAYS[index]].append(name)
                total_people += 1
            index += 1

    if DEBUG_INFO >= 1:
        print("Successfully parsed people data!")
    return people


def parse_chores():
    if DEBUG_INFO >= 1:
        print("Attempting to parse chore data...")

    global total_chores
    scaled_chores = []
    for i in range(NUM_DAYS):
        scaled_chores.append([])

    # Define a filename.
    filename = "chores_data.tsv"

    if not os.path.isfile(filename):
        print('Chores file does not exist.')
        raise IOError

    # Open the file as f.
    # The function readlines() reads the file.
    reading_header = True
    with open(filename) as f:
        if reading_header:
            head = f.readline()
            head = head.split("\n")
            if head[0].split("\t") != ["Desc", "Chore", "Freq", "Locked Day"]:
                print("Chores file is formatted differently than what code is built to parse")
                raise IOError

        reading_header = False

        content = f.read().splitlines()
    f.close()

    # Show the file contents line by line.
    if DEBUG_INFO >= 2:
        print("-------------------------------")
        print("    chores data:")

    for line in content:
        if DEBUG_INFO >= 3:
            print("        " + line)

        key, desc, freq, specific_day = line.split("\t")
        parsed_chore = Chore(key, desc, freq, specific_day)
        chores.append(parsed_chore)

        if specific_day != "any":
            locked_day.append((specific_day, parsed_chore))
            # todo: incomplete special case coverage

        if freq.lower() == "daily":
            for i in range(NUM_DAYS):
                scaled_chores[i].append(parsed_chore)
            total_chores += NUM_DAYS
        elif (freq.lower() == "biweekly") | (freq.lower() == "bi-weekly"):  # for the mf who uses hyphens.
            scaled_chores[0].append(parsed_chore)
            scaled_chores[int((NUM_DAYS+1)/2)].append(parsed_chore)
            total_chores += 2
        elif freq.lower() == "weekly":
            min = 420  # arbitrary high  number
            min_index = -1
            for i in range(NUM_DAYS):
                if len(scaled_chores[i]) < min:
                    min = len(scaled_chores[i])
                    min_index = i
            scaled_chores[min_index].append(parsed_chore)
        elif (freq.lower() == "bimonthly") | (freq.lower() == "bi-monthly"):
            # really sus way of doing bimonthly. tricky to do legit,
            # because this program runs on a weekly system
            if random.random() >= 0.51:  # .51 because more often then not you should do.
                min = 420
                min_index = -1
                for i in range(NUM_DAYS):
                    if len(scaled_chores[i]) < min:
                        min = len(scaled_chores[i])
                        min_index = i
                scaled_chores[min_index].append(parsed_chore)
        elif freq.lower() == "monthly":
            # still jank
            if random.random() <= 0.26:  # .26 because more often then not, need the chore
                min = 420
                min_index = -1
                for i in range(NUM_DAYS):
                    if len(scaled_chores[i]) < min:
                        min = len(scaled_chores[i])
                        min_index = i
                scaled_chores[min_index].append(parsed_chore)
        else:
            print(freq + " is not a valid freq parameter. Must be 'daily, bi-weekly, or weekly'")
            raise IOError

    merged_chores = []
    for l in scaled_chores:
        merged_chores += l

    if DEBUG_INFO >= 1:
        print("Successfully parsed chore data!")
    return merged_chores


def show_diagnostics():
    if DEBUG_INFO >= 1:
        print("-------------------------------")
        print("Chore manager initialized with these params:")
        print("number of chores (scaled) - " + str(total_chores))
        print("number of people (scaled) - " + str(total_people * CHORES_PER_WEEK))
        print("running schedule for " + str(WEEKS) + " weeks.")


def build_schedule(days_people, chore_rotation):
    schedule = {}
    index = 0
    for day in ACTIVE_DAYS:
        schedule[day] = {}
        for person in days_people[day]:
            if index < len(chore_rotation):
                schedule[day][person] = chore_rotation[index]
            else:
                schedule[day][person] = "free day"
            index += 1

    if DEBUG_INFO >= 3:
        print(schedule)
    return schedule


def write_schedule(file, schedule, week_num):
    file.write("WEEK " + str(week_num) + " CHORES: \n")
    for day, assigned_chores in schedule.items():
        file.write(day + " Chores --------------------------------------------------------------\n")
        for person, chore in assigned_chores.items():
            file.write(person + " - " + str(chore) + "\n")
        file.write("\n")


def build_weekly_schedules(people, scaled_chores_list):
    # Define a filename.
    filename = "schedule.txt"

    # Open the file as f.
    f = open(filename, 'w')
    f.write("Chore schedule, created " + str(datetime.date.today()))

    for index in range(WEEKS):
        schedule = build_schedule(people, scaled_chores_list)
        write_schedule(f, schedule, index+1)
        scaled_chores_list.append(scaled_chores_list.pop(0))
        f.write("\n")
    f.close()


people = parse_people_data()
scaled_chores_list = parse_chores()
show_diagnostics()
build_weekly_schedules(people, scaled_chores_list)


