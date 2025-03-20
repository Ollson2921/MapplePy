from .mapped_tiling import MappedTiling, Parameter
from gridded_cayley_permutations import Tiling
from tilescope_folder.strategies.row_column_separation import LessThanRowColSeparation

class MTRowColSeperation:
    def __init__(self, mapped_tiling: MappedTiling):
        self.tiling = mapped_tiling.tiling
        self.avoiding_parameters = mapped_tiling.avoiding_parameters
        self.containing_parameters = mapped_tiling.containing_parameters
        self.enumeration_parameters = mapped_tiling.enumeration_parameters
        self.seperation = LessThanRowColSeparation(self.tiling)

    def adjust_parameter_size(self, param : Parameter):
        preimage_map = self.seperation.row_col_map.preimage_map()
        new_map = param.map
        for item in sorted(list(preimage_map[0].items()))[::-1]:
            if len[item[1]] > 1:
                col_preimages = param.map.preimages_of_col(item[0])
                new_map = new_map.expand_row_col_map_at_index(len(col_preimages),0,max(col_preimages),0)
        for item in sorted(list(preimage_map[1].items()))[::-1]:
            if len[item[1]] > 1:
                row_preimages = param.map.preimages_of_row(item[0])
                new_map = new_map.expand_row_col_map_at_index(0,len(row_preimages),0,max(row_preimages))
        new_param = Parameter(Tiling([],[],(len(new_map.col_map),len(new_map.row_map))),new_map).back_map_obs_and_reqs(param.ghost)
        # From here, figure out the map from new_param to new base
        return new_param
    
    def seperate_base_tiling(self):
        # Row col seperate the base tiling - map from old base cells to new base cells
        # Figure out the dimension each new param should be - map from new param cells to old param cells
        # back map old param onto new param
        # New row col map is a composition of a bunch of row col maps
        pass

    def seperate_parameters(self):
        pass

