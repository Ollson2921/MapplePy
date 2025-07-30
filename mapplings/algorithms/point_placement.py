"""Point placement algorithm for MappedTiling."""

from typing import Dict, Tuple, List, Iterator
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations.point_placements import (
    PointPlacement,
    DIR_LEFT,
    DIR_RIGHT,
)
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from cayley_permutations import CayleyPermutation
from mapplings import MappedTiling, Parameter, ParameterList
from gridded_cayley_permutations import GriddedCayleyPerm
from gridded_cayley_permutations.point_placements import (
    MultiplexMap,
    PartialMultiplexMap,
    PointPlacement,
)
from gridded_cayley_permutations.row_col_map import RowColMap
from itertools import combinations


class MTRequirementPlacement:
    def __init__(self, mappling: MappedTiling) -> None:
        self.mappling = mappling

    def point_placement(
        self,
        requirement_list: Tuple[GriddedCayleyPerm, ...],
        indices: Tuple[int, ...],
        direction: int,
    ) -> Tuple[MappedTiling, ...]:
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
        base_tiling = PointPlacement(self.mappling.tiling).point_placement_in_cell(
            requirement_list, indices, direction, cell
        )
        new_avoiding_parameters = self.req_placement_in_list(
            self.mappling.avoiding_parameters,
            requirement_list,
            indices,
            direction,
            cell,
        )
        new_containing_parameters = self.req_placement_param_list(
            self.mappling.containing_parameters,
            requirement_list,
            indices,
            direction,
            cell,
        )
        new_enumerating_parameters = self.req_placement_param_list(
            self.mappling.enumerating_parameters,
            requirement_list,
            indices,
            direction,
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
        param_lists: tuple[tuple[Parameter, ...], ...],
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
        cell: tuple[int, int],
    ) -> tuple[Parameter, ...]:
        """Point placement in a list of lists of parameters."""
        return tuple(
            self.req_placement_in_list(
                param_list, requirement_list, indices, direction, cell
            )
            for param_list in param_lists
        )

    def req_placement_in_list(
        self,
        param_list: tuple[Parameter, ...],
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
        cell: tuple[int, int],
    ) -> tuple[Parameter, ...]:
        """Point placement in a single list of parameters.
        For a given list of lists of parameters, maps each individual
        parameter to a a new list of parameters with the requirement list
        placed in the cell given (where cell, requirement_list, etc have
        been mapped to the parameter)."""
        new_param_list = set()
        for parameter in param_list:
            if cell not in parameter.image_cells():
                if any(
                    image_cell[0] == cell[0] for image_cell in parameter.image_cells()
                ):
                    for new_param in self.unfuse_cols_in_param(parameter, cell):
                        new_param_list.add(new_param)
                if any(
                    image_cell[1] == cell[1] for image_cell in parameter.image_cells()
                ):
                    for new_param in self.unfuse_rows_in_param(parameter, cell):
                        new_param_list.add(new_param)
                else:
                    new_map = self.map_for_param_unchanged(parameter, cell)
                    new_param_list.add(Parameter(parameter.ghost, new_map))
            else:
                (
                    param_requirement_list,
                    param_indices,
                ) = self.map_requirement_list_to_parameter(
                    requirement_list, indices, parameter
                )
                for param_cell in parameter.map.preimage_of_cell(cell):
                    new_ghost = PointPlacement(parameter.ghost).point_placement_in_cell(
                        param_requirement_list, param_indices, direction, param_cell
                    )
                    new_map = self.map_for_param_placed_point(
                        new_ghost, param_cell, parameter.map
                    )
                    new_param_list.add(Parameter(new_ghost, new_map))
        return tuple(sorted(new_param_list))

    def unfuse_cols_in_param(
        self, parameter: Parameter, cell: tuple[int, int]
    ) -> Iterator[Parameter]:
        """For each column in param, if it's preimage is in the same column as the cell in the
        base tiling that was inserted into then unfuse it by 3 columns and make the middle one a point column.
        """
        for col in range(parameter.dimensions[0]):
            if parameter.map.col_map[col] == cell[0]:
                new_ghost = self.unfuse_col(parameter, col)
                new_col_map = self.map_for_param_expanded(
                    new_ghost, parameter.map.col_map, (col + 1, 0), 0
                )
                new_row_map = self.map_for_adjust_rowcols(
                    parameter.map.row_map, cell, 1
                )
                yield Parameter(new_ghost, RowColMap(new_col_map, new_row_map))

    def unfuse_col(self, parameter: Parameter, col: int) -> Tiling:
        """Unfuse the param by 3 columns at the given column index and make
        the middle one a point column."""
        n, m = parameter.dimensions
        new_n = n + 2
        row_map = {i: i for i in range(m)}
        col_map = {i: i for i in range(col + 1)}
        col_map.update({i: i - 2 for i in range(col + 2, new_n)})
        col_map[col + 1] = col
        obs, reqs = RowColMap(col_map, row_map).preimage_of_tiling(parameter.ghost)
        col_obs = [
            GriddedCayleyPerm(CayleyPermutation([0]), [(col + 1, i)]) for i in range(m)
        ]
        return Tiling(obs, reqs, (new_n, m)).add_obstructions(col_obs)

    def unfuse_rows_in_param(
        self, parameter: Parameter, cell: tuple[int, int]
    ) -> Iterator[Parameter]:
        """For each row in param, if it's preimage is in the same row as the cell in the
        base tiling that was inserted into then unfuse it by 3 rows and make the middle one a point row.
        Anything below the point row stays the same,
        the point row is shifted up by one and anything above it is shifted up by 2."""
        for row in range(parameter.dimensions[1]):
            if parameter.map.row_map[row] == cell[1]:
                new_ghost = self.unfuse_row(parameter, row)
                new_row_map = self.map_for_param_expanded(
                    new_ghost, parameter.map.row_map, (0, row + 1), 1
                )
                new_col_map = self.map_for_adjust_rowcols(
                    parameter.map.col_map, cell, 0
                )
                yield Parameter(new_ghost, RowColMap(new_col_map, new_row_map))

    def unfuse_row(self, parameter: Parameter, row: int) -> Tiling:
        """Unfuse the param by 3 rows at the given row index and make
        the middle one a point row."""
        n, m = parameter.dimensions
        new_m = m + 2
        col_map = {i: i for i in range(n)}
        row_map = {i: i for i in range(row + 1)}
        row_map.update({i: i - 2 for i in range(row + 2, new_m)})
        row_map[row + 1] = row
        obs, reqs = RowColMap(col_map, row_map).preimage_of_tiling(parameter.ghost)
        return Tiling(obs, reqs, (n, new_m)).add_obstructions(self.row_obs(n, row + 1))

    def row_obs(self, x: int, row: int) -> List[GriddedCayleyPerm]:
        """Returns the row observations for a given row in a parameter."""
        row_obs: list[GriddedCayleyPerm] = []
        for col in range(x):
            row_obs.append(
                GriddedCayleyPerm(CayleyPermutation([0, 1]), [(col, row), (col, row)])
            )
            row_obs.append(
                GriddedCayleyPerm(CayleyPermutation([1, 0]), [(col, row), (col, row)])
            )
        for col1, col2 in combinations(range(x), 2):
            row_obs.append(
                GriddedCayleyPerm(CayleyPermutation([0, 1]), [(col1, row), (col2, row)])
            )
            row_obs.append(
                GriddedCayleyPerm(CayleyPermutation([1, 0]), [(col1, row), (col2, row)])
            )
        return row_obs

    def map_for_param_unchanged(
        self, parameter: Parameter, cell: tuple[int, int]
    ) -> RowColMap:
        """Updates the map of a parameter which didn't have a
        point placement in, so the parameter itself is unchanged."""
        new_row_map = self.map_for_adjust_rowcols(parameter.map.row_map, cell, 1)
        new_col_map = self.map_for_adjust_rowcols(parameter.map.col_map, cell, 0)
        return RowColMap(new_col_map, new_row_map)

    def map_for_adjust_rowcols(
        self, old_map: dict[int:int], cell: tuple[int, int], row: int
    ) -> dict[int, int]:
        """Updates the map of a parameter which didn't have a
        point placement in, so the parameter itself is unchanged."""
        """Adjusts the row/column map of a parameter after a point placement.
        cols if row == 0, rows if row == 1."""
        if old_map[0] < cell[row]:
            return old_map
        return {idx: old_map[row] + 2 for idx in old_map}

    def map_for_param_placed_point(
        self, new_ghost: Tiling, param_cell: tuple[int, int], old_rowcolmap: RowColMap
    ) -> RowColMap:
        """Creates a new map for a parameter which had a point placement in.

        Expands the map in the parameter at the indices corresponding to the
        cell where the point was placed in the parameter, and the cell where
        the point was placed in the tiling."""
        new_row_map = self.map_for_param_expanded(
            new_ghost, old_rowcolmap.row_map, (param_cell[0] + 1, param_cell[1] + 1), 1
        )
        new_col_map = self.map_for_param_expanded(
            new_ghost, old_rowcolmap.col_map, (param_cell[0] + 1, param_cell[1] + 1), 0
        )
        return RowColMap(new_col_map, new_row_map)

    def map_for_param_expanded(
        self,
        new_ghost: Tiling,
        old_map: dict[int:int],
        param_cell: Tuple[int, int],
        row: int,
    ) -> dict[int, int]:
        """Creates a new row/col map for a parameter which was expanded
        because of a point placement."""
        new_map = {}
        for idx in range(new_ghost.dimensions[row]):
            if idx < param_cell[row]:
                new_map[idx] = old_map[idx]
            elif idx == param_cell[row]:
                new_map[idx] = old_map[idx - 1] + 1
            else:
                new_map[idx] = old_map[idx - 2] + 2
        return new_map

    def map_requirement_list_to_parameter(
        self,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        parameter: Parameter,
    ) -> tuple[tuple[GriddedCayleyPerm, ...], tuple[int, ...]]:
        """Maps each requirement in a requirement list to a new requirement based on
        parameter.map and creates new requirement list for the parameter. Also turns
        indices into a list length len(new_requirement_list), with one occurrence of each
        index for each requirement in new_requirement_list."""
        new_requirement_list = []
        new_indices = []
        for idx, gcp in zip(indices, requirement_list):
            for stretched_gcp in parameter.map.preimage_of_gridded_cperm(gcp):
                new_requirement_list.append(stretched_gcp)
                new_indices.append(idx)
        return new_requirement_list, new_indices

    ### Directionless point placement ###

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
        self, param_lists: list[ParameterList], cell: Tuple[int, int]
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
        return new_param_list

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
        self, cell: Tuple[int], direction: int
    ) -> Tuple[
        Tuple[GriddedCayleyPerm, ...] | Tuple[Tuple[GriddedCayleyPerm, ...], ...]
    ]:
        cell = self.placed_cell(cell)
        _, y = self.new_dimensions()
        col_obs = [
            GriddedCayleyPerm(CayleyPermutation([0]), [(cell[0], i)])
            for i in range(y)
            if i != cell[1]
        ]
        return [
            [
                GriddedCayleyPerm(CayleyPermutation((0, 1)), [cell, cell]),
                GriddedCayleyPerm(CayleyPermutation((0, 0)), [cell, cell]),
                GriddedCayleyPerm(CayleyPermutation((1, 0)), [cell, cell]),
            ]
            + col_obs,
            [[GriddedCayleyPerm(CayleyPermutation([0]), [cell])]],
        ]

    def placed_cell(self, cell: Tuple[int]) -> Tuple[int]:
        return (cell[0] + 1, cell[1])

    def multiplex_map(self, cell: Tuple[int]) -> MultiplexMap:
        return PartialMultiplexMap(cell, self.mappling.tiling.dimensions)

    def new_dimensions(self):
        return (
            self.mappling.tiling.dimensions[0] + 2,
            self.mappling.tiling.dimensions[1],
        )
