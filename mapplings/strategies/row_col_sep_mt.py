"""Module for row and column separating mapped tilings and related strategies."""

from itertools import accumulate
from typing import Iterator
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)
from ..mapped_tiling import MappedTiling, Parameter, ParameterList


class LTRowColSeparationMT:
    """
    When separating, cells must be strictly above/below each other.
    """

    def __init__(self, mapped_tiling: MappedTiling):
        self.mt = mapped_tiling
        self.separation = LessThanRowColSeparation(self.mt.tiling)
        self.expansion_map = self.separation.row_col_map
        self.row_expansion, self.col_expansion = self.expansions(
            self.expansion_map.row_map
        ), self.expansions(self.expansion_map.col_map)

        self.row_expansion, self.col_expansion = {0: 3, 1: 2}, {
            0: 3,
            1: 2,
        }  # TODO: remove this!!

    def expansions(self, rowcol_map: dict[int]) -> dict[int]:
        """Returns a list of multipliers for how much larger each row/column
        becomes in the map."""
        expansion = {}
        for val in set(rowcol_map.values()):
            expansion[val] = sum(1 for v in rowcol_map.values() if v == val)
        return expansion

    def map_param(self, param: Parameter) -> Parameter:
        """Maps a parameter to a new parameter."""
        param_row_expansion = self.expansions(param.row_map)
        param_col_expansion = self.expansions(param.col_map)
        new_row_expan = {
            key: param_row_expansion[key] * self.row_expansion[key]
            for key in param_row_expansion
        }
        new_col_expan = {
            key: param_col_expansion[key] * self.col_expansion[key]
            for key in param_col_expansion
        }
        row_partial_sum = list(accumulate(new_row_expan.values()))
        col_partial_sum = list(accumulate(new_col_expan.values()))
        new_row_map = self.new_row_col_map(row_partial_sum)
        new_col_map = self.new_row_col_map(col_partial_sum)
        new_map = RowColMap(new_row_map, new_col_map)

        ## Expand param based on these partial sums

    def new_row_col_map(self, partial_sum: list[int]) -> dict[int, int]:
        """Creates a new row/col map based on the partial sums."""
        new_map = {}
        last_index = 0
        for idx, val in enumerate(partial_sum):
            for value in range(last_index, val):
                new_map[value] = idx
            last_index = val
        return new_map

    def separate(self) -> Iterator[MappedTiling]:
        """Returns MappedTilings with row and column separated."""
        new_avoiders = ParameterList(
            [self.map_param(param) for param in self.mt.avoiding_parameters]
        )
        new_containers = [
            ParameterList([self.map_param(param) for param in c_list])
            for c_list in self.mt.containing_parameters
        ]
        new_enumerators = [
            ParameterList([self.map_param(param) for param in c_list])
            for c_list in self.mt.enumerating_parameters
        ]
        for T in self.separation.row_col_separation():
            yield MappedTiling(T, new_avoiders, new_containers, new_enumerators)
