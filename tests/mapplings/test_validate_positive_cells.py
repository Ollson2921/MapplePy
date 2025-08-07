"""Testing positive cell validation for parameters"""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings import Parameter


def test_positive_cell_validation():
    """Test that we're validating the positive cells correctly."""
    t1 = Tiling(
        [],
        [
            [GriddedCayleyPerm((0, 1), ((0, 0), (1, 1)))],
            [GriddedCayleyPerm((0, 1), ((2, 1), (3, 3)))],
            [GriddedCayleyPerm((0, 0), ((0, 2), (2, 2)))],
        ],
        (4, 4),
    )
    t2 = Tiling([GriddedCayleyPerm((1, 0), [(0, 1), (0, 0)])], [], (1, 2))

    p1 = Parameter(t1, RowColMap({0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 0, 2: 1, 3: 1}))
    p2 = Parameter(t1, RowColMap({0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 1, 2: 1, 3: 1}))
    assert not p1.positive_cells_are_valid(t2)
    assert p2.positive_cells_are_valid(t2)
