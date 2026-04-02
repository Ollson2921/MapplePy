from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings import Parameter, MappedTiling, ParameterList
from gridded_cayley_permutations.point_placements import PointPlacement
from mapplings.cleaners.mappling_cleaner import MTCleaner


def test_removing_rows_cols_with_point_rows():
    """Parameter with lots of blank rows and columns intersected by a point
    placement. Mappling has the parameter as avoiding, containing and enumerating.
    Should not change the enumerating parameter."""

    ghost = PointPlacement(Tiling([], [], (6, 7))).point_placement_in_cell(
        [GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])], [0], 0, (0, 0)
    )
    param = Parameter(
        ghost,
        RowColMap(
            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0},
            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
        ),
    )
    mappling = MappedTiling(Tiling([], [], (1, 1)), [param], [[param]], [[param]])
    cleaned = MappedTiling(
        Tiling((), (), (1, 1)),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 1), (3, 1))
                                ),
                            ),
                            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),),
                            (4, 4),
                        ),
                        RowColMap({0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 0, 2: 0, 3: 0}),
                    )
                }
            )
        ),
        (
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 1), (3, 1))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 1),)
                                        ),
                                    ),
                                ),
                                (4, 4),
                            ),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 0, 2: 0, 3: 0}
                            ),
                        )
                    }
                )
            ),
        ),
        (
            [
                Parameter(
                    Tiling(
                        (
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 6),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 8),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (3, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (3, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((3, 1), (3, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((3, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((3, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((3, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((3, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((4, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((4, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((4, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((4, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((5, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((5, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((5, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((6, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((6, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((7, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (3, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (3, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((3, 1), (3, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((3, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((3, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((3, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((3, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((4, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((4, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((4, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((4, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((5, 1), (5, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((5, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((5, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((6, 1), (6, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((6, 1), (7, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((7, 1), (7, 1))
                            ),
                        ),
                        ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),),
                        (8, 9),
                    ),
                    RowColMap(
                        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0},
                        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
                    ),
                )
            ],
        ),
    )
    assert MTCleaner.remove_blank_rows_and_cols_params(mappling) == cleaned
