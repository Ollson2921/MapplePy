# import pytest
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies import MappedTileScopePack
from comb_spec_searcher import (
    CombinatorialSpecificationSearcher,
    CombinatorialSpecification,
)
import json

from mapplings.strategies.tilescope_strategies import (
    MapplingLessThanOrEqualRowColSeparationFactory,
)
from mapplings.algorithms.row_col_sep_mt import (
    MTLTRowColSeparation,
    MTLTORERowColSeparation,
)


mt = MappedTiling(
    Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (2, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
        ),
        ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),),),
        (3, 4),
    ),
    ParameterList(frozenset()),
    (
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 1))
                                ),
                            ),
                            (),
                            (3, 4),
                        ),
                        RowColMap({0: 0, 1: 0, 2: 2}, {0: 0, 1: 1, 2: 2, 3: 3}),
                    )
                }
            )
        ),
    ),
    (),
)
correct_output = MappedTiling(
    Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 3),)),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (3, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (3, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 0), (4, 0))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (3, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (3, 1))),
        ),
        ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),),),
        (5, 4),
    ),
    ParameterList(frozenset()),
    (
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 1))
                                ),
                            ),
                            (),
                            (5, 4),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 2, 3: 3, 4: 4}, {0: 0, 1: 1, 2: 2, 3: 3}
                        ),
                    )
                }
            )
        ),
    ),
    (),
)
print(mt)
# print(repr(set(MTLTRowColSeparation(mt).separate())))
for output in MTLTRowColSeparation(mt).separate():
    print(output)
    # assert output == correct_output


# til = Tiling(
#     (
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 2))),
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 2))),
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (1, 0))),
#         GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (1, 0))),
#         GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 1), (1, 1))),
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
#         GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 2), (1, 2))),
#         GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 2))),
#         GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 2))),
#     ),
#     (),
#     (2, 3),
# )

# param = Parameter(
#     Tiling([], [], (6, 7)),
#     RowColMap(
#         {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
#         {0: 0, 1: 0, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2},
#     ),
# )
# mt = MappedTiling(til, [param], [], [])
# print(mt)
# for output in MTLTRowColSeparation(mt).separate():
#     print(output)


til = Tiling(
    (
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (1, 0))),
        GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (1, 0))),
    ),
    (),
    (2, 1),
)

param = Parameter(
    Tiling([], [], (2, 3)),
    RowColMap(
        {0: 0, 1: 1},
        {0: 0, 1: 0, 2: 0},
    ),
)
mt = MappedTiling(til, [param], [], [])
print(mt)
for output in MTLTRowColSeparation(mt).separate():
    print(output)
