import os.path
import random
from chore import Chore
import datetime

DEBUG_INFO = 1  # 0 - silent. 1 - method calls. 2 - details. 3 - variable values
ACTIVE_DAYS = []
NUM_DAYS = -1
WEEKS = 12
CHORES_PER_WEEK = 1
FREE_CHORE = None

locked_day = []
total_chores = 0
total_people = 0


def debug_print(message, debug_level):
    if DEBUG_INFO >= debug_level:
        print(message)


def parse_people_data():
    debug_print("Attempting to parse people data...", 1)
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

            debug_print("    Active days: " + str(ACTIVE_DAYS), 2)
            debug_print("    Num days; " + str(NUM_DAYS), 2)
            reading_header = False

        content = f.read().splitlines()
    f.close()

    for day in ACTIVE_DAYS:
        people[day] = []

    debug_print("-------------------------------", 2)
    debug_print("    people data:", 2)
    for line in content:
        debug_print("        " + line, 3)

        day_data = line.split("\t")
        index = 0
        for name in day_data:
            if name != "":
                people[ACTIVE_DAYS[index]].append(name)
                total_people += 1
            index += 1

    debug_print("Successfully parsed people data!", 1)
    return people


def parse_chores():
    debug_print("Attempting to parse chore data...", 1)

    global total_chores
    global FREE_CHORE
    chores = []
    scaled_chores = []
    dailies = []

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
    debug_print("-------------------------------", 2)
    debug_print("    chores data:", 2)

    for line in content:
        debug_print("        " + line, 3)

        desc, chore, freq, specific_day = line.split("\t")
        parsed_chore = Chore(desc, chore, freq, specific_day)

        if desc.lower() == "free space":
            FREE_CHORE = parsed_chore
        else:
            chores.append(parsed_chore)

        if specific_day != "any":
            locked_day.append((specific_day, parsed_chore))
            # todo: incomplete special case coverage (fridge clean on Monday)
            # but could I really be fucked to do this bit. It's a bit tricky. Bleh.

        if freq.lower() == "daily":
            dailies.append(parsed_chore)
            # for i in range(NUM_DAYS):
            #     scaled_chores[i].append(parsed_chore)
            # total_chores += NUM_DAYS
        elif (freq.lower() == "biweekly") | (freq.lower() == "bi-weekly"):  # for the mf who uses hyphens.
            scaled_chores[0].append(parsed_chore)
            scaled_chores[int((NUM_DAYS+1)/2)].append(parsed_chore)
            total_chores += 2
        elif freq.lower() == "weekly":
            min = 420  # arbitrary high number bc Python doesn't have max_int
            min_index = -1
            for i in range(NUM_DAYS):
                if len(scaled_chores[i]) < min:
                    min = len(scaled_chores[i])
                    min_index = i
            scaled_chores[min_index].append(parsed_chore)
            total_chores += 1
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
                total_chores += 1
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
                total_chores += 1
        else:
            print(freq + " is not a valid freq parameter. Must be 'daily, bi-weekly, or weekly'")
            raise IOError

    merged_chores = []
    for l in scaled_chores:
        merged_chores += l

    debug_print("Successfully parsed chore data!", 1)
    return merged_chores, dailies


def show_diagnostics(len_scaled_chores, len_dailies):
    if DEBUG_INFO >= 1:
        print("-------------------------------")
        print("Chore manager initialized with these params:")
        print("number of daily chores - " + str(len_dailies))
        print("number of non-daily chores (scaled) - " + str(len_scaled_chores))
        print("number of people (scaled) - " + str(total_people * CHORES_PER_WEEK))
        print("running schedule for " + str(WEEKS) + " weeks.")
        if len_scaled_chores + len_dailies - (total_people * CHORES_PER_WEEK) >= 0.2 * total_chores:
            print("WARNING: more than 10% gap between total chores and people slots. Continuing means many free chores")
        if len_scaled_chores + len_dailies - (total_people * CHORES_PER_WEEK) >= -1 * 0.2 * total_chores:
            print("WARNING: more than 10% gap between people slots and total chores. Continuing means many repeat chores")

        print("-------------------------------")


def build_schedule(days_people, chore_rotation, dailies):
    schedule = {}
    index = 0

    for day in ACTIVE_DAYS:
        schedule[day] = {}
        daily_chores = []

        for x in range(len(days_people[day]) - len(dailies)):
            daily_chores.append(chore_rotation[index])
            index += 1
        for chore in dailies:
            daily_chores.insert(random.randint(0, len(daily_chores)), chore)

        day_index = 0
        for person in days_people[day]:
            if day_index < len(daily_chores):
                schedule[day][person] = daily_chores[day_index]
            else:
                schedule[day][person] = FREE_CHORE
                debug_print("added free space: " + str(FREE_CHORE), 2)
            day_index += 1

    if DEBUG_INFO >= 3:
        print(schedule)
    return schedule


def insert_dailies(chore_rotation, dailies, max_index):
    if len(dailies) == 0:
        debug_print("no dailies to insert", 1)
        print("no dailies to insert")
        return chore_rotation

    completed_rotation = chore_rotation.copy()
    d = dailies.copy()
    while len(d) > 0:
        i = random.randint(0, max_index - 1)
        c = d.pop()
        print("i: " + str(i) + ", " + str(c))
        completed_rotation.insert(i, c)
    return completed_rotation


def write_schedule(file, schedule, week_num):
    file.write("WEEK " + str(week_num) + "\n")
    for day, assigned_chores in schedule.items():
        file.write(day + " Chores --------------------------------------------------------------\n")
        for person, chore in assigned_chores.items():
            file.write(person + " - " + str(chore) + "\n")
        file.write("\n")


def build_weekly_schedules(people, scaled_chores_list, dailies):
    debug_print("Building schedule...", 1)

    # Define a filename.
    filename = "schedule.txt"

    # Open the file as f.
    f = open(filename, 'w')
    f.write("Chore schedule, created " + str(datetime.datetime.today()) + "\n\n")

    for index in range(WEEKS):
        schedule = build_schedule(people, scaled_chores_list, dailies)
        write_schedule(f, schedule, index+1)
        scaled_chores_list.append(scaled_chores_list.pop(0))
    f.write("\n")
    f.close()
    debug_print("Building succeeded...", 1)


people = parse_people_data()
scaled_chores_list, dailies = parse_chores()
show_diagnostics(len(scaled_chores_list), len(dailies))
build_weekly_schedules(people, scaled_chores_list, dailies)
