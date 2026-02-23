from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.cleaners import MTCleaner


def test_containing_parameter_list():
    """One containing parameter contains another containing parameter
    in the same list, checks that the correct one is kept."""
    mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (1, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (3, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (1, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (3, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 0), (3, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 1), (3, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 0), (3, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 1), (3, 1))),
            ),
            (),
            (4, 2),
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
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                ),
                                (),
                                (1, 1),
                            ),
                            RowColMap({0: 0}, {0: 0}),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 2), (2, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 2), (3, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 2), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 2), (4, 2))
                                    ),
                                ),
                                (),
                                (5, 3),
                            ),
                            RowColMap(
                                {0: 0, 1: 1, 2: 2, 3: 2, 4: 3}, {0: 0, 1: 1, 2: 1}
                            ),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((4, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((4, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
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
                                (),
                                (5, 3),
                            ),
                            RowColMap(
                                {0: 0, 1: 1, 2: 1, 3: 2, 4: 3}, {0: 0, 1: 0, 2: 1}
                            ),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((4, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((4, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                ),
                                (),
                                (5, 3),
                            ),
                            RowColMap(
                                {0: 0, 1: 0, 2: 1, 3: 2, 4: 3}, {0: 0, 1: 0, 2: 1}
                            ),
                        ),
                    }
                )
            ),
        ),
        (),
    )
    cleaned = MTCleaner.simple_reduce_redundant_parameters(mt)

    correct_cleaned = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (1, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (3, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (1, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (3, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 0), (2, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 0), (3, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 1), (2, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 1), (3, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 0), (3, 0))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 1), (3, 1))),
            ),
            (),
            (4, 2),
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
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((2, 2), (2, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 2), (3, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 2), (4, 2))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((4, 2), (4, 2))
                                    ),
                                ),
                                (),
                                (5, 3),
                            ),
                            RowColMap(
                                {0: 0, 1: 1, 2: 2, 3: 2, 4: 3}, {0: 0, 1: 1, 2: 1}
                            ),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((4, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((4, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
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
                                (),
                                (5, 3),
                            ),
                            RowColMap(
                                {0: 0, 1: 1, 2: 1, 3: 2, 4: 3}, {0: 0, 1: 0, 2: 1}
                            ),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((4, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((4, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                ),
                                (),
                                (5, 3),
                            ),
                            RowColMap(
                                {0: 0, 1: 0, 2: 1, 3: 2, 4: 3}, {0: 0, 1: 0, 2: 1}
                            ),
                        ),
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                    ),
                                ),
                                (),
                                (1, 1),
                            ),
                            RowColMap({0: 0}, {0: 0}),
                        ),
                    }
                )
            ),
        ),
        (),
    )
    assert cleaned == correct_cleaned
