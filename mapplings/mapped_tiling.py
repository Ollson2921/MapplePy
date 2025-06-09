"""Module with the mapped tiling class."""

from typing import (
    Iterable,
    List,
    DefaultDict,
    Iterator,
    Callable,
    TypeVar,
    TypeVarTuple,
    Union,
)
from collections import defaultdict
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm

from .parameter import Parameter
from .parameter_list import ParameterList


Objects = DefaultDict[tuple[int, ...], List[GriddedCayleyPerm]]
Cell = tuple[int, int]

FuncTypeT = TypeVar("FuncTypeT")
ArgsType = TypeVarTuple("ArgsType")


class MappedTiling(Tiling):
    """A mapped tiling is a tiling with avoiding and containing parameters
    which map to it by row and column maps."""

    # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        tiling: Tiling,
        avoiding_parameters: Iterable[Parameter],
        containing_parameters: Iterable[ParameterList],
        enumerating_parameters: Iterable[ParameterList],
        simplify: bool = False,
    ):
        self.avoiding_parameters = ParameterList(avoiding_parameters)
        self.containing_parameters = tuple(sorted(containing_parameters))
        self.enumerating_parameters = tuple(sorted(enumerating_parameters))
        self.tiling = tiling
        super().__init__(
            tiling.obstructions, tiling.requirements, tiling.dimensions, simplify
        )

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

    def parameters_are_contradictory(self) -> bool:
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
            avoiding_parameter in contain_list
            for contain_list in len_one_cont_params
            for avoiding_parameter in self.avoiding_parameters
        ):
            return True
        return False

    @classmethod
    def empty_mappling(cls) -> "MappedTiling":
        """Returns the mappling with no parameters and base as the empty tiling"""
        return MappedTiling(Tiling.empty_tiling(), [], [], [])

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

    def get_parameters(self, obj: GriddedCayleyPerm) -> tuple[int, ...]:
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
        return self.tiling.is_empty() or self.parameters_are_contradictory()

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

    # dunder methods

    def __eq__(self, other: object) -> bool:
        """Check if two MappedTilings are equal."""
        if not isinstance(other, MappedTiling):
            return NotImplemented
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
            + "\nEnumerating parameters:\n"
            + "\nNew enumerating parameters list\n".join(
                ["\n".join([str(p) for p in ps]) for ps in self.enumerating_parameters]
            )
        )
