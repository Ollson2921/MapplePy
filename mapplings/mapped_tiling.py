from typing import Iterable, Tuple, List, DefaultDict
from collections import defaultdict
from comb_spec_searcher import CombinatorialClass

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm

from .parameter import Parameter

Objects = DefaultDict[Tuple[int, ...], List[GriddedCayleyPerm]]


class MappedTiling(CombinatorialClass):
    def __init__(
        self,
        tiling: Tiling,
        avoiding_parameters: Iterable[Parameter],
        containing_parameters: Iterable[Iterable[Parameter]],
        enumeration_parameters: Iterable[Iterable[Parameter]],
    ):
        self.avoiding_parameters = avoiding_parameters
        self.containing_parameters = containing_parameters
        self.enumeration_parameters = enumeration_parameters
        self.tiling = tiling

    ## Combintatorial class stuff ##

    def has_parameters(self) -> bool:
        """Check if the tiling has avoiding or containing parameters
        (doesn't check for enumeration parameters)."""
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

    def objects_of_size(self, n, **parameters) -> Iterable[GriddedCayleyPerm]:
        """Return gridded Cayley permutations of size n in the tiling."""
        for val in self.get_objects(n).values():
            for gcp in val:
                yield gcp

    def get_objects(self, n: int) -> Objects:
        """Return the objects of size n in the tiling."""
        objects = defaultdict(list)
        for gcp in self.tiling.objects_of_size(n):
            if self.gcp_in_tiling(gcp):
                param = self.get_parameters(gcp)
                objects[param].append(gcp)
        return objects

    def get_parameters(self, gcp: GriddedCayleyPerm) -> Tuple[int, ...]:
        """Parameters are not what you think!!! This is specific to combinatorical class parameters"""
        all_lists = []
        for param_list in self.enumeration_parameters:
            all_lists.append(
                sum(1 for _ in param.preimage_of_gcp(gcp)) for param in param_list
            )
        return tuple(all_lists)

    def gcp_in_tiling(self, gcp: GriddedCayleyPerm) -> bool:
        """Returns True if the gridded cayley permutation is in the tiling"""
        return self.gcp_satisfies_containing_params(
            gcp
        ) and self.gcp_satisfies_avoiding_params(gcp)

    def gcp_satisfies_avoiding_params(self, gcp: GriddedCayleyPerm) -> bool:
        """Returns True if the gridded cayley permutation satisfies the avoiding parameters"""
        return not any(
            any(True for _ in param.preimage_of_gcp(gcp))
            for param in self.avoiding_parameters
        )

    def gcp_satisfies_containing_params(self, gcp: GriddedCayleyPerm) -> bool:
        """Returns True if the gridded cayley permutation satisfies the containing parameters"""
        return all(
            any(any(True for _ in param.preimage_of_gcp(gcp)) for param in params)
            for params in self.containing_parameters
        )

    def are_contradictory_parameters(self) -> bool:
        """Returns True if there is a contradiction between the avoiding and
        containing parameters - if a len 1 containing parameter list is the
        same as an avoiding parameter.
        TODO: add more checks for contradictory parameters."""
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

    def is_empty(self) -> bool:
        """Assume this is run after all cleanup functions have been applied.

        Returns True if the tiling is empty or there is a contradiction between
        containing and avoiding parameters.
        TODO: Are there any other times when a mapped tiling is empty?"""
        return self.tiling.is_empty() or self.are_contradictory_parameters()

    def __eq__(self, other) -> bool:
        """Check if two MappedTilings are equal."""
        return (
            self.tiling == other.tiling
            and sorted(tuple(self.avoiding_parameters))
            == sorted(tuple(other.avoiding_parameters))
            and sorted(tuple(self.containing_parameters))
            == sorted(tuple(other.containing_parameters))
            and sorted(tuple(self.enumeration_parameters))
            == sorted(tuple(other.enumeration_parameters))
        )

    def __hash__(self) -> int:
        """Hash the MappedTiling."""
        return hash(
            (
                self.tiling,
                tuple(sorted(self.avoiding_parameters)),
                tuple(
                    sorted(tuple(sorted(clist)) for clist in self.containing_parameters)
                ),
                tuple(
                    sorted(
                        tuple(sorted(elist)) for elist in self.enumeration_parameters
                    )
                ),
            )
        )

    def from_dict(self, d: dict) -> "MappedTiling":
        """Construct a MappedTiling from a dictionary."""
        return MappedTiling(
            Tiling.from_dict(d["tiling"]),
            [Parameter.from_dict(p) for p in d["avoiding_parameters"]],
            [[Parameter.from_dict(p) for p in ps] for ps in d["containing_parameters"]],
            [
                [Parameter.from_dict(p) for p in ps]
                for ps in d["enumeration_parameters"]
            ],
        )

    def __repr__(self) -> str:
        """The repr for the MappedTiling."""
        return (
            self.__class__.__name__
            + f"({repr(self.tiling)}, {repr(self.avoiding_parameters)}, "
            + f"{repr(self.containing_parameters)}, {repr(self.enumeration_parameters)})"
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
            + "\nEnumeration parameters:\n"
            + "\nNew enumeration parameters list\n".join(
                ["\n".join([str(p) for p in ps]) for ps in self.enumeration_parameters]
            )
        )
