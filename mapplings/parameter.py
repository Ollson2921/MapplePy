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

    def __eq__(self, other) -> bool:
        return self.ghost == other.ghost and self.map == other.map

    def __hash__(self) -> int:
        return hash((self.ghost, self.map))

    def __leq__(self, other) -> int:
        return self.ghost <= other.ghost

    def __lt__(self, other) -> bool:
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

    @staticmethod
    def method_name0(param: Parameter) -> Parameter:
        """An example cleaning function"""
        return param

    @staticmethod
    def method_name1(param: Parameter) -> Parameter:
        """An example cleaning function"""
        return param


param_cleaning_function_map = {
    pc_method_nickname0: ParamCleaner.method_name0,
    pc_method_nickname1: ParamCleaner.method_name1,
}
