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
        self.expansion_map = self.separation.row_col_map()
        self.row_expansion, self.col_expansion = self.expansions(
            self.expansion_map.row_map
        ), self.expansions(self.expansion_map.col_map)

    def expansions(self, rowcol_map: dict[int]) -> list[int]:
        """Returns a list of multipliers for how much larger each row/column
        becomes in the map."""
        expansion = []
        for val in set(rowcol_map.values()):
            expansion.append(sum(1 for v in rowcol_map.values() if v == val))
        return expansion

    def map_param(self, param: Parameter) -> Parameter:
        """Maps a parameter to a new parameter."""
        param_row_expansion = self.expansions(param.row_map)
        param_col_expansion = self.expansions(param.col_map)
        new_param_row_expansion = [
            param_row_expansion[i] * self.row_expansion[i]
            for i in range(len(param_row_expansion))
        ]  ## TODO: these might not line up! Only use part of self.row_expansion that
        # maps to image region of param in bt. Maybe create them as dict so can keep
        # track of where each multiplier comes from?
        new_param_col_expansion = [
            param_col_expansion[i] * self.col_expansion[i]
            for i in range(len(param_col_expansion))
        ]
        row_partial_sum = list(accumulate(new_param_row_expansion))
        col_partial_sum = list(accumulate(new_param_col_expansion))
        ## Expand param based on these partial sums

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
