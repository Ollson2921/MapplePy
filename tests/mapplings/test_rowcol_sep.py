"""Testing row col separation for mapplings."""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation
import pytest
from mapplings import MappedTiling, LTRowColSeparationMT, Parameter


def test_less_than_row_col_separation():
    """Test less than row col separation for mapplings."""
    mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 2))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 3))),
            ),
            (),
            (1, 4),
        ),
        [
            Parameter(
                Tiling(
                    (),
                    (
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                    ),
                    (1, 2),
                ),
                RowColMap({0: 0}, {0: 0, 1: 2}),
            )
        ],
        (),
        (),
    )

    separated_mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
            ),
            (),
            (2, 4),
        ),
        [
            Parameter(
                Tiling(
                    (),
                    (
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),),
                    ),
                    (2, 2),
                ),
                RowColMap({0: 0, 1: 1}, {0: 0, 1: 2}),
            )
        ],
        (),
        (),
    )

    for mappling in LTRowColSeparationMT(mt).separate():
        assert mappling == separated_mt


def test_less_than_row_col_separation_rows():
    """Test less than row col separation for mapplings."""
    mt = MappedTiling(
        Tiling(
            (GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 1))),),
            (),
            (1, 2),
        ),
        [
            Parameter(
                Tiling(
                    (),
                    (
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),),
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                    ),
                    (2, 2),
                ),
                RowColMap({0: 0, 1: 0}, {0: 0, 1: 1}),
            )
        ],
        (),
        (),
    )

    separated_mt = MappedTiling(
        Tiling(
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
            ),
            (),
            (2, 2),
        ),
        [
            Parameter(
                Tiling(
                    (),
                    (
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),),
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),),
                        (GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),),
                    ),
                    (4, 2),
                ),
                RowColMap({0: 0, 1: 0, 2: 1, 3: 1}, {0: 0, 1: 1}),
            )
        ],
        (),
        (),
    )

    for mappling in LTRowColSeparationMT(mt).separate():
        assert mappling == separated_mt
