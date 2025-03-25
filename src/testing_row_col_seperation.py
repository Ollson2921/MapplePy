from mapplings import ParameterPlacement, MappedTiling, Parameter
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope_folder.strategies.row_column_separation import LessThanRowColSeparation, LessThanOrEqualRowColSeparation
from mapplings.MT_row_col_separation import MTRowColSeperation, MTRowColSeperation_EQ

Base = Tiling.from_vincular(CayleyPermutation((2,1,0)),[0])
print(Base)
P = Parameter(Base, RowColMap({0:0,1:0,2:0,3:0,4:1,5:1,6:1},{0:0,1:0,2:1,3:1,4:1,5:1,6:1}))

Q = Tiling([GriddedCayleyPerm(CayleyPermutation((0,1)),[(0,0),(0,1)])],[],(1,2))
Q2 = Parameter(Tiling([],[],(2,2)),RowColMap({0:0,1:0},{0:0,1:1})).back_map_obs_and_reqs(Q).ghost

M = MappedTiling(Q2,[P],[],[])

Test = MTRowColSeperation(M)
for T in Test.separate_base_tiling():
    print(T)
