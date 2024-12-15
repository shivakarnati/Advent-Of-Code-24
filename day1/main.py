import os
import numpy as np

def get_data():
    
    cwd = os.getcwd()
    with open(cwd + '/input_file.txt', 'r') as file:
        data = file.readlines()
        column1 = []
        column2 = []
        for line in data:
            # split the data using whitespaces
            values = line.strip().split()  
            if len(values) == 2: 
                column1.append(int(values[0]))  
                column2.append(int(values[1])) 
    return column1, column2
 
def part1():
    
    column1, column2 = get_data()
    # sort, and check absolute difference between the values
    a1 = np.sort(np.array(column1))
    a2 = np.sort(np.array(column2))

    abs_diff = np.sum(np.abs(a1 - a2))
    
    return abs_diff

def part2():
    column1, column2 = get_data()
    b = 0
    for i in column1:
        # count the similarity score in column2
        sim_score = column2.count(i)
        b += i*sim_score

    return b

print("Part1 answer is:", part1())

print("Part2 answer is :", part2())

