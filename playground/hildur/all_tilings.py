from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm, RowColMap
from mapplings import MappedTiling, Parameter, ParameterList

til = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 1, 2]), [])
ghost = til.delete_rows([4])
avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(7)}, {i: 0 for i in range(6)}))
]
motzkin = MappedTiling(
    Tiling(
        [
            GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), [(0, 0), (0, 0)]),
        ],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)

ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 0), (1, 0)]),
    ],
    [],
    (2, 1),
)


containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0})),)),
)
inc_inc = MappedTiling(
    Tiling(
        [],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)

ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)


containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0, 1: 0})),)),
)
l0 = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)

ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)

containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0, 1: 0})),)),
)
l1 = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)

ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)

containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0, 1: 0})),)),
)
l3 = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)


containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0, 1: 0})),)),
)
l4 = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)

containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0, 1: 0})),)),
)
l5 = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)

containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0, 1: 0})),)),
)
l7 = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)
til = MappedTiling.from_vincular_with_obs(CayleyPermutation([2, 1, 3, 0]), [])
ghost = til.add_obstructions([GriddedCayleyPerm(CayleyPermutation([0]), [(2, 8)])])
avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(9)}, {i: 0 for i in range(9)}))
]
hare_2_stack = MappedTiling(
    Tiling(
        [
            GriddedCayleyPerm(
                CayleyPermutation([1, 2, 3, 0]), ((0, 0), (0, 0), (0, 0), (0, 0))
            ),
        ],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
til = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 1, 2]), [])
ghost = til.delete_columns([2])
til2 = MappedTiling.from_vincular_with_obs(CayleyPermutation([0, 2, 1]), [])
ghost2 = til.delete_rows([4])
avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost2, RowColMap({i: 0 for i in range(7)}, {i: 0 for i in range(6)})),
]
ten_point_one = MappedTiling(
    Tiling(
        [
            GriddedCayleyPerm(CayleyPermutation((0, 0)), [(0, 0), (0, 0)]),
        ],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)

L_classes = [l0, l1, l3, l4, l5, l7]
all_other_mapplings = [motzkin, inc_inc, hare_2_stack, ten_point_one]


# from comb_spec_searcher import CombinatorialSpecification
# import json

# with open("from_table_7_point_place.json", "r") as f:
#     load_dict = eval(f.readline())
# spec = CombinatorialSpecification.from_dict(load_dict)
# spec.show()
# for n in range(10):
#     print(spec.count_objects_of_size(n))
