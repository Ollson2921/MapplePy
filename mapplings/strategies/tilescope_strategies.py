"""Strategies for mapplings tilescope."""

from typing import Iterator, Optional
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.point_placements import Directions
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
    StrategyFactory,
)
from comb_spec_searcher.exception import StrategyDoesNotApply
from comb_spec_searcher.strategies.constructor import DisjointUnion, Complement
from comb_spec_searcher.strategies.rule import Rule
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, ParameterList
from mapplings.algorithms import (
    MTRequirementPlacement,
    ParameterPlacement,
    Factor,
    ILFactorNormal,
    ILFactorInverted,
    LTORERowColSeparationMT,
    LTRowColSeparationMT,
)
from mapplings.cleaners import MTCleaner, ParamCleaner


MTCleaner.global_debug_toggle(0)
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


class ParameterPlacementStrategy(DisjointUnionStrategy):
    """Strategy for placing parameters"""

    cleaner = MTCleaner.make_full_cleaner("Param Placement Cleaner")

    def __init__(
        self,
        c_list_index: int,
        point_index: int,
        direction: int,
        ignore_parent: bool = False,
    ):
        self.c_list_index = c_list_index
        self.index = point_index
        self.direction = direction
        super().__init__(ignore_parent)

    def algorithm(self, mappling: MappedTiling):
        """Algorithm used by the decomposition function"""
        c_list = mappling.containing_parameters[self.c_list_index]
        return ParameterPlacement(mappling, c_list)

    def decomposition_function(self, comb_class):
        new_mappling = self.algorithm(comb_class).param_placement(
            self.direction, self.index
        )
        return (self.__class__.cleaner(new_mappling),)

    def formal_step(self):
        return (
            f"Placed point {self.index} of containing parameter {self.c_list_index} "
            + f"in direction {self.direction}"
        )

    def backward_map(
        self,
        comb_class: MappedTiling,
        objs: tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[tuple[MappedTiling, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: MappedTiling,
        obj: GriddedCayleyPerm,
        children: Optional[tuple[MappedTiling, ...]] = None,
    ) -> tuple[Optional[GriddedCayleyPerm], ...]:
        raise NotImplementedError

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        d.pop("possibly_empty")
        d["c_list_index"] = self.c_list_index
        d["point_index"] = self.index
        d["direction"] = self.direction
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ParameterPlacementStrategy":
        """Return a strategy from a dictionary."""
        return cls(**d)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            + f"{self.c_list_index}, {self.index}, {self.direction}"
            + f"ignore_parent={self.ignore_parent})"
        )

    def __str__(self):
        return "Placed a parameter"


class ParamPlacementFactory(StrategyFactory[MappedTiling]):
    """Tries to place the points of any size 1 containing parameter list"""

    def __call__(
        self, comb_class: MappedTiling
    ) -> Iterator[ParameterPlacementStrategy]:
        for c_index, c_list in enumerate(comb_class.containing_parameters):
            if len(c_list) != 1:
                continue
            param = tuple(c_list)[0]
            points = tuple(param.point_cells())
            if not points:
                continue
            for i in range(len(points)):
                for direction in Directions:
                    yield ParameterPlacementStrategy(c_index, i, direction)

    @classmethod
    def from_dict(cls, d: dict) -> "ParamPlacementFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Parameter placement"


class ParameterInsertionStrategy(DisjointUnionStrategy):
    """Straregy for inserting parameters"""

    cleaner = MTCleaner.make_full_cleaner("Param Insertion Cleaner")

    def __init__(
        self,
        params: ParameterList,
        ignore_parent=False,
    ):
        self.params = params
        super().__init__(ignore_parent)

    def decomposition_function(self, comb_class: MappedTiling):
        avoiders, containers, enumerators = comb_class.ace_parameters()
        base = comb_class.tiling
        new_avoiders = ParameterList(avoiders | self.params)
        new_containers = list(containers) + [self.params]
        clean = self.__class__.cleaner
        m1 = MappedTiling(base, new_avoiders, containers, enumerators)
        m2 = MappedTiling(base, avoiders, new_containers, enumerators)
        return (clean(m1), clean(m2))

    def formal_step(self):
        return "Contain or avoid parameters"

    def backward_map(
        self,
        comb_class: MappedTiling,
        objs: tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[tuple[MappedTiling, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: MappedTiling,
        obj: GriddedCayleyPerm,
        children: Optional[tuple[MappedTiling, ...]] = None,
    ) -> tuple[Optional[GriddedCayleyPerm], ...]:
        raise NotImplementedError

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        d.pop("possibly_empty")
        d["params"] = self.params
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ParameterInsertionStrategy":
        """Return a strategy from a dictionary."""
        return cls(**d)


class AvoiderExorcismStrategy(ParameterInsertionStrategy):
    """Strategy for transforming Avoiders into Containers"""

    cleaner = MTCleaner.make_full_cleaner("Avoider Exorcism Cleaner")

    def __init__(self, params, ignore_parent=False):
        assert len(params) == 1
        super().__init__(params, ignore_parent)

    def __call__(
        self,
        comb_class: MappedTiling,
        children: Optional[tuple[MappedTiling, MappedTiling]] = None,
    ) -> Rule:
        if children is None:
            children = self.decomposition_function(comb_class)
            if children is None:
                raise StrategyDoesNotApply("Strategy does not apply")
        return Rule(self, children[0], (comb_class, children[1]))

    def decomposition_function(self, comb_class):
        avoider = tuple(self.params)[0]
        avoiders, containers, enumerators = comb_class.ace_parameters()
        assert avoider in avoiders, "Avoider Does Not Exist"
        base = comb_class.tiling
        new_avoiders = list(avoiders)
        new_avoiders.remove(avoider)
        new_containers = list(containers) + [self.params]
        clean = self.__class__.cleaner
        m1 = MappedTiling(base, new_avoiders, containers, enumerators)
        m2 = MappedTiling(base, new_avoiders, new_containers, enumerators)
        return (clean(m1), clean(m2))

    def constructor(
        self,
        comb_class: MappedTiling,
        children: Optional[tuple[MappedTiling, MappedTiling]] = None,
    ) -> DisjointUnion:
        if children is None:
            children = self.decomposition_function(comb_class)
            if children is None:
                raise StrategyDoesNotApply("Strategy does not apply")
        return DisjointUnion(children[0], (comb_class, children[1]))

    def reverse_constructor(
        self,
        idx: int,
        comb_class: MappedTiling,
        children: Optional[tuple[MappedTiling, MappedTiling]] = None,
    ):
        if children is None:
            children = self.decomposition_function(comb_class)
            if children is None:
                raise StrategyDoesNotApply("Strategy does not apply")
        return Complement(children[0], (comb_class, children[1]), idx)


class ContainerExorcismStrategy(AvoiderExorcismStrategy):
    """Strategy for transforming Containers into Avoiders"""

    cleaner = MTCleaner.make_full_cleaner("Container Exorcism Cleaner")

    def decomposition_function(self, comb_class: MappedTiling):
        contianer = tuple(self.params)[0]
        avoiders, containers, enumerators = comb_class.ace_parameters()
        assert self.params in containers, "Container Does Not Exist"
        base = comb_class.tiling
        new_avoiders = avoiders.add(contianer)
        new_containers = list(containers)
        new_containers.remove(self.params)
        clean = self.__class__.cleaner
        m1 = MappedTiling(base, avoiders, new_containers, enumerators)
        m2 = MappedTiling(base, new_avoiders, new_containers, enumerators)
        return (clean(m1), clean(m2))


class AvoiderExorcismFactory(StrategyFactory[MappedTiling]):
    """Transforms avoiders which map to a single cell into containers"""

    def __call__(self, comb_class):
        for avoider in comb_class.avoiding_parameters:
            if (
                len(set(avoider.col_map.values()))
                == len(set(avoider.row_map.values()))
                == 1
            ):
                yield AvoiderExorcismStrategy(ParameterList({avoider}))

    @classmethod
    def from_dict(cls, d: dict) -> "AvoiderExorcismFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Avoider exorcism"


class ContainerExorcismFactory(StrategyFactory[MappedTiling]):
    """Transforms solo containers which map to a single cell into avoiders"""

    def __call__(self, comb_class):
        for c_list in comb_class.containing_parameters:
            if len(c_list) > 1:
                continue
            for container in c_list:
                if (
                    len(container.col_map.values())
                    == len(container.row_map.values())
                    == 1
                ):
                    yield ContainerExorcismStrategy(ParameterList({container}))


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

    cleaner = MTCleaner.make_full_cleaner("Factoring Cleaner")

    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = Factor(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        factors = tuple(map(self.__class__.cleaner, factors))
        return factors


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
        return tuple(map(self.__class__.cleaner, algo.separate()))


class MapplingLessThanOrEqualRowColSeparationStrategy(
    LessThanOrEqualRowColSeparationStrategy
):
    """A strategy for separating rows and columns with less than or equal constraints."""

    cleaner = MTCleaner.make_full_cleaner("LEQ Separation Cleaner")

    def decomposition_function(self, comb_class):
        algo = LTORERowColSeparationMT(comb_class)
        return tuple(map(self.__class__.cleaner, algo.separate()))
