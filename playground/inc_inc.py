from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.tilescope_strategies import PointPlacementsPack
from comb_spec_searcher import CombinatorialSpecificationSearcher

ghost = Tiling([GriddedCayleyPerm(CayleyPermutation([0, 1]), [(0, 0), (0, 0)]), GriddedCayleyPerm(CayleyPermutation([0, 1]), [(1, 0), (1, 0)])], [], (2, 1))


containing_params = (ParameterList(
    (Parameter(ghost, RowColMap({0:0, 1:0}, {0:0})),)
),)
mappling = MappedTiling(
    Tiling(
        [],
        [],
        (1, 1),
    ),
    [], containing_params,
    [],
)
pack = PointPlacementsPack
searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)

spec = searcher.auto_search(status_update=30)
spec.show()
