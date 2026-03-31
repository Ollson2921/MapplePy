"""Module with the parameter class."""

from collections import defaultdict
from copy import copy
from typing import Iterator, Iterable, Optional
from itertools import product, chain

from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.unplacement import PointUnplacement
from gridded_cayley_permutations.row_col_map import RowColMap
from gridded_cayley_permutations.factors import Factors

Cell = tuple[int, int]
Objects = defaultdict[tuple[int, ...], list[GriddedCayleyPerm]]


class Parameter(Tiling):
    """A tiling (called a ghost) mapping to a base tiling."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-public-methods
    def __init__(self, ghost: Tiling, row_col_map: RowColMap):
        self.map = row_col_map
        self.row_map = row_col_map.row_map
        self.col_map = row_col_map.col_map
        self.ghost = ghost
        super().__init__(
            ghost.obstructions, ghost.requirements, ghost.dimensions, False
        )

    @classmethod
    def empty_parameter(cls) -> "Parameter":
        """Returns an empty parameter."""
        return Parameter(Tiling.empty_tiling(), RowColMap({}, {}))

    def image_cells(self) -> set[Cell]:
        """Gives the cells to which the parameter maps"""
        return self.map.image_cells

    def injective_cells(self) -> set[Cell]:
        """Returns the set of cells that have a unique image under the row col map"""
        preimage_cols, preimage_rows = self.map.preimage_map()
        inj_cols = chain.from_iterable(
            (value for value in preimage_cols.values() if len(value) == 1)
        )
        inj_rows = chain.from_iterable(
            (value for value in preimage_rows.values() if len(value) == 1)
        )
        return set(product(inj_cols, inj_rows))

    def preimage_of_gcp(self, gcperm: GriddedCayleyPerm) -> Iterator[GriddedCayleyPerm]:
        """Returns the preimage of a gridded cayley permutation"""
        for gcp in self.map.preimage_of_gridded_cperm(gcperm):
            if self.gcp_in_tiling(gcp):
                yield gcp

    def gcp_has_preimage(self, gcp: GriddedCayleyPerm) -> bool:
        """Determines if the sub-gridding of the gcp that lives in the image region
        has a preimage on the ghost"""
        sub_gridding = gcp.sub_gridded_cayley_perm(self.image_cells())
        if not sub_gridding.positions and not self.requirements:
            return True
        for preimage in self.map.preimage_of_gridded_cperm(sub_gridding):
            if self.gcp_in_tiling(preimage):
                return True
        return False

    def backmap_obstructions(
        self, obstructions=Iterable[GriddedCayleyPerm]
    ) -> "Parameter":
        """Places the obstructions on the tiling"""
        new_ghost = super().add_obstructions(obstructions)
        return Parameter(new_ghost, self.map)

    def backmap_all_from_tiling(self, tiling: Tiling) -> "Parameter":
        """Places all obs and reqs of tiling into the parameter according to the row/col map."""
        new_obs = self.obstructions + self.map.preimage_of_obstructions(
            tiling.obstructions
        )
        new_reqs = self.requirements + self.map.preimage_of_requirements(
            tiling.requirements
        )
        return Parameter(Tiling(new_obs, new_reqs, self.dimensions), self.map)

    def back_map_point_obstructions_from_tiling(self, tiling: Tiling) -> "Parameter":
        """Places all point obstructions in the parameter"""
        new_obs = self.obstructions + self.map.preimage_of_obstructions(
            [ob for ob in tiling.obstructions if len(ob) == 1]
        )
        return Parameter(
            Tiling(new_obs, self.requirements, self.dimensions),
            self.map,
        )

    def update_active_cells(self, tiling: Tiling) -> "Parameter":
        """Makes self.active_cells account for point obs in the base tiling"""
        self.active_cells = self.active_cells & set(
            self.map.preimage_of_cells(tiling.active_cells)
        )
        new_obs = tuple(
            ob
            for ob in self.obstructions
            if ob.pattern == CayleyPermutation((0,))
            or all(cell in self.active_cells for cell in ob.positions)
        )
        new_reqs = []
        for req_list in self.requirements:
            new_req_list = tuple(
                req
                for req in req_list
                if all(cell in self.active_cells for cell in req.positions)
            )
            if not new_req_list:
                return Parameter(Tiling.empty_tiling(), RowColMap({}, {}))
            new_reqs.append(new_req_list)
        temp = Parameter(Tiling(new_obs, new_reqs, self.dimensions, False), self.map)
        temp.active_cells = self.active_cells
        return temp

    def find_blank_columns_and_rows_in_param(
        self, tiling: Tiling
    ) -> tuple[list[int], list[int]]:
        """Collect all obstructions and requirements. Any obs that imply point rows or cols
        ignore. Any that are implied by the tiling ignore. Then for the cells of gcps
        left, can't remove rows or columns that have any of these cells, remove all others.
        """
        point_cells = self.point_cells()
        if self.dimensions == (0, 0):
            return [], []
        if not self.obstructions and not self.requirements:
            return list(range(self.dimensions[0])), list(range(self.dimensions[1]))
        point_obs: set[GriddedCayleyPerm] = set()
        point_cols = set(cell[0] for cell in point_cells)
        for ob in self.obstructions:
            if ob.pattern == CayleyPermutation(
                (0, 1)
            ) or ob.pattern == CayleyPermutation((1, 0)):
                if (
                    ob.positions[0][1] in self.point_rows
                    and ob.positions[1][1] in self.point_rows
                ):
                    point_obs.add(ob)
                elif (
                    ob.positions[0] in point_cells
                    and ob.positions[1] == ob.positions[0]
                ):
                    point_obs.add(ob)
            elif (
                ob.pattern == CayleyPermutation((0, 0))
                and ob.positions[0] == ob.positions[1]
                and ob.positions[0] in point_cells
            ):
                point_obs.add(ob)
            elif (
                ob.pattern == CayleyPermutation((0,))
                and ob.positions[0][0] in point_cols
            ):
                point_obs.add(ob)
        not_point_obs = set(self.obstructions) - point_obs
        gcps_to_remove = set()
        for ob in not_point_obs:
            mapped_ob = self.map.map_gridded_cperm(ob)
            if mapped_ob in tiling.obstructions:
                gcps_to_remove.add(ob)
        final_obs_dont_ignore = not_point_obs - gcps_to_remove
        dont_ignore_cols = set(
            cell[0]
            for gcp in chain(final_obs_dont_ignore, *self.requirements)
            for cell in gcp.positions
        )
        dont_ignore_rows = set(
            cell[1]
            for gcp in chain(final_obs_dont_ignore, *self.requirements)
            for cell in gcp.positions
        )
        blank_rows = [
            row for row in range(self.dimensions[1]) if row not in dont_ignore_rows
        ]
        blank_cols = [
            col for col in range(self.dimensions[0]) if col not in dont_ignore_cols
        ]
        return blank_cols, blank_rows

    def delete_blank_row_cols_in_param(self, base_tiling: Tiling) -> "Parameter":
        """Deletes all blank rows and columns in the parameter."""
        blank_cols, blank_rows = self.find_blank_columns_and_rows_in_param(base_tiling)
        cols_to_remove = set()
        rows_to_remove = set()
        for i in range(self.dimensions[0] - 1):
            if i in blank_cols and i + 1 in blank_cols:
                cols_to_remove.add(i + 1)
        for j in range(self.dimensions[1] - 1):
            if j in blank_rows and j + 1 in blank_rows:
                rows_to_remove.add(j + 1)
        return self.delete_rows_and_columns(cols_to_remove, rows_to_remove)

    def find_empty_rows_and_columns(self):
        if not self.active_cells:
            return tuple(range(self.dimensions[0])), tuple(range(self.dimensions[1]))
        active_cols, active_rows = map(set, zip(*self.active_cells))
        empty_cols = set(range(self.dimensions[0])) - active_cols
        empty_rows = set(range(self.dimensions[1])) - active_rows
        return tuple(empty_cols), tuple(empty_rows)

    def delete_rows_and_columns(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> "Parameter":
        """Removes rows and columns from the parameter.
        Adjusts row/col map keys while preserving values."""
        new_ghost = super().delete_rows_and_columns(cols, rows)
        image_cols = sorted(
            (self.col_map[key] for key in self.col_map.keys() if key not in cols)
        )
        image_rows = sorted(
            (self.row_map[key] for key in self.row_map.keys() if key not in rows)
        )
        new_col_map = dict(enumerate(image_cols))
        new_row_map = dict(enumerate(image_rows))
        if 0 in new_ghost.dimensions:
            return Parameter(Tiling([], [], (0, 0)), RowColMap({}, {}))
        return Parameter(new_ghost, RowColMap(new_col_map, new_row_map))

    def delete_preimage_of_rows_and_columns(
        self,
        image_cols_to_delete: tuple[int, ...],
        image_rows_to_delete: tuple[int, ...],
    ) -> "Parameter":
        """Removes rows and columns from the parameter.
        Adjusts row/col map keys and values."""
        preimage_cols = self.map.preimages_of_cols(image_cols_to_delete)
        preimage_rows = self.map.preimages_of_rows(image_rows_to_delete)
        temp_param = self.delete_rows_and_columns(preimage_cols, preimage_rows)
        new_col_map, new_row_map = {}, {}
        for key, value in temp_param.col_map.items():
            adjust = sum(idx < value for idx in image_cols_to_delete)
            new_col_map[key] = temp_param.col_map[key] = value - adjust
        for key, value in temp_param.row_map.items():
            adjust = sum(idx < value for idx in image_rows_to_delete)
            new_row_map[key] = temp_param.row_map[key] = value - adjust
        return Parameter(temp_param.ghost, RowColMap(new_col_map, new_row_map))

    def insert_cols_and_rows(
        self, cols: Iterable[int], rows: Iterable[int]
    ) -> "Parameter":
        """Inserts a blank col or col at each index.
        New col/row gets map data from the col/row at the given index."""
        col_adjust = {
            i: i + sum((j < i for j in cols)) for i in range(self.dimensions[0])
        }
        row_adjust = {
            i: i + sum((j < i for j in rows)) for i in range(self.dimensions[1])
        }
        adjust = RowColMap(col_adjust, row_adjust)
        new_obs = adjust.map_gridded_cperms(self.obstructions)
        new_reqs = adjust.map_requirements(self.requirements)
        new_col_map = dict[int, int]()
        new_row_map = dict[int, int]()
        new_dimensions = (
            self.dimensions[0] + len(tuple(cols)),
            self.dimensions[1] + len(tuple(rows)),
        )
        tweak = 0

        for i in range(new_dimensions[0]):
            if i - tweak - 1 in cols:
                if i - tweak - 1 == -1:
                    new_col_map[i] = self.col_map[0]
                    tweak += 1
                    continue
                new_col_map[i] = new_col_map[i - 1]
                tweak += 1
            else:
                new_col_map[i] = self.col_map[i - tweak]
        tweak = 0
        for i in range(new_dimensions[1]):
            if i - tweak - 1 in rows:
                if i - tweak - 1 == -1:
                    new_row_map[i] = self.row_map[0]
                    tweak += 1
                    continue
                new_row_map[i] = new_row_map[i - 1]
                tweak += 1
            else:
                new_row_map[i] = self.row_map[i - tweak]
        return Parameter(
            Tiling(
                new_obs,
                new_reqs,
                new_dimensions,
                False,
            ),
            RowColMap(new_col_map, new_row_map),
        )

    def sub_parameter(self, cells: Iterable[Cell]) -> "Parameter":
        """Returns the parameter containing only the specified cells"""
        cols, rows = zip(*cells)
        cols_to_delete = {i for i in range(self.dimensions[0]) if i not in cols}
        rows_to_delete = {i for i in range(self.dimensions[1]) if i not in rows}
        return self.delete_rows_and_columns(cols_to_delete, rows_to_delete)

    def factor(self) -> Iterator["Parameter"]:
        """Factors the ghost and combines factors with overlapping images."""
        factor_cells = Factors(self.ghost).find_factors_as_cells
        find_images = self.map.image_rows_and_cols
        factor_image_rows_and_cols = list(
            (find_images(*zip(*factor)) for factor in factor_cells)
        )
        for index1, pair1 in enumerate(factor_image_rows_and_cols):
            for index2, pair2 in enumerate(factor_image_rows_and_cols):
                if pair1[0] & pair2[0] and pair1[1] & pair2[1]:
                    new_images = (pair1[0] | pair2[0], pair1[1] | pair2[1])
                    factor_image_rows_and_cols[index1] = new_images
                    factor_image_rows_and_cols[index2] = new_images
        make_factor = self.map.preimages_of_rows_and_cols
        factors = {
            tuple(product(*make_factor(*factor_image)))
            for factor_image in factor_image_rows_and_cols
        }
        for factor in factors:
            yield self.sub_parameter(factor)

    def unplace_point(self, cell: Cell) -> "Parameter":
        """index is the index of the point to be unplaced in self.point_cells"""
        new_ghost = PointUnplacement(self.ghost, cell).unplace_point()
        temp_col_map, temp_row_map = self.col_map, self.row_map
        del temp_col_map[cell[0]], temp_col_map[cell[0] + 1]
        del temp_row_map[cell[1]], temp_row_map[cell[1] + 1]
        new_col_map = dict(enumerate(temp_col_map.values()))
        new_row_map = dict(enumerate(temp_row_map.values()))
        return Parameter(new_ghost, RowColMap(new_col_map, new_row_map))

    def positive_cells_are_valid(self, tiling: Tiling) -> bool:
        """Creates a set of requirements implied by the ghost's positive cells.
        Returns False if any of these requirements contradict tiling's obstructions."""

        positive_cells = self.positive_cells()
        by_cols, by_rows = defaultdict(set), defaultdict(set)
        for cell in positive_cells:
            by_cols[cell[0]].add(cell)
            by_rows[cell[1]].add(cell)
        final_cells = list[tuple[tuple[int, int], ...]]()
        for cell_list in set(
            product(*by_cols.values())
        ):  # each cell list has one positive cell from each col
            used_rows = set(cell[1] for cell in cell_list)
            final_cells.extend(product(*(by_rows[i] for i in used_rows)))
            # now we have lists of cells that don't overlap in rows/cols

        def make_mapped_gcp(cells: Iterable[tuple[int, int]]) -> GriddedCayleyPerm:
            cells = sorted(cells)
            perm = CayleyPermutation.standardise((cell[1] for cell in cells))
            return GriddedCayleyPerm(
                perm, ((self.col_map[cell[0]], self.row_map[cell[1]]) for cell in cells)
            )

        reqs_to_check = set(make_mapped_gcp(cells) for cells in set(final_cells))
        return not any(req.contains(tiling.obstructions) for req in reqs_to_check)

    def is_contradictory(self, tiling: Tiling) -> bool:
        """Returns True if the parameter is contradictory.
        Is contradictory if any of the requirements in the ghost map to a gcp
        containing an obstruction in the tiling

        Ideal world, we would backmap the obs and reqs from parent to the ghost
        and check if it is empty, however this is probably really slow!
        """
        if any(
            all(
                not self.ghost.satisfies_obstructions(gcp)
                for req in req_list
                for gcp in self.map.preimage_of_gridded_cperm(req)
            )
            for req_list in tiling.requirements
            if all(
                cell in self.image_cells()
                for cell in chain.from_iterable(req.positions for req in req_list)
            )
        ):
            return True
        for req_list in self.ghost.requirements:
            if all(
                self.map.map_gridded_cperm(gcp).contains(tiling.obstructions)
                for gcp in req_list
            ):
                return True
        return False

    @staticmethod
    def make_vincular(
        pattern: tuple[int, ...], adjacency: Iterable[int], image_cell: Cell = (0, 0)
    ) -> "Parameter":
        """Returns a parameter equivilent to the vincular pattern mapping to image_cell"""
        col_positions = list[int]()
        col = 0 - int(0 in adjacency)
        obs = set[GriddedCayleyPerm]()
        for idx in range(len(pattern)):
            if idx + 1 in adjacency:
                col += 1
                obs.update(
                    {
                        GriddedCayleyPerm((0, 0), ((col, 0), (col, 0))),
                        GriddedCayleyPerm((0, 1), ((col, 0), (col, 0))),
                        GriddedCayleyPerm((1, 0), ((col, 0), (col, 0))),
                    }
                )
                col_positions.append(col)
            elif idx in adjacency:
                col += 1
                obs.update(
                    {
                        GriddedCayleyPerm((0, 0), ((col, 0), (col, 0))),
                        GriddedCayleyPerm((0, 1), ((col, 0), (col, 0))),
                        GriddedCayleyPerm((1, 0), ((col, 0), (col, 0))),
                    }
                )
                col_positions.append(col)
                col += 1
            else:
                col_positions.append(col)
        ghost = Tiling(
            obs,
            [[GriddedCayleyPerm(pattern, [(col, 0) for col in col_positions])]],
            (col + 1, 1),
        )
        col_map = {i: image_cell[0] for i in range(col + 1)}
        return Parameter(ghost, RowColMap(col_map, {0: image_cell[1]}))

    @staticmethod
    def make_covincular(
        pattern: tuple[int, ...], adjacency: Iterable[int], image_cell: Cell = (0, 0)
    ) -> "Parameter":
        """Returns a parameter equivilent to the vincular pattern mapping to image_cell"""
        row_positions = list[int]()
        row = 0 - int(0 in adjacency)
        obs = set[GriddedCayleyPerm]()
        for idx in range(len(pattern)):
            if idx + 1 in adjacency:
                row += 1
                obs.update(
                    {
                        GriddedCayleyPerm((0, 0), ((0, row), (0, row))),
                        GriddedCayleyPerm((0, 1), ((0, row), (0, row))),
                        GriddedCayleyPerm((1, 0), ((0, row), (0, row))),
                    }
                )
                row_positions.append(row)
            elif idx in adjacency:
                row += 1
                obs.update(
                    {
                        GriddedCayleyPerm((0, 0), ((0, row), (0, row))),
                        GriddedCayleyPerm((0, 1), ((0, row), (0, row))),
                        GriddedCayleyPerm((1, 0), ((0, row), (0, row))),
                    }
                )
                row_positions.append(row)
                row += 1
            else:
                row_positions.append(row)
        ghost = Tiling(
            obs,
            [[GriddedCayleyPerm(pattern, [(0, row) for row in row_positions])]],
            (1, row + 1),
        )
        row_map = {i: image_cell[1] for i in range(row + 1)}
        return Parameter(ghost, RowColMap({0: image_cell[0]}, row_map))

    def to_html_representation(self) -> str:
        """Returns an html representation of the tilings object
        Mimics code from original tilings"""
        rc_style = """
            border: 0;
            width: 24px;
            height: 24px;
            text-align: center;
            background-color : white;
            color : grey;
            """
        dim_i, dim_j = self.dimensions
        result = self._html_table()
        result.insert(-1, "<tr>")
        result.insert(-1, f"<th style='{rc_style}'>")
        result.insert(-1, " ")
        result.insert(-1, "</th>")
        for j in range(dim_i):
            result.insert(-1, f"<th style='{rc_style}'>")
            result.insert(-1, str(self.col_map[j]))
            result.insert(-1, "</th>")
        result.insert(-1, "</tr>")
        row_width = 3 * (dim_i) + 2
        for i in range(dim_j):
            index = (i) * (row_width + 3) + 2
            result.insert(index, "</th>")
            result.insert(index, str(self.row_map[dim_j - i - 1]))
            result.insert(index, f"<th style='{rc_style}'>")

        return "".join(result)

    def compare_parameters(
        self, other: "Parameter", depth: int = 4
    ) -> tuple[bool, Optional[GriddedCayleyPerm]]:
        """Compares the gcps that live on self to the gcps on other up to size depth"""

        col_map = {
            val: key
            for key, val in enumerate(
                sorted(set(self.col_map.values()) | set(other.col_map.values()))
            )
        }
        row_map = {
            val: key
            for key, val in enumerate(
                sorted(set(self.row_map.values()) | set(other.row_map.values()))
            )
        }
        self_reduction = RowColMap(
            {key: col_map[val] for key, val in self.col_map.items()},
            {key: row_map[val] for key, val in self.row_map.items()},
        )
        other_reduction = RowColMap(
            {key: col_map[val] for key, val in other.col_map.items()},
            {key: row_map[val] for key, val in other.row_map.items()},
        )
        temp_self = Parameter(self.ghost, self_reduction)
        temp_other = Parameter(other.ghost, other_reduction)
        base = Tiling([], [], (len(col_map), len(row_map)))
        i = 0
        while i < depth:
            for gcp in base.objects_of_size(i):
                if temp_self.gcp_has_preimage(gcp) != temp_other.gcp_has_preimage(gcp):
                    return False, gcp
            i += 1
        return True, None

    def objects_of_size(self, n, **parameters) -> Iterator[GriddedCayleyPerm]:
        """Return gridded Cayley permutations of size n in the tiling."""
        for val in self.get_objects(n).values():
            yield from val

    def get_objects(self, n: int) -> Objects:
        """Return the objects of size n in the tiling."""
        objects = defaultdict(list)
        col_map = {
            val: key for key, val in enumerate(sorted(set(self.col_map.values())))
        }
        row_map = {
            val: key for key, val in enumerate(sorted(set(self.row_map.values())))
        }
        map_reduction = RowColMap(
            {key: col_map[val] for key, val in self.col_map.items()},
            {key: row_map[val] for key, val in self.row_map.items()},
        )
        temp = Parameter(self.ghost, map_reduction)
        base = Tiling([], [], (len(col_map), len(row_map)))
        for gcp in base.objects_of_size(n):
            if temp.gcp_has_preimage(gcp):
                param = self.get_parameters(gcp)
                objects[param].append(gcp)
        return objects

    def get_parameters(self, obj: GriddedCayleyPerm) -> tuple[int, ...]:
        """Parameters are not what you think!!! This is specific to
        combinatorical class parameters"""
        return (1,)

    # dunder methods

    def to_jsonable(self) -> dict:
        d = super().to_jsonable()
        d["row_col_map"] = self.map.to_jsonable()
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Parameter":
        """Used for constructing Parameters from a dictionary."""
        d = copy(d)
        row_col_map = RowColMap.from_dict(d.pop("row_col_map"))
        tiling = Tiling.from_dict(d)
        return cls(tiling, row_col_map)

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"({repr(self.ghost)}, {repr(self.map)})"

    def __bool__(self) -> bool:
        return not bool(self.ghost)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Parameter):
            return NotImplemented
        return (self.ghost, self.map) == (other.ghost, other.map)

    def __hash__(self) -> int:
        return hash(
            (
                self.ghost,
                tuple(sorted(self.col_map.items())),
                tuple(sorted(self.row_map.items())),
            )
        )

    def __leq__(self, other: object) -> bool:
        if not isinstance(other, Parameter):
            return NotImplemented
        return (self.map, self.ghost) <= (other.map, other.ghost)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Parameter):
            return NotImplemented
        return (self.map, self.ghost) < (other.map, other.ghost)

    def _string_table(self) -> list[str]:
        """Creates a list of strings for each row of the __str__ grid"""
        if self.dimensions == (0, 0):
            return ["┌ ┐", " ε ", "└ ┘"]
        cell_labels = self.cell_labels

        # Style
        for cell in self.empty_cells():
            cell_labels[cell] = "░"
            if cell in self.point_rows:
                cell_labels[cell] = "#"
        row_separator = "├" + ("┼─" * self.dimensions[0] + "┤")[1:]
        internal_row = "├" + ("┼ " * self.dimensions[0] + "┤")[1:]
        top_row = "┌" + ("┬─" * self.dimensions[0])[1:] + "┐"
        bottom_row = "└" + ("┴─" * self.dimensions[0])[1:] + "┘"

        # Make Table
        final_table = [row_separator]
        for row in range(self.dimensions[1]):
            new_row = "│"
            for col in range(self.dimensions[0]):
                cell_end = "│"
                if col < self.dimensions[0] - 1:
                    if self.col_map[col] == self.col_map[col + 1]:
                        cell_end = " "
                label = " "
                if (col, row) in cell_labels:
                    label = self.cell_labels[(col, row)]
                new_row += label + cell_end
            separator = row_separator
            if row < self.dimensions[1] - 1:
                if self.row_map[row] == self.row_map[row + 1]:
                    separator = internal_row
            new_row += f"{self.row_map[row]}"
            if row in self.point_rows:
                new_row += "*"
            final_table += [new_row, separator]
        final_table.reverse()
        final_table[0] = top_row
        final_table[-1] = bottom_row
        final_table.append(
            " " + " ".join((str(value) for _, value in self.col_map.items()))
        )
        return final_table
