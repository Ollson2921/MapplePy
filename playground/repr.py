from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm

tiling = Tiling([], [], (1, 1))
print(repr(tiling))

mt = MappedTiling(tiling, ParameterList([]), [], [])
print(repr(mt))
