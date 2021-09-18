import os.path
from chore import Chore

chores = []
week1 = []
week2 = []
week3 = []
week4 = []
locked_day = []
total_chores = 0

day_people_map = dict()
total_people = 0


def parse_chores():
    print("\n[INIT - reading chores tsv]")
    global total_chores

    # Define a filename.
    filename = "chores_half_data.tsv"

    if not os.path.isfile(filename):
        print('File does not exist.')
        raise IOError

    # Open the file as f.
    # The function readlines() reads the file.

    reading_header = True
    with open(filename) as f:
        if reading_header:
            f.readline()
            reading_header = False

        content = f.read().splitlines()
        # print(content)

    # Show the file contents line by line.
    for line in content:
        # print(line)
        key, desc, freq, prio, specific_day = line.split("\t")
        parsed_chore = Chore(key, desc, freq, prio, specific_day)
        chores.append(parsed_chore)

        if specific_day != "any":
            locked_day.append(parsed_chore)
            # todo: incomplete special case coverage

        if freq == "1":
            if len(week2) < len(week4):
                week2.append(parsed_chore)
            else:
                week4.append(parsed_chore)
            total_chores += 1
        elif freq == "2":
            week1.append(parsed_chore)
            week3.append(parsed_chore)
            total_chores += 2
        elif freq == "4":
            week1.append(parsed_chore)
            week2.append(parsed_chore)
            week3.append(parsed_chore)
            week4.append(parsed_chore)
            total_chores += 4
            if freq == "8":
                week1.insert(0, parsed_chore)
                week2.insert(0, parsed_chore)
                week3.insert(0, parsed_chore)
                week4.insert(0, parsed_chore)
                total_chores += 4


def print_weekly_chores(print_level):
    if print_level == 1:
        print("week 1: " + str(len(week1)) + " items")
        print("week 2: " + str(len(week2)) + " items")
        print("week 3: " + str(len(week3)) + " items")
        print("week 4: " + str(len(week4)) + " items")
        print("-------------------")
        print("(total chores: " + str(total_chores) + ")")
    elif print_level == 2:
        print("week1 --------------------------------------------")
        for c in week1:
            print(c + "\n")
        print("week2 --------------------------------------------")
        for c in week2:
            print(c + "\n")
        print("week3 --------------------------------------------")
        for c in week3:
            print(c + "\n")
        print("week4 --------------------------------------------")
        for c in week4:
            print(c + "\n")
        print("-------------------")
        print("(total chores: " + str(total_chores) + ")")


def parse_people_data():
    print("\n[INIT - reading people tsv]")
    global total_people
    # Define a filename.
    filename = "people_data.tsv"

    if not os.path.isfile(filename):
        print('File does not exist.')
        raise IOError

    day_people_map["mon"] = []
    day_people_map["tue"] = []
    day_people_map["wed"] = []
    day_people_map["thu"] = []
    day_people_map["fri"] = []
    day_people_map["sat"] = []
    day_people_map["sun"] = []

    # Open the file as f.
    # The function readlines() reads the file.

    reading_header = True
    with open(filename) as f:
        if reading_header:
            f.readline()
            reading_header = False

        content = f.read().splitlines()
        # print(content)

    # Show the file contents line by line.
    for line in content:
        # print(line)
        mon, tue, wed, thu, fri, sat, sun = line.split("\t")
        if mon != "":
            day_people_map["mon"].append(mon)
            total_people += 1
        if tue != "":
            day_people_map["tue"].append(tue)
            total_people += 1
        if wed != "":
            day_people_map["wed"].append(wed)
            total_people += 1
        if thu != "":
            day_people_map["thu"].append(thu)
            total_people += 1
        if fri != "":
            day_people_map["fri"].append(fri)
            total_people += 1
        if sat != "":
            day_people_map["sat"].append(sat)
            total_people += 1
        if sun != "":
            day_people_map["sun"].append(sun)
            total_people += 1


def print_people(print_level):
    if print_level == 1:
        print("mondays: " + str(len(day_people_map["mon"])) + " people")
        print("tuesdays: " + str(len(day_people_map["tue"])) + " people")
        print("wednesdays: " + str(len(day_people_map["wed"])) + " people")
        print("thursdays: " + str(len(day_people_map["thu"])) + " people")
        print("fridays: " + str(len(day_people_map["fri"])) + " people")
        print("saturdays: " + str(len(day_people_map["sat"])) + " people")
        print("sundays: " + str(len(day_people_map["sun"])) + " people")
        print("-------------------")
        print("(total people: " + str(total_people) + ")")

    elif print_level == 2:
        print("mondays: " + ' '.join(day_people_map["mon"]))
        print("tuesdays: " + ' '.join(day_people_map["tue"]))
        print("wednesdays: " + ' '.join(day_people_map["wed"]))
        print("thursdays: " + ' '.join(day_people_map["thu"]))
        print("fridays: " + ' '.join(day_people_map["fri"]))
        print("saturdays: " + ' '.join(day_people_map["sat"]))
        print("sundays: " + ' '.join(day_people_map["sun"]))
        print("-------------------")
        print("(total people: " + str(total_people) + ")")


parse_chores()
print_weekly_chores(1)

parse_people_data()
print_people(1)