from mapplings import MappedTiling, Parameter, RowColMap
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation

basetiling = Tiling(
    [GriddedCayleyPerm(CayleyPermutation([1, 2, 3]), [(1, 0), (1, 0), (1, 0)])],
    [],
    (2, 2),
)

ghost = Tiling([], [], (2, 2))

rowcolmap = RowColMap({0: 1, 1: 1}, {0: 0, 1: 1})

param = Parameter(ghost, rowcolmap)

mappling = MappedTiling(basetiling, [param], [], [])

print(mappling)

print(
    rowcolmap._product_of_cols(
        GriddedCayleyPerm(CayleyPermutation([1, 2, 3]), [(0, 0), (0, 0), (0, 0)])
    )
)

# for gcp in rowcolmap.preimage_of_gridded_cperm(
#     GriddedCayleyPerm(CayleyPermutation([1, 2, 3]), [(0, 0), (0, 0), (0, 0)])
# ):
#     print(gcp)
