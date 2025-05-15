"""Module with the parameter list class."""

from typing import (
    Iterator,
    Iterable,
    Tuple,
    Set,
    Callable,
    TypeVar,
    TypeVarTuple,
    Union,
)
from itertools import chain
from .parameter import Parameter


Cell = Tuple[int, int]

FuncTypeT = TypeVar("FuncTypeT")
ArgsType = TypeVarTuple("ArgsType")


class ParameterList:
    """A tiling (called a ghost) mapping to a base tiling."""

    def __init__(self, parameters: Iterable[Parameter]):
        self.parameters = tuple(sorted(parameters))

    def append(self, param: Parameter):
        """Adds param to self"""
        return ParameterList(self.parameters + (param,))

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

    def combined_image_rows_and_cols(self) -> Tuple[Set[int], Set[int]]:
        """Gives all base tiling rows and cols to which a parameter in the list maps"""
        col_images, row_images = map(
            set, zip(*self.apply_to_all(Parameter.image_rows_and_cols))
        )
        return col_images, row_images

    def combined_image_cells(self) -> Set[Cell]:
        """Gives all base cells to which a parameter in the list maps"""
        return set(chain(*self.apply_to_all(Parameter.image_cells)))

    # dunder methods

    def __getitem__(self, index) -> Parameter:
        return self.parameters[index]

    def __add__(self, other: "ParameterList") -> "ParameterList":
        return ParameterList(self.parameters + other.parameters)

    def __iter__(self) -> Iterator[Parameter]:
        return self.parameters.__iter__()

    def __len__(self) -> int:
        return len(self.parameters)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ParameterList):
            return NotImplemented
        return self.parameters == other.parameters

    def __lt__(self, other: "ParameterList") -> bool:
        return self.parameters < other.parameters

    def __leq__(self, other: "ParameterList") -> bool:
        return self.parameters <= other.parameters

    def __hash__(self) -> int:
        return hash(self.parameters)

    def __repr__(self) -> str:
        return repr(self.parameters)

    def __str__(self) -> str:
        return "\n".join([str(p) for p in self])
