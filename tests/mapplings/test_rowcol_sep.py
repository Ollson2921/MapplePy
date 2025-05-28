from mapplings import MappedTiling, LTRowColSeparationMT, Parameter

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation
import pytest


def test_LTRowColSeparationMT():
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

    for mappling in LTRowColSeparationMT(mt).separate_base_tiling():
        assert mappling == separated_mt
