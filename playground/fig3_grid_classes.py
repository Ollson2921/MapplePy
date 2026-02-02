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

# pack = MappedTileScopePack.point_placement(mappling1)
# searcher = CombinatorialSpecificationSearcher(mappling1, pack, debug=False)

# spec = searcher.auto_search(status_update=30)
# spec.show()

# json_dict = spec.to_jsonable()
# json_str = json.dumps(json_dict)
# with open("fig_3_gc_1.json", "w") as f:
#     f.write(json_str)

# new_spec = spec.expand_verified()
# new_spec.show()

# json_dict = new_spec.to_jsonable()
# json_str = json.dumps(json_dict)
# with open("fig_3_gc_1_expanded.json", "w") as f:
#     f.write(json_str)

# new_spec.get_genf()
# spec_counts = [new_spec.count_objects_of_size(i) for i in range(10)]
# mappling_counts = [mappling1.get_terms(i).total() for i in range(10)]
# print(spec_counts, "spec counts")
# print(mappling_counts, "mappling counts")

# new_spec.sanity_check()


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

print(mappling2)


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

print(mappling3)
