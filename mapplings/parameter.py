"""Module with the parameter class."""

from collections import defaultdict
from copy import copy
from typing import Iterator, Iterable
from itertools import product, chain

from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.unplacement import PointUnplacement
from gridded_cayley_permutations.row_col_map import RowColMap
from gridded_cayley_permutations.factors import Factors

Cell = tuple[int, int]


class Parameter(Tiling):
    """A tiling (called a ghost) mapping to a base tiling."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-positional-arguments
    def __init__(self, ghost: Tiling, row_col_map: RowColMap):
        self.map = row_col_map
        self.row_map = row_col_map.row_map
        self.col_map = row_col_map.col_map
        self.ghost = ghost
        super().__init__(
            ghost.obstructions, ghost.requirements, ghost.dimensions, False
        )

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
        if not sub_gridding.positions and not self.positive_cells():
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
        temp = Parameter(Tiling(new_obs, new_reqs, self.dimensions), self.map)
        temp.active_cells = self.active_cells
        return temp

    def find_blank_columns_and_rows_in_param(
        self, tiling: Tiling
    ) -> tuple[list[int], list[int]]:
        """Collect all obstructions and requirements. Any obs that imply point rows or cols
        ignore. Any that are implied by the tiling ignore. Then for the cells of gcps
        left, can't remove rows or columns that have any of these cells, remove all others.
        """
        if self.dimensions == (0, 0):
            return [], []
        if not self.obstructions and not self.requirements:
            return list(range(self.dimensions[0])), list(range(self.dimensions[1]))
        point_obs: set[GriddedCayleyPerm] = set()
        point_cols = set(cell[0] for cell in self.point_cells())
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
        dont_ignore_rows = set(
            ob.positions[i][1]
            for ob in final_obs_dont_ignore
            for i in range(len(ob.pattern))
        ).union(
            set(
                req.positions[i][0]
                for req_list in self.requirements
                for req in req_list
                for i in range(len(req.pattern))
            )
        )
        dont_ignore_cols = set(
            ob.positions[i][0]
            for ob in final_obs_dont_ignore
            for i in range(len(ob.pattern))
        ).union(
            set(
                req.positions[i][0]
                for req_list in self.requirements
                for req in req_list
                for i in range(len(req.pattern))
            )
        )
        blank_rows = [
            row for row in range(self.dimensions[1]) if row not in dont_ignore_rows
        ]
        blank_cols = [
            col for col in range(self.dimensions[0]) if col not in dont_ignore_cols
        ]
        return blank_cols, blank_rows

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
        return (self.ghost, self.map) <= (other.ghost, other.map)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Parameter):
            return NotImplemented
        return (self.ghost, self.map) < (other.ghost, other.map)

    def __str__(self) -> str:
        return str(self.map) + "\n" + str(self.ghost)
