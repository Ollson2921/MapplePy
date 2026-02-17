"""Module with the parameter list class."""

from typing import (
    Iterator,
    Callable,
    TypeVar,
    TypeVarTuple,
    Union,
    Iterable,
)
from itertools import chain, combinations, product

from gridded_cayley_permutations import Tiling, RowColMap
from gridded_cayley_permutations.simplify_obstructions_and_requirements import (
    SimplifyObstructionsAndRequirements as Simplify,
)

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
                for req_list in smaller.requirements:
                    if not Simplify.requirement_implied_by_some_requirement(
                        req_list, temp_bigger.requirements
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

    def remove_redundant(self) -> "ParameterList":
        """Returns self with redundant parameters removed"""
        return CompareParameters(self)()

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


class CompareParameters:
    """Used to check for redundant parameters"""

    def __init__(self, params: Iterable[Parameter]):
        self.params = ParameterList(params)
        self.redundant = set[Parameter]()
        self.find_redundant()

    def __call__(self) -> ParameterList:
        if len(self.params) < 2:
            return self.params
        return ParameterList(
            param for param in self.params if param not in self.redundant
        )

    @staticmethod
    def all_maps(
        param1: Parameter, param2: Parameter
    ) -> tuple[tuple[RowColMap, ...], tuple[RowColMap, ...]]:
        """Every way to map from one param to the other"""
        preimages1, preimages2 = param1.map.preimage_map(), param2.map.preimage_map()
        if param1.positive_cells():
            positive1 = tuple(map(set[int], zip(*param1.positive_cells())))
        else:
            positive1 = (set[int](), set[int]())
        if param2.positive_cells():
            positive2 = tuple(map(set[int], zip(*param2.positive_cells())))
        else:
            positive2 = (set[int](), set[int]())

        point_indices1 = param1.point_cols, param1.point_rows
        point_indices2 = param2.point_cols, param2.point_rows

        def make_maps(
            row_maps: bool,
        ) -> tuple[tuple[dict[int, int], ...], tuple[dict[int, int], ...]]:
            all_sections1, all_sections2 = (
                list[set[tuple[tuple[int, int], ...]]](),
                list[set[tuple[tuple[int, int], ...]]](),
            )
            for image in set(preimages1[row_maps].keys()) & set(
                preimages2[row_maps].keys()
            ):
                maxes = max(preimages1[row_maps][image]), max(
                    preimages2[row_maps][image]
                )
                mins = min(preimages1[row_maps][image]), min(
                    preimages2[row_maps][image]
                )
                force_extremal = (
                    [i in point_indices1[row_maps] for i in (mins[0], maxes[0])],
                    [i in point_indices2[row_maps] for i in (maxes[1], mins[1])],
                )
                check_positive = (
                    set(preimages1[row_maps][image]) & positive1[row_maps],
                    set(preimages2[row_maps][image]) & positive2[row_maps],
                )
                section_maps1, section_maps2 = (
                    set[tuple[tuple[int, int], ...]](),
                    set[tuple[tuple[int, int], ...]](),
                )
                if len(preimages1[row_maps][image]) > len(preimages2[row_maps][image]):
                    for indices in combinations(
                        preimages1[row_maps][image], len(preimages2[row_maps][image])
                    ):
                        if force_extremal[1][0] and mins[0] not in indices:
                            continue
                        if force_extremal[1][1] and maxes[0] not in indices:
                            continue

                        if not check_positive[0].issubset(indices):
                            continue
                        section_maps1.add(
                            tuple(zip(indices, preimages2[row_maps][image]))
                        )
                        section_maps2.add(
                            tuple(zip(preimages2[row_maps][image], indices))
                        )
                else:
                    for indices in combinations(
                        preimages2[row_maps][image], len(preimages1[row_maps][image])
                    ):
                        if force_extremal[0][0] and mins[1] not in indices:
                            continue
                        if force_extremal[0][1] and maxes[1] not in indices:
                            continue
                        if not check_positive[1].issubset(indices):
                            continue
                        section_maps2.add(
                            tuple(zip(indices, preimages1[row_maps][image]))
                        )
                        section_maps1.add(
                            tuple(zip(preimages1[row_maps][image], indices))
                        )
                all_sections1.append(section_maps1)
                all_sections2.append(section_maps2)
            return tuple(
                dict(chain(*tuples)) for tuples in product(*all_sections1)
            ), tuple(dict(chain(*tuples)) for tuples in product(*all_sections2))

        col_maps = make_maps(False)
        row_maps = make_maps(True)
        return tuple(
            RowColMap(*maps) for maps in product(col_maps[0], row_maps[0])
        ), tuple(RowColMap(*maps) for maps in product(col_maps[1], row_maps[1]))

    @staticmethod
    def redundancy_check(param1: Parameter, param2: Parameter):
        """Returns true if param1 implies param2"""
        positive_images1 = {
            (param1.col_map[x], param1.row_map[y]) for x, y in param1.positive_cells()
        }
        positive_images2 = {
            (param2.col_map[x], param2.row_map[y]) for x, y in param2.positive_cells()
        }
        intersection = param1.image_cells() & param2.image_cells()
        if not (
            positive_images1.issubset(intersection)
            and positive_images2.issubset(intersection)
        ):
            return False
        maps = CompareParameters.all_maps(param1, param2)[0]
        req_free2 = Tiling(param2.obstructions, [], param2.dimensions)

        def _check(temp_map: RowColMap) -> bool:
            temp_param = Parameter(param1.ghost, temp_map)
            backwards_map = RowColMap(
                {val: key for key, val in temp_map.col_map.items()},
                {val: key for key, val in temp_map.row_map.items()},
            )
            if any(
                req_free2.gcp_in_tiling(
                    temp_param.map.map_gridded_cperm(
                        ob.sub_gridded_cayley_perm(backwards_map.image_cells)
                    )
                )
                for ob in temp_param.obstructions
            ):
                return False
            for req_list in temp_param.requirements:
                temp_req_list = [
                    req
                    for req in req_list
                    if set(req.positions).issubset(backwards_map.image_cells)
                ]
                if not temp_req_list:
                    return False
                if not Simplify.requirement_implied_by_some_requirement(
                    temp_param.map.map_gridded_cperms(temp_req_list),
                    param2.requirements,
                ):
                    return False
            return True

        for temp_map in maps:
            if _check(temp_map):
                return True
        return False

    def find_redundant(self) -> None:
        """Finds all redundant parameters in the list"""
        for p1, p2 in combinations(self.params, 2):
            if {p1, p2} & self.redundant:
                continue
            if self.redundancy_check(p1, p2):
                self.redundant.add(p1)
                continue
            if self.redundancy_check(p2, p1):
                self.redundant.add(p2)
