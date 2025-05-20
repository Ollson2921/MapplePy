"""Module with the cleaner classes"""

from typing import TypeVar, Callable, Generic, Iterable
from itertools import product, chain

from gridded_cayley_permutations import GriddedCayleyPerm, Tiling
from gridded_cayley_permutations.row_col_map import RowColMap
from cayley_permutations import CayleyPermutation

from .parameter import Parameter
from .parameter_list import ParameterList
from .mapped_tiling import MappedTiling

T = TypeVar("T")
Cell = tuple[int, int]


class Register(Generic[T]):
    """Used within cleaners to register core functions.
    Can be initialized with a custom string
    to determine the name of the attribute added to functions
    """

    def __init__(self, attr_name: str = "index"):
        self.registered_functions = set[Callable[[T], T]]()
        self.map = dict[int, Callable[[T], T]]()
        self.attr_name = attr_name

    def __call__(
        self, idx: int, update_register: bool = True
    ) -> Callable[[Callable[[T], T]], Callable[[T], T]]:
        """Used as the decorator to register functions. Setting update_register to False"""

        def register_function(func: Callable[[T], T]) -> Callable[[T], T]:
            if update_register:
                assert idx not in self.map.keys(), " ".join(
                    (
                        self.attr_name,
                        str(idx),
                        "is already assigned to",
                        self[idx].__name__,
                        "and cannot be assigned to",
                        func.__name__,
                    )
                )
                self.registered_functions.add(func)
                self.map[idx] = func
            setattr(func, self.attr_name, idx)

            return func

        return register_function

    def sorting_key(self, func: Callable[[T], T]) -> int:
        """Used to sort fuctions in cleaners"""
        assert hasattr(func, self.attr_name), (
            func.__name__ + " has no assigned " + self.attr_name
        )
        return getattr(func, self.attr_name)

    def __getitem__(self, key: int) -> Callable[[T], T]:
        return self.map[key]

    def __repr__(self):
        return (
            self.attr_name
            + " : "
            + repr({idx: self[idx].__name__ for idx in sorted(self.map)})
        )


class Cleaner(Generic[T]):
    """The class used to clean paramaters.
    Core fuctions are decorated with @reg(index)
    where index is the order of cleaning"""

    reg = Register[T]()

    def __init__(self, todo_list: Iterable[Callable[[T], T]]):
        self.todo_list = tuple(sorted(todo_list, key=self.__class__.reg.sorting_key))

    def __call__(self, cleaning_object: T) -> T:
        """Cleans the input cleaning_object according to the cleaner's todo_list"""
        return self.__class__.list_cleanup(cleaning_object, self.todo_list)

    def __repr__(self):
        return self.__class__.__name__ + repr(
            tuple(func.__name__ for func in self.todo_list)
        )

    @classmethod
    def list_cleanup(
        cls, cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Applies all functions in cleaning_list in order according to their index"""
        cleaning_list = sorted(cleaning_list, key=cls.reg.sorting_key)
        return Cleaner.unordered_cleanup(cleaning_object, cleaning_list)

    @staticmethod
    def unordered_cleanup(
        cleaning_object: T, cleaning_list: Iterable[Callable[[T], T]]
    ) -> T:
        """Applies all functions in cleaning_list without reordering"""
        new_cleaning_object = cleaning_object
        for func in cleaning_list:
            new_cleaning_object = func(new_cleaning_object)
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
        return cls.unordered_cleanup(
            cleaning_object,
            tuple(sorted(cls.reg.registered_functions, key=cls.reg.sorting_key)),
        )


class ParamCleaner(Cleaner[Parameter]):
    """The cleaner for parameters.
    core functions need to be registered with @reg(index)
    where index determines cleaning order"""

    reg = Register[Parameter]("param_register")
    # Final Methods

    @staticmethod
    @reg(3)
    def reduce_by_fusion(param: Parameter) -> Parameter:
        """Fuses valid rows and columns"""
        return ParamCleaner._fuse_valid_rows_or_cols(
            ParamCleaner._fuse_valid_rows_or_cols(param, 0), 1
        )

    @staticmethod
    @reg(1)
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

    @staticmethod
    @reg(0)
    def remove_blank_rows_and_cols(param: Parameter) -> Parameter:
        """Deletes all rows and cols which have no obs or reqs"""
        return param.delete_rows_and_columns(*param.ghost.find_blank_columns_and_rows())

    @staticmethod
    @reg(2, update_register=False)
    def unplace_points(param: Parameter) -> Parameter:
        """Unplaces points wherever possible"""
        points = param.ghost.point_cells()
        new_param = param
        for cell in points:
            new_param = ParamCleaner._unplace_point(new_param, cell)
        return new_param

    # Internal Methods

    @staticmethod
    def _fuse_valid_rows_or_cols(param: Parameter, direction: int) -> Parameter:
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
    def _unplace_point(param: Parameter, cell: Cell) -> Parameter:
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
        intersecting_list = ParamCleaner._find_unplaced_req_list(param, cell)
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
    def _find_unplaced_req_list(
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

        @MTCleaner.reg(6, update_register=False)
        def _clean_parameters(mappling: MappedTiling) -> MappedTiling:
            return mappling.apply_to_all_parameters(param_cleaner)

        return _clean_parameters

    @staticmethod
    @reg(6)
    def fully_clean_parameters(mappling: MappedTiling) -> MappedTiling:
        """Applies all parameter cleanning functions to all parameters"""
        return MTCleaner.clean_parameters(ParamCleaner.make_full_cleaner())(mappling)

    @staticmethod
    @reg(0)
    def try_to_kill(mappling: MappedTiling) -> MappedTiling:
        """Used to decide how to kill mapplings in full_cleanup"""
        raise NotImplementedError

    @staticmethod
    @reg(1)
    def tidy_containers(mappling: MappedTiling) -> MappedTiling:
        """For parameters with empty tilings, if it is the only
        one in a list then the mappling is empty, otherwise remove the empty
        parameter.
        If only one parameter in a list and it maps to base tiling by the identity map
        then map obs and reqs down and remove the parameter list.
        Note: As we always assume a parameter maps to the whole tiling, we defined a row
        col map as being trivial iff the dimensions of the tiling and ghost are the same.
        """
        raise NotImplementedError

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
        return MappedTiling(
            mappling.tiling,
            mappling.avoiding_parameters,
            new_containers,
            mappling.enumerating_parameters,
        )

    @staticmethod
    @reg(2)
    def insert_valid_avoiders(mappling: MappedTiling) -> MappedTiling:
        """Adds requirements from every avoider that is near-trivial and removes that avoider"""
        raise NotImplementedError

    @staticmethod
    @reg(4)
    def backmap_points(mappling: MappedTiling) -> MappedTiling:
        """Backmaps point obstructions to all parameters"""
        point_obstructions = (ob for ob in mappling.obstructions if len(ob) == 1)
        return mappling.apply_to_all_parameters(
            Parameter.backmap_obstructions, (point_obstructions,)
        )

    @staticmethod
    @reg(3)
    def reap_all_contradictions(mappling: MappedTiling) -> MappedTiling:
        """Removes any contradictory parameters"""
        raise NotImplementedError

    @staticmethod
    @reg(5)
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
    @reg(8)
    def reduce_redundant_parameters(mappling: MappedTiling) -> MappedTiling:
        """Removes any parameter implied by another"""
        raise NotImplementedError

    # Internal Methods

    @staticmethod
    def _find_intersection(container_list: ParameterList) -> Iterable[ParameterList]:
        """Returns the intersection of the factors of the container list"""
        if len(container_list) == 1:
            return [ParameterList([factor]) for factor in tuple(container_list)[0].factor()]
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
