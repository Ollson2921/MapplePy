from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.tilescope_strategies import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher

# ghost = Tiling(
#     [
#         GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)]),
#         GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 0), (1, 0)]),
#     ],
#     [],
#     (2, 1),
# )


# containing_params = (
#     ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0})),)),
# )
# mappling = MappedTiling(
#     Tiling(
#         [],
#         [],
#         (1, 1),
#     ),
#     [],
#     containing_params,
#     [],
# )
# pack = PointPlacementsPack
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)

# spec = searcher.auto_search(status_update=30)
# spec.show()
# spec.get_genf()

from mapplings.cleaners import MTCleaner

MTCleaner.DEBUG = 2
# ghost = Tiling(
#     [
#         GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
#         GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 1), (0, 1)]),
#         GriddedCayleyPerm(CayleyPermutation([1, 0]), [(1, 1), (1, 1)]),
#     ],
#     [],
#     (2, 2),
# )


# containing_params = (
#     ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0, 1: 0})),)),
# )
# mappling = MappedTiling(
#     Tiling(
#         [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
#         [],
#         (1, 1),
#     ),
#     [],
#     containing_params,
#     [],
# )
# pack = MappedTileScopePack.point_placement(mappling)
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
# spec = searcher.auto_search(status_update=30)
# spec.show()
# spec.get_genf()


mt = MappedTiling(
    Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (1, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (2, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (3, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (1, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (2, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 0), (3, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 0), (2, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 0), (3, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 1), (2, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 1), (3, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 0), (3, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 1), (3, 1))),
        ),
        (),
        (4, 2),
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
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                            ),
                            (),
                            (1, 1),
                        ),
                        RowColMap({0: 0}, {0: 0}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 0),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((2, 2), (2, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 2), (3, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((3, 2), (4, 2))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((4, 2), (4, 2))
                                ),
                            ),
                            (),
                            (5, 3),
                        ),
                        RowColMap({0: 0, 1: 1, 2: 2, 3: 2, 4: 3}, {0: 0, 1: 1, 2: 1}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 0), (1, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                                ),
                            ),
                            (),
                            (5, 3),
                        ),
                        RowColMap({0: 0, 1: 1, 2: 1, 3: 2, 4: 3}, {0: 0, 1: 0, 2: 1}),
                    ),
                    Parameter(
                        Tiling(
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 1),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((4, 2),)),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((0, 0), (0, 0))
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                                ),
                            ),
                            (),
                            (5, 3),
                        ),
                        RowColMap({0: 0, 1: 0, 2: 1, 3: 2, 4: 3}, {0: 0, 1: 0, 2: 1}),
                    ),
                }
            )
        ),
    ),
    (),
)

# print(mt)

cleaned = MTCleaner.full_cleanup(mt)
print(cleaned)
