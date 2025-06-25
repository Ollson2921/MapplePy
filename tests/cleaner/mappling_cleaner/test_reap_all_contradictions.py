"""Testing the reap_all_contradictions cleaning function on
MTCleaner for MappedTiling."""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation
from mapplings import MTCleaner, MappedTiling, Parameter, ParameterList


def test_make_mappling_empty():
    """Test reap_all_contradictions with a containing
    parameter which contradicts the base tiling so makes the
    mapplings empty."""
    bt = Tiling(
        [
            GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),
            GriddedCayleyPerm(CayleyPermutation([0]), [(1, 1)]),
        ],
        [],
        (2, 2),
    )

    ghost = Tiling([], [[GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])]], (1, 1))
    colmap = {0: 0}
    rowmap = {0: 0}
    param1 = Parameter(ghost, RowColMap(colmap, rowmap))

    mt = MappedTiling(
        bt,
        ParameterList([]),
        [ParameterList([param1])],
        [],
    )

    cleaned = MappedTiling(
        Tiling((GriddedCayleyPerm(CayleyPermutation(()), ()),), (), (0, 0)),
        ParameterList(frozenset()),
        (),
        (),
    )

    assert MTCleaner.reap_all_contradictions(mt) == cleaned


def test_remove_contradictory_containing_params():
    """Test reap_all_contradictions with a containing
    parameter in a list which contradicts the base tiling
    and another which doesn't so removes the contradictory
    parameter."""
    bt = Tiling(
        [
            GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),
            GriddedCayleyPerm(CayleyPermutation([0]), [(1, 1)]),
        ],
        [],
        (2, 2),
    )

    ghost = Tiling([], [[GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])]], (1, 1))
    colmap = {0: 0}
    rowmap = {0: 0}
    param1 = Parameter(ghost, RowColMap(colmap, rowmap))

    colmap = {0: 1}
    rowmap = {0: 0}
    param2 = Parameter(ghost, RowColMap(colmap, rowmap))

    mt = MappedTiling(
        bt,
        ParameterList([]),
        [ParameterList([param1, param2])],
        [],
    )

    cleaned = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
            ),
            (),
            (2, 2),
        ),
        ParameterList(frozenset()),
        (
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                    ),
                                ),
                                (1, 1),
                            ),
                            RowColMap({0: 1}, {0: 0}),
                        )
                    }
                )
            ),
        ),
        (),
    )
    assert MTCleaner.reap_all_contradictions(mt) == cleaned


def test_remove_cont_avoiding_param():
    """Test removing an avoiding parameter
    which contradicts the base tiling."""
    bt = Tiling(
        [
            GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),
            GriddedCayleyPerm(CayleyPermutation([0]), [(1, 1)]),
        ],
        [],
        (2, 2),
    )

    ghost = Tiling([], [[GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])]], (1, 1))

    colmap = {0: 0}
    rowmap = {0: 0}
    param1 = Parameter(ghost, RowColMap(colmap, rowmap))

    colmap = {0: 1}
    rowmap = {0: 0}
    param2 = Parameter(ghost, RowColMap(colmap, rowmap))

    mt = MappedTiling(
        bt,
        ParameterList([param1]),
        [ParameterList([param1, param2])],
        [],
    )
    cleaned = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
            ),
            (),
            (2, 2),
        ),
        ParameterList(frozenset()),
        (
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (),
                                (
                                    (
                                        GriddedCayleyPerm(
                                            CayleyPermutation((0,)), ((0, 0),)
                                        ),
                                    ),
                                ),
                                (1, 1),
                            ),
                            RowColMap({0: 1}, {0: 0}),
                        )
                    }
                )
            ),
        ),
        (),
    )

    assert MTCleaner.reap_all_contradictions(mt) == cleaned


def test_obs_contradict_base_tiling():
    """Test reap_all_contradictions with containing
    and avoiding parameters with obstructions that
    contradict the base tiling."""
    bt = Tiling(
        [],
        [
            [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)])],
            [GriddedCayleyPerm(CayleyPermutation([0]), [(1, 1)])],
        ],
        (2, 2),
    )

    ghost = Tiling([GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])], [], (1, 1))

    colmap = {0: 0}
    rowmap = {0: 0}
    param1 = Parameter(ghost, RowColMap(colmap, rowmap))

    colmap = {0: 1}
    rowmap = {0: 0}
    param2 = Parameter(ghost, RowColMap(colmap, rowmap))

    mt = MappedTiling(
        bt,
        ParameterList([param1]),
        [ParameterList([param1, param2])],
        [],
    )
    cleaned = MappedTiling(
        Tiling(
            (),
            (
                (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 0))),),
            ),
            (2, 2),
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
                                        CayleyPermutation((0,)), ((0, 0),)
                                    ),
                                ),
                                (),
                                (1, 1),
                            ),
                            RowColMap({0: 1}, {0: 0}),
                        )
                    }
                )
            ),
        ),
        (),
    )

    assert MTCleaner.reap_all_contradictions(mt) == cleaned


def test_obs_contradiction_becomes_empty():
    """Test reap_all_contradictions with a containing
    parameter whose obstructions contradict the
    base tiling makes the mapplings empty."""
    bt = Tiling(
        [],
        [
            [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)])],
            [GriddedCayleyPerm(CayleyPermutation([0]), [(1, 1)])],
        ],
        (2, 2),
    )

    ghost = Tiling([GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)])], [], (1, 1))

    colmap = {0: 0}
    rowmap = {0: 0}
    param1 = Parameter(ghost, RowColMap(colmap, rowmap))

    mt = MappedTiling(
        bt,
        ParameterList([param1]),
        [ParameterList([param1])],
        [],
    )

    cleaned = MappedTiling(
        Tiling((GriddedCayleyPerm(CayleyPermutation(()), ()),), (), (0, 0)),
        ParameterList(frozenset()),
        (),
        (),
    )
    assert MTCleaner.reap_all_contradictions(mt) == cleaned
