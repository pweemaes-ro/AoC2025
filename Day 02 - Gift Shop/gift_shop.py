"""
Solutions for AoC 2025 Day 2.
"""
import re
from collections.abc import Iterator, Sequence
from io import TextIOWrapper


# I considered sorting and merging the intervals, to avoid checking numbers
# more than once, but it turned out there is no overlap in the intervals...
def merge_intervals(intervals: Sequence[tuple[int, int]]) -> \
        Sequence[tuple[int, int]]:
    """
    Reduce a list of integer intervals, by merging overlapping and connected
    intervals. Return the (sorted) result.
    """

    if len(intervals) == 0:
        return []

    (sorted_intervals := list(intervals)).sort(key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        last = merged[-1]
        # If current overlaps or is connected to last: merge them!
        if current[0] <= last[1] + 1:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)

    return merged


def _merged_intervals(intervals: Sequence[tuple[int, int]]) \
        -> Iterator[tuple[int, int]]:
    """
    Same as merge_intervals, but now as a generator. Yield integer intervals,
    by merging overlapping and connected intervals.
    """

    if len(intervals) == 0:
        return

    (sorted_intervals := list(intervals)).sort(key=lambda x: x[0])
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

    pattern = re.compile(r'^(.+?)\1+$')

    return sum(x if pattern.match(str(x)) else 0
               for first, last in intervals
               for x in range(first, last + 1))


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "gift_shop_test_input.txt"
            expected = 1227775554, 4174379265
        else:
            filename = "gift_shop_input.txt"
            expected = 12850231731, 24774350322

        with open(filename, encoding="utf-8") as file:
            # intervals_before = list(_intervals(file))
            # intervals_after = list(_merged_intervals(file))
            # print(len(intervals_before))
            # print(len(intervals_after))
            # print(sum((b - a) for (a, b) in intervals_before))
            # print(sum((b - a) for (a, b) in intervals_before))
            # solutions = (sum_invalid_ids_01(_merged_intervals(file)),
            #              sum_invalid_ids_02(_merged_intervals(file)))
            solutions = (sum_invalid_ids_01(_intervals(file)),
                         sum_invalid_ids_02(_intervals(file)))
            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
