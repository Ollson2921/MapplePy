from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
import json
from mapplings.cleaners import MTCleaner, ParamCleaner

MTCleaner.global_debug_toggle(2)
ParamCleaner.global_debug_toggle(2)

til = MappedTiling.from_vincular_with_obs(CayleyPermutation([2, 1, 3, 0]), [])
ghost = til.add_obstructions([GriddedCayleyPerm(CayleyPermutation([0]), [(2, 8)])])
avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(9)}, {i: 0 for i in range(9)}))
]
mappling = MappedTiling(
    Tiling(
        [
            GriddedCayleyPerm(
                CayleyPermutation([1, 2, 3, 0]), ((0, 0), (0, 0), (0, 0), (0, 0))
            ),
        ],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
pack = MappedTileScopePack.point_placement(mappling)
searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=True)

spec = searcher.auto_search(status_update=30)
spec.show()

spec.sanity_check()

# json_dict = spec.to_jsonable()
# json_str = json.dumps(json_dict)
# with open("hare_2_stack_sortable.json", "w") as f:
#     f.write(json_str)

# new_spec = spec.expand_verified()
# new_spec.show()

# json_dict = new_spec.to_jsonable()
# json_str = json.dumps(json_dict)
# with open("hare_2_stack_sortable_expanded.json", "w") as f:
#     f.write(json_str)

# new_spec.get_genf()
# print([new_spec.count_objects_of_size(i) for i in range(10)])
