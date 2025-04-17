from CayleyPerms.gridded_cayley_permutations import Tiling
from CayleyPerms.gridded_cayley_permutations.row_col_map import RowColMap


class Parameter:
    def __init__(self, ghost: Tiling, row_col_map: RowColMap):
        """we may need to keep track of which direction the row_col_map goes"""
        self.map = row_col_map
        self.ghost = ghost

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"({repr(self.ghost)}, {repr(self.map)})"

    def __eq__(self, other) -> bool:
        return self.ghost == other.ghost and self.map == other.map

    def __hash__(self) -> int:
        return hash((self.ghost, self.map))

    def __leq__(self, other) -> int:
        return self.ghost <= other.ghost

    def __lt__(self, other) -> bool:
        return self.ghost < other.ghost

    def __str__(self) -> str:
        return str(self.map) + "\n" + str(self.ghost)
