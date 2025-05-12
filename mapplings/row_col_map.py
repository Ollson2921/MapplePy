"""Module with the inherited RowColMap class."""

from typing import Iterable, Tuple, List, DefaultDict, Iterator, Callable
from gridded_cayley_permutations.row_col_map import RowColMap as RCMap


class RowColMap(RCMap):
    """The new rowcolmap used for mapplings"""

    def __init__(self, col_map, row_map):
        super().__init__(col_map, row_map)

    def preimages_of_rows_and_cols(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> Tuple[set[int], set[int]]:
        return set(self.preimages_of_cols(cols)), set(self.preimages_of_rows(rows))

    def images_of_cols(self, cols: Iterable[int]) -> set[int]:
        return {self.col_map[col] for col in cols}

    def images_of_rows(self, rows: Iterable[int]) -> set[int]:
        return {self.row_map[row] for row in rows}

    def images_of_rows_and_cols(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> Tuple[set[int], set[int]]:
        return self.images_of_cols(cols), self.images_of_rows(rows)
