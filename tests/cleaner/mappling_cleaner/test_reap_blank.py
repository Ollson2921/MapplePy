"""Testing the reap_blank cleaning function on
MTCleaner for MappedTiling - removes blank avoiding parameters
or containing parameter lists if they have any blank parameters in."""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, Parameter, ParameterList
from mapplings.cleaners import MTCleaner


def test_reap_blank_containing_params():
    """Mappling has a cotaining parameter list with just a
    blank parameter, one with a blank and a non-blank
    parameter, and one with just a non-blank parameter.
    Should remove the first two lists and keep the last."""
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
    ghost = Tiling([], [], (1, 1))
    param2 = Parameter(ghost, RowColMap(colmap, rowmap))

    mt = MappedTiling(
        bt,
        [],
        [
            ParameterList([param1, param2]),
            ParameterList([param2]),
            ParameterList([param1]),
        ],
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
                            RowColMap({0: 0}, {0: 0}),
                        )
                    }
                )
            ),
        ),
        (),
    )
    assert MTCleaner.reap_blank(mt) == cleaned


def test_reap_blank_avoiding_params():
    """Mappling contains a blank avoiding parameter,
    should make the mappling empty."""
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
    rowmap = {0: 1}
    param1 = Parameter(ghost, RowColMap(colmap, rowmap))

    colmap = {0: 1}
    rowmap = {0: 0}
    ghost = Tiling([], [], (1, 1))
    param2 = Parameter(ghost, RowColMap(colmap, rowmap))

    mt = MappedTiling(
        bt,
        ParameterList([param1, param2]),
        [ParameterList([param1])],
        [],
    )
    cleaned = MappedTiling(
        Tiling((GriddedCayleyPerm(CayleyPermutation(()), ()),), (), (0, 0)),
        ParameterList(frozenset()),
        (),
        (),
    )

    assert MTCleaner.reap_blank(mt) == cleaned
