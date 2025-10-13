from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.tilescope_strategies import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher
from mapplings.cleaners import MTCleaner
from itertools import combinations_with_replacement
from mapplings.strategies.tilescope_strategies import (
    CellInsertionFactory,
    MapplingPointPlacementFactory,
    CleaningStrategy,
    MapplingFactorStrategy,
    MapplingLessThanOrEqualRowColSeparationStrategy,
    MapplingLessThanRowColSeparationStrategy,
)
# MTCleaner.DEBUG = 2

# L3
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([1, 0]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)

# L4
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([0,1]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([1,0]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0,1]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)
# L7
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1,0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([1,0]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([1,0]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)
# L1
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1,0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0,1]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0,1]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)
# L5
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([1,0]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([1,0]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0,1]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)
# L0
ghost = Tiling(
    [
        GriddedCayleyPerm(CayleyPermutation([0,1]), [(0, 0), (0, 0)]),
        GriddedCayleyPerm(CayleyPermutation([0,1]), [(0, 1), (0, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0,1]), [(1, 1), (1, 1)]),
        GriddedCayleyPerm(CayleyPermutation([0]), [(1, 0)]),
    ],
    [],
    (2, 2),
)


containing_params = (
    ParameterList((Parameter(ghost, RowColMap({0: 0, 1: 0}, {0: 0, 1: 0})),)),
)
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    [],
    containing_params,
    [],
)
pack = MappedTileScopePack.point_placement(mappling)
searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
spec = searcher.auto_search(status_update=30)
spec.show()
spec.get_genf()
