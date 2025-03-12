from mapplings import ParameterPlacement, MappedTiling, Parameter
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations.row_col_map import RowColMap

obs = [GriddedCayleyPerm(CayleyPermutation([0, 1, 2]), ((0, 0), (0, 0), (0, 0)))]
obs = []

base_tiling = Tiling(obs, [], (1, 1))

mesh_pattern = Tiling.from_vincular(CayleyPermutation((0, 1)), (0,))


P0 = Parameter(
    mesh_pattern,
    RowColMap(
        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
    ),
)

M0 = MappedTiling(base_tiling, [], [], [])


TT = Parameter(
    Tiling(
        [
            GriddedCayleyPerm(CayleyPermutation((0, 1)), [(0, 0), (0, 0)]),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), [(0, 0), (1, 0)]),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), [(1, 0), (1, 0)]),
        ],
        [],
        (3, 1),
    ),
    RowColMap({0: 0, 1: 0, 2: 0}, {0: 0}),
)

# print(TT)
# MT = MappedTiling(base_tiling, [TT], [], [])

# MT.avoiding_parameters[0] = MT.avoiding_parameters[0].reduce_by_fusion()

# print(MT)


print("=" * 150)


def fully_place_parameter(mappling: MappedTiling, param: Parameter, direction):
    """Places all points of a parameter (assumes parameter is not already in the containing parameter list, so we can pop eligable containing parameters when we find them). We can use this as a base for the strategy"""
    points_to_place = sorted(param.ghost.point_cells())
    new_mappling = MappedTiling(
        mappling.tiling,
        mappling.avoiding_parameters,
        [[param]] + mappling.containing_parameters,
        mappling.enumeration_parameters,
    )
    for i in range(len(points_to_place)):
        new_param = new_mappling.containing_parameters[0][0]
        temp_map = new_param.map
        cell = (
            temp_map.col_map[points_to_place[i][0]],
            temp_map.row_map[points_to_place[i][1]],
        )
        new_mappling = ParameterPlacement(
            new_mappling, new_param, cell
        ).param_placement(direction, i)
        yield new_mappling


new_mappling = list(fully_place_parameter(M0, P0, 3))[0].reduced_str()
print(new_mappling)
# print(P0)
# cell = (0, 0)
# output = ParameterPlacement(mappling, param, cell).param_placement(3, 0)
# output = MappedTiling(output.tiling, [], output.containing_parameters, [])
# print(output.reduced_str())
# m2 = output

# cell_in_param = ParameterPlacement(
#     mappling, param, cell
# ).cell_of_inserted_point_in_param(1)
# to_place = output.containing_parameters[0][0]
# cell = (
#     to_place.map.col_map[cell_in_param[0]],
#     to_place.map.row_map[cell_in_param[1]],
# )
# new_output = ParameterPlacement(output, to_place, cell).param_placement(3, 1)
# output = MappedTiling(output.tiling, [], output.containing_parameters, [])
# print(new_output.reduced_str())

# param = output.containing_parameters[0][0]
# cell_in_param = ParameterPlacement(output, param, cell).cell_of_inserted_point_in_param(
#     2
# )
# to_place = output.containing_parameters[0][0]
# cell = (
#     to_place.map.col_map[cell_in_param[0]],
#     to_place.map.row_map[cell_in_param[1]],
# )
# new_output = ParameterPlacement(output, to_place, cell).param_placement(3, 2)
# output = MappedTiling(output.tiling, [], output.containing_parameters, [])
# print(new_output.reduced_str())


# output = MappedTiling(output.tiling, [], output.containing_parameters, [])
# to_place = output.containing_parameters[0][0]
# new_output = ParameterPlacement(output, to_place, (2, 2)).param_placement(3, 1)
# print(new_output.reduced_str())

# new_output = MappedTiling(new_output.tiling, [], new_output.containing_parameters, [])
# cell = (4, 2)
# to_place = new_output.containing_parameters[0][0]
# last_point_placed = ParameterPlacement(new_output, to_place, cell).param_placement(3, 2)
# print(last_point_placed.reduced_str())

# remove_containing_param = (
#     last_point_placed.containing_parameters[0][0]
#     .back_map_obs_and_reqs(last_point_placed.tiling)
#     .ghost
# )
# final_mappling = MappedTiling(
#     remove_containing_param, last_point_placed.avoiding_parameters, [], []
# )
# print(final_mappling.reduced_str())

# # for n in range(1, 8):
# #     param_placed_count = output.get_terms(n)
# #     map_count = mappling.get_terms(n)
# #     print(map_count)
# #     print(param_placed_count)
# #     print("Are they equal?", map_count == param_placed_count)
