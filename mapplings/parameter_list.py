"""Module with the parameter class."""

from typing import Iterator, Iterable
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from parameter import Parameter, ParamCleaner


class ParameterList:
    """A tiling (called a ghost) mapping to a base tiling."""

    def __init__(self, parameters: Iterable[Parameter]):
        self.parameters = parameters

    def __getitem__(self, index) -> Parameter:
        return self.parameters[index]

    def apply_to_all(
        self, func: function, additional_arguments: tuple
    ) -> "ParameterList":
        """Applies function to all parameters in the list
        requires parameter to be the first argument"""
        return ParameterList(
            [func(*((param,) + additional_arguments)) for param in self.parameters]
        )
