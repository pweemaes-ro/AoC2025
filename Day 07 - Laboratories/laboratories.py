"""
Solutions for AoC 2025 Day 6.
"""
from collections import defaultdict
from io import TextIOWrapper


def get_solutions(file: TextIOWrapper) -> tuple[int, int]:
    """
    Return the solutions for part 1 and part 2.
    """

    file.seek(0)
    lines = file.readlines()

    split_count = 0
    min_position, max_position = 0, len(lines[0]) - 1
    positions = {lines[0].index('S'): 1}
    new_positions: defaultdict[int, int] = defaultdict(int)

    for line in lines[1:]:
        for position in positions:
            paths_count = positions.get(position, 0)
            if line[position] == "^":
                if position >= min_position + 1:
                    new_positions[position - 1] += paths_count
                if position <= max_position - 1:
                    new_positions[position + 1] += paths_count
                split_count += 1
            else:
                new_positions[position] += paths_count
        positions, new_positions = new_positions, defaultdict(int)

    return split_count, sum(positions.values())


# pylint: disable = duplicate-code
def _main() -> None:
    for test in (True, False):

        if test:
            filename = "laboratories_test_input.txt"
            expected = 21, 40
        else:
            filename = "laboratories_input.txt"
            expected = 1594, 15650261281478

        with open(filename, encoding="utf-8") as file:
            solutions = get_solutions(file)
            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
