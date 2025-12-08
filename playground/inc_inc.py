from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
import json

ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 0), (1, 0)]),
    ],
    [],
    (2, 1),
)


containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0})),)),
)
mappling = MappedTiling(
    Tiling(
        [],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)
pack = MappedTileScopePack.point_placement(mappling)
searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)

spec = searcher.auto_search(status_update=30)
spec.show()

json_dict = spec.to_jsonable()
json_str = json.dumps(json_dict)
with open("inc_inc.json", "w") as f:
    f.write(json_str)

new_spec = spec.expand_verified()
new_spec.show()

json_dict = new_spec.to_jsonable()
json_str = json.dumps(json_dict)
with open("inc_inc_expanded.json", "w") as f:
    f.write(json_str)

new_spec.get_genf()
print([new_spec.count_objects_of_size(i) for i in range(10)])

# pack = MappedTileScopePack.no_param_ver_point_placement()
# new_spec = spec.expand_comb_classes([13, 8], pack, True, True)
# new_spec.show()
# new_spec.get_genf()
# from mapplings.strategies.verification_strategy import NoParameterVerificationStrategy
# to_expand = []
# for rule in spec:
#     if isinstance(rule.strategy, NoParameterVerificationStrategy):
#         to_expand.append(rule.comb_class)

# new_spec = spec.expand_comb_classes(to_expand, True, True)
# new_spec.show()
# new_spec.get_genf()
