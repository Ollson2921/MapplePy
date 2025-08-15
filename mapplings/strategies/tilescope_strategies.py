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
    def algorithm(self, mappling):
        return MTRequirementPlacement(mappling)


class MapplingPointPlacementFactory(StrategyFactory[MappedTiling]):
    def __call__(self, comb_class: MappedTiling) -> Iterator[DisjointUnionStrategy]:
        for cell in comb_class.positive_cells():
            gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
            indices = (0,)
            directionless_placement = MTRequirementPlacement(
                comb_class
            ).directionless_point_placement_in_cell(cell)
            for direction in Directions:
                yield PointPlacementFactoryStrategy(
                    directionless_placement, gcps, indices, direction, cell
                )
                # if direction in PartialRequirementPlacementStrategy.DIRECTIONS:
                #     yield PartialRequirementPlacementStrategy(gcps, indices, direction)

    @classmethod
    def from_dict(cls, d: dict) -> "MapplingPointPlacementFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Point placement"


class PointPlacementFactoryStrategy(
    DisjointUnionStrategy[MappedTiling, GriddedCayleyPerm]
):
    def __init__(
        self,
        directionless_placement: MappedTiling,
        gcps: Iterable[GriddedCayleyPerm],
        indices: Iterable[int],
        direction: int,
        cell: tuple[int, int],
        ignore_parent: bool = False,
        possibly_empty: bool = True,
    ):
        self.directionless_placement = directionless_placement
        self.gcps = tuple(gcps)
        self.indices = tuple(indices)
        self.direction = direction
        self.cell = cell
        super().__init__(ignore_parent=ignore_parent, possibly_empty=possibly_empty)

    def algorithm(self, mappling: MappedTiling):
        return MTRequirementPlacement(mappling)

    def decomposition_function(self, comb_class):
        return (comb_class.add_obstructions(self.gcps),) + (
            self.algorithm(comb_class).force_direction(
                self.directionless_placement,
                self.gcps,
                self.indices,
                self.direction,
                self.cell,
            ),
        )

    def formal_step(self) -> str:
        return (
            f"Placed the point of the requirement {self.gcps} "
            + f"at indices {self.indices} in direction {self.direction}"
        )

    def forward_map(self, comb_class, obj, children=None):
        return super().forward_map(comb_class, obj, children)

    def backward_map(self, comb_class, objs, children=None):
        return super().backward_map(comb_class, objs, children)

    @classmethod
    def from_dict(cls, d):
        raise NotImplementedError


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
