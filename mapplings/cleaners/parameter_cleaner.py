"""Module with the parameter cleaner"""

from typing import Iterator, Iterable
from itertools import chain
from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations.row_col_map import RowColMap
from gridded_cayley_permutations.unplacement import PartialUnplacement
from gridded_cayley_permutations import Tiling
from mapplings import Parameter

from .cleaner import GenericCleaner, Register, CleanerLog


class ParamCleaner(GenericCleaner[Parameter]):
    """The cleaner for parameters.
    core functions need to be registered with @reg(index)
    where index determines cleaning order"""

    DEBUG = 0
    reg = Register[Parameter](
        run_on_avoiders=True,
        run_on_containers=True,
        run_on_enumerators=True,
    )
    global_tracker = CleanerLog[Parameter](
        reg.registered_functions, name="Global Tracker"
    )

    all_loggers = {global_tracker}

    # Final Methods

    @staticmethod
    @reg(4, run_on_enumerators=False)
    def reduce_by_fusion(param: Parameter) -> Parameter:
        """Fuses valid rows and columns"""
        deleted_cols, deleted_rows = set(
            ParamCleaner._find_indixes_to_fuse(param, False)
        ), set(ParamCleaner._find_indixes_to_fuse(param, True))
        temp = Parameter(
            Tiling(param.obstructions, [], param.dimensions, False), param.map
        ).delete_rows_and_columns(deleted_cols, deleted_rows)
        if not param.requirements:
            return temp
        new_ghost = Tiling(
            temp.obstructions,
            [
                ParamCleaner._make_adjustment_map(
                    param, deleted_cols, deleted_rows
                ).map_gridded_cperms(param.minimal_gridded_cperms())
            ],
            temp.dimensions,
        )
        return Parameter(new_ghost, temp.map)

    @staticmethod
    @reg(0)
    def reduce_empty_rows_and_cols(param: Parameter) -> Parameter:
        """Removes empty rows and columns in the parameter"""
        empty_cols, empty_rows = map(set, param.find_empty_rows_and_columns())
        cols_to_remove, rows_to_remove = set(), set()
        col_preimages, row_preimages = param.map.preimage_map()
        for key in col_preimages.keys():
            intersection = set(col_preimages[key]) & empty_cols
            if len(intersection) == len(col_preimages[key]):
                intersection.remove(col_preimages[key][0])
            cols_to_remove.update(intersection)
        for key in row_preimages.keys():
            intersection = set(row_preimages[key]) & empty_rows
            if len(intersection) == len(row_preimages[key]):
                intersection.remove(row_preimages[key][0])
            rows_to_remove.update(intersection)
        return param.delete_rows_and_columns(cols_to_remove, rows_to_remove)

    @staticmethod
    @reg(1, run_on_enumerators=False)
    def remove_blank_rows_and_cols(param: Parameter) -> Parameter:
        """Deletes all rows and cols which have no obs or reqs"""

        try:
            blank = tuple(map(set[int], param.find_blank_columns_and_rows()))
        except ValueError:
            return param
        col_preimages, row_preimages = param.map.preimage_map()
        try:
            splits = param.requirement_columns_and_rows()
        except ValueError:
            splits = (set[int](), set[int]())

        def to_remove(
            preimages: dict[int, tuple[int, ...]], find_rows: bool
        ) -> Iterator[set[int]]:
            for preimage in sorted(preimages.values()):
                if not set(preimage) & blank[find_rows]:
                    continue
                if not splits[find_rows]:
                    yield set(preimage)
                    continue
                slice_start = 0
                for i, check in enumerate(preimage):
                    if check in splits[find_rows]:
                        section = set(preimage[slice_start:i])
                        slice_start = i + 1
                        try:
                            yield section - {tuple(section & blank[find_rows])[0]}
                        except IndexError:
                            pass
                if slice_start == 0:
                    yield set(preimage)

        cols_to_remove = set(chain(*to_remove(col_preimages, False)))
        rows_to_remove = set(chain(*to_remove(row_preimages, True)))
        if (
            len(cols_to_remove) == param.dimensions[0]
            or len(rows_to_remove) == param.dimensions[1]
        ):
            return Parameter(Tiling([], [], (0, 0)), RowColMap({}, {}))
        return param.delete_rows_and_columns(cols_to_remove, rows_to_remove)

    @staticmethod
    @reg(3, run_on_enumerators=False)
    def unplace_points(param: Parameter) -> Parameter:
        """Unplaces all possible points in the parameter"""
        algo = PartialUnplacement(param.ghost)
        points = param.single_value_cells()
        cells, cols, rows = set[tuple[int, int]](), set[int](), set[int]()
        for cell in points:
            valid = algo.cell_in_valid_region(cell)
            if valid[0] and param.col_map[cell[0] - 1] == param.col_map[cell[0] + 1]:
                cells.add(cell)
                cols.add(cell[0])
            if valid[1] and param.row_map[cell[1] - 1] == param.row_map[cell[1] + 1]:
                cells.add(cell)
                rows.add(cell[1])
        unplace_cols, unplace_rows = algo.fusable_check(cells, cols, rows)
        if not (unplace_cols or unplace_rows):
            return param
        new_ghost = algo.unplace(unplace_cols, unplace_rows)
        col_preimages, row_preimages = algo.adjustment_map(
            unplace_cols, unplace_rows
        ).preimage_map()
        new_col_map = {
            i: param.col_map[col_preimages[i][0]]
            for i in range(new_ghost.dimensions[0])
        }
        new_row_map = {
            i: param.row_map[row_preimages[i][0]]
            for i in range(new_ghost.dimensions[1])
        }
        return Parameter(new_ghost, RowColMap(new_col_map, new_row_map))

    @staticmethod
    @reg(2, run_on_enumerators=False)
    def insert_blank(param: Parameter) -> Parameter:
        """Inserts a blank col/row in between descents/ascents wherever possible"""
        if not param.requirements:
            return param
        to_insert = [set[int](), set[int]()]
        maps = param.col_map, param.row_map
        blank = tuple(map(set[int], param.find_blank_columns_and_rows()))
        point_indices = param.point_cols, param.point_rows

        def validate_two_cells(index1: int, index2: int, check_rows: bool) -> bool:
            """Returns True if two adjacent cells are in point rows/cols with a
            blank row/col adjacent to them mapping to the same place."""
            indices = {index1, index2}
            mapping_to = maps[check_rows][index1]
            if mapping_to != maps[check_rows][index2] or not indices.issubset(
                point_indices[check_rows]
            ):
                return False
            if (
                index1 - 1 in blank[check_rows]
                and mapping_to == maps[check_rows][index1 - 1]
            ):
                return True
            if (
                index2 + 1 in blank[check_rows]
                and mapping_to == maps[check_rows][index2 + 1]
            ):
                return True
            return False

        def validate_one_cell(index: int, check_rows: bool) -> bool:
            """Returns True if a cell is in a point row/col
            with a blank row/col adjacent to it mapping to the
            same place."""
            if index not in point_indices[check_rows]:
                return False
            mapping_to = maps[check_rows][index]
            if (
                index - 1 in blank[check_rows]
                and mapping_to == maps[check_rows][index - 1]
            ):
                return True
            if (
                index + 1 in blank[check_rows]
                and mapping_to == maps[check_rows][index + 1]
            ):
                return True
            return False

        for req_list in param.requirements:
            if not len(req_list) == 1:
                continue
            req = req_list[0]
            if req.pattern == CayleyPermutation((0,)):
                cell = req.positions[0]
                if validate_one_cell(cell[0], False):
                    to_insert[0].add(cell[0])
                    continue
                if validate_one_cell(cell[1], True):
                    to_insert[1].add(cell[1])
                    continue
                continue

            if req.pattern not in (
                CayleyPermutation((0, 1)),
                CayleyPermutation((1, 0)),
            ):
                continue
            cell1, cell2 = req.positions
            if (cell1[0] != cell2[0]) and (cell1[1] != cell2[1]):
                continue
            if cell1[0] + 1 == cell2[0]:
                if validate_two_cells(cell1[0], cell2[0], False):
                    to_insert[0].add(cell1[0])
                    continue
            idx1, idx2 = sorted([cell1[1], cell2[1]])
            if idx1 + 1 == idx2:
                if validate_two_cells(idx1, idx2, True):
                    to_insert[1].add(idx1)
        if not any(to_insert):
            return param

        return param.insert_cols_and_rows(*to_insert)

    # Internal Methods

    @staticmethod
    def _find_indixes_to_fuse(param: Parameter, fuse_rows: bool) -> Iterator[int]:
        """Yields all indices that can be fused"""
        maps = param.col_map, param.row_map
        temp = Parameter(
            Tiling(param.obstructions, [], param.dimensions, False), param.map
        )
        for i in range(param.dimensions[fuse_rows] - 1):
            if maps[fuse_rows][i] == maps[fuse_rows][i + 1]:
                if temp.is_fusable(fuse_rows, i):
                    yield i + 1

    @staticmethod
    def _make_adjustment_map(
        original_param: Parameter,
        deleted_cols: Iterable[int],
        deleted_rows: Iterable[int],
    ) -> RowColMap:
        """Makes a map from original param to that param after cols and rows are deleted"""
        col_correction, row_correction = dict[int, int](), dict[int, int]()
        adjust = 0
        for i in range(original_param.dimensions[0]):
            if i in deleted_cols:
                col_correction[i] = col_correction[i - 1]
                adjust += 1
            else:
                col_correction[i] = i - adjust
        adjust = 0
        for i in range(original_param.dimensions[1]):
            if i in deleted_rows:
                row_correction[i] = row_correction[i - 1]
                adjust += 1
            else:
                row_correction[i] = i - adjust
        return RowColMap(col_correction, row_correction)
