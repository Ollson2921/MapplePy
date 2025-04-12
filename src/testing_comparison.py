from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling, MTFactor, ParameterPlacement, MTRequirementPlacement, MappedTileScopePack, MappedTileScope
from mapplings.MT_row_col_separation import MTRowColSeparation, MTRowColSeparation_EQ
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope_folder.strategies.factor import Factors
from tilescope_folder import TileScope, TileScopePack
from comb_spec_searcher.rule_db import RuleDBForest

point = CayleyPermutation((0,))
cay = CayleyPermutation((0, 0))
asc2 = CayleyPermutation((0, 1))
des2 = CayleyPermutation((1, 0))
asc3 = CayleyPermutation((0, 1, 2))

# Base = Tiling.from_vincular(point,[]).delete_rows_and_columns([],[0])
# Cayley_Base = Tiling([GriddedCayleyPerm(cay, [(0,0),(0,0)])],[],(0,0))

# G1 = Tiling.from_vincular(CayleyPermutation((0,2,1)),[1]).delete_rows_and_columns([],[0])
# G2 = Tiling.from_vincular(CayleyPermutation((1,3,2,0)),[1]).delete_rows_and_columns([],[0])
# G3 = Tiling.from_vincular(CayleyPermutation((1,0,3,2)),[2]).delete_rows_and_columns([],[0])
# G4 = Tiling.from_vincular(CayleyPermutation((0,1,3,2)),[2]).delete_rows_and_columns([],[0])

# A1 = Parameter(G1, RowColMap({0:0,1:1,2:2,3:2,4:2,5:2,6:2},{0:0,1:1,2:1,3:1,4:1,5:1}))
# A2 = Parameter(G2, RowColMap({0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:1,8:2},{0:0,1:1,2:1,3:1,4:1,5:1,6:1,7:1}))
# A3 = Parameter(G3, RowColMap({0:0,1:0,2:0,3:1,4:2,5:2,6:2,7:2,8:2},{0:0,1:1,2:1,3:1,4:1,5:1,6:1,7:1}))
# A4 = Parameter(G4, RowColMap({0:0,1:1,2:2,3:2,4:2,5:2,6:2,7:2,8:2},{0:0,1:1,2:1,3:1,4:1,5:1,6:1,7:1}))
# M1 = MappedTiling(Base,[A1,A2],[],[])

fix_rows = [
    GriddedCayleyPerm(point,[(0,1),]),
    GriddedCayleyPerm(point,[(0,3),]),
    GriddedCayleyPerm(point,[(0,5),]),
    GriddedCayleyPerm(point,[(2,1),]),
    GriddedCayleyPerm(point,[(2,3),]),
    GriddedCayleyPerm(point,[(2,5),]),
    GriddedCayleyPerm(point,[(6,1),]),
    GriddedCayleyPerm(point,[(6,3),]),
    GriddedCayleyPerm(point,[(6,5),]),
]

G = Tiling.from_vincular(CayleyPermutation((0,2,1)),[1,]).add_obstructions(fix_rows)
A = Parameter(G,RowColMap({0:0,1:0,2:0,3:0,4:0,5:0,6:0},{0:0,1:0,2:0,3:0,4:0,5:0,6:0}))
M0 = MappedTiling(Tiling([],[], (1,1)), [A], [], []).full_cleanup()

n=4
#### MANUAL CONSTRUCTION
# print("=============== ORIGINAL ===============")
# print(M0)
# print("Counts: ", M0.initial_conditions(n))
# print("=============== CELL INSERTION ===============")
# M0A = M0.add_obstructions_to_tiling([GriddedCayleyPerm(point,[(0,0),])]).reap_all_contradictions()
# M0C = M0.add_requirements_to_tiling([[GriddedCayleyPerm(point,[(0,0),])]]).reap_all_contradictions()
# print('------------ AVOIDS ------------')
# print(M0A)
# print('------------ CONTAINS ------------')
# print(M0C)
# print("Counts: ", M0A.initial_conditions(n), M0C.initial_conditions(n))
# M1 = MTRequirementPlacement(M0C).point_placement(M0C.tiling.requirements[0],(0,),4)[0].full_cleanup()
# print("=============== PLACED POINT ===============")
# print(M1)
# print("Counts: ", M1.initial_conditions(n))
# M2 = M1.remove_redundant_parameters()
# print("=============== REMOVED REDUNDANT PARAMETERS ===============")
# print(M2)
# print("Counts: ", M2.initial_conditions(n))
# print("=============== IL FACTORING ===============")
# i=0
# for factor in MTFactor(M2).make_factors(MTFactor(M2).find_IL_factor_cells()):
#     print('------------ FACTOR',i,'------------')
#     print(factor)
#     print("Counts: ", factor.initial_conditions(n))
#     i+=1



    
ruledb = RuleDBForest()
scope = MappedTileScope(
    M0, MappedTileScopePack.MTpoint_placement(M0), debug=True, ruledb=ruledb
)
spec = scope.auto_search()
print(spec)
spec.show()
for i in range(10):
    print(spec.count_objects_of_size(i))
print(spec.get_genf())




