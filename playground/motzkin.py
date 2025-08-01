from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from mapplings import Parameter, MappedTiling
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

searcher = CombinatorialSpecificationSearcher(mappling, PointPlacementsPack, debug=True)

spec = searcher.auto_search(status_update=30)
