from mapplings import ParameterPlacement, MappedTiling, Parameter
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope_folder.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)
from mapplings.MT_row_col_separation import MTRowColSeparation, MTRowColSeparation_EQ
from mapplings.strategies import MTParamLessThanRowColSeparationStrategy

n = 5
Base = Tiling.from_vincular(CayleyPermutation((1, 0)), [])
P = Parameter(
    Base,
    RowColMap(
        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
        {0: 0, 1: 0, 2: 1, 3: 1, 4: 1},
    ),
)
Q = Tiling([GriddedCayleyPerm(CayleyPermutation((0, 1)), [(0, 0), (0, 1)])], [], (1, 2))
Q2 = (
    Parameter(Tiling([], [], (2, 2)), RowColMap({0: 0, 1: 0}, {0: 0, 1: 1}))
    .back_map_obs_and_reqs(Q)
    .ghost
)
M = MappedTiling(Q, [P], [], [])
print(M)
# print("Counts: ", M.initial_conditions(n))

# Test = MTRowColSeparation_EQ(M)
# for T in Test.separate_base_tiling():
#     print(T)
#     print("Counts: ", T.initial_conditions(n))

print(MTParamLessThanRowColSeparationStrategy().decomposition_function(M))
