"""
Solutions for AoC 2025 Day 1.
"""
from collections.abc import Iterator
from io import TextIOWrapper


def _turns(file: TextIOWrapper) -> Iterator[tuple[int, int]]:
    """
    Yield tuple[direction, clicks] with direction == 1 if clockwise, else -1.
    """

    file.seek(0)
    while turn := file.readline():
        direction = 1 if turn[0] == "R" else -1
        clicks = int(turn[1:])
        yield direction, clicks


def get_pwd_01(turns: Iterator[tuple[int, int]]) -> int:
    """
    Calculate the password from the turns (part 1 solution).
    """

    pwd, pos = 0, 50

    for (direction, clicks) in turns:
        pwd += int((pos := (pos + direction * clicks) % 100) == 0)

    return pwd


def get_pwd_02(turns: Iterator[tuple[int, int]]) -> int:
    """
    Calculate the password from the turns (part 2 solution).
    """

    pwd, pos = 0, 50

    for (direction, clicks) in turns:
        pwd += clicks // 100
        new_position = (pos + direction * clicks % 100) % 100
        if pos != 0:
            pwd += int((direction * pos > direction * new_position) or
                       new_position == 0)
        pos = new_position

    return pwd


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "secret_entrance_test_input.txt"
            expected = 3, 6
        else:
            filename = "secret_entrance_input.txt"
            expected = 964, 5872

        with open(filename, encoding="utf-8") as file:
            solutions = get_pwd_01(_turns(file)), get_pwd_02(_turns(file))
            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
