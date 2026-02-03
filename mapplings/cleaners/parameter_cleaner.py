"""Module with the parameter cleaner"""

from typing import Iterator
from itertools import chain
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

        blank = tuple(map(set[int], param.blank_and_near_blank()))
        if not any(blank):
            return param

        col_preimages, row_preimages = param.map.preimage_map()

        try:
            splits = tuple(map(set[int], zip(*param.requirement_cells())))
        except ValueError:
            splits = set[int](), set[int]()

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
            old_idx += extend
            new_idx += 1
            extend = 1
        new_direction_map = {
            idx: new_maps[fuse_rows][value]
            for idx, value in enumerate(new_maps[fuse_rows].keys())
        }
        new_maps[fuse_rows] = new_direction_map
        return Parameter(new_ghost, RowColMap(*new_maps))
