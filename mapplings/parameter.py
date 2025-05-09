"""Module with the parameter class."""

from row_col_map import RowColMap
from cleaning_keys import *

from typing import Iterator, Tuple, Set, Iterable
from itertools import product

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm

Cell = Tuple[int, int]


class Parameter:
    """A tiling (called a ghost) mapping to a base tiling."""

    def __init__(self, ghost: Tiling, row_col_map: RowColMap):
        self.map = row_col_map
        self.row_map = row_col_map.row_map
        self.col_map = row_col_map.col_map
        self.ghost = ghost
        self.obstructions = ghost.obstructions
        self.requirements = ghost.requirements
        self.dimensions = ghost.dimensions
        self.cleaner = ParamCleaner()

    def image_rows_and_cols(self) -> Tuple[Set[int], Set[int]]:
        """Gives the indices for the rows and cols to which the parameter maps"""
        return set(self.col_map.values()), set(self.row_map.values())

    def image_cells(self) -> Set[Cell]:
        """Gives the cells to which the parameter maps"""
        return set(product(*self.image_rows_and_cols()))

    def preimage_of_gcp(self, gcperm: GriddedCayleyPerm) -> Iterator[GriddedCayleyPerm]:
        """Returns the preimage of a gridded cayley permutation"""
        for gcp in self.map.preimage_of_gridded_cperm(gcperm):
            if self.ghost.gcp_in_tiling(gcp):
                yield gcp

    def gcp_has_preimage(self, gcp: GriddedCayleyPerm) -> bool:
        """Determines if the sub-gridding of the gcp that lives in the image region has a preimage on the ghost"""
        sub_gridding = gcp.sub_gridded_cayley_perm(self.image_cells())
        for preimage in self.map.preimage_of_gridded_cperm(sub_gridding):
            if self.ghost.gcp_in_tiling(sub_gridding):
                return True
        return False

    def backmap_obstrucctions(
        self, obstructions=Iterable[GriddedCayleyPerm]
    ) -> "Parameter":
        """Places the obstructions on the tiling"""
        new_ghost = self.ghost.add_obstructions(obstructions)
        return Parameter(new_ghost, self.map)

    def backmap_all_from_tiling(self, tiling: Tiling) -> "Parameter":
        """Places all obs and reqs of tiling into the parameter according to the row/col map."""
        new_obs = self.ghost.obstructions + self.map.preimage_of_obstructions(
            tiling.obstructions
        )
        new_reqs = self.ghost.requirements + self.map.preimage_of_requirements(
            tiling.requirements
        )
        return Parameter(Tiling(new_obs, new_reqs, self.ghost.dimensions), self.map)

    def back_map_point_obstructions_from_tiling(self, tiling: Tiling) -> "Parameter":
        """Places all point obstructions in the parameter"""
        new_obs = self.ghost.obstructions + self.map.preimage_of_obstructions(
            [ob for ob in tiling.obstructions if len(ob) == 1]
        )
        return Parameter(
            Tiling(new_obs, self.ghost.requirements, self.ghost.dimensions),
            self.map,
        )

    def delete_rows_and_columns(
        self, cols_to_delete: tuple[int, ...], rows_to_delete: tuple[int, ...]
    ) -> "Parameter":
        """Removes rows and columns from the parameter.
        Adjusts row/col map keys while preserving values."""
        new_ghost = self.ghost.delete_rows_and_columns(cols_to_delete, rows_to_delete)
        image_cols = sorted(
            (
                self.col_map[key]
                for key in self.col_map.keys()
                if key not in cols_to_delete
            )
        )
        image_rows = sorted(
            (
                self.row_map[key]
                for key in self.row_map.keys()
                if key not in rows_to_delete
            )
        )
        new_col_map = dict(enumerate(image_cols))
        new_row_map = dict(enumerate(image_rows))
        return Parameter(new_ghost, RowColMap(new_col_map, new_row_map))

    def delete_preimage_of_rows_and_columns(
        self,
        image_cols_to_delete: tuple[int, ...],
        image_rows_to_delete: tuple[int, ...],
    ) -> "Parameter":
        """Removes rows and columns from the parameter.
        Adjusts row/col map keys and values."""
        preimage_cols = self.map.preimages_of_cols(image_cols_to_delete)
        preimage_rows = self.map.preimages_of_cols(image_rows_to_delete)
        temp_param = self.delete_rows_and_columns(preimage_cols, preimage_rows)
        new_map = temp_param.map.standardise_map()
        return ParamCleaner(temp_param.ghost, new_map)

    def is_contradictory(self, tiling: Tiling) -> bool:
        """Returns True if the parameter is contradictory.
        Is contradictory if any of the requirements in the ghost map to a gcp
        containing an obstruction in the tiling
        """
        raise NotImplementedError

    def clean_desired(self) -> "Parameter":
        """Cleans the parameter according to the todo list"""
        return self.cleaner(self)

    def full_cleanup(self) -> "Parameter":
        """Applies all cleaning functions to the parameter"""
        return ParamCleaner.full_cleanup(self)

    # dunder methods

    @classmethod
    def from_dict(cls, d: dict) -> "Parameter":
        """Used for constructing Parameters from a dictionary."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"({repr(self.ghost)}, {repr(self.map)})"

    def __eq__(self, other: "Parameter") -> bool:
        return self.ghost == other.ghost and self.map == other.map

    def __hash__(self) -> int:
        return hash((self.ghost, self.map))

    def __leq__(self, other: "Parameter") -> int:
        return self.ghost <= other.ghost

    def __lt__(self, other: "Parameter") -> bool:
        return self.ghost < other.ghost

    def __str__(self) -> str:
        return str(self.map) + "\n" + str(self.ghost)


class ParamCleaner:
    def __init__(self, todo_list: Iterable[int] = set()):
        self.todo_list = set(todo_list)

    def __call__(self, param: Parameter) -> Parameter:
        """Cleans the input param according to the cleaner's todo_list"""
        return ParamCleaner.list_cleanup(param, self.todo_list)

    def __add__(self, other: Iterable[int]):
        return ParamCleaner(self.todo_list | set(other))

    @staticmethod
    def list_cleanup(param: Parameter, cleaning_list: Iterable[int]) -> Parameter:
        """Applies all functions indicated by keys in cleaning_list"""
        cleaning_list = tuple(sorted(cleaning_list))
        new_param = param
        for i in cleaning_list:
            new_param = param_cleaning_function_map[i](new_param)
        return new_param

    def tracked_cleanup(
        self, param: Parameter, cleaning_list: Iterable[int]
    ) -> Parameter:
        """Cleans param according to the cleaning list, and removes any completed cleaning functions from the cleaner's todo_list"""
        new_param = ParamCleaner.list_cleanup(param, cleaning_list)
        new_param.cleaner = ParamCleaner(self.todo_list - set(cleaning_list))
        return new_param

    @staticmethod
    def full_cleanup(param: Parameter) -> Parameter:
        """Applies all cleanup functions."""
        return ParamCleaner.list_cleanup(
            param, tuple(param_cleaning_function_map.keys())
        )

    # Final Methods

    @staticmethod
    def reduce_by_fusion(param: Parameter) -> Parameter:
        """Fuses valid rows and columns"""
        rows_to_delete = tuple(
            row
            for row in range(param.dimensions[1] - 1)
            if (
                param.row_map[row] == param.row_map[row + 1]
                and param.ghost.can_fuse_row(row)
            )
        )
        cols_to_delete = tuple(
            col
            for col in range(param.dimensions[0] - 1)
            if (
                param.col_map[col] == param.col_map[col + 1]
                and param.ghost.can_fuse_col(col)
            )
        )
        return param.delete_rows_and_columns(cols_to_delete, rows_to_delete)

    @staticmethod
    def reduce_empty_rows_and_cols(param: Parameter) -> Parameter:
        """Removes empty rows and columns in the parameter"""
        empty_cols, empty_rows = param.ghost.find_empty_rows_and_columns()
        cols_to_remove, rows_to_remove = set(empty_cols), set(empty_rows)
        col_preimages, row_preimages = param.map.preimage_map()
        for key in col_preimages.keys():
            intersection = set(col_preimages[key]) & cols_to_remove
            if len(intersection) == len(col_preimages[key]):
                intersection.remove(col_preimages[key[0]])
                cols_to_remove = cols_to_remove - intersection
        for key in row_preimages.keys():
            intersection = set(row_preimages[key]) & rows_to_remove
            if len(intersection) == len(row_preimages[key]):
                intersection.remove(row_preimages[key[0]])
                rows_to_remove = rows_to_remove - intersection
        return param.delete_rows_and_columns(cols_to_remove, rows_to_remove)

    @staticmethod
    def remove_blank_rows_and_cols(param: Parameter) -> Parameter:
        """Deletes all rows and cols which have no obs or reqs"""
        raise NotImplementedError

    @staticmethod
    def unplace_points(param: Parameter) -> Parameter:
        """Unplaces points wherever possible"""
        raise NotImplementedError


param_cleaning_function_map = {
    pc_fusion: ParamCleaner.reduce_by_fusion,
    pc_reduce_empty: ParamCleaner.reduce_empty_rows_and_cols,
    pc_remove_blank: ParamCleaner.remove_blank_rows_and_cols,
    pc_unplace_points: ParamCleaner.unplace_points,
}
