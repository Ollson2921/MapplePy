from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.algorithms.row_col_sep_mt import (
    MTLTRowColSeparation,
    MTLTORERowColSeparation,
)


def test_3_rows_param():
    """Three rows in a parameter map to one separating row in the base tiling."""
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

    output = {
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
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 3), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 4), (1, 2))
                                    ),
                                ),
                                (),
                                (2, 6),
                            ),
                            RowColMap(
                                {0: 0, 1: 1}, {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1}
                            ),
                        )
                    }
                )
            ),
            (),
            (),
        )
    }

    assert set(MTLTRowColSeparation(mt).separate()) == output


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


def test_relative_order_cols_LTORE():
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
                                        CayleyPermutation((0,)), ((0, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (0, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (1, 1))
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
                                            CayleyPermutation((0,)), ((0, 2),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1,)), ((1, 3),)
                                        ),
                                    ),
                                ),
                                (2, 4),
                            ),
                            RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 2: 1, 3: 1}),
                        )
                    }
                )
            ),
            (),
            (),
        )
    }

    assert set(MTLTRowColSeparation(mt).separate()) == separated


def test_multiple_expansions():
    """Double, triple, then double row expansions in parameter."""
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

    separation = {
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
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (2, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (3, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (5, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (1, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (2, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (3, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 6), (5, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 11), (1, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 11), (2, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 11), (3, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 11), (4, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 11), (5, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (2, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (3, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (5, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 6), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 6), (2, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 6), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 6), (3, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 6), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 6), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 6), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 6), (5, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 11), (2, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 11), (3, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 11), (4, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 11), (5, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (3, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (5, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 6), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 6), (3, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 6), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 6), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 6), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 6), (5, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 11), (3, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 11), (4, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 11), (5, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (5, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 5), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 5), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 6), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 6), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 6), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 6), (5, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 11), (4, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 11), (5, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (5, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 6), (5, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 6), (5, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 11), (5, 12))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 2), (5, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (1, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (1, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (3, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (3, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (5, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (1, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (3, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 12), (1, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 12), (2, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 12), (3, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 12), (4, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 12), (5, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (5, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (3, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (3, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (5, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (3, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 12), (2, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 12), (3, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 12), (4, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 12), (5, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 2), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 2), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 2), (5, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (3, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (3, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (5, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (3, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 12), (3, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 12), (4, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 12), (5, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 2), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 2), (5, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (5, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 8), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 8), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 12), (4, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 12), (5, 11))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 2), (5, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (5, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 8), (5, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 12), (5, 11))
                                    ),
                                ),
                                (),
                                (6, 14),
                            ),
                            RowColMap(
                                {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1},
                                {
                                    0: 0,
                                    1: 0,
                                    2: 1,
                                    3: 1,
                                    4: 2,
                                    5: 2,
                                    6: 2,
                                    7: 3,
                                    8: 3,
                                    9: 3,
                                    10: 4,
                                    11: 4,
                                    12: 5,
                                    13: 5,
                                },
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
                                        CayleyPermutation((0,)), ((3, 8),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 9),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 10),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 11),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 12),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 13),)
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
                                        CayleyPermutation((0,)), ((5, 10),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 11),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 12),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((5, 13),)
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
                                        CayleyPermutation((0,)), ((7, 9),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 11),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 12),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 13),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (1, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 2), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (0, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (0, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (1, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (1, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (1, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (2, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 3), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (0, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (0, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (1, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (1, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (1, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (1, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (2, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (2, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 4), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (1, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (1, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (1, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (1, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (2, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (2, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (2, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 5), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 7), (0, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 7), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 9), (0, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 9), (1, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 10), (0, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 10), (1, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 2), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (1, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (2, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 3), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (1, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (2, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (2, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 4), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (2, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (2, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (2, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (2, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 5), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 7), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 9), (1, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 10), (1, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 1), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 2), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 2), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 2), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 2), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 2), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 2), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 2), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (2, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 3), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (2, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 4), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (4, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 5), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 7), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 7), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 7), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 9), (2, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 9), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 9), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 10), (2, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 10), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 10), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 10), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (4, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 7), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 7), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 1), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 2), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 2), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 2), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 2), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 3), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 4), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 5), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 7), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 9), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 9), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 10), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 10), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((4, 10), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (6, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (6, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 3), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 9), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((5, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 1), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 1), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 1), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 1), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 2), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 2), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 3), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 3), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 3), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 3), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 3), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 3), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 4), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 5), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 5), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 5), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 5), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 5), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 5), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 10), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((6, 10), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (8, 6))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (8, 8))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 4), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((7, 10), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 1), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 1), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 3), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 3), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 4), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((8, 10), (8, 10))
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
                                        CayleyPermutation((1, 0)), ((0, 6), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (1, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (2, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (6, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 6), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (0, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (1, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (1, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (2, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (6, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (1, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 8), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (0, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (0, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (1, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (1, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (2, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (0, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (0, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (1, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (1, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (2, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 10), (8, 10))
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
                                        CayleyPermutation((1, 0)), ((1, 6), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (2, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (6, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 6), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (1, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (2, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (6, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 8), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (1, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (1, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (2, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (1, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (1, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (2, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (2, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 10), (8, 10))
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
                                        CayleyPermutation((1, 0)), ((2, 6), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (6, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 6), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (2, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (6, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 8), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (2, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (2, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (2, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (2, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 10), (8, 10))
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
                                        CayleyPermutation((1, 0)), ((3, 7), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (3, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (4, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (6, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 7), (8, 7))
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
                                        CayleyPermutation((1, 0)), ((4, 6), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (6, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 6), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (4, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (6, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 8), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 8), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 8), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 8), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 8), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 8), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 8), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 8), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (4, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (4, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (4, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (4, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 10), (8, 10))
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
                                        CayleyPermutation((1, 0)), ((5, 9), (5, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (5, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (6, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((5, 9), (8, 9))
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
                                        CayleyPermutation((1, 0)), ((6, 6), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 6), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 6), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 6), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 6), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 6), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 7), (6, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 7), (6, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 7), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 7), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 7), (8, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 7), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 7), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 7), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 8), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 8), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 8), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 8), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 9), (6, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 9), (6, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 9), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 9), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 9), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 9), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 10), (6, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 10), (6, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 10), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 10), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 10), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((6, 10), (8, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 4), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 4), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 10), (7, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 10), (7, 10))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 10), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 10), (8, 5))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 10), (8, 10))
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
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((8, 7), (8, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((8, 7), (8, 7))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((8, 9), (8, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((8, 9), (8, 9))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((8, 10), (8, 4))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((8, 10), (8, 10))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 7),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((5, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((5, 9),)
                                        ),
                                    ),
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((7, 4),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((7, 10),)
                                        ),
                                    ),
                                ),
                                (9, 14),
                            ),
                            RowColMap(
                                {0: 0, 1: 1, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3},
                                {
                                    0: 0,
                                    1: 0,
                                    2: 0,
                                    3: 0,
                                    4: 0,
                                    5: 0,
                                    6: 1,
                                    7: 1,
                                    8: 1,
                                    9: 1,
                                    10: 1,
                                    11: 1,
                                    12: 3,
                                    13: 4,
                                },
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
