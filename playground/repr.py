from ..mapplings import MappedTiling, Parameter
from CayleyPerms.gridded_cayley_permutations import Tiling, GriddedCayleyPerm

tiling = Tiling([], [], (1, 1))
print(tiling)

mt = MappedTiling(tiling, [], [], [])
print(mt)
