from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from mapplings import MappedTiling, Parameter, ParameterList
from mapplings.algorithms import ParameterPlacement
from mapplings.cleaners import MTCleaner
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings.strategies.mapped_tilescope import MappedTileScopePack
from comb_spec_searcher import CombinatorialSpecificationSearcher

ghost = Tiling.from_vincular_with_obs(CayleyPermutation((0,)), [])
ghost = ghost.add_obstructions(
    (
        GriddedCayleyPerm((0,), [(0, 2)]),
        GriddedCayleyPerm((0,), [(2, 0)]),
        GriddedCayleyPerm((0,), [(0, 1)]),
        GriddedCayleyPerm((0,), [(2, 1)]),
    )
)
P = Parameter(ghost, RowColMap({0: 0, 1: 0, 2: 0}, {0: 0, 1: 0, 2: 0}))
B = Tiling([GriddedCayleyPerm((0, 0), [(0, 0), (0, 0)])], [], (1, 1))

c_list = ParameterList([P])
mappling = MappedTiling(B, [], [c_list], [])
mappling = MTCleaner.full_cleanup(mappling)
c_list = mappling.containing_parameters[0]
print(mappling)

mappling = MTCleaner.full_cleanup(
    ParameterPlacement(mappling, c_list).param_placement(0, 0)
)
print(mappling)
