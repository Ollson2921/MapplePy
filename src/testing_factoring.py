from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling, MTFactor, ParameterPlacement
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope_folder.strategies.factor import Factors

base_obs = [
    GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((0, 0), (0, 0), (0, 0))),
    GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((0, 1), (0, 1), (0, 1))),
    GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((1, 0), (1, 0), (1, 0))),
    GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((1, 1), (1, 1), (1, 1))),
    GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((2, 0), (2, 0), (2, 0))),
    GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((2, 1), (2, 1), (2, 1))),
]

point_obs = [
    GriddedCayleyPerm(CayleyPermutation([0]), ((0, 1),)),
    GriddedCayleyPerm(CayleyPermutation([0]), ((1, 0),)),
    GriddedCayleyPerm(CayleyPermutation([0]), ((2, 0),)),
]

base_tiling = Tiling(
    base_obs + point_obs,
    [[GriddedCayleyPerm(CayleyPermutation((0,)), [(2, 1)])]],
    (3, 2),
)
# print(base_tiling)

extra_obs = [
    GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((3, 0), (3, 0), (3, 0))),
    GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((3, 1), (3, 1), (3, 1))),
]
ghost_tiling = Tiling(
    base_obs + extra_obs,
    [[GriddedCayleyPerm(CayleyPermutation([0]), ((3, 1),))]],
    (4, 2),
)

# print(ghost_tiling)

P3 = Parameter(base_tiling, RowColMap({0: 0, 1: 1, 2: 2}, {0: 0, 1: 1}))

P1 = Parameter(
    ghost_tiling.add_obstructions(
        [
            # GriddedCayleyPerm(CayleyPermutation([0]), ((0, 1),)),
            GriddedCayleyPerm(CayleyPermutation([0]), ((1, 0),)),
            # GriddedCayleyPerm(CayleyPermutation([0]), ((0, 1),)),
            GriddedCayleyPerm(CayleyPermutation([0]), ((2, 0),)),
            GriddedCayleyPerm(CayleyPermutation([0]), ((3, 0),)),
        ]
    ).add_requirement_list([GriddedCayleyPerm(CayleyPermutation([0]), ((0, 1),))]),
    RowColMap({0: 0, 1: 1, 2: 1, 3: 2}, {0: 0, 1: 1}),
)
P2 = Parameter(
    ghost_tiling.add_obstructions(
        [
            GriddedCayleyPerm(CayleyPermutation([0]), ((0, 1),)),
            GriddedCayleyPerm(CayleyPermutation([0]), ((1, 0),)),
            # GriddedCayleyPerm(CayleyPermutation([0]), ((1, 1),)),
            GriddedCayleyPerm(CayleyPermutation([0]), ((2, 0),)),
            GriddedCayleyPerm(CayleyPermutation([0]), ((3, 0),)),
        ]
    ),
    RowColMap({0: 0, 1: 0, 2: 1, 3: 2}, {0: 0, 1: 1}),
)


M = MappedTiling(base_tiling, [P1, P2], [], [])
# M = MappedTiling(base_tiling, [P2, P1], [], [])
M = MappedTiling(base_tiling, [P3], [], [])
# M.reap_contradictory_ghosts()
# print(M)
# print("FACTORS:")

# for factor in MTFactor(M).find_factors():
#    print("-------------------------------------")
#    print(factor)
# print(base_tiling.sub_tiling(factor))
# print(M.find_factors())

# print(MTFactor(M).is_factorable2(MTFactor(M).find_factor_cells()))


point = CayleyPermutation((0,))
cay = CayleyPermutation((0, 0))
asc2 = CayleyPermutation((0, 1))
des2 = CayleyPermutation((1, 0))
asc3 = CayleyPermutation((0, 1, 2))
obstructions = [
    GriddedCayleyPerm(point, ((0, 0),)),
    GriddedCayleyPerm(point, ((0, 2),)),
    GriddedCayleyPerm(point, ((2, 0),)),
    GriddedCayleyPerm(point, ((2, 2),)),
    GriddedCayleyPerm(point, ((4, 4),))
]

requirements = [
    [GriddedCayleyPerm(point, ((1, 1),))],
    [GriddedCayleyPerm(point, ((3, 3),))],
]

T1 = Tiling.from_vincular(CayleyPermutation((0,1)),[]).add_obstructions(obstructions)
temp = Tiling([GriddedCayleyPerm(cay, ((0, 0), (0, 0)))], [], (1, 1))


P0 = Parameter(
    T1, RowColMap({0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, {0: 0, 1: 0, 2: 0, 3: 0, 4: 0})
)
#P0 = P0.back_map_obs_and_reqs(temp)

T1 = P0.ghost

# print(T1)

new_obstructions = [
    GriddedCayleyPerm(point, ((4, 0),)),
    GriddedCayleyPerm(point, ((4, 2),)),
    GriddedCayleyPerm(point, ((4, 3),)),
    GriddedCayleyPerm(point, ((5, 0),)),
    GriddedCayleyPerm(point, ((5, 2),)),
    GriddedCayleyPerm(point, ((5, 4),)),
    GriddedCayleyPerm(point, ((6, 3),)),
    GriddedCayleyPerm(point, ((6, 4),)),
    GriddedCayleyPerm(des2, ((5, 3), (5, 3))),
    GriddedCayleyPerm(asc2, ((5, 3), (5, 3))),
    GriddedCayleyPerm(cay, ((5, 3), (5, 3))),
]
new_requirements = [[GriddedCayleyPerm(point, ((5, 3),))]]

P1 = Parameter(
    Tiling(new_obstructions, new_requirements, (7, 7)),
    RowColMap(
        {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4},
        {0: 0, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 4},
    ),
)
P1 = P1.back_map_obs_and_reqs(T1)
# print(P1.ghost)

P2 = Parameter(
    Tiling(
        [GriddedCayleyPerm(point, ((5, 6),)), GriddedCayleyPerm(point, ((7, 6),))],
        [],
        (9, 9),
    ),
    RowColMap({4: 0, 5: 1, 6: 2, 7: 3, 8: 4}, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4}),
)
P2 = Parameter(
    P2.back_map_obs_and_reqs(T1).ghost,
    RowColMap(
        {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4},
        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 2, 7: 3, 8: 4},
    ),
)
P2 = P2.back_map_obs_and_reqs(T1)
# print(P2.ghost)

T0 = Tiling(
    [
        GriddedCayleyPerm(asc3, ((0, 0), (0, 0), (0, 0))),
        GriddedCayleyPerm(cay, ((0, 0), (0, 0))),
    ],
    [[GriddedCayleyPerm(point, ((0, 0),))]],
    (1, 1),
)

M0 = MappedTiling(
    T0,
    [],
    [],
    [],
)

M1 = MappedTiling(T0, [], [[P0]], [])


def fully_place_parameter(mappling: MappedTiling, param: Parameter, direction):
    """Places all points of a parameter (assumes parameter is not already in the
    containing parameter list, so we can pop eligable containing parameters
    when we find them). We can use this as a base for the strategy"""
    new_mappling = MappedTiling(
        mappling.tiling,
        mappling.avoiding_parameters,
        [[param]] + mappling.containing_parameters,
        mappling.enumeration_parameters,
    )
    for i in range(len(param.ghost.point_cells())):
        new_param = new_mappling.containing_parameters[0][0]
        temp_map = new_param.map
        points_to_place = sorted(new_param.ghost.point_cells())
        cell = (
            temp_map.col_map[points_to_place[i][0]],
            temp_map.row_map[points_to_place[i][1]],
        )
        new_mappling = (
            ParameterPlacement(new_mappling, new_param, cell)
            .param_placement(direction, i)
            .reduce_empty_rows_and_cols_in_parameters()
            .full_cleanup()
        )
        yield new_mappling


des3 = CayleyPermutation((2, 1, 0))
IL_TEST = Tiling(
    [
        GriddedCayleyPerm(point, [(0, 0)]),
        GriddedCayleyPerm(point, [(0, 1)]),
        GriddedCayleyPerm(point, [(1, 0)]),
        GriddedCayleyPerm(point, [(2, 1)]),
        GriddedCayleyPerm(point, [(1, 2)]),
        GriddedCayleyPerm(point, [(0, 2)]),
        GriddedCayleyPerm(asc2, [(1, 1), (1, 1)]),
        GriddedCayleyPerm(des2, [(1, 1), (1, 1)]),
        GriddedCayleyPerm(cay, [(1, 1), (1, 1)]),
        GriddedCayleyPerm(des3, [(2, 0), (2, 0), (2, 0)]),
        GriddedCayleyPerm(des3, [(2, 2), (2, 2), (2, 2)]),
    ],
    [[GriddedCayleyPerm(point, [(1, 1)])]],
    (3, 3),
)


n = 7  # how far to check counts
print("====================Initial Mappling====================")
print(M1.reduced_str())
#print("Counts: ", M1.initial_conditions(n))

print("====================Start Parameter Placement====================")
param_placement = list(fully_place_parameter(M0, P0, 4))
print("++++ First Point Placed ++++")
print(param_placement[0].reduced_str())
#print("Counts: ", param_placement[0].initial_conditions(n))

print("++++ Second Point Placed ++++")
print(param_placement[1].reduced_str())
#print("Counts: ", param_placement[1].initial_conditions(n))

print("====================Start Factoring====================")
i = 0
for factor in MTFactor(param_placement[-1]).find_factors():
    print("----- Factor:", i)
    i += 1
    print(factor.reduced_str())
    #print("Counts: ", factor.initial_conditions(n))
