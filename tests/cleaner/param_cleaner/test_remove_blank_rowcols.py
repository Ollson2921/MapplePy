"""Testing the remove_blank_rows_and_cols function for Parameters."""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, Parameter, ParameterList
from mapplings.cleaners import MTCleaner, ParamCleaner


def test_remove_blank_rowcols():
    """Test removing blank rows and columns from a parameter."""
    ghost = Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)])], [], (2, 2)
    )
    colmap = {0: 0, 1: 1}
    rowmap = {0: 0, 1: 0}
    param = Parameter(ghost, RowColMap(colmap, rowmap))

    bt = Tiling([], [], (2, 1))
    mt = MappedTiling(
        bt,
        ParameterList(frozenset()),
        (ParameterList([param]),),
        (),
    )

    param_cleaner = ParamCleaner([ParamCleaner.remove_blank_rows_and_cols])
    cleaning_list = [MTCleaner.clean_parameters(param_cleaner)]

    cleaned = MappedTiling(
        Tiling((), (), (2, 1)),
        ParameterList(frozenset()),
        (
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling(
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0, 1)), ((0, 0), (0, 0))
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

    assert MTCleaner.list_cleanup(mt, cleaning_list) == cleaned
