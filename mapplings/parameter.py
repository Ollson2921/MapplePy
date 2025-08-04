"""Module with the parameter class."""

from typing import Iterator, Iterable
from itertools import product

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.row_col_map import RowColMap
from gridded_cayley_permutations.simplify_obstructions_and_requirements import (
    SimplifyObstructionsAndRequirements,
)
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

    def preimage_of_gcp(self, gcperm: GriddedCayleyPerm) -> Iterator[GriddedCayleyPerm]:
        """Returns the preimage of a gridded cayley permutation"""
        for gcp in self.map.preimage_of_gridded_cperm(gcperm):
            if self.gcp_in_tiling(gcp):
                yield gcp

    def gcp_has_preimage(self, gcp: GriddedCayleyPerm) -> bool:
        """Determines if the sub-gridding of the gcp that lives in the image region
        has a preimage on the ghost"""
        sub_gridding = gcp.sub_gridded_cayley_perm(self.image_cells())
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
        """Reutrns the parameter containig only the specified cells"""
        cols, rows = zip(*cells)
        cols_to_delete = {i for i in range(self.dimensions[0]) if i not in cols}
        rows_to_delete = {i for i in range(self.dimensions[1]) if i not in rows}
        return self.delete_rows_and_columns(cols_to_delete, rows_to_delete)

    def factor(self) -> Iterator["Parameter"]:
        """Factors the ghost and combines factors with overlapping images."""
        factor_cells = Factors(self.ghost).find_factors_as_cells()
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
        ):
            return True
        for req_list in self.ghost.requirements:
            if all(
                self.map.map_gridded_cperm(gcp).contains(tiling.obstructions)
                for gcp in req_list
            ):
                return True
        return False

    def strong_is_contradictory(self, tiling: Tiling) -> bool:
        """backmap the obs and reqs from parent to the ghost
        and check if it is empty"""
        return self.backmap_all_from_tiling(tiling).is_empty()

    # dunder methods

    @classmethod
    def from_dict(cls, d: dict) -> "Parameter":
        """Used for constructing Parameters from a dictionary."""
        raise NotImplementedError

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
