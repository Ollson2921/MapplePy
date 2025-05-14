"""Module with the parameter class."""

from typing import Iterator, Tuple, Set, Iterable, Callable
from itertools import product

from gridded_cayley_permutations import Tiling, GriddedCayleyPerm
from gridded_cayley_permutations.factors import Factors
from cayley_permutations import CayleyPermutation

from .row_col_map import RowColMap
from . import cleaning_keys as ck


Cell = Tuple[int, int]


class Parameter:
    """A tiling (called a ghost) mapping to a base tiling."""

    def __init__(self, ghost: Tiling, row_col_map: RowColMap):
        self.map = row_col_map
        self.row_map = row_col_map.row_map
        self.col_map = row_col_map.col_map
        self.ghost = ghost
        self.obstructions = ghost.obstructions
        self.requirements = ghost.requirements
        self.dimensions = ghost.dimensions
        self.cleaner = ParamCleaner()

    def image_rows_and_cols(self) -> Tuple[Set[int], Set[int]]:
        """Gives the indices for the rows and cols to which the parameter maps"""
        return set(self.col_map.values()), set(self.row_map.values())

    def image_cells(self) -> Set[Cell]:
        """Gives the cells to which the parameter maps"""
        return set(product(*self.image_rows_and_cols()))

    def preimage_of_gcp(self, gcperm: GriddedCayleyPerm) -> Iterator[GriddedCayleyPerm]:
        """Returns the preimage of a gridded cayley permutation"""
        for gcp in self.map.preimage_of_gridded_cperm(gcperm):
            if self.ghost.gcp_in_tiling(gcp):
                yield gcp

    def gcp_has_preimage(self, gcp: GriddedCayleyPerm) -> bool:
        """Determines if the sub-gridding of the gcp that lives in the image region
        has a preimage on the ghost"""
        sub_gridding = gcp.sub_gridded_cayley_perm(self.image_cells())
        for preimage in self.map.preimage_of_gridded_cperm(sub_gridding):
            if self.ghost.gcp_in_tiling(preimage):
                return True
        return False

    def backmap_obstructions(
        self, obstructions=Iterable[GriddedCayleyPerm]
    ) -> "Parameter":
        """Places the obstructions on the tiling"""
        new_ghost = self.ghost.add_obstructions(obstructions)
        return Parameter(new_ghost, self.map)

    def backmap_all_from_tiling(self, tiling: Tiling) -> "Parameter":
        """Places all obs and reqs of tiling into the parameter according to the row/col map."""
        new_obs = self.ghost.obstructions + self.map.preimage_of_obstructions(
            tiling.obstructions
        )
        new_reqs = self.ghost.requirements + self.map.preimage_of_requirements(
            tiling.requirements
        )
        return Parameter(Tiling(new_obs, new_reqs, self.ghost.dimensions), self.map)

    def back_map_point_obstructions_from_tiling(self, tiling: Tiling) -> "Parameter":
        """Places all point obstructions in the parameter"""
        new_obs = self.ghost.obstructions + self.map.preimage_of_obstructions(
            [ob for ob in tiling.obstructions if len(ob) == 1]
        )
        return Parameter(
            Tiling(new_obs, self.ghost.requirements, self.ghost.dimensions),
            self.map,
        )

    def delete_rows_and_columns(
        self, cols_to_delete: Iterable[int], rows_to_delete: Iterable[int]
    ) -> "Parameter":
        """Removes rows and columns from the parameter.
        Adjusts row/col map keys while preserving values."""
        # """vvv This bit is only needed while deleting rows and cols is broken vvv"""
        keep_cols = (i for i in range(self.dimensions[0]) if i not in cols_to_delete)
        keep_rows = (i for i in range(self.dimensions[1]) if i not in rows_to_delete)
        # """^^^ This bit is only needed while deleting rows and cols is broken ^^^"""
        new_ghost = self.ghost.sub_tiling(
            product(keep_cols, keep_rows)
        ).delete_rows_and_columns(cols_to_delete, rows_to_delete)
        image_cols = sorted(
            (
                self.col_map[key]
                for key in self.col_map.keys()
                if key not in cols_to_delete
            )
        )
        image_rows = sorted(
            (
                self.row_map[key]
                for key in self.row_map.keys()
                if key not in rows_to_delete
            )
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
        preimage_rows = self.map.preimages_of_cols(image_rows_to_delete)
        temp_param = self.delete_rows_and_columns(preimage_cols, preimage_rows)
        new_map = temp_param.map.standardise_map()
        return Parameter(temp_param.ghost, new_map)

    def sub_parameter(self, cells: Iterable[Cell]) -> "Parameter":
        """Reutrns the parameter containig only the specified cells"""
        cols, rows = zip(*cells)
        cols_to_delete = {i for i in range(self.dimensions[0]) if i not in cols}
        rows_to_delete = {i for i in range(self.dimensions[1]) if i not in rows}
        return self.delete_rows_and_columns(cols_to_delete, rows_to_delete)

    def factor(self) -> Iterator["Parameter"]:
        """Factors the ghost and combines factors with overlapping images."""
        factor_cells = Factors(self.ghost).find_factors_as_cells()
        find_images = lambda pair: self.map.images_of_rows_and_cols(*pair)
        factor_image_rows_and_cols = list(
            (find_images(zip(*factor)) for factor in factor_cells)
        )
        for index1, pair1 in enumerate(factor_image_rows_and_cols):
            for index2, pair2 in enumerate(factor_image_rows_and_cols):
                if pair1[0] & pair2[0] and pair1[1] & pair2[1]:
                    new_images = (pair1[0] | pair2[0], pair1[1] | pair2[1])
                    factor_image_rows_and_cols[index1] = new_images
                    factor_image_rows_and_cols[index2] = new_images
        make_factor = lambda pair: product(*self.map.preimages_of_rows_and_cols(*pair))
        factors = {
            tuple(make_factor(factor_image))
            for factor_image in factor_image_rows_and_cols
        }
        for factor in factors:
            yield self.sub_parameter(factor)

    def is_contradictory(self, tiling: Tiling) -> bool:
        """Returns True if the parameter is contradictory.
        Is contradictory if any of the requirements in the ghost map to a gcp
        containing an obstruction in the tiling
        """
        raise NotImplementedError

    def add_to_cleaner(self, cleaner_items: Iterable[int]) -> "Parameter":
        """Adds the cleaner items to the Parameter's Cleaner's todo list."""
        new_param = self
        new_param.cleaner = self.cleaner + cleaner_items
        return new_param

    def clean_desired(self) -> "Parameter":
        """Cleans the parameter according to the todo list"""
        return self.cleaner(self)

    def full_cleanup(self) -> "Parameter":
        """Applies all cleaning functions to the parameter"""
        return ParamCleaner.full_cleanup(self)

    # dunder methods

    @classmethod
    def from_dict(cls, d: dict) -> "Parameter":
        """Used for constructing Parameters from a dictionary."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"({repr(self.ghost)}, {repr(self.map)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Parameter):
            return NotImplemented
        return self.ghost == other.ghost and self.map == other.map

    def __hash__(self) -> int:
        return hash((self.ghost, self.map))

    def __leq__(self, other: "Parameter") -> int:
        return self.ghost <= other.ghost

    def __lt__(self, other: "Parameter") -> bool:
        return self.ghost < other.ghost

    def __str__(self) -> str:
        return str(self.map) + "\n" + str(self.ghost)


# This is the mao used in the cleaner functions and the decorator used to build the map
param_cleaning_function_map = dict[int, Callable[[Parameter], Parameter]]()
param_register = ck.make_register(param_cleaning_function_map)


class ParamCleaner:
    """The class used to clean paramaters.
    Core fuctions are decorated with @param_register(index)
    where index is the order of cleaning"""

    def __init__(self, todo_list: Iterable[int] = set()):
        self.todo_list = set(todo_list)

    def __call__(self, param: Parameter) -> Parameter:
        """Cleans the input param according to the cleaner's todo_list"""
        return ParamCleaner.list_cleanup(param, self.todo_list)

    def __add__(self, other: Iterable[int]) -> "ParamCleaner":
        return ParamCleaner(self.todo_list | set(other))

    @staticmethod
    def list_cleanup(param: Parameter, cleaning_list: Iterable[int]) -> Parameter:
        """Applies all functions indicated by keys in cleaning_list"""
        if -1 in cleaning_list:
            cleaning_list = param_cleaning_function_map.keys()
        cleaning_list = tuple(sorted(cleaning_list))
        new_param = param
        for i in cleaning_list:
            new_param = param_cleaning_function_map[i](new_param)
        return new_param

    def tracked_cleanup(
        self, param: Parameter, cleaning_list: Iterable[int]
    ) -> Parameter:
        """Cleans param according to the cleaning list,
        removes any completed cleaning functions from the cleaner's todo_list"""
        if -1 in cleaning_list:
            cleaning_list = param_cleaning_function_map.keys()
        new_param = ParamCleaner.list_cleanup(param, cleaning_list)
        new_param.cleaner = ParamCleaner(self.todo_list - set(cleaning_list))
        return new_param

    @staticmethod
    def full_cleanup(param: Parameter) -> Parameter:
        """Applies all cleanup functions."""
        return ParamCleaner.list_cleanup(
            param, tuple(param_cleaning_function_map.keys())
        )

    # Final Methods
    @param_register(ck.pc_fusion)
    @staticmethod
    def reduce_by_fusion(param: Parameter) -> Parameter:
        """Fuses valid rows and columns"""
        return ParamCleaner.fuse_valid_rows_or_cols(
            ParamCleaner.fuse_valid_rows_or_cols(param, 0), 1
        )

    @param_register(ck.pc_reduce_empty)
    @staticmethod
    def reduce_empty_rows_and_cols(param: Parameter) -> Parameter:
        """Removes empty rows and columns in the parameter"""
        empty_cols, empty_rows = param.ghost.find_empty_rows_and_columns()
        cols_to_remove, rows_to_remove = set(empty_cols), set(empty_rows)
        col_preimages, row_preimages = param.map.preimage_map()
        for key in col_preimages.keys():
            intersection = set(col_preimages[key]) & cols_to_remove
            if len(intersection) == len(col_preimages[key]):
                intersection.remove(col_preimages[key][0])
                cols_to_remove = cols_to_remove - intersection
        for key in row_preimages.keys():
            intersection = set(row_preimages[key]) & rows_to_remove
            if len(intersection) == len(row_preimages[key]):
                intersection.remove(row_preimages[key][0])
                rows_to_remove = rows_to_remove - intersection
        return param.delete_rows_and_columns(cols_to_remove, rows_to_remove)

    @param_register(ck.pc_remove_blank)
    @staticmethod
    def remove_blank_rows_and_cols(param: Parameter) -> Parameter:
        """Deletes all rows and cols which have no obs or reqs"""
        raise NotImplementedError

    @param_register(ck.pc_unplace_points)
    @staticmethod
    def unplace_points(param: Parameter) -> Parameter:
        """Unplaces points wherever possible"""
        points = param.ghost.point_cells()
        new_param = param
        for cell in points:
            new_param = ParamCleaner.unplace_point(new_param, cell)
        return new_param

    # Internal Methods

    @staticmethod
    def fuse_valid_rows_or_cols(param: Parameter, direction: int) -> Parameter:
        """fully fuses rows or cols of the parameter if they are fusable and map to the same index.
        direction = 0 for cols, directions = 1 for rows"""
        new_ghost = param.ghost
        new_maps = [param.col_map, param.row_map]
        old_idx, new_idx, extend = 0, 0, 1
        while old_idx + extend < param.dimensions[direction]:
            if new_maps[direction][old_idx] == new_maps[direction][old_idx + extend]:
                if new_ghost.is_fusable(direction, new_idx):
                    if direction == 0:
                        new_ghost = new_ghost.delete_columns([new_idx])
                    else:
                        new_ghost = new_ghost.delete_rows([new_idx])
                    del new_maps[direction][old_idx + extend]
                    extend += 1
                    continue
            old_idx += extend
            new_idx += 1
            extend = 1
        new_direction_map = {
            idx: new_maps[direction][value]
            for idx, value in enumerate(new_maps[direction].keys())
        }
        new_maps[direction] = new_direction_map
        return Parameter(new_ghost, RowColMap(*new_maps))

    @staticmethod
    def unplace_point(param: Parameter, cell: Cell) -> Parameter:
        """Tries to unplace a point in cell"""
        preimage_map = param.map.preimage_map()
        if (
            not cell[0] - 1 in preimage_map[param.col_map[cell[0]]]
            or cell[0] + 1 in preimage_map[0][param.col_map[cell[0]]]
        ):
            return param
        if (
            not cell[1] - 1 in preimage_map[param.row_map[cell[1]]]
            or cell[1] + 1 in preimage_map[1][param.row_map[cell[1]]]
        ):
            return param
        if (
            0 in cell
            or param.dimensions[0] == cell[0]
            or param.dimensions[1] == cell[1]
        ):
            return param
        intersecting_list = ParamCleaner.find_unplaced_req_list(param, cell)
        if not intersecting_list:
            return param
        new_reqs = tuple(
            req_list for req_list in param.requirements if req_list != intersecting_list
        )
        new_ghost = Tiling(param.obstructions, new_reqs, param.dimensions)
        new_ghost = new_ghost.delete_columns((cell[0],))
        if not new_ghost.is_fusable(0, cell[0]):
            return param
        new_ghost = new_ghost.delete_rows((cell[1],))
        if not new_ghost.is_fusable(1, cell[1]):
            return param
        raise NotImplementedError

    @staticmethod
    def find_unplaced_req_list(
        param: Parameter, cell: Cell
    ) -> Iterable[GriddedCayleyPerm]:
        """Identifies a valid req list that can be merged with the point to be unplaced"""
        check_cells = set(
            product((cell[0] - 1, cell[0] + 1), (cell[1] - 1, cell[1], cell[1] + 1))
        )
        list_found: tuple = tuple()
        for req_list in param.requirements:
            reqs_intersect = (
                bool(set(req.positions).intersection(check_cells)) for req in req_list
            )
            if any(reqs_intersect):
                if all(reqs_intersect):
                    if not list_found:
                        list_found = req_list
                        continue
                    return tuple()
                return tuple()
        if not list_found:
            return (GriddedCayleyPerm(CayleyPermutation((0,)), (cell,)),)
        return list_found
