"""
Solutions for AoC 2025 Day 4.
"""
from io import TextIOWrapper

type Coordinate = tuple[int, int]
type RollsGrid = list[list[str]]
type NeigborCountsGrid = list[list[int]]


# pylint: disable=too-few-public-methods
class Rolls:
    """
    Class for holding info about the rolls and their neighbor-counts, plus two
    public functions that generate the solutions.
    """

    def __init__(self, file: TextIOWrapper) -> None:
        self._rolls = [list(line[:-1]) for line in file.readlines()]
        self._neighbor_counts = self._rolls_to_neighbors(self._rolls)
        self._accessible_rolls = self._get_accessible_rolls()

    @property
    def nr_accessible_rolls(self) -> int:
        """
        Return the nr of accessible rolls.
        """

        return len(self._accessible_rolls)

    def _get_accessible_rolls(self) -> set[Coordinate]:
        """
        Return a set of coordinates (r, c) of all currently accessible rolls,
        that is, rolls with less than four neighbors.
        """

        size_range = range(len(self._rolls))
        return set((r, c) for r in size_range for c in size_range
                   if self._neighbor_counts[r][c] < 4
                   and self._rolls[r][c] == '@')

    @staticmethod
    def _update_neighbor_count(grid: NeigborCountsGrid, location: Coordinate,
                               delta: int) -> None:
        """
        Increment the neighbor count for all neighbors of location (row, col)
        by delta.
        """

        row, col = location
        nr_rows = nr_cols = len(grid)
        is_first_row = row == 0
        is_last_row = row == nr_rows - 1
        is_first_col = col == 0
        is_last_col = col == nr_cols - 1

        # update the current row
        if not is_first_col:
            grid[row][col - 1] += delta
        if not is_last_col:
            grid[row][col + 1] += delta

        # update row above
        if not is_first_row:
            grid[row - 1][col] += delta
            if not is_first_col:
                grid[row - 1][col - 1] += delta
            if not is_last_col:
                grid[row - 1][col + 1] += delta

        # update row below
        if not is_last_row:
            grid[row + 1][col] += delta
            if not is_first_col:
                grid[row + 1][col - 1] += delta
            if not is_last_col:
                grid[row + 1][col + 1] += delta

    def _rolls_to_neighbors(self, grid: RollsGrid) -> NeigborCountsGrid:
        """
        Create and return a grid of size equal to rolls_grid, where each cell
        is an integer representing the number of neighbors (from 0 to 8) that
        are '@'. Assumes that the grid is square!
        """

        size_range = range(len(grid))
        neighbor_grid = [[0] * len(grid[0]) for _ in size_range]

        for row in size_range:
            for col in size_range:
                if grid[row][col] == "@":
                    self._update_neighbor_count(neighbor_grid, (row, col), 1)

        return neighbor_grid

    def remove_rolls(self) -> int:
        """
        Remove (repeatedly) all accessible rolls from the grid, until no more
        rolls are accessible. Return nr of removed rolls.
        """

        removed = 0

        while self.nr_accessible_rolls != 0:

            for r, c in self._accessible_rolls:
                self._update_neighbor_count(self._neighbor_counts, (r, c), -1)
                self._rolls[r][c] = '.'
                removed += 1

            self._accessible_rolls = self._get_accessible_rolls()

        return removed


def _main() -> None:
    for test in (True, False):

        if test:
            filename = "printing_department_test_input.txt"
            expected = 13, 43
        else:
            filename = "printing_department_input.txt"
            expected = 1367, 9144

        with open(filename, encoding="utf-8") as file:
            solutions = ((rolls_grid := Rolls(file)).nr_accessible_rolls,
                         rolls_grid.remove_rolls())
            print(solutions)
            assert solutions == expected

    print("OK!")


_main()
