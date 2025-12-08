"""
Solutions for AoC 2025 Day 2.
"""
from collections.abc import Iterator
from io import TextIOWrapper


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
        for x in range(first, last + 1):
            for d in range(1, (n := len(s := str(x))) // 2 + 1):
                if n % d == 0:
                    base = s[0: d]
                    if all((s[i: i + d] == base) for i in range(d, n, d)):
                        total += x
                        break

    return total


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "02_gift_shop_test_input.txt"
            expected = 1227775554, 4174379265
        else:
            filename = "02_gift_shop_input.txt"
            expected = 12850231731, 24774350322

        with open(filename, encoding="utf-8") as file:
            solutions = (sum_invalid_ids_01(_intervals(file)),
                         sum_invalid_ids_02(_intervals(file)))
            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
