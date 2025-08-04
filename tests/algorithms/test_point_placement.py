from mapplings.algorithms.point_placement import MTRequirementPlacement
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, ParameterList, Parameter
from gridded_cayley_permutations.row_col_map import RowColMap


def test_map_for_param_unchanged():
    """Test for map_for_param_unchanged function for point placement"""
    ghost = Tiling(
        [],
        [],
        (2, 2),
    )
    colmap = {0: 1, 1: 1}
    rowmap = {0: 1, 1: 1}
    param = Parameter(ghost, RowColMap(colmap, rowmap))
    bt = Tiling([], [], (2, 2))
    mt = MappedTiling(
        bt,
        ParameterList(frozenset()),
        (ParameterList([param]),),
        (),
    )
    assert MTRequirementPlacement(mt).map_for_param_unchanged(
        param, (0, 0)
    ) == RowColMap({0: 3, 1: 3}, {0: 3, 1: 3})


def test_unfuse_row():
    """Test for unfuse_row function for point placement"""
    ghost = Tiling(
        [],
        [],
        (2, 2),
    )
    colmap = {0: 1, 1: 1}
    rowmap = {0: 0, 1: 0}
    param = Parameter(ghost, RowColMap(colmap, rowmap))
    bt = Tiling([], [], (2, 2))
    mt = MappedTiling(
        bt,
        ParameterList(frozenset()),
        (ParameterList([param]),),
        (),
    )
    print(repr(MTRequirementPlacement(mt).unfuse_row(param, 0)))
    assert MTRequirementPlacement(mt).unfuse_row(param, 0) == Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
        ),
        (),
        (2, 4),
    )

    assert MTRequirementPlacement(mt).unfuse_row(param, 1) == Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
        ),
        (),
        (2, 4),
    )


def test_unfuse_cols_in_param():
    """Test for unfuse_cols_in_param"""
    ghost = Tiling(
        [],
        [],
        (2, 2),
    )
    colmap = {0: 0, 1: 0}
    rowmap = {0: 1, 1: 1}
    param = Parameter(ghost, RowColMap(colmap, rowmap))
    bt = Tiling([], [], (2, 2))
    mt = MappedTiling(
        bt,
        ParameterList(frozenset()),
        (ParameterList([param]),),
        (),
    )
    assert list(MTRequirementPlacement(mt).unfuse_cols_in_param(param, (0, 0)))[
        0
    ] == Parameter(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
            ),
            (),
            (4, 2),
        ),
        RowColMap({0: 0, 1: 1, 2: 2, 3: 2}, {0: 3, 1: 3}),
    )
    assert list(MTRequirementPlacement(mt).unfuse_cols_in_param(param, (0, 0)))[
        1
    ] == Parameter(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
            ),
            (),
            (4, 2),
        ),
        RowColMap({0: 0, 1: 0, 2: 1, 3: 2}, {0: 3, 1: 3}),
    )


def test_unfuse_rows_in_param():
    """Test for unfuse_rows_in_param"""
    ghost = Tiling(
        [],
        [],
        (2, 2),
    )
    colmap = {0: 1, 1: 1}
    rowmap = {0: 0, 1: 0}
    param = Parameter(ghost, RowColMap(colmap, rowmap))
    bt = Tiling([], [], (2, 2))
    mt = MappedTiling(
        bt,
        ParameterList(frozenset()),
        (ParameterList([param]),),
        (),
    )
    assert list(MTRequirementPlacement(mt).unfuse_rows_in_param(param, (0, 0)))[
        0
    ] == Parameter(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
            ),
            (),
            (2, 4),
        ),
        RowColMap({0: 3, 1: 3}, {0: 0, 1: 1, 2: 2, 3: 2}),
    )
    assert list(MTRequirementPlacement(mt).unfuse_rows_in_param(param, (0, 0)))[
        1
    ] == Parameter(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
            ),
            (),
            (2, 4),
        ),
        RowColMap({0: 3, 1: 3}, {0: 0, 1: 0, 2: 1, 3: 2}),
    )


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
    print(mt)
    for p in MTRequirementPlacement(mt).point_placement(
        (GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),), (0,), 1
    ):
        print(p)
    assert list(
        MTRequirementPlacement(mt).point_placement(
            (GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),), (0,), 1
        )
    ) == [
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
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((0, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 0),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 3),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 1),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 2),)
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((1, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((3, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((0, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((1, 1), (3, 1))
                                    ),
                                    GriddedCayleyPerm(
                                        CayleyPermutation((1, 0)), ((3, 1), (3, 1))
                                    ),
                                ),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 1),)
                                        ),
                                    ),
                                ),
                                (4, 4),
                            ),
                            RowColMap(
                                {0: 0, 1: 1, 2: 2, 3: 3}, {0: 0, 1: 1, 2: 2, 3: 3}
                            ),
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
                                            CayleyPermutation((0,)), ((1, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 3),)
                                        ),
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
                                    (
                                        (
                                            GriddedCayleyPerm(
                                                CayleyPermutation((0,)), ((1, 2),)
                                            ),
                                        ),
                                    ),
                                    (4, 4),
                                ),
                                RowColMap(
                                    {0: 0, 1: 1, 2: 2, 3: 2}, {0: 0, 1: 0, 2: 1, 3: 2}
                                ),
                            ),
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 0)), ((2, 2), (2, 2))
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
                                    (
                                        (
                                            GriddedCayleyPerm(
                                                CayleyPermutation((0,)), ((2, 2),)
                                            ),
                                        ),
                                    ),
                                    (4, 4),
                                ),
                                RowColMap(
                                    {0: 0, 1: 0, 2: 1, 3: 2}, {0: 0, 1: 0, 2: 1, 3: 2}
                                ),
                            ),
                            Parameter(
                                Tiling(
                                    (
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
                                    (2, 4),
                                ),
                                RowColMap({0: 3, 1: 3}, {0: 0, 1: 0, 2: 1, 3: 2}),
                            ),
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
                                            CayleyPermutation((0,)), ((1, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 0)), ((2, 1), (2, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((0, 1), (2, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((1, 1), (2, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 1)), ((2, 1), (2, 1))
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
                                            CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1, 0)), ((1, 1), (2, 1))
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                        ),
                                    ),
                                    (
                                        (
                                            GriddedCayleyPerm(
                                                CayleyPermutation((0,)), ((2, 1),)
                                            ),
                                        ),
                                    ),
                                    (4, 4),
                                ),
                                RowColMap(
                                    {0: 0, 1: 0, 2: 1, 3: 2}, {0: 0, 1: 1, 2: 2, 3: 2}
                                ),
                            ),
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
                                            CayleyPermutation((0,)), ((1, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((1, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 1),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 2),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((3, 3),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0, 0)), ((1, 1), (1, 1))
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
                                    (
                                        (
                                            GriddedCayleyPerm(
                                                CayleyPermutation((0,)), ((1, 1),)
                                            ),
                                        ),
                                    ),
                                    (4, 4),
                                ),
                                RowColMap(
                                    {0: 0, 1: 1, 2: 2, 3: 2}, {0: 0, 1: 1, 2: 2, 3: 2}
                                ),
                            ),
                            Parameter(
                                Tiling(
                                    (
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
                                    (2, 4),
                                ),
                                RowColMap({0: 3, 1: 3}, {0: 0, 1: 1, 2: 2, 3: 2}),
                            ),
                        }
                    )
                ),
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
                                            CayleyPermutation((0,)), ((1, 1),)
                                        ),
                                    ),
                                    (),
                                    (4, 2),
                                ),
                                RowColMap({0: 0, 1: 1, 2: 2, 3: 2}, {0: 3, 1: 3}),
                            ),
                            Parameter(
                                Tiling(
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 0),)
                                        ),
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((2, 1),)
                                        ),
                                    ),
                                    (),
                                    (4, 2),
                                ),
                                RowColMap({0: 0, 1: 0, 2: 1, 3: 2}, {0: 3, 1: 3}),
                            ),
                        }
                    )
                ),
            ),
            (),
        )
    ]
