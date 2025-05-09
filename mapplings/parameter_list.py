"""Module with the parameter list class."""

from typing import Iterator, Iterable, Tuple, Set, Callable
from itertools import product

from parameter import Parameter, ParamCleaner
from cleaning_keys import *

from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap


Cell = Tuple[int, int]


class ParameterList:
    """A tiling (called a ghost) mapping to a base tiling."""

    def __init__(self, parameters: Iterable[Parameter]):
        self.parameters = tuple(sorted(parameters))
        self.cleaner = ListCleaner()

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

    def clean_desired(self) -> "ParameterList":
        """Cleans the param list according to todo list"""
        return self.cleaner(self)

    def full_cleanup(self) -> "ParameterList":
        """Applies all cleaning functions to the param list"""
        return ListCleaner.full_cleanup(self)

    # dunder methods

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


class ListCleaner:
    def __init__(self, todo_list: Iterable[int] = set()):
        self.todo_list = set(todo_list)

    def __call__(self, param_list: ParameterList) -> ParameterList:
        """Cleans the input param according to the cleaner's todo_list"""
        return ListCleaner.list_cleanup(param_list, self.todo_list)

    def __add__(self, other: Iterable[int]):
        return ListCleaner(self.todo_list | set(other))

    @staticmethod
    def list_cleanup(
        param_list: ParameterList, cleaning_list: Iterable[int]
    ) -> ParameterList:
        """Applies all functions indicated by keys in cleaning_list"""
        cleaning_list = tuple(sorted(cleaning_list))
        new_param_list = param_list
        for i in cleaning_list:
            new_param_list = list_cleaning_function_map[i](new_param_list)
        return new_param_list

    def tracked_cleanup(
        self, param: ParameterList, cleaning_list: Iterable[int]
    ) -> ParameterList:
        """Cleans param according to the cleaning list, and removes any completed cleaning functions from the cleaner's todo_list"""
        new_param_list = ListCleaner.list_cleanup(param, cleaning_list)
        new_param_list.cleaner = ListCleaner(self.todo_list - set(cleaning_list))
        return new_param_list

    @staticmethod
    def full_cleanup(param_list: ParameterList) -> ParameterList:
        """Applies all cleanup functions."""
        return ListCleaner.list_cleanup(
            param_list, tuple(list_cleaning_function_map.keys())
        )

    @staticmethod
    def method_name0(param_list: ParameterList) -> ParameterList:
        """An example cleaning function"""
        return param_list

    @staticmethod
    def method_name1(param_list: ParameterList) -> ParameterList:
        """An example cleaning function"""
        return param_list


list_cleaning_function_map = {
    lc_method_nickname0: ListCleaner.method_name0,
    lc_method_nickname1: ListCleaner.method_name1,
}
