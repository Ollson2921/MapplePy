"""Strategies and pack for mapplings tilescope."""

from typing import Iterator
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.point_placements import Directions
from tilescope.strategies import (
    FactorStrategy,
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
from comb_spec_searcher import StrategyPack, DisjointUnionStrategy, AtomStrategy
from comb_spec_searcher.exception import StrategyDoesNotApply
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling
from mapplings.algorithms import (
    MTRequirementPlacement,
    Factor,
    LTORERowColSeparationMT,
    LTRowColSeparationMT,
)
from mapplings.cleaners import MTCleaner
from .verification_strategy import NoParameterVerificationStrategy


class MapplingRequirementPlacementStrategy(RequirementPlacementStrategy):
    """
    A strategy for placing requirements in a mapped tiling.
    """

    def algorithm(self, tiling):
        return MTRequirementPlacement(tiling)


class MapplingPointPlacementFactory(PointPlacementFactory):
    """
    A factory for creating point placement strategies for mapped tilings.
    """

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementPlacementStrategy]:
        for cell in comb_class.positive_cells():
            for direction in Directions:
                gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
                indices = (0,)
                yield MapplingRequirementPlacementStrategy(gcps, indices, direction)
                # if direction in PartialRequirementPlacementStrategy.DIRECTIONS:
                #     yield PartialRequirementPlacementStrategy(gcps, indices, direction)


class MapplingRowPlacementFactory(RowInsertionFactory):
    """A factory for placing the minimum points in the rows of tilings."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
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
    CellInsertionFactory
):
    """A factory for making columns positive in mapplings for vertical insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        for col in range(comb_class.dimensions[0]):
            if not comb_class.col_is_positive(col):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_col(col)
                )
                yield RequirementInsertionStrategy(gcps, ignore_parent=True)
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

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
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
    CellInsertionFactory
):
    """A factory for making rows positive in mapplings for horizontal insertion encoding."""

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementInsertionStrategy]:
        for row in range(comb_class.dimensions[1]):
            if not comb_class.row_is_positive(row):
                gcps = tuple(
                    GriddedCayleyPerm(CayleyPermutation([0]), [cell])
                    for cell in comb_class.cells_in_row(row)
                )
                yield RequirementInsertionStrategy(gcps, ignore_parent=True)

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
        return (MTCleaner.full_cleanup(comb_class),)

    def formal_step(self) -> str:
        return "Clean mappling"

    @classmethod
    def from_dict(cls, d):
        raise NotImplementedError

    def forward_map(self, comb_class, obj, children=None):
        raise NotImplementedError

    def backward_map(self, comb_class, objs, children=None):
        raise NotImplementedError


class MapplingFactorStrategy(FactorStrategy):
    """
    A strategy for finding factors in a mapped tiling.
    """

    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = Factor(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        return factors


class MapplingLessThanRowColSeparationStrategy(LessThanRowColSeparationStrategy):
    """A strategy for separating rows and columns with less than constraints."""

    def decomposition_function(self, comb_class):
        algo = LTRowColSeparationMT(comb_class)
        return (next(algo.separate()),)


class MapplingLessThanOrEqualRowColSeparationStrategy(
    LessThanOrEqualRowColSeparationStrategy
):
    """A strategy for separating rows and columns with less than or equal constraints."""

    def decomposition_function(self, comb_class):
        algo = LTORERowColSeparationMT(comb_class)
        return tuple(algo.separate())


class MappedTileScopePack(StrategyPack):
    """A strategy pack for mapplings tilescope."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def point_placement(cls, rootmt):
        """
        Create a point placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
                MapplingPointPlacementFactory(),
            ],
            inferral_strats=[
                CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    CellInsertionFactory(),
                ]
            ],
            ver_strats=[AtomStrategy(), NoParameterVerificationStrategy(rootmt)],
            name="Point placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_placement(cls, rootmt):
        """
        Create a row placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
            ],
            inferral_strats=[
                CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    MapplingRowPlacementFactory(),
                ]
            ],
            ver_strats=[AtomStrategy(), NoParameterVerificationStrategy(rootmt)],
            name="Row placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def col_placement(cls, rootmt):
        """
        Create a column placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
            ],
            inferral_strats=[
                CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    MapplingColPlacementFactory(),
                ]
            ],
            ver_strats=[AtomStrategy(), NoParameterVerificationStrategy(rootmt)],
            name="Column placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def row_and_col_placement(cls, rootmt):
        """
        Create a row and column placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
            ],
            inferral_strats=[
                CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    MapplingRowPlacementFactory(),
                    MapplingColPlacementFactory(),
                ]
            ],
            ver_strats=[AtomStrategy(), NoParameterVerificationStrategy(rootmt)],
            name="Point placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def point_row_and_col_placement(cls, rootmt):
        """
        Create a point, row and column placement strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingLessThanOrEqualRowColSeparationStrategy(),
                MapplingPointPlacementFactory(),
            ],
            inferral_strats=[
                CleaningStrategy(),
                MapplingLessThanRowColSeparationStrategy(),
            ],
            expansion_strats=[
                [
                    CellInsertionFactory(),
                    MapplingRowPlacementFactory(),
                    MapplingColPlacementFactory(),
                ]
            ],
            ver_strats=[AtomStrategy(), NoParameterVerificationStrategy(rootmt)],
            name="Point placements",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def vertical_insertion_encoding(cls):
        """
        Create a vertical insertion encoding strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingVerticalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[CleaningStrategy()],
            expansion_strats=[[MapplingVerticalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="Vertical Insertion Encoding",
            symmetries=[],
            iterative=False,
        )

    @classmethod
    def horizontal_insertion_encoding(cls):
        """
        Create a horizontal insertion encoding strategy pack for the given root mapped tiling.
        """
        return MappedTileScopePack(
            initial_strats=[
                MapplingFactorStrategy(),
                MapplingHorizontalInsertionEncodingRequirementInsertionFactory(),
            ],
            inferral_strats=[CleaningStrategy()],
            expansion_strats=[[MapplingHorizontalInsertionEncodingPlacementFactory()]],
            ver_strats=[AtomStrategy()],
            name="Horizontal Insertion Encoding",
            symmetries=[],
            iterative=False,
        )
