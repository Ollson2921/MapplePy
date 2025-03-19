from typing import Dict, Iterable, Iterator, Optional, Tuple
from comb_spec_searcher import DisjointUnionStrategy, StrategyFactory
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from cayley_permutations import CayleyPermutation
from mapped_tiling import Parameter, MappedTiling
from gridded_cayley_permutations.row_col_map import RowColMap

Cell = Tuple[int, int]

point = CayleyPermutation((0,))

special_pattern_0 = Parameter(
    Tiling.from_vincular(CayleyPermutation((0,1)),[]).add_obstructions(
        [GriddedCayleyPerm(point,[(0,0)]),
         GriddedCayleyPerm(point,[(2,0)]),
         GriddedCayleyPerm(point,[(0,2)]),
         GriddedCayleyPerm(point,[(2,2)]),
         GriddedCayleyPerm(point,[(4,4)]),
         ]
    ), RowColMap({0:0,1:0,2:0,3:0,4:0},{0:0,1:0,2:0,3:0,4:0}))

SpecialPatterns = [special_pattern_0]


class SpecialInsertionStrategy(
    DisjointUnionStrategy[MappedTiling, GriddedCayleyPerm]
):
    """Places the requirements in gcps at the indices in the direction given in the mappling."""

    def __init__(
        self,
        index: int,
        ignore_parent: bool = False,
    ):
        self.index = index
        self.pattern = SpecialPatterns[index]
        super().__init__(ignore_parent=ignore_parent)

    def decomposition_function(
        self, comb_class: MappedTiling
    ) -> Tuple[MappedTiling, ...]:
        """Adds a special pattern as either an avoiding parameter or a length 1 containing parameter list"""
        new_pattern = self.pattern.back_map_obs_and_reqs(comb_class.tiling)
        containing = self.simplify(MappedTiling(comb_class.add_parameters([],[[new_pattern]],[])))
        avoiding = self.simplify(MappedTiling(comb_class.add_parameters([new_pattern],[],[])))
        return (containing,avoiding) 

    def simplify(self, comb_class: MappedTiling) -> MappedTiling:
        return comb_class
        
    def extra_parameters(
        self,
        comb_class: MappedTiling,
        children: Optional[Tuple[MappedTiling, ...]] = None,
    ) -> Tuple[Dict[str, str], ...]:
        return tuple({} for _ in self.decomposition_function(comb_class))

    def formal_step(self):
        return f"Inserted pattern {self.index}"

    def backward_map(
        self,
        comb_class: MappedTiling,
        objs: Tuple[Optional[GriddedCayleyPerm], ...],
        children: Optional[Tuple[MappedTiling, ...]] = None,
    ) -> Iterator[GriddedCayleyPerm]:
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def forward_map(
        self,
        comb_class: MappedTiling,
        obj: GriddedCayleyPerm,
        children: Optional[Tuple[MappedTiling, ...]] = None,
    ) -> Tuple[Optional[GriddedCayleyPerm], ...]:
        if children is None:
            children = self.decomposition_function(comb_class)
        raise NotImplementedError

    def __str__(self) -> str:
        return self.formal_step()

    def __repr__(self) -> str:
        return (
            f"SpecialInsertionFactory(pattern {self.index}, "
        )

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        d.pop("possibly_empty")
        d["pattern"] = self.index
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "SpecialInsertionStrategy":
        pattern = d["pattern"]
        return cls(pattern=pattern, **d)


class SpecialInsertionFactory(StrategyFactory[MappedTiling]):
    def __call__(
        self, comb_class: MappedTiling
    ) -> Iterator[SpecialInsertionStrategy]:
        """Factory to place each special parameter if the base tiling is 1x1 and has no parameters."""
        if all([comb_class.tiling.dimensions == (1,1),
            len(comb_class.avoiding_parameters), 
            len(comb_class.containing_parameters), 
            len(comb_class.enumeration_parameters)]):
            for i in range(1):
                yield SpecialInsertionStrategy(i)

    @classmethod
    def from_dict(cls, d: dict) -> "SpecialInsertionFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Special Insertion"