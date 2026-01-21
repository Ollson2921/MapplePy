from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
from mapplings.cleaners import MTCleaner
from itertools import combinations_with_replacement

import json

# MTCleaner.DEBUG = 2


# # L1
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)

containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0, 1: 0})),)),
)
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)
pack = MappedTileScopePack.row_and_col_placement(mappling)
searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
spec = searcher.auto_search(status_update=30)
spec.show()

spec.sanity_check()

# json_dict = spec.to_jsonable()
# json_str = json.dumps(json_dict)
# with open("L1.json", "w") as f:
#     f.write(json_str)

# new_spec = spec.expand_verified()
# new_spec.show()

# json_dict = new_spec.to_jsonable()
# json_str = json.dumps(json_dict)
# with open("L1_expanded.json", "w") as f:
#     f.write(json_str)

# new_spec.get_genf()
# print([new_spec.count_objects_of_size(i) for i in range(10)])
