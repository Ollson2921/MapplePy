from mapplings import MappedTiling, ParameterList, Parameter
from gridded_cayley_permutations import GriddedCayleyPerm, RowColMap, Tiling
from cayley_permutations import CayleyPermutation
from mapplings.algorithms.row_col_sep_mt import MTLTRowColSeparation


def test_lt_rc_separation():
    """Base tiling doesn't seprate but because of empty rows, check it
    doesn't try to map params anyway"""
    mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (1, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (1, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 0), (1, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
            ),
            (
                (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),
                (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),),
            ),
            (2, 4),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((4, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((4, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((4, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 2), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 0), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 0), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 1), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((5, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 0), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 0), (5, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 1), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (4, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 0), (5, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 2), (4, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 2), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 3), (4, 3))
                                    ),
                                ),
                            ),
                            (6, 4),
                        ),
                        RowColMap(
                            {0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
                            {0: 0, 1: 1, 2: 2, 3: 3},
                        ),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 2), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 0), (3, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 1),)
                                    ),
                                ),
                            ),
                            (4, 4),
                        ),
                        RowColMap({0: 0, 1: 1, 2: 1, 3: 1}, {0: 0, 1: 1, 2: 2, 3: 3}),
                    ),
                }
            )
        ),
        (),
        (),
    )

    separated = list(MTLTRowColSeparation(mt).separate())[0]

    for i in range(5):
        assert mt.get_terms(i)[()] == separated.get_terms(i)[()]


def test_rc_sep_after_fix():
    """Previous fix gave this error, check it doesn't break again.
    Had tried to take into account base tiling may have empty rows
    or columns, instead not working on mapplings that do."""
    mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 4), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 3), (0, 1), (0, 4))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 3), (0, 2), (0, 4))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 4), (0, 3), (0, 4))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((1, 0, 2)), ((0, 4), (0, 4), (0, 4))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((2, 0, 1)), ((0, 3), (0, 1), (0, 2))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((2, 0, 1)), ((0, 3), (0, 2), (0, 2))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((2, 0, 1)), ((0, 4), (0, 3), (0, 4))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((2, 0, 1)), ((0, 4), (0, 4), (0, 4))
                ),
            ),
            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),),),
            (3, 5),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 0), (1, 0))
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
                                    CayleyPermutation((0, 0)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 2), (1, 0))
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
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 4))
                                ),
                            ),
                            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),),),
                            (3, 5),
                        ),
                        RowColMap({0: 0, 1: 0, 2: 0}, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 0), (1, 0))
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
                                    CayleyPermutation((0, 0)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((4, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 2), (1, 0))
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
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 4))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 2), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (4, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (4, 1))
                                    ),
                                ),
                            ),
                            (6, 5),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 0, 3: 2, 4: 2, 5: 2},
                            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
                        ),
                    ),
                    Parameter(
                        Tiling(
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),
                            (),
                            (1, 1),
                        ),
                        RowColMap({0: 0}, {0: 1}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 0), (2, 0))
                                ),
                            ),
                            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),),),
                            (4, 1),
                        ),
                        RowColMap({0: 0, 1: 2, 2: 2, 3: 2}, {0: 1}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 2), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 3), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 4), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 0), (1, 0))
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
                                    CayleyPermutation((0, 0)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 2), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 3), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 4), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 0), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 1), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 1), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 1), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 2), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 2), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 2), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 3), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 4), (3, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 2), (1, 0))
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
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 2), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 2), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 3), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 3), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 4), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 4), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 4), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 4), (3, 4))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (3, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (3, 3))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (3, 4))
                                    ),
                                ),
                            ),
                            (5, 5),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                            {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
                        ),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 3), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 3), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 4))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 4),)
                                    ),
                                ),
                            ),
                            (3, 5),
                        ),
                        RowColMap({0: 0, 1: 0, 2: 0}, {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}),
                    ),
                }
            )
        ),
        (),
        (),
    )

    separated = list(MTLTRowColSeparation(mt).separate())[0]

    for i in range(5):
        assert mt.get_terms(i)[()] == separated.get_terms(i)[()]
