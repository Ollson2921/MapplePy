from collections import Counter
from functools import reduce
from operator import mul
from typing import Callable, Iterable, Iterator, Optional

from comb_spec_searcher import CartesianProduct
from gridded_cayley_permutations import GriddedCayleyPerm
from sympy import Eq, Function

from mapplings.mapped_tiling import MappedTiling
from tilescope.strategies import FactorStrategy, ShuffleFactorStrategy
from mapplings.cleaners import MTCleaner
from mapplings.algorithms import Factor, ILFactorNormal, ILFactorInverted
from comb_spec_searcher.exception import StrategyDoesNotApply
from comb_spec_searcher.typing import (
    Parameters,
    SubObjects,
    SubRecs,
    SubSamplers,
    SubTerms,
    Terms,
)


def multinomial(lst):
    """
    Returns the multinomial. Taken from
    https://stackoverflow.com/questions/46374185/does-python-have-a-function-which-computes-multinomial-coefficients
    """
    res, i = 1, sum(lst)
    i0 = lst.index(max(lst))
    for a in lst[:i0] + lst[i0 + 1 :]:
        for j in range(1, a + 1):
            res *= i
            res //= j
            i -= 1
    return res


class Interleaving(CartesianProduct[MappedTiling, GriddedCayleyPerm]):
    def __init__(
        self,
        parent: MappedTiling,
        children: Iterable[MappedTiling],
        extra_parameters: tuple[dict[str, str], ...],
        interleaving_parameters: Iterable[tuple[str, ...]],
        # insertion_constructor: Optional[AddAssumptionsConstructor],
    ):
        super().__init__(parent, children, extra_parameters)
        self.interleaving_parameters = tuple(interleaving_parameters)
        self.interleaving_indices = tuple(
            tuple(parent.extra_parameters.index(k) for k in parameters)
            for parameters in interleaving_parameters
        )
        # self.insertion_constructor = insertion_constructor

    @staticmethod
    def is_equivalence(
        is_empty: Optional[Callable[[MappedTiling], bool]] = None,
    ) -> bool:
        return False

    def get_equation(self, lhs_func: Function, rhs_funcs: tuple[Function, ...]) -> Eq:
        raise NotImplementedError

    def get_terms(
        self, parent_terms: Callable[[int], Terms], subterms: SubTerms, n: int
    ) -> Terms:
        non_interleaved_terms = super().get_terms(parent_terms, subterms, n)
        interleaved_terms: Terms = Counter()
        for parameters, value in non_interleaved_terms.items():
            # multinomial counts the number of ways to interleave the values k1, ...,kn.
            multiplier = reduce(
                mul,
                [
                    multinomial([parameters[k] for k in int_parameters])
                    for int_parameters in self.interleaving_indices
                ],
                1,
            )
            interleaved_terms[parameters] += multiplier * value
        # if self.insertion_constructor:
        #     new_terms: Terms = Counter()
        #     for param, value in interleaved_terms.items():
        #         new_terms[self.insertion_constructor.child_param_map(param)] += value
        #     return new_terms
        return interleaved_terms

    def get_sub_objects(
        self, subobjs: SubObjects, n: int
    ) -> Iterator[tuple[Parameters, tuple[list[Optional[GriddedCayleyPerm]], ...]]]:
        for param, objs in super().get_sub_objects(subobjs, n):
            if self.insertion_constructor:
                param = self.insertion_constructor.child_param_map(param)
            yield param, objs

    def random_sample_sub_objects(
        self,
        parent_count: int,
        subsamplers: SubSamplers,
        subrecs: SubRecs,
        n: int,
        **parameters: int,
    ):
        raise NotImplementedError


class MapplingFactorStrategy(FactorStrategy):
    """
    A strategy for finding factors in a mapped tiling.
    """

    cleaner = MTCleaner([], "Factoring Cleaner")

    def decomposition_function(self, comb_class) -> tuple[MappedTiling, ...]:
        factors = Factor(comb_class).find_factors()
        if len(factors) <= 1:
            raise StrategyDoesNotApply
        factors = tuple(map(self.__class__.cleaner, factors))
        return factors


# pylint:disable=too-many-ancestors
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

    def constructor(self, comb_class, children=None):
        return Interleaving(
            comb_class,
            children,
            self.extra_parameters(comb_class, children),
            self.interleaving_parameters(comb_class),
        )

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
