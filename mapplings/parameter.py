"""Module with the parameter class."""

from typing import Iterator
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap


class Parameter:
    """A tiling (called a ghost) mapping to a base tiling."""

    def __init__(self, ghost: Tiling, row_col_map: RowColMap):
        self.map = row_col_map
        self.ghost = ghost

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
