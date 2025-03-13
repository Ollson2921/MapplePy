from mapplings import MappedTiling, Parameter
from gridded_cayley_permutations import GriddedCayleyPerm
from cayley_permutations import CayleyPermutation
from typing import Tuple, Dict, Iterable
from gridded_cayley_permutations.point_placements import PointPlacement
from gridded_cayley_permutations.row_col_map import RowColMap
from .MT_point_placement import MTRequirementPlacement


class ParameterPlacement:
    """For a given mappling and containing parameter, places the parameter
    in a cell of the tiling of the mappling. Places the point of the parameter
    at the given index (0 based) in the given direction."""

    def __init__(
        self, mappling: MappedTiling, param: Parameter, cell: Tuple[int, int]
    ) -> None:
        """cell is the cell in the tiling which the parameter will be placed into"""
        self.mappling = mappling
        self.param = param
        self.cell = cell

    def param_placement(self, direction: int, index_of_pattern: int) -> MappedTiling:
        """Place a parameter in the tiling.
        index_of_pattern is the index of the pattern that is placed in the tiling and is 0 based.
        """
        temp_containing_parameters = self.mappling.containing_parameters.copy()
        if [self.param] in temp_containing_parameters:
            temp_containing_parameters.remove([self.param])
        new_mappling = MTRequirementPlacement(
            MappedTiling(
                self.mappling.tiling,
                self.mappling.avoiding_parameters,
                temp_containing_parameters,
                self.mappling.enumeration_parameters,
            )
        ).directionless_point_placement(self.cell)
        new_avoiding_parameters = (
            new_mappling.avoiding_parameters
            + self.find_new_avoiding_parameters(direction, index_of_pattern)
        )

        new_containing_parameters = self.update_containing_parameters(
            index_of_pattern, new_mappling.containing_parameters
        )
        new_enumeration_parameters = new_mappling.enumeration_parameters
        return MappedTiling(
            new_mappling.tiling,
            new_avoiding_parameters,
            new_containing_parameters,
            new_enumeration_parameters,
        )

    def find_new_avoiding_parameters(self, direction: int, index_of_pattern: int):
        """Return a list of new avoiding parameters for the new mappling."""
        cells_to_insert_in = self.cells_to_insert_point_in(direction, index_of_pattern)
        new_avoiding_parameters = []
        for cell in cells_to_insert_in:
            new_ghost = PointPlacement(self.param.ghost).directionless_point_placement(
                cell
            )
            new_avoiding_parameters.append(
                MTRequirementPlacement(
                    self.mappling
                ).new_parameter_from_point_placed_tiling(self.param, new_ghost, cell)
            )
        return new_avoiding_parameters

    def new_cell_block_in_tiling(self):
        """The new block of cells in the tiling after the point placement."""
        return [
            (i, j)
            for i in range(self.cell[0], self.cell[0] + 3)
            for j in range(self.cell[1], self.cell[1] + 3)
        ]

    def cells_to_insert_point_in(self, direction: int, index_of_pattern: int):
        """Returns a list of cells in the parameter which a point can be
        placed into for the resulting tiling to be an avoiding parameter (cells
        which are not further in the given direction so that the pattern in the
        parameter will be, therefore it must be avoided.)"""
        all_cells = [
            cell
            for cell in self.cells_in_parameter()
            if GriddedCayleyPerm(CayleyPermutation([0]), [cell])
            not in self.param.ghost.obstructions
        ]
        cell_of_point_being_placed = self.cell_in_param(index_of_pattern)
        cells_to_insert_in = [
            cell
            for cell in all_cells
            if PointPlacement(self.param.ghost).farther(
                cell_of_point_being_placed, cell, direction
            )
        ]
        return cells_to_insert_in

    def place_point_in_base_tiling(self) -> MappedTiling:
        """Place a directionless point in the base tiling in self.cell."""
        return PointPlacement(self.mappling.tiling).directionless_point_placement(
            self.cell
        )

    def cells_in_parameter(self):
        """The cells in the parameter that are being placed in the
        tiling at the cell specified."""
        return self.param.map.preimage_of_cell(self.cell)

    def update_containing_parameters(
        self,
        index_of_pattern: int,
        containing_parameters: Iterable[Iterable[Parameter]],
    ):
        """Remove [self.param] from containing parameters and add new
        containing parameter list (one that is the identity)."""
        param_to_update = self.param.copy()
        point_placed_ghost = PointPlacement(
            param_to_update.ghost
        ).directionless_point_placement(self.cell_in_param(index_of_pattern))
        new_map = self.new_containing_param_map(index_of_pattern, point_placed_ghost)
        new_containing_param = Parameter(point_placed_ghost, new_map)
        return [[new_containing_param]] + containing_parameters

    def cell_in_param(self, index_of_pattern: int):
        """The cell in the parameter where the point is placed."""
        return list(sorted(self.param.ghost.point_cells()))[index_of_pattern]

    def new_containing_param_map(self, index_of_pattern: int, ghost: Parameter):
        """Return a new RowColMap for the containing parameter that was placed."""
        middle_cell = self.cell_in_param(index_of_pattern)
        row_map = self.param.map.row_map.copy()
        col_map = self.param.map.col_map.copy()
        new_row_map = self.adjust_dict_in_param(
            middle_cell, 1, row_map, ghost.dimensions[1]
        )
        new_col_map = self.adjust_dict_in_param(
            middle_cell, 0, col_map, ghost.dimensions[0]
        )
        return RowColMap(new_col_map, new_row_map)

    def adjust_dict_in_param(
        self,
        middle_cell: Tuple[int, int],
        row_or_col: int,
        new_map: Dict[int, int],
        dimension: int,
    ):
        """Update a row or col map given the cell in the new parameter where the point is placed
        and the old row or col map.
        If row_or_col = 0 then it returns the new col map, if 1 then it returns the new row map.
        """
        vals_in_param = set(cell[row_or_col] for cell in self.cells_in_parameter())
        middle_val = middle_cell[row_or_col] + 1
        for val in range(dimension):
            if val not in vals_in_param:
                if val > middle_val:
                    if val not in new_map:
                        new_map[val] = self.cell[row_or_col] + 2
                    else:
                        new_map[val] += 2
            elif val < middle_val:
                new_map[val] = self.cell[row_or_col]
            elif val > middle_val:
                new_map[val] = self.cell[row_or_col] + 2
            else:
                new_map[val] = self.cell[row_or_col] + 1
        return new_map
