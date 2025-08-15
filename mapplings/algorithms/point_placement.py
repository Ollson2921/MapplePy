"""Point placement algorithm for MappedTiling."""

from itertools import chain, product
from typing import Tuple, Iterable
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
        self.directionless_point_placements: dict[Cell, MappedTiling] = dict()

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
            self.point_placement_in_cell(
                cell,
                requirement_list,
                indices,
                direction,
            )
            for cell in cells
        )

    def point_placement_in_cell(
        self,
        cell: Cell,
        requirement_list: tuple[GriddedCayleyPerm, ...],
        indices: tuple[int, ...],
        direction: int,
    ) -> MappedTiling:
        """Adds the neccecary obstructions to turn a directionless point placement
        into a direction-ed point placement"""
        directionless_placement = self.directionless_point_placement_in_cell(cell)
        forced = PointPlacement(self.mappling.tiling).forced_obstructions(
            cell, requirement_list, indices, direction
        )
        new_base = directionless_placement.add_obstructions(forced)
        return MappedTiling(new_base, *directionless_placement.ace_parameters())

    def directionless_point_placement_in_cell(
        self,
        cell: Cell,
    ) -> MappedTiling:
        """Directionless point placement in a specific cell of the mapped tiling."""
        if cell not in self.directionless_point_placements:
            avoiders, containers, enumerators = self.mappling.ace_parameters()
            new_base_tiling = PointPlacement(
                self.mappling.tiling
            ).directionless_point_placement(cell)
            new_avoiders = ParameterList(
                chain.from_iterable(
                    self.all_param_expansions(avoider, cell) for avoider in avoiders
                )
            )
            new_containers = tuple(
                ParameterList(
                    chain.from_iterable(
                        self.all_param_expansions(container, cell)
                        for container in c_list
                    )
                )
                for c_list in containers
            )
            new_enumerators = tuple(
                ParameterList(
                    chain.from_iterable(
                        self.all_param_expansions(enumerator, cell)
                        for enumerator in e_list
                    )
                )
                for e_list in enumerators
            )
            self.directionless_point_placements[cell] = MappedTiling(
                new_base_tiling, new_avoiders, new_containers, new_enumerators
            )
        return self.directionless_point_placements[cell]

    @staticmethod
    def parameter_row_plex_and_ghost_maps(
        param: Parameter, ghost_row: int
    ) -> tuple[dict[int, int], dict[int, int]]:
        """Creates the row components for the mutliplex map and the new row/col map"""
        plex_map = {}
        ghost_map = {}
        found = 0
        for i in range(param.dimensions[1] + 2):
            ghost_map[i] = param.row_map[i - found] + found
            if i < ghost_row:
                plex_map[i] = i
            elif ghost_row <= i <= ghost_row + 2:
                plex_map[i] = ghost_row
                found = min(found + 1, 2)
            else:
                plex_map[i] = i - 2
        return plex_map, ghost_map

    @staticmethod
    def parameter_col_plex_and_ghost_maps(
        param: Parameter, ghost_col: int
    ) -> tuple[dict[int, int], dict[int, int]]:
        """Creates the col components for the mutliplex map and the new row/col map"""
        plex_map = {}
        ghost_map = {}
        found = 0
        for i in range(param.dimensions[0] + 1):
            ghost_map[i] = param.col_map[i - found] + 2 * found
            if i < ghost_col:
                plex_map[i] = i
            elif ghost_col <= i <= ghost_col + 1:
                plex_map[i] = ghost_col
                found = 1
            else:
                plex_map[i] = i - 1
        return plex_map, ghost_map

    @staticmethod
    def make_new_parameter(
        param: Parameter, multiplex_map: RowColMap, new_ghost_map: RowColMap
    ) -> Parameter:
        """Uses a multiplex map to create a new ghost,
        and uses new_ghost_map as the row/col map to the base tiling"""
        new_dimensions = (len(multiplex_map.col_map), len(multiplex_map.row_map))
        if new_dimensions == param.dimensions:
            new_obstructions, new_requirements = param.obstructions, param.requirements
        else:
            new_obstructions, new_requirements = multiplex_map.preimage_of_tiling(
                param.ghost
            )
        return Parameter(
            Tiling(new_obstructions, new_requirements, new_dimensions), new_ghost_map
        )

    @staticmethod
    def all_param_expansions(param: Parameter, image_cell: Cell) -> Iterable[Parameter]:
        """Creates all new parameters need for a point placement in image_cell"""
        image_cols, image_rows = param.map.image_rows_and_cols()
        if image_cell[0] in image_cols:
            col_maps = tuple(
                MTRequirementPlacement.parameter_col_plex_and_ghost_maps(
                    param, ghost_col
                )
                for ghost_col in param.map.preimages_of_col(image_cell[0])
            )
        else:
            col_maps = (
                (
                    {i: i for i in range(param.dimensions[0])},
                    {
                        key: value + 2 * int(value > image_cell[0])
                        for key, value in param.col_map.items()
                    },
                ),
            )
        if image_cell[1] in image_rows:
            row_maps = tuple(
                MTRequirementPlacement.parameter_row_plex_and_ghost_maps(
                    param, ghost_row
                )
                for ghost_row in param.map.preimages_of_row(image_cell[1])
            )
        else:
            row_maps = (
                (
                    {i: i for i in range(param.dimensions[1])},
                    {
                        key: value + 2 * int(value > image_cell[1])
                        for key, value in param.row_map.items()
                    },
                ),
            )
        for new_col_maps, new_row_maps in product(col_maps, row_maps):
            multiplex_map = RowColMap(new_col_maps[0], new_row_maps[0])
            ghost_map = RowColMap(new_col_maps[1], new_row_maps[1])
            yield MTRequirementPlacement.make_new_parameter(
                param, multiplex_map, ghost_map
            )
