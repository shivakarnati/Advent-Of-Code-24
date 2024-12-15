from __future__ import annotations

import sys
from typing import Optional


def get_start_position(data: list[str]) -> tuple[int, int] | None:
    """Find the start position in the provided grid."""
    for y, line in enumerate(data):
        x = line.find("^")
        if x != -1:
            return x, y
    return None


def get_data(
    test_data: Optional[str] = None,
) -> tuple[tuple[int, int], tuple[int, int], list[str]]:
    """Get the input data.

    Will return a tuple with the first item being another tuple containing
    (width x height), the second containing (x,y) of the start location,
    followed by a list of strings with the full data.

    We assume the input is square, or at least all lines have the same length.
    """
    if test_data:
        data = test_data.split()
    else:
        with open("input.txt") as file:
            data = file.readlines()

    # get dimensions
    width = len(data[0].strip())
    height = len(data)

    # find start place
    start = get_start_position(data)
    if not start:
        print("Cannot determine start location")
        sys.exit(1)

    return ((width, height), start, data)


def part1(
    dimensions: tuple[int, int],
    start_pos: tuple[int, int],
    grid: list[str],
) -> int:
    """Solve part 1 of the puzzle."""
    # Direction vectors for [up, right, down, left] as [y, x]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    current_direction = 0  # Start facing up

    # Get input data
    width, height = dimensions
    visited = {start_pos}
    current_pos = start_pos

    while True:
        # Calculate next position
        next_y = current_pos[1] + directions[current_direction][0]
        next_x = current_pos[0] + directions[current_direction][1]

        # Check if we're about to leave the grid
        if not (0 <= next_y < height and 0 <= next_x < width):
            break

        # Check if there's an obstacle ahead
        if grid[next_y][next_x] == "#":
            # Turn right
            current_direction = (current_direction + 1) % 4
        else:
            # Move forward
            current_pos = (next_x, next_y)
            visited.add(current_pos)

    return len(visited)


def part2(
    dimensions: tuple[int, int], start_pos: tuple[int, int], grid: list[str]
) -> int:
    """Solve part 2 of the puzzle."""
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    width, height = dimensions
    valid_positions = 0

    current_pos = start_pos
    current_direction = 0
    original_path = set()
    adjacent_positions = set()

    # Get the original path and build set of adjacent positions Really should be
    # able to extract this out so can be used in both Part1 and Part2, maybe
    # later if i have a bit of time.
    while True:
        state = (*current_pos, current_direction)
        if state in original_path:
            break
        original_path.add(state)

        # Add adjacent positions to test
        for dy, dx in directions:
            adj_y = current_pos[1] + dy
            adj_x = current_pos[0] + dx
            if (
                0 <= adj_y < height
                and 0 <= adj_x < width
                and grid[adj_y][adj_x] == "."
                and (adj_x, adj_y) != start_pos
            ):
                adjacent_positions.add((adj_x, adj_y))

        # Calculate next position
        next_y = current_pos[1] + directions[current_direction][0]
        next_x = current_pos[0] + directions[current_direction][1]

        if not (0 <= next_y < height and 0 <= next_x < width):
            break

        if grid[next_y][next_x] == "#":
            current_direction = (current_direction + 1) % 4
        else:
            current_pos = (next_x, next_y)

    # Now test only adjacent positions
    for test_x, test_y in adjacent_positions:
        current_pos = start_pos
        current_direction = 0
        path = set()

        while True:
            state = (*current_pos, current_direction)
            if state in path:
                valid_positions += 1
                break

            path.add(state)

            next_y = current_pos[1] + directions[current_direction][0]
            next_x = current_pos[0] + directions[current_direction][1]

            if not (0 <= next_y < height and 0 <= next_x < width):
                break

            # Check if next position is our test obstacle
            if (next_x, next_y) == (test_x, test_y) or grid[next_y][next_x] == "#":
                current_direction = (current_direction + 1) % 4
            else:
                current_pos = (next_x, next_y)

    return valid_positions


test_data = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


def main() -> None:
    """Run the AOC problems for Day 6."""
    dimensions, start_pos, grid = get_data()

    result1 = part1(dimensions, start_pos, grid)
    print(f"Part 1: The guard will visit {result1} distinct positions.") # 5331

    result2 = part2(dimensions, start_pos, grid)
    print(
        f"Part 2: We can find {result2} different positions to block so as to put the guard in a loop." 
    ) # 1812


if __name__ == "__main__":
    main()