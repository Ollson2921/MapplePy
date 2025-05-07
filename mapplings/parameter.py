"""Module with the parameter class."""

from typing import Iterator
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap


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

    def image_region(self):
        pass

    def clean_desired(self):
        return self.cleaner.clean_desired()

    def full_cleanup(self):
        return self.cleaner.full_cleanup()

    def preimage_of_gcp(self, gcperm: GriddedCayleyPerm) -> Iterator[GriddedCayleyPerm]:
        """Returns the preimage of a gridded cayley permutation"""
        for gcp in self.map.preimage_of_gridded_cperm(gcperm):
            if self.ghost.gcp_in_tiling(gcp):
                yield gcp

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
        """Applies cleaning functions for each true variable"""
        return self.param

    def full_cleanup(self) -> Parameter:
        """Applies all cleanup functions"""
        return self.param
