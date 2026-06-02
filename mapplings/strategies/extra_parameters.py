"""Class with extra parameters functions for strategies"""

import abc
from typing import Optional
from comb_spec_searcher.strategies.strategy import StrategyDoesNotApply
from comb_spec_searcher import Strategy
from gridded_cayley_permutations import GriddedCayleyPerm
from mapplings import MappedTiling, ParameterList

from mapplings.cleaners.parameter_cleaner import ParamCleaner


class ExtraParametersForStrategies(Strategy[MappedTiling, GriddedCayleyPerm]):
    """Strategies inherit to implement extra_parameters function.
    Need to also implement map_for_clouds function on the strategy,
    which returns a tuple of RowColMaps for each child, mapping from the parent to the child.
    """

    def extra_parameters(
        self,
        comb_class: MappedTiling,
        children: Optional[tuple[MappedTiling, ...]] = None,
    ) -> tuple[dict[str, str], ...]:
        """Returns a tuple of dictionaries of extra parameters for each child."""
        if children is None:
            children = self.decomposition_function(comb_class)
        if children is None:
            raise StrategyDoesNotApply("Strategy does not apply")
        dicts: tuple[dict[str, str], ...] = tuple({} for _ in range(len(children)))
        for enumerating_param_list in comb_class.enumerating_parameters:
            parent_param = comb_class.find_parameter(enumerating_param_list)
            child_enumerating_params_tuple = self.update_enumerator_list(
                comb_class, enumerating_param_list
            )
            for idx, child in enumerate(children):
                child_enumerating_params = child_enumerating_params_tuple[idx]
                cleaned_child_enumerating_params = self.update_from_cleaner(
                    child, child_enumerating_params
                )
                if cleaned_child_enumerating_params in child.enumerating_parameters:
                    dicts[idx][parent_param] = child.find_parameter(
                        cleaned_child_enumerating_params
                    )
        return dicts

    def update_from_cleaner(
        self, comb_class: MappedTiling, enumerator_list: ParameterList
    ) -> ParameterList:
        """Updates an enumerator list using the cleaner."""
        param_cleaner = ParamCleaner.make_full_cleaner("Param Default Cleaner")
        new_enumerator_list = enumerator_list
        for func in param_cleaner:
            if getattr(func, "run_on_enumerators"):
                new_enumerator_list = ParameterList(
                    param.update_active_cells(comb_class.tiling)
                    for param in new_enumerator_list.apply_to_all(func)
                )
        return new_enumerator_list

    @abc.abstractmethod
    def update_enumerator_list(
        self, comb_class: MappedTiling, enumerator_list: ParameterList
    ) -> tuple[ParameterList, ...]:
        """For a enumerator list on the parent, returns a tuple of the updated lists
        for each child"""
