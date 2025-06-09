"""Testing the reduce_by_fusions function for Parameters."""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation
from mapplings import MTCleaner, ParamCleaner, MappedTiling, Parameter, ParameterList


def test_reduce_by_fusion_rows_and_cols():
    """Test reducing a size 2x2 parameter to a 1x1 parameter
    by fusion."""
    av12 = Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)])], [], (1, 1)
    )
    ghost = Tiling([], [], (2, 2))
    colmap = {0: 0, 1: 0}
    rowmap = {0: 0, 1: 0}
    param = Parameter(ghost, RowColMap(colmap, rowmap)).backmap_all_from_tiling(av12)

    bt = Tiling([], [], (2, 1))
    mt = MappedTiling(bt, (param,), (), ())
    cleaned = MappedTiling(
        Tiling((), (), (2, 1)),
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
        (),
        (),
    )
    param_cleaner = ParamCleaner([ParamCleaner.reduce_by_fusion])
    cleaning_list = [MTCleaner.clean_parameters(param_cleaner)]

    assert MTCleaner.list_cleanup(mt, cleaning_list) == cleaned


param_cleaner = ParamCleaner([ParamCleaner.reduce_by_fusion])
cleaning_list = [MTCleaner.clean_parameters(param_cleaner)]


def test_reduce_by_fusion_3_rows_to_1():
    """Test reducing a size 2x3 parameter to a 2x1 parameter
    by fusion."""
    av12 = Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)])], [], (1, 1)
    )
    ghost = Tiling([], [], (2, 3))
    colmap = {0: 0, 1: 1}
    rowmap = {0: 0, 1: 0, 2: 0}
    param = Parameter(ghost, RowColMap(colmap, rowmap)).backmap_all_from_tiling(av12)

    bt = Tiling([], [], (2, 1))
    mt = MappedTiling(bt, ParameterList((param,)), (), ())

    param_cleaner = ParamCleaner([ParamCleaner.reduce_by_fusion])
    cleaning_list = [MTCleaner.clean_parameters(param_cleaner)]

    cleaned_tiling = MappedTiling(
        Tiling((), (), (2, 1)),
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
                            (2, 1),
                        ),
                        RowColMap({0: 0, 1: 1}, {0: 0}),
                    )
                }
            )
        ),
        (),
        (),
    )

    assert MTCleaner.list_cleanup(mt, cleaning_list) == cleaned_tiling


def test_reduce_by_fusion_dont_fuse_columns():
    """Fuses a 2x2 parameter to a 2x1 parameter, the columns
    are still fuseable but map to different columns in the
    base tiling so shouldn't fuse."""
    ghost = Tiling([], [], (2, 2))
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

    param_cleaner = ParamCleaner([ParamCleaner.reduce_by_fusion])
    cleaning_list = [MTCleaner.clean_parameters(param_cleaner)]
    cleaned = MappedTiling(
        Tiling((), (), (2, 1)),
        ParameterList(frozenset()),
        (
            ParameterList(
                frozenset(
                    {Parameter(Tiling((), (), (2, 1)), RowColMap({0: 0, 1: 1}, {0: 0}))}
                )
            ),
        ),
        (),
    )

    assert MTCleaner.list_cleanup(mt, cleaning_list) == cleaned
