from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling, MTFactor, ParameterPlacement
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope_folder.strategies.factor import Factors

point = CayleyPermutation((0,))
cay = CayleyPermutation((0, 0))
asc2 = CayleyPermutation((0, 1))
des2 = CayleyPermutation((1, 0))
asc3 = CayleyPermutation((0, 1, 2))

Base = Tiling.from_vincular(CayleyPermutation((0,)),[]).delete_rows_and_columns([],[0])

G1 = Tiling.from_vincular(CayleyPermutation((0,2,1)),[1]).delete_rows_and_columns([],[0])
G2 = Tiling.from_vincular(CayleyPermutation((1,3,2,0)),[1]).delete_rows_and_columns([],[0])
G3 = Tiling.from_vincular(CayleyPermutation((1,0,3,2)),[2]).delete_rows_and_columns([],[0])
G4 = Tiling.from_vincular(CayleyPermutation((0,1,3,2)),[2]).delete_rows_and_columns([],[0])

A1 = Parameter(G1, RowColMap({0:0,1:1,2:2,3:2,4:2,5:2,6:2},{0:0,1:1,2:1,3:1,4:1,5:1}))
A2 = Parameter(G2, RowColMap({0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:1,8:2},{0:0,1:1,2:1,3:1,4:1,5:1,6:1,7:1}))
A3 = Parameter(G3, RowColMap({0:0,1:0,2:0,3:1,4:2,5:2,6:2,7:2,8:2},{0:0,1:1,2:1,3:1,4:1,5:1,6:1,7:1}))
A4 = Parameter(G4, RowColMap({0:0,1:1,2:2,3:2,4:2,5:2,6:2,7:2,8:2},{0:0,1:1,2:1,3:1,4:1,5:1,6:1,7:1}))

M1 = MappedTiling(Base,[],[[A2, A3 ,A1, A4]],[])

print(M1.remove_redundant_parameters())