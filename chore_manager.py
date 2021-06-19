import os.path

chore_map = dict()
week1 = []
week2 = []
week3 = []
week4 = []
locked_day = []


def read_chores_list():
    print("[INIT - reading chores csv]")
    # Define a filename.
    filename = "chore_list_data.tsv"

    if not os.path.isfile(filename):
        print('File does not exist.')

    # Open the file as f.
    # The function readlines() reads the file.

    reading_header = True
    with open(filename) as f:
        if reading_header:
            f.readline()
            reading_header = False

        content = f.read().splitlines()
        # print(content)

    twice_weekly = []

    # Show the file contents line by line.
    for line in content:
        # print(line)
        key, desc, freq, prio, locked_day = line.split("\t")
        chore_map[key] = (desc, freq, prio)
        if locked_day != "any":
            locked_day.append((key, desc, freq, prio, locked_day))
            # todo: incomplete

        if freq == "1":
            week2.append(key)
        elif freq == "2":
            week1.append(key)
            week3.append(key)
        elif freq == "4":
            week1.append(key)
            week2.append(key)
            week3.append(key)
            week4.append(key)
            if freq == "8":
                week1.insert(0, key)
                week2.insert(0, key)
                week3.insert(0, key)
                week4.insert(0, key)


def print_weekly_chores(print_level):
    if print_level == 1:
        print("week 1: " + str(len(week1)) + " items")
        print("week 2: " + str(len(week2)) + " items")
        print("week 3: " + str(len(week3)) + " items")
        print("week 4: " + str(len(week4)) + " items")
    elif print_level == 2:
        print("week1 --------------------------------------------")
        for c in week1:
            print(chore_map.get(c)[0])
        print("week2 --------------------------------------------")
        for c in week2:
            print(chore_map.get(c)[0])
        print("week3 --------------------------------------------")
        for c in week3:
            print(chore_map.get(c)[0])
        print("week4 --------------------------------------------")
        for c in week4:
            print(chore_map.get(c)[0])


read_chores_list()
print_weekly_chores(1)
