from mapplings import ParameterPlacement, MappedTiling, Parameter
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope_folder.strategies.row_column_separation import LessThanRowColSeparation


P = Parameter(Tiling([],[],(4,4)), RowColMap({0:0,1:0,2:0,3:0},{0:0,1:0,2:1,3:1}))

Q = Tiling([GriddedCayleyPerm(CayleyPermutation((0,1)),[(0,0),(0,1)])],[],(1,2))

P = P.back_map_obs_and_reqs(Q)
print(Q)
print(P)
Test = LessThanRowColSeparation(P.ghost)
for k in Test.row_col_separation():
    print(k.reduced_str())
    
print(Test.row_col_map.preimage_map()) #this can get us the rows and cols that need to be seperated in the parameter



# for i in range(4):
#     for j in range(4):
#         print('(',i, ',' ,j, ')' ,Test.map_cell((i,j)))

# print(Test.col_order)
# print(Test.row_order)