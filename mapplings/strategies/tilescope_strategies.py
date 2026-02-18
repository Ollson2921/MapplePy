"""Strategies for mapplings tilescope."""

from typing import Iterator
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.point_placements import DIRECTIONS
from tilescope.strategies import (
    FactorStrategy,
    ShuffleFactorStrategy,
    RequirementPlacementStrategy,
    LessThanRowColSeparationStrategy,
    LessThanOrEqualRowColSeparationStrategy,
    CellInsertionFactory,
    PointPlacementFactory,
    RowInsertionFactory,
    ColInsertionFactory,
    RequirementInsertionStrategy,
)

from tilescope.strategies.point_placements import (
    DIR_LEFT_BOT,
    DIR_RIGHT_BOT,
    DIR_LEFT_TOP,
    DIR_RIGHT_TOP,
    DIR_LEFT,
    DIR_RIGHT,
)
from comb_spec_searcher import (
    DisjointUnionStrategy,
    CombinatorialSpecificationSearcher,
)
from comb_spec_searcher.exception import StrategyDoesNotApply
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling
from mapplings.algorithms import (
    MTRequirementPlacement,
    Factor,
    ILFactorNormal,
    ILFactorInverted,
    LTORERowColSeparationMT,
    LTRowColSeparationMT,
)
from mapplings.cleaners import MTCleaner, ParamCleaner

temp = CombinatorialSpecificationSearcher.status


def new_status(self, elaborate: bool) -> str:
    """Overwrites CSS status method"""
    output = (
        temp(self, elaborate) + MTCleaner.status_update() + ParamCleaner.status_update()
    )
    return output


CombinatorialSpecificationSearcher.status = new_status  # type: ignore


class MapplingRequirementPlacementStrategy(RequirementPlacementStrategy):
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


class MapplingRequirementInsertionStrategy(RequirementInsertionStrategy):
    """Mappling version of RequirementInsertionStrategy with a cleaner"""

    cleaner = MTCleaner.make_full_cleaner("Req Insertion Cleaner")

    def decomposition_function(self, comb_class):
        return tuple(
            map(self.__class__.cleaner, super().decomposition_function(comb_class))
        )


class MapplingCellInsertionFactory(CellInsertionFactory):
    """Factory for inserting points into active cells of a tiling."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementInsertionStrategy]:
        for cell in comb_class.active_cells:
            gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
            strategy = MapplingRequirementInsertionStrategy(gcps, ignore_parent=False)
            yield strategy


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


class CleaningStrategy(DisjointUnionStrategy[MappedTiling, GriddedCayleyPerm]):
    """
    A strategy for cleaning a mapped tiling.
    """

    cleaner = MTCleaner.make_full_cleaner("Cleaner Strategy")

    def __init__(
        self,
        ignore_parent: bool = True,
        inferrable: bool = True,
        possibly_empty: bool = True,
        workable: bool = True,
    ):

        super().__init__(
            ignore_parent=ignore_parent,
            inferrable=inferrable,
            possibly_empty=possibly_empty,
            workable=workable,
        )

    def decomposition_function(self, comb_class):
        return (self.__class__.cleaner(comb_class),)

    def formal_step(self) -> str:
        return "Clean mappling"

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def forward_map(self, comb_class, obj, children=None):
        raise NotImplementedError

    def backward_map(self, comb_class, objs, children=None):
        raise NotImplementedError


class MapplingFactorStrategy(FactorStrategy):
    """
    A strategy for finding factors in a mapped tiling.
    """

    cleaner = MTCleaner([], "Factoring Cleaner")

    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = Factor(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        factors = tuple(map(self.__class__.cleaner, factors))
        return factors


# pylint:disable=too-many-ancestors
class MapplingILFactorStrategy(ShuffleFactorStrategy):
    """
    A strategy for finding interleaving factors in a mapped tiling.
    """

    cleaner = MTCleaner.make_full_cleaner("IL Factoring Cleaner")

    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = ILFactorNormal(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        factors = tuple(map(self.__class__.cleaner, factors))
        return factors

    def formal_step(self) -> str:
        return "Factor the mappling into interleaving factors"


class MapplingInvertedILFactorStrategy(ShuffleFactorStrategy):
    """
    A strategy for finding interleaving factors in a mapped tiling by inverting 00 obstructions
    """

    cleaner = MTCleaner.make_full_cleaner("Inverted IL Factoring Cleaner")

    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = ILFactorInverted(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        factors = tuple(map(self.__class__.cleaner, factors))
        return factors

    def formal_step(self) -> str:
        return "Invert obstructions and factor the mappling into interleaving factors"


class MapplingLessThanRowColSeparationStrategy(LessThanRowColSeparationStrategy):
    """A strategy for separating rows and columns with less than constraints."""

    cleaner = MTCleaner.make_full_cleaner("LT Separation Cleaner")

    def decomposition_function(self, comb_class):
        algo = LTRowColSeparationMT(comb_class)
        if algo.separation.row_col_map.is_identity():
            raise StrategyDoesNotApply
        return tuple(map(self.__class__.cleaner, algo.separate()))


class MapplingLessThanOrEqualRowColSeparationStrategy(
    LessThanOrEqualRowColSeparationStrategy
):
    """A strategy for separating rows and columns with less than or equal constraints."""

    cleaner = MTCleaner.make_full_cleaner("LEQ Separation Cleaner")

    def decomposition_function(self, comb_class):
        algo = LTORERowColSeparationMT(comb_class)
        if algo.separation.row_col_map.is_identity():
            raise StrategyDoesNotApply
        return tuple(map(self.__class__.cleaner, algo.separate()))
