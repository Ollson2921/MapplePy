from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from tilescope.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)
from cayley_permutations import CayleyPermutation

from gridded_cayley_permutations.row_col_map import RowColMap

from mapplings import MappedTiling, Parameter, LTRowColSeparationMT

gcp = GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 2)])
gcp2 = GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 3)])
gcp3 = GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 1), (0, 2)])
gcp4 = GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 1), (0, 3)])
# gcp1 = GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (2, 0)])

tiling = Tiling([gcp, gcp2, gcp3, gcp4], [], (1, 4))

all_prs = []
for row in range(1):
    for col in range(2):
        all_prs.append([GriddedCayleyPerm(CayleyPermutation([0]), [(row, col)])])

# print(mt)

param = Parameter(Tiling([], all_prs, (1, 2)), RowColMap({0: 0}, {0: 0, 1: 2}))
# print(param)
mt = MappedTiling(tiling, [param], [], [])

print(mt)
# print(
#     LTRowColSeparationMT(MappedTiling(Tiling([], [], (2, 2)), [], [], [])).expansions(
#         {0: 0, 1: 0, 2: 0, 3: 1, 4: 1}
#     )
# )  # should be {0: 3, 1: 2}


for newmt in LTRowColSeparationMT(mt).separate_base_tiling():
    print("new one")
    print(newmt)
