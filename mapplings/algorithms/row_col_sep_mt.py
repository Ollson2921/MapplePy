"""Module for row and column separating mapped tilings and related strategies."""

import abc
from functools import cached_property
from itertools import combinations
from typing import Iterator, Optional
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from tilescope.strategies.row_column_separation import (
    LessThanRowColSeparation,
    LessThanOrEqualRowColSeparation,
    AbstractSeparation,
)
from ..mapped_tiling import MappedTiling, Parameter, ParameterList

Cell = tuple[int, int]


class AbstractMTRowColSeparation:
    """
    When separating, cells must be strictly above/below each other.
    """

    def __init__(
        self,
        mapped_tiling: MappedTiling,
        row_order: Optional[list[set[Cell]]] = None,
    ):
        self.mapped_tiling = mapped_tiling
        self.tiling = mapped_tiling.tiling
        self.avoiding_parameters = mapped_tiling.avoiding_parameters
        self.containing_parameters = mapped_tiling.containing_parameters
        self.enumeration_parameters = mapped_tiling.enumerating_parameters
        self.separation = self.separation_map(row_order=row_order)

    @cached_property
    def preimage_map(
        self,
    ) -> tuple[dict[int, tuple[int, ...]], dict[int, tuple[int, ...]]]:
        """Returns the preimage map for the row/col separation map."""
        return self.separation.row_col_map.preimage_map()

    @abc.abstractmethod
    def separation_map(
        self, row_order: Optional[list[set[Cell]]] = None
    ) -> AbstractSeparation:
        """Returns the row/col separation map."""

    @abc.abstractmethod
    def make_new_parameter(self, param: Parameter) -> Iterator[Parameter]:
        """Returns the adjusted param after row/col separation"""

    def update_params(
        self,
    ) -> tuple[ParameterList, list[ParameterList], list[ParameterList]]:
        """Updates the parameter to be consistent with the new base tiling and map."""

        new_avoiders = ParameterList(
            [
                param
                for param in self.avoiding_parameters
                for param in self.make_new_parameter(param)
            ]
        )
        new_containers = [
            ParameterList(
                [param for param in c_list for param in self.make_new_parameter(param)]
            )
            for c_list in self.containing_parameters
        ]
        new_enumerators = [
            ParameterList(
                [param for param in e_list for param in self.make_new_parameter(param)]
            )
            for e_list in self.enumeration_parameters
        ]
        return new_avoiders, new_containers, new_enumerators


class MTLTRowColSeparation(AbstractMTRowColSeparation):
    """
    Allow cells to interleave in the top/bottom rows when
    separating cells in a row.
    """

    def separation_map(
        self, row_order: Optional[list[set[Cell]]] = None
    ) -> LessThanRowColSeparation:
        """Returns the row/col separation map."""
        return LessThanRowColSeparation(self.tiling, row_order=row_order)

    def separate(self) -> Iterator[MappedTiling]:
        """Returns the row/col separated mapping"""
        if self.separation.row_col_map.is_identity():
            yield self.mapped_tiling
            return
        new_avoiders, new_containers, new_enumerators = self.update_params()
        for base in self.separation.row_col_separation():
            yield MappedTiling(base, new_avoiders, new_containers, new_enumerators)

    def make_new_parameter(self, param: Parameter) -> Iterator[Parameter]:
        """Returns the adjusted param after row/col separation"""
        row_param_to_bt_map, row_param_param_map = self.make_new_parameter_maps(
            param, rows=True
        )
        col_param_to_bt_map, col_param_param_map = self.make_new_parameter_maps(
            param, rows=False
        )
        n, m = (len(col_param_to_bt_map), len(row_param_to_bt_map))
        rc_map = RowColMap(col_param_param_map, row_param_param_map)
        obs, reqs = rc_map.preimage_of_tiling(param.ghost)
        implied_obs = self.implied_obs(rc_map, (n, m))
        new_ghost = Tiling(
            obs + implied_obs,
            reqs,
            (n, m),
        )
        yield Parameter(new_ghost, RowColMap(col_param_to_bt_map, row_param_to_bt_map))

    def implied_obs(
        self, param_map: RowColMap, dimensions: tuple[int, int]
    ) -> tuple[GriddedCayleyPerm, ...]:
        """The obstructions that were previously implied by GCPs being consistent."""
        col_map, row_map = param_map.preimage_map()
        n, m = dimensions
        implied_obs = []
        row_pairs = self.row_or_col_pairs(row_map, param_map.row_map)
        col_pairs = self.row_or_col_pairs(col_map, param_map.col_map)
        for row1, row2 in row_pairs:
            for col1, col2 in combinations(range(n), 2):
                if param_map.col_map[col1] != param_map.col_map[col2]:
                    implied_obs.append(
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1)),
                            ((col1, row1), (col2, row2)),
                        )
                    )
                    implied_obs.append(
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0)),
                            ((col1, row2), (col2, row1)),
                        )
                    )
        for col1, col2 in col_pairs:
            for row1, row2 in combinations(range(m), 2):
                if param_map.row_map[row1] != param_map.row_map[row2]:
                    implied_obs.append(
                        GriddedCayleyPerm(
                            CayleyPermutation((0, 1)),
                            ((col1, row1), (col2, row2)),
                        )
                    )
                    implied_obs.append(
                        GriddedCayleyPerm(
                            CayleyPermutation((1, 0)),
                            ((col2, row1), (col1, row2)),
                        )
                    )
        return tuple(implied_obs)

    def row_or_col_pairs(
        self,
        row_map: dict[int, tuple[int, ...]],
        forward_map: dict[int, int],
    ) -> set[tuple[int, int]]:
        """Finds the pairs of rows or columns to add implied obstructions to."""
        row_pairs = set()
        sorted_rows = set()
        for row in row_map:
            if row in sorted_rows:
                continue
            if len(row_map[row]) <= 1:
                continue
            initial_row = row_map[row][0]
            for next_row in row_map[row][1:]:
                if next_row != initial_row + 1:
                    end_points: list[int] = []
                    for skipped_row in range(initial_row + 1, next_row):
                        row_pairs.add((skipped_row, next_row))
                        for end_point in end_points:
                            row_pairs.add((skipped_row, end_point))
                        skipped_row_preimage = forward_map[skipped_row]
                        sorted_rows.add(skipped_row_preimage)
                        end_points.append(row_map[skipped_row_preimage][-1])
                initial_row = next_row
        return row_pairs

    def make_new_parameter_maps(
        self,
        param: Parameter,
        rows: bool,
    ) -> tuple[dict[int, int], dict[int, int]]:
        """Returns maps between old param and possible new params
        Each is in a tuple with indices of point rows to add obs for."""
        param_to_param_map: dict[int, int] = {}
        param_to_bt_map: dict[int, int] = {}
        bt_to_param_map = param.map.preimage_map()[rows]
        count = 0
        for bt_row in self.preimage_map[int(rows)]:
            if bt_row not in bt_to_param_map:
                continue
            bt_mapping_to = self.preimage_map[int(rows)][bt_row]
            for row_mapping_to in bt_mapping_to:
                for og_row in bt_to_param_map[bt_row]:
                    param_to_bt_map[count] = row_mapping_to
                    param_to_param_map[count] = og_row
                    count += 1
        return (param_to_bt_map, param_to_param_map)

    @staticmethod
    def separate_parameter(param: Parameter) -> Iterator[Parameter]:
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
        for parameter in separation.row_col_separation():
            yield Parameter(parameter, RowColMap(new_col_map, new_row_map))


class MTLTORERowColSeparation(AbstractMTRowColSeparation):
    """
    Allow cells to interleave in the top/bottom rows when
    separating cells in a row.
    """

    def separation_map(
        self, row_order: Optional[list[set[Cell]]] = None
    ) -> LessThanOrEqualRowColSeparation:
        """Returns the row/col separation map."""
        return LessThanOrEqualRowColSeparation(self.tiling, row_order=row_order)

    def separate(self) -> Iterator[MappedTiling]:
        """Returns the row/col separated mapping"""
        if self.separation.row_col_map.is_identity():
            yield self.mapped_tiling
            return
        new_avoiders, new_containers, new_enumerators = self.update_params()
        for base in self.separation.row_col_separation():
            yield MappedTiling(base, new_avoiders, new_containers, new_enumerators)

    def make_new_parameter_maps(
        self, param: Parameter, rows: bool, interleaving: bool = False
    ) -> list[tuple[dict[int, int], list[int], dict[int, int]]]:
        """Returns maps between old param and possible new params
        Each is in a tuple with indices of point rows to add obs for."""
        # pylint: disable=too-many-nested-blocks
        # pylint: disable=too-many-locals
        base_map = self.preimage_map
        base_rows_or_cols = (
            set(param.col_map.values()) if not rows else set(param.row_map.values())
        )
        reverse_col_maps: list[tuple[dict[int, int], list[int], dict[int, int]]] = [
            ({}, [], {})
        ]
        for bt_col in base_rows_or_cols:
            all_cols_to_map = (
                param.map.preimages_of_col(bt_col)
                if not rows
                else param.map.preimages_of_row(bt_col)
            )
            base_mapping_to = base_map[int(rows)][bt_col]
            if len(base_mapping_to) < 2:  # col didn't separate
                new_reverse_col_maps = []
                for reverse_col_map, point_rows_added, param_map in reverse_col_maps:
                    new_reverse_col_map = reverse_col_map.copy()
                    new_param_map = param_map.copy()
                    for og_col in all_cols_to_map:
                        new_col = (
                            og_col
                            + len(point_rows_added)
                            + len(point_rows_added) * int(interleaving)
                        )
                        new_reverse_col_map[new_col] = og_col
                        new_param_map[new_col] = base_mapping_to[0]
                    new_reverse_col_maps.append(
                        (new_reverse_col_map, point_rows_added, new_param_map)
                    )
            else:  # col did separate
                # choose a col to add a point row in,
                # map everything above to the top of separation and
                # everything below to the bottom of separation
                new_reverse_col_maps = []
                for col in all_cols_to_map:
                    for (
                        reverse_col_map,
                        point_rows_added,
                        param_map,
                    ) in reverse_col_maps:
                        new_reverse_col_map = reverse_col_map.copy()
                        new_point_rows_added = point_rows_added.copy()
                        new_param_map = param_map.copy()
                        for og_col in all_cols_to_map:
                            new_col = (
                                og_col
                                + len(new_point_rows_added)
                                + len(new_point_rows_added) * int(interleaving)
                            )
                            if og_col <= col:
                                new_reverse_col_map[new_col] = og_col
                                new_param_map[new_col] = base_mapping_to[0]
                            if col == og_col:
                                new_col = new_col + 1
                                new_reverse_col_map[new_col] = og_col
                                new_param_map[new_col] = base_mapping_to[1]
                                new_point_rows_added.append(col + 1)
                                if interleaving:
                                    new_reverse_col_map[
                                        og_col
                                        + len(new_point_rows_added)
                                        + len(new_point_rows_added) * int(interleaving)
                                    ] = og_col
                                    new_param_map[new_col + 1] = base_mapping_to[2]
                            if og_col > col:
                                new_reverse_col_map[new_col] = og_col
                                new_param_map[new_col] = base_mapping_to[
                                    1 + int(interleaving)
                                ]
                        new_reverse_col_maps.append(
                            (new_reverse_col_map, new_point_rows_added, new_param_map)
                        )
            reverse_col_maps = new_reverse_col_maps
        return reverse_col_maps

    def make_new_parameter(self, param: Parameter) -> Iterator[Parameter]:
        """Returns the adjusted param after row/col separation"""
        for row_map, rows_added, param_row_map in self.make_new_parameter_maps(
            param, rows=True, interleaving=True
        ):
            for col_map, _, param_col_map in self.make_new_parameter_maps(
                param, rows=False, interleaving=False
            ):
                rc_map = RowColMap(col_map, row_map)
                obs, reqs = rc_map.preimage_of_tiling(param.ghost)
                new_ghost = Tiling(obs, reqs, (len(col_map), len(row_map)))
                for point_row in rows_added:
                    new_ghost = new_ghost.add_point_row(point_row)
                new_map = RowColMap(param_col_map, param_row_map)

                yield Parameter(new_ghost, new_map)
