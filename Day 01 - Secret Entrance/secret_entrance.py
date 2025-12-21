"""
Solutions for AoC 2025 Day 1.
"""
from collections.abc import Iterable


def get_pwd_01(turns: Iterable[tuple[str, int]]) -> int:
    """
    Return the solution for part 1 (based on the faster RvB code...).
    """

    pos, pwd = 50, 0
    for directions, clicks in turns:
        if directions == "R":
            pos = (pos + clicks) % 100
        else:
            pos = (pos - clicks) % 100
        if pos == 0:
            pwd += 1

    return pwd


def get_pwd_02(turns: Iterable[tuple[str, int]]) -> int:
    """
    Return result for part 2 (based on faster RvB code...).
    """

    pos, pwd = 50, 0
    for direction, clicks in turns:
        quotient, remainder = divmod(clicks, 100)
        pwd += quotient
        if direction == "R":
            pos += remainder
            if pos > 99:
                pos -= 100
                pwd += 1
            elif pos == 0:
                pwd += 1
        else:
            old_dial = pos
            pos -= remainder
            if pos < 0:
                pos += 100
                if old_dial != 0:
                    pwd += 1
            elif pos == 0:
                pwd += 1

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
            turns = [(s[0], int(s[1:])) for s in file]
            solutions = get_pwd_01(turns), get_pwd_02(turns)
            print(solutions)
        assert solutions == expected

    print("OK!")


_main()
