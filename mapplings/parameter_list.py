"""Module with the parameter list class."""

from typing import (
    Iterator,
    Callable,
    TypeVar,
    TypeVarTuple,
    Union,
)
from itertools import chain

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
    
    def remove_contradictions(self, tiling : Tiling) -> "ParameterList":
        """Removes any contradictory ghosts from the parameter list."""
        return ParameterList(param for param in self if not param.is_contradictory(tiling))

    def __le__(self, other: object):
        if isinstance(other, ParameterList):
            return tuple(sorted(self)) <= tuple(sorted(other))
        return NotImplemented

    def __lt__(self, other: object):
        if isinstance(other, ParameterList):
            return tuple(sorted(self)) < tuple(sorted(other))
        return NotImplemented
