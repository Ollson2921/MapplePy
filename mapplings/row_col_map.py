"""This module contains a type of RowColMap which is not surjective
so that not everything is mapped onto.

This is used for parameters mapping onto a part of the base tiling
rather than the whole tiling."""

from typing import Iterator, Tuple
from itertools import product
from functools import cached_property

from gridded_cayley_permutations.row_col_map import (
    RowColMap as RCMap,
    GriddedCayleyPerm,
)


OBSTRUCTIONS = Tuple[GriddedCayleyPerm, ...]
REQUIREMENTS = Tuple[Tuple[GriddedCayleyPerm, ...], ...]
Cell = Tuple[int, int]


class RowColMap(RCMap):
    """
    The pre-image of any value is an interval.
    If a > b then every pre-image of a is to the greater than every pre-image of b.

    Not every value has a preimage.
    """

    def image_rows_and_cols(self) -> Tuple[set[int], set[int]]:
        """Gives the indices for the rows and cols on the base tiling
        to which the parameter maps"""
        return set(self.col_map.values()), set(self.row_map.values())

    @cached_property
    def image_cells(self) -> set[Cell]:
        """Gives the cells on the base tiling to which the parameter maps"""
        return set(product(*self.image_rows_and_cols()))

    def preimage_of_gridded_cperm(
        self, gcp: GriddedCayleyPerm
    ) -> Iterator[GriddedCayleyPerm]:
        """
        Return the preimages of a gridded Cayley permutation with respect to the map.
        Only use this on subgcps that have a preimage fully in the parameter.

        If a gcp is not fully in the image cells of the base tiling then
        new_positions will be cells not in the parameter
        """
        for cols, rows in product(
            self._product_of_cols(gcp), self._product_of_rows(gcp)
        ):
            new_positions = tuple(zip(cols, rows))
            if any(cell not in self.cells_in_parameter for cell in new_positions):
                raise ValueError(
                    f"The gridded Cayley perm {gcp} does not have a preimage in the parameter."
                )
            yield GriddedCayleyPerm(gcp.pattern, new_positions)

    @cached_property
    def cells_in_parameter(self) -> set[Cell]:
        """Returns the cells in the parameter"""
        all_cells = set()
        for col in self.col_map.values():
            for row in self.row_map.values():
                all_cells.add((col, row))
        return all_cells
