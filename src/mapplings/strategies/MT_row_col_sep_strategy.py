from typing import Dict, Iterator, Optional, Tuple
from comb_spec_searcher import DisjointUnionStrategy
from comb_spec_searcher.exception import StrategyDoesNotApply
from comb_spec_searcher.strategies.constructor import Constructor
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.factors import Factors, ShuffleFactors
from mapplings import MappedTiling, Parameter, MTFactor
from mapplings.MT_row_col_separation import MTRowColSeparation, MTRowColSeparation_EQ


class MTLessThanRowColSeparationStrategy(
    DisjointUnionStrategy[MappedTiling, GriddedCayleyPerm]
):
    def __init__(
        self,
        ignore_parent: bool = True,
        possibly_empty: bool = True,
    ):
        super().__init__(ignore_parent=ignore_parent, possibly_empty=possibly_empty)

    def decomposition_function(
        self, comb_class: MappedTiling
    ) -> Tuple[MappedTiling, ...]:
        algo = MTRowColSeparation(comb_class)
        if algo.separation.new_dimensions == comb_class.tiling.dimensions:
            raise StrategyDoesNotApply
        return (next(algo.separate_base_tiling()),)

    def extra_parameters(
        self, comb_class: Tiling, children: Optional[Tuple[Tiling, ...]] = None
    ) -> Tuple[Dict[str, str], ...]:
        return tuple({} for _ in self.decomposition_function(comb_class))

    def formal_step(self):
        return "Separate rows and columns in the base tiling"

    def backward_map(
        self,
        comb_class: Tiling,
        objs: Tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: Tiling,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[Tiling, ...]] = None,
    ) -> Tuple[Optional[GriddedCayleyPerm], ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def __str__(self) -> str:
        return self.formal_step()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"ignore_parent={self.ignore_parent}, "
            f"possibly_empty={self.possibly_empty})"
        )

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "MTLessThanRowColSeparationStrategy":
        return cls(
            ignore_parent=d["ignore_parent"],
            possibly_empty=d["possibly_empty"],
        )


class MTLessThanOrEqualRowColSeparationStrategy(MTLessThanRowColSeparationStrategy):
    def decomposition_function(
        self, comb_class: MappedTiling
    ) -> Tuple[MappedTiling, ...]:
        algo = MTRowColSeparation_EQ(comb_class)
        if algo.separation.new_dimensions == comb_class.tiling.dimensions:
            raise StrategyDoesNotApply
        return tuple(algo.separate_base_tiling())

    def formal_step(self):
        return super().formal_step() + " allowing interleaving in top/bottom rows"


class MTParamLessThanRowColSeparationStrategy(MTLessThanRowColSeparationStrategy):
    def decomposition_function(
        self, comb_class: MappedTiling
    ) -> Tuple[MappedTiling, ...]:
        new_avoiders = []
        new_containers = []
        new_enumerators = []
        for param in comb_class.avoiding_parameters:
            new_avoiders.append(MTRowColSeparation.separate_parameter(param))
        for c_list in comb_class.containing_parameters:
            new_c_list = []
            for param in c_list:
                new_c_list.append(MTRowColSeparation.separate_parameter(param))
            new_containers.append(new_c_list)
        for e_list in comb_class.enumeration_parameters:
            new_e_list = []
            for param in e_list:
                new_e_list.append(MTRowColSeparation.separate_parameter(param))
            new_enumerators.append(new_e_list)
        return [
            MappedTiling(
                comb_class.tiling, new_avoiders, new_containers, new_enumerators
            )
        ]

    def formal_step(self):
        return "Separate rows and columns in the parameter"
