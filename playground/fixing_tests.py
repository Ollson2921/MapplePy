# import pytest
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies import MappedTileScopePack
from comb_spec_searcher import (
    CombinatorialSpecificationSearcher,
    CombinatorialSpecification,
)
import json


til = Tiling.create_vincular_or_bivincular(CayleyPermutation([0, 1, 2]))
ghost = til.delete_rows([4])
avoiding_parameter = Parameter(
    ghost, RowColMap({i: 0 for i in range(7)}, {i: 0 for i in range(6)})
)
avoiding_parameters = [avoiding_parameter]
motzkin_mappling = MappedTiling(
    Tiling(
        [
            GriddedCayleyPerm(CayleyPermutation([0, 2, 1]), ((0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), [(0, 0), (0, 0)]),
        ],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)


# pack = MappedTileScopePack.point_placement(motzkin_mappling)
# searcher = CombinatorialSpecificationSearcher(motzkin_mappling, pack, debug=False)
# spec = searcher.auto_search()
# spec.show()

# for mt in spec.comb_classes():
#     print(mt)
#     print(repr(mt))

# spec_counts = [spec.count_objects_of_size(i) for i in range(9)]
# print(spec_counts)
# assert spec_counts == [1, 1, 2, 4, 9, 21, 51, 127, 323]

# json_dict = spec.to_jsonable()
# json_str = json.dumps(json_dict)
# load_dict = json.loads(json_str)
# reloaded_spec = CombinatorialSpecification.from_dict(load_dict)
# assert spec == reloaded_spec
# spec_counts = [spec.count_objects_of_size(i) for i in range(9)]
# assert spec_counts == [1, 1, 2, 4, 9, 21, 51, 127, 323]


mt = MappedTiling(
    Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((2, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (2, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((2, 0), (2, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (2, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 1), (1, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 2, 1)), ((0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 2, 1)), ((2, 0), (2, 0), (2, 0))),
        ),
        ((GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),),
        (3, 2),
    ),
    ParameterList(
        frozenset(
            {
                Parameter(
                    Tiling(
                        (
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                            ),
                        ),
                        (
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1)), ((0, 0), (0, 1))
                                ),
                            ),
                        ),
                        (2, 2),
                    ),
                    RowColMap({0: 0, 1: 2}, {0: 0, 1: 0}),
                ),
                Parameter(
                    Tiling(
                        (
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (0, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (1, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (0, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (1, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                            ),
                        ),
                        (
                            (
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1, 2)),
                                    ((0, 0), (0, 1), (0, 2)),
                                ),
                                GriddedCayleyPerm(
                                    CayleyPermutation((0, 1, 2)),
                                    ((1, 0), (1, 1), (1, 2)),
                                ),
                            ),
                        ),
                        (2, 4),
                    ),
                    RowColMap({0: 0, 1: 2}, {0: 0, 1: 0, 2: 0, 3: 0}),
                ),
            }
        )
    ),
    (),
    (),
)

# print(mt)
from mapplings.strategies.tilescope_strategies import (
    MapplingLessThanOrEqualRowColSeparationFactory,
)
from mapplings.algorithms.row_col_sep_mt import (
    MTLTRowColSeparation,
    MTLTORERowColSeparation,
)

# all_separated = list(MTLTORERowColSeparation(mt).separate())
# for out in all_separated:
#     print(out)


bt = Tiling(
    (
        GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (1, 0))),
        GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (1, 0))),
    ),
    (),
    (2, 2),
)

ghost = Tiling(
    (GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),),
    (),
    (2, 5),
)
param = Parameter(ghost, RowColMap({0: 0, 1: 1}, {0: 0, 1: 0, 2: 0, 3: 1, 4: 1}))
mt = MappedTiling(bt, ParameterList(frozenset({param})), (), ())
print(mt)

all_separated = list(MTLTRowColSeparation(mt).separate())
for out in all_separated:
    print(out)
