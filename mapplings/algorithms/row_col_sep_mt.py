"""Module for row and column separating mapped tilings and related strategies."""

import abc
from functools import cached_property
from typing import Iterator, Optional
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
        rc_map = RowColMap(col_param_param_map, row_param_param_map)
        obs, reqs = rc_map.preimage_of_tiling(param.ghost)
        new_ghost = Tiling(
            obs,
            reqs,
            (len(col_param_to_bt_map), len(row_param_to_bt_map)),
        )
        yield Parameter(new_ghost, RowColMap(col_param_to_bt_map, row_param_to_bt_map))

    def make_new_parameter_maps(
        self,
        param: Parameter,
        rows: bool,
    ) -> tuple[dict[int, int], dict[int, int]]:
        """Returns maps between old param and possible new params
        Each is in a tuple with indices of point rows to add obs for."""
        param_to_param_map: dict[int, int] = {}
        param_to_bt_map: dict[int, int] = {}
        new_param_col = 0
        count = -1
        bt_count = 0
        old_bt_mapping_to = None
        for n in range(param.dimensions[int(rows)]):
            bt_mapping_to = self.preimage_map[int(rows)][
                param.col_map[n] if not rows else param.row_map[n]
            ]
            if len(bt_mapping_to) > 1 and old_bt_mapping_to == bt_mapping_to:
                bt_count += 1
            else:
                bt_count = 0
                count += 1
            for i in range(len(bt_mapping_to)):
                param_to_bt_map[new_param_col] = bt_mapping_to[bt_count]
                param_to_param_map[new_param_col] = i + count
                new_param_col += 1
            old_bt_mapping_to = bt_mapping_to
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
