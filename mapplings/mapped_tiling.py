"""Module with the mapped tiling class."""

from .parameter import Parameter, ParamCleaner
from .parameter_list import ParameterList
from .cleaning_keys import *

from typing import (
    Iterable,
    Tuple,
    List,
    DefaultDict,
    Iterator,
    Callable,
    TypeVar,
    TypeVarTuple,
    Union,
)
from collections import defaultdict
from itertools import chain
from comb_spec_searcher import CombinatorialClass

from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm

Objects = DefaultDict[Tuple[int, ...], List[GriddedCayleyPerm]]
Cell = Tuple[int, int]

FuncType = TypeVar("FuncType")
ArgsType = TypeVarTuple("ArgsType")


class MappedTiling(CombinatorialClass):
    """A mapped tiling is a tiling with avoiding and containing parameters
    which map to it by row and column maps."""

    def __init__(
        self,
        tiling: Tiling,
        avoiding_parameters: ParameterList,
        containing_parameters: Iterable[ParameterList],
        enumerating_parameters: Iterable[ParameterList],
    ):
        self.avoiding_parameters = avoiding_parameters
        self.containing_parameters = tuple(sorted(containing_parameters))
        self.enumerating_parameters = tuple(sorted(enumerating_parameters))
        self.tiling = tiling
        self.obstructions = tiling.obstructions
        self.requirements = tiling.requirements
        self.dimensions = tiling.dimensions
        self.cleaner = Cleaner()

    # Containment and avoidance functions

    def gcp_in_tiling(self, gcp: GriddedCayleyPerm) -> bool:
        """Returns True if the gridded cayley permutation is in the tiling"""
        return self.gcp_satisfies_containing_params(
            gcp
        ) and self.gcp_satisfies_avoiding_params(gcp)

    def gcp_satisfies_avoiding_params(self, gcp: GriddedCayleyPerm) -> bool:
        """Returns True if the gridded cayley permutation satisfies the avoiding parameters"""
        return not any(
            self.avoiding_parameters.apply_to_all(Parameter.gcp_has_preimage, (gcp,))
        )

    def gcp_satisfies_containing_params(self, gcp: GriddedCayleyPerm) -> bool:
        """Returns True if the gridded cayley permutation satisfies the containing parameters"""
        return all(
            any(c_list.apply_to_all(Parameter.gcp_has_preimage, (gcp,)))
            for c_list in self.containing_parameters
        )

    def has_contradictory_parameters(self) -> bool:
        """
        Returns True if there is a contradiction between the avoiding and
        containing parameters - if a len 1 containing parameter list is the
        same as an avoiding parameter.
        """
        if not self.avoiding_parameters:
            return False
        len_one_cont_params = [
            contain_list
            for contain_list in self.containing_parameters
            if len(contain_list) == 1
        ]
        if not len_one_cont_params:
            return False
        if any(
            contain_list[0] == avoiding_parameter
            for contain_list in len_one_cont_params
            for avoiding_parameter in self.avoiding_parameters
        ):
            return True
        return False

    # Combintatorial class stuff

    def has_parameters(self) -> bool:
        """Check if the tiling has avoiding or containing parameters
        (doesn't check for enumerating parameters)."""
        return bool(self.avoiding_parameters or self.containing_parameters)

    def is_atom(self) -> bool:
        """Check if the tiling is an atom."""
        return self.tiling.is_atom() and not self.has_parameters()

    def minimum_size_of_object(self) -> int:
        """Return the minimum size of object in the tiling."""
        assert not self.is_empty()
        i = 0
        while True:
            for _ in self.objects_of_size(i):
                return i
            i += 1

    def objects_of_size(self, n, **parameters) -> Iterator[GriddedCayleyPerm]:
        """Return gridded Cayley permutations of size n in the tiling."""
        for val in self.get_objects(n).values():
            yield from val

    def get_objects(self, n: int) -> Objects:
        """Return the objects of size n in the tiling."""
        objects = defaultdict(list)
        for gcp in self.tiling.objects_of_size(n):
            if self.gcp_in_tiling(gcp):
                param = self.get_parameters(gcp)
                objects[param].append(gcp)
        return objects

    def get_parameters(self, obj: GriddedCayleyPerm) -> Tuple[int, ...]:
        """Parameters are not what you think!!! This is specific to
        combinatorical class parameters"""
        return tuple(
            sum(1 for param in param_list for _ in param.preimage_of_gcp(obj))
            for param_list in self.enumerating_parameters
        )

    def is_empty(self) -> bool:
        """
        Assume this is run after all cleanup functions have been applied.

        Returns True if the tiling is empty or there is a contradiction between
        containing and avoiding parameters.
        """
        return self.tiling.is_empty() or self.has_contradictory_parameters()

    @classmethod
    def from_dict(cls, d: dict) -> "MappedTiling":
        """Construct a MappedTiling from a dictionary."""
        return MappedTiling(
            Tiling.from_dict(d["tiling"]),
            ParameterList(Parameter.from_dict(p) for p in d["avoiding_parameters"]),
            [
                ParameterList(Parameter.from_dict(p) for p in ps)
                for ps in d["containing_parameters"]
            ],
            [
                ParameterList(Parameter.from_dict(p) for p in ps)
                for ps in d["enumerating_parameters"]
            ],
        )

    # other stuff

    def apply_to_all_parameters(
        self,
        func: Callable[[Parameter, *ArgsType], Parameter],
        additional_arguments: Union[tuple[*ArgsType], tuple] = tuple(),
    ) -> "MappedTiling":
        """Applies func to all parameters with additional arguments.
        Parameter must be the first argument of the function"""
        param_method = (func, additional_arguments)
        new_avoiders = ParameterList(
            self.avoiding_parameters.apply_to_all(*param_method)
        )
        new_containers = (
            ParameterList(c_list.apply_to_all(*param_method))
            for c_list in self.containing_parameters
        )
        new_enumerators = (
            ParameterList(e_list.apply_to_all(*param_method))
            for e_list in self.enumerating_parameters
        )
        return MappedTiling(self.tiling, new_avoiders, new_containers, new_enumerators)

    def clean_desired(self) -> "MappedTiling":
        return self.cleaner(self)

    def full_cleanup(self) -> "MappedTiling":
        return Cleaner.full_cleanup(self)

    # dunder methods

    def __eq__(self, other) -> bool:
        """Check if two MappedTilings are equal."""
        return (
            self.tiling == other.tiling
            and self.avoiding_parameters == other.avoiding_parameters
            and self.containing_parameters == other.containing_parameters
            and self.enumerating_parameters == other.enumerating_parameters
        )

    def __hash__(self) -> int:
        """Hash the MappedTiling."""
        return hash(
            (
                self.tiling,
                self.avoiding_parameters,
                self.containing_parameters,
                self.enumerating_parameters,
            )
        )

    def __repr__(self) -> str:
        """The repr for the MappedTiling."""
        return (
            self.__class__.__name__
            + f"({repr(self.tiling)}, {repr(self.avoiding_parameters)}, "
            + f"{repr(self.containing_parameters)}, {repr(self.enumerating_parameters)})"
        )

    def __str__(self) -> str:
        """Return a string representation of the MappedTiling."""
        return (
            "Base tiling: \n"
            + str(self.tiling)
            + "\nAvoiding parameters:\n"
            + "\n".join([str(p) for p in self.avoiding_parameters])
            + "\nContaining parameters:\n"
            + "\nNew containing parameters list \n".join(
                ["\n".join([str(p) for p in ps]) for ps in self.containing_parameters]
            )
            + "\nenumerating parameters:\n"
            + "\nNew enumerating parameters list\n".join(
                ["\n".join([str(p) for p in ps]) for ps in self.enumerating_parameters]
            )
        )


class Cleaner:
    def __init__(self, todo_list: Iterable[int] = set()):
        self.todo_list = set(todo_list)

    def __call__(self, mappling: MappedTiling) -> MappedTiling:
        """Cleans the input mappling according to the cleaner's todo_list"""
        return Cleaner.list_cleanup(mappling, self.todo_list)

    def __add__(self, other: Iterable[int]):
        return Cleaner(self.todo_list | set(other))

    @staticmethod
    def list_cleanup(
        mappling: MappedTiling, cleaning_list: Iterable[int]
    ) -> MappedTiling:
        """Applies all functions indicated by keys in cleaning_list"""
        if -1 in cleaning_list:
            cleaning_list = cleaning_function_map.keys()
        cleaning_list = tuple(sorted(cleaning_list))
        new_mappling = mappling
        for i in cleaning_list:
            new_mappling = cleaning_function_map[i](new_mappling)
        return new_mappling

    def tracked_cleanup(
        self, mappling: MappedTiling, cleaning_list: Iterable[int]
    ) -> MappedTiling:
        """Cleans mappling according to the cleaning list, and removes any completed cleaning functions from the cleaner's todo_list"""
        if -1 in cleaning_list:
            cleaning_list = cleaning_function_map.keys()
        new_mappling = Cleaner.list_cleanup(mappling, cleaning_list)
        new_mappling.cleaner = Cleaner(self.todo_list - set(cleaning_list))
        return new_mappling

    @staticmethod
    def full_cleanup(mappling: MappedTiling) -> MappedTiling:
        """Applies all cleanup functions."""
        mappling.apply_to_all_parameters(
            Parameter.add_to_cleaner,
            (
                {
                    pc_full,
                },
            ),
        )
        return Cleaner.list_cleanup(mappling, tuple(cleaning_function_map.keys()))

    # Final Methods

    @staticmethod
    def try_to_kill(mappling: MappedTiling) -> MappedTiling:
        """Used to decide how to kill mapplings in full_cleanup"""
        raise NotImplementedError

    @staticmethod
    def tidy_containers(mappling: MappedTiling) -> MappedTiling:
        """For parameters with empty tilings, if it is the only
        one in a list then the mappling is empty, otherwise remove the empty
        parameter.
        If only one parameter in a list and it maps to base tiling by the identity map
        then map obs and reqs down and remove the parameter list.
        Note: As we always assume a parameter maps to the whole tiling, we defined a row
        col map as being trivial iff the dimensions of the tiling and ghost are the same.
        """
        raise NotImplementedError

    @staticmethod
    def factor_containters(mappling: MappedTiling) -> MappedTiling:
        """Factors out the intersection factors of a containing parameter list"""
        new_containers = list(
            chain(
                *(
                    Cleaner.find_intersection(c_list)
                    for c_list in mappling.containing_parameters
                )
            )
        )
        return MappedTiling(
            mappling.tiling,
            mappling.avoiding_parameters,
            new_containers,
            mappling.enumerating_parameters,
        )

    @staticmethod
    def insert_valid_avoiders(mappling: MappedTiling) -> MappedTiling:
        """Adds requirements from every avoider that is near-trivial and removes that avoider"""
        raise NotImplementedError

    @staticmethod
    def backmap_points(mappling: MappedTiling) -> MappedTiling:
        """Backmaps point obstructions to all parameters"""
        point_obstructions = (ob for ob in mappling.obstructions if len(ob) == 1)
        return mappling.apply_to_all_parameters(
            Parameter.backmap_obstructions, (point_obstructions,)
        )

    @staticmethod
    def reap_all_contradictions(mappling: MappedTiling) -> MappedTiling:
        """Removes any contradictory parameters"""
        raise NotImplementedError

    @staticmethod
    def remove_empty_rows_and_cols(mappling: MappedTiling) -> MappedTiling:
        """Removes empty rows and cols in the base tiling and removes preimage rows and cols from the parameters"""
        empty_cols, empty_rows = mappling.tiling.find_empty_rows_and_columns()
        if (
            len(empty_cols) == mappling.dimensions[0]
            or len(empty_rows) == mappling.dimensions[1]
        ):
            return MappedTiling(
                Tiling(
                    [GriddedCayleyPerm(CayleyPermutation((0,)), [(0, 0)])], [], (1, 1)
                ),
                ParameterList([]),
                [],
                [],
            )
        mappling.tiling = mappling.tiling.delete_rows_and_columns(
            empty_cols, empty_rows
        )
        return mappling.apply_to_all_parameters(
            Parameter.delete_preimage_of_rows_and_columns, (empty_cols, empty_rows)
        )

    @staticmethod
    def clean_parameter_lists(mappling: MappedTiling) -> MappedTiling:
        new_avoiders = mappling.avoiding_parameters.cleaner(
            mappling.avoiding_parameters
        )
        new_containers = (
            c_list.cleaner(c_list) for c_list in mappling.containing_parameters
        )
        new_enumerators = (
            e_list.cleaner(e_list) for e_list in mappling.enumerating_parameters
        )
        return MappedTiling(
            mappling.tiling, new_avoiders, new_containers, new_enumerators
        )

    @staticmethod
    def reduce_redundant_parameters(mappling: MappedTiling) -> MappedTiling:
        """Removes any parameter implied by another"""
        raise NotImplementedError

    # Internal Methods

    @staticmethod
    def find_intersection(container_list: ParameterList) -> Iterable[ParameterList]:
        """Returns the intersection of the factors of the container list"""
        if len(container_list) == 1:
            return [ParameterList([factor]) for factor in container_list[0].factor()]
        all_factors = tuple(map(set, container_list.apply_to_all(Parameter.factor)))
        intersection = all_factors[0]
        for factors in all_factors:
            intersection = intersection & factors
            if not intersection:
                return [
                    container_list,
                ]
        image_cells = set(chain(*(factor.image_cells() for factor in intersection)))
        new_param_list = ParameterList([])
        for param in container_list:
            keep_cells = param.map.preimage_of_cells(param.image_cells() - image_cells)
            new_param_list.append(param.sub_parameter(keep_cells))
        return [new_param_list] + [ParameterList([factor]) for factor in intersection]

    @staticmethod
    def new_method(param: Parameter):
        pass


# this uses the keys from cleaning_keys to assign an order to the cleaning functions
cleaning_function_map = {
    mc_try_to_kill: Cleaner.try_to_kill,
    mc_tidy_containers: Cleaner.tidy_containers,
    mc_insert_avoiders: Cleaner.insert_valid_avoiders,
    mc_backmap: Cleaner.backmap_points,
    mc_reap_contradictions: Cleaner.reap_all_contradictions,
    mc_remove_empty: Cleaner.remove_empty_rows_and_cols,
    mc_clean_params: Cleaner.clean_parameter_lists,
}
