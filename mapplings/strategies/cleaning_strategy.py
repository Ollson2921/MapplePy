"""Strategies for mapplings tilescope."""

from gridded_cayley_permutations import GriddedCayleyPerm
from comb_spec_searcher import (
    DisjointUnionStrategy,
    CombinatorialSpecificationSearcher,
)
from mapplings import MappedTiling, ParameterList
from mapplings.strategies.extra_parameters import ExtraParametersForStrategies
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


class CleaningStrategy(
    ExtraParametersForStrategies, DisjointUnionStrategy[MappedTiling, GriddedCayleyPerm]
):
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

    def update_enumerator_list(
        self, comb_class: MappedTiling, enumerator_list: ParameterList
    ) -> tuple[ParameterList, ...]:
        raise NotImplementedError

    def formal_step(self) -> str:
        return "Clean mappling"

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def forward_map(self, comb_class, obj, children=None):
        raise NotImplementedError

    def backward_map(self, comb_class, objs, children=None):
        raise NotImplementedError
