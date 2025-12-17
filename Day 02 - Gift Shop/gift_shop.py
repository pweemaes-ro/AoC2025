"""
Solutions for AoC 2025 Day 2.
"""
from functools import lru_cache


@lru_cache
def get_repeat_infos(n: int) -> list[tuple[int, int]]:
    """
    Return tuples (d, n // d) of all divisors d of n, except n itself. Example:
    for n = 8, return [(1, 8), (2, 4), (4, 2)], but do not include (8, 1).
    """

    return [(i, n // i) for i in range(1, n // 2 + 1) if n % i == 0]


def get_first_last(length: int, first: int, last: int) -> tuple[int, int]:
    """
    Return tuple (s_first, s_last) where s_first is the smallest repeat string
    of length digits and s_last is the largest repeat string of length digits
    that might result in an invalid id. Example:

        get_first_last(length=3, first=123456789, last=234000000) => (123, 234)

    since for each nr in [123, 234], repeating nr may be in the interval
    [123456, 234000] (in fact: 123123123, 124124124, ..., 199199199, 200200200,
    ..., 233233233) are all invalid ids in [123456789, 234000000], but
    234234234 is not, since it is not in the interval),
    """

    s_first, s_last = first, last
    upper_limit = 10 ** length
    while s_first >= upper_limit:
        s_first //= 10
    while s_last >= upper_limit:
        s_last //= 10
    return s_first, s_last


def process_r_info(r_info: tuple[int, int], interval_first: int,
                   interval_last: int, part_1: set[int],
                   part_2: set[int]) -> None:
    """
    Process the repeat information on the interval (invalid ids for both parts
    are stored in the sets)
    """

    r_first, r_last = get_first_last(r_info[0], interval_first, interval_last)
    for repeat_start in range(r_first, r_last + 1):
        candidate = int(str(repeat_start) * (r_repeats := r_info[1]))
        if interval_first <= candidate <= interval_last:
            part_2.add(candidate)
            if r_repeats == 2:
                part_1.add(candidate)


def process_interval(interval_first: int, interval_last: int, part_1: set[int],
                     part_2: set[int]) -> None:
    """
    Process the interval (invalid ids for both parts are stored in the sets)
    """

    for length in range(len(str(interval_first)), len(str(interval_last)) + 1):

        repeat_last = min(interval_last, (i := 10 ** length) - 1)
        repeat_first = max(interval_first, i // 10)

        for r_info in get_repeat_infos(length):
            process_r_info(r_info, repeat_first, repeat_last, part_1, part_2)


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "gift_shop_test_input.txt"
            expected = 1227775554, 4174379265
        else:
            filename = "gift_shop_input.txt"
            expected = 12850231731, 24774350322

        with open(filename, encoding="utf-8") as file:
            intervals = list(tuple(map(int, interval.split('-')))
                             for interval in file.readline().split(','))
            part_1: set[int] = set()
            part_2: set[int] = set()

            for first, last in intervals:
                process_interval(first, last, part_1, part_2)

            solutions = sum(part_1), sum(part_2)

            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
