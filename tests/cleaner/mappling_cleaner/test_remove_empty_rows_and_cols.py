"""Testing the remove_empty_rows_and_cols cleaning function on
MTCleaner for MappedTiling."""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, Parameter, ParameterList
from mapplings.cleaners import MTCleaner


def test_reduce_empty_rowcols_mapped_tiling():
    """Base tiling is a vincular pattern avoiding 1|2|3. Parameter
    is empty, 4x4 mapping onto rows 1,2,3,4 and columns 1,2,3,4.
    Removes empty rows and columns on the base tiling (also removed
    from the ghost)."""
    bt = Tiling.from_vincular(CayleyPermutation([0, 1, 2]), [0, 1])
    ghost = Tiling([], [], (4, 4))
    map_dict = {0: 1, 1: 2, 2: 3, 3: 4}
    param = Parameter(ghost, RowColMap(map_dict, map_dict))
    mt = MappedTiling(
        bt,
        ParameterList(frozenset()),
        (ParameterList((param,)),),
        (),
    )
    cleaning_list = [MTCleaner.remove_empty_rows_and_cols]

    cleaned_mt = MappedTiling(
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
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 3), (2, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 5), (3, 5))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (0, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 1), (4, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (2, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (4, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 5), (0, 5))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 5), (3, 5))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 5), (4, 5))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (4, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (2, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (4, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 5), (3, 5))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 5), (4, 5))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 1), (4, 1))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 3), (4, 3))),
                GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 5), (4, 5))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (0, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 1), (4, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (2, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (4, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 5), (0, 5))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 5), (3, 5))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 5), (4, 5))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (4, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (2, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (4, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 5), (3, 5))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 5), (4, 5))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 1), (4, 1))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 3), (4, 3))),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 5), (4, 5))),
            ),
            (
                (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                (GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 3),)),),
                (GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 5),)),),
            ),
            (5, 7),
        ),
        ParameterList(frozenset()),
        (
            ParameterList(
                frozenset(
                    {
                        Parameter(
                            Tiling((), (), (2, 4)),
                            RowColMap({0: 1, 1: 2}, {0: 1, 1: 2, 2: 3, 3: 4}),
                        )
                    }
                )
            ),
        ),
        (),
    )

    assert MTCleaner.list_cleanup(mt, cleaning_list) == cleaned_mt


def test_empty_base_tiling():
    """The base tiling is multiple empty rows and columns."""
    obs = [
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 1)]),
    ]
    bt = Tiling(obs, [], (2, 2))
    map_dict = {0: 0, 1: 1, 2: 1}

    ghost = Tiling([], [obs], (3, 3))
    param = Parameter(ghost, RowColMap(map_dict, map_dict))
    mt = MappedTiling(
        bt,
        (param,),
        (ParameterList([param]),),
        (),
    )
    cleaned_tiling = MappedTiling(
        Tiling((GriddedCayleyPerm(CayleyPermutation(tuple()), tuple()),), (), (0, 0)),
        [],
        [],
        [],
    )

    cleaning_list = [MTCleaner.remove_empty_rows_and_cols]
    assert MTCleaner.list_cleanup(mt, cleaning_list) == cleaned_tiling
