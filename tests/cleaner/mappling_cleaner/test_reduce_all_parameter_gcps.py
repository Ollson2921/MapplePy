"""Testing the reduce_all_parameter_gcps cleaning function on
MTCleaner for MappedTiling.
TODO: this cleaning function isn't working properly yet! Put tests
back in when it is."""

import pytest
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation
from mapplings import MTCleaner, MappedTiling, Parameter, ParameterList


@pytest.mark.skip(reason="strategy not working yet")
def test_reduce_all_parameter_gcps():
    """Test reduce_all_parameter_gcps with multiple obstructions
    and requirements and containing and avoiding parameters."""
    obs = [
        GriddedCayleyPerm(CayleyPermutation([2, 1, 0]), [(1, 1), (1, 1), (1, 1)]),
        GriddedCayleyPerm(
            CayleyPermutation([0, 1, 3, 2]), [(1, 0), (1, 0), (1, 1), (1, 1)]
        ),
    ]

    reqs = [
        [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 0), (1, 1)])],
        [
            GriddedCayleyPerm(CayleyPermutation([0, 1, 0]), [(1, 0), (1, 0), (1, 0)]),
            GriddedCayleyPerm(CayleyPermutation([0, 1, 0]), [(1, 0), (1, 0), (1, 1)]),
        ],
    ]
    bt = Tiling(obs, reqs, (3, 2))

    ghost = Tiling([], [], (2, 2))
    colmap = {0: 0, 1: 1}
    rowmap = {0: 0, 1: 1}
    param = Parameter(ghost, RowColMap(colmap, rowmap)).backmap_all_from_tiling(bt)

    colmap = {0: 1, 1: 2}
    param2 = Parameter(ghost, RowColMap(colmap, rowmap)).backmap_all_from_tiling(bt)

    mt = MappedTiling(
        bt,
        ParameterList([param]),
        [ParameterList([param, param2]), ParameterList([param2])],
        [],
    )

    cleaned = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(
                    CayleyPermutation((2, 1, 0)), ((1, 1), (1, 1), (1, 1))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 3, 2)), ((1, 0), (1, 0), (1, 1), (1, 1))
                ),
            ),
            (
                (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 1))),),
                (
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 0)), ((1, 0), (1, 0), (1, 0))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 0)), ((1, 0), (1, 0), (1, 1))
                    ),
                ),
            ),
            (3, 2),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling((), (), (2, 2)), RowColMap({0: 0, 1: 1}, {0: 0, 1: 1})
                    )
                }
            )
        ),
        (
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling((), (), (2, 2)),
                            RowColMap({0: 1, 1: 2}, {0: 0, 1: 1}),
                        ),
                        Parameter(
                            Tiling((), (), (2, 2)),
                            RowColMap({0: 0, 1: 1}, {0: 0, 1: 1}),
                        ),
                    }
                )
            ),
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling((), (), (2, 2)),
                            RowColMap({0: 1, 1: 2}, {0: 0, 1: 1}),
                        )
                    }
                )
            ),
        ),
        (),
    )
    assert MTCleaner.reduce_all_parameter_gcps(mt) == cleaned


@pytest.mark.skip(reason="strategy not working yet")
def test_reduce_all_parameter_gcps_identical_params():
    """Test reduce_all_parameter_gcps when the parameters are identical
    to the base tiling."""
    obs = [
        GriddedCayleyPerm(CayleyPermutation([2, 1, 0]), [(1, 1), (1, 1), (1, 1)]),
        GriddedCayleyPerm(
            CayleyPermutation([0, 1, 3, 2]), [(1, 0), (1, 0), (1, 1), (1, 1)]
        ),
    ]
    reqs = [
        [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 0), (1, 1)])],
        [
            GriddedCayleyPerm(CayleyPermutation([0, 1, 0]), [(1, 0), (1, 0), (1, 0)]),
            GriddedCayleyPerm(CayleyPermutation([0, 1, 0]), [(1, 0), (1, 0), (1, 1)]),
        ],
    ]
    bt = Tiling(obs, reqs, (3, 2))

    colmap = {0: 0, 1: 1, 2: 2}
    rowmap = {0: 0, 1: 1}
    param = Parameter(bt, RowColMap(colmap, rowmap))

    mt = MappedTiling(
        bt,
        ParameterList([param]),
        [ParameterList([param])],
        [],
    )
    cleaned = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(
                    CayleyPermutation((2, 1, 0)), ((1, 1), (1, 1), (1, 1))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 3, 2)), ((1, 0), (1, 0), (1, 1), (1, 1))
                ),
            ),
            (
                (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 0), (1, 1))),),
                (
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 0)), ((1, 0), (1, 0), (1, 0))
                    ),
                    GriddedCayleyPerm(
                        CayleyPermutation((0, 1, 0)), ((1, 0), (1, 0), (1, 1))
                    ),
                ),
            ),
            (3, 2),
        ),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling((), (), (3, 2)),
                        RowColMap({0: 0, 1: 1, 2: 2}, {0: 0, 1: 1}),
                    )
                }
            )
        ),
        (
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling((), (), (3, 2)),
                            RowColMap({0: 0, 1: 1, 2: 2}, {0: 0, 1: 1}),
                        )
                    }
                )
            ),
        ),
        (),
    )

    assert MTCleaner.reduce_all_parameter_gcps(mt) == cleaned
