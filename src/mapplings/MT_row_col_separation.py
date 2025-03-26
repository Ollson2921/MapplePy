from .mapped_tiling import MappedTiling, Parameter
from gridded_cayley_permutations import Tiling
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope_folder.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)


class MTRowColSeparation:
    def __init__(self, mapped_tiling: MappedTiling):
        self.tiling = mapped_tiling.tiling
        self.avoiding_parameters = mapped_tiling.avoiding_parameters
        self.containing_parameters = mapped_tiling.containing_parameters
        self.enumeration_parameters = mapped_tiling.enumeration_parameters
        self.separation = LessThanRowColSeparation(self.tiling)
        self.preimage_map = self.separation.row_col_map.preimage_map()

    def create_new_param_maps(self, param: Parameter, direction):
        """new_map will map a new parameter to the base tiling.
        temp_map will map a new parameter to the original parameter for backmapping.
        temp_map is usually interleaving, but its fine(?) since it's only for backmapping.
        direction 0 creates the col map, direction 0 creates the row map."""
        new_map, temp_map = dict(), dict()
        additions = 0
        for item in self.preimage_map[direction].items():
            if direction:
                preimages = param.map.preimages_of_row(item[0])
            else:
                preimages = param.map.preimages_of_col(item[0])
            new_additions = len(preimages)
            for i in range(len(item[1])):
                if i:
                    additions += new_additions
                for index in preimages:
                    new_index = index + additions
                    new_map[new_index] = item[1][i]
                    temp_map[new_index] = index
        return new_map, temp_map

    def adjust_parameter(self, param: Parameter):
        """Transforms param into the correct parameter corresponding with the row/col separation of the base tiling.
        Does not do any cleanup."""
        new_col_map, temp_col_map = self.create_new_param_maps(param, 0)
        new_row_map, temp_row_map = self.create_new_param_maps(param, 1)
        temp_parameter = Parameter(
            Tiling([], [], (len(new_col_map), len(new_row_map))),
            RowColMap(temp_col_map, temp_row_map),
        ).back_map_obs_and_reqs(param.ghost)
        return Parameter(temp_parameter.ghost, RowColMap(new_col_map, new_row_map))

    def separate_base_tiling(self):
        """Transforms all of the parameters according to the adjust_parameter function
        Yields a mappling for each tiling produced by row/col separating the base"""
        new_avoiders = [
            self.adjust_parameter(param) for param in self.avoiding_parameters
        ]
        new_containers = []
        for c_list in self.containing_parameters:
            new_c_list = [
                self.adjust_parameter(param) for param in self.containing_parameters
            ]
            new_containers.append(new_c_list)
        new_enumerators = []
        for e_list in self.enumeration_parameters:
            new_e_list = [
                self.adjust_parameter(param) for param in self.enumeration_parameters
            ]
            new_enumerators.append(new_e_list)
        seperated = self.separation.row_col_separation()
        for T in seperated:
            yield MappedTiling(
                T, new_avoiders, new_containers, new_enumerators
            ).full_cleanup()  # Full clean up is probably overkill, we primarily just need backmapping

    @staticmethod
    def separate_parameter(param: Parameter):
        """Row/Col separates a parameter and adjusts the map without altering the base tiling"""
        separation = LessThanRowColSeparation(param.ghost)
        separation_map = separation.row_col_map
        new_col_map = {
            i: param.map.col_map[separation_map.col_map[i]]
            for i in separation_map.col_map
        }
        new_row_map = {
            i: param.map.row_map[separation_map.row_map[i]]
            for i in separation_map.row_map
        }
        for P in separation.row_col_separation():
            return Parameter(P, RowColMap(new_col_map, new_row_map))


class MTRowColSeparation_EQ:
    def __init__(self, mapped_tiling: MappedTiling):
        self.tiling = mapped_tiling.tiling
        self.avoiding_parameters = mapped_tiling.avoiding_parameters
        self.containing_parameters = mapped_tiling.containing_parameters
        self.enumeration_parameters = mapped_tiling.enumeration_parameters
        self.separation = LessThanOrEqualRowColSeparation(self.tiling)
        self.preimage_map = self.separation.row_col_map.preimage_map()

    def create_new_param_maps(self, param: Parameter, direction):
        """new_map will map a new parameter to the base tiling.
        temp_map will map a new parameter to the original parameter for backmapping.
        temp_map is usually interleaving, but its fine(?) since it's only for backmapping.
        direction 0 creates the col map, direction 0 creates the row map."""
        new_map, temp_map = dict(), dict()
        additions = 0
        for item in self.preimage_map[direction].items():
            if direction:
                preimages = param.map.preimages_of_row(item[0])
            else:
                preimages = param.map.preimages_of_col(item[0])
            new_additions = len(preimages)
            for i in range(len(item[1])):
                if i:
                    additions += new_additions
                for index in preimages:
                    new_index = index + additions
                    new_map[new_index] = item[1][i]
                    temp_map[new_index] = index
        return new_map, temp_map

    def adjust_parameter(self, param: Parameter):
        """Transforms param into the correct parameter corresponding with the row/col separation of the base tiling.
        Does not do any cleanup."""
        new_col_map, temp_col_map = self.create_new_param_maps(param, 0)
        new_row_map, temp_row_map = self.create_new_param_maps(param, 1)
        temp_parameter = Parameter(
            Tiling([], [], (len(new_col_map), len(new_row_map))),
            RowColMap(temp_col_map, temp_row_map),
        ).back_map_obs_and_reqs(param.ghost)
        return Parameter(temp_parameter.ghost, RowColMap(new_col_map, new_row_map))

    def separate_base_tiling(self):
        """Transforms all of the parameters according to the adjust_parameter function
        Yields a mappling for each tiling produced by row/col separating the base"""
        new_avoiders = [
            self.adjust_parameter(param) for param in self.avoiding_parameters
        ]
        new_containers = []
        for c_list in self.containing_parameters:
            new_c_list = [
                self.adjust_parameter(param) for param in self.containing_parameters
            ]
            new_containers.append(new_c_list)
        new_enumerators = []
        for e_list in self.enumeration_parameters:
            new_e_list = [
                self.adjust_parameter(param) for param in self.enumeration_parameters
            ]
            new_enumerators.append(new_e_list)
        seperated = self.separation.row_col_separation()
        for T in seperated:
            yield MappedTiling(
                T, new_avoiders, new_containers, new_enumerators
            ).full_cleanup()  # Full clean up is probably overkill, we primarily just need backmapping

    @staticmethod
    def separate_parameter(param: Parameter):
        """Row/Col separates a parameter and adjusts the map without altering the base tiling"""
        separation = LessThanOrEqualRowColSeparation(param.ghost)
        separation_map = separation.row_col_map
        new_col_map = {
            i: param.map.col_map[separation_map.col_map[i]]
            for i in separation_map.col_map
        }
        new_row_map = {
            i: param.map.row_map[separation_map.row_map[i]]
            for i in separation_map.row_map
        }
        for P in separation.row_col_separation():
            yield Parameter(P, RowColMap(new_col_map, new_row_map))
