from mapplings.algorithms.point_placement import MTRequirementPlacement
from mapplings.cleaners import MTCleaner
from mapplings import MappedTiling, ParameterList, Parameter
from gridded_cayley_permutations import GriddedCayleyPerm, RowColMap, Tiling
from cayley_permutations import CayleyPermutation


def test_delete_rcs_in_params_after_pp():
    "Placed the point of the requirement (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),) at indices (0,) in direction 1 then check counts after cleaning."
    mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 0)), ((0, 1), (0, 2), (0, 1))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 0, 0)), ((0, 0), (0, 0), (0, 0), (0, 0))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 0, 0)), ((0, 0), (0, 1), (0, 0), (0, 0))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 0, 0)), ((0, 0), (0, 2), (0, 0), (0, 0))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 0, 0)), ((0, 2), (0, 2), (0, 2), (0, 2))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2, 1)), ((0, 1), (0, 2), (0, 2), (0, 2))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2, 1, 0)),
                    ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2, 1, 0)),
                    ((0, 0), (0, 0), (0, 1), (0, 0), (0, 0)),
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2, 1, 0)),
                    ((0, 0), (0, 0), (0, 2), (0, 0), (0, 0)),
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2, 1, 0)),
                    ((0, 0), (0, 2), (0, 2), (0, 2), (0, 0)),
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2, 1, 0)),
                    ((0, 2), (0, 2), (0, 2), (0, 2), (0, 2)),
                ),
            ),
            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),),),
            (1, 3),
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
                                        CayleyPermutation((1, 0)), ((1, 3), (3, 1))
                                    ),
                                ),
                            ),
                            (5, 5),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                            {0: 2, 1: 2, 2: 2, 3: 2, 4: 2},
                        ),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 4),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 5),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 4), (0, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 4), (2, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 4), (4, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (2, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 4), (4, 4))
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
                                    CayleyPermutation((0, 1)), ((2, 4), (2, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 4), (4, 4))
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
                                    CayleyPermutation((0, 1)), ((4, 4), (4, 4))
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
                                    CayleyPermutation((1, 0)), ((1, 4), (1, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (2, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 4), (4, 4))
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
                                    CayleyPermutation((1, 0)), ((2, 4), (2, 4))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 4), (4, 4))
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
                                    CayleyPermutation((1, 0)), ((4, 4), (4, 4))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 4), (3, 1))
                                    ),
                                ),
                            ),
                            (5, 6),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                            {0: 0, 1: 0, 2: 0, 3: 2, 4: 2, 5: 2},
                        ),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 2), (0, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 2), (0, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 2), (2, 2))
                                ),
                            ),
                            ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),),),
                            (3, 4),
                        ),
                        RowColMap({0: 0, 1: 0, 2: 0}, {0: 1, 1: 2, 2: 2, 3: 2}),
                    ),
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
                                        CayleyPermutation((1, 0)), ((1, 3), (3, 1))
                                    ),
                                ),
                            ),
                            (5, 5),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                        ),
                    ),
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
                                    CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 1), (4, 1))
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
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (3, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (4, 1))
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
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (3, 1))
                                    ),
                                ),
                            ),
                            (5, 5),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                            {0: 0, 1: 0, 2: 0, 3: 1, 4: 2},
                        ),
                    ),
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
                                    CayleyPermutation((0, 1)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 3), (4, 3))
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
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (4, 3))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 3), (3, 1))
                                    ),
                                ),
                            ),
                            (5, 5),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                            {0: 0, 1: 1, 2: 2, 3: 2, 4: 2},
                        ),
                    ),
                }
            )
        ),
        (),
        (),
    )
    placed = MTRequirementPlacement(mt).point_placement(
        (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),), (0,), 3
    )[0]
    placed = MTCleaner.full_cleanup(placed)

    for i in range(4):
        assert placed.get_terms(i) == mt.get_terms(i)
