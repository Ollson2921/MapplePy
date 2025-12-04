"""Algorithm for parameter placement"""

from cayley_permutations import CayleyPermutation

from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from gridded_cayley_permutations.point_placements import PointPlacement
from gridded_cayley_permutations.row_col_map import RowColMap

from mapplings import MappedTiling, Parameter, ParameterList
from .point_placement import MTRequirementPlacement


Cell = tuple[int, int]


class ParameterPlacement:
    """For a given mappling and containing parameter, places the parameter
    in a cell of the tiling of the mappling. Places the point of the parameter
    at the given index (0 based) in the given direction."""

    def __init__(self, mappling: MappedTiling, param_list: ParameterList) -> None:
        """cell is the cell in the tiling which the parameter will be placed into"""
        assert len(param_list) == 1, "Too many Parameters in ParameterList."
        assert (
            param_list in mappling.containing_parameters
        ), "ParameterList does not exist."
        self.mappling = mappling
        new_containers = list(mappling.containing_parameters)
        new_containers.remove(param_list)
        self.adjusted_mappling = MappedTiling(
            mappling.tiling,
            mappling.avoiding_parameters,
            new_containers,
            mappling.enumerating_parameters,
        )
        self.param = tuple(param_list)[0]

    def param_placement(self, direction: int, index_of_pattern: int) -> MappedTiling:
        """Place a parameter in the tiling.
        index_of_pattern is the index of the pattern that is placed in the tiling and is 0 based.
        """
        param_cell = tuple(self.param.point_cells())[index_of_pattern]
        cell = (self.param.col_map[param_cell[0]], self.param.col_map[param_cell[1]])
        new_mappling = MTRequirementPlacement(
            self.adjusted_mappling
        ).directionless_point_placement(cell)
        new_avoiding_parameters = list(
            new_mappling.avoiding_parameters
        ) + self.find_new_avoiding_parameters(direction, cell, param_cell)

        new_containing_parameters = self.update_containing_parameters(
            param_cell, cell, new_mappling.containing_parameters
        )
        new_base = new_mappling.tiling
        algo = PointPlacement(self.mappling.tiling)
        point_obs, point_reqs = algo.point_obstructions_and_requirements(cell)
        new_obs = new_base.obstructions + point_obs
        new_reqs = new_base.requirements + point_reqs
        new_base = Tiling(new_obs, new_reqs, new_base.dimensions)
        return MappedTiling(
            new_base,
            new_avoiding_parameters,
            new_containing_parameters,
            new_mappling.enumerating_parameters,
        )

    def find_new_avoiding_parameters(
        self, direction: int, base_cell: Cell, param_cell: Cell
    ):
        """Return a list of new avoiding parameters for the new mappling."""
        cells_to_insert_in = self.cells_to_insert_point_in(
            direction, base_cell, param_cell
        )
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

    def cells_in_parameter(self, base_cell: Cell) -> tuple[Cell, ...]:
        """Gets the preimage of the base cell according to the param map."""
        return self.param.map.preimage_of_cell(base_cell)

    def cells_to_insert_point_in(
        self, direction: int, base_cell: Cell, param_cell: Cell
    ):
        """Returns a list of cells in the parameter which a point can be
        placed into for the resulting tiling to be an avoiding parameter (cells
        which are not further in the given direction so that the pattern in the
        parameter will be, therefore it must be avoided.)"""
        all_cells = [
            cell
            for cell in self.cells_in_parameter(base_cell)
            if GriddedCayleyPerm(CayleyPermutation([0]), [cell])
            not in self.param.ghost.obstructions
        ]
        cell_of_point_being_placed = param_cell
        cells_to_insert_in = [
            cell
            for cell in all_cells
            if PointPlacement(self.param.ghost).farther(
                cell_of_point_being_placed, cell, direction
            )
        ]
        return cells_to_insert_in

    def update_containing_parameters(
        self,
        param_cell: Cell,
        base_cell: Cell,
        containing_parameters: tuple[ParameterList, ...],
    ) -> tuple[ParameterList, ...]:
        """Remove [self.param] from containing parameters and add new
        containing parameter list (one that is the identity)."""
        param_to_update = Parameter(self.param.ghost, self.param.map)
        point_placed_ghost = PointPlacement(
            param_to_update.ghost
        ).directionless_point_placement(param_cell)
        new_map = self.new_containing_param_map(
            param_cell, base_cell, point_placed_ghost
        )
        new_containing_param = Parameter(point_placed_ghost, new_map)
        return (ParameterList((new_containing_param,)),) + containing_parameters

    def new_containing_param_map(
        self, param_cell: Cell, base_cell: Cell, ghost: Tiling
    ):
        """Return a new RowColMap for the containing parameter that was placed."""
        new_row_map = self.adjust_dict_in_param(
            param_cell, base_cell, True, ghost.dimensions[1]
        )
        new_col_map = self.adjust_dict_in_param(
            param_cell, base_cell, False, ghost.dimensions[0]
        )
        return RowColMap(new_col_map, new_row_map)

    def adjust_dict_in_param(
        self,
        middle_cell: Cell,
        base_cell: Cell,
        adjust_rows: bool,
        dimension: int,
    ):
        """Update a row or col map given the cell in the new parameter where the point is placed
        and the old row or col map.
        If adjust_rows = 0 then it returns the new col map, if 1 then it returns the new row map.
        """
        if adjust_rows:
            new_map = self.param.row_map
        else:
            new_map = self.param.col_map
        vals_in_param = set(
            cell[adjust_rows] for cell in self.cells_in_parameter(base_cell)
        )
        middle_val = middle_cell[adjust_rows] + 1
        for val in range(dimension):
            if val not in vals_in_param:
                if val > middle_val:
                    if val not in new_map:
                        new_map[val] = base_cell[adjust_rows] + 2
                    else:
                        new_map[val] += 2
            elif val < middle_val:
                new_map[val] = base_cell[adjust_rows]
            elif val > middle_val:
                new_map[val] = base_cell[adjust_rows] + 2
            else:
                new_map[val] = base_cell[adjust_rows] + 1
        return new_map
