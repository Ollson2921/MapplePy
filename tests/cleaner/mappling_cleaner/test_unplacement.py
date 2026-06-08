from mapplings.cleaners import MTCleaner
from mapplings import MappedTiling, ParameterList, Parameter
from gridded_cayley_permutations import GriddedCayleyPerm, RowColMap, Tiling
from cayley_permutations import CayleyPermutation


def test_unplacement_on_rgfs_param():
    """Mappling with the rgfs param as an avoider, test full cleaning doesn't
    fully unplace all points and counts are the same."""
    rgfs_mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 0, 0)), ((0, 0), (0, 0), (0, 0), (0, 0))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2, 1, 0)),
                    ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
                ),
            ),
            (),
            (1, 1),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 4),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 3), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 3), (0, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 3), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 3), (4, 3))
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
                                    CayleyPermutation((0, 1)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 3), (4, 3))
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
                                    CayleyPermutation((1, 0)), ((1, 3), (1, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 3), (4, 3))
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
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (4, 3))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 3),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 1),)
                                    ),
                                ),
                            ),
                            (5, 5),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                        ),
                    )
                }
            )
        ),
        (),
        (),
    )

    cleaned = MTCleaner.full_cleanup(rgfs_mt)
    for i in range(5):
        assert rgfs_mt.get_terms(i)[()] == cleaned.get_terms(i)[()]
