from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from mapplings.cleaners import MTCleaner, ParamCleaner
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher

from mapplings.strategies.tilescope_strategies import (
    MapplingCellInsertionFactory,
    MapplingPointPlacementFactory,
    CleaningStrategy,
    MapplingFactorStrategy,
    MapplingLessThanOrEqualRowColSeparationStrategy,
    MapplingLessThanRowColSeparationStrategy,
)

cleaner = MTCleaner.make_full_cleaner()

til = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 1, 2]), [])
ghost = til.delete_rows([4])
avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(7)}, {i: 0 for i in range(6)}))
]
mappling = MappedTiling(
    Tiling(
        [
            GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), [(0, 0), (0, 0)]),
        ],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
mappling = MTCleaner.list_cleanup(mappling, MTCleaner.reg.registered_functions)
pack = MappedTileScopePack.point_placement(mappling)
searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)

spec = searcher.auto_search(status_update=10)
print(spec.count_objects_of_size(5))
spec.show()

M0 = cleaner(mappling)
print(M0)

print("------------------ Cell Insertion ------------------")
rule0 = list(MapplingCellInsertionFactory()(M0))[0](M0)
print(rule0.sanity_check(5))
M1 = rule0.children[1]
print(M1)

print("------------------ Placed Rightmost ------------------")
rule1 = list(MapplingPointPlacementFactory()(M1))[0](M1)
print(rule1.sanity_check(5))
M2 = rule1.children[1]
M3 = cleaner(M2)
print(M3)


print("------------------ Factored ------------------")

rule2 = MapplingFactorStrategy()(M3)
print(rule2.sanity_check(5))
M4 = cleaner(rule2.children[0])

print(M4)
print("------------------ RC Seperation ------------------")
rule3 = MapplingLessThanRowColSeparationStrategy()(M4)
print(rule3.sanity_check(5))
M5 = rule3.children[0]

M6 = cleaner(M5)
print(M6)
print("------------------ Factored ------------------")
rule4 = MapplingFactorStrategy()(M6)
print(rule4.sanity_check(5))
M7 = rule4.children[1]
print(M7)
M7 = cleaner(M7)
print("------------------ Cell Insertion ------------------")
rule5 = list(MapplingCellInsertionFactory()(M7))[0](M7)
print(rule5.sanity_check(5))
M8 = rule5.children[1]
print(M8)

print("------------------ Placed Top-Rightmost ------------------")
rule6 = list(MapplingPointPlacementFactory()(M8))[1](M8)
print(rule6.sanity_check(5))
M9 = rule6.children[1]
M10 = cleaner(M9)
print(cleaner(M10))
print("------------------ Factored ------------------")
rule7 = MapplingFactorStrategy()(M10)
print(rule7.sanity_check(5))
M11 = rule7.children[1]
M12 = cleaner(M11)
print(M12)
print(M12 == M0)
