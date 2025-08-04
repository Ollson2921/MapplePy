from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.algorithms.row_col_sep_mt import LTRowColSeparationMT

tiling = Tiling(
    [GriddedCayleyPerm(CayleyPermutation([0, 1]), ((0, 0), (0, 1)))], [], (1, 2)
)

ghost = Tiling(
    [],
    [
        [GriddedCayleyPerm(CayleyPermutation([0]), ((0, 0),))],
        [GriddedCayleyPerm(CayleyPermutation([1]), ((1, 1),))],
    ],
    (2, 2),
)
row_col_map = RowColMap({0: 0, 1: 0}, {0: 0, 1: 1})
param = Parameter(ghost, row_col_map)
mapped_tiling = MappedTiling(tiling, [param], [], [])


print(LTRowColSeparationMT(mapped_tiling).separate())
