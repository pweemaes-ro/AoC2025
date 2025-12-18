"""
Solutions for AoC 2025 Day 1.
"""
from collections.abc import Iterable
from io import TextIOWrapper


def get_turns(file: TextIOWrapper) -> list[tuple[int, int]]:
    """
    Return a list of tuples (direction, clicks) where direction == 1 if turn is
    clockwise ("R"), else -1.
    """

    return [(1 if turn[0] == "R" else - 1, int(turn[1:]))
            for turn in file.readlines()]


def get_pwd_01(turns: Iterable[tuple[int, int]]) -> int:
    """
    Calculate the password from the turns (part 1 solution).
    """

    pos = 50
    return sum(int((pos := (pos + direction * clicks) % 100) == 0)
               for direction, clicks in turns)


def get_pwd_02(turns: Iterable[tuple[int, int]]) -> int:
    """
    Calculate the password from the turns (part 2 solution).
    """

    pwd, pos = 0, 50

    for (direction, clicks) in turns:
        div, mod = divmod(clicks, 100)

        pwd += div
        new_position = (pos + direction * mod) % 100
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
            turns = get_turns(file)
            solutions = get_pwd_01(turns), get_pwd_02(turns)
            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
