"""
Solutions for AoC 2025 Day 6.
"""
import re
from io import TextIOWrapper
from operator import add, mul


# Note for part 2: The positions of '+' and '*' on the last line
# (the operator line) determine the start of a next group of numbers on the
# numbers lines.
# 123 328  51 64
#  45 64  387 23
#   6 98  215 314
# *   +   *   +
# has operators at pos 0, 4, 8, 12 (don't assume regularity in the positions!)
# so
# 1st group of nrs is from col 0 to 3 inc
# 2nd group of nrs is from col 4 to 7 inc
# 3rd group of nrs is from col 8 to 11 inc
# 4th group of nrs is from col 12 to last
# this gives
# 1st group: 1, 24, 356 (operator: *)
# 1st group: 369, 248, 8 (operator: +)
# 1st group: 32, 581, 175 (operator: *)
# 1st group: 623, 431, 4 (operator: +)


def solve_part_1(file: TextIOWrapper) -> int:
    """
    Return the solution for part 1.
    """

    nrs = []
    ops = []
    nrs_pattern = re.compile(r'\d+')
    ops_pattern = re.compile(r'([*+])')

    file.seek(0)
    for line in file.readlines():
        if line[0] in ('+', '*'):
            ops = ops_pattern.findall(line)
        else:
            nrs.append(list(map(int, nrs_pattern.findall(line))))

    total = 0
    for i, op in enumerate(ops):
        operator = add
        result = 0
        if op == '*':
            operator = mul
            result = 1
        for row in nrs:
            result = operator(result, row[i])
        total += result

    return total


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "trash_compactor_test_input.txt"
            expected = 4277556, -1
        else:
            filename = "trash_compactor_input.txt"
            expected = 4583860641327, -1

        with open(filename, encoding="utf-8") as file:
            part_1 = solve_part_1(file)
            print(part_1)
            assert part_1 == expected[0]

    print("OK!")


_main()
