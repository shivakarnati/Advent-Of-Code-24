import re
from operator import mul

with open('input_file.txt', 'r') as f:
    input_file = f.read()


def part1(input_file):
    total = 0
    for a, b in re.findall(r"mul\((\d+),(\d+)\)", input_file):
        total += int(a) * int(b)
    return total


def part2(input_file):
    do = r"do\(\)"
    dont = r"don't\(\)"
    mul = r"mul\((\d+),(\d+)\)"
    total = 0
    enabled = True
    for x in re.finditer(f'{do}|{dont}|{mul}', input_file):
        if re.fullmatch(do, x.group()):
            enabled = True
        elif re.fullmatch(dont, x.group()):
            enabled = False
        elif enabled:
            total += int(x.group(1)) * int(x.group(2))

    return total

print('Part 1:', part1(input_file))
print('Part 2:', part2(input_file))