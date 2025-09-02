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

    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
        for cell in comb_class.positive_cells():
            for direction in Directions:
                gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
                indices = (0,)
                yield MapplingRequirementPlacementStrategy(gcps, indices, direction)
                # if direction in PartialRequirementPlacementStrategy.DIRECTIONS:
                #     yield PartialRequirementPlacementStrategy(gcps, indices, direction)


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
            expansion_strats=[[CellInsertionFactory()]],
            ver_strats=[AtomStrategy(), NoParameterVerificationStrategy(rootmt)],
            name="Point placements",
            symmetries=[],
            iterative=False,
        )
