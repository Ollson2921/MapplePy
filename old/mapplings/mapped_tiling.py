from typing import Iterable, Iterator, Tuple, List, Dict, DefaultDict
from itertools import chain
from collections import defaultdict
from comb_spec_searcher import CombinatorialClass


from cayley_permutations import CayleyPermutation
from gridded_cayley_permutations import (
    GriddedCayleyPerm,
    Tiling,
)
from gridded_cayley_permutations.row_col_map import RowColMap

Objects = DefaultDict[Tuple[int, ...], List[GriddedCayleyPerm]]

REDUNDANCE_TOLERANCE = (
    0  # Higher values globally increase sizes of GCPS used in redundancy checks
)


class Parameter:
    def __init__(self, ghost: Tiling, row_col_map: RowColMap):
        """we may need to keep track of which direction the row_col_map goes"""
        self.map = row_col_map
        self.ghost = ghost

    def cleanup(self):  # cleaner
        cols_to_remove, rows_to_remove = self.empty_rows_and_columns_to_delete(
            self.ghost, self.map
        )
        new_map = self.reduce_row_col_map(cols_to_remove, rows_to_remove)
        new_ghost = self.ghost.delete_rows_and_columns(cols_to_remove, rows_to_remove)
        return Parameter(new_ghost, new_map)

    def empty_rows_and_columns_to_delete(
        self, ghost: Tiling, row_col_map: RowColMap
    ):  # cleaner
        """Delete empty rows and columns in parameters if not
        only row/col mapping to a row/col in the base tiling.
        Only delete rows/cols if they map to something that another
        row/col in the parameter maps to."""
        empty_cols, empty_rows = ghost.find_empty_rows_and_columns()
        col_values = [row_col_map.col_map[col] for col in range(ghost.dimensions[0])]
        cols_to_remove = []
        for col in empty_cols:
            if col_values.count(row_col_map.col_map[col]) > 1:
                col_values.remove(row_col_map.col_map[col])
                cols_to_remove.append(col)
        row_values = [row_col_map.row_map[row] for row in range(ghost.dimensions[1])]
        rows_to_remove = []
        for row in empty_rows:
            if row_values.count(row_col_map.row_map[row]) > 1:
                row_values.remove(row_col_map.row_map[row])
                rows_to_remove.append(row)
        return cols_to_remove, rows_to_remove

    def is_contradictory(self, tiling: Tiling) -> bool:  # cleaner
        """Returns True if the parameter is contradictory.
        Is contradictory if any of the requirements in the ghost map to a gcp
        containing an obstruction in the tiling
        """
        for req_list in self.ghost.requirements:
            if all(
                self.map.map_gridded_cperm(gcp).contains(tiling.obstructions)
                for gcp in req_list
            ):
                return True
        return False

    def preimage_of_gcp(
        self, gcp: GriddedCayleyPerm
    ) -> Iterator[GriddedCayleyPerm]:  # main
        """Returns the preimage of a gridded cayley permutation"""
        for gcp in self.map.preimage_of_gridded_cperm(gcp):
            if self.ghost.gcp_in_tiling(gcp):
                yield gcp

    def reduce_row_col_map(self, col_preimages, row_preimages):  # cleaner
        """This function removes rows and collumns from the map and standardizes the output"""
        new_col_map, new_row_map = self.map.col_map.copy(), self.map.row_map.copy()
        for index in col_preimages:
            del new_col_map[index]
        for index in row_preimages:
            del new_row_map[index]
        return RowColMap(new_col_map, new_row_map).standardise_map()

    def back_map_obs_and_reqs(self, tiling: Tiling, simplify=True) -> "Parameter":
        """Places all obs and reqs of tiling into the parameter according to the row/col map.
        Returns a new parameter, but maybe we should just add obs and reqs to existing parameters, IDK
        Doing this for req lists is weird...
        """
        new_obs = self.ghost.obstructions + self.map.preimage_of_obstructions(
            tiling.obstructions
        )
        new_reqs = self.ghost.requirements + self.map.preimage_of_requirements(
            tiling.requirements
        )
        return Parameter(
            Tiling(new_obs, new_reqs, self.ghost.dimensions, simplify), self.map
        )

    def back_map_point_obstructions(self, tiling: Tiling, simplify=True) -> "Parameter":
        """Places all obs and reqs of tiling into the parameter according to the row/col map.
        Returns a new parameter, but maybe we should just add obs and reqs to existing parameters, IDK
        Doing this for req lists is weird...
        """
        new_obs = self.ghost.obstructions + self.map.preimage_of_obstructions(
            [ob for ob in tiling.obstructions if len(ob) == 1]
        )
        return Parameter(
            Tiling(new_obs, self.ghost.requirements, self.ghost.dimensions, simplify),
            self.map,
        )

    def sub_parameter(self, factor):  # main
        """For a given factor of cells in the tiling, finds the preimage of these cells in
        the parameter and returns a new parameter with a subghost but the same map."""
        preimage_of_cells = self.map.preimage_of_cells(factor)
        return Parameter(self.ghost.sub_tiling(preimage_of_cells), self.map)

    def reduce_by_fusion(self):
        """Fuses valid rows and columns"""
        rows_to_delete = tuple(
            row
            for row in range(self.ghost.dimensions[1] - 1)
            if (
                self.map.row_map[row] == self.map.row_map[row + 1]
                and self.ghost.can_fuse_row(row)
            )
        )
        cols_to_delete = tuple(
            col
            for col in range(self.ghost.dimensions[0] - 1)
            if (
                self.map.col_map[col] == self.map.col_map[col + 1]
                and self.ghost.can_fuse_col(col)
            )
        )
        return self.delete_rows_and_columns(cols_to_delete, rows_to_delete)

    def delete_rows_and_columns(
        self, cols_to_delete: tuple[int, ...], rows_to_delete: tuple[int, ...]
    ) -> "Parameter":
        """Removes rows and columns from the parameter"""
        new_map = self.reduce_row_col_map(cols_to_delete, rows_to_delete)
        new_ghost = self.ghost.delete_rows_and_columns(cols_to_delete, rows_to_delete)
        return Parameter(new_ghost, new_map)

    def _reduce_empty_rows_or_cols(
        self,
        rows: bool,
        preimages: dict[int, list[int, ...]],
        currently_empty: set[int],
    ) -> "Parameter":
        """
        Removes empty rows or columns if they share an image with another row or column.

        Preimages is a dictionary with the tiling index pointing to a list of its preimages
        """
        new_maps = (self.map.col_map, self.map.row_map)
        to_remove = []
        for row, preimage_row in preimages.items():
            if len(preimage_row) == 1:
                continue
            for idx in preimage_row:
                if idx in currently_empty:
                    to_remove.append(idx)
                    new_maps[rows].pop(idx)
        empty_rows, empty_cols = tuple(), tuple()
        if rows:
            empty_rows = tuple(to_remove)
        else:
            empty_cols = tuple(to_remove)
        new_ghost = self.ghost.delete_rows_and_columns(empty_cols, empty_rows)
        return Parameter(new_ghost, RowColMap(*new_maps).standardise_map())

    def reduce_empty_rows_and_cols(self):
        """Removes empty rows and columns in the parameter"""
        col_preimages = {
            i: self.map.preimages_of_col(i) for i in set(self.map.col_map.values())
        }
        row_preimages = {
            i: self.map.preimages_of_row(i) for i in set(self.map.row_map.values())
        }
        currently_empty = self.ghost.find_empty_rows_and_columns()
        return self._reduce_empty_rows_or_cols(
            0, col_preimages, currently_empty[0]
        )._reduce_empty_rows_or_cols(1, row_preimages, currently_empty[1])

    def split_and_squish_in_range(self, min_index, max_index, direction):
        """Used in expand together. splits each row/column in the range of min_index, max_index.
        each way the parameter is split contributes to a final parameter made by backmapping obs and reqs without simplifying
        """
        maps = [
            {i: i for i in range(self.ghost.dimensions[0])},
            {i: i for i in range(self.ghost.dimensions[1])},
        ]
        new_parameter = Parameter(
            Tiling(
                [],
                [],
                (
                    self.ghost.dimensions[0] + int(direction == 0),
                    self.ghost.dimensions[1] + int(direction == 1),
                ),
            ),
            self.map,
        )
        for i in range(min_index, max_index + 1):
            maps[direction] = {
                k: k - int(k > i) for k in range(self.ghost.dimensions[direction] + 1)
            }
            new_parameter = Parameter(
                new_parameter.ghost, RowColMap(*tuple(maps))
            ).back_map_obs_and_reqs(self.ghost, simplify=True)
        original_maps = [self.map.col_map, self.map.row_map]
        original_maps[direction] = {
            k: original_maps[direction][k - int(k > max_index)]
            for k in range(self.ghost.dimensions[direction] + 1)
        }
        return Parameter(new_parameter.ghost, RowColMap(*tuple(original_maps)))

    def expand_together(self, other):
        """Transforms self and other into parameters with the same dimension while respecting the row col map.
        The returned parameters are not simplified."""
        parameters = [self, other]
        for direction in (0, 1):
            preimage_maps = (
                self.map.preimage_map()[direction],
                other.map.preimage_map()[direction],
            )
            for i in preimage_maps[0].keys():
                preimage_maps = (
                    parameters[0].map.preimage_map()[direction],
                    parameters[1].map.preimage_map()[direction],
                )
                difference = len(preimage_maps[0][i]) - len(preimage_maps[1][i])
                choice = int(difference > 0)
                min_index, max_index = min(preimage_maps[choice][i]), max(
                    preimage_maps[choice][i]
                )
                k = 0
                while k < abs(difference):
                    parameters[choice] = parameters[choice].split_and_squish_in_range(
                        min_index, max_index + k, direction
                    )
                    k += 1
        return parameters[0], parameters[1]

    @staticmethod
    def make_comparisons(parameters, base_dimensions, tolerance):
        """Creates a comparisons dictionary from a list of parameters.
        comparisons[a] is the set of indices b such that the objects from a mappling with parameters[a] as an avoider are a subset of the objects with parameters[b] as an avoider.
        The size of objects created is the maximum size of the upper bound of mimimal GCPS across all paramters plus the tolerance
        """
        if len(parameters) <= 1:
            return {0: {}}
        base_size = tolerance + max(
            [
                param.ghost.maximum_length_of_minimal_gridded_cayley_perm()
                for param in parameters
            ]
        )
        base_tiling = Tiling([], [], base_dimensions)
        objects = []
        for param in parameters:
            objects.append(
                set(
                    MappedTiling(base_tiling, [param], [], []).objects_of_size(
                        base_size
                    )
                )
            )
        comparisons = {i: set() for i in range(len(parameters))}
        for i in range(len(parameters) - 1):
            for j in range(i + 1, len(parameters)):
                if objects[i].issubset(objects[j]):
                    comparisons[i].add(j)
                    continue
                if objects[j].issubset(objects[i]):
                    comparisons[j].add(i)
                    continue
        return comparisons

    def copy(self):
        return Parameter(self.ghost, self.map)

    def __repr__(self):
        return self.__class__.__name__ + f"({repr(self.ghost)}, {repr(self.map)})"

    def __eq__(self, other) -> bool:
        return self.ghost == other.ghost and self.map == other.map

    def __hash__(self):
        return hash((self.ghost, self.map))

    def __leq__(self, other):
        return self.ghost <= other.ghost

    def __lt__(self, other):
        return self.ghost < other.ghost

    def reduced_str(self):
        """Returns a string representation of the parameter without the
        crossing obs and reqs."""
        return str(self.map) + "\n" + self.ghost.reduced_str()

    def __str__(self) -> str:
        return str(self.map) + "\n" + str(self.ghost)


class MappedTiling(CombinatorialClass):
    def __init__(
        self,
        tiling: Tiling,
        avoiding_parameters: Iterable[Parameter],
        containing_parameters: Iterable[Iterable[Parameter]],
        enumeration_parameters: Iterable[Iterable[Parameter]],
    ):
        self.avoiding_parameters = avoiding_parameters
        self.containing_parameters = containing_parameters
        self.enumeration_parameters = enumeration_parameters
        self.tiling = tiling
        # if self.is_empty():
        #     self.avoiding_parameters = []
        #     self.containing_parameters = [[]]
        #     self.enumeration_parameters = [[]]

    ## Combintatorial class stuff ##

    def is_atom(self):  # main
        return self.tiling.is_atom() and not self.all_parameters()

    def minimum_size_of_object(self) -> int:  # main
        assert not self.is_empty()
        i = 0
        while True:
            for _ in self.objects_of_size(i):
                return i
            i += 1

    def objects_of_size(self, n, **parameters):  # main
        for val in self.get_objects(n).values():
            for gcp in val:
                yield gcp

    def get_objects(self, n: int) -> Objects:  # Good
        objects = defaultdict(list)
        for gcp in self.tiling.objects_of_size(n):
            if self.gcp_in_tiling(gcp):
                param = self.get_parameters(gcp)
                objects[param].append(gcp)
        return objects

    def get_parameters(self, gcp: GriddedCayleyPerm) -> Tuple[int, ...]:  # Good
        """Parameters are not what you think!!! This is specific to combinatorical class parameters"""
        all_lists = []
        for param_list in self.enumeration_parameters:
            all_lists.append(
                sum(1 for _ in param.preimage_of_gcp(gcp)) for param in param_list
            )
        return tuple(all_lists)

    def gcp_in_tiling(self, gcp: GriddedCayleyPerm) -> bool:  # Good
        """Returns True if the gridded cayley permutation is in the tiling"""
        return self.gcp_satisfies_containing_params(
            gcp
        ) and self.gcp_satisfies_avoiding_params(gcp)

    def gcp_satisfies_avoiding_params(self, gcp: GriddedCayleyPerm) -> bool:  # Good
        """Returns True if the gridded cayley permutation satisfies the avoiding parameters"""
        return not any(
            any(True for _ in param.preimage_of_gcp(gcp))
            for param in self.avoiding_parameters
        )

    def gcp_satisfies_containing_params(self, gcp: GriddedCayleyPerm) -> bool:  # Good
        """Returns True if the gridded cayley permutation satisfies the containing parameters"""
        return all(
            any(any(True for _ in param.preimage_of_gcp(gcp)) for param in params)
            for params in self.containing_parameters
        )

    ## Tidying functions ##

    def full_cleanup(self):  # cleaner
        """Applies every cleanup function"""
        if not self.tiling.active_cells:
            return self.kill_to_empty_or_obstructed()
        new_mappling = self.tidy_containing_parameters()
        if not new_mappling.tiling.active_cells:
            return new_mappling.kill_to_empty_or_obstructed()
        new_mappling = new_mappling.insert_valid_avoiders().reap_all_contradictions()
        avoiding_parameters = [
            param.back_map_point_obstructions(new_mappling.tiling)
            for param in new_mappling.avoiding_parameters
        ]
        avoiding_parameters = new_mappling.remove_empty_ghosts_from_list(
            avoiding_parameters
        )
        new_mappling = MappedTiling(
            new_mappling.tiling,
            avoiding_parameters,
            new_mappling.containing_parameters,
            new_mappling.enumeration_parameters,
        )
        return (
            new_mappling.remove_empty_rows_and_columns()
            .reduce_empty_rows_and_cols_in_parameters()
            .fuse_parameters()
        )

    def kill_to_empty_or_obstructed(self):
        """Used to decide how to kill mapplings in full_cleanup"""
        if self.tiling.is_empty():
            return MappedTiling.empty_mappling()
        return MappedTiling(
            Tiling([GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),))]), [], [], []
        )

    def fuse_parameters(self):
        """Fuses valid rows and cols in every parameter"""
        avoiding_parameters, containing_parameters = [], []
        for avoider in self.avoiding_parameters:
            avoiding_parameters.append(avoider.reduce_by_fusion())
        for c_list in self.containing_parameters:
            containing_parameters.append(
                [container.reduce_by_fusion() for container in c_list]
            )
        return MappedTiling(
            self.tiling,
            avoiding_parameters,
            containing_parameters,
            self.enumeration_parameters,
        )

    def reduce_empty_rows_and_cols_in_parameters(self):  # cleaner
        """removes valid rows and cols in every parameter"""
        avoiding_parameters, containing_parameters, enumerating_parameters = [], [], []
        for avoider in self.avoiding_parameters:
            avoiding_parameters.append(avoider.reduce_empty_rows_and_cols())
        for c_list in self.containing_parameters:
            containing_parameters.append(
                [container.reduce_empty_rows_and_cols() for container in c_list]
            )
        for e_list in self.enumeration_parameters:
            enumerating_parameters.append(
                [enumerator.reduce_empty_rows_and_cols() for enumerator in e_list]
            )
        return MappedTiling(
            self.tiling,
            avoiding_parameters,
            containing_parameters,
            enumerating_parameters,
        )

    def insert_valid_avoiders(self):  # cleaner
        """Adds requirements from every avoider that is near-trivial and removes that avoider"""
        new_avoiders = []
        new_mappling = self.copy()
        for avoider in self.avoiding_parameters:
            placeable_req = new_mappling.avoider_can_be_placed(avoider)
            if placeable_req:
                new_mappling = new_mappling.add_obstructions_to_tiling(
                    [placeable_req[0]]
                )
            else:
                new_avoiders.append(avoider)
        return MappedTiling(
            new_mappling.tiling,
            new_avoiders,
            self.containing_parameters,
            self.enumeration_parameters,
        )

    def avoider_can_be_placed(self, avoider: Parameter):
        """returns the index of a requirement in the avoider that can be added to the tiling as an obstruction if it exists
        for now, this only happens if the avoider is trivial other than that single requirement
        """
        if self.tiling.dimensions != avoider.ghost.dimensions:
            return
        if set(self.tiling.obstructions) != set(avoider.ghost.obstructions):
            return
        temp_tiling_reqs = self.tiling.requirements
        placeable_req = None
        for req_list in avoider.ghost.requirements:
            try:
                temp_tiling_reqs.remove(req_list)
            except:
                if placeable_req:
                    return
                placeable_req = req_list
        if len(placeable_req) == 1:
            return placeable_req

    def remove_empty_ghosts_from_list(
        self, avoiding_parameters: List[Parameter]
    ) -> List[Parameter]:  # cleaner
        """Remove any parameters with empty tilings."""
        return [param for param in avoiding_parameters if not param.ghost.is_empty()]

    def back_maps_obs_and_reqs_for_param_list(
        self, tiling: Tiling, param_list: List[Parameter]
    ):  # param list cleaner
        """Map all obs and reqs in the tiling to the parameters in the parameter list"""
        return [param.back_map_obs_and_reqs(tiling) for param in param_list]

    def back_maps_point_obs_for_param_list(
        self, tiling: Tiling, param_list: List[Parameter]
    ):  # param list cleaner
        """Map all obs and reqs in the tiling to the parameters in the parameter list"""
        return [param.back_map_point_obstructions(tiling) for param in param_list]

    def tidy_containing_parameters(self):  # cleaner
        """For parameters with empty tilings, if it is the only
        one in a list then the mappling is empty, otherwise remove the empty
        parameter.
        If only one parameter in a list and it maps to base tiling by the identity map
        then map obs and reqs down and remove the parameter list.
        Note: As we always assume a parameter maps to the whole tiling, we defined a row
        col map as being trivial iff the dimensions of the tiling and ghost are the same.
        """
        new_containing_parameters = []
        new_tiling = self.tiling
        for param_list in self.containing_parameters:
            param_list = self.back_maps_point_obs_for_param_list(new_tiling, param_list)
            if len(param_list) == 0:
                return MappedTiling(Tiling.empty_tiling(), [], [], [])
            if len(param_list) == 1:
                if param_list[0].ghost.is_empty():
                    return MappedTiling(Tiling.empty_tiling(), [], [], [])
                if param_list[0].ghost.dimensions == self.tiling.dimensions:
                    new_tiling = param_list[0].back_map_obs_and_reqs(new_tiling).ghost
                else:
                    new_containing_parameters.append(param_list)
            else:
                new_containing_parameters.append(
                    self.remove_empty_ghosts_from_list(param_list)
                )
        return MappedTiling(
            new_tiling,
            self.avoiding_parameters,
            new_containing_parameters,
            self.enumeration_parameters,
        )

    def reap_contradictory_ghosts_from_list(
        self, parameter_list: list[Parameter]
    ):  # cleaner
        """Removes parameters which are contradictory from parameter list"""
        return [A for A in parameter_list if not A.is_contradictory(self.tiling)]

    def reap_all_contradictions(self):  # cleaner
        """Removes any contradictory ghosts from each ACE list.
        Also removes empty C or E lists"""
        new_avoiders = self.reap_contradictory_ghosts_from_list(
            self.avoiding_parameters
        )
        new_containers = [
            self.reap_contradictory_ghosts_from_list(c_list)
            for c_list in self.containing_parameters
        ]
        if any(not bool(c_list) for c_list in new_containers):
            return MappedTiling.empty_mappling()
        new_enumerators = [
            self.reap_contradictory_ghosts_from_list(e_list)
            for e_list in self.enumeration_parameters
        ]
        new_enumerators = [e_list for e_list in new_enumerators if e_list]
        return MappedTiling(self.tiling, new_avoiders, new_containers, new_enumerators)

    def kill_ghost(self, ghost_number: int):  # BAD
        """removes a ghost from the mapped tiling"""
        new_ghost = self.parameters.pop(ghost_number)
        for i in range(new_ghost.ghost.dimensions[0]):
            for j in range(new_ghost.ghost.dimensions[1]):
                new_ghost.ghost = new_ghost.ghost.add_obstruction(
                    GriddedCayleyPerm(CayleyPermutation([0]), [(i, j)])
                )
        self.parameters.append(new_ghost)

    def remove_redundant_parameters(self, tolerance=REDUNDANCE_TOLERANCE):
        """Removes reduncant parameters from the avoiding parameters, and from each containing parameter list.
        Higher tolerance makes the function check largers GCPS"""
        avoider_comparisons = Parameter.make_comparisons(
            self.avoiding_parameters, self.tiling.dimensions, tolerance
        )
        supersets = set(chain(*avoider_comparisons.values()))
        new_avoiders = [
            self.avoiding_parameters[i]
            for i in range(len(self.avoiding_parameters))
            if i not in supersets
        ]
        new_containers = []
        for c_list in self.containing_parameters:
            container_comparisons = Parameter.make_comparisons(
                c_list, self.tiling.dimensions, tolerance
            )
            new_containers.append(
                [c_list[i] for i in range(len(c_list)) if not container_comparisons[i]]
            )
        return MappedTiling(
            self.tiling, new_avoiders, new_containers, self.enumeration_parameters
        )

    def is_trivial(self, confidence=8):  # TODO: Make this better and based on theory
        return set(self.objects_of_size(confidence)) == set(
            self.tiling.objects_of_size(confidence)
        )

    def avoiders_are_trivial(self):  # cleaner
        for param in self.avoiding_parameters:
            if param.ghost != self.tiling:
                return False
        return True

    def is_contradictory(
        self, confidence=8
    ):  # TODO: Make this better and based on theory and correct #cleaner
        return len(set(self.objects_of_size(confidence))) == 0

    def add_obs_to_param_list(
        self, parameters: List[Parameter], obs: List[GriddedCayleyPerm]
    ):  # param list
        """Adds obstructions to a list of parameters and returns the new list"""
        new_parameters = []
        for parameter in parameters:
            new_parameter = parameter.ghost.add_obstructions(
                parameter.map.preimage_of_obstructions(obs)
            )
            new_parameters.append(Parameter(new_parameter, parameter.map))
        return new_parameters

    def add_obstructions(self, obstructions: List[GriddedCayleyPerm]):  # bad
        """Adds obstructions to the tiling (and corrects the parameters)"""
        new_containing_parameters = []
        for parameter_list in self.containing_parameters:
            new_containing_parameters.append(
                self.add_obs_to_param_list(parameter_list, obstructions)
            )
        new_enumeration_parameters = []
        for parameter_list in self.enumeration_parameters:
            new_enumeration_parameters.append(
                self.add_obs_to_param_list(parameter_list, obstructions)
            )
        return MappedTiling(
            self.tiling.add_obstructions(obstructions),
            self.add_obs_to_param_list(self.avoiding_parameters, obstructions),
            new_containing_parameters,
            new_enumeration_parameters,
        )

    def add_reqs_to_param_list(
        self, parameters: List[Parameter], reqs: List[List[GriddedCayleyPerm]]
    ):  # bad
        """Adds requirements to a list of parameters and returns the new list"""
        new_parameters = []
        for parameter in parameters:
            new_parameter = parameter.ghost.add_requirements(
                parameter.map.preimage_of_requirements(reqs)
            )
            new_parameters.append(Parameter(new_parameter, parameter.map))
        return new_parameters

    def add_requirements_to_tiling(self, requirements):
        new_tiling = self.tiling.add_requirements(requirements)
        return MappedTiling(
            new_tiling,
            self.avoiding_parameters,
            self.containing_parameters,
            self.enumeration_parameters,
        )

    def add_obstructions_to_tiling(self, obstructions):
        new_tiling = self.tiling.add_obstructions(obstructions)
        return MappedTiling(
            new_tiling,
            self.avoiding_parameters,
            self.containing_parameters,
            self.enumeration_parameters,
        )

    def add_requirements(self, requirements: List[List[GriddedCayleyPerm]]):  # Good
        """Adds requirements to the mappling by adding them to each of the
        parameters in all possible ways."""
        new_containing_parameters = []
        for parameter_list in self.containing_parameters:
            new_containing_parameters.append(
                self.add_reqs_to_param_list(parameter_list, requirements)
            )
        new_enumeration_parameters = []
        for parameter_list in self.enumeration_parameters:
            new_enumeration_parameters.append(
                self.add_reqs_to_param_list(parameter_list, requirements)
            )

        return MappedTiling(
            self.tiling.add_requirements(requirements),
            self.add_reqs_to_param_list(self.avoiding_parameters, requirements),
            new_containing_parameters,
            new_enumeration_parameters,
        )

    def add_requirement_list(self, req_list: List[GriddedCayleyPerm]):  # useless
        """Adds a requirement list to the tiling and the parameters."""
        return self.add_requirements([req_list])

    def remove_empty_rows_and_columns(self) -> "MappedTiling":  # Good
        """Finds and removes empty rows and cols in the base tiling then removes the
        corresponding rows and columns in the parameters"""
        empty_cols, empty_rows = self.tiling.find_empty_rows_and_columns()
        if not empty_cols and not empty_rows:
            return self
        if len(empty_cols) == self.tiling.dimensions[0]:
            empty_cols = empty_cols[1:]
        if len(empty_rows) == self.tiling.dimensions[1]:
            empty_rows = empty_rows[1:]
        new_tiling = self.tiling.delete_rows_and_columns(empty_cols, empty_rows)
        new_avoiding_parameters = self.remove_empty_rows_and_cols_from_param_list(
            self.avoiding_parameters, empty_cols, empty_rows
        )
        new_containing_parameters = []
        for parameter_list in self.containing_parameters:
            new_containing_parameters.append(
                self.remove_empty_rows_and_cols_from_param_list(
                    parameter_list, empty_cols, empty_rows
                )
            )
        new_enumeration_parameters = []
        for parameter_list in self.enumeration_parameters:
            new_enumeration_parameters.append(
                self.remove_empty_rows_and_cols_from_param_list(
                    parameter_list, empty_cols, empty_rows
                )
            )
        return MappedTiling(
            new_tiling,
            new_avoiding_parameters,
            new_containing_parameters,
            new_enumeration_parameters,
        )

    def remove_empty_rows_and_cols_from_param_list(
        self, parameters, empty_cols, empty_rows
    ):  # param list cleaner
        """Removes the rows and cols from each ghost in the parameter list then
        returns new parameter list."""
        new_parameters = []
        for P in parameters:
            col_preimages, row_preimages = P.map.preimages_of_cols(
                empty_cols
            ), P.map.preimages_of_rows(empty_rows)
            new_parameter = P.ghost.delete_rows_and_columns(
                col_preimages, row_preimages
            )
            new_map = P.reduce_row_col_map(col_preimages, row_preimages)
            new_parameters.append(Parameter(new_parameter, new_map))
        return new_parameters

    def add_parameters(
        self, avoiding_parameters, containing_parameters, enumeration_parameters
    ):  # main
        return MappedTiling(
            self.tiling,
            self.avoiding_parameters + avoiding_parameters,
            self.containing_parameters + containing_parameters,
            self.enumeration_parameters + enumeration_parameters,
        )

    def all_parameters(self) -> tuple["Parameter", ...]:  # Good
        """Returns a list of all parameters."""
        return (
            self.avoiding_parameters
            + list(chain.from_iterable(self.containing_parameters))
            + list(chain.from_iterable(self.enumeration_parameters))
        )

    @classmethod
    def empty_mappling(cls) -> "MappedTiling":
        return MappedTiling(
            Tiling.empty_tiling(),
            [],
            [],
            [],
        )

    def copy(self):
        return MappedTiling(
            self.tiling,
            self.avoiding_parameters,
            self.containing_parameters,
            self.enumeration_parameters,
        )

    def __eq__(self, other) -> bool:
        return (
            self.tiling == other.tiling
            and sorted(tuple(self.avoiding_parameters))
            == sorted(tuple(other.avoiding_parameters))
            and sorted(tuple(self.containing_parameters))
            == sorted(tuple(other.containing_parameters))
            and sorted(tuple(self.enumeration_parameters))
            == sorted(tuple(other.enumeration_parameters))
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.tiling,
                tuple(sorted(self.avoiding_parameters)),
                tuple(
                    sorted(tuple(sorted(clist)) for clist in self.containing_parameters)
                ),
                tuple(
                    sorted(
                        tuple(sorted(elist)) for elist in self.enumeration_parameters
                    )
                ),
            )
        )

    def from_dict(self, d):
        return MappedTiling(
            Tiling.from_dict(d["tiling"]),
            [Parameter.from_dict(p) for p in d["avoiding_parameters"]],
            [[Parameter.from_dict(p) for p in ps] for ps in d["containing_parameters"]],
            [
                [Parameter.from_dict(p) for p in ps]
                for ps in d["enumeration_parameters"]
            ],
        )

    def are_contradictory_parameters(self):  # cleaner
        """Returns True if there is a contradiction between the avoiding and
        containing parameters - if a len 1 containing parameter list is the
        same as an avoiding parameter."""
        if not self.avoiding_parameters:
            return False
        len_one_cont_params = [
            contain_list
            for contain_list in self.containing_parameters
            if len(contain_list) == 1
        ]
        if not len_one_cont_params:
            return False
        if any(
            contain_list[0] == avoiding_parameter
            for contain_list in len_one_cont_params
            for avoiding_parameter in self.avoiding_parameters
        ):
            return True
        return False

    def is_empty(self) -> bool:
        """Assume this is run after all cleanup functions have been applied.

        Returns True if the tiling is empty or there is a contradiction between
        containing and avoiding parameters.
        TODO: Are there any other times when a mapped tiling is empty?"""
        return self.tiling.is_empty() or self.are_contradictory_parameters()

    def __repr__(self):
        return (
            self.__class__.__name__
            + f"({repr(self.tiling)}, {repr(self.avoiding_parameters)}, "
            + f"{repr(self.containing_parameters)}, {repr(self.enumeration_parameters)})"
        )

    def reduced_str(self):
        """Returns a string representation of the parameter without the
        crossing obs and reqs."""
        return (
            "Base tiling: \n"
            + self.tiling.reduced_str()
            + "\nAvoiding parameters:\n"
            + "\n".join([p.reduced_str() for p in self.avoiding_parameters])
            + "\nContaining parameters:\n"
            + "\nNew containing parameters list \n".join(
                [
                    "\n".join([p.reduced_str() for p in ps])
                    for ps in self.containing_parameters
                ]
            )
            + "\nEnumeration parameters:\n"
            + "\nNew enumeration parameters list\n".join(
                [
                    "\n".join([p.reduced_str() for p in ps])
                    for ps in self.enumeration_parameters
                ]
            )
        )

    def __str__(self) -> str:
        return (
            "Base tiling: \n"
            + str(self.tiling)
            + "\nAvoiding parameters:\n"
            + "\n".join([str(p) for p in self.avoiding_parameters])
            + "\nContaining parameters:\n"
            + "\nNew containing parameters list \n".join(
                ["\n".join([str(p) for p in ps]) for ps in self.containing_parameters]
            )
            + "\nEnumeration parameters:\n"
            + "\nNew enumeration parameters list\n".join(
                ["\n".join([str(p) for p in ps]) for ps in self.enumeration_parameters]
            )
        )
