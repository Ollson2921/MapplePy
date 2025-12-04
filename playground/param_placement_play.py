from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from mapplings.algorithms import ParameterPlacement
from mapplings.cleaners import MTCleaner
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
from comb_spec_searcher.rule_db import RuleDBForest

ghost = Tiling.from_vincular_with_obs(CayleyPermutation((0,)), [])
ghost = ghost.add_obstructions(
    (
        GriddedCayleyPerm((0,), [(0, 2)]),
        GriddedCayleyPerm((0,), [(2, 0)]),
        GriddedCayleyPerm((0,), [(0, 1)]),
        GriddedCayleyPerm((0,), [(2, 1)]),
    )
)
P = Parameter(ghost, RowColMap({0: 0, 1: 0, 2: 0}, {0: 0, 1: 0, 2: 0}))
B = Tiling([GriddedCayleyPerm((0, 0), [(0, 0), (0, 0)])], [], (1, 1))
ruledb = RuleDBForest()
c_list = ParameterList([P])
mappling = MappedTiling(B, [P], [], [])
mappling = MTCleaner.full_cleanup(mappling)
pack = MappedTileScopePack.parameter_tomfoolery(None)
searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=True, ruledb=ruledb)

spec = searcher.auto_search(
    status_update=10,
)
spec.show()
