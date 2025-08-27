from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling, MTCleaner, ParamCleaner, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from itertools import combinations_with_replacement
from mapplings.strategies.tilescope_strategies import (
    CellInsertionFactory,
    MapplingPointPlacementFactory,
    CleaningStrategy,
    MapplingFactorStrategy,
    MapplingLessThanOrEqualRowColSeparationStrategy,
    MapplingLessThanRowColSeparationStrategy,
    PointPlacementsPack,
)
from comb_spec_searcher.exception import StrategyDoesNotApply
from comb_spec_searcher import CombinatorialSpecificationSearcher

all_obs = []
for i in [1, 3, 5]:
    for j in range(7):
        if i == j:
            continue
        all_obs.append(GriddedCayleyPerm(CayleyPermutation([0]), ((i, j),)))
for i in range(7):
    all_obs.append(GriddedCayleyPerm(CayleyPermutation([0]), ((i, 4),)))

reqs = []
for i in [1, 3, 5]:
    all_obs.append(GriddedCayleyPerm(CayleyPermutation([0, 0]), ((i, i), (i, i))))
    all_obs.append(GriddedCayleyPerm(CayleyPermutation([0, 1]), ((i, i), (i, i))))
    all_obs.append(GriddedCayleyPerm(CayleyPermutation([1, 0]), ((i, i), (i, i))))
    reqs.append([GriddedCayleyPerm(CayleyPermutation([0]), ((i, i),))])

for i in [1, 3, 5]:
    cells_in_row = []
    for j in range(7):
        cells_in_row.append((j, i))
    for subset in combinations_with_replacement(cells_in_row, 2):
        all_obs.append(GriddedCayleyPerm(CayleyPermutation([0, 1]), subset))
        all_obs.append(GriddedCayleyPerm(CayleyPermutation([1, 0]), subset))

# print(all_obs)
ghost = Tiling(all_obs, reqs, (7, 7))
# print(ghost)
avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(7)}, {i: 0 for i in range(7)}))
]
mappling = MappedTiling(
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

print(mappling)

# comb_classes = set()
# factory = CellInsertionFactory()
# for strategy in factory(mappling):
#     rule = strategy(mappling)
#     print(rule)
#     comb_classes.update(rule.children)

# ppfactroy = MapplingPointPlacementFactory()
# for mappling in set(comb_classes):
#     for strategy in ppfactroy(mappling):
#         rule = strategy(mappling)
#         print(rule)
#         comb_classes.update(rule.children)

# strategy = CleaningStrategy()
# for mappling in set(comb_classes):
#     rule = strategy(mappling)
#     print(rule)
#     # rule._sanity_check_count(3)
#     comb_classes.update(rule.children)
#     if (rule.comb_class,) != rule.children:
#         comb_classes.remove(rule.comb_class)

# strategy = MapplingFactorStrategy()
# for mappling in set(comb_classes):
#     try:
#         rule = strategy(mappling)
#     except StrategyDoesNotApply:
#         continue
#     print(rule)
#     comb_classes.update(rule.children)
#     comb_classes.remove(rule.comb_class)

# strategy = MapplingLessThanRowColSeparationStrategy()
# for mappling in set(comb_classes):
#     rule = strategy(mappling)
#     comb_classes.update(rule.children)
#     if (rule.comb_class,) != rule.children:
#         comb_classes.remove(rule.comb_class)
#         print(rule)

# strategy = MapplingLessThanOrEqualRowColSeparationStrategy()
# for mappling in set(comb_classes):
#     rule = strategy(mappling)
#     comb_classes.update(rule.children)
#     if (rule.comb_class,) != rule.children:
#         comb_classes.remove(rule.comb_class)
#         print(rule)

# for i in range(10):
#     print(mappling.get_terms(i))
M0 = MTCleaner.full_cleanup(mappling)
# searcher = CombinatorialSpecificationSearcher(M0, PointPlacementsPack, debug=False)

# spec = searcher.auto_search(status_update=10)
cleaner = MTCleaner.make_full_cleaner()


print(M0)

print("------------------ Cell Insertion ------------------")
M1 = list(list(CellInsertionFactory()(M0))[0].decomposition_function(M0))[1]
print(M1)

print("------------------ Placed Rightmost ------------------")
M2 = list(list(MapplingPointPlacementFactory()(M1))[0].decomposition_function(M1))[1]
M3 = cleaner(M2)
print(M3)


print("------------------ Factored ------------------")
M4 = cleaner(list(MapplingFactorStrategy().decomposition_function(M3))[0])

print(M4)
print("------------------ RC Seperation ------------------")
M5 = list(MapplingLessThanRowColSeparationStrategy().decomposition_function(M4))[0]

M6 = cleaner(M5)
print(M6)
print("------------------ Factored ------------------")
M7 = list(MapplingFactorStrategy().decomposition_function(M6))[1]
print(M7)
M7 = cleaner(M7)
print("------------------ Cell Insertion ------------------")
M8 = list(list(CellInsertionFactory()(M7))[0].decomposition_function(M7))[1]
print(M8)

print("------------------ Placed Top-Rightmost ------------------")
M9 = list(list(MapplingPointPlacementFactory()(M8))[1].decomposition_function(M8))[1]
M10 = cleaner(M9)
print(cleaner(M10))
print("------------------ Factored ------------------")
M11 = list(MapplingFactorStrategy().decomposition_function(M10))[1]
M12 = cleaner(M11)
print(M12)
print(M12 == M0)


MM = MappedTiling(
    Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((0, 1), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 0), (0, 1))),
            GriddedCayleyPerm(CayleyPermutation((0, 2, 1)), ((0, 0), (0, 0), (0, 0))),
            GriddedCayleyPerm(CayleyPermutation((0, 2, 1)), ((0, 1), (0, 1), (0, 1))),
        ),
        (),
        (1, 2),
    ),
    ParameterList(
        frozenset(
            {
                Parameter(
                    Tiling(
                        (
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                            ),
                        ),
                        (
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                        ),
                        (3, 3),
                    ),
                    RowColMap({0: 0, 1: 0, 2: 0}, {0: 0, 1: 0, 2: 1}),
                ),
                Parameter(
                    Tiling(
                        (
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 4),)),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 0)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 0)), ((3, 2), (3, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (0, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (0, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (3, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 2), (3, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((3, 2), (3, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((3, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((4, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((4, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (0, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (0, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (3, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (1, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 1), (2, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 2), (3, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((3, 2), (3, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((3, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((4, 1), (4, 1))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((4, 2), (4, 2))
                            ),
                        ),
                        (
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),),
                        ),
                        (5, 5),
                    ),
                    RowColMap(
                        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, {0: 0, 1: 0, 2: 0, 3: 0, 4: 1}
                    ),
                ),
                Parameter(
                    Tiling(
                        (
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
                            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 4),)),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 0)), ((1, 2), (1, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 0)), ((3, 3), (3, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (0, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (1, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 3), (0, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 3), (2, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 3), (3, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((0, 3), (4, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 2), (1, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((1, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 3), (2, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 3), (3, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((2, 3), (4, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((3, 3), (3, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((3, 3), (4, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((4, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((0, 1)), ((4, 3), (4, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (0, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (1, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 3), (0, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 3), (2, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 3), (3, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((0, 3), (4, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 2), (1, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((1, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 2), (2, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 3), (2, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 3), (3, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((2, 3), (4, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((3, 3), (3, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((3, 3), (4, 3))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((4, 2), (4, 2))
                            ),
                            GriddedCayleyPerm(
                                CayleyPermutation((1, 0)), ((4, 3), (4, 3))
                            ),
                        ),
                        (
                            (
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
                            ),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),),
                            (GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)),),
                        ),
                        (5, 5),
                    ),
                    RowColMap(
                        {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, {0: 0, 1: 1, 2: 1, 3: 1, 4: 1}
                    ),
                ),
            }
        )
    ),
    (),
    (),
)


P = Parameter(
    Tiling(
        (
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 3),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 4),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 0),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 1),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 2),)),
            GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 4),)),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((1, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 0)), ((3, 3), (3, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (0, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 2), (4, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (0, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (2, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (3, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((0, 3), (4, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((1, 2), (4, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 2), (4, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (2, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (3, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((2, 3), (4, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 3), (3, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((3, 3), (4, 3))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 2), (4, 2))),
            GriddedCayleyPerm(CayleyPermutation((0, 1)), ((4, 3), (4, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (0, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 2), (4, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (0, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (2, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (3, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((0, 3), (4, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (1, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((1, 2), (4, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (2, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 2), (4, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (2, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (3, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((2, 3), (4, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 3), (3, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((3, 3), (4, 3))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 2), (4, 2))),
            GriddedCayleyPerm(CayleyPermutation((1, 0)), ((4, 3), (4, 3))),
        ),
        (
            (
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),)),
                GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 1),)),
            ),
            (GriddedCayleyPerm(CayleyPermutation((0,)), ((1, 2),)),),
            (GriddedCayleyPerm(CayleyPermutation((0,)), ((3, 3),)),),
        ),
        (5, 5),
    ),
    RowColMap({0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, {0: 0, 1: 1, 2: 1, 3: 1, 4: 1}),
)
