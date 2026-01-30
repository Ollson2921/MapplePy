"""Testing the insert_containers cleaning function on
MTCleaner for MappedTiling.

TODO: Tests turned off because they are not working yet in cleaner"""

import pytest
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, Parameter, ParameterList
from mapplings.cleaners import MTCleaner, ParamCleaner

MTCleaner.DEBUG = 2
ParamCleaner.DEBUG = 0


@pytest.mark.skip(reason="strategy not working yet")
def test_insert_containers():
    """Check that the gcps on the ghost are mapped down and the
    containing parameter is removed."""
    req_list = [
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(2, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(2, 1)]),
    ]

    obs = [
        GriddedCayleyPerm(CayleyPermutation([0, 1, 2]), [(0, 0), (1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1, 2]), [(0, 0), (1, 1), (2, 1)]),
    ]

    ghost = Tiling(
        obs,
        [req_list],
        (3, 2),
    )
    colmap = {0: 0, 1: 1, 2: 2}
    rowmap = {0: 0, 1: 1}
    param = Parameter(ghost, RowColMap(colmap, rowmap))
    bt = Tiling([], [], (3, 2))
    mt = MappedTiling(
        bt,
        ParameterList(frozenset()),
        (ParameterList([param]),),
        (),
    )
    cleaning_list = [MTCleaner.insert_containers]
    cleaned_mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 0), (1, 1), (1, 1))
                ),
                GriddedCayleyPerm(
                    CayleyPermutation((0, 1, 2)), ((0, 0), (1, 1), (2, 1))
                ),
            ),
            (
                (
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                    GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                ),
            ),
            (3, 2),
        ),
        ParameterList(frozenset()),
        (),
        (),
    )

    assert MTCleaner.list_cleanup(mt, cleaning_list) == cleaned_mt


@pytest.mark.skip(reason="strategy not working yet")
def test_insert_containers_empty():
    """Check that parameters that don't map to the whole base tiling
    (but are still one-to-one maps) are still mapped down."""
    gcps = [
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 1)]),
    ]

    ghost = Tiling(gcps, [], (2, 2))
    colmap = {0: 0, 1: 1}
    rowmap = {0: 0, 1: 1}
    param = Parameter(ghost, RowColMap(colmap, rowmap))

    colmap = {0: 1, 1: 2}
    param2 = Parameter(ghost, RowColMap(colmap, rowmap))
    bt = Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)])], [], (3, 2)
    )
    mt = MappedTiling(
        bt, ParameterList([]), [ParameterList([param]), ParameterList([param2])], []
    )
    cleaned_mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
            ),
            (),
            (3, 2),
        ),
        ParameterList(frozenset()),
        (),
        (),
    )

    assert MTCleaner.insert_containers(mt) == cleaned_mt
