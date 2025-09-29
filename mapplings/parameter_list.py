"""Module with the parameter list class."""

from typing import (
    Iterator,
    Callable,
    TypeVar,
    TypeVarTuple,
    Union,
)
from itertools import chain, combinations

from gridded_cayley_permutations import Tiling

from .parameter import Parameter


Cell = tuple[int, int]

FuncTypeT = TypeVar("FuncTypeT")
ArgsType = TypeVarTuple("ArgsType")


class ParameterList(frozenset[Parameter]):
    """A tiling (called a ghost) mapping to a base tiling."""

    def add(self, param: Parameter) -> "ParameterList":
        """Adds param to self"""
        return ParameterList(
            self.union(
                ParameterList(
                    {
                        param,
                    }
                )
            )
        )

    def apply_to_all(
        self,
        func: Callable[[Parameter, *ArgsType], FuncTypeT],
        additional_arguments: Union[tuple[*ArgsType], tuple] = tuple(),
    ) -> Iterator[FuncTypeT]:
        """Applies func to all parameters in the list and yields the output"""

        def temp_func(param):
            return func(*((param,) + additional_arguments))

        for param in self:
            yield temp_func(param)

    def combined_image_rows_and_cols(self) -> tuple[set[int], set[int]]:
        """Gives all base tiling rows and cols to which a parameter in the list maps"""
        image_cols, image_rows = map(set[int], zip(*self.combined_image_cells()))
        return image_cols, image_rows

    def combined_image_cells(self) -> set[Cell]:
        """Gives all base cells to which a parameter in the list maps"""
        return set(chain(*self.apply_to_all(Parameter.image_cells)))

    def remove_contradictions(self, tiling: Tiling) -> "ParameterList":
        """Removes any contradictory ghosts from the parameter list."""
        return ParameterList(
            param for param in self if not param.is_contradictory(tiling)
        )

    def remove_empty(self) -> "ParameterList":
        """Removes parameters with empty ghost"""
        return ParameterList(param for param in self if not param.is_empty())

    def simple_remove_redundant(self) -> "ParameterList":
        """Removes any parameter implied by another through a basic check"""
        exclude = set[Parameter]()
        for param0, param1 in combinations(self, 2):
            if {param0, param1} & exclude:
                continue
            image_cells = param0.image_cells()
            if not image_cells.issubset(param1.image_cells()):
                continue
            temp_param = param1.sub_parameter(param1.map.preimage_of_cells(image_cells))
            if param0.map != temp_param.map:
                continue
            if param0.ghost.is_subset(temp_param.ghost):
                exclude.add(param1)
        return ParameterList(param for param in self if param not in exclude)

    def __repr__(self):
        return self.__class__.__name__ + f"({frozenset(self)})"

    def __le__(self, other: object):
        if isinstance(other, ParameterList):
            return tuple(sorted(self)) <= tuple(sorted(other))
        return NotImplemented

    def __lt__(self, other: object):
        if isinstance(other, ParameterList):
            return tuple(sorted(self)) < tuple(sorted(other))
        return NotImplemented
