"""
Solutions for AoC 2025 Day 1.
"""
from operator import sub, add


def get_pwd_01(filename: str) -> int:
    """
    Calculate the password from the turns in data_file.
    """

    password, current = 0, 50

    with open(filename, encoding="utf-8") as data_file:
        while turn := data_file.readline():
            if turn[0] == "R":
                current = (current + int(turn[1:])) % 100
            else:
                assert turn[0] == "L"
                current = (current - int(turn[1:])) % 100
            password += int(current == 0)

    return password


def get_pwd_02(filename: str) -> int:
    """
    Calculate the password from the turns in data_file.
    """

    password, current = 0, 50

    with open(filename, encoding="utf-8") as data_file:
        while turn := data_file.readline():
            passes, remaining = divmod(int(turn[1:]), 100)
            operator = add if turn[0] == "R" else sub
            new_current = operator(current, remaining) % 100
            if current != 0:
                passes += int((operator is add and current > new_current) or
                              (operator is sub and current < new_current) or
                              new_current == 0)
            password, current = password + passes, new_current

    return password


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "secret_entrance_test_input_01.txt"
            expected = 3, 6
        else:
            filename = "secret_entrance_input_01.txt"
            expected = 964, 5872

        solutions = get_pwd_01(filename), get_pwd_02(filename)
        assert solutions == expected

    print("OK!")


_main()
