"""Contains the ParamUnplacement class"""

from gridded_cayley_permutations.row_col_map import RowColMap
from gridded_cayley_permutations.unplacement import PartialUnplacement
from mapplings import Parameter, MappedTiling


class ParamUnplacement(PartialUnplacement):
    """A class for unplacing point rows and cols in a parameter"""

    def __init__(self, param: Parameter):
        self.param = param
        # self.base = base_tiling
        # self.base_obs = base_tiling.obstructions
        super().__init__(param.ghost)

    def check_cols_and_rows(
        self, check_cols: set[int], check_rows: set[int]
    ) -> tuple[set[int], set[int]]:
        """Filters the input cols and rows to only include those which can be unplaced."""
        valid_cols = check_cols & self.point_cols
        valid_rows = check_rows & self.point_rows
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
        new_algo = ParamUnplacement(temp)
        return new_algo.param_unplace(new_algo.find_cols_and_rows()[0], set())
