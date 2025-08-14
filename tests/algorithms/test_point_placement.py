from mapplings.algorithms.point_placement import MTRequirementPlacement
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, ParameterList, Parameter
from gridded_cayley_permutations.row_col_map import RowColMap


def test_point_placement_in_mapped_tiling():
    """Test for point placement in a MappedTiling"""
    ghost = Tiling(
        [],
        [],
        (2, 2),
    )
    colmap = {0: 1, 1: 1}
    rowmap = {0: 0, 1: 0}
    param1 = Parameter(ghost, RowColMap(colmap, rowmap))
    colmap = {0: 1, 1: 1}
    rowmap = {0: 1, 1: 1}
    param2 = Parameter(ghost, RowColMap(colmap, rowmap))
    colmap = {0: 0, 1: 0}
    rowmap = {0: 0, 1: 0}
    param3 = Parameter(ghost, RowColMap(colmap, rowmap))
    colmap = {0: 0, 1: 0}
    rowmap = {0: 1, 1: 1}
    param4 = Parameter(ghost, RowColMap(colmap, rowmap))
    colmap = {0: 0, 1: 1}
    rowmap = {0: 0, 1: 1}
    param5 = Parameter(ghost, RowColMap(colmap, rowmap))
    bt = Tiling([], [], (2, 2))
    mt = MappedTiling(
        bt,
        ParameterList([param2, param5]),
        (ParameterList([param1, param3]), ParameterList([param4])),
        (),
    )
    output = list(
        MTRequirementPlacement(mt).point_placement(
            (GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),), (0,), 1
        )
    )
    correct_output = [
        MappedTiling(
            Tiling(
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                    GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (3, 1))),
                    GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 1), (3, 1))),
                ),
                ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),),
                (4, 4),
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling((), (), (3, 4)),
                            RowColMap({0: 0, 1: 2, 2: 3}, {0: 0, 1: 1, 2: 2, 3: 3}),
                        ),
                        Parameter(
                            Tiling((), (), (2, 2)),
                            RowColMap({0: 3, 1: 3}, {0: 3, 1: 3}),
                        ),
                    }
                )
            ),
            (
                ParameterList(
                    frozenset(
                        {
                            Parameter(
                                Tiling((), (), (3, 4)),
                                RowColMap({0: 0, 1: 0, 2: 2}, {0: 0, 1: 1, 2: 2, 3: 2}),
                            ),
                            Parameter(
                                Tiling((), (), (3, 4)),
                                RowColMap({0: 0, 1: 2, 2: 2}, {0: 0, 1: 0, 2: 1, 3: 2}),
                            ),
                            Parameter(
                                Tiling((), (), (2, 4)),
                                RowColMap({0: 3, 1: 3}, {0: 0, 1: 0, 2: 1, 3: 2}),
                            ),
                            Parameter(
                                Tiling((), (), (3, 4)),
                                RowColMap({0: 0, 1: 0, 2: 2}, {0: 0, 1: 0, 2: 1, 3: 2}),
                            ),
                            Parameter(
                                Tiling((), (), (2, 4)),
                                RowColMap({0: 3, 1: 3}, {0: 0, 1: 1, 2: 2, 3: 2}),
                            ),
                            Parameter(
                                Tiling((), (), (3, 4)),
                                RowColMap({0: 0, 1: 2, 2: 2}, {0: 0, 1: 1, 2: 2, 3: 2}),
                            ),
                        }
                    )
                ),
                ParameterList(
                    frozenset(
                        {
                            Parameter(
                                Tiling((), (), (3, 2)),
                                RowColMap({0: 0, 1: 0, 2: 2}, {0: 3, 1: 3}),
                            ),
                            Parameter(
                                Tiling((), (), (3, 2)),
                                RowColMap({0: 0, 1: 2, 2: 2}, {0: 3, 1: 3}),
                            ),
                        }
                    )
                ),
            ),
            (),
        )
    ]
    assert output == correct_output
