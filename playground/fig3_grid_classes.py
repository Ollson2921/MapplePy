from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
import json

ghost1 = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 0), (1, 0)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(2, 1), (2, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(2, 0)]),
    ],
    [],
    (3, 2),
)

containing_params = (
    ParameterList((Parameter(ghost1, RowColMap({0: 0, 1: 0, 2: 0}, {0: 0, 1: 0})),)),
)
mappling1 = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)

# print(mappling1)


ghost2 = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(2, 3), (2, 3)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(3, 2), (3, 2)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(3, 0), (3, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(2, 1), (2, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 2)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 3)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 2)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 3)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(2, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(2, 2)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(3, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(3, 3)]),
    ],
    [],
    (4, 4),
)

containing_params = (
    ParameterList(
        (
            Parameter(
                ghost2, RowColMap({0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 0, 2: 0, 3: 0})
            ),
        )
    ),
)
mappling2 = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)

# print(mappling2)


ghost3 = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(1, 2), (1, 2)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 0), (1, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 2)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(2, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(2, 2)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(2, 1), (2, 1)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(2, 1), (2, 1)]),
    ],
    [],
    (3, 3),
)

containing_params = (
    ParameterList(
        (Parameter(ghost3, RowColMap({0: 0, 1: 0, 2: 0}, {0: 0, 1: 0, 2: 0})),)
    ),
)
mappling3 = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)

# print(mappling3)

"""Finding spec"""
# mappling = mappling2
# mt = 2

# from mapplings.cleaners import MTCleaner

# MTCleaner.global_debug_toggle(2)

# pack = MappedTileScopePack.point_placement(mappling)
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=True)

# spec = searcher.auto_search(status_update=30)
# spec.show()

# json_dict = spec.to_jsonable()
# json_str = json.dumps(json_dict)
# with open(f"fig_3_gc_{mt}.json", "w") as f:
#     f.write(json_str)

# new_spec = spec.expand_verified()
# new_spec.show()

# json_dict = new_spec.to_jsonable()
# json_str = json.dumps(json_dict)
# with open(f"fig_3_gc_{mt}_expanded.json", "w") as f:
#     f.write(json_str)

# new_spec.get_genf()
# spec_counts = [new_spec.count_objects_of_size(i) for i in range(10)]
# mappling_counts = [mappling.get_terms(i).total() for i in range(10)]
# print(spec_counts, "spec counts")
# print(mappling_counts, "mappling counts")

# new_spec.sanity_check()


"""Debudding 1"""
mt = MappedTiling(
    Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 2), (0, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
        ),
        ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),),
        (2, 3),
    ),
    ParameterList(frozenset()),
    (
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                            ),
                            (),
                            (3, 2),
                        ),
                        RowColMap({0: 0, 1: 1, 2: 1}, {0: 1, 1: 2}),
                    )
                }
            )
        ),
    ),
    (),
)

print(mt)

from mapplings.strategies.tilescope_strategies import (
    MapplingRequirementPlacementStrategy,
)

for out in MapplingRequirementPlacementStrategy(
    (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),), (0,), 0
).decomposition_function(mt):
    print(out)
    print(repr(out))
