"""Module with the cleaner classes"""

from typing import TypeVar, Callable, Generic, Iterable
from itertools import chain
from functools import partial
from time import time

from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from gridded_cayley_permutations.row_col_map import RowColMap
from gridded_cayley_permutations.simplify_obstructions_and_requirements import (
    SimplifyObstructionsAndRequirements,
)
from gridded_cayley_permutations.simplify_obstructions_and_requirements import (
    SimplifyObstructionsAndRequirements,
)
from cayley_permutations import CayleyPermutation

from .parameter import Parameter
from .parameter_list import ParameterList
from .mapped_tiling import MappedTiling

T = TypeVar("T", MappedTiling, Parameter)
Cell = tuple[int, int]

DEBUG = False


class Register(Generic[T]):
    """Used within cleaners to register core functions.
    Initialize with a string to determine the name of the index attribute added to functions.
    Initialize with flag_name = bool to make flag_name an attribute of all registered functions.
    """

    def __init__(self, attr_name: str = "index", **additional_flags: bool):
        self.registered_functions: set[Callable[[T], T]] = set()
        self.map: dict[int, Callable[[T], T]] = {}
        self.flags = dict(additional_flags)
        self.attr_name = attr_name

    def __call__(
        self, idx: int, update_register: bool = True, **flag_updates: bool
    ) -> Callable[[Callable[[T], T]], Callable[[T], T]]:
        """Used as the decorator to register functions.
        Setting update_register to False doesn't add the function to registered functions
        Flag updates will overwrite the register's default flag states."""

        def register_function(func: Callable[[T], T]) -> Callable[[T], T]:
            if update_register:
                self.add_to_register(func, idx)
            setattr(func, self.attr_name, idx)
            return self.set_flags(func, flag_updates)

        return register_function

    def add_to_register(self, func: Callable[[T], T], idx: int) -> None:
        """Used to add functions to the register"""
        assert idx not in self.map, (
            f"{self.attr_name} {idx} is already assigned to {self[idx].__qualname__} "
            + f"and cannot be assigned to {func.__qualname__}"
        )
        self.registered_functions.add(func)
        self.map[idx] = func

    def set_flags(self, func: Callable[[T], T], flag_updates: dict[str, bool]):
        """Adds all registered flags as attributes to func.
        Default flag values are overwritten by flag updates."""
        known_flags = tuple(self.flags.keys())
        adjusted_dict = self.flags.copy()
        for key, value in flag_updates.items():
            assert key in known_flags, (
                f"Unknown Flag : {key} \n."
                + f"{func.__qualname__} can be registered with the following flags : {known_flags}"
            )
            adjusted_dict[key] = value
        func.__dict__.update(adjusted_dict)
        return func

    def sorting_key(self, func: Callable[[T], T]) -> int:
        """Used to sort fuctions in cleaners"""
        assert hasattr(
            func, self.attr_name
        ), f"{func.__qualname__} has no assigned {self.attr_name}"
        return getattr(func, self.attr_name)

    def __getitem__(self, key: int) -> Callable[[T], T]:
        return self.map[key]

    def __repr__(self):
        output = f"{self.__class__.__name__}(attr_name={self.attr_name}"
        for key, value in self.flags.items():
            output += f", {key}={value}"
        return output + ")"

    def __str__(self):
        funcs = sorted(self.registered_functions, key=self.sorting_key)
        output = f"{funcs[0].__qualname__.split('.')[0]} has registered the following functions:"
        for func in funcs:
            output += f"\n{getattr(func, self.attr_name)} : {func.__name__}"
            for key, value in tuple(func.__dict__.items())[1:]:
                output += f"\n    -{key}={value}"
            output += "\n"
        return output


def debug(func: Callable[[T], T], run: bool = DEBUG):
    """Sets the debug behavior for cleaning functions."""
    if run:

        def wrapper(clening_object: T) -> T:
            old_object = clening_object
            start_time = time()
            new_object = func(old_object)
            elapsed_time = start_time - time()
            print(f"{func.__name__} elapsed time : {elapsed_time}")
            if hasattr(clening_object, "initial_conditions"):
                old_counts = old_object.initial_conditions()
                new_counts = new_object.initial_conditions()
                assert (
                    old_counts == new_counts
                ), f"Counts differ after running {func.__name__}"
            return new_object

        return wrapper
    return func


class Cleaner(Generic[T]):
    """The class used to clean paramaters.
    Core fuctions are decorated with @reg(index)
    where index is the order of cleaning"""

    reg = Register[T]()

    def __init__(self, todo_list: Iterable[Callable[[T], T]]):
        self.todo_list: tuple[Callable[[T], T], ...] = tuple(
            sorted(todo_list, key=self.__class__.reg.sorting_key)
        )

    def __call__(self, cleaning_object: T) -> T:
        """Cleans the input cleaning_object according to the cleaner's todo_list"""
        return self.__class__.loop_cleanup(cleaning_object, self.todo_list)

    def __repr__(self):
        return self.__class__.__name__ + f"({self.todo_list})"
   
    def __str__(self):
        return (
            self.__class__.__name__
            + f"({dict((self.reg.sorting_key(func) , func.__name__) for func in self.todo_list)})"
        )

    def __iter__(self):
        return iter(sorted(self.todo_list, key=self.reg.sorting_key))

    @classmethod
    def loop_cleanup(
        cls, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Cleans the cleaning object according to the cleaning functions."""
        new_cleaning_object = cleaning_object
        continue_cleaning = True
        while continue_cleaning:
            old_cleaning_object = new_cleaning_object
            new_cleaning_object = cls.list_cleanup(old_cleaning_object, cleaning_list)
            continue_cleaning = old_cleaning_object != new_cleaning_object
        return new_cleaning_object

    @classmethod
    def list_cleanup(
        cls, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Applies all functions in cleaning_list in order according to their index"""
        cleaning_list = sorted(cleaning_list, key=cls.reg.sorting_key)
        return Cleaner.unordered_cleanup(cleaning_object, cleaning_list)

    @classmethod
    def unordered_cleanup(
        cls, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Applies all functions in cleaning_list without reordering"""
        new_cleaning_object = cleaning_object
        for func in cleaning_list:
            if not bool(new_cleaning_object):
                return new_cleaning_object
            new_cleaning_object = debug(func)(new_cleaning_object)
        return new_cleaning_object

    def tracked_cleanup(
        self, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Cleans cleaning_object according to the cleaning list,
        removes any completed cleaning functions from the cleaner's todo_list"""
        new_cleaning_object = self.list_cleanup(cleaning_object, cleaning_list)
        self.todo_list = tuple(set(self.todo_list) - set(cleaning_list))
        return new_cleaning_object

    @classmethod
    def make_full_cleaner(cls):
        """Returns an instance of a cleaner with all registered cleaning functions"""
        return cls(tuple(sorted(cls.reg.registered_functions, key=cls.reg.sorting_key)))

    @classmethod
    def full_cleanup(cls, cleaning_object: T) -> T:
        """Applies all cleanup functions."""
        return cls.make_full_cleaner()(cleaning_object)


class ParamCleaner(Cleaner[Parameter]):
    """The cleaner for parameters.
    core functions need to be registered with @reg(index)
    where index determines cleaning order"""

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
    @reg(1)
    def reduce_empty_rows_and_cols(param: Parameter) -> Parameter:
        """Removes empty rows and columns in the parameter"""
        empty_cols, empty_rows = map(set, param.ghost.find_empty_rows_and_columns())
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
    @reg(0, run_on_enumerators=False)
    def remove_blank_rows_and_cols(param: Parameter) -> Parameter:
        """Deletes all rows and cols which have no obs or reqs"""
        return param.delete_rows_and_columns(*param.ghost.find_blank_columns_and_rows())

    @staticmethod
    @reg(2, update_register=False, run_on_enumerators=False)
    def unplace_points(param: Parameter) -> Parameter:
        """Unplaces points wherever possible"""
        raise NotImplementedError

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


class MTCleaner(Cleaner[MappedTiling]):
    """The cleaner for mapped tilings.
    core functions need to be registered with @reg(index)
    where index determines cleaning order"""

    reg = Register[MappedTiling]("mappling_register")

    # Final Methods
    @staticmethod
    def clean_parameters(
        param_cleaner: ParamCleaner,
    ) -> Callable[[MappedTiling], MappedTiling]:
        """Creates a function (index = 6) that applies a param cleaner to all parameters.
        Must be called to use in list cleanup
        To apply to a mappling, can be run as MTCleaner.make_param_cleaner(param_cleaner)(mappling)
        """

        @MTCleaner.reg(5, update_register=False)
        def _clean_parameters(mappling: MappedTiling) -> MappedTiling:
            new_avoiders, new_containers, new_enumerators = mappling.ace_parameters()
            for func in param_cleaner:
                if getattr(func, "run_on_avoiders"):
                    new_avoiders = ParameterList(new_avoiders.apply_to_all(func))
                if getattr(func, "run_on_containers"):
                    new_containers = [
                        ParameterList(c_list.apply_to_all(func))
                        for c_list in new_containers
                    ]
                if getattr(func, "run_on_containers"):
                    new_enumerators = [
                        ParameterList(e_list.apply_to_all(func))
                        for e_list in new_enumerators
                    ]
            return MappedTiling(
                mappling.tiling, new_avoiders, new_containers, new_enumerators
            )

        return _clean_parameters

    @staticmethod
    @reg(5)
    def fully_clean_parameters(mappling: MappedTiling) -> MappedTiling:
        """Applies all parameter cleanning functions to all parameters"""
        return MTCleaner.clean_parameters(ParamCleaner.make_full_cleaner())(mappling)

    @staticmethod
    @reg(0)
    def try_to_kill(mappling: MappedTiling) -> MappedTiling:
        """Used to decide how to kill mapplings in full_cleanup"""
        if mappling.is_empty():
            return MappedTiling.empty_mappling()
        if not mappling.tiling.active_cells:
            return MappedTiling(
                Tiling(
                    [GriddedCayleyPerm(CayleyPermutation((0,)), ((0, 0),))], [], (1, 1)
                ),
                [],
                [],
                [],
            )
        return mappling

    @staticmethod
    @reg(7)
    def factor_containters(mappling: MappedTiling) -> MappedTiling:
        """Factors out the intersection factors of a containing parameter list"""
        new_containers = list(
            chain(
                *(
                    MTCleaner._find_intersection(c_list)
                    for c_list in mappling.containing_parameters
                )
            )
        )
        new_mappling = MappedTiling(
            mappling.tiling,
            mappling.avoiding_parameters,
            new_containers,
            mappling.enumerating_parameters,
        )
        return MTCleaner.list_cleanup(
            new_mappling,
            (MTCleaner.reap_all_contradictions, MTCleaner.reduce_all_parameter_gcps),
        )

    @staticmethod
    @reg(9, update_register=False)
    def backmap_points(mappling: MappedTiling) -> MappedTiling:
        """Backmaps point obstructions to all parameters"""
        point_obstructions = (ob for ob in mappling.obstructions if len(ob) == 1)
        return mappling.apply_to_all_parameters(
            Parameter.backmap_obstructions, (point_obstructions,)
        )

    @staticmethod
    @reg(1)
    def reap_all_contradictions(mappling: MappedTiling) -> MappedTiling:
        """Removes any contradictory parameters
        and kills the mappling if all containers in a c-list are contradictory"""
        base = mappling.tiling
        new_containers = []
        for c_list in mappling.containing_parameters:
            if not c_list:
                continue
            new_c_list = c_list.remove_contradictions(base)
            if not new_c_list:
                return MappedTiling.empty_mappling()
            new_containers.append(new_c_list)
        new_avoiders = mappling.avoiding_parameters.remove_contradictions(base)
        new_enumerators = []
        for e_list in mappling.enumerating_parameters:
            new_e_list = e_list.remove_contradictions(base)
            if new_e_list:
                new_enumerators.append(e_list)
        return MappedTiling(
            mappling.tiling, new_avoiders, new_containers, new_enumerators
        )

    @staticmethod
    @reg(2)
    def remove_empty_rows_and_cols(mappling: MappedTiling) -> MappedTiling:
        """Removes empty rows and cols in the base tiling and removes
        preimage rows and cols from the parameters"""
        empty_cols, empty_rows = mappling.tiling.find_empty_rows_and_columns()
        if (
            len(empty_cols) == mappling.dimensions[0]
            or len(empty_rows) == mappling.dimensions[1]
        ):
            return MappedTiling(
                Tiling(
                    [GriddedCayleyPerm(CayleyPermutation((0,)), [(0, 0)])], [], (1, 1)
                ),
                ParameterList([]),
                [],
                [],
            )
        mappling.tiling = mappling.tiling.delete_rows_and_columns(
            empty_cols, empty_rows
        )
        return mappling.apply_to_all_parameters(
            Parameter.delete_preimage_of_rows_and_columns, (empty_cols, empty_rows)
        )

    @staticmethod
    @reg(10)
    def simple_reduce_redundant_parameters(mappling: MappedTiling) -> MappedTiling:
        """Removes any parameter implied by another with a basic check"""
        new_avoiders = mappling.avoiding_parameters.simple_remove_redundant()
        new_containers = [
            c_list.simple_remove_redundant(True)
            for c_list in mappling.containing_parameters
        ]
        return MappedTiling(
            mappling.tiling,
            new_avoiders,
            new_containers,
            mappling.enumerating_parameters,
        )

    @staticmethod
    @reg(3)
    def reduce_all_parameter_gcps(mappling: MappedTiling) -> MappedTiling:
        """Removes all obs and reqs that are implied by the base tiling from all Parameters"""
        param_reducer = partial(MTCleaner._reduce_parameter_gcps, mappling)
        return mappling.apply_to_all_parameters(param_reducer)

    @staticmethod
    @reg(4)
    def reap_blank(mappling: MappedTiling) -> MappedTiling:
        """Kills mappling if any avoiders are blank,
        and removes any c_lists with blank containers"""
        if any(
            not (param.ghost.not_blank_cells())
            for param in mappling.avoiding_parameters
        ):
            return MappedTiling.empty_mappling()
        new_containeres = []
        for c_list in mappling.containing_parameters:
            if any(not (param.ghost.not_blank_cells()) for param in c_list):
                continue
            new_containeres.append(c_list)
        return MappedTiling(
            mappling.tiling,
            mappling.avoiding_parameters,
            new_containeres,
            mappling.enumerating_parameters,
        )

    @staticmethod
    @reg(8)
    def insert_containers(mappling: MappedTiling) -> MappedTiling:
        """For parameters with empty tilings, if it is the only
        one in a list then the mappling is empty, otherwise remove the empty
        parameter.
        If only one parameter in a list and it maps to base tiling by the identity map
        then map obs and reqs down and remove the parameter list.
        Note: As we always assume a parameter maps to the whole tiling, we defined a row
        col map as being trivial iff the dimensions of the tiling and ghost are the same.
        """
        new_containers = []
        new_tiling = mappling.tiling
        for c_list in mappling.containing_parameters:
            if len(c_list) == 1:
                container = tuple(c_list)[0]
                image_cols, image_rows = container.map.image_rows_and_cols()
                if container.dimensions[0] == len(image_cols) and container.dimensions[
                    1
                ] == len(image_rows):
                    new_tiling = MTCleaner._insert_param(new_tiling, container)
                    continue
            new_containers.append(c_list)
        return MappedTiling(
            new_tiling,
            mappling.avoiding_parameters,
            new_containers,
            mappling.enumerating_parameters,
        )

    @staticmethod
    @reg(6)
    def insert_avoiders(mappling: MappedTiling) -> MappedTiling:
        """Adds requirements from every avoider that is near-trivial and removes that avoider"""
        new_avoiders = []
        new_tiling = mappling.tiling
        for avoider in mappling.avoiding_parameters:
            image_cols, image_rows = avoider.map.image_rows_and_cols()
            if avoider.dimensions[0] == len(image_cols) and avoider.dimensions[
                1
            ] == len(image_rows):
                reqs = avoider.requirements
                if reqs:
                    if max(len(req) for req in reqs) > 1:
                        new_avoiders.append(avoider)
                        continue
                inverse = Parameter(
                    Tiling(chain(*reqs), [avoider.obstructions], avoider.dimensions),
                    avoider.map,
                )
                new_tiling = MTCleaner._insert_param(new_tiling, inverse)
                continue
            new_avoiders.append(avoider)
        return MappedTiling(
            new_tiling,
            new_avoiders,
            mappling.containing_parameters,
            mappling.enumerating_parameters,
        )

    # Internal Methods

    @staticmethod
    def _insert_param(tiling: Tiling, param: Parameter) -> Tiling:
        return tiling.add_obstructions(
            param.map.map_gridded_cperms(param.obstructions)
        ).add_requirements(param.map.map_requirements(param.requirements))

    @staticmethod
    def _reduce_parameter_gcps(mappling: MappedTiling, param: Parameter) -> Parameter:
        """Removes all obs and reqs from param that are implied by mappling"""
        simplify = SimplifyObstructionsAndRequirements(
            mappling.obstructions, mappling.requirements, mappling.dimensions
        )
        new_obs = []
        new_reqs = []
        for ob in param.obstructions:
            if any(
                param.map.map_gridded_cperm(ob).contains_gridded_cperm(mt_ob)
                for mt_ob in mappling.obstructions
            ):
                continue
            new_obs.append(ob)
        for req_list in param.requirements:
            new_req_list = [
                req
                for req in req_list
                if not simplify.implied_by_requirements(
                    param.map.map_gridded_cperm(req)
                )
            ]
            if new_req_list:
                new_reqs.append(tuple(new_req_list))
        new_ghost = Tiling(new_obs, new_reqs, param.dimensions, simplify=False)
        return Parameter(new_ghost, param.map)

    @staticmethod
    def _find_intersection(container_list: ParameterList) -> Iterable[ParameterList]:
        """Returns the intersection of the factors of the container list"""
        if len(container_list) == 1:
            return [
                ParameterList([factor]) for factor in tuple(container_list)[0].factor()
            ]
        all_factors = tuple(map(set, container_list.apply_to_all(Parameter.factor)))
        intersection = all_factors[0]
        for factors in all_factors:
            intersection = intersection & factors
            if not intersection:
                return [
                    container_list,
                ]
        image_cells = set(chain(*(factor.image_cells() for factor in intersection)))
        new_param_list = ParameterList([])
        for param in container_list:
            keep_cells = param.map.preimage_of_cells(param.image_cells() - image_cells)
            new_param_list.add(param.sub_parameter(keep_cells))
        return [new_param_list] + [ParameterList([factor]) for factor in intersection]
