"""Module with the parameter list class."""

from typing import (
    Iterator,
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

    def combined_image_rows_and_cols(self) -> Tuple[Set[int], Set[int]]:
        """Gives all base tiling rows and cols to which a parameter in the list maps"""
        col_images, row_images = set[int](), set[int]()
        for col_image, row_image in self.apply_to_all(Parameter.image_rows_and_cols):
            col_images.update(col_image)
            row_images.update(row_image)
        return col_images, row_images

    def combined_image_cells(self) -> Set[Cell]:
        """Gives all base cells to which a parameter in the list maps"""
        return set(chain(*self.apply_to_all(Parameter.image_cells)))
