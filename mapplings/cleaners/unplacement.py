"""Contains the ParamUnplacement class"""

from itertools import product
from typing import Iterator
from functools import cached_property

from gridded_cayley_permutations import RowColMap, GriddedCayleyPerm
from gridded_cayley_permutations.simplify_obstructions_and_requirements import (
    SimplifyObstructionsAndRequirements as Simplify,
)
from gridded_cayley_permutations.unplacement import PartialUnplacement
from mapplings import Parameter, MappedTiling


class ParamUnplacement(PartialUnplacement):
    """A class for unplacing point rows and cols in a parameter"""

    def __init__(self, param: Parameter, parent_mappling: MappedTiling):
        self.param = param
        self.base = parent_mappling
        self.base_obs = parent_mappling.obstructions
        super().__init__(param.ghost)

    def implied_point_obs(self) -> Iterator[GriddedCayleyPerm]:
        """Finds point obs in the parameter that are implied by the base mappling"""
        for cells in product(self.param.empty_cells(), self.param.positive_cells()):
            pos = sorted(cells)
            pattern = (pos[0][1] > pos[1][1], pos[1][1] > pos[0][1])
            gcp = GriddedCayleyPerm(pattern, pos)
            if self.param.map.map_gridded_cperm(gcp) not in self.base_obs:
                yield GriddedCayleyPerm((0,), (cells[0],))

    @cached_property
    def expected_obs(self) -> set[GriddedCayleyPerm]:
        unsimplified = tuple(super().expected_obs | set(self.implied_point_obs()))
        algo = Simplify(unsimplified, tuple(tuple()), self.param.dimensions)
        algo.simplify()
        return set(algo.obstructions)

    def check_cols_and_rows(
        self, check_cols: set[int], check_rows: set[int]
    ) -> tuple[set[int], set[int]]:
        """Filters the input cols and rows to only include those which can be unplaced."""
        valid_cols = {
            col
            for col in check_cols & self.positive_cols
            if (0 < col < self.dimensions[0] - 1)
        }
        valid_rows = {
            row
            for row in check_rows & self.positive_rows
            if (0 < row < self.dimensions[1] - 1)
        }
        valid_cols = {
            col
            for col in valid_cols
            if self.param.col_map[col - 1] == self.param.col_map[col + 1]
        }
        valid_rows = {
            row
            for row in valid_rows
            if self.param.row_map[row - 1] == self.param.row_map[row + 1]
        }
        valid_cols = set(filter(self.col_fuse_check, valid_cols))
        valid_rows = set(filter(self.row_fuse_check, valid_rows))
        return valid_cols, valid_rows

    def param_unplace(
        self, unplace_cols: set[int], unplace_rows: set[int]
    ) -> Parameter:
        """Unplaces rows and cols in the ghost and creates a new row col map"""
        if not any((unplace_cols, unplace_rows)):
            return self.param
        new_ghost = self.unplace(unplace_cols, unplace_rows)

        col_preimages, row_preimages = self.adjustment_map(
            unplace_cols, unplace_rows
        ).preimage_map()

        new_col_map = {
            i: self.param.col_map[col_preimages[i][0]]
            for i in range(new_ghost.dimensions[0])
        }
        new_row_map = {
            i: self.param.row_map[row_preimages[i][0]]
            for i in range(new_ghost.dimensions[1])
        }
        return Parameter(new_ghost, RowColMap(new_col_map, new_row_map))

    def auto_unplace(self):
        """Does all valid unplacements for the tiling's point cells"""
        temp = self.param_unplace(set(), self.find_cols_and_rows()[1])
        new_algo = ParamUnplacement(temp, self.base)
        return new_algo.param_unplace(new_algo.find_cols_and_rows()[0], set())
