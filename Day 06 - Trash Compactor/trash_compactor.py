"""
Solutions for AoC 2025 Day 6.
"""
from re import compile as regexp_compile
from io import TextIOWrapper
from math import prod

nrs_pattern = regexp_compile(r'\d+')
ops_pattern = regexp_compile(r'([*+])')


def _transpose_to_ints(strings: list[str]) -> list[int]:
    """
    Given a list of strings representing ints transpose the strings and return
    a list of integers represented by the transposed strings. The input strings
    may have leading and/or trailing spaces, but must be of equal length!

    Example: The list of input strings:

    [" 4 ",
     "636"
     "612"
     "996"]

    results in transposed strings

    [" 669",
     "4319",
     " 629"]

    so the returned list of integers is

    [669, 4319, 626]
    """

    return [int(t) for t in (''.join(s[c] for s in strings)
                             for c in range(len(strings[0])))]


def _get_total(ops_and_offsets: list[tuple[str, int]], int_rows: list[str]) \
        -> int:
    """
    Return the total for part 2 calculated from a list of (operator, offset)
    pairs and a list of string lines from the input.
    """

    op, offset = ops_and_offsets[0][0], 0
    total = 0

    for next_op, next_offset in ops_and_offsets[1:]:
        strings = [int_row[offset: next_offset - 1] for int_row in int_rows]
        operands = _transpose_to_ints(strings)
        total += sum(operands) if op == '+' else prod(operands)
        offset, op = next_offset, next_op

    return total


def solve_part_1(file: TextIOWrapper) -> int:
    """
    Return the solution for part 1.
    """

    nr_rows = []
    ops = []

    file.seek(0)
    for line in file.readlines():
        if line[0] in ('+', '*'):
            ops = ops_pattern.findall(line)
        else:
            nr_rows.append(list(map(int, nrs_pattern.findall(line))))

    total = 0

    for i, op in enumerate(ops):
        operands = [nr_row[i] for nr_row in nr_rows]
        total += sum(operands) if op == '+' else prod(operands)
    return total


def solve_part_2(file: TextIOWrapper) -> int:
    """
    Return the solution for part 2.
    """

    file.seek(0)

    int_rows: list[str] = []
    ops_and_offsets = []

    for line in file.readlines():
        if line[0] not in ('+', '*'):
            int_rows.append(line[:-1])  # skip newline char at end of each line
        else:
            ops_and_offsets = [(match.group(), match.start())
                               for match in ops_pattern.finditer(line)]
            max_length = max(len(s) for s in int_rows)
            # add one dummy operator at virtual next operator position
            ops_and_offsets.append(('DUMMY', max_length + 1))
            # pad strings in int_rows with spaces if necessary
            int_rows = [s + ' ' * (max_length - len(s)) for s in int_rows]
            break

    return _get_total(ops_and_offsets, int_rows)


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "trash_compactor_test_input.txt"
            expected = 4277556, 3263827
        else:
            filename = "trash_compactor_input.txt"
            expected = 4583860641327, 11602774058280

        with open(filename, encoding="utf-8") as file:
            solution = solve_part_1(file), solve_part_2(file)
            print(solution)
            assert solution == expected

    print("OK!")


_main()
