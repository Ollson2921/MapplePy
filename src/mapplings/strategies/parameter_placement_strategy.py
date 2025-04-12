"""Places a point requirement in a mappling in extreme directions.
0 = rightmost
1 = topmost, taking the rightmost if there are multiple
2 = topmost, taking the leftmost if there are multiple
3 = leftmost
4 = bottommost, taking the leftmost if there are multiple
5 = bottommost, taking the rightmost if there are multiple"""

from typing import Dict, Iterable, Iterator, Optional, Tuple
from comb_spec_searcher import DisjointUnionStrategy, StrategyFactory
from gridded_cayley_permutations.point_placements import (
    Directions,
    Right_bot,
    Left,
    Right,
    Left_bot,
    Left_top,
    Right_top,
)
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from cayley_permutations import CayleyPermutation
from mapplings.mapped_tiling import MappedTiling, Parameter
from mapplings.parameter_placement import ParameterPlacement

Cell = Tuple[int, int]


class MTParameterPlacementStrategy(
    DisjointUnionStrategy[MappedTiling, GriddedCayleyPerm]
):
    """Places the parameter at the indices in the direction and cell given in the mappling."""

    DIRECTIONS = Directions

    def __init__(
        self,
        mappling: MappedTiling,
        parameter: Parameter,
        index_of_pattern: int,
        direction: int,
        cell: Cell,
        ignore_parent: bool = False,
        possibly_empty: bool = True,
    ):
        self.mappling = mappling
        self.parameter = parameter
        self.index_of_pattern = index_of_pattern
        self.direction = direction
        self.cell = cell
        assert direction in self.DIRECTIONS
        super().__init__(ignore_parent=ignore_parent, possibly_empty=possibly_empty)

    def algorithm(self) -> ParameterPlacement:
        return ParameterPlacement(self.mappling, self.parameter, self.cell)

    def decomposition_function(
        self, comb_class: MappedTiling
    ) -> Tuple[MappedTiling, ...]:
        """Either the cells doesn't contain gcp so add it as obstruction
        or it contains an occurrence of it furthest in the direction given
        so add it as a requirement in every possible way."""
        return self.simplify(
            self.algorithm().param_placement(self.index_of_pattern, self.direction)
        )

    def simplify(self, comb_class: MappedTiling) -> MappedTiling:
        return comb_class.full_cleanup()

    def extra_parameters(
        self,
        comb_class: MappedTiling,
        children: Optional[Tuple[MappedTiling, ...]] = None,
    ) -> Tuple[Dict[str, str], ...]:
        return tuple({} for _ in self.decomposition_function(comb_class))

    def formal_step(self):
        return f"Placed the point of the parameter {self.parameter} at indices {self.index_of_pattern} in direction {self.direction} in cell {self.cell}"

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
            f"MTParameterPlacementStrategy(gcps={self.gcps}, "
            f"indices={self.indices}, direction={self.direction}, "
            f"ignore_parent={self.ignore_parent})"
        )

    def to_jsonable(self) -> dict:
        """Return a dictionary form of the strategy."""
        d: dict = super().to_jsonable()
        d.pop("workable")
        d.pop("inferrable")
        d.pop("possibly_empty")
        d["gcps"] = tuple(gp.to_jsonable() for gp in self.gcps)
        d["indices"] = self.indices
        d["direction"] = self.direction
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "MTParameterPlacementStrategy":
        gcps = tuple(GriddedCayleyPerm.from_dict(gcp) for gcp in d.pop("gcps"))
        return cls(gcps=gcps, **d)


class MTParameterPlacementFactory(StrategyFactory[MappedTiling]):
    def __call__(
        self, comb_class: MappedTiling
    ) -> Iterator[MTParameterPlacementStrategy]:
        """Factory to place every point of a containing parameter into a mappling in every possible way."""
        for c_list in comb_class.containing_parameters:
            if len(c_list) == 1:
                param = c_list[0]
                points = sorted(list(param.ghost.point_cells()))
                for i in range(len(points)):
                    cell = (
                        param.map.col_map[points[i][0]],
                        param.map.row_map[points[i][1]],
                    )
                    if not comb_class.tiling.cell_is_point_cell(cell):
                        for direction in Directions:
                            yield MTParameterPlacementStrategy(
                                comb_class, param, i, direction, cell
                            )

    @classmethod
    def from_dict(cls, d: dict) -> "MTParameterPlacementFactory":
        return cls(**d)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "Parameter placement"
