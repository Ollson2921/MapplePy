"""Strategy for requirement placement and various placement factories."""

from typing import Iterator
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.point_placements import DIRECTIONS, PointPlacement
from tilescope.strategies import (
    RequirementPlacementStrategy,
    PointPlacementFactory,
    RowInsertionFactory,
    ColInsertionFactory,
)

from tilescope.strategies.point_placements import (
    DIR_LEFT_BOT,
    DIR_RIGHT_BOT,
    DIR_LEFT_TOP,
    DIR_RIGHT_TOP,
    DIR_LEFT,
    DIR_RIGHT,
)
from cayley_permutations import CayleyPermutation
from mapplings.algorithms import (
    MTRequirementPlacement,
)
from mapplings.cleaners import MTCleaner
from mapplings import MappedTiling, ParameterList
from mapplings.strategies.extra_parameters import ExtraParametersForStrategies


class MapplingRequirementPlacementStrategy(
    ExtraParametersForStrategies, RequirementPlacementStrategy
):
    """
    A strategy for placing requirements in a mapped tiling.
    """

    cleaner = MTCleaner.make_full_cleaner("Req Placement Cleaner")

    def algorithm(self, tiling):
        return MTRequirementPlacement(tiling)

    def decomposition_function(self, comb_class):
        return tuple(
            map(self.__class__.cleaner, super().decomposition_function(comb_class))
        )

    def update_enumerator_list(
        self, comb_class: MappedTiling, enumerator_list: ParameterList
    ) -> tuple[ParameterList, ...]:
        """Returns a tuple of the updated parameter lists for each child"""
        children_param_lists = [enumerator_list]
        for cell in self.algorithm(comb_class).cells_to_place_in:
            children_param_lists.append(
                self.algorithm(comb_class).update_param_list(enumerator_list, cell)
            )
        return tuple(children_param_lists)


class MapplingPointPlacementFactory(PointPlacementFactory):
    """
    A factory for creating point placement strategies for mapped tilings.
    """

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementPlacementStrategy]:
        for cell in comb_class.positive_cells():
            for direction in DIRECTIONS:
                gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
                indices = (0,)
                yield MapplingRequirementPlacementStrategy(gcps, indices, direction)
                # if direction in PartialRequirementPlacementStrategy.DIRECTIONS:
                #     yield PartialRequirementPlacementStrategy(gcps, indices, direction)


class MapplingRowPlacementFactory(RowInsertionFactory):
    """A factory for placing the minimum points in the rows of tilings."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementPlacementStrategy]:
        not_point_rows = set(range(comb_class.dimensions[1])) - comb_class.point_rows
        for row in not_point_rows:
            all_gcps = []
            for col in range(comb_class.dimensions[0]):
                cell = (col, row)
                if cell in comb_class.active_cells:
                    gcps = GriddedCayleyPerm(CayleyPermutation([0]), (cell,))
                    all_gcps.append(gcps)
            indices = tuple(0 for _ in all_gcps)
            for direction in [DIR_LEFT_BOT, DIR_RIGHT_BOT, DIR_LEFT_TOP, DIR_RIGHT_TOP]:
                yield MapplingRequirementPlacementStrategy(all_gcps, indices, direction)


class MapplingColPlacementFactory(ColInsertionFactory):
    """A factory for placing the leftmost or rightmost points in
    the columns of tilings."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
        not_point_cols = set(range(comb_class.dimensions[0])) - set(
            cell[0] for cell in comb_class.point_cells()
        )
        for col in not_point_cols:
            all_gcps = []
            for row in range(comb_class.dimensions[1]):
                cell = (col, row)
                gcps = GriddedCayleyPerm(CayleyPermutation([0]), (cell,))
                all_gcps.append(gcps)
            indices = tuple(0 for _ in all_gcps)
            for direction in [DIR_LEFT, DIR_RIGHT]:
                yield MapplingRequirementPlacementStrategy(all_gcps, indices, direction)


class MapplingHorizontalInsertionEncodingPlacementFactory(MapplingColPlacementFactory):
    """A factory for placing the leftmost points in mapplings."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        direction = DIR_LEFT
        yield MapplingRequirementPlacementStrategy(gcps, indices, direction)

    @classmethod
    def from_dict(
        cls, d: dict
    ) -> "MapplingHorizontalInsertionEncodingPlacementFactory":
        return cls(**d)

    def __str__(self) -> str:
        return "Place next point of insertion encoding"


class MapplingVerticalInsertionEncodingPlacementFactory(MapplingRowPlacementFactory):
    """A factory for placing the bottom leftmost points in mapplings."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementPlacementStrategy]:
        cells = comb_class.active_cells
        gcps = tuple(
            GriddedCayleyPerm(CayleyPermutation([0]), [cell]) for cell in cells
        )
        indices = tuple(0 for _ in gcps)
        direction = DIR_LEFT_BOT
        yield MapplingRequirementPlacementStrategy(gcps, indices, direction)

    @classmethod
    def from_dict(cls, d: dict) -> "MapplingVerticalInsertionEncodingPlacementFactory":
        return cls(**d)

    def __str__(self) -> str:
        return "Place next point of insertion encoding"
