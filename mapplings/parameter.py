"""Module with the parameter class."""

from typing import Iterator, Tuple, Set
from itertools import product

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from .row_col_map import RowColMap

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
        self.cleaner = ParamCleaner(self)

    def clean_desired(self) -> "Parameter":
        """Cleans the parameter according to specified cleaning bools"""
        return self.cleaner.clean_desired()

    def full_cleanup(self) -> "Parameter":
        """Applies all cleaning functions to the parameter"""
        return self.cleaner.full_cleanup()

    def preimage_of_gcp(self, gcperm: GriddedCayleyPerm) -> Iterator[GriddedCayleyPerm]:
        """Returns the preimage of a gridded cayley permutation"""
        for gcp in self.map.preimage_of_gridded_cperm(gcperm):
            if self.ghost.gcp_in_tiling(gcp):
                yield gcp

    def gcp_has_preimage(self, gcp: GriddedCayleyPerm) -> bool:
        sub_gridding = gcp.sub_gridded_cayley_perm(self.map.image_cells())
        for preimage in self.map.preimage_of_gridded_cperm(sub_gridding):
            if self.ghost.gcp_in_tiling(sub_gridding):
                return True
        return False

    # dunder methods

    @classmethod
    def from_dict(cls, d: dict) -> "Parameter":
        """Used for constructing MappedTilings from a dictionary."""
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
    def __init__(self, param: Parameter):
        self.param = param
        self.cleaning_bool_name = False  # this is what a to do list item will look like

    def clean_desired(self) -> Parameter:
        """Applies cleaning functions for each true cleaning bool"""
        return self.param

    def full_cleanup(self) -> Parameter:
        """Applies all cleanup functions"""
        return self.param
