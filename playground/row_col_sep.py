from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from tilescope.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)
from cayley_permutations import CayleyPermutation

from gridded_cayley_permutations.row_col_map import RowColMap

from mapplings import MappedTiling, Parameter, LTRowColSeparationMT


tiling = Tiling([], [], (2, 2))

mt = MappedTiling(Tiling([], [], (2, 2)), [], [], [])

print(mt)

param = Parameter(
    Tiling([], [], (3, 3)), RowColMap({0: 0, 1: 1, 2: 1}, {0: 0, 1: 1, 2: 1})
)
print(param)

# print(
#     LTRowColSeparationMT(MappedTiling(Tiling([], [], (2, 2)), [], [], [])).expansions(
#         {0: 0, 1: 0, 2: 0, 3: 1, 4: 1}
#     )
# )  # should be {0: 3, 1: 2}


print(LTRowColSeparationMT(mt).map_param(param))
