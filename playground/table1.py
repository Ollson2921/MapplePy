from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.tilescope_strategies import PointPlacementsPack
from comb_spec_searcher import CombinatorialSpecificationSearcher

"""Row 1"""
## Basis 1 ##
# til = MappedTiling.from_vincular(CayleyPermutation([0, 1, 2]), [])
# ghost = til.delete_columns([2])

# til2 = MappedTiling.from_vincular(CayleyPermutation([2, 1, 0]), [])
# ghost2 = til2.delete_columns([4])

# avoiding_parameters = [
#     Parameter(ghost, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
#     Parameter(ghost2, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
# ]
# mappling = MappedTiling(
#     Tiling(
#         [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
#         [],
#         (1, 1),
#     ),
#     avoiding_parameters,
#     [],
#     [],
# )
# pack = PointPlacementsPack
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
# spec = searcher.auto_search(status_update=30)
# spec.show()
# spec.get_genf()

## Basis 2 ##

# til3 = MappedTiling.from_vincular(CayleyPermutation([2, 1, 0]), [])
# ghost3 = til3.delete_columns([2])

# til4 = MappedTiling.from_vincular(CayleyPermutation([0, 1, 2]), [])
# ghost4 = til4.delete_columns([4])

# avoiding_parameters = [
#     Parameter(ghost3, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
#     Parameter(ghost4, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
# ]
# mappling = MappedTiling(
#     Tiling(
#         [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
#         [],
#         (1, 1),
#     ),
#     avoiding_parameters,
#     [],
#     [],
# )
# pack = PointPlacementsPack
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
# spec = searcher.auto_search(status_update=30)
# spec.show()
# spec.get_genf()

"""Row 2"""
## Basis 1 ##
til = MappedTiling.from_vincular(CayleyPermutation([0, 1, 2]), [])
ghost = til.delete_columns([2])

til2 = MappedTiling.from_vincular(CayleyPermutation([2, 1, 0]), [])
ghost2 = til2.delete_columns([2])

avoiding_parameters = [
    Parameter(ghost, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
    Parameter(ghost2, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
]
mappling = MappedTiling(
    Tiling(
        [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
        [],
        (1, 1),
    ),
    avoiding_parameters,
    [],
    [],
)
pack = PointPlacementsPack
searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
spec = searcher.auto_search(status_update=30)
spec.show()
spec.get_genf()

## Basis 2 ##

# til3 = MappedTiling.from_vincular(CayleyPermutation([2, 1, 0]), [])
# ghost3 = til3.delete_columns([4])

# til4 = MappedTiling.from_vincular(CayleyPermutation([0, 1, 2]), [])
# ghost4 = til4.delete_columns([4])

# avoiding_parameters = [
#     Parameter(ghost3, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
#     Parameter(ghost4, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
# ]
# mappling = MappedTiling(
#     Tiling(
#         [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
#         [],
#         (1, 1),
#     ),
#     avoiding_parameters,
#     [],
#     [],
# )
# pack = PointPlacementsPack
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
# spec = searcher.auto_search(status_update=30)
# spec.show()
# spec.get_genf()

"""Row 3"""
## Basis 1 ##
# til = MappedTiling.from_vincular(CayleyPermutation([0, 1, 2]), [])
# ghost = til.delete_columns([2])

# til2 = MappedTiling.from_vincular(CayleyPermutation([1, 2, 0]), [])
# ghost2 = til2.delete_columns([2])

# avoiding_parameters = [
#     Parameter(ghost, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
#     Parameter(ghost2, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
# ]
# mappling = MappedTiling(
#     Tiling(
#         [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
#         [],
#         (1, 1),
#     ),
#     avoiding_parameters,
#     [],
#     [],
# )
# pack = PointPlacementsPack
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
# spec = searcher.auto_search(status_update=30)
# spec.show()
# spec.get_genf()

## Basis 2 ##

# til3 = MappedTiling.from_vincular(CayleyPermutation([2, 1, 0]), [])
# ghost3 = til2.delete_columns([2])

# til4 = MappedTiling.from_vincular(CayleyPermutation([1, 0, 2]), [])
# ghost4 = til2.delete_columns([2])

# avoiding_parameters = [
#     Parameter(ghost3, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
#     Parameter(ghost4, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
# ]
# mappling = MappedTiling(
#     Tiling(
#         [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
#         [],
#         (1, 1),
#     ),
#     avoiding_parameters,
#     [],
#     [],
# )
# pack = PointPlacementsPack
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
# spec = searcher.auto_search(status_update=30)
# spec.show()
# spec.get_genf()

## Basis 3 ##
# til = MappedTiling.from_vincular(CayleyPermutation([0, 1, 2]), [])
# ghost = til.delete_columns([4])

# til2 = MappedTiling.from_vincular(CayleyPermutation([2, 0, 1]), [])
# ghost2 = til2.delete_columns([4])

# avoiding_parameters = [
#     Parameter(ghost, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
#     Parameter(ghost2, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
# ]
# mappling = MappedTiling(
#     Tiling(
#         [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
#         [],
#         (1, 1),
#     ),
#     avoiding_parameters,
#     [],
#     [],
# )
# pack = PointPlacementsPack
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
# spec = searcher.auto_search(status_update=30)
# spec.show()
# spec.get_genf()

## Basis 4 ##

# til3 = MappedTiling.from_vincular(CayleyPermutation([2, 1, 0]), [])
# ghost3 = til3.delete_columns([4])

# til4 = MappedTiling.from_vincular(CayleyPermutation([0, 2, 1]), [])
# ghost4 = til4.delete_columns([4])

# avoiding_parameters = [
#     Parameter(ghost3, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
#     Parameter(ghost4, RowColMap({i: 0 for i in range(6)}, {i: 0 for i in range(7)})),
# ]
# mappling = MappedTiling(
#     Tiling(
#         [GriddedCayleyPerm(CayleyPermutation([0, 0]), [(0, 0), (0, 0)])],
#         [],
#         (1, 1),
#     ),
#     avoiding_parameters,
#     [],
#     [],
# )
# pack = PointPlacementsPack
# searcher = CombinatorialSpecificationSearcher(mappling, pack, debug=False)
# spec = searcher.auto_search(status_update=30)
# spec.show()
# spec.get_genf()
