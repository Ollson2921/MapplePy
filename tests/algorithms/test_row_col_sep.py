from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.algorithms.row_col_sep_mt import (
    MTLTRowColSeparation,
    MTLTORERowColSeparation,
)


def test_ltore_orders():
    """Check that not allowing new gcps which were not consistent before."""
    bt = Tiling(
        (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (1, 0))),),
        (),
        (2, 2),
    )

    ghost = Tiling(
        (GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),),
        (),
        (2, 5),
    )
    param = Parameter(ghost, RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 2: 0, 3: 1, 4: 1}))
    mt = MappedTiling(bt, ParameterList(frozenset({param})), (), ())
    all_separated = list(MTLTORERowColSeparation(mt).separate())
    output = [
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                ),
                (),
                (2, 4),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                                    ),
                                ),
                                (),
                                (2, 7),
                            ),
                            RowColMap(
                                {0: 0, 1: 1}, {0: 0, 1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3}
                            ),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                ),
                                (),
                                (2, 7),
                            ),
                            RowColMap(
                                {0: 0, 1: 1}, {0: 0, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3}
                            ),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (0, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (0, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 3))
                                    ),
                                ),
                                (),
                                (2, 7),
                            ),
                            RowColMap(
                                {0: 0, 1: 1}, {0: 0, 1: 0, 2: 0, 3: 1, 4: 2, 5: 3, 6: 3}
                            ),
                        ),
                    }
                )
            ),
            (),
            (),
        ),
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                ),
                (
                    (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                    (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                ),
                (2, 4),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                                    ),
                                ),
                                (),
                                (2, 7),
                            ),
                            RowColMap(
                                {0: 0, 1: 1}, {0: 0, 1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3}
                            ),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                ),
                                (),
                                (2, 7),
                            ),
                            RowColMap(
                                {0: 0, 1: 1}, {0: 0, 1: 1, 2: 2, 3: 2, 4: 2, 5: 3, 6: 3}
                            ),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (0, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (0, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 3))
                                    ),
                                ),
                                (),
                                (2, 7),
                            ),
                            RowColMap(
                                {0: 0, 1: 1}, {0: 0, 1: 0, 2: 0, 3: 1, 4: 2, 5: 3, 6: 3}
                            ),
                        ),
                    }
                )
            ),
            (),
            (),
        ),
    ]

    assert all_separated == output


def test_less_than_row_col_separation():
    """Test less than row col separation for mapplings."""
    mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 3))),
            ),
            (),
            (1, 4),
        ),
        ParameterList(
            [
                Parameter(
                    Tiling(
                        (),
                        (
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                        ),
                        (1, 2),
                    ),
                    RowColMap({0: 0}, {0: 0, 1: 2}),
                )
            ]
        ),
        ParameterList([]),
        ParameterList([]),
    )

    separated_mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
            ),
            (),
            (2, 4),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 1),)
                                    ),
                                ),
                            ),
                            (2, 2),
                        ),
                        RowColMap({0: 0, 1: 1}, {0: 0, 1: 2}),
                    )
                }
            )
        ),
        (),
        (),
    )

    all_separated = list(MTLTRowColSeparation(mt).separate())
    assert len(all_separated) == 1
    assert all_separated[0] == separated_mt


def test_less_than_row_col_separation_rows():
    """Test less than row col separation for mapplings."""
    mt = MappedTiling(
        Tiling(
            (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 1))),),
            (),
            (1, 2),
        ),
        ParameterList(
            [
                Parameter(
                    Tiling(
                        (),
                        (
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                        ),
                        (2, 2),
                    ),
                    RowColMap({0: 0, 1: 0}, {0: 0, 1: 1}),
                )
            ]
        ),
        ParameterList([]),
        ParameterList([]),
    )

    separated_mt = {
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                ),
                (),
                (2, 2),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 0),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 1),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 0),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 1),)
                                        ),
                                    ),
                                ),
                                (3, 2),
                            ),
                            RowColMap({0: 0, 1: 1, 2: 1}, {0: 0, 1: 1}),
                        ),
                        Parameter(
                            Tiling(
                                (),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 1),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 0),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 1),)
                                        ),
                                    ),
                                ),
                                (3, 2),
                            ),
                            RowColMap({0: 0, 1: 0, 2: 1}, {0: 0, 1: 1}),
                        ),
                    }
                )
            ),
            (),
            (),
        )
    }

    assert set(MTLTRowColSeparation(mt).separate()) == separated_mt


def test_relative_order_active_cells_rows():
    """Test that the relative order of active cells is preserved
    in a parameter after row separation."""
    mt = MappedTiling(
        Tiling(
            (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 1))),),
            (),
            (1, 2),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 0),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1,)), ((1, 1),)
                                    ),
                                ),
                            ),
                            (2, 2),
                        ),
                        RowColMap({0: 0, 1: 0}, {0: 0, 1: 1}),
                    )
                }
            )
        ),
        (),
        (),
    )

    separation = {
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                ),
                (),
                (2, 2),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((2, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((2, 1),)
                                        ),
                                    ),
                                ),
                                (3, 2),
                            ),
                            RowColMap({0: 0, 1: 0, 2: 1}, {0: 0, 1: 1}),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (1, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 0), (1, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((2, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (1, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (1, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 0),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((2, 1),)
                                        ),
                                    ),
                                ),
                                (3, 2),
                            ),
                            RowColMap({0: 0, 1: 1, 2: 1}, {0: 0, 1: 1}),
                        ),
                    }
                )
            ),
            (),
            (),
        )
    }

    assert set(MTLTRowColSeparation(mt).separate()) == separation


def test_relative_order_active_cells_cols():
    """Test that the relative order of active cells is preserved
    in a parameter after column separation."""
    mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (1, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (1, 0))),
            ),
            (),
            (2, 1),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 0),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1,)), ((1, 1),)
                                    ),
                                ),
                            ),
                            (2, 2),
                        ),
                        RowColMap({0: 0, 1: 1}, {0: 0, 1: 0}),
                    )
                }
            )
        ),
        (),
        (),
    )

    separated = {
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                ),
                (),
                (2, 2),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 2),)
                                        ),
                                    ),
                                ),
                                (2, 3),
                            ),
                            RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 2: 1}),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 1),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 2),)
                                        ),
                                    ),
                                ),
                                (2, 3),
                            ),
                            RowColMap({0: 0, 1: 1}, {0: 0, 1: 1, 2: 1}),
                        ),
                    }
                )
            ),
            (),
            (),
        )
    }

    assert set(MTLTRowColSeparation(mt).separate()) == separated


def test_relative_order_cols_LORE():
    """Test that the relative order of active cells is preserved
    in a parameter after less than or equal to col separation."""
    mt = MappedTiling(
        Tiling(
            (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (1, 0))),),
            (),
            (2, 1),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 0),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1,)), ((1, 1),)
                                    ),
                                ),
                            ),
                            (2, 2),
                        ),
                        RowColMap({0: 0, 1: 1}, {0: 0, 1: 0}),
                    )
                }
            )
        ),
        (),
        (),
    )

    separation = {
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                ),
                (
                    (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                    (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                ),
                (2, 3),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 3))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 3),)
                                        ),
                                    ),
                                ),
                                (2, 4),
                            ),
                            RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 2: 1, 3: 2}),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 3))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 2),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 3),)
                                        ),
                                    ),
                                ),
                                (2, 4),
                            ),
                            RowColMap({0: 0, 1: 1}, {0: 0, 1: 1, 2: 2, 3: 2}),
                        ),
                    }
                )
            ),
            (),
            (),
        ),
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                ),
                (),
                (2, 3),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 3))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 3),)
                                        ),
                                    ),
                                ),
                                (2, 4),
                            ),
                            RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 2: 1, 3: 2}),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 3))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 2),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 3),)
                                        ),
                                    ),
                                ),
                                (2, 4),
                            ),
                            RowColMap({0: 0, 1: 1}, {0: 0, 1: 1, 2: 2, 3: 2}),
                        ),
                    }
                )
            ),
            (),
            (),
        ),
    }

    assert set(MTLTORERowColSeparation(mt).separate()) == separation


def test_double_expansion_param():
    """This mappling has two row separations and a column separation. When separating the
    avoiding parameter, the cell map was wrong and moved the rows up twice for the top
    expansion. Now it looks at the difference in the number of rows instead."""
    mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (2, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 2, 1)), ((0, 0), (0, 0), (0, 0))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 2, 1)), ((2, 0), (2, 0), (2, 0))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 2, 1)), ((2, 0), (2, 2), (2, 0))
                ),
            ),
            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),),
            (3, 3),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 5),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 4),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 5),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 6),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((6, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((6, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((6, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((6, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((6, 5),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((6, 6),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 3), (0, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 4), (0, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (5, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (5, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (6, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 1), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 3), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 3), (5, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 4), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 4), (5, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 4), (6, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 3), (5, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((5, 1), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((5, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((5, 3), (5, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((5, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((5, 4), (5, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((5, 4), (6, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((5, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((6, 4), (6, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((6, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((7, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((7, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((7, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 3), (0, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 3), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 3), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 3), (5, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 4), (0, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 4), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 4), (5, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 4), (6, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 3), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 3), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 3), (5, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (5, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (6, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 1), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 3), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 3), (5, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 4), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 4), (5, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 4), (6, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (5, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 1), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 3), (5, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 4), (5, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 4), (6, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((6, 4), (6, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((6, 4), (7, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 3), (7, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 4), (7, 4))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 1),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((4, 3),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((6, 4),)
                                    ),
                                ),
                            ),
                            (8, 7),
                        ),
                        RowColMap(
                            {0: 0, 1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2},
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 2},
                        ),
                    )
                }
            )
        ),
        (),
        (),
    )
    separation = {
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 3), (0, 3))),
                    GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 0), (3, 0))),
                    GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 4), (3, 4))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 3))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 4), (3, 4))),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 2, 1)), ((1, 1), (1, 1), (1, 1))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 2, 1)), ((3, 0), (3, 0), (3, 0))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 2, 1)), ((3, 0), (3, 4), (3, 0))
                    ),
                ),
                ((GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),),),
                (4, 5),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 4),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 5),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 6),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 7),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 8),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 4),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 5),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 6),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 7),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 8),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 5),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 6),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 7),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 8),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (0, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (0, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (0, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 4), (0, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 4), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 4), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 4), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 3), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 3), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 4), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 4), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 3), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 4), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((8, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((8, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((8, 4), (8, 4))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 1),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((5, 3),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((7, 4),)
                                        ),
                                    ),
                                ),
                                (9, 9),
                            ),
                            RowColMap(
                                {0: 0, 1: 1, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3},
                                {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 3, 8: 4},
                            ),
                        )
                    }
                )
            ),
            (),
            (),
        )
    }

    assert set(MTLTRowColSeparation(mt).separate()) == separation


def test_expand_3_rows():
    """Test expanding 3 rows of a MappedTiling"""
    til = Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (1, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (1, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 2))),
        ),
        (),
        (2, 3),
    )

    param = Parameter(
        Tiling([], [], (6, 7)),
        RowColMap(
            {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
            {0: 0, 1: 0, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2},
        ),
    )
    mt = MappedTiling(til, [param], [], [])

    separated = {
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 4))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (1, 5))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 5))),
                ),
                (),
                (2, 6),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 0,
                                    2: 1,
                                    3: 2,
                                    4: 3,
                                    5: 3,
                                    6: 3,
                                    7: 4,
                                    8: 5,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 0,
                                    2: 1,
                                    3: 2,
                                    4: 2,
                                    5: 2,
                                    6: 3,
                                    7: 4,
                                    8: 5,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 1,
                                    2: 1,
                                    3: 2,
                                    4: 3,
                                    5: 3,
                                    6: 3,
                                    7: 4,
                                    8: 4,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 0,
                                    2: 1,
                                    3: 2,
                                    4: 3,
                                    5: 3,
                                    6: 3,
                                    7: 4,
                                    8: 4,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 1,
                                    2: 1,
                                    3: 2,
                                    4: 3,
                                    5: 3,
                                    6: 3,
                                    7: 4,
                                    8: 5,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 0,
                                    2: 1,
                                    3: 2,
                                    4: 2,
                                    5: 2,
                                    6: 3,
                                    7: 4,
                                    8: 4,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 1,
                                    2: 1,
                                    3: 2,
                                    4: 2,
                                    5: 3,
                                    6: 3,
                                    7: 4,
                                    8: 4,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 1,
                                    2: 1,
                                    3: 2,
                                    4: 2,
                                    5: 3,
                                    6: 3,
                                    7: 4,
                                    8: 5,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 1,
                                    2: 1,
                                    3: 2,
                                    4: 2,
                                    5: 2,
                                    6: 3,
                                    7: 4,
                                    8: 5,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 1,
                                    2: 1,
                                    3: 2,
                                    4: 2,
                                    5: 2,
                                    6: 3,
                                    7: 4,
                                    8: 4,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 0,
                                    2: 1,
                                    3: 2,
                                    4: 2,
                                    5: 3,
                                    6: 3,
                                    7: 4,
                                    8: 4,
                                    9: 5,
                                },
                            ),
                        ),
                        Parameter(
                            Tiling((), (), (6, 10)),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 0,
                                    2: 1,
                                    3: 2,
                                    4: 2,
                                    5: 3,
                                    6: 3,
                                    7: 4,
                                    8: 5,
                                    9: 5,
                                },
                            ),
                        ),
                    }
                )
            ),
            (),
            (),
        )
    }

    assert set(MTLTRowColSeparation(mt).separate()) == separated


def test_double_column_expansion():
    """Base tiling has a column which expands into two columns,
    check parameter map adjusts correctly."""
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
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 2),)
                                    ),
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
    correct_output = {
        MappedTiling(
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
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 2),)
                                        ),
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
                                    {0: 0, 1: 0, 2: 2, 3: 3, 4: 4},
                                    {0: 0, 1: 1, 2: 2, 3: 3},
                                ),
                            )
                        }
                    )
                ),
            ),
            (),
        )
    }
    assert correct_output == set(MTLTRowColSeparation(mt).separate())
