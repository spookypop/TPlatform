def find_type(actions):
    actions = int(actions)
    if 1 <= actions <= 3:
        return 1
    elif 5 <= actions <= 10:
        return 2
    elif 14 <= actions <= 17:
        return 3
    elif (11 <= actions <= 13) or actions == 4:
        return 4
