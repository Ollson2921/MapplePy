from mapplings.algorithms.point_placement import MTRequirementPlacement, PointPlacement
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, ParameterList, Parameter
from gridded_cayley_permutations.row_col_map import RowColMap

"""Test for map_for_param_placed_point function for point placement"""
# ghost = Tiling(
#     [],
#     [],
#     (2, 2),
# )
# colmap = {0: 0, 1: 0}
# rowmap = {0: 0, 1: 0}
# param = Parameter(ghost, RowColMap(colmap, rowmap))
# bt = Tiling([], [], (2, 2))
# mt = MappedTiling(
#     bt,
#     ParameterList(frozenset()),
#     (ParameterList([param]),),
#     (),
# )
# placed_ghost = Tiling([], [], (4, 4))

# assert MTRequirementPlacement(mt).map_for_param_placed_point(
#     placed_ghost, (1, 1), param.map
# ) == RowColMap({0: 0, 1: 1, 2: 2, 3: 2}, {0: 0, 1: 1, 2: 2, 3: 2})

"""Test for map_for_param_unchanged function for point placement"""
# ghost = Tiling(
#     [],
#     [],
#     (2, 2),
# )
# colmap = {0: 1, 1: 1}
# rowmap = {0: 1, 1: 1}
# param = Parameter(ghost, RowColMap(colmap, rowmap))
# bt = Tiling([], [], (2, 2))
# mt = MappedTiling(
#     bt,
#     ParameterList(frozenset()),
#     (ParameterList([param]),),
#     (),
# )
# print(mt)
# placed_ghost = Tiling([], [], (2, 2))

# assert MTRequirementPlacement(mt).map_for_param_unchanged(param, (0, 0)) == RowColMap({0: 3, 1: 3}, {0: 3, 1: 3})

"""Test for unfuse_row function for point placement"""
# ghost = Tiling(
#     [],
#     [],
#     (2, 2),
# )
# colmap = {0: 1, 1: 1}
# rowmap = {0: 0, 1: 0}
# param = Parameter(ghost, RowColMap(colmap, rowmap))
# bt = Tiling([], [], (2, 2))
# mt = MappedTiling(
#     bt,
#     ParameterList(frozenset()),
#     (ParameterList([param]),),
#     (),
# )
# assert MTRequirementPlacement(mt).unfuse_row(param, 0) == Tiling(
#     (
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
#         GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
#         GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
#         GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
#     ),
#     (),
#     (2, 4),
# )

# assert MTRequirementPlacement(mt).unfuse_row(param, 1) == Tiling(
#     (
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
#         GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
#         GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
#         GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
#     ),
#     (),
#     (2, 4),
# )

"""Test for unfuse_cols_in_param"""
# ghost = Tiling(
#     [],
#     [],
#     (2, 2),
# )
# colmap = {0: 0, 1: 0}
# rowmap = {0: 1, 1: 1}
# param = Parameter(ghost, RowColMap(colmap, rowmap))
# bt = Tiling([], [], (2, 2))
# mt = MappedTiling(
#     bt,
#     ParameterList(frozenset()),
#     (ParameterList([param]),),
#     (),
# )
# print(mt)
# for new_param in MTRequirementPlacement(mt).unfuse_cols_in_param(param, (0, 0)):
#     print(repr(new_param))
# #  Parameter(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),))), (),(4, 2)), RowColMap({0: 0, 1: 1, 2: 2, 3: 2}, {0: 3, 1: 3}))
# # Parameter(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),))), (),(4, 2)), RowColMap({0: 0, 1: 0, 2: 1, 3: 2}, {0: 3, 1: 3}))


"""Test for unfuse_rows_in_param"""
# ghost = Tiling(
#     [],
#     [],
#     (2, 2),
# )
# colmap = {0: 1, 1: 1}
# rowmap = {0: 0, 1: 0}
# param = Parameter(ghost, RowColMap(colmap, rowmap))
# bt = Tiling([], [], (2, 2))
# mt = MappedTiling(
#     bt,
#     ParameterList(frozenset()),
#     (ParameterList([param]),),
#     (),
# )
# print(mt)
# for new_param in MTRequirementPlacement(mt).unfuse_rows_in_param(param, (0, 0)):
#     print(repr(new_param))
# Parameter(Tiling((GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1)))), (),(2, 4)), RowColMap({0: 3, 1: 3}, {0: 0, 1: 1, 2: 2, 3: 2}))
# Parameter(Tiling((GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2)))), (),(2, 4)), RowColMap({0: 3, 1: 3}, {0: 0, 1: 0, 2: 1, 3: 2}))

"""Test for point placement in a MappedTiling"""
ghost = Tiling(
    [],
    [],
    (2, 2),
)
colmap = {0: 1, 1: 1}
rowmap = {0: 0, 1: 0}
param1 = Parameter(ghost, RowColMap(colmap, rowmap))
colmap = {0: 1, 1: 1}
rowmap = {0: 1, 1: 1}
param2 = Parameter(ghost, RowColMap(colmap, rowmap))
colmap = {0: 0, 1: 0}
rowmap = {0: 0, 1: 0}
param3 = Parameter(ghost, RowColMap(colmap, rowmap))
colmap = {0: 0, 1: 0}
rowmap = {0: 1, 1: 1}
param4 = Parameter(ghost, RowColMap(colmap, rowmap))
colmap = {0: 0, 1: 1}
rowmap = {0: 0, 1: 1}
param5 = Parameter(ghost, RowColMap(colmap, rowmap))
bt = Tiling([], [], (2, 2))
mt = MappedTiling(
    bt,
    ParameterList([param2, param5]),
    (ParameterList([param1, param3]), ParameterList([param4])),
    (),
)
for mappling in MTRequirementPlacement(mt).point_placement(
    (GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),), (0,), 1
):
    print(mappling)
