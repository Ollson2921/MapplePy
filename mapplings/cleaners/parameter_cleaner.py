"""Module with the parameter cleaner"""

from typing import Iterable
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
    @reg(3, run_on_enumerators=False)
    def reduce_by_fusion(param: Parameter) -> Parameter:
        """Fuses valid rows and columns"""
        return ParamCleaner._fuse_valid_rows_or_cols(
            ParamCleaner._fuse_valid_rows_or_cols(param, True), False
        )

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

        columns, rows = param.find_blank_columns_and_rows()
        cols_to_remove, rows_to_remove = set(), set()
        if param.positive_cells():
            positive_cols, positive_rows = map(set, zip(*param.positive_cells()))
        else:
            positive_cols, positive_rows = set(), set()

        def check_for_blank(columns: Iterable[int], image: int, check_rows: bool):
            for col in columns:
                if check_rows:
                    if col in rows_to_remove:
                        break
                    if param.row_map[col] == image and col not in positive_rows:
                        rows_to_remove.add(col)
                    else:
                        break
                else:
                    if col in cols_to_remove:
                        break
                    if param.col_map[col] == image and col not in positive_cols:
                        cols_to_remove.add(column)
                    else:
                        break

        for column in columns:
            image_col = param.map.col_map[column]
            cols_to_remove.add(column)
            check_for_blank(range(column - 1, -1, -1), image_col, False)
            check_for_blank(range(column + 1, param.dimensions[0]), image_col, False)
        for blank_row in rows:
            image_row = param.row_map[blank_row]
            rows_to_remove.add(blank_row)
            check_for_blank(range(blank_row - 1, -1, -1), image_row, True)
            check_for_blank(range(blank_row + 1, param.dimensions[1]), image_row, True)
        if (
            len(cols_to_remove) == param.dimensions[0]
            or len(rows_to_remove) == param.dimensions[1]
        ):
            return Parameter(Tiling([], [], (1, 1)), RowColMap({0: 0}, {0: 0}))

        if param.point_cells():
            cols_with_point, rows_with_point = map(set, zip(*param.point_cells()))
            temp_cols, temp_rows = set(), set()
            for col in cols_to_remove:
                if col - 1 in cols_with_point:
                    if col + 1 in cols_to_remove:
                        temp_cols.add(col + 1)
                else:
                    temp_cols.add(col)
            cols_to_remove = set()
            for col in temp_cols:
                if col + 1 in cols_with_point:
                    if col - 1 in temp_cols:
                        cols_to_remove.add(col - 1)
                else:
                    cols_to_remove.add(col)
            for row in rows_to_remove:
                if row - 1 in rows_with_point:
                    if row + 1 in rows_to_remove:
                        temp_rows.add(row + 1)
                else:
                    temp_rows.add(row)
            rows_to_remove = set()
            for row in temp_rows:
                if row + 1 in rows_with_point:
                    if row - 1 in temp_rows:
                        rows_to_remove.add(row - 1)
                else:
                    rows_to_remove.add(row)
        return param.delete_rows_and_columns(cols_to_remove, rows_to_remove)

    @staticmethod
    @reg(2, run_on_enumerators=False)
    def unplace_points(param: Parameter) -> Parameter:
        """Unplaces all possible points in the parameter"""
        algo = PartialUnplacement(param.ghost)
        points = param.point_cells()
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

    # Internal Methods

    @staticmethod
    def _fuse_valid_rows_or_cols(param: Parameter, fuse_rows: bool) -> Parameter:
        """fully fuses rows or cols of the parameter if they are fusable and map to the same index.
        direction = 0 for cols, directions = 1 for rows"""
        new_ghost = param.ghost
        new_maps = [param.col_map, param.row_map]
        old_idx, new_idx, extend = 0, 0, 1
        while old_idx + extend < param.dimensions[fuse_rows]:
            if new_maps[fuse_rows][old_idx] == new_maps[fuse_rows][old_idx + extend]:
                if new_ghost.is_fusable(fuse_rows, new_idx):
                    if fuse_rows:
                        new_ghost = new_ghost.delete_rows([new_idx])
                    else:
                        new_ghost = new_ghost.delete_columns([new_idx])
                    del new_maps[fuse_rows][old_idx + extend]
                    extend += 1
                    continue
            old_idx += extend
            new_idx += 1
            extend = 1
        new_direction_map = {
            idx: new_maps[fuse_rows][value]
            for idx, value in enumerate(new_maps[fuse_rows].keys())
        }
        new_maps[fuse_rows] = new_direction_map
        return Parameter(new_ghost, RowColMap(*new_maps))
