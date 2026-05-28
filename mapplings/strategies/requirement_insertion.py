"""Requirement insertion strategies for mapplings."""

from typing import Iterator
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from tilescope.strategies import (
    CellInsertionFactory,
    RequirementInsertionStrategy,
)
from cayley_permutations import CayleyPermutation
from mapplings.cleaners import MTCleaner
from mapplings.strategies.extra_parameters import ExtraParametersForStrategies
from mapplings import MappedTiling, ParameterList


class MapplingRequirementInsertionStrategy(
    ExtraParametersForStrategies, RequirementInsertionStrategy
):
    """Mappling version of RequirementInsertionStrategy with a cleaner"""

    cleaner = MTCleaner.make_full_cleaner("Req Insertion Cleaner")

    def decomposition_function(self, comb_class):
        return tuple(
            map(self.__class__.cleaner, super().decomposition_function(comb_class))
        )

    def update_enumerator_list(
        self, comb_class: MappedTiling, enumerator_list: ParameterList
    ) -> tuple[ParameterList, ...]:
        return (enumerator_list,) * len(self.decomposition_function(comb_class))


class MapplingCellInsertionFactory(CellInsertionFactory):
    """Factory for inserting points into active cells of a tiling."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementInsertionStrategy]:
        for cell in comb_class.active_cells:
            gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
            strategy = MapplingRequirementInsertionStrategy(gcps, ignore_parent=False)
            yield strategy


class MapplingVerticalInsertionEncodingRequirementInsertionFactory(
    MapplingCellInsertionFactory
):
    """A factory for making columns positive in mapplings for vertical insertion encoding."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementInsertionStrategy]:
        for col in range(comb_class.dimensions[0]):
            if not comb_class.col_is_positive(col):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_col(col)
                )
                yield MapplingRequirementInsertionStrategy(gcps, ignore_parent=True)
                return

    @classmethod
    def from_dict(
        cls, d: dict
    ) -> "MapplingVerticalInsertionEncodingRequirementInsertionFactory":
        return cls(**d)

    def __str__(self) -> str:
        return "Make columns positive"


class MapplingHorizontalInsertionEncodingRequirementInsertionFactory(
    MapplingCellInsertionFactory
):
    """A factory for making rows positive in mapplings for horizontal insertion encoding."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementInsertionStrategy]:
        for row in range(comb_class.dimensions[1]):
            if not comb_class.row_is_positive(row):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_row(row)
                )
                yield MapplingRequirementInsertionStrategy(gcps, ignore_parent=True)

    @classmethod
    def from_dict(
        cls, d: dict
    ) -> "MapplingHorizontalInsertionEncodingRequirementInsertionFactory":
        return cls(**d)

    def __str__(self) -> str:
        return "Make rows positive"
