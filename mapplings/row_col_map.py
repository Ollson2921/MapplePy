"""This module contains a type of RowColMap which is not surjective
so that not everything is mapped onto.

This is used for parameters mapping onto a part of the base tiling
rather than the whole tiling."""

from gridded_cayley_permutations.row_col_map import (
    RowColMap as RCMap,
    GriddedCayleyPerm,
)

from typing import Iterator, Tuple
from itertools import product


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

        TODO: Is this what we want it to do?
        """
        for cols, rows in product(
            self._product_of_cols(gcp), self._product_of_rows(gcp)
        ):
            new_positions = tuple(zip(cols, rows))
            print(new_positions)
            yield GriddedCayleyPerm(gcp.pattern, new_positions)

    def standardise_map(self) -> "RowColMap":
        """
        Return the row col map with the keys and the values
        both standardised to the integers 0 to n.
        """
        raise NotImplementedError(
            "Standardise map not implemented for RowColMap. \nUse standardise_map "
            "in the base class instead. \n(I don't think we want to use it now?)"
        )
