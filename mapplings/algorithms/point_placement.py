"""Point placement algorithm for MappedTiling."""

from typing import Tuple, Iterable
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations.point_placements import (
    PointPlacement,
    DIR_LEFT,
    DIR_RIGHT,
    MultiplexMap,
    PartialMultiplexMap,
)
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings import MappedTiling, Parameter, ParameterList


class MTRequirementPlacement:
    """Handles point placement for requirements in a MappedTiling."""

    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-arguments
    def __init__(self, mappling: MappedTiling) -> None:
        self.mappling = mappling

    def point_placement(
        self,
        requirement_list: Tuple[GriddedCayleyPerm, ...],
        indices: Tuple[int, ...],
        direction: int,
    ) -> Tuple[MappedTiling, ...]:
        """Point placement in the mapped tiling."""
        cells = []
        for idx, gcp in zip(indices, requirement_list):
            cells.append(gcp.positions[idx])
        cells = sorted(set(cells))
        return tuple(
            self.point_placement_in_cell(requirement_list, indices, direction, cell)
            for cell in cells
        )

    def point_placement_in_cell(
        self,
        requirement_list: Tuple[GriddedCayleyPerm, ...],
        indices: Tuple[int, ...],
        direction: int,
        cell: Tuple[int, int],
    ) -> MappedTiling:
        """Point placement in a specific cell of the mapped tiling."""
        base_tiling = PointPlacement(self.mappling.tiling).point_placement_in_cell(
            requirement_list, indices, direction, cell
        )
        new_avoiding_parameters = self.req_placement_in_list(
            self.mappling.avoiding_parameters,
            cell,
        )
        new_containing_parameters = self.req_placement_param_list(
            self.mappling.containing_parameters,
            cell,
        )
        new_enumerating_parameters = self.req_placement_param_list(
            self.mappling.enumerating_parameters,
            cell,
        )
        return MappedTiling(
            base_tiling,
            new_avoiding_parameters,
            new_containing_parameters,
            new_enumerating_parameters,
        )

    def req_placement_param_list(
        self,
        param_lists: tuple[ParameterList, ...],
        cell: tuple[int, int],
    ) -> Iterable[ParameterList]:
        """Point placement in a list of lists of parameters."""
        return tuple(
            self.req_placement_in_list(param_list, cell) for param_list in param_lists
        )

    def req_placement_in_list(
        self,
        param_list: ParameterList,
        cell: tuple[int, int],
    ) -> ParameterList:
        """Point placement in a single list of parameters.
        For a given list of lists of parameters, maps each individual
        parameter to a a new list of parameters with the requirement list
        placed in the cell given (where cell, requirement_list, etc have
        been mapped to the parameter)."""
        new_param_list = set()
        for parameter in param_list:
            all_params = [parameter]
            image_row_cols = parameter.map.image_rows_and_cols()
            if cell[0] in image_row_cols[0]:
                all_params = [
                    self.unfuse_col(parameter, col)
                    for col in parameter.map.preimages_of_col(cell[0])
                ]
            else:
                new_col_map = self.map_for_adjust_rowcols(
                    parameter.map.row_map, cell, 0
                )
                all_params = [
                    Parameter(
                        parameter.ghost, RowColMap(new_col_map, parameter.map.row_map)
                    )
                ]
            if cell[1] in image_row_cols[1]:
                preimage_rows = parameter.map.preimages_of_row(cell[1])
                for param in all_params:
                    new_param_list.update(
                        self.unfuse_row(param, row) for row in preimage_rows
                    )
            else:
                new_param_list = {
                    Parameter(
                        param.ghost,
                        RowColMap(
                            param.map.col_map,
                            self.map_for_adjust_rowcols(parameter.map.row_map, cell, 1),
                        ),
                    )
                    for param in all_params
                }
        return ParameterList(tuple(sorted(new_param_list)))

    def unfuse_col(self, parameter: Parameter, col: int) -> Parameter:
        """Unfuse the param by 3 columns at the given column index and make
        the middle one a point column."""
        n, m = parameter.dimensions
        new_n = n + 1
        row_map = {i: i for i in range(m)}
        col_map = {i: i for i in range(col + 1)}
        col_map.update({i: i - 1 for i in range(col + 1, new_n)})
        col_map[col + 1] = col
        obs, reqs = RowColMap(col_map, row_map).preimage_of_tiling(parameter.ghost)
        til = Tiling(obs, reqs, (new_n, m))
        new_col_map = self.colmap_for_param_expanded(til, parameter.col_map, col)
        return Parameter(til, RowColMap(new_col_map, parameter.row_map))

    def unfuse_row(self, parameter: Parameter, row: int) -> Parameter:
        """Unfuse the param by 3 rows at the given row index and make
        the middle one a point row."""
        n, m = parameter.dimensions
        new_m = m + 2
        col_map = {i: i for i in range(n)}
        row_map = {i: i for i in range(row + 1)}
        row_map.update({i: i - 2 for i in range(row + 2, new_m)})
        row_map[row + 1] = row
        obs, reqs = RowColMap(col_map, row_map).preimage_of_tiling(parameter.ghost)
        til = Tiling(obs, reqs, (n, new_m))
        new_row_map = self.rowmap_for_param_expanded(til, parameter.row_map, row)
        return Parameter(til, RowColMap(parameter.col_map, new_row_map))

    def map_for_adjust_rowcols(
        self, old_map: dict[int, int], cell: tuple[int, int], row: int
    ) -> dict[int, int]:
        """Updates the map of a parameter which didn't have a
        point placement in, so the parameter itself is unchanged.
        Adjusts the row/column map of a parameter after a point placement.
        cols if row == 0, rows if row == 1."""
        if old_map[0] < cell[row]:
            return old_map
        return {idx: old_map[row] + 2 for idx in old_map}

    def rowmap_for_param_expanded(
        self,
        new_ghost: Tiling,
        old_map: dict[int, int],
        row: int,
    ) -> dict[int, int]:
        """Creates a new row map for a parameter which was expanded
        because of a point placement."""
        row += 1
        new_map = {}
        for idx in range(new_ghost.dimensions[1]):
            if idx < row:
                new_map[idx] = old_map[idx]
            elif idx == row:
                new_map[idx] = old_map[idx - 1] + 1
            else:
                new_map[idx] = old_map[idx - 2] + 2
        return new_map

    def colmap_for_param_expanded(
        self,
        new_ghost: Tiling,
        old_map: dict[int, int],
        col: int,
    ) -> dict[int, int]:
        """Creates a new col map for a parameter which was expanded
        because of a point placement."""
        new_map = {}
        for idx in range(new_ghost.dimensions[0]):
            if idx <= col:
                new_map[idx] = old_map[idx]
            else:
                new_map[idx] = old_map[idx - 1] + 2
        return new_map

    # Directionless point placement #

    def directionless_point_placement(self, cell: Tuple[int, int]) -> MappedTiling:
        """Place a directionless point in the tiling and all parameters and update maps."""
        new_tiling = PointPlacement(self.mappling.tiling).directionless_point_placement(
            cell
        )
        new_avoiding_parameters = self.update_param_list(
            self.mappling.avoiding_parameters, cell
        )
        new_containing_parameters = self.update_list_of_param_lists(
            self.mappling.containing_parameters, cell
        )
        new_enumeration_parameters = self.update_list_of_param_lists(
            self.mappling.enumerating_parameters, cell
        )
        return MappedTiling(
            new_tiling,
            new_avoiding_parameters,
            new_containing_parameters,
            new_enumeration_parameters,
        )

    def update_list_of_param_lists(
        self, param_lists: Iterable[ParameterList], cell: Tuple[int, int]
    ) -> list[ParameterList]:
        """Doing directionless point placements in a list of parameter lists and updating maps."""
        new_param_lists = []
        for param_list in param_lists:
            new_param_lists.append(self.update_param_list(param_list, cell))
        return new_param_lists

    def update_param_list(
        self, param_list: ParameterList, cell: Tuple[int, int]
    ) -> ParameterList:
        """Doing directionless point placements in parameter list and updating maps."""
        new_param_list = []
        for parameter in param_list:
            new_cells = parameter.map.preimage_of_cell(cell)
            for new_cell in new_cells:
                new_ghost = PointPlacement(
                    parameter.ghost
                ).directionless_point_placement(new_cell)
                if new_ghost.is_empty():
                    continue
                new_param = self.new_parameter_from_point_placed_tiling(
                    parameter, new_ghost, new_cell
                )
                new_param_list.append(new_param)
        return ParameterList(new_param_list)

    def new_parameter_from_point_placed_tiling(
        self, parameter: Parameter, new_ghost: Tiling, cell: Tuple[int, int]
    ) -> Parameter:
        """For a given parameter and a tiling after a point has been placed
        in the cell of the parameter, returns a new parameter with the new tiling
        and correct map."""
        n, m = parameter.ghost.dimensions
        new_n, new_m = new_ghost.dimensions
        new_map = parameter.map.expand_at_index(new_n - n, new_m - m, cell[0], cell[1])
        return Parameter(new_ghost, new_map)


class MTPartialPointPlacements(MTRequirementPlacement):
    """TODO: update for mapplings"""

    DIRECTIONS = [DIR_LEFT, DIR_RIGHT]

    def point_obstructions_and_requirements(
        self, cell: Tuple[int, int]
    ) -> Iterable[Iterable[GriddedCayleyPerm] | Iterable[Iterable[GriddedCayleyPerm]]]:
        """Returns the point obstructions and requirements for a point placement in a cell."""
        cell = self.placed_cell(cell)
        _, y = self.new_dimensions()
        col_obs = [
            GriddedCayleyPerm(CayleyPermutation([0]), [(cell[0], i)])
            for i in range(y)
            if i != cell[1]
        ]
        return (
            [
                GriddedCayleyPerm(CayleyPermutation((0, 1)), [cell, cell]),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), [cell, cell]),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), [cell, cell]),
            ]
            + col_obs,
            [[GriddedCayleyPerm(CayleyPermutation([0]), [cell])]],
        )

    def placed_cell(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        """Returns the cell where the point is placed in the mapped tiling."""
        return (cell[0] + 1, cell[1])

    def multiplex_map(self, cell: Tuple[int, int]) -> MultiplexMap:
        """Returns a multiplex map for the point placement in the cell."""
        return PartialMultiplexMap(cell, self.mappling.tiling.dimensions)

    def new_dimensions(self):
        """Returns the new dimensions of the mapped tiling after point placement."""
        return (
            self.mappling.tiling.dimensions[0] + 2,
            self.mappling.tiling.dimensions[1],
        )
