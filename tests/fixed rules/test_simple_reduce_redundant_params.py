from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, ParameterList, Parameter
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.cleaners import MTCleaner


def test_simple_reduce_redundant_params():
    """Before it used subparameter, now uses restrict to region for subsets of params."""
    mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((5, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((6, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((6, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((6, 3),)),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (5, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 3), (3, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 1), (5, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 3), (3, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 2), (4, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((5, 1), (5, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((6, 0), (6, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (5, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (1, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (3, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 3), (4, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 1), (5, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 3), (3, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((5, 1), (5, 1))),
            ),
            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),),),
            (7, 4),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (2, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 0), (2, 0))
                                ),
                            ),
                            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),),),
                            (4, 3),
                        ),
                        RowColMap({0: 0, 1: 6, 2: 6, 3: 6}, {0: 0, 1: 1, 2: 2}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                            ),
                            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),),
                            (3, 2),
                        ),
                        RowColMap({0: 1, 1: 1, 2: 1}, {0: 1, 1: 3}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (7, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((7, 0), (7, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((7, 0), (7, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (7, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 1), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 1), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((6, 0), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 0), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 0), (5, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 0), (7, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((7, 0),)
                                    ),
                                ),
                            ),
                            (9, 3),
                        ),
                        RowColMap(
                            {0: 0, 1: 4, 2: 4, 3: 4, 4: 5, 5: 5, 6: 6, 7: 6, 8: 6},
                            {0: 0, 1: 1, 2: 2},
                        ),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (3, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 0), (3, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (3, 0))
                                    ),
                                ),
                            ),
                            (5, 2),
                        ),
                        RowColMap({0: 1, 1: 1, 2: 1, 3: 1, 4: 1}, {0: 1, 1: 3}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (10, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((4, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((4, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((7, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((10, 0), (10, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 0), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (3, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 0), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 1), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((10, 0), (10, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 1), (10, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((9, 0), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((9, 0), (8, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((10, 0), (8, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((10, 0), (10, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 0), (10, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 1), (10, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 3), (7, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 3), (10, 0))
                                    ),
                                ),
                            ),
                            (12, 4),
                        ),
                        RowColMap(
                            {
                                0: 0,
                                1: 0,
                                2: 0,
                                3: 1,
                                4: 1,
                                5: 1,
                                6: 5,
                                7: 5,
                                8: 5,
                                9: 6,
                                10: 6,
                                11: 6,
                            },
                            {0: 0, 1: 1, 2: 2, 3: 3},
                        ),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (13, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 2), (4, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((4, 2), (4, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((7, 1), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((10, 0), (13, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((11, 0), (11, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((13, 0), (13, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 2), (4, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((11, 0), (11, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((13, 0), (13, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (11, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 2), (4, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 2), (13, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((6, 1), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((6, 1), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((6, 1), (4, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((6, 1), (5, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 1), (11, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((10, 0), (7, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((10, 0), (8, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((10, 0), (9, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((11, 0), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((11, 0), (4, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((11, 0), (5, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((11, 0), (8, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((11, 0), (9, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((11, 0), (11, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((12, 0), (4, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((12, 0), (5, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((12, 0), (9, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((13, 0), (5, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((13, 0), (9, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((13, 0), (13, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 2), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 2), (13, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((7, 1), (13, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((11, 0), (13, 0))
                                    ),
                                ),
                            ),
                            (15, 3),
                        ),
                        RowColMap(
                            {
                                0: 0,
                                1: 4,
                                2: 4,
                                3: 4,
                                4: 4,
                                5: 4,
                                6: 5,
                                7: 5,
                                8: 5,
                                9: 5,
                                10: 6,
                                11: 6,
                                12: 6,
                                13: 6,
                                14: 6,
                            },
                            {0: 0, 1: 1, 2: 2},
                        ),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((0, 0), (10, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((5, 2), (5, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((10, 0), (10, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((5, 2), (5, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((10, 0), (10, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 2), (5, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((5, 2), (10, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 1), (5, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((7, 1), (6, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((9, 0), (8, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((10, 0), (6, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((10, 0), (8, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((10, 0), (10, 0))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 3), (5, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 3), (10, 0))
                                    ),
                                ),
                            ),
                            (12, 4),
                        ),
                        RowColMap(
                            {
                                0: 0,
                                1: 3,
                                2: 3,
                                3: 3,
                                4: 4,
                                5: 4,
                                6: 4,
                                7: 5,
                                8: 5,
                                9: 6,
                                10: 6,
                                11: 6,
                            },
                            {0: 0, 1: 1, 2: 2, 3: 3},
                        ),
                    ),
                }
            )
        ),
        (),
        (),
    )

    MTCleaner.global_debug_toggle(2)

    cleaned = MTCleaner.full_cleanup(mt)

    for n in range(4):
        print(mt.get_terms(n)[()])
        print(cleaned.get_terms(n)[()])
        assert mt.get_terms(n)[()] == cleaned.get_terms(n)[()]
