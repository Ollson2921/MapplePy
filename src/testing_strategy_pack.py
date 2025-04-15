from mapplings import MappedTiling, Parameter, MappedTileScopePack, MappedTileScope
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling, RowColMap
from tilescope_folder import TileScope, TileScopePack
from comb_spec_searcher.rule_db import RuleDBForest


basis = "00"

basis_patterns = [CayleyPermutation.standardise(p) for p in basis.split("_")]

rules = []
tiling = Tiling(
    [GriddedCayleyPerm(p, [(0, 0) for _ in p]) for p in basis_patterns],
    [],
    (1, 1),
)

ghost = Tiling.from_vincular(CayleyPermutation((0, 1, 2)), [1])
parameter = Parameter(
    ghost,
    RowColMap(
        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
    ),
)
#parameter = parameter.back_map_obs_and_reqs(tiling)

mt = MappedTiling(tiling, [parameter], [], [])




ruledb = RuleDBForest()
scope = MappedTileScope(
    mt, MappedTileScopePack.MTpoint_placement(mt), debug=False, ruledb=ruledb
)
spec = scope.auto_search()
print(spec)
spec.show()
for i in range(10):
    print(spec.count_objects_of_size(i))
print(spec.get_genf())
