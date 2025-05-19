from mapplings import MappedTiling, Parameter, MTCleaner
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm

tiling = Tiling([], [], (1, 1))
print(repr(tiling))

mt = MappedTiling(tiling, [], [], [])
print(repr(mt))

print(MTCleaner.registered_functions)
