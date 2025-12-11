"""
Solutions for AoC 2025 Day 4.
"""
from collections.abc import Sequence, Iterator
from io import TextIOWrapper

type Interval = tuple[int, int]
type Id = int


def _sorted_merged_intervals(intervals: Sequence[Interval]) \
        -> Iterator[Interval]:
    """
    Same as merge_intervals, but now as a generator. Yield integer intervals,
    by merging overlapping and connected intervals.
    """

    if len(intervals) == 0:
        return

    (sorted_intervals := list(intervals)).sort()
    last = sorted_intervals[0]

    for current in sorted_intervals[1:]:
        # If current overlaps or is connected to last: merge them, but don't
        # yield yet, since it may merge with next!
        if current[0] <= last[1] + 1:
            last = (last[0], max(last[1], current[1]))
        else:
            yield last
            last = current

    yield last


def _intervals_and_ids(file: TextIOWrapper) -> tuple[list[Interval], list[Id]]:
    file.seek(0)

    intervals = []

    while len(line := file.readline()) > 1:
        first, last = map(int, line.split('-'))
        intervals.append((first, last))

    ids = [int(line) for line in file.readlines()]

    return list(_sorted_merged_intervals(intervals)), sorted(ids)


def get_solutions(file: TextIOWrapper) -> tuple[int, int]:
    """
    Return a tuple of solution for parts 1 and 2.
    """

    intervals, ids = _intervals_and_ids(file)
    fresh_ids = sum(iv[1] - iv[0] + 1 for iv in intervals)

    found = 0
    nr_intervals = len(intervals)
    interval_offset = 0

    for _id in ids:
        while (interval := intervals[interval_offset])[1] < _id:
            interval_offset += 1
            if interval_offset == nr_intervals:
                break
        else:
            found += int(interval[0] <= _id)

    return found, fresh_ids


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "cafeteria_test_input.txt"
            expected = 3, 14
        else:
            filename = "cafetera_input.txt"
            expected = 726, 354226555270043

        with open(filename, encoding="utf-8") as file:
            solutions = get_solutions(file)
            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
