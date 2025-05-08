"""Module with the inherited RowColMap class."""

from gridded_cayley_permutations.row_col_map import RowColMap as RCMap


class RowColMap(RCMap):
    """The new rowcolmap used for mapplings"""
    def __init__(self, col_map, row_map):
        super().__init__(col_map, row_map)
