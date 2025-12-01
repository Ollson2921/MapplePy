from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter
from mapplings.cleaners import MTCleaner
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher


til = MappedTiling.from_vincular(CayleyPermutation([0, 1, 2]), [])
ghost = til.delete_rows([4])
avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(7)}, {i: 0 for i in range(6)}))
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

pack = MappedTileScopePack.point_placement(mappling)
searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)

spec = searcher.auto_search(status_update=10)
spec.show()
