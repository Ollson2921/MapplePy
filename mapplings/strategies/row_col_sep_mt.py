"""Module for row and column separating mapped tilings and related strategies."""

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
)
from ..mapped_tiling import MappedTiling, Parameter


class LTRowColSeparationMT:
    """
    When separating, cells must be strictly above/below each other.
    """

    def __init__(self, mapped_tiling: MappedTiling, or_equal=False):
        self.tiling = mapped_tiling.tiling
        self.avoiding_parameters = mapped_tiling.avoiding_parameters
        self.containing_parameters = mapped_tiling.containing_parameters
        self.enumeration_parameters = mapped_tiling.enumerating_parameters
        if or_equal:
            self.separation = LessThanOrEqualRowColSeparation(self.tiling)
        else:
            self.separation = LessThanRowColSeparation(self.tiling)
        self.preimage_map = self.separation.row_col_map.preimage_map()

    def base_extensions(self) -> tuple:
        """Returns how many new rows/cols are added to the new base tiling
        for each row/col in the original tiling"""
        row_extensions = [
            (len(self.preimage_map[1][i]) - 1) for i in range(len(self.preimage_map[1]))
        ]
        col_extensions = [
            (len(self.preimage_map[0][i]) - 1) for i in range(len(self.preimage_map[0]))
        ]
        return col_extensions, row_extensions

    def parameter_extensions(self, base_extensions, param: Parameter):
        """Returns how many rows/cols must be added to the new parameter
        for each row/col in the original tiling"""
        col_parameter_extensions = [
            base_extensions[0][i] * len(param.map.preimages_of_col(i))
            for i in range(len(base_extensions[0]))
        ]
        row_parameter_extensions = [
            base_extensions[1][i] * len(param.map.preimages_of_row(i))
            for i in range(len(base_extensions[1]))
        ]
        return col_parameter_extensions, row_parameter_extensions

    def total_extensions(self, parameter_extensions):
        """Returns how far each preimage group moves in the new parameter"""
        total_extensions = (
            [0]
            + [
                sum(parameter_extensions[0][: k + 1])
                for k in range(len(parameter_extensions[0]))
            ],
            [0]
            + [
                sum(parameter_extensions[1][: k + 1])
                for k in range(len(parameter_extensions[1]))
            ],
        )
        return total_extensions

    def cell_map(self, total_extensions, param: Parameter):
        """Maps each cell of the original parameter to the correct active cell
        in the new parameter."""
        cell_map = {}
        for i in range(param.ghost.dimensions[0]):
            for j in range(param.ghost.dimensions[1]):
                cell_map[(i, j)] = (
                    i + total_extensions[0][param.map.col_map[i]],
                    j + total_extensions[1][param.map.row_map[j]],
                )
        inequalities = self.separation.column_row_inequalities()
        cells_to_move = set(pair[1] for pair in inequalities[0])
        for base_cell in cells_to_move:
            if base_cell in param.image_cells():
                for cell in param.map.preimage_of_cell(base_cell):
                    cell_map[cell] = (
                        cell_map[cell][0] + total_extensions[0][base_cell[0] + 1],
                        cell_map[cell][1],
                    )
        cells_to_move = set(pair[1] for pair in inequalities[1])
        for base_cell in cells_to_move:
            if base_cell in param.image_cells():
                for cell in param.map.preimage_of_cell(base_cell):
                    cell_map[cell] = (
                        cell_map[cell][0],
                        cell_map[cell][1] + total_extensions[1][base_cell[1] + 1],
                    )
        return cell_map

    def transform_gcp(self, cell_map, gcp: GriddedCayleyPerm) -> GriddedCayleyPerm:
        """Moves a GCP to the correct cell"""
        new_positions = (cell_map[position] for position in gcp.positions)
        return GriddedCayleyPerm(gcp.pattern, new_positions)

    def make_new_map(self, param: Parameter, direction, parameter_extensions):
        """Makes the RowColMap from a new parameter to the new base tiling"""
        new_map = {}
        additions = 0
        for item in self.preimage_map[direction].items():
            if direction:
                preimages = param.map.preimages_of_row(item[0])
            else:
                preimages = param.map.preimages_of_col(item[0])
            to_add = parameter_extensions[direction][item[0]]
            for i in range(len(item[1])):
                if i:
                    additions += to_add
                for index in preimages:
                    new_index = index + additions
                    new_map[new_index] = item[1][i]
        return new_map

    def make_new_parameter(self, base_extensions, param: Parameter) -> Parameter:
        """Returns the adjusted param after row/col separation"""
        param_extensions = self.parameter_extensions(base_extensions, param)
        total_extensions = self.total_extensions(param_extensions)
        new_dimensions = (
            param.ghost.dimensions[0] + total_extensions[0][-1],
            param.ghost.dimensions[1] + total_extensions[1][-1],
        )
        cell_map = self.cell_map(total_extensions, param)
        new_obstructions = [
            self.transform_gcp(cell_map, ob) for ob in param.ghost.obstructions
        ]
        new_requirements = [
            [self.transform_gcp(cell_map, req) for req in req_list]
            for req_list in param.ghost.requirements
        ]
        new_ghost = Tiling(new_obstructions, new_requirements, new_dimensions)
        new_map = RowColMap(
            self.make_new_map(param, 0, param_extensions),
            self.make_new_map(param, 1, param_extensions),
        )

        return Parameter(new_ghost, new_map)

    def separate(self):
        """Returns the row/col seperated mappling"""
        base_extensions = self.base_extensions()
        new_avoiders = [
            self.make_new_parameter(base_extensions, param)
            for param in self.avoiding_parameters
        ]
        new_containers = [
            [self.make_new_parameter(base_extensions, param) for param in c_list]
            for c_list in self.containing_parameters
        ]
        new_enumerators = [
            [self.make_new_parameter(base_extensions, param) for param in e_list]
            for e_list in self.enumeration_parameters
        ]
        for base in self.separation.row_col_separation():
            yield MappedTiling(base, new_avoiders, new_containers, new_enumerators)

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
        for parameter in separation.row_col_separation():
            yield Parameter(parameter, RowColMap(new_col_map, new_row_map))
