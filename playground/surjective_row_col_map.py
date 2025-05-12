from mapplings import MappedTiling, Parameter, RowColMap
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation

gcp = GriddedCayleyPerm(CayleyPermutation([1, 2, 3]), [(0, 0), (0, 0), (1, 0)])

basetiling = Tiling(
    [],
    [],
    (2, 2),
)

ghost = Tiling([gcp], [], (2, 2))

rowcolmap = RowColMap({0: 1, 1: 1}, {0: 0, 1: 1})

param = Parameter(ghost, rowcolmap)

mappling = MappedTiling(basetiling, [param], [], [])

print(mappling)

for mapped_gcp in rowcolmap.preimage_of_gridded_cperm(gcp):
    print(mapped_gcp)
