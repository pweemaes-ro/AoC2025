"""
Solutions for AoC 2025 Day 2.
"""
import re
from collections.abc import Iterator
from functools import lru_cache
from io import TextIOWrapper


def get_split_intervals(first: int, last: int) -> list[tuple[int, int]]:
    """
    Split the interval into ordered list of intervals, with first and last of
    equal nr of digits. If first and last are already of equal nr of digits,
    the orignal interval is returned, else a list of two or more new intervals
    is returned.
    Example: with first = 950 and last = 1100, [(950, 999), (1000, 1100)] is
    returned.
    """

    if (dif := len(str(last)) - (len_first := len(str(first)))) == 0:
        return [(first, last)]

    result = []
    new_first = first

    for _ in range(dif + 1):
        new_last = min(10 ** len_first - 1, last)
        result.append((new_first, new_last))
        new_first = new_last + 1
        len_first += 1
    return result


@lru_cache
def get_repeat_infos(n: int) -> list[tuple[int, int]]:
    """
    Return tuples of all divisors d of n, except n itself, and n // d.
    Example: for n = 8, return [(1, 8), (2, 4), (4, 2)], do not include (8, 1).
    """

    divisors = []
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            divisors.append((i, n // i))
    return divisors


def _intervals(file: TextIOWrapper) -> Iterator[tuple[int, int]]:
    """
    Yield tuple[first, last] from file, where file contains a single line
    consisting of comma-separated first-last.
    """

    file.seek(0)
    for interval in file.readline().split(','):
        first, last = map(int, interval.split('-'))
        yield first, last


def sum_invalid_ids_01(intervals: Iterator[tuple[int, int]]) -> int:
    """
    Return solution for part 1.
    """

    return sum(sum(x for x in range(first, last + 1)
                   if not (n := len(s := str(x))) % 2
                   and s[:n // 2] == s[n // 2:])
               for first, last in intervals)


def sum_invalid_ids_02(intervals: Iterator[tuple[int, int]]) -> int:
    """
    Return solution for part 2.
    """

    total = 0

    for first, last in intervals:
        split_intervals = get_split_intervals(first, last)

        for split_first, split_last in split_intervals:
            length = len(str(split_first))
            repeat_infos = get_repeat_infos(length)

            for s in map(str, range(split_first, split_last + 1)):
                for repeat_length, repeats in repeat_infos:
                    if s == s[:repeat_length] * repeats:
                        total += int(s)
                        break

    return total


def re_sum_invalid_ids_02(intervals: Iterator[tuple[int, int]]) -> int:
    """
    Return solution for part 2.
    """

    pattern = re.compile(r'^(.+?)\1+$')
    return sum(x if pattern.match(str(x)) else 0
               for first, last in intervals
               for x in range(first, last + 1))


def _main() -> None:
    for test in (True, False,):

        if test:
            filename = "gift_shop_test_input.txt"
            expected = 1227775554, 4174379265
        else:
            filename = "gift_shop_input.txt"
            expected = 12850231731, 24774350322

        with open(filename, encoding="utf-8") as file:
            solutions = (sum_invalid_ids_01(_intervals(file)),
                         sum_invalid_ids_02(_intervals(file)))
            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
