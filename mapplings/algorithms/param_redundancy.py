from typing import Iterable
from itertools import chain, combinations, product
from gridded_cayley_permutations import Tiling, RowColMap
from gridded_cayley_permutations.simplify_obstructions_and_requirements import (
    SimplifyObstructionsAndRequirements as Simplify,
)

from mapplings import ParameterList, Parameter


class CompareParameters:
    """Used to check for redundant parameters"""

    def __init__(self, params: Iterable[Parameter]):
        self.params = ParameterList(params)
        self.redundant = set[Parameter]()
        self.find_redundant()

    def __call__(self) -> ParameterList:
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
            if any(
                req_free2.gcp_in_tiling(temp_param.map.map_gridded_cperm(ob))
                for ob in temp_param.obstructions
            ):
                print("NO", temp_param.map)
                return False
            for req_list in temp_param.requirements:
                if not Simplify.requirement_implied_by_some_requirement(
                    temp_param.map.map_gridded_cperms(req_list), param2.requirements
                ):
                    print("NO", temp_param.map)
                    return False
            print("Yes?", temp_param.map)
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
