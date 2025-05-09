"""Module with the parameter list class."""

from typing import Iterator, Iterable, Tuple, Set, Callable
from itertools import product

from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from .parameter import Parameter, ParamCleaner

Cell = Tuple[int, int]


class ParameterList:
    """A tiling (called a ghost) mapping to a base tiling."""

    def __init__(self, parameters: Iterable[Parameter]):
        self.parameters = tuple(sorted(parameters))

    def append(self, param: Parameter):
        return ParameterList(self.parameters + (param,))

    def apply_to_all(
        self, func: Callable, additional_arguments: tuple = tuple()
    ) -> Iterator:
        """Applies func to all parameters in the list and yields the output"""
        for param in self:
            yield func(*((param,) + additional_arguments))

    def combined_image_rows_and_cols(self) -> Tuple[Set[int], Set[int]]:
        """Gives all base tiling rows and cols to which a parameter in the list maps"""
        col_images, row_images = set(), set()
        for param in self:
            param_images = param.image_rows_and_cols()
            col_images = col_images.union(param_images[0])
            row_images = row_images.union(param_images[1])
        return col_images, row_images

    def combined_image_cells(self) -> Set[Cell]:
        """Gives all base cells to which a parameter in the list maps"""
        return set(product(*self.combined_image_rows_and_cols()))

    def __getitem__(self, index) -> Parameter:
        return self.parameters[index]

    def __add__(self, other: "ParameterList") -> "ParameterList":
        return ParameterList(self.parameters + other.parameters)

    def __iter__(self) -> Iterator[Parameter]:
        return self.parameters.__iter__()

    def __len__(self) -> int:
        return len(self.parameters)

    def __eq__(self, other: "ParameterList") -> bool:
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
