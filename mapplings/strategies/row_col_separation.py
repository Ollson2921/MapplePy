"""Row and column separation strategies for mapped tilings."""

from mapplings import MappedTiling, ParameterList
from gridded_cayley_permutations import GriddedCayleyPerm
from mapplings.cleaners import MTCleaner
from mapplings.strategies.extra_parameters import ExtraParametersForStrategies
from comb_spec_searcher.exception import StrategyDoesNotApply
from tilescope.strategies import (
    LessThanRowColSeparationStrategy,
    LessThanOrEqualRowColSeparationStrategy,
)
from mapplings.algorithms import (
    LTORERowColSeparationMT,
    LTRowColSeparationMT,
)
from tilescope.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)


class MapplingLessThanRowColSeparationStrategy(
    ExtraParametersForStrategies, LessThanRowColSeparationStrategy
):
    """A strategy for separating rows and columns with less than constraints."""

    cleaner = MTCleaner.make_full_cleaner("LT Separation Cleaner")

    def algorithm(self, comb_class: MappedTiling) -> LessThanRowColSeparation:
        return LTRowColSeparationMT(comb_class).separation

    def decomposition_function(self, comb_class):
        if self.algorithm(comb_class).row_col_map.is_identity():
            raise StrategyDoesNotApply
        return tuple(
            map(self.__class__.cleaner, LTRowColSeparationMT(comb_class).separate())
        )

    def update_enumerator_list(
        self, comb_class: MappedTiling, enumerator_list: ParameterList
    ) -> tuple[ParameterList, ...]:
        new_param_list = ParameterList(
            [
                LTRowColSeparationMT(comb_class).make_new_parameter(param)
                for param in enumerator_list
            ]
        )
        return (new_param_list,) * len(self.decomposition_function(comb_class))


class MapplingLessThanOrEqualRowColSeparationStrategy(
    ExtraParametersForStrategies, LessThanOrEqualRowColSeparationStrategy
):
    """A strategy for separating rows and columns with less than or equal constraints."""

    cleaner = MTCleaner.make_full_cleaner("LEQ Separation Cleaner")

    def algorithm(self, comb_class: MappedTiling) -> LessThanOrEqualRowColSeparation:
        return LTORERowColSeparationMT(comb_class).separation

    def decomposition_function(self, comb_class):
        if self.algorithm(comb_class).row_col_map.is_identity():
            raise StrategyDoesNotApply
        return tuple(
            map(self.__class__.cleaner, LTORERowColSeparationMT(comb_class).separate())
        )

    def update_enumerator_list(
        self, comb_class: MappedTiling, enumerator_list: ParameterList
    ) -> tuple[ParameterList, ...]:
        new_param_list = ParameterList(
            [
                LTORERowColSeparationMT(comb_class).make_new_parameter(param)
                for param in enumerator_list
            ]
        )
        return (new_param_list,) * len(self.decomposition_function(comb_class))
