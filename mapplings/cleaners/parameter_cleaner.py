"""Module with the parameter cleaner"""

from typing import Iterable
from gridded_cayley_permutations.row_col_map import RowColMap
from gridded_cayley_permutations.unplacement import PointUnplacement
from gridded_cayley_permutations import Tiling
from mapplings import Parameter

from .cleaner import GenericCleaner, Register


class ParamCleaner(GenericCleaner[Parameter]):
    """The cleaner for parameters.
    core functions need to be registered with @reg(index)
    where index determines cleaning order"""

    DEBUG = 0
    reg = Register[Parameter](
        "param_register",
        run_on_avoiders=True,
        run_on_containers=True,
        run_on_enumerators=True,
    )
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
    @reg(2, run_on_enumerators=False)
    def unplace_points(param: Parameter) -> Parameter:
        """Unplaces all possible points in the parameter"""
        found = True
        new_param = Parameter(param.ghost, param.map)
        while found:
            found = False
            for cell in new_param.point_cells():
                algo = PointUnplacement(new_param.ghost, cell)
                if not algo.cell_in_valid_region():
                    continue
                if (
                    not new_param.col_map[cell[0] - 1]
                    == new_param.col_map[cell[0]]
                    == new_param.col_map[cell[0] + 1]
                ):
                    continue
                if (
                    not new_param.row_map[cell[1] - 1]
                    == new_param.row_map[cell[1]]
                    == new_param.row_map[cell[1] + 1]
                ):
                    continue
                check_reqs = algo.intersecting_req_list()
                if PointUnplacement(new_param.ghost, cell).point_can_be_unplaced(
                    check_reqs
                ):
                    new_param = new_param.unplace_point(cell)
                    found = True
                    break
        return new_param

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
