from mapplings import ParameterPlacement, MappedTiling, Parameter
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope_folder.strategies.row_column_separation import LessThanRowColSeparation, LessThanOrEqualRowColSeparation


P = Parameter(Tiling([],[],(2,2)), RowColMap({0:0,1:0},{0:0,1:1}))

Q = Tiling([GriddedCayleyPerm(CayleyPermutation((0,1)),[(0,0),(0,1)])],[],(1,2))

P = P.back_map_obs_and_reqs(Q)
print(Q)
print(P)
Test = LessThanOrEqualRowColSeparation(P.ghost)
for k in Test.row_col_separation():
    for z in LessThanOrEqualRowColSeparation(k).row_col_separation():
        print(z)

# for k in Test.inequalities_sets():
#     print(k)
print(Test.row_col_map.preimage_map()) # this can get us the rows and cols that need to be seperated in the parameter