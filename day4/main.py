# open the input file
with open("input.txt") as file:
    input_grid = file.readlines()

def part1(grid: list[str]) -> int:
    # helpful to check all the directions
    def is_valid(nr: int, nc: int, char: str) -> bool:
        return 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == char

    count = 0
    rows, cols = len(grid), len(grid[0])
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    ]
    target = "XMAS"
    target_chars = list(target)
    target_len = len(target)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != target_chars[0]:
                continue
            for dr, dc in directions:
                if all(
                    is_valid(r + dr * i, c + dc * i, target_chars[i])
                    for i in range(target_len)
                ):
                    count += 1

    return count


def part2(grid: list[str]) -> int:

    rows, cols = len(grid), len(grid[0])
    count = 0

    if rows < 3 or cols < 3:
        return 0 
    
    # check if we can form two 'MAS' segments in the X
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Center must be 'A'
            if grid[r][c] != "A":
                continue

            # check all possible diagonal configurations
            top_left = grid[r - 1][c - 1]
            top_right = grid[r - 1][c + 1]
            bottom_left = grid[r + 1][c - 1]
            bottom_right = grid[r + 1][c + 1]

            if (top_left + bottom_right in {"MS", "SM"}) and (
                top_right + bottom_left in {"MS", "SM"}
            ):
                count += 1
    return count


print(f"Answer for Part 1 is {part1(input_grid)}")
print(f"Answer for Part 2 is {part2(input_grid)}")