"""Point placement algorithm for MappedTiling."""

from typing import Tuple, Iterator, Iterable
from gridded_cayley_permutations.point_placements import PointPlacement
from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from gridded_cayley_permutations.row_col_map import RowColMap
from mapplings import MappedTiling, Parameter, ParameterList

Cell = tuple[int, int]


class MTRequirementPlacement:
    """Handles point placement for requirements in a MappedTiling."""

    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-arguments
    def __init__(self, mappling: MappedTiling) -> None:
        self.mappling = mappling
        self.directionless_dict = dict[Cell, MappedTiling]()

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
        directionless = self.directionless_point_placement(cell)
        algo = PointPlacement(self.mappling.tiling)
        forced_obs = algo.forced_obstructions(
            cell, requirement_list, indices, direction
        )
        point_obs, point_reqs = algo.point_obstructions_and_requirements(cell)
        new_obs = directionless.obstructions + forced_obs + point_obs
        new_reqs = directionless.requirements + point_reqs
        new_base = Tiling(new_obs, new_reqs, directionless.dimensions)
        return MappedTiling(new_base, *directionless.ace_parameters())

    def unfuse_cols_in_param(
        self, parameter: Parameter, cell: tuple[int, int]
    ) -> Iterator[Parameter]:
        """For each column in param, if it's preimage is in the same column as the cell in the
        base tiling that was inserted into then unfuse it by 2 columns.
        """
        for col in range(parameter.dimensions[0]):
            if parameter.map.col_map[col] == cell[0]:
                new_ghost = self.unfuse_col(parameter, col)
                new_col_map = self.map_for_cols_param_expanded(
                    new_ghost, parameter.map.col_map, (col + 1, 0), 0
                )
                new_row_map = self.map_for_adjust_rowcols(
                    parameter.map.row_map, cell, True
                )
                yield Parameter(new_ghost, RowColMap(new_col_map, new_row_map))

    def unfuse_col(self, parameter: Parameter, col: int) -> Tiling:
        """Unfuse the param by 2 columns at the given column index."""
        n, m = parameter.dimensions
        new_n = n + 1
        row_map = {i: i for i in range(m)}
        col_map = {i: i for i in range(col)}
        col_map.update({i: i - 1 for i in range(col + 1, new_n)})
        obs, reqs = RowColMap(col_map, row_map).preimage_of_tiling(parameter.ghost)
        return Tiling(obs, reqs, (new_n, m))

    def unfuse_rows_in_param(
        self, parameter: Parameter, cell: tuple[int, int]
    ) -> Iterator[Parameter]:
        """For each row in param, if it's preimage is in the same row as the cell in the
        base tiling that was inserted into then unfuse it by 3 rows and make the middle
        one a point row.
        Anything below the point row stays the same,
        the point row is shifted up by one and anything above it is shifted up by 2."""
        for row in range(parameter.dimensions[1]):
            if parameter.map.row_map[row] == cell[1]:
                new_ghost = self.unfuse_row(parameter, row)
                new_row_map = self.map_for_rows_param_expanded(
                    new_ghost, parameter.map.row_map, (0, row + 1), 1
                )
                new_col_map = self.map_for_adjust_rowcols(
                    parameter.map.col_map, cell, False
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
        return Tiling(obs, reqs, (n, new_m))

    def map_for_param_unchanged(
        self, parameter: Parameter, cell: tuple[int, int]
    ) -> RowColMap:
        """Updates the map of a parameter which didn't have a
        point placement in, so the parameter itself is unchanged."""
        new_row_map = self.map_for_adjust_rowcols(parameter.map.row_map, cell, True)
        new_col_map = self.map_for_adjust_rowcols(parameter.map.col_map, cell, False)
        return RowColMap(new_col_map, new_row_map)

    def map_for_adjust_rowcols(
        self, old_map: dict[int, int], cell: tuple[int, int], adjust_rows: bool
    ) -> dict[int, int]:
        """Updates the map of a parameter which didn't have a
        point placement in, so the parameter itself is unchanged.
        Adjusts the row/column map of a parameter after a point placement.
        cols if adjust_rows == 0, rows if adjust_rows == 1."""
        return {
            idx: value + 2 * int(value > cell[adjust_rows])
            for idx, value in old_map.items()
        }

    def map_for_param_placed_point(
        self, new_ghost: Tiling, param_cell: tuple[int, int], old_rowcolmap: RowColMap
    ) -> RowColMap:
        """Creates a new map for a parameter which had a point placement in.

        Expands the map in the parameter at the indices corresponding to the
        cell where the point was placed in the parameter, and the cell where
        the point was placed in the tiling."""
        new_row_map = self.map_for_rows_param_expanded(
            new_ghost, old_rowcolmap.row_map, (param_cell[0] + 1, param_cell[1] + 1), 1
        )
        new_col_map = self.map_for_cols_param_expanded(
            new_ghost, old_rowcolmap.col_map, (param_cell[0] + 1, param_cell[1] + 1), 0
        )
        return RowColMap(new_col_map, new_row_map)

    def map_for_cols_param_expanded(
        self,
        new_ghost: Tiling,
        old_map: dict[int, int],
        param_cell: Tuple[int, int],
        row: int,
    ) -> dict[int, int]:
        """Creates a new row/col map for a parameter which was expanded
        because of a point placement."""
        new_map = {}
        for idx in range(new_ghost.dimensions[row]):
            if idx < param_cell[row]:
                new_map[idx] = old_map[idx]
            else:
                new_map[idx] = old_map[idx - 1] + 2
        return new_map

    def map_for_rows_param_expanded(
        self,
        new_ghost: Tiling,
        old_map: dict[int, int],
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
    ) -> Tuple[Tuple[GriddedCayleyPerm, ...], Tuple[int, ...]]:
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
        return tuple(new_requirement_list), tuple(new_indices)

    # Directionless point placement #

    def directionless_point_placement(self, cell: Tuple[int, int]) -> MappedTiling:
        """Place a directionless point in the tiling and all parameters and update maps."""
        if cell not in self.directionless_dict:
            new_tiling = PointPlacement(
                self.mappling.tiling
            ).directionless_point_placement(cell)
            new_avoiding_parameters = self.update_param_list(
                self.mappling.avoiding_parameters, cell
            )
            new_containing_parameters = self.update_list_of_param_lists(
                self.mappling.containing_parameters, cell
            )
            new_enumeration_parameters = self.update_list_of_param_lists(
                self.mappling.enumerating_parameters, cell
            )
            self.directionless_dict[cell] = MappedTiling(
                new_tiling,
                new_avoiding_parameters,
                new_containing_parameters,
                new_enumeration_parameters,
            )
        return self.directionless_dict[cell]

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
            if cell in parameter.image_cells():
                algo = PointPlacement(parameter.ghost)
                new_cells = parameter.map.preimage_of_cell(cell)
                for new_cell in new_cells:
                    new_ghost = algo.directionless_point_placement(new_cell)
                    if new_ghost.is_empty():
                        continue
                    new_param = self.new_parameter_from_point_placed_tiling(
                        parameter, new_ghost, new_cell
                    )
                    new_param_list.append(new_param)
            else:
                image_cols, image_rows = parameter.map.image_rows_and_cols()
                if cell[0] in image_cols:
                    for new_param in self.unfuse_cols_in_param(parameter, cell):
                        new_param_list.append(new_param)
                elif cell[1] in image_rows:
                    for new_param in self.unfuse_rows_in_param(parameter, cell):
                        new_param_list.append(new_param)
                else:
                    new_map = self.map_for_param_unchanged(parameter, cell)
                    new_param_list.append(Parameter(parameter.ghost, new_map))

        return ParameterList(new_param_list)

    def new_parameter_from_point_placed_tiling(
        self, parameter: Parameter, new_ghost: Tiling, cell: Tuple[int, int]
    ) -> Parameter:
        """For a given parameter and a tiling after a point has been placed
        in the cell of the parameter, returns a new parameter with the new tiling
        and correct map.
        Also removes the column in the param relating to the column of the
        placed point in the base tiling."""
        n, m = parameter.ghost.dimensions
        new_n, new_m = new_ghost.dimensions
        new_map = parameter.map.expand_at_index(new_n - n, new_m - m, cell[0], cell[1])
        return Parameter(new_ghost, new_map).delete_rows_and_columns([cell[0] + 1], [])
