"""
Solutions for AoC 2025 Day 3.
"""
from collections.abc import Iterable
from io import TextIOWrapper


def _get_power_banks(file: TextIOWrapper) -> list[str]:
    """
    Return a list of all powerbanks in the file.
    """

    return [s[:-1] for s in file.readlines()]


def _get_output_joltage(bank: str, nr_digits: int) -> str:
    """
    Return the max joltage in the bank consisting of given nr of digits.
    """

    if nr_digits == 1:
        return max(bank)
    pos = bank.find(digit := max(bank[:-nr_digits + 1]))
    return digit + _get_output_joltage(bank[pos + 1:], nr_digits - 1)


def get_output_joltage_01(banks: Iterable[str]) -> int:
    """
    Return the solution for part 1.
    """

    return sum(int(_get_output_joltage(bank, 2)) for bank in banks)


def get_output_joltage_02(banks: Iterable[str]) -> int:
    """
    Return the solution for part 2.
    """

    return sum(int(_get_output_joltage(bank, 12)) for bank in banks)


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "lobby_test_input.txt"
            expected = 357, 3121910778619
        else:
            filename = "lobby_input.txt"
            expected = 17427, 173161749617495

        with open(filename, encoding="utf-8") as file:
            power_banks = _get_power_banks(file)
            solutions = (get_output_joltage_01(power_banks),
                         get_output_joltage_02(power_banks))
            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
