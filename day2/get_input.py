import os

def is_safe(lst):
    diff_range = range(1, 4)
    increasing = all(lst[i] < lst[i+1] for i in range(len(lst)-1))
    decreasing = all(lst[i] > lst[i+1] for i in range(len(lst)-1))
    
    if not (increasing or decreasing):
        return False
    for i in range(1, len(lst)):
        if abs(lst[i] - lst[i-1]) not in diff_range:
            return False
    return True

def get_data():
    cwd = os.getcwd()
    with open(cwd + '/input_file.txt', 'r') as file:
        data = file.readlines()
        column = []
        for line in data:
            values = line.strip().split()
            column.append(values)
    return column

def part1():
    column = get_data()
    safe_count = 0

    for row in column:
        individual_lst = list(map(int, row))
        if is_safe(individual_lst):
            safe_count += 1

    print(f"Total safe reports in part 1 are: {safe_count}")
    

def part2():
    column = get_data()
    safe_count = 0

    for row in column:
        individual_lst = list(map(int, row))
        if is_safe(individual_lst):
            safe_count += 1
        else:
            # check if removing one element makes it safe
            for i in range(len(individual_lst)):
                temp_lst = individual_lst[:i] + individual_lst[i+1:]
                if is_safe(temp_lst):
                    safe_count += 1
                    break

    print(f"Total safe reports in part 2 are: {safe_count}")

part1()
part2()