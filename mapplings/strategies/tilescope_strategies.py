from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from tilescope.strategies import (
    FactorStrategy,
    RequirementPlacementStrategy,
    LessThanRowColSeparationStrategy,
    LessThanOrEqualRowColSeparationStrategy,
    CellInsertionFactory,
    PointPlacementFactory,
)
from mapplings.algorithms import (
    MTRequirementPlacement,
    Factor,
    LTORERowColSeparationMT,
    LTRowColSeparationMT,
)
from comb_spec_searcher import StrategyPack, DisjointUnionStrategy
from comb_spec_searcher.exception import StrategyDoesNotApply
from gridded_cayley_permutations.point_placements import Directions
from typing import Iterator
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling
from mapplings.cleaners import MTCleaner
from comb_spec_searcher import AtomStrategy
from .verification_strategy import NoParameterVerificationStrategy


class MapplingRequirementPlacementStrategy(RequirementPlacementStrategy):
    def algorithm(self, mappling):
        return MTRequirementPlacement(mappling)


class MapplingPointPlacementFactory(PointPlacementFactory):
    def __call__(self, comb_class: Tiling) -> Iterator[RequirementPlacementStrategy]:
        for cell in comb_class.positive_cells():
            for direction in Directions:
                gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
                indices = (0,)
                yield MapplingRequirementPlacementStrategy(gcps, indices, direction)
                # if direction in PartialRequirementPlacementStrategy.DIRECTIONS:
                #     yield PartialRequirementPlacementStrategy(gcps, indices, direction)


class CleaningStrategy(DisjointUnionStrategy[MappedTiling, GriddedCayleyPerm]):
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

    def forward_map(self, comb_class, obj, children=None):
        return super().forward_map(comb_class, obj, children)

    def backward_map(self, comb_class, objs, children=None):
        return super().backward_map(comb_class, objs, children)

    @classmethod
    def from_dict(cls, d):
        raise NotImplementedError


class MapplingFactorStrategy(FactorStrategy):
    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = Factor(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        return factors


class MapplingLessThanRowColSeparationStrategy(LessThanRowColSeparationStrategy):
    def decomposition_function(self, comb_class):
        algo = LTRowColSeparationMT(comb_class)
        return (next(algo.separate()),)


class MapplingLessThanOrEqualRowColSeparationStrategy(
    LessThanOrEqualRowColSeparationStrategy
):
    def decomposition_function(self, comb_class):
        algo = LTORERowColSeparationMT(comb_class)
        return tuple(algo.separate())


# PointPlacementsPack = StrategyPack(
#     initial_strats=[
#         MapplingFactorStrategy(),
#         MapplingLessThanOrEqualRowColSeparationStrategy(),
#         MapplingPointPlacementFactory(),
#     ],
#     inferral_strats=[CleaningStrategy(), MapplingLessThanRowColSeparationStrategy()],
#     expansion_strats=[[CellInsertionFactory()]],
#     ver_strats=[AtomStrategy()],
#     name="Point placements",
# )


class MappedTileScopePack(StrategyPack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def MTpoint_placement(cls, rootmt):
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
