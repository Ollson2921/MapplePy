from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.tilescope_strategies import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher

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
new_spec = spec.expand_verified()
new_spec.show()

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