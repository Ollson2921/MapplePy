"""Module with the parameter list class."""

from typing import (
    Iterator,
    Callable,
    TypeVar,
    TypeVarTuple,
    Union,
)
from itertools import chain, combinations

from gridded_cayley_permutations import Tiling

from .parameter import Parameter


Cell = tuple[int, int]

FuncTypeT = TypeVar("FuncTypeT")
ArgsType = TypeVarTuple("ArgsType")

OPEN_DISPLAY = "open"  # Change to "open" for fully expanded html trees


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

    def remove_contradictions(self, tiling: Tiling) -> "ParameterList":
        """Removes any contradictory ghosts from the parameter list."""
        return ParameterList(
            param for param in self if not param.is_contradictory(tiling)
        )

    def remove_empty(self) -> "ParameterList":
        """Removes parameters with empty ghost"""
        return ParameterList(param for param in self if not param.is_empty())

    def simple_remove_redundant(self, reverse: bool = False) -> "ParameterList":
        """Removes any parameter implied by another through a basic check"""
        exclude = set[Parameter]()

        def match_reverse(smaller: Parameter, bigger: Parameter) -> None:
            if reverse:
                exclude.add(smaller)
            else:
                exclude.add(bigger)

        def compare(smaller: Parameter, bigger: Parameter) -> bool:
            temp_bigger = bigger.sub_parameter(
                bigger.map.preimage_of_cells(smaller.image_cells())
            )
            if len(bigger.requirements) != len(temp_bigger.requirements):
                return False

            if smaller.map != temp_bigger.map:
                return False
            if not reverse:
                if any(smaller.gcp_in_tiling(ob) for ob in temp_bigger.obstructions):
                    return False
                for req_list in temp_bigger.requirements:
                    # any req list that doesnt have any req implied by all reqs of a small req list
                    if all(
                        all(
                            any(small_req.avoids([req]) for small_req in small_list)
                            for small_list in smaller.requirements
                        )
                        for req in req_list
                    ):
                        return False
                return True
            if any(temp_bigger.gcp_in_tiling(ob) for ob in smaller.obstructions):
                return False
            for req_list in smaller.requirements:
                # any req list that doesnt have any req implied by all reqs of a small req list
                if all(
                    all(
                        any(big_req.avoids([req]) for big_req in big_list)
                        for big_list in temp_bigger.requirements
                    )
                    for req in req_list
                ):
                    return False
            return True

        for param0, param1 in combinations(self, 2):
            if {param0, param1} & exclude:
                continue
            image_cells = param0.image_cells(), param1.image_cells()
            if image_cells[0] == image_cells[1]:
                if compare(param0, param1):
                    match_reverse(param0, param1)
                elif compare(param1, param0):
                    match_reverse(param1, param0)

            elif image_cells[0].issubset(image_cells[1]):
                if compare(param0, param1):
                    match_reverse(param0, param1)

            elif image_cells[1].issubset(image_cells[0]):
                if compare(param1, param0):
                    match_reverse(param1, param0)

        return ParameterList(param for param in self if param not in exclude)

    def to_html(self) -> str:
        """Returns a html of all parameters in self seperated by a line"""
        return "<br>".join((param.to_html_representation() for param in sorted(self)))

    def html_dropdown(self, label: str, border_color: str = "grey") -> str:
        """Makes a cute html dropdown for the parameter list"""
        style = f"""
            border : 1px solid;
            border-color : {border_color};
            background-color : white;
            padding-left : 5px;
            padding-right : 29px;
            """
        return (
            f'<details {OPEN_DISPLAY} style = "{style}"><summary>{label}</summary>'
            + f"<br>{self.to_html()}</details>"
        )

    def to_jsonable(self) -> dict:
        """Dictionary version of self for json serialization."""
        return {"params": [param.to_jsonable() for param in self]}

    @classmethod
    def from_dict(cls, d: dict):
        """Constructs a ParameterList from a dictionary."""
        return cls(Parameter.from_dict(p) for p in d["params"])

    def __repr__(self):
        return self.__class__.__name__ + f"({frozenset(self)})"

    def __le__(self, other: object):
        if isinstance(other, ParameterList):
            return tuple(sorted(self)) <= tuple(sorted(other))
        return NotImplemented

    def __lt__(self, other: object):
        if isinstance(other, ParameterList):
            return tuple(sorted(self)) < tuple(sorted(other))
        return NotImplemented
