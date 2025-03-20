from mapplings import ParameterPlacement, MappedTiling, Parameter
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope_folder.strategies.row_column_separation import LessThanRowColSeparation


P = Parameter(Tiling([],[],(4,4)), RowColMap({0:0,1:0,2:0,3:0},{0:0,1:0,2:1,3:1}))

Q = Tiling([GriddedCayleyPerm(CayleyPermutation((0,1)),[(0,0),(0,1)])],[],(1,2))

P = P.back_map_obs_and_reqs(Q)

for k in LessThanRowColSeparation(P.ghost).row_col_separation():
    print(k)