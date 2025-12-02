from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.algorithms.row_col_sep_mt import (
    LTRowColSeparationMT,
    LTORERowColSeparationMT,
)


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
            [
                Parameter(
                    Tiling(
                        (),
                        (
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),),
                        ),
                        (2, 2),
                    ),
                    RowColMap({0: 0, 1: 1}, {0: 0, 1: 2}),
                )
            ]
        ),
        ParameterList([]),
        ParameterList([]),
    )

    all_separated = list(LTRowColSeparationMT(mt).separate())
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

    separated_mt = MappedTiling(
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
                            (GriddedCayleyPerm(CayleyPermutation(()), ()),), (), (0, 0)
                        ),
                        RowColMap({}, {}),
                    )
                }
            )
        ),
        (),
        (),
    )

    for mappling in LTRowColSeparationMT(mt).separate():
        assert mappling == separated_mt


def test_less_than__or_equal_row_col_separation_cols():
    """Test less than row col or equal separation for mapplings."""
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
            [
                Parameter(
                    Tiling(
                        (),
                        (
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                            ),
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0, 2)),
                                    ((1, 1), (1, 1), (1, 1)),
                                ),
                            ),
                        ),
                        (2, 2),
                    ),
                    RowColMap({0: 0, 1: 1}, {0: 0, 1: 0}),
                )
            ]
        ),
        ParameterList([]),
        ParameterList([]),
    )

    sep1 = MappedTiling(
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
                            (GriddedCayleyPerm(CayleyPermutation(()), ()),), (), (0, 0)
                        ),
                        RowColMap({}, {}),
                    )
                }
            )
        ),
        (),
        (),
    )

    sep2 = MappedTiling(
        Tiling((GriddedCayleyPerm(CayleyPermutation(()), ()),), (), (2, 3)),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (GriddedCayleyPerm(CayleyPermutation(()), ()),), (), (0, 0)
                        ),
                        RowColMap({}, {}),
                    )
                }
            )
        ),
        (),
        (),
    )

    all_separated = list(LTORERowColSeparationMT(mt).separate())
    assert len(all_separated) == 2
    assert all_separated[0] == sep1
    assert all_separated[1] == sep2


def test_less_than_or_equal_row_col_separation():
    """Test less than or equal row col separation for mapplings."""
    original_mt = MappedTiling(
        Tiling(
            (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (1, 0))),),
            (),
            (2, 1),
        ),
        ParameterList(
            [
                Parameter(
                    Tiling(
                        (),
                        (
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),),
                        ),
                        (2, 2),
                    ),
                    RowColMap({0: 0, 1: 1}, {0: 0, 1: 0}),
                )
            ]
        ),
        ParameterList([]),
        ParameterList([]),
    )

    separated_1 = MappedTiling(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),))), (),(2, 3)), ParameterList(frozenset({Parameter(Tiling((), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),)),(2, 6)), RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2}))})), (), ())

    separated_2 = MappedTiling(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),)),(2, 3)), ParameterList(frozenset({Parameter(Tiling((), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 5),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),)),(2, 6)), RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2}))})), (), ())

    all_separated = list(LTORERowColSeparationMT(original_mt).separate())
    assert len(all_separated) == 2
    assert all_separated[0] == separated_1
    assert all_separated[1] == separated_2


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

    assert list(LTRowColSeparationMT(mt).separate()) == [
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
                                (GriddedCayleyPerm(CayleyPermutation(()), ()),),
                                (),
                                (0, 0),
                            ),
                            RowColMap({}, {}),
                        )
                    }
                )
            ),
            (),
            (),
        )
    ]


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

    separated = [
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
                                (GriddedCayleyPerm(CayleyPermutation(()), ()),),
                                (),
                                (0, 0),
                            ),
                            RowColMap({}, {}),
                        )
                    }
                )
            ),
            (),
            (),
        )
    ]

    assert list(LTRowColSeparationMT(mt).separate()) == separated


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

    separation = [MappedTiling(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),))), (),(2, 3)), ParameterList(frozenset({Parameter(Tiling((GriddedCayleyPerm(CayleyPermutation(()), ()),), (),(0, 0)), RowColMap({}, {}))})), (), ()), MappedTiling(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),)),(2, 3)), ParameterList(frozenset({Parameter(Tiling((GriddedCayleyPerm(CayleyPermutation(()), ()),), (),(0, 0)), RowColMap({}, {}))})), (), ())]

    assert list(LTORERowColSeparationMT(mt).separate()) == separation


def test_double_expansion_param():
    """This mappling has two row separations and a column separation. When separating the
    avoiding parameter, the cell map was wrong and moved the rows up twice for the top
    expansion. Now it looks at the difference in the number of rows instead."""
    mt = [MappedTiling(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)), GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 3), (0, 3))), GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 2), (2, 2))), GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 0), (3, 0))), GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 4), (3, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 4), (3, 4))), GriddedCayleyPerm(CayleyPermutation((0, 2, 1)), ((1, 1), (1, 1), (1, 1))), GriddedCayleyPerm(CayleyPermutation((0, 2, 1)), ((3, 0), (3, 0), (3, 0))), GriddedCayleyPerm(CayleyPermutation((0, 2, 1)), ((3, 0), (3, 4), (3, 0)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),),),(4, 5)), ParameterList(frozenset({Parameter(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 7),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 9),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 10),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 13),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 4),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 13),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((7, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((7, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((7, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((7, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((7, 5),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((7, 13),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (3, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (4, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (6, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (2, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (4, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (5, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (6, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (4, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (6, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (7, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 4), (8, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (3, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (4, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (6, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 1), (4, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 1), (6, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 3), (4, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 3), (5, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 3), (6, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 4), (4, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 4), (6, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 4), (7, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 4), (8, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((5, 3), (5, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((5, 3), (6, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((5, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((6, 1), (6, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((6, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((6, 3), (6, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((6, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((6, 4), (6, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((6, 4), (7, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((6, 4), (8, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((7, 4), (7, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((7, 4), (8, 4))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((8, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((8, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((8, 4), (8, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (3, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (4, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (6, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (2, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (4, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (5, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (6, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (2, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (4, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (6, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (7, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 4), (8, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (3, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (4, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (6, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 1), (4, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 1), (6, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 3), (4, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 3), (5, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 3), (6, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 4), (4, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 4), (6, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 4), (7, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 4), (8, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((5, 3), (5, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((5, 3), (6, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((5, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((6, 1), (6, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((6, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((6, 3), (6, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((6, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((6, 4), (6, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((6, 4), (7, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((6, 4), (8, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((7, 4), (7, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((7, 4), (8, 4))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((8, 1), (8, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((8, 3), (8, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((8, 4), (8, 4)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 3),)),), (GriddedCayleyPerm(CayleyPermutation((0,)), ((7, 4),)),)),(9, 14)), RowColMap({0: 0, 1: 1, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3}, {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 3, 13: 4}))})), (), ())]


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

    separated = [
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
                            Tiling((), (), (6, 14)),
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
    ]

    assert list(LTRowColSeparationMT(mt).separate()) == separated


def test_double_column_expansion():
    """Base tiling has a column which expands into two columns,
    check parameter map adjusts correctly."""
    mt = MappedTiling(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (2, 0))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 0), (2, 2))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 2))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),),),(3, 4)), ParameterList(frozenset()), (ParameterList(frozenset({Parameter(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 1)))), (),(3, 4)), RowColMap({0: 0, 1: 0, 2: 2}, {0: 0, 1: 1, 2: 2, 3: 3}))})),), ())
    correct_output = MappedTiling(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 3),)), GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (3, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (3, 1))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 0), (4, 0))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (3, 1))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))), GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (3, 1)))), ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),),),(5, 4)), ParameterList(frozenset()), (ParameterList(frozenset({Parameter(Tiling((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 3),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)), GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))), GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 1)))), (),(5, 4)), RowColMap({0: 0, 1: 0, 2: 2, 3: 3, 4: 4}, {0: 0, 1: 1, 2: 2, 3: 3}))})),), ())
    for output in LTRowColSeparationMT(mt).separate():
            assert output == correct_output