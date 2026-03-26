from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.tilescope_strategies import MapplingLessThanOrEqualRowColSeparationFactory




def test_ltoreq_rc_separation_factory_one_big_separation():
    """Base tiling separates in different ways, should return different separations."""
    til_error_1 = Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 1, 2)), ((0, 0), (0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1, 2)), ((0, 1), (0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0, 2)), ((0, 1), (0, 0), (0, 1))),
            GriddedCayleyPerm(
                CayleyPermutation((1, 0, 2, 0)), ((0, 1), (0, 1), (0, 1), (0, 1))
            ),
            GriddedCayleyPerm(
                CayleyPermutation((1, 0, 2, 0)), ((0, 1), (0, 1), (0, 1), (1, 1))
            ),
            GriddedCayleyPerm(
                CayleyPermutation((1, 0, 2, 0)), ((0, 1), (0, 1), (0, 1), (2, 1))
            ),
        ),
        (),
        (3, 2),
    )

    param = Parameter(
        Tiling(
            (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),), (), (1, 1)
        ),
        RowColMap({0: 0}, {0: 1}),
    )

    mt = MappedTiling(til_error_1, [param], [], [])

    out = set()
    for strat in MapplingLessThanOrEqualRowColSeparationFactory()(mt):
        out.add(strat(mt).children)
        for child in strat(mt).children:


    separated = {
        (
            MappedTiling(
                Tiling(
                    (
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 0), (0, 2), (0, 2))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 2), (0, 2), (0, 2))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2)), ((0, 2), (0, 0), (0, 2))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((2, 1, 0)), ((2, 1), (2, 1), (2, 1))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2, 0)),
                            ((0, 2), (0, 2), (0, 2), (0, 2)),
                        ),
                    ),
                    (),
                    (3, 3),
                ),
                ParameterList(
                    frozenset(
                        {
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 2, 1)),
                                            ((0, 0), (0, 0), (0, 0)),
                                        ),
                                    ),
                                    (),
                                    (1, 1),
                                ),
                                RowColMap({0: 0}, {0: 2}),
                            ),
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                        ),
                                    ),
                                    (),
                                    (1, 1),
                                ),
                                RowColMap({0: 0}, {0: 2}),
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
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 0), (0, 2), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 0), (0, 3), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 2), (0, 3), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 3), (0, 3), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2)), ((0, 2), (0, 0), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2)), ((0, 3), (0, 0), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((2, 1, 0)), ((2, 1), (2, 1), (2, 1))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((2, 1, 0)), ((2, 2), (2, 1), (2, 1))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2, 0)),
                            ((0, 3), (0, 2), (0, 3), (0, 2)),
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2, 0)),
                            ((0, 3), (0, 2), (0, 3), (1, 2)),
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2, 0)),
                            ((0, 3), (0, 2), (0, 3), (2, 2)),
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2, 0)),
                            ((0, 3), (0, 3), (0, 3), (0, 3)),
                        ),
                    ),
                    (
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),),
                        (
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                        ),
                    ),
                    (3, 4),
                ),
                ParameterList(
                    frozenset(
                        {
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 2, 1)),
                                            ((0, 0), (0, 1), (0, 1)),
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 2, 1)),
                                            ((0, 1), (0, 1), (0, 1)),
                                        ),
                                    ),
                                    (),
                                    (1, 2),
                                ),
                                RowColMap({0: 0}, {0: 2, 1: 3}),
                            ),
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((0, 0), (0, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                        ),
                                    ),
                                    (),
                                    (1, 2),
                                ),
                                RowColMap({0: 0}, {0: 2, 1: 3}),
                            ),
                        }
                    )
                ),
                (),
                (),
            ),
        ),
        (
            MappedTiling(
                Tiling(
                    (
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 0), (0, 2), (0, 2))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 2), (0, 2), (0, 2))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2)), ((0, 2), (0, 0), (0, 2))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((2, 1, 0)), ((2, 1), (2, 1), (2, 1))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2, 0)),
                            ((0, 2), (0, 2), (0, 2), (0, 2)),
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2, 0)),
                            ((0, 2), (0, 2), (0, 2), (1, 2)),
                        ),
                    ),
                    (),
                    (3, 3),
                ),
                ParameterList(
                    frozenset(
                        {
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 2, 1)),
                                            ((0, 0), (0, 0), (0, 0)),
                                        ),
                                    ),
                                    (),
                                    (1, 1),
                                ),
                                RowColMap({0: 0}, {0: 2}),
                            ),
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                        ),
                                    ),
                                    (),
                                    (1, 1),
                                ),
                                RowColMap({0: 0}, {0: 2}),
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
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                        GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 3))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (1, 3))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 3))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (1, 3))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (2, 2))),
                        GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 0), (0, 2), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 0), (0, 3), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 2), (0, 3), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1, 2)), ((0, 3), (0, 3), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2)), ((0, 2), (0, 0), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2)), ((0, 3), (0, 0), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2)), ((0, 3), (0, 2), (0, 3))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((2, 1, 0)), ((2, 1), (2, 1), (2, 1))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((2, 1, 0)), ((2, 2), (2, 1), (2, 1))
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2, 0)),
                            ((0, 3), (0, 3), (0, 3), (0, 3)),
                        ),
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0, 2, 0)),
                            ((0, 3), (0, 3), (0, 3), (1, 3)),
                        ),
                    ),
                    (
                        (
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                        ),
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),),
                    ),
                    (3, 4),
                ),
                ParameterList(
                    frozenset(
                        {
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 2, 1)),
                                            ((0, 0), (0, 1), (0, 1)),
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 2, 1)),
                                            ((0, 1), (0, 1), (0, 1)),
                                        ),
                                    ),
                                    (),
                                    (1, 2),
                                ),
                                RowColMap({0: 0}, {0: 2, 1: 3}),
                            ),
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((0, 0), (0, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                        ),
                                    ),
                                    (),
                                    (1, 2),
                                ),
                                RowColMap({0: 0}, {0: 2, 1: 3}),
                            ),
                        }
                    )
                ),
                (),
                (),
            ),
        ),
    }

    assert out == separated