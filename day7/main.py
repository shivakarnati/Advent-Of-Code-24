from __future__ import annotations

import time
from functools import wraps
from itertools import product
from pathlib import Path
from typing import TYPE_CHECKING, Callable, ParamSpec, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure the execution time of a function in milliseconds.

    This is a decorator that can be added to any function.
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time_ms = (end_time - start_time) * 1000
        print(f"{func.__name__}() took {elapsed_time_ms:.3f} ms")
        return result

    return wrapper


@timer
def get_data() -> Iterable[tuple[int, list[int]]]:
    """Process the input file and return a list of tuples.

    Each tuple contains:
        - An integer (test value)
        - A list of integers (operators)

    This could be done with a generator instead to reduce memory usage, but
    since it is needed in part2 as well we would have to regenerate it, and that
    would cost twice the disk access time.
    """
    with Path("./input.txt").open() as file:
        return [
            (
                int(line_parts[0][:-1]),  # Test value (remove trailing colon)
                list(map(int, line_parts[1:])),  # List of operators
            )
            for line in file
            if (line_parts := line.strip().split(" "))
        ]


def is_valid_equation(target: int, numbers: list[int], operators: list[str]) -> bool:
    """Check if the target value can be produced with provided operators."""
    num_operators = len(numbers) - 1
    all_operator_combinations = product(operators, repeat=num_operators)

    for operator_combination in all_operator_combinations:
        result = numbers[0]
        for num, op in zip(numbers[1:], operator_combination):
            if op == "+":
                result += num
            elif op == "*":
                result *= num
            elif op == "||":
                result = int(str(result) + str(num))

            # Prune if result exceeds the target (assuming non-negative numbers)
            if result > target:
                break
        else:  # Only execute if the loop didn't break
            if result == target:
                return True
    return False


@timer
def part1(
    data: Iterable[tuple[int, list[int]]],
) -> tuple[int, list[tuple[int, list[int]]]]:
    """Solve Part 1.

    We determine the total of all valid test values using + and *.
    Returns the total and the list of failed equations.
    """
    total = 0
    failed_equations = []

    for target, numbers in data:
        if is_valid_equation(target, numbers, ["+", "*"]):  # Only + and *
            total += target
        else:
            failed_equations.append((target, numbers))  # Keep track of failed equations

    return total, failed_equations


@timer
def part2(failed_data: list[tuple[int, list[int]]]) -> int:
    """Solve Part 2.

    We only work on the failed sets from the first part.
    """
    total = 0
    for target, numbers in failed_data:
        if is_valid_equation(target, numbers, ["+", "*", "||"]):  # Include ||
            total += target
    return total


def main() -> None:
    data = get_data()

    # Part 1 - answer for me is 6083020304036
    result1, failed_data = part1(data)
    print(f"Part 1: The total calibration result is : {result1}")

    # Part 2 - answer for me is 59002246504791
    result2 = result1 + part2(failed_data)
    print(f"Part 2: The Fixed calibration result is : {result2}")


if __name__ == "__main__":
    main()