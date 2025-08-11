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

    separated_1 = MappedTiling(
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
                            (),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 5),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                ),
                            ),
                            (2, 6),
                        ),
                        RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 4: 1, 5: 1, 8: 2, 9: 2}),
                    )
                }
            )
        ),
        (),
        (),
    )

    separated_2 = MappedTiling(
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
                            (),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 5),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                ),
                            ),
                            (2, 6),
                        ),
                        RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 4: 1, 5: 1, 8: 2, 9: 2}),
                    )
                }
            )
        ),
        (),
        (),
    )

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

    assert list(LTORERowColSeparationMT(mt).separate()) == [sep1, sep2]
