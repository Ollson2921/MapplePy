"""Algorithms and functions for uncbalanced fusion"""

from typing import Iterator, Iterable
from gridded_cayley_permutations import Tiling, RowColMap
from mapplings import Parameter


class UnbalancedFusion:
    """A class for the Unbalanced Fusion Algorithm"""

    def __init__(self, param: Parameter):
        self.sorted_obs = param.obs_by_col_and_row()
        self.sorted_reqs = param.reqs_by_col_and_row()
        self.default_maps = dict(enumerate(range(param.dimensions[0]))), dict(
            enumerate(range(param.dimensions[1]))
        )
        self.param_maps = param.col_map, param.row_map
        self.param = param

    @staticmethod
    def auto_fuse(param: Parameter, fuse_rows: bool) -> Parameter:
        """Fuses rows or cols in both directions"""
        if param.dimensions[fuse_rows] <= 1:
            return param
        new_fuse = UnbalancedFusion(param)
        indices = tuple(new_fuse.fusable_indices(fuse_rows, True))
        temp = new_fuse.fuse(indices, fuse_rows, True)
        new_fuse = UnbalancedFusion(temp)
        indices = tuple(new_fuse.fusable_indices(fuse_rows, False))
        return new_fuse.fuse(indices, fuse_rows, False)

    def fuse(
        self, indices: Iterable[int], fuse_rows: bool, positive_direction: bool
    ) -> Parameter:
        """Returns the fusion resulting from removing the rows/cols in indices"""
        if not indices:
            return self.param
        if fuse_rows:
            adjust_map = self.make_adjustment_map([], indices, not positive_direction)
        else:
            adjust_map = self.make_adjustment_map(indices, [], not positive_direction)
        mgcps = tuple(self.param.minimal_gridded_cperms())
        new_reqs = adjust_map.map_requirements((mgcps,))
        temp_param = Parameter(
            Tiling(self.param.obstructions, new_reqs, self.param.dimensions),
            self.param.map,
        )
        if fuse_rows:
            return temp_param.delete_rows_and_columns([], indices)
        return temp_param.delete_rows_and_columns(indices, [])

    def fusable_indices(
        self, fuse_rows: bool, positive_direction: bool
    ) -> Iterator[int]:
        """Returns all indices to be deleted in fusion"""
        max_index = max(self.param_maps[fuse_rows].keys())
        index = (max_index, 0)[positive_direction]
        merge_direction = (-1, 1)[positive_direction]
        while 0 <= index + merge_direction <= max_index:
            if (
                self.param_maps[fuse_rows][index]
                != self.param_maps[fuse_rows][index + merge_direction]
            ):
                index += merge_direction
                continue
            if self.check_obs(index, fuse_rows, merge_direction) and self.check_reqs(
                index, fuse_rows, merge_direction
            ):
                yield index + merge_direction
            index += merge_direction

    def check_obs(self, index: int, fuse_rows: bool, merge_direction: int) -> bool:
        """Makes sure all obs at index are implied when fusing"""
        temp_maps = list(self.default_maps)
        temp_maps[fuse_rows][index + merge_direction] = index
        new_obs = (
            set(
                RowColMap(*temp_maps).preimage_of_obstructions(
                    self.sorted_obs[fuse_rows][index]
                )
            )
            - self.sorted_obs[fuse_rows][index]
        )
        if any(
            ob.avoids(self.sorted_obs[fuse_rows][index + merge_direction])
            for ob in new_obs
        ):
            return False
        return True

    def check_reqs(self, index: int, fuse_rows: bool, merge_direction: int) -> bool:
        """Validates the requirements"""
        temp_maps = list(self.default_maps)
        temp_maps[fuse_rows][index] = index + merge_direction
        preimage_map = RowColMap(*temp_maps)
        obs = self.sorted_obs[fuse_rows][index + merge_direction]
        isolated_obs = {
            ob: set(preimage_map.preimage_of_gridded_cperm(ob))
            for ob in obs
            if all(pos[fuse_rows] == index + merge_direction for pos in ob.positions)
        }
        combined_obs = obs | self.sorted_obs[fuse_rows][index]
        for req_list in self.sorted_reqs[fuse_rows][index + merge_direction]:
            for req in req_list:
                relevant_positions = set(pos[fuse_rows] for pos in req.positions)
                if relevant_positions != {index + merge_direction}:
                    return False
                subreq = req.sub_gridded_cayley_perm(
                    (
                        pos
                        for pos in req.positions
                        if pos[fuse_rows] == index + merge_direction
                    )
                )
                for ob in isolated_obs.keys():
                    if ob.avoids((subreq,)):
                        if not all(
                            pre_ob in combined_obs
                            for pre_ob in isolated_obs[ob]
                        ):
                            return False
                
        return True

    def make_adjustment_map(
        self,
        deleted_cols: Iterable[int],
        deleted_rows: Iterable[int],
        reverse_direction: bool = False,
    ) -> RowColMap:
        """Makes a map from original param to that param after cols and rows are deleted"""
        dimensions = self.param.dimensions
        col_correction, row_correction = dict[int, int](), dict[int, int]()
        adjust = 0
        direction = (1, -1)[reverse_direction]
        indices = tuple(range(dimensions[0]))
        if reverse_direction:
            indices = tuple(reversed(indices))
        for i in indices:
            if i in deleted_cols:
                col_correction[i] = col_correction[i - direction]
                adjust += direction
            else:
                col_correction[i] = i - adjust * direction
        adjust = 0
        indices = tuple(range(dimensions[1]))
        if reverse_direction:
            indices = tuple(reversed(indices))
        for i in indices:
            if i in deleted_rows:
                row_correction[i] = row_correction[i - direction]
                adjust += direction
            else:
                row_correction[i] = i - adjust * direction
        return RowColMap(col_correction, row_correction)
