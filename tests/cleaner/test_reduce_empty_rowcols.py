"""Testing the reduce_empty_rows_and_cols function for MappedTiling
and for Parameters."""

import pytest
from mapplings import MTCleaner, ParamCleaner, MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation


def test_reduce_empty_rowcols_parameter():
    """Mappling with empty 1x1 base tiling and parameter that is a
    vincular pattern avoiding 1|2|3. Removes empty rows and columns
    on the parameter."""
    ghost = Tiling.from_vincular(CayleyPermutation([0, 1, 2]), [0, 1])
    map_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    param = Parameter(ghost, RowColMap(map_dict, map_dict))
    bt = Tiling([], [], (1, 1))
    mt = MappedTiling(bt, ParameterList([param]), ParameterList([]), ParameterList([]))
    param_cleaner = ParamCleaner([ParamCleaner.reduce_empty_rows_and_cols])
    cleaning_list = [MTCleaner.clean_parameters(param_cleaner)]

    reduced_mt = MappedTiling(
        Tiling((), (), (1, 1)),
        ParameterList(
            frozenset(
                {
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 5),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 6),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 4),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 5),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 6),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 4),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 6),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 0)), ((3, 5), (3, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 3), (0, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 5), (0, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 5), (3, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 5), (4, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 5), (3, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((3, 5), (4, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((4, 5), (4, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 3), (0, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 5), (0, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 5), (3, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 5), (4, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (2, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 5), (3, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 5), (4, 5))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 1), (4, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 3), (4, 3))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 5), (4, 5))
                                ),
                            ),
                            (
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((1, 1),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((2, 3),)
                                    ),
                                ),
                                (
                                    GriddedCayleyPerm(
                                        CayleyPermutation((0,)), ((3, 5),)
                                    ),
                                ),
                            ),
                            (5, 7),
                        ),
                        RowColMap(
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
                            {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
                        ),
                    )
                }
            )
        ),
        (),
        (),
    )

    assert MTCleaner.list_cleanup(mt, cleaning_list) == reduced_mt
