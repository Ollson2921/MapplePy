from functools import cached_property
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
from comb_spec_searcher import StrategyPack, DisjointUnionStrategy, StrategyFactory
from comb_spec_searcher.exception import StrategyDoesNotApply
from gridded_cayley_permutations.point_placements import Directions
from typing import Iterator, Iterable
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, MTCleaner
from comb_spec_searcher import AtomStrategy


class MapplingRequirementPlacementStrategy(RequirementPlacementStrategy):
    def algorithm(self, mappling: MappedTiling):
        return MTRequirementPlacement(mappling)


class MapplingPointPlacementFactory(StrategyFactory[MappedTiling]):

    def algorithm(self, mappling: MappedTiling):
        return MTRequirementPlacement(mappling)

    def __call__(self, comb_class: MappedTiling) -> Iterator[DisjointUnionStrategy]:
        algo = self.algorithm(comb_class)
        for cell in comb_class.positive_cells():
            gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
            indices = (0,)
            for direction in Directions:
                children = (comb_class.add_obstructions(gcps),) + algo.point_placement(
                    gcps, indices, direction
                )
                yield MapplingRequirementPlacementStrategy(
                    gcps, indices, direction, cell
                )(comb_class, children)
                # if direction in PartialRequirementPlacementStrategy.DIRECTIONS:
                #     yield PartialRequirementPlacementStrategy(gcps, indices, direction)

    @classmethod
    def from_dict(cls, d: dict) -> "MapplingPointPlacementFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Point placement"


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
        return "cleaned"

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


PointPlacementsPack = StrategyPack(
    initial_strats=[
        MapplingFactorStrategy(),
        MapplingLessThanOrEqualRowColSeparationStrategy(),
        MapplingPointPlacementFactory(),
    ],
    inferral_strats=[CleaningStrategy(), MapplingLessThanRowColSeparationStrategy()],
    expansion_strats=[[CellInsertionFactory()]],
    ver_strats=[AtomStrategy()],
    name="Point placements",
)
