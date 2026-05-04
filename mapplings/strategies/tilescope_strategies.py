"""Strategies for mapplings tilescope."""

from typing import Iterator, Iterable
from gridded_cayley_permutations import (
    Tiling,
    GriddedCayleyPerm,
    ObstructionTransitivity,
)
from gridded_cayley_permutations.point_placements import (
    DIRECTIONS,
    DIR_LEFT_BOT,
    DIR_RIGHT_BOT,
    DIR_LEFT_TOP,
    DIR_RIGHT_TOP,
    DIR_LEFT,
    DIR_RIGHT,
)
from tilescope.strategies import (
    AbstractFactorStrategy,
    AbstractShuffleFactorStrategy,
    AbstractRequirementPlacementStrategy,
    AbstractLessThanRowColSeparationStrategy,
    AbstractLessThanOrEqualRowColSeparationStrategy,
    AbstractLessThanOrEqualRowColSeparationFactory,
    AbstractCellInsertionFactory,
    AbstractPointPlacementFactory,
    AbstractRowInsertionFactory,
    AbstractColInsertionFactory,
    AbstractRequirementInsertionStrategy,
    AbstractObstructionTransitivityStrategy,
)
from tilescope.strategies.row_column_separation import LessThanOrEqualRowColSeparation
from mapplings import MappedTiling, ParameterList, Parameter


from comb_spec_searcher import (
    DisjointUnionStrategy,
    CombinatorialSpecificationSearcher,
)
from comb_spec_searcher.exception import StrategyDoesNotApply
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, Parameter
from mapplings.algorithms import (
    MTRequirementPlacement,
    MTFactors,
    MTILFactorNormal,
    MTILFactorInverted,
    MTLTORERowColSeparation,
    MTLTRowColSeparation,
)
from mapplings.cleaners import MTCleaner, ParamCleaner

MTCleaner.global_log_toggle(1)
temp = CombinatorialSpecificationSearcher.status


def new_status(self, elaborate: bool) -> str:
    """Overwrites CSS status method"""
    output = (
        temp(self, elaborate) + MTCleaner.status_update() + ParamCleaner.status_update()
    )
    return output


CombinatorialSpecificationSearcher.status = new_status  # type: ignore


class MapplingRequirementPlacementStrategy(AbstractRequirementPlacementStrategy):
    """
    A strategy for placing requirements in a mapped tiling.
    """

    cleaner = MTCleaner.make_full_cleaner("Req Placement Cleaner")

    def algorithm(self, tiling):
        """Returns the algorithm to use for placing points in a mapped tiling."""
        return MTRequirementPlacement(tiling)

    def decomposition_function(self, comb_class):
        return tuple(
            map(
                self.__class__.cleaner,
                (comb_class.add_obstructions(self.gcps),)
                + self.algorithm(comb_class).point_placement(
                    self.gcps, self.indices, self.direction
                ),
            )
        )


class MapplingRequirementInsertionStrategy(AbstractRequirementInsertionStrategy):
    """Mappling version of RequirementInsertionStrategy with a cleaner"""

    cleaner = MTCleaner.make_full_cleaner("Req Insertion Cleaner")

    def decomposition_function(self, comb_class):
        return tuple(
            map(
                self.__class__.cleaner,
                (
                    comb_class.add_obstructions(self.gcps),
                    comb_class.add_requirement_list(self.gcps),
                ),
            )
        )


class MapplingCellInsertionFactory(AbstractCellInsertionFactory):
    """Factory for inserting points into active cells of a tiling."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementInsertionStrategy]:
        for cell in comb_class.active_cells:
            gcps = (GriddedCayleyPerm(CayleyPermutation([0]), (cell,)),)
            strategy = MapplingRequirementInsertionStrategy(gcps, ignore_parent=False)
            yield strategy


class MapplingPointPlacementFactory(AbstractPointPlacementFactory):
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


class MapplingRowPlacementFactory(AbstractRowInsertionFactory):
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


class MapplingColPlacementFactory(AbstractColInsertionFactory):
    """A factory for placing the leftmost or rightmost points in
    the columns of tilings."""

    def __call__(
        self, comb_class: Tiling
    ) -> Iterator[MapplingRequirementPlacementStrategy]:
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


class MapplingFactorStrategy(AbstractFactorStrategy):
    """
    A strategy for finding factors in a mapped tiling.
    """

    cleaner = MTCleaner([], "Factoring Cleaner")

    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = MTFactors(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        factors = tuple(map(self.__class__.cleaner, factors))
        return factors


class MapplingILFactorStrategy(AbstractShuffleFactorStrategy):
    """
    A strategy for finding interleaving factors in a mapped tiling.
    """

    cleaner = MTCleaner.make_full_cleaner("IL Factoring Cleaner")

    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = MTILFactorNormal(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        factors = tuple(map(self.__class__.cleaner, factors))
        return factors

    def formal_step(self) -> str:
        return "Factor the mappling into interleaving factors"


class MapplingInvertedILFactorStrategy(AbstractShuffleFactorStrategy):
    """
    A strategy for finding interleaving factors in a mapped tiling by inverting 00 obstructions
    """

    cleaner = MTCleaner.make_full_cleaner("Inverted IL Factoring Cleaner")

    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = MTILFactorInverted(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        factors = tuple(map(self.__class__.cleaner, factors))
        return factors

    def formal_step(self) -> str:
        return "Invert obstructions and factor the mappling into interleaving factors"


class MapplingLessThanRowColSeparationStrategy(
    AbstractLessThanRowColSeparationStrategy
):
    """A strategy for separating rows and columns with less than constraints."""

    cleaner = MTCleaner.make_full_cleaner("LT Separation Cleaner")

    def decomposition_function(self, comb_class):
        algo = MTLTRowColSeparation(comb_class)
        if algo.separation.row_col_map.is_identity():
            raise StrategyDoesNotApply
        return tuple(map(self.__class__.cleaner, algo.separate()))


class MapplingLessThanOrEqualRowColSeparationStrategy(
    AbstractLessThanOrEqualRowColSeparationStrategy
):
    """A strategy for separating rows and columns with less than or equal constraints."""

    cleaner = MTCleaner.make_full_cleaner("LEQ Separation Cleaner")

    def algorithm(self, comb_class):
        """Returns the algorithm for finding the row and column separation."""
        return MTLTORERowColSeparation(comb_class, self.row_order)

    def decomposition_function(self, comb_class):
        algo = self.algorithm(comb_class)
        if algo.separation.row_col_map.is_identity():
            raise StrategyDoesNotApply
        return tuple(map(self.__class__.cleaner, algo.separate()))


class MapplingLessThanOrEqualRowColSeparationFactory(
    AbstractLessThanOrEqualRowColSeparationFactory
):
    """A factory for making less than or equal row/col separation strategies."""

    def algorithm(self, comb_class: MappedTiling) -> LessThanOrEqualRowColSeparation:
        """The algorithm for finding the row and column separation."""
        return LessThanOrEqualRowColSeparation(comb_class.tiling)

    def __call__(
        self, comb_class: MappedTiling
    ) -> Iterator[MapplingLessThanOrEqualRowColSeparationStrategy]:
        """Finds max expansion and if any row separates more than 2 cells then
        it merges them together so that each row splits into at most 2 rows
        (plus a point row between them) and yields all possible ways of doing this."""
        for row_order in self.row_separations(comb_class):
            yield MapplingLessThanOrEqualRowColSeparationStrategy(
                row_order=row_order,
            )


class MapplingObstructionTransitivityStrategy(AbstractObstructionTransitivityStrategy):
    """A strategy for adding new obstructions to the tiling based on the current obstructions."""

    def decomposition_function(
        self, comb_class: MappedTiling
    ) -> tuple[MappedTiling, ...]:
        """Updates base tiling, avoiding parameters, and containing parameters
        based on obstruction transitivity.

        TODO: As we're adding obstructions, we should simplify the parameter's tilings
        too. Should this happen when simplify=True for a mappling?"""
        new_bt_obs = ObstructionTransitivity(comb_class).new_obs()
        found_new_obs = bool(new_bt_obs)
        new_av_params, found_new = self.obs_trans_for_param_list(
            comb_class.avoiding_parameters
        )
        found_new_obs = found_new_obs or found_new
        new_cont_params = []
        for cont_param_list in comb_class.containing_parameters:
            new_cont_param_list, found_new = self.obs_trans_for_param_list(
                cont_param_list
            )
            new_cont_params.append(ParameterList(new_cont_param_list))
            found_new_obs = found_new_obs or found_new

        if not found_new_obs:
            raise StrategyDoesNotApply("No new obstructions to add.")
        return (
            MappedTiling(
                comb_class.add_obstructions(new_bt_obs).tiling,
                new_av_params,
                new_cont_params,
                comb_class.enumerating_parameters,
                simplify=True,
            ),
        )

    def obs_trans_for_param_list(
        self, param_list: Iterable[Parameter]
    ) -> tuple[list[Parameter], bool]:
        """Does obstruction transitivity on each param in a param list,
        returns the new list and a bool if any new obstructions were added."""
        added_obs = False
        new_param_list = []
        for param in param_list:
            new_obs = ObstructionTransitivity(param).new_obs()
            if new_obs:
                added_obs = True
                param = param.add_obstructions(new_obs)
            new_param_list.append(param)
        return new_param_list, added_obs
