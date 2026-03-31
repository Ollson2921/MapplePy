"""Algorithms and functions for uncbalanced fusion"""

from typing import Iterator, Iterable
from itertools import chain
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
            adjust_map = RowColMap.make_adjustment_map(
                RowColMap(*self.param_maps), [], indices, not positive_direction
            )
        else:
            adjust_map = RowColMap.make_adjustment_map(
                RowColMap(*self.param_maps), indices, [], not positive_direction
            )
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
                print("yay")
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
        """Makes sure requirements live entirely in one of the rows/cols we're trying to fuse"""
        new_reqs = chain.from_iterable(
            self.sorted_reqs[fuse_rows][index]
            | self.sorted_reqs[fuse_rows][index + merge_direction]
        )
        for req in new_reqs:
            relevant_positions = list(map(set[int], zip(*req.positions)))[fuse_rows]
            if relevant_positions != {index} and (
                relevant_positions
                != {index + merge_direction}
                # or len(self.param.map.image_rows_and_cols()[not fuse_rows]) > 1
            ):
                return False
        return True
