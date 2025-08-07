"""Testing positive cell validation for parameters"""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings import Parameter


def test_positive_cell_validation():
    """Test less than row col separation for mapplings."""
    T1 = Tiling(
        [],
        [
            [GriddedCayleyPerm((0, 1), ((0, 0), (1, 1)))],
            [GriddedCayleyPerm((0, 1), ((2, 1), (3, 3)))],
            [GriddedCayleyPerm((0, 0), ((0, 2), (2, 2)))],
        ],
        (4, 4),
    )
    T2 = Tiling([GriddedCayleyPerm((1, 0), [(0, 1), (0, 0)])], [], (1, 2))

    P1 = Parameter(T1, RowColMap({0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 0, 2: 1, 3: 1}))
    P2 = Parameter(T1, RowColMap({0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 1, 2: 1, 3: 1}))
    assert not P1.positive_cells_are_valid(T2)
    assert P2.positive_cells_are_valid(T2)
