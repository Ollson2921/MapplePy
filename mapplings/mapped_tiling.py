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
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
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
        for c_list in self.containing_parameters:
            if all(param in self.avoiding_parameters for param in c_list):
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
        """Return the minimum size of gcps on the mappling
        (or a lower bound)."""
        assert not self.is_empty()
        working_minimum = self.tiling.minimum_size_of_object()
        for param_list in self.containing_parameters:
            param_list_min = min(param.minimum_size_of_object() for param in param_list)
            working_minimum = max(working_minimum, param_list_min)
        return working_minimum

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
        return (
            self.tiling.is_empty()
            or self.parameters_are_contradictory()
            or any(len(c_list) == 0 for c_list in self.containing_parameters)
        )

    # requirement insertion functions

    def add_obstructions(self, gcps) -> "MappedTiling":
        return MappedTiling(
            self.tiling.add_obstructions(gcps),
            self.avoiding_parameters,
            self.containing_parameters,
            self.enumerating_parameters,
        )

    def add_requirement_list(self, requirement_list) -> "MappedTiling":
        return MappedTiling(
            self.tiling.add_requirement_list(requirement_list),
            self.avoiding_parameters,
            self.containing_parameters,
            self.enumerating_parameters,
        )

    # other stuff
    def ace_parameters(
        self,
    ) -> tuple[ParameterList, Iterable[ParameterList], Iterable[ParameterList]]:
        """Returns the mappling's avoiding, containing, and enumerating parameters as a tuple"""
        return (
            self.avoiding_parameters,
            self.containing_parameters,
            self.enumerating_parameters,
        )

    def apply_to_all_parameters(
        self,
        func: Callable[[Parameter, *ArgsType], Parameter],
        additional_arguments: Union[tuple[*ArgsType], tuple] = tuple(),
    ) -> "MappedTiling":
        """Applies func to all parameters with additional arguments.
        Parameter must be the first argument of the function"""
        new_avoiders = ParameterList(
            self.avoiding_parameters.apply_to_all(func, additional_arguments)
        )
        new_containers = [
            ParameterList(c_list.apply_to_all(func, additional_arguments))
            for c_list in self.containing_parameters
        ]
        new_enumerators = [
            ParameterList(e_list.apply_to_all(func, additional_arguments))
            for e_list in self.enumerating_parameters
        ]
        return MappedTiling(self.tiling, new_avoiders, new_containers, new_enumerators)

    # html stuff
    def to_html_representation(self):
        """Create an HTML string representing the mappling"""
        base = super().to_html_representation()
        if self.avoiding_parameters:
            base += f'<br>{self.avoiding_parameters.html_dropdown("Avoiding Parameters", "red")}'
        for i, c_list in enumerate(self.containing_parameters):
            base += f'<br>{c_list.html_dropdown(f"Containing Parameters {i}", "blue")}'
        for i, e_list in enumerate(self.enumerating_parameters):
            base += (
                f'<br>{e_list.html_dropdown(f"Enumerating Parameters {i}", "green")}'
            )
        return base

    # json methods

    def to_jsonable(self) -> dict:
        d = super().to_jsonable()
        d["tiling"] = self.tiling.to_jsonable()
        d["avoiding_parameters"] = [
            param.to_jsonable() for param in self.avoiding_parameters
        ]
        d["containing_parameters"] = [
            param_list.to_jsonable() for param_list in self.containing_parameters
        ]
        d["enumerating_parameters"] = [
            param_list.to_jsonable() for param_list in self.enumerating_parameters
        ]
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "MappedTiling":
        """Construct a MappedTiling from a dictionary."""
        return MappedTiling(
            Tiling.from_dict(d["tiling"]),
            ParameterList(Parameter.from_dict(p) for p in d["avoiding_parameters"]),
            [ParameterList.from_dict(p) for p in d["containing_parameters"]],
            [ParameterList.from_dict(p) for p in d["enumerating_parameters"]],
        )

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
        string = "Base tiling: \n" + str(self.tiling)
        if self.avoiding_parameters:
            string += "\nAvoiding parameters:\n" + "\n".join(
                [str(p) for p in sorted(self.avoiding_parameters)]
            )
        if self.containing_parameters:
            string += (
                "\nContaining parameters:\n"
                + "\nNew containing parameters list \n".join(
                    [
                        "\n".join([str(p) for p in sorted(ps)])
                        for ps in self.containing_parameters
                    ]
                )
            )
        if self.enumerating_parameters:
            string += (
                "\nEnumerating parameters:\n"
                + "\nNew enumerating parameters list\n".join(
                    [
                        "\n".join([str(p) for p in sorted(ps)])
                        for ps in self.enumerating_parameters
                    ]
                )
            )
        return string
