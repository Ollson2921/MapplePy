"""This module contains a type of RowColMap which is not surjective
so that not everything is mapped onto.

This is used for parameters mapping onto a part of the base tiling
rather than the whole tiling."""

from gridded_cayley_permutations.row_col_map import (
    RowColMap as RCMap,
    GriddedCayleyPerm,
)

from typing import Iterable, Iterator, Tuple


OBSTRUCTIONS = Tuple[GriddedCayleyPerm, ...]
REQUIREMENTS = Tuple[Tuple[GriddedCayleyPerm, ...], ...]


class RowColMap(RCMap):
    """
    The pre-image of any value is an interval.
    If a > b then every pre-image of a is to the greater than every pre-image of b.

    Not every value has a preimage.
    """

    def __init__(self, col_map, row_map):
        super().__init__(col_map, row_map)

    def preimage_of_gridded_cperm(
        self, gcp: GriddedCayleyPerm
    ) -> Iterator[GriddedCayleyPerm]:
        """
        Return the preimages of a gridded Cayley permutation with respect to the map.
        TODO: Not all gcps will have a preimage, check that here?
        """
        super().preimage_of_gridded_cperm(gcp)

    def restriction(
        self, col_values: Iterable[int], row_values: Iterable[int]
    ) -> "RowColMap":
        """
        The restriction of the row col map to only the col_values
        and the row_values of the preimage.
        TODO: I don't think I understand what this does or where it is used
        but it looks good?
        """
        new_col_map, new_row_map = {}, {}
        for index in col_values:
            new_col_map[index] = self.col_map[index]
        for index in row_values:
            new_row_map[index] = self.row_map[index]
        return RowColMap(new_col_map, new_row_map)

    def standardise_map(self) -> "RowColMap":
        """
        Return the row col map with the keys and the values
        both standardised to the integers 0 to n.
        """
        raise NotImplementedError(
            "Standardise map not implemented for RowColMap. \nUse standardise_map "
            "in the base class instead. \n(I don't think we want to use it now?)"
        )
