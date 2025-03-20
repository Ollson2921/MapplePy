from .mapped_tiling import MappedTiling, Parameter
from gridded_cayley_permutations import Tiling
from tilescope_folder.strategies.row_column_separation import LessThanRowColSeparation

class MTRowColSeperation:
    def __init__(self, mapped_tiling: MappedTiling):
        self.tiling = mapped_tiling.tiling
        self.avoiding_parameters = mapped_tiling.avoiding_parameters
        self.containing_parameters = mapped_tiling.containing_parameters
        self.enumeration_parameters = mapped_tiling.enumeration_parameters

    def row_col_seperation_(self):
        pass

